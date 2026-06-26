#!/usr/bin/env python3
"""Test bout-en-bout : copie les fixtures dans un sandbox temporaire et lance main.py.

Vérifie : le fast-path structuré (UBL/CII/CAMT/CSV), la consommation d'un sidecar LLM
(photo de ticket), l'invariant par période, et la boucle worklist quand un sidecar manque.
Lancer : python3 scripts/test_e2e.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
FIXTURE = SKILL / "fixtures" / "demo-corse-plomberie"
T = {"passed": 0, "failed": 0}


def check(name, cond):
    T["passed" if cond else "failed"] += 1
    if not cond:
        print(f"  FAIL: {name}")


def run_main(root, *extra):
    return subprocess.run([sys.executable, str(HERE / "main.py"), str(root), *extra],
                          capture_output=True, text=True)


def main():
    tmp = Path(tempfile.mkdtemp())
    try:
        root = tmp / "clients-test"
        shutil.copytree(FIXTURE, root / "demo-corse-plomberie")

        # --- Run complet (tous les sidecars présents) ---
        r = run_main(root, "--today", "2026-05-15")
        check("exit 0", r.returncode == 0)
        check("auto-contrôle affiché", "AUTO-CONTRÔLE" in r.stdout)
        check("aucune période KO", "KO" not in r.stdout)

        rapp = json.loads((root / "demo-corse-plomberie" / "rapprochement.json").read_text())
        periods = {p["period"]: p for p in rapp["periods"]}
        check("période 2026-04 présente", "2026-04" in periods)
        check("période 2026-03 présente (CAMT)", "2026-03" in periods)

        p4 = periods["2026-04"]
        check("2026-04 : 7 transactions", p4["bank_transactions_count"] == 7)
        ex_cats = sorted(l["category"] for l in p4["excluded_bank_lines"])
        # Moteur PARTAGÉ ⑤ (politique conservatrice unique) : salaire ET URSSAF →
        # rh_charges (charges sur salaires). prestations_sociales est réservé aux
        # prestations REÇUES (CAF/CPAM/MSA/allocations), pas aux cotisations.
        check("2026-04 exclus = [rh_charges, rh_charges] (salaire + URSSAF)",
              ex_cats == ["rh_charges", "rh_charges"])
        inv = {i["invoice_id"]: i for i in p4["invoices"]}
        check("vente UBL rapprochée (réf)", inv.get("FV-2026-001", {}).get("status") == "paid")
        check("achat CII rapproché (fuzzy)", inv.get("AQ-2026-041", {}).get("status") == "paid")
        check("ticket photo (sidecar LLM) rapproché", inv.get("TIC-2026-0411", {}).get("status") == "paid")
        check("type ticket = in", inv.get("TIC-2026-0411", {}).get("type") == "in")
        check("type vente UBL = out", inv.get("FV-2026-001", {}).get("type") == "out")
        check("contrepartie CII = fournisseur", inv.get("AQ-2026-041", {}).get("counterparty_name") == "Aquatech Fournitures")

        types = sorted(l["type"] for l in p4["unmatched_bank_lines"])
        check("2026-04 unmatched = [facture_manquante, paiement_orphelin]",
              types == ["facture_manquante", "paiement_orphelin"])

        p3 = periods["2026-03"]
        check("2026-03 : 1 transaction CAMT", p3["bank_transactions_count"] == 1)
        check("frais bancaires -> excluded (frais_bancaires)",
              len(p3["unmatched_bank_lines"]) == 0
              and p3["excluded_bank_lines"][0]["category"] == "frais_bancaires"
              and p3["excluded_bank_lines"][0]["amount"] < 0)

        # invariant global (3 termes : matched + unmatched + excluded == count)
        invariants_ok = all(
            p["bank_transactions_count"] ==
            _matched_tx_in_period(p) + len(p["unmatched_bank_lines"]) + len(p["excluded_bank_lines"])
            for p in rapp["periods"]
        )
        check("invariant tx-level (matched+unmatched+excluded==count)", invariants_ok)

        # validation humaine : la vente à 1980 € (> seuil 1000) doit être signalée
        review = json.loads((root / "demo-corse-plomberie" / "_review.json").read_text())
        ids = {x.get("invoice_id") for x in review["needs_human_review"]}
        check("validation humaine sur montant > seuil", "FV-2026-001" in ids)

        # company.json conservé
        comp = json.loads((root / "demo-corse-plomberie" / "company.json").read_text())
        check("company.json conservé", comp.get("siren") == "812345678")

        # --- Boucle worklist : on retire le sidecar du ticket ---
        side = root / "demo-corse-plomberie" / "invoices" / "ticket-brico.png.invoice.json"
        side.unlink()
        r2 = run_main(root, "--today", "2026-05-15")
        check("worklist annoncée", "EXTRACTION LLM REQUISE" in r2.stdout)
        check("ticket listé dans la worklist", "ticket-brico.png" in r2.stdout)
        wl = json.loads((root / "_worklist.json").read_text())
        check("worklist json non vide", len(wl["items"]) >= 1)
        check("mode vision pour la photo",
              any(i["mode"] == "vision" and "ticket-brico" in i["path"] for i in wl["items"]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"\n{T['passed']} passed, {T['failed']} failed")
    return 1 if T["failed"] else 0


def _matched_tx_in_period(period):
    # nb de transactions consommées = count - unmatched - excluded
    return (period["bank_transactions_count"]
            - len(period["unmatched_bank_lines"])
            - len(period["excluded_bank_lines"]))


if __name__ == "__main__":
    raise SystemExit(main())
