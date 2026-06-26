#!/usr/bin/env python3
"""
Analyse d'UNE pièce comptable isolée (facture ou relevé bancaire).

S'appuie sur extract.py (même dossier) pour l'extraction déterministe des
champs, puis ajoute des contrôles de cohérence qui ont un sens sur une pièce
seule — sans aucun accès au reste du dossier client, sans rien déplacer.

Usage :
  python3 analyse.py <fichier.pdf> [--date-ref AAAA-MM-JJ]

Sortie : un objet JSON sur stdout.

  {
    "kind": "invoice | bank-statement | other",
    "text_found": true,            # false = PDF sans couche texte (scan/photo)
    "confidence": "haute | moyenne | faible",
    "fields": { ... sortie brute d'extract.py ... },
    "checks": [
      {"code": "...", "severity": "bloquant | alerte | info", "detail": "..."}
    ]
  }

Aucun champ n'est inventé : si extract.py renvoie null, le contrôle le signale
comme champ manquant plutôt que de combler le vide.
"""

import json
import sys
from datetime import date, datetime

import extract  # même dossier


# ── Helpers ───────────────────────────────────────────────────────────────

def _to_date(iso):
    try:
        return datetime.strptime(iso, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def _iban_valid(iban):
    """Validation IBAN par mod 97 (norme ISO 13616)."""
    if not iban:
        return None  # rien à valider
    s = iban.replace(" ", "").upper()
    if len(s) < 15 or not s[:2].isalpha():
        return False
    rearranged = s[4:] + s[:4]
    digits = "".join(str(int(c, 36)) for c in rearranged)
    try:
        return int(digits) % 97 == 1
    except ValueError:
        return False


# ── Contrôles facture ─────────────────────────────────────────────────────

INVOICE_REQUIRED = {
    "invoice_id": "numéro de facture",
    "issue_date": "date d'émission",
    "total_ttc": "montant TTC",
    "emitter": "émetteur",
}


def check_invoice(f, date_ref):
    checks = []

    for key, label in INVOICE_REQUIRED.items():
        if not f.get(key):
            checks.append({"code": "champ_manquant", "severity": "bloquant",
                           "detail": f"{label} introuvable sur la pièce"})

    ht, tva_rate, tva_amount, ttc = (f.get("total_ht"), f.get("tva_rate"),
                                     f.get("tva_amount"), f.get("total_ttc"))

    # Cohérence TVA : HT × taux ≈ TVA déclarée (tolérance 5 %, exonération ignorée)
    if ht and tva_rate and tva_amount is not None and tva_rate > 0:
        attendu = round(ht * tva_rate, 2)
        base = max(attendu, 1.0)
        if abs(attendu - tva_amount) / base > 0.05:
            checks.append({"code": "tva_incoherente", "severity": "alerte",
                           "detail": f"TVA déclarée {tva_amount} € — attendue ≈ {attendu} € "
                                     f"(HT {ht} × {round(tva_rate*100)} %)"})

    # Cohérence du total : HT + TVA ≈ TTC (tolérance 1 % ou 0,02 €)
    if ht is not None and tva_amount is not None and ttc is not None:
        attendu = round(ht + tva_amount, 2)
        if abs(attendu - ttc) > max(0.02, 0.01 * ttc):
            checks.append({"code": "montant_aberrant", "severity": "alerte",
                           "detail": f"HT {ht} + TVA {tva_amount} = {attendu} € ≠ TTC affiché {ttc} €"})

    issue = _to_date(f.get("issue_date"))
    due = _to_date(f.get("due_date"))
    if issue and issue > date_ref:
        checks.append({"code": "date_future", "severity": "alerte",
                       "detail": f"date d'émission {f['issue_date']} postérieure à {date_ref.isoformat()}"})
    if issue and due and due < issue:
        checks.append({"code": "echeance_anterieure", "severity": "alerte",
                       "detail": f"échéance {f['due_date']} antérieure à l'émission {f['issue_date']}"})

    return checks


# ── Contrôles note de frais ───────────────────────────────────────────────

EXPENSE_REQUIRED = {
    "company": "société (employeur)",
    "total_ttc": "montant à rembourser",
    "issue_date": "date",
}


def check_expense(f, date_ref):
    checks = []

    for key, label in EXPENSE_REQUIRED.items():
        if not f.get(key):
            checks.append({"code": "champ_manquant", "severity": "bloquant",
                           "detail": f"{label} introuvable sur la note de frais"})
    if not f.get("beneficiary"):
        checks.append({"code": "champ_manquant", "severity": "alerte",
                       "detail": "bénéficiaire (salarié) introuvable"})

    ht, tva_rate, tva_amount = f.get("total_ht"), f.get("tva_rate"), f.get("tva_amount")
    if ht and tva_rate and tva_amount is not None and tva_rate > 0:
        attendu = round(ht * tva_rate, 2)
        base = max(attendu, 1.0)
        if abs(attendu - tva_amount) / base > 0.05:
            checks.append({"code": "tva_incoherente", "severity": "alerte",
                           "detail": f"TVA déclarée {tva_amount} € — attendue ≈ {attendu} €"})

    issue = _to_date(f.get("issue_date"))
    if issue and issue > date_ref:
        checks.append({"code": "date_future", "severity": "alerte",
                       "detail": f"date {f['issue_date']} postérieure à {date_ref.isoformat()}"})

    return checks


# ── Contrôles relevé bancaire ─────────────────────────────────────────────

def check_statement(f):
    checks = []

    if not f.get("holder"):
        checks.append({"code": "champ_manquant", "severity": "bloquant",
                       "detail": "titulaire du compte introuvable"})
    if not f.get("operations"):
        checks.append({"code": "releve_non_parseable", "severity": "bloquant",
                       "detail": "aucune opération extraite du relevé"})

    iban_ok = _iban_valid(f.get("iban"))
    if iban_ok is False:
        checks.append({"code": "iban_invalide", "severity": "alerte",
                       "detail": f"IBAN {f.get('iban')} échoue le contrôle mod 97"})

    # Cohérence des soldes : ouverture + somme des opérations ≈ clôture
    opening, closing = f.get("opening_balance"), f.get("closing_balance")
    ops = f.get("operations") or []
    if opening is not None and closing is not None and ops:
        mouvement = round(sum(o.get("amount", 0) for o in ops), 2)
        attendu = round(opening + mouvement, 2)
        if abs(attendu - closing) > max(0.02, 0.01 * abs(closing or 1)):
            checks.append({"code": "solde_incoherent", "severity": "alerte",
                           "detail": f"ouverture {opening} + mouvements {mouvement} = {attendu} € "
                                     f"≠ clôture affichée {closing} €"})

    return checks


# ── Confiance globale ─────────────────────────────────────────────────────

def confidence(fields, checks, text_found):
    if not text_found:
        return "faible"
    if any(c["severity"] == "bloquant" for c in checks):
        return "faible"
    if any(c["severity"] == "alerte" for c in checks):
        return "moyenne"
    return "haute"


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    args = [a for a in sys.argv[1:]]
    date_ref = date.today()
    if "--date-ref" in args:
        i = args.index("--date-ref")
        date_ref = _to_date(args[i + 1]) or date_ref
        del args[i:i + 2]
    if not args:
        print(json.dumps({"kind": "other", "error": "usage: analyse.py <pdf> [--date-ref AAAA-MM-JJ]"}))
        return

    path = args[0]
    text = extract.pdftext(path)
    text_found = bool(text.strip())
    fields = extract.classify_and_extract(text)
    kind = fields.get("kind", "other")

    if kind == "invoice":
        checks = check_invoice(fields, date_ref)
    elif kind == "note-de-frais":
        checks = check_expense(fields, date_ref)
    elif kind == "bank-statement":
        checks = check_statement(fields)
    else:
        checks = []
        if not text_found:
            checks.append({"code": "sans_texte", "severity": "info",
                           "detail": "aucun texte exploitable — pièce probablement scannée ou photographiée"})

    out = {
        "kind": kind,
        "text_found": text_found,
        "confidence": confidence(fields, checks, text_found),
        "fields": fields,
        "checks": checks,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
