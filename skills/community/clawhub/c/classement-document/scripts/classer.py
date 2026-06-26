#!/usr/bin/env python3
"""
Étape ④ du pipeline comptable — CLASSEMENT.

Action humaine : prendre une pièce dont on connaît déjà la nature et le client,
et la ranger dans le bon classeur sous un nom normalisé.

Cette brique ne décide RIEN : elle reçoit la pièce analysée (étape ②) et le
client identifié (étape ③), puis range. Elle possède l'arborescence
`clients/<slug>/<AAAA>/<MM>/...` et l'index de déduplication (`_index.json`).
Elle ne lit ni n'écrit jamais `clients.json` (domaine d'identification-client).

Aucune perte : une pièce dont le client n'est pas tranché va en `_a-identifier/`,
une extraction incomplète en `_incomplet/`, une pièce non comptable en
`_non-attribue/`. On copie (on ne supprime jamais la source).

Usage :
  echo '<dossier.json>' | python3 classer.py [--clients-root clients] [--source <fichier>]

Entrée : dossier contenant
  { "analyse": {"kind","fields"}, "client": {"slug","role","counterparty","needs_review"},
    "source": {"path","filename"} }

Sortie : le dossier enrichi d'un bloc "classement" :
  { ..., "classement": { "status": "classé|_a-identifier|_incomplet|_non-attribue|doublon",
                         "dest": "clients/acme-sa/2026/03/invoices/in/…", "filename": "…" } }
"""

import hashlib
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path


# ── Helpers ───────────────────────────────────────────────────────────────

def slugify(s):
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()


def short_name(s, n=14):
    if not s:
        return "inconnu"
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")
    return (s[:n].strip("-") or "inconnu")


def amount_str(x):
    return f"{x:.2f}" if isinstance(x, (int, float)) else None


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def place(src, dest_rel, root):
    dest = root / dest_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest = dest.with_name(f"{dest.stem}__{src.stem[:8]}{dest.suffix}")
    shutil.copy2(src, dest)
    return dest


# ── Décision du chemin cible ───────────────────────────────────────────────

def target_path(analyse, client, src):
    """Renvoie (chemin_relatif, status). Ne range pas encore."""
    kind = analyse.get("kind")
    f = analyse.get("fields") or {}

    if kind not in ("invoice", "bank-statement", "note-de-frais"):
        return Path("_non-attribue") / src.name, "_non-attribue"

    if client.get("needs_review") or not client.get("slug"):
        return Path("_a-identifier") / src.name, "_a-identifier"

    slug = client["slug"]

    if kind == "bank-statement":
        ps = f.get("period_start") or f.get("period_end")
        if not ps:
            # période non imprimée → on date par la 1re opération (évite le bucket
            # 0000/00, qui sortirait le relevé de sa période réelle pour le suivi).
            op_dates = sorted(o["date"] for o in (f.get("operations") or []) if o.get("date"))
            ps = op_dates[0] if op_dates else None
        yyyy, mm = (ps[:4], ps[5:7]) if ps else ("0000", "00")
        bank = slugify(f.get("bank") or "banque")
        return Path(slug) / yyyy / mm / "bank-statements" / f"{yyyy}-{mm}_{bank}.pdf", "classé"

    if kind == "note-de-frais":
        date = f.get("issue_date") or f.get("period_end") or f.get("period_start")
        ttc = f.get("total_ttc")
        if not date or ttc is None:
            return Path("_incomplet") / src.name, "_incomplet"
        yyyy, mm = date[:4], date[5:7]
        benef = short_name(client.get("counterparty") or f.get("beneficiary"))
        fname = f"{date}_{benef}_{amount_str(ttc)}.pdf"
        return Path(slug) / yyyy / mm / "notes-de-frais" / fname, "classé"

    # facture
    date, ttc = f.get("issue_date"), f.get("total_ttc")
    if not date or ttc is None:
        return Path("_incomplet") / src.name, "_incomplet"
    inv_no = re.sub(r"[^A-Za-z0-9\-]+", "-", f.get("invoice_id") or "SANS-NUM").strip("-") or "SANS-NUM"
    yyyy, mm = date[:4], date[5:7]
    direction = client.get("role") if client.get("role") in ("in", "out") else "in"
    fname = f"{date}_{inv_no}_{short_name(client.get('counterparty'))}_{amount_str(ttc)}.pdf"
    return Path(slug) / yyyy / mm / "invoices" / direction / fname, "classé"


def classer(dossier, root, source_override=None):
    root = Path(root)
    src_path = source_override or (dossier.get("source") or {}).get("path")
    if not src_path or not Path(src_path).exists():
        dossier["classement"] = {"status": "erreur", "dest": None,
                                 "filename": None, "detail": "fichier source introuvable"}
        return dossier
    src = Path(src_path)

    index = load_json(root / "_index.json", {})
    sha = sha256_file(src)
    if sha in index:
        dossier["classement"] = {"status": "doublon", "dest": index[sha],
                                 "filename": Path(index[sha]).name,
                                 "detail": "pièce déjà classée (même empreinte)"}
        return dossier

    dest_rel, status = target_path(dossier.get("analyse") or {}, dossier.get("client") or {}, src)
    placed = place(src, dest_rel, root)
    rel = str(placed.relative_to(root))
    # On n'indexe que les pièces réellement rangées dans un dossier client.
    if status == "classé":
        index[sha] = rel
        save_json(root / "_index.json", index)

    dossier["classement"] = {"status": status, "dest": rel, "filename": placed.name}
    return dossier


def main():
    args = sys.argv[1:]
    root, source = "clients", None
    if "--clients-root" in args:
        i = args.index("--clients-root"); root = args[i + 1]; del args[i:i + 2]
    if "--source" in args:
        i = args.index("--source"); source = args[i + 1]; del args[i:i + 2]
    raw = sys.stdin.read() if not args else open(args[0], encoding="utf-8").read()
    try:
        dossier = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"entrée JSON invalide : {e}"}))
        sys.exit(1)
    print(json.dumps(classer(dossier, root, source), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
