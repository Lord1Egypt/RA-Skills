"""Ingestion BANQUE — relevé -> liste normalisée de transactions.

Formats structurés (haute confiance) :
  - CAMT.053 (ISO 20022, .xml)
  - OFX / QFX (.ofx)
  - CSV (export bancaire ; colonnes auto-détectées, débit/crédit séparés ou montant signé)

Sortie = dict `normalized statement` :
  {
    "source": "camt053|ofx|csv",
    "account_iban": "...",
    "opening_balance": float|None,
    "closing_balance": float|None,
    "reconciled": bool,            # opening + somme(tx) == closing (gate de fiabilité)
    "transactions": [
      {"date":"YYYY-MM-DD", "amount": float (SIGNÉ: +crédit / -débit),
       "label":"...", "invoice_ref":"...|null"}
    ]
  }

Un PDF/scan de relevé n'est PAS traité ici : il part en extraction LLM (sidecar `.bank.json`),
exactement comme un ticket de caisse côté factures.
"""
from __future__ import annotations

import csv
import io
import re
from pathlib import Path

from lxml import etree

from normalize import extract_invoice_ref, money_close, parse_date, parse_money


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower() if "}" in tag else tag.lower()


def _find(el, name: str):
    name = name.lower()
    return [e for e in el.iter() if _local(e.tag) == name]


def _text(el, name: str):
    for e in _find(el, name):
        if e.text and e.text.strip():
            return e.text.strip()
    return None


def _tx(date, amount, label, *, ref=None):
    label = (label or "").strip() or "Ligne bancaire"
    return {
        "date": parse_date(date),
        "amount": amount,
        "label": label,
        "invoice_ref": ref or extract_invoice_ref(label),
    }


def _gate(opening, closing, txs) -> bool:
    """Le relevé réconcilie-t-il arithmétiquement ? (filet de fiabilité)"""
    if opening is None or closing is None or not txs:
        return False
    total = round(sum(t["amount"] for t in txs), 2)
    return money_close(round(opening + total, 2), closing) and abs(opening + total - closing) < max(1.0, abs(closing) * 0.001)


# --------------------------------------------------------------------------- #
# CAMT.053                                                                     #
# --------------------------------------------------------------------------- #

def parse_camt053(data: bytes) -> dict:
    root = etree.fromstring(data)
    txs = []
    for ntry in _find(root, "Ntry"):
        amt_el = next(iter(_find(ntry, "Amt")), None)
        amount = parse_money(amt_el.text) if amt_el is not None else None
        if amount is None:
            continue
        ind = (_text(ntry, "CdtDbtInd") or "").upper()
        if ind.startswith("DBIT"):
            amount = -abs(amount)
        else:
            amount = abs(amount)
        # date : BookgDt/Dt sinon ValDt/Dt
        d = None
        for holder in ("BookgDt", "ValDt"):
            h = next(iter(_find(ntry, holder)), None)
            if h is not None:
                d = _text(h, "Dt") or _text(h, "DtTm")
                if d:
                    break
        # libellé : RmtInf/Ustrd, sinon AddtlNtryInf, sinon AddtlTxInf
        label = " ".join(e.text.strip() for e in _find(ntry, "Ustrd") if e.text) \
            or _text(ntry, "AddtlNtryInf") or _text(ntry, "AddtlTxInf") or ""
        txs.append(_tx(d, amount, label))

    # soldes : Bal avec Tp/CdOrPrtry/Cd = OPBD (ouverture) / CLBD (clôture)
    opening = closing = None
    for bal in _find(root, "Bal"):
        code = (_text(bal, "Cd") or "").upper()
        amt_el = next(iter(_find(bal, "Amt")), None)
        val = parse_money(amt_el.text) if amt_el is not None else None
        if val is None:
            continue
        ind = (_text(bal, "CdtDbtInd") or "").upper()
        if ind.startswith("DBIT"):
            val = -abs(val)
        if code in {"OPBD", "PRCD"}:
            opening = val
        elif code in {"CLBD", "CLAV"}:
            closing = val
    iban = _text(root, "IBAN")
    return {
        "source": "camt053", "account_iban": iban,
        "opening_balance": opening, "closing_balance": closing,
        "reconciled": _gate(opening, closing, txs), "transactions": txs,
    }


# --------------------------------------------------------------------------- #
# OFX / QFX                                                                    #
# --------------------------------------------------------------------------- #

_OFX_TAG = re.compile(r"<([A-Z0-9.]+)>([^<\r\n]*)", re.I)


