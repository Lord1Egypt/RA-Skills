#!/usr/bin/env python3
"""Tests du moteur (déterministes, sans fichiers). Lancer : python3 scripts/test_reconcile.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from normalize import (classify_non_billable, extract_invoice_ref,
                       name_similarity, parse_date, parse_money)
from reconcile import reconcile

T = {"passed": 0, "failed": 0}


def check(name, cond):
    if cond:
        T["passed"] += 1
    else:
        T["failed"] += 1
        print(f"  FAIL: {name}")


# --------------------------------------------------------------------------- #
# Helpers de normalisation                                                     #
# --------------------------------------------------------------------------- #
def test_helpers():
    check("money fr", parse_money("1 234,56") == 1234.56)
    check("money us", parse_money("1,234.56") == 1234.56)
    check("money int", parse_money("3600") == 3600.0)
    check("money 1dec", parse_money("1847,2") == 1847.2)
    check("money neg", parse_money("-742,50") == -742.50)
    check("money thousands fr", parse_money("12.500,00") == 12500.0)
    check("date fr", parse_date("09/04/2026") == "2026-04-09")
    check("date iso", parse_date("2026-04-09") == "2026-04-09")
    check("ref marked", extract_invoice_ref("VIR REF AQ-2026-041 ACME") == "AQ-2026-041")
    check("ref glued", extract_invoice_ref("PRLV FAC-2024-012") == "FAC-2024-012")
    check("ref none on sepa", extract_invoice_ref("PRLV SEPA ICS FR12ZZZ") is None)
    check("name sim high", name_similarity("Aquatech Fournitures", "VIR AQUATECH FOURNIT") > 0.6)
    check("name sim low", name_similarity("Aquatech", "Boulangerie Martin") < 0.4)
    check("nb salaire", classify_non_billable("VIR SALAIRE M ROSSI") == "rh_charges")
    check("nb urssaf", classify_non_billable("PRLV URSSAF CORSE") == "prestations_sociales")
    check("nb impot", classify_non_billable("PRLV DGFIP IMPOT SOCIETES") == "impots_taxes")
    check("nb frais", classify_non_billable("FRAIS BANCAIRES TENUE DE COMPTE") == "frais_bancaires")
    check("nb retrait", classify_non_billable("RETRAIT DAB AJACCIO") == "especes")
    check("facturable non exclu", classify_non_billable("PRLV AQUATECH FOURNITURES") is None)
    check("edf facturable", classify_non_billable("PRLV EDF ELECTRICITE") is None)


# --------------------------------------------------------------------------- #
# Scénario complet                                                             #
# --------------------------------------------------------------------------- #
def scenario():
    invoices = [
        # vente (out) encaissée par un crédit, référencée
        {"invoice_id": "FV-2026-001", "type": "out", "counterparty_name": "Hotel Alba Rossa",
         "amount": 1980.00, "issued_date": "2026-04-02", "due_date": "2026-04-30", "confidence": 1.0},
        # achat (in) réglé par un débit, fuzzy (libellé + date)
        {"invoice_id": "AQ-2026-041", "type": "in", "counterparty_name": "Aquatech Fournitures",
         "amount": 742.50, "issued_date": "2026-04-09", "due_date": "2026-05-09", "confidence": 1.0},
        # vente (out) NON payée, échéance dépassée -> overdue + relance
        {"invoice_id": "FV-2026-002", "type": "out", "counterparty_name": "Garage Petrus",
         "amount": 540.00, "issued_date": "2026-04-15", "due_date": "2026-04-20", "confidence": 1.0},
        # achat (in) payé partiellement (acompte)
        {"invoice_id": "AC-2026-077", "type": "in", "counterparty_name": "Materiaux Sud",
         "amount": 2000.00, "issued_date": "2026-04-05", "due_date": "2026-05-05", "confidence": 1.0,
         "total_ht": 1666.67, "tva_amount": 333.33, "tva_rate_pct": 20},
    ]
    statements = [{
        "source": "csv", "reconciled": True,
        "transactions": [
            {"date": "2026-04-08", "amount": 1980.00, "label": "VIR CLIENT HOTEL ALBA ROSSA REF FV-2026-001", "invoice_ref": "FV-2026-001"},
            {"date": "2026-04-12", "amount": -742.50, "label": "PRLV AQUATECH FOURNITURES", "invoice_ref": None},
            {"date": "2026-04-10", "amount": -800.00, "label": "VIR MATERIAUX SUD ACOMPTE", "invoice_ref": None},
            # débit sans facture -> facture_manquante
            {"date": "2026-04-18", "amount": -350.00, "label": "PRLV EDF ELECTRICITE", "invoice_ref": None},
            # crédit non identifié -> paiement_orphelin
            {"date": "2026-04-22", "amount": 1200.00, "label": "VIR RECU PARTICULIER", "invoice_ref": None},
            # NON facturables -> excluded_bank_lines (jamais facture_manquante)
            {"date": "2026-04-28", "amount": -2500.00, "label": "VIR SALAIRE M ROSSI", "invoice_ref": None},
            {"date": "2026-04-15", "amount": -890.00, "label": "PRLV URSSAF CORSE", "invoice_ref": None},
            {"date": "2026-04-20", "amount": -200.00, "label": "RETRAIT DAB AJACCIO", "invoice_ref": None},
        ],
    }]
    return invoices, statements


def test_scenario():
    invoices, statements = scenario()
    res = reconcile(invoices, statements, today="2026-05-15")
    periods = {p["period"]: p for p in res["periods"]}
    check("période 2026-04 existe", "2026-04" in periods)
    p = periods["2026-04"]

    inv = {i["invoice_id"]: i for i in p["invoices"]}
    check("FV-001 payée par référence", inv["FV-2026-001"]["status"] == "paid" and inv["FV-2026-001"]["bank_matched"])
    check("AQ-041 réglée fuzzy", inv["AQ-2026-041"]["bank_matched"] and inv["AQ-2026-041"]["status"] == "paid")
    check("FV-002 overdue", inv["FV-2026-002"]["status"] == "overdue" and not inv["FV-2026-002"]["bank_matched"])
    check("AC-077 partielle", inv["AC-2026-077"]["status"] == "partial"
          and inv["AC-2026-077"]["amount_remaining"] == 1200.0)

    types = sorted(l["type"] for l in p["unmatched_bank_lines"])
    check("1 facture_manquante + 1 paiement_orphelin", types == ["facture_manquante", "paiement_orphelin"])
    fm = next(l for l in p["unmatched_bank_lines"] if l["type"] == "facture_manquante")
    check("facture_manquante = débit (négatif)", fm["amount"] < 0)
    po = next(l for l in p["unmatched_bank_lines"] if l["type"] == "paiement_orphelin")
    check("paiement_orphelin = crédit (positif)", po["amount"] > 0)

    # NON facturables -> excluded_bank_lines, jamais en facture_manquante
    cats = sorted(l["category"] for l in p["excluded_bank_lines"])
    check("3 lignes exclues", len(p["excluded_bank_lines"]) == 3)
    check("catégories exclues correctes", cats == ["especes", "prestations_sociales", "rh_charges"])
    check("salaire non compté en facture_manquante",
          not any("SALAIRE" in l["label"] for l in p["unmatched_bank_lines"]))

    # relance générée pour l'overdue
    check("relance overdue", any(r["invoice_id"] == "FV-2026-002" for r in p["relances"]))

    # INVARIANT (3 termes : rappr + unmatched + excluded == count)
    sc = {s["period"]: s for s in res["selfcheck"]}["2026-04"]
    check("invariant rappr+unmat+exclu==count",
          sc["somme"] == sc["bank_transactions_count"] and sc["ok"])
    check("count = 8 transactions", sc["bank_transactions_count"] == 8)
    check("matched = 3 transactions", sc["matched"] == 3)
    check("excluded = 3 transactions", sc["excluded"] == 3)


def test_tva_anomaly():
    invoices = [{"invoice_id": "X1", "type": "in", "counterparty_name": "Z", "amount": 1200,
                 "issued_date": "2026-04-01", "due_date": "2026-05-01", "confidence": 1.0,
                 "total_ht": 1000, "tva_amount": 250, "tva_rate_pct": 20}]  # attendu 200, déclaré 250
    res = reconcile(invoices, [], today="2026-04-15")
    inv = res["periods"][0]["invoices"][0]
    check("tva_incorrecte détectée", any(a["type"] == "tva_incorrecte" for a in inv["anomalies"]))


def test_no_match_amount_alone():
    # même montant mais libellé étranger ET hors fenêtre date -> ne doit PAS matcher
    invoices = [{"invoice_id": "Y1", "type": "out", "counterparty_name": "Boulangerie Martin",
                 "amount": 500.00, "issued_date": "2026-01-01", "due_date": "2026-01-31", "confidence": 1.0}]
    statements = [{"source": "csv", "transactions": [
        {"date": "2026-06-30", "amount": 500.00, "label": "VIR INCONNU XYZ", "invoice_ref": None}]}]
    res = reconcile(invoices, statements, today="2026-07-15")
    matched = any(i["bank_matched"] for pr in res["periods"] for i in pr["invoices"])
    check("montant seul ne matche pas", not matched)
    # la transaction non rapprochée doit tout de même être comptée (invariant)
    check("invariant tenu malgré non-match", all(s["ok"] for s in res["selfcheck"]))


if __name__ == "__main__":
    test_helpers()
    test_scenario()
    test_tva_anomaly()
    test_no_match_amount_alone()
    print(f"\n{T['passed']} passed, {T['failed']} failed")
    raise SystemExit(1 if T["failed"] else 0)
