#!/usr/bin/env python3
"""Orchestrateur du skill e-facture-rapprochement.

Pipeline par client :
  A. INGESTION FACTURES   (fast-path structuré ; sinon sidecar LLM .invoice.json)
  B. INGESTION BANQUE      (CAMT.053 / OFX / CSV ; sinon sidecar LLM .bank.json)
  C. RAPPROCHEMENT         (reconcile.py)
  D. SORTIE                company.json + rapprochement.json + auto-contrôle (§8)

Boucle en DEUX temps (les PDF/photos passent par le LLM de l'agent) :
  1) `python3 main.py <root>` ingère tout ce qui est structuré, et liste les documents
     qui nécessitent une extraction LLM (worklist). S'il en reste -> il S'ARRÊTE.
  2) L'agent extrait chaque document de la worklist en écrivant un sidecar JSON à côté,
     puis relance la commande. Quand la worklist est vide -> rapprochement + écriture.

Disposition d'entrée attendue, PAR CLIENT :
  <root>/<slug>/invoices|factures/   -> factures (pdf, jpg, png, xml…)
  <root>/<slug>/bank|releves|banque/ -> relevés  (xml CAMT, ofx, csv, pdf…)
  <root>/<slug>/company.json         -> identité (optionnel ; sert à déduire in/out)

Sorties (écriture atomique) :
  <root>/<slug>/company.json, <root>/<slug>/rapprochement.json   (CONTRAT backend)
  <root>/<slug>/_review.json, <root>/_worklist.json             (INTERNES, ignorés du backend)
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bank_parsers import parse_structured_statement          # noqa: E402
from invoice_parsers import finalize_type, parse_structured_invoice  # noqa: E402
from normalize import (HUMAN_REVIEW_AMOUNT, HUMAN_REVIEW_CONFIDENCE,  # noqa: E402
                       slugify)

# Le RAPPROCHEMENT est délégué au moteur unique et audité du skill
# `rapprochement-paiements` (⑤) — un seul moteur pour les deux skills, donc des
# sorties identiques à entrées identiques. e-facture garde toute son INGESTION
# (Factur-X/UBL/CII + tickets LLM + CAMT/OFX/CSV) ; seule la décision de
# rapprochement est partagée. (Ancien moteur local `reconcile.py` conservé pour
# ses tests, mais plus utilisé pour produire la sortie.)
import datetime as _dt  # noqa: E402
import importlib.util as _ilu  # noqa: E402


def _load_engine():
    """Charge rapprochement-paiements/scripts/main.py comme moteur partagé."""
    engine_path = (Path(__file__).resolve().parents[2]
                   / "rapprochement-paiements" / "scripts" / "main.py")
    spec = _ilu.spec_from_file_location("rappro_engine", str(engine_path))
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

DEFAULT_SANDBOX = os.path.expanduser("~/.openclaw/workspace/clients-test")
REAL_ROOT = os.path.expanduser("~/.openclaw/workspace/clients")
INVOICE_DIRS = {"invoices", "factures"}
BANK_DIRS = {"bank", "banque", "releves", "relevés", "statements"}
INVOICE_EXT = {".pdf", ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".xml", ".webp"}
BANK_EXT = {".xml", ".ofx", ".qfx", ".csv", ".tsv", ".pdf", ".jpg", ".jpeg", ".png"}


# --------------------------------------------------------------------------- #
# Écriture atomique                                                            #
# --------------------------------------------------------------------------- #

def write_json(path: Path, data) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


# --------------------------------------------------------------------------- #
# Hint d'extraction (texte vs vision) pour un PDF                              #
# --------------------------------------------------------------------------- #

def _pdf_has_text(path: Path) -> bool:
    try:
        out = subprocess.run(["pdftotext", "-l", "2", str(path), "-"],
                             capture_output=True, timeout=30)
        return len((out.stdout or b"").strip()) > 200
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _mode_hint(path: Path) -> str:
    if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}:
        return "vision"
    if path.suffix.lower() == ".pdf":
        return "text" if _pdf_has_text(path) else "vision"
    return "text"


# --------------------------------------------------------------------------- #
# Ingestion d'un client                                                        #
# --------------------------------------------------------------------------- #

def _doc_files(client_dir: Path, dir_names: set[str], exts: set[str]) -> list[Path]:
    files = []
    for sub in client_dir.iterdir():
        if sub.is_dir() and sub.name.lower() in dir_names:
            for f in sorted(sub.rglob("*")):
                if f.is_file() and f.suffix.lower() in exts and not f.name.endswith((".invoice.json", ".bank.json")):
                    files.append(f)
    return files


def ingest_client(client_dir: Path) -> dict:
    """Renvoie {invoices, statements, worklist, ingestion_anomalies, review}."""
    company = load_json(client_dir / "company.json") or {}
    client_ids = {k: company.get(k) for k in ("siren", "siret", "iban", "name")}

    invoices, statements, worklist, anomalies, review = [], [], [], [], []

    # --- FACTURES ---
    for f in _doc_files(client_dir, INVOICE_DIRS, INVOICE_EXT):
        inv = parse_structured_invoice(f)                 # tier 1-2 : Factur-X / UBL / CII
        if inv is None:
            side = f.with_suffix(f.suffix + ".invoice.json")
            cached = load_json(side)
            if cached is None:
                worklist.append({"path": str(f), "kind": "invoice",
                                 "mode": _mode_hint(f),
                                 "sidecar": str(side)})
                continue
            inv = cached
            inv.setdefault("source", "llm")
        inv["source_file"] = str(f.relative_to(client_dir))
        inv = finalize_type(inv, client_ids) if inv.get("type") is None else inv
        inv.setdefault("counterparty_name", inv.get("counterparty_name") or "(inconnu)")
        # validation humaine ?
        conf = float(inv.get("confidence", 1.0))
        amt = abs(float(inv.get("amount") or 0))
        reasons = list(inv.get("review_reasons", []))
        if amt > HUMAN_REVIEW_AMOUNT:
            reasons.append(f"montant>{HUMAN_REVIEW_AMOUNT:.0f}")
        if conf < HUMAN_REVIEW_CONFIDENCE:
            reasons.append(f"confiance<{HUMAN_REVIEW_CONFIDENCE}")
        if reasons:
            review.append({"source_file": inv["source_file"], "invoice_id": inv.get("invoice_id"),
                           "amount": inv.get("amount"), "confidence": conf, "reasons": reasons})
        if not inv.get("invoice_id") or inv.get("amount") is None:
            anomalies.append({"type": "facture_illisible", "label": inv["source_file"],
                              "amount": 0, "date": None,
                              "period": (inv.get("issued_date") or "")[:7] or None,
                              "source_file": inv["source_file"]})
            continue
        invoices.append(inv)

    # --- BANQUE ---
    for f in _doc_files(client_dir, BANK_DIRS, BANK_EXT):
        st = parse_structured_statement(f)                # CAMT.053 / OFX / CSV
        if st is None:
            side = f.with_suffix(f.suffix + ".bank.json")
            cached = load_json(side)
            if cached is None:
                worklist.append({"path": str(f), "kind": "bank",
                                 "mode": _mode_hint(f), "sidecar": str(side)})
                continue
            st = cached
            st.setdefault("source", "llm")
        st["source_file"] = str(f.relative_to(client_dir))
        if not st.get("transactions"):
            anomalies.append({"type": "releve_non_parseable", "label": st["source_file"],
                              "amount": 0, "date": None, "period": None,
                              "source_file": st["source_file"]})
            continue
        statements.append(st)

    return {"company": company, "invoices": invoices, "statements": statements,
            "worklist": worklist, "ingestion_anomalies": anomalies, "review": review}


# --------------------------------------------------------------------------- #
# Sortie d'un client                                                           #
# --------------------------------------------------------------------------- #

def write_outputs(client_dir: Path, ing: dict, today: str | None) -> list[dict]:
    """Rapprochement délégué au moteur PARTAGÉ ⑤ (politique conservatrice unique).
    On mappe l'ingestion e-facture (factures + relevés normalisés) vers la forme
    attendue par `reconcile_invoices` / `backend_rapprochement`, puis on écrit le
    contrat backend. → sorties identiques au skill rapprochement-paiements."""
    engine = _load_engine()
    try:
        today_date = (_dt.datetime.strptime(today, "%Y-%m-%d").date()
                      if today else _dt.date.today())
    except (ValueError, TypeError):
        today_date = _dt.date.today()

    # 1) Factures -> forme du cœur ⑤
    invoice_list = []
    for inv in ing["invoices"]:
        cp = inv.get("counterparty_name") or "(inconnu)"
        issued = inv.get("issued_date")
        due = inv.get("due_date")
        if not due and issued:
            try:
                due = (_dt.datetime.strptime(issued, "%Y-%m-%d").date()
                       + _dt.timedelta(days=30)).isoformat()
            except ValueError:
                due = None
        invoice_list.append({
            "invoice_id": inv.get("invoice_id"), "type": inv.get("type") or "in",
            "amount": inv.get("amount"), "status": "unpaid",
            "issued_date": issued, "due_date": due,
            "counterparty": cp, "counterparty_name": cp,
            "bank_matched": False, "source_file": inv.get("source_file"),
        })

    # 2) Relevés -> transactions à plat (période = mois de l'opération)
    transactions, period_stmt = [], {}
    for st in ing["statements"]:
        reliable = bool(st.get("reconciled", True))
        st_periods = set()
        for op in st.get("transactions", []):
            d = op.get("date")
            pk = (d or "")[:7]
            lbl = op.get("label") or ""
            transactions.append({
                "date": d, "label": lbl.lower(), "raw_label": lbl,
                "amount": op.get("amount"), "invoice_ref": op.get("invoice_ref"),
                "reliable": reliable, "period": pk if len(pk) == 7 else None,
            })
            if len(pk) == 7:
                st_periods.add(pk)
                period_stmt.setdefault(pk, {"statements": 0, "transactions": 0})["transactions"] += 1
        for pk in st_periods:
            period_stmt[pk]["statements"] += 1

    # 3) Cœur de rapprochement PARTAGÉ ⑤
    anomalies = list(ing["ingestion_anomalies"])
    consumed, relances = engine.reconcile_invoices(invoice_list, transactions, anomalies, today_date)
    prior = load_json(client_dir / "rapprochement.json") or {}
    periods = engine.backend_rapprochement(
        client_dir, invoice_list, anomalies, relances, period_stmt,
        prior, transactions, consumed)["periods"]

    # 4) Sortie contractuelle (company.json préservé tel quel)
    write_json(client_dir / "company.json", dict(ing["company"]))
    write_json(client_dir / "rapprochement.json", {"periods": periods})
    if ing["review"]:
        write_json(client_dir / "_review.json", {"needs_human_review": ing["review"]})
    elif (client_dir / "_review.json").exists():
        (client_dir / "_review.json").unlink()

    # 5) selfcheck (même forme) recalculé depuis les périodes
    selfcheck = []
    for p in periods:
        matched = p.get("bank_matched_count", 0)
        unm, exc = len(p.get("unmatched_bank_lines", [])), len(p.get("excluded_bank_lines", []))
        somme = matched + unm + exc
        selfcheck.append({"period": p.get("period"),
                          "bank_transactions_count": p.get("bank_transactions_count", 0),
                          "matched": matched, "unmatched": unm, "excluded": exc,
                          "somme": somme, "ok": somme == p.get("bank_transactions_count", 0)})
    return selfcheck


# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #

def discover_clients(root: Path, only: str | None) -> list[Path]:
    if only:
        return [root / only]
    return sorted(d for d in root.iterdir()
                  if d.is_dir() and not d.name.startswith("_"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="e-facture-rapprochement")
    ap.add_argument("root", nargs="?", default=None,
                    help="racine clients (défaut : clients-test sandbox)")
    ap.add_argument("--real", action="store_true",
                    help="écrire dans le vrai ~/.openclaw/workspace/clients/ (sinon sandbox)")
    ap.add_argument("--client", help="ne traiter qu'un slug")
    ap.add_argument("--today", help="date de référence ISO pour overdue/relances")
    args = ap.parse_args(argv)

    root = Path(args.root) if args.root else Path(REAL_ROOT if args.real else DEFAULT_SANDBOX)
    if not root.exists():
        print(f"!! racine introuvable : {root}", file=sys.stderr)
        return 2

    clients = discover_clients(root, args.client)
    all_worklist, all_selfcheck, all_review = [], [], []
    pending = False

    for cdir in clients:
        if not cdir.exists():
            print(f"!! client introuvable : {cdir}", file=sys.stderr)
            continue
        ing = ingest_client(cdir)
        slug = cdir.name
        if ing["worklist"]:
            pending = True
            for w in ing["worklist"]:
                w["client"] = slug
            all_worklist.extend(ing["worklist"])
            continue
        selfcheck = write_outputs(cdir, ing, args.today)
        for s in selfcheck:
            s["client"] = slug
        all_selfcheck.extend(selfcheck)
        all_review.extend({**r, "client": slug} for r in ing["review"])

    # --- worklist : extraction LLM requise ---
    if pending:
        write_json(root / "_worklist.json", {"items": all_worklist})
        print("\n=== EXTRACTION LLM REQUISE ===")
        print(f"{len(all_worklist)} document(s) ne sont pas structurés (PDF / photo de ticket).")
        print("Pour CHACUN : lis le document, extrais au schéma (references/invoice-extraction.md")
        print("ou bank-formats.md), et écris le JSON dans le chemin 'sidecar'. Puis relance.\n")
        for w in all_worklist:
            print(f"  [{w['kind']:7}] {w['client']}/{Path(w['path']).name}"
                  f"  (mode={w['mode']}) -> {Path(w['sidecar']).name}")
        print("\nWorklist détaillée :", root / "_worklist.json")
        return 0

    # --- auto-contrôle (§8) ---
    print("\n=== AUTO-CONTRÔLE (par période) ===")
    print(f"{'client':24} {'période':9} {'tx':>4} {'rappr':>6} {'unmat':>6} {'exclu':>6} {'somme':>6}  état")
    ko = 0
    for s in all_selfcheck:
        flag = "OK" if s["ok"] else "** KO **"
        ko += 0 if s["ok"] else 1
        print(f"{s['client'][:24]:24} {s['period']:9} {s['bank_transactions_count']:>4} "
              f"{s['matched']:>6} {s['unmatched']:>6} {s['excluded']:>6} {s['somme']:>6}  {flag}")
    if all_review:
        print(f"\n=== VALIDATION HUMAINE conseillée ({len(all_review)} facture(s)) ===")
        for r in all_review:
            print(f"  {r['client']}/{r.get('invoice_id') or r['source_file']}: {', '.join(r['reasons'])}")
    if ko:
        print(f"\n!! {ko} période(s) en KO — invariant non respecté. Sortie NON validée.", file=sys.stderr)
        return 1
    print(f"\nOK — {len(all_selfcheck)} période(s) valides. "
          f"company.json + rapprochement.json écrits sous {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