def parse_ofx(data: bytes) -> dict:
    text = data.decode("latin-1", errors="replace")
    txs = []
    for block in re.split(r"<STMTTRN>", text, flags=re.I)[1:]:
        block = block.split("</STMTTRN>")[0]
        fields = {k.upper(): v.strip() for k, v in _OFX_TAG.findall(block)}
        amount = parse_money(fields.get("TRNAMT"))
        if amount is None:
            continue
        label = fields.get("NAME") or fields.get("MEMO") or ""
        if fields.get("MEMO") and fields.get("NAME"):
            label = f"{fields['NAME']} {fields['MEMO']}"
        txs.append(_tx(fields.get("DTPOSTED"), amount, label, ref=fields.get("CHECKNUM")))
    all_fields = {k.upper(): v.strip() for k, v in _OFX_TAG.findall(text)}
    iban = all_fields.get("ACCTID")
    opening = parse_money(all_fields.get("BALAMT"))  # approx, souvent solde courant
    return {
        "source": "ofx", "account_iban": iban,
        "opening_balance": None, "closing_balance": opening,
        "reconciled": False, "transactions": txs,  # OFX n'a pas toujours opening+closing fiables
    }


# --------------------------------------------------------------------------- #
# CSV                                                                          #
# --------------------------------------------------------------------------- #

_DATE_COLS = ("date", "date operation", "date op", "date valeur", "datecomptable", "booking date")
_LABEL_COLS = ("libelle", "libellé", "label", "description", "designation", "nature", "intitule", "memo", "details")
_AMOUNT_COLS = ("montant", "amount", "valeur", "value")
_DEBIT_COLS = ("debit", "débit", "retrait", "withdrawal")
_CREDIT_COLS = ("credit", "crédit", "depot", "dépôt", "deposit")


def _norm_header(h: str) -> str:
    from normalize import strip_accents
    return strip_accents((h or "").strip().lower())


def parse_csv(data: bytes) -> dict:
    text = data.decode("utf-8-sig", errors="replace")
    # détecter le délimiteur
    sample = text[:2000]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=";,\t|")
        delim = dialect.delimiter
    except csv.Error:
        delim = ";" if sample.count(";") >= sample.count(",") else ","
    reader = csv.reader(io.StringIO(text), delimiter=delim)
    rows = [r for r in reader if any(c.strip() for c in r)]
    if not rows:
        return {"source": "csv", "transactions": [], "reconciled": False,
                "opening_balance": None, "closing_balance": None, "account_iban": None}

    header = [_norm_header(c) for c in rows[0]]

    def col(cands):
        for i, h in enumerate(header):
            if any(h == c or h.startswith(c) for c in cands):
                return i
        return None

    ci_date, ci_label = col(_DATE_COLS), col(_LABEL_COLS)
    ci_amount = col(_AMOUNT_COLS)
    ci_debit, ci_credit = col(_DEBIT_COLS), col(_CREDIT_COLS)
    has_header = ci_date is not None or ci_amount is not None or ci_debit is not None
    body = rows[1:] if has_header else rows
    if not has_header:  # heuristique : col0=date, dernière=montant, milieu=libellé
        ci_date, ci_label, ci_amount = 0, 1, len(rows[0]) - 1

    txs = []
    for r in body:
        get = lambda i: r[i].strip() if i is not None and i < len(r) else ""
        amount = None
        if ci_amount is not None:
            amount = parse_money(get(ci_amount))
        if amount is None and (ci_debit is not None or ci_credit is not None):
            d, c = parse_money(get(ci_debit)), parse_money(get(ci_credit))
            if d:
                amount = -abs(d)
            elif c:
                amount = abs(c)
        if amount is None:
            continue
        txs.append(_tx(get(ci_date), amount, get(ci_label)))
    return {
        "source": "csv", "account_iban": None,
        "opening_balance": None, "closing_balance": None,
        "reconciled": bool(txs), "transactions": txs,  # le CSV liste les opérations, pas de gate solde
    }


# --------------------------------------------------------------------------- #
# Point d'entrée                                                               #
# --------------------------------------------------------------------------- #

def parse_structured_statement(path: Path) -> dict | None:
    """CAMT.053 / OFX / CSV -> relevé normalisé, ou None si format non structuré (-> LLM)."""
    suffix = path.suffix.lower()
    try:
        if suffix == ".xml":
            data = path.read_bytes()
            if b"camt.053" in data[:4000].lower() or _find(etree.fromstring(data), "Ntry"):
                return parse_camt053(data)
            return None
        if suffix in {".ofx", ".qfx"}:
            return parse_ofx(path.read_bytes())
        if suffix in {".csv", ".tsv"}:
            return parse_csv(path.read_bytes())
    except (etree.XMLSyntaxError, ValueError):
        return None
    return None
