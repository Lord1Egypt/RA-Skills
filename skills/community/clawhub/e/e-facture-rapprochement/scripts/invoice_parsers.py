"""Ingestion FACTURES — fast-path structuré (haute confiance).

Cascade (confiance décroissante) :
  1. Factur-X / ZUGFeRD  : PDF/A-3 -> XML CII embarqué (pdfdetach) -> parse CII
  2. XML pur UBL (OASIS) ou CII (UN/CEFACT) -> parse direct
  3. (tier 3 = LLM) : géré HORS de ce module, par l'agent, via un sidecar `.invoice.json`.

Tout est parsé en "namespace-agnostic" (on regarde le local-name des balises) : les
profils et les versions de schéma changent les namespaces mais pas les noms de champs.
Sortie = dict au schéma `normalized invoice` (voir references/invoice-extraction.md).
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from lxml import etree

from normalize import parse_date, parse_money, slugify


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower() if "}" in tag else tag.lower()


def _findall_local(root, name: str):
    name = name.lower()
    return [e for e in root.iter() if _local(e.tag) == name]


def _first_text(root, name: str) -> str | None:
    for e in _findall_local(root, name):
        if e.text and e.text.strip():
            return e.text.strip()
    return None


def detect_xml_kind(data: bytes) -> str | None:
    """'ubl' | 'cii' | None à partir du contenu XML."""
    try:
        root = etree.fromstring(data)
    except etree.XMLSyntaxError:
        return None
    r = _local(root.tag)
    if r in {"invoice", "creditnote"}:
        return "ubl"
    if r == "crossindustryinvoice":
        return "cii"
    # repli : présence de namespaces caractéristiques
    blob = data[:4000].lower()
    if b"crossindustryinvoice" in blob or b"un/cefact" in blob:
        return "cii"
    if b"oasis" in blob and b"invoice" in blob:
        return "ubl"
    return None


# --------------------------------------------------------------------------- #
# UBL (OASIS)                                                                  #
# --------------------------------------------------------------------------- #

def parse_ubl(data: bytes) -> dict:
    root = etree.fromstring(data)
    inv = {"source": "ubl"}
    inv["invoice_id"] = _first_text(root, "ID")
    inv["issued_date"] = parse_date(_first_text(root, "IssueDate"))
    inv["due_date"] = parse_date(_first_text(root, "DueDate"))

    # Totaux : LegalMonetaryTotal/PayableAmount = TTC ; TaxExclusiveAmount = HT.
    lmt = next(iter(_findall_local(root, "LegalMonetaryTotal")), None)
    if lmt is not None:
        inv["amount"] = parse_money(_first_text(lmt, "PayableAmount") or _first_text(lmt, "TaxInclusiveAmount"))
        inv["total_ht"] = parse_money(_first_text(lmt, "TaxExclusiveAmount"))
    tt = next(iter(_findall_local(root, "TaxTotal")), None)
    if tt is not None:
        inv["tva_amount"] = parse_money(_first_text(tt, "TaxAmount"))

    inv["_supplier"] = _party_name(root, "AccountingSupplierParty")
    inv["_customer"] = _party_name(root, "AccountingCustomerParty")
    inv["_supplier_id"] = _party_id(root, "AccountingSupplierParty")
    inv["_customer_id"] = _party_id(root, "AccountingCustomerParty")
    return inv


def _party_name(root, party_tag: str) -> str | None:
    p = next(iter(_findall_local(root, party_tag)), None)
    if p is None:
        return None
    # RegistrationName (PartyLegalEntity) prioritaire, sinon Name (PartyName).
    for tag in ("RegistrationName", "Name"):
        v = _first_text(p, tag)
        if v:
            return v
    return None


def _party_id(root, party_tag: str) -> str | None:
    p = next(iter(_findall_local(root, party_tag)), None)
    if p is None:
        return None
    for tag in ("CompanyID", "EndpointID", "ID"):
        v = _first_text(p, tag)
        if v:
            return v
    return None


# --------------------------------------------------------------------------- #
# CII (UN/CEFACT — utilisé aussi par Factur-X)                                 #
# --------------------------------------------------------------------------- #

def parse_cii(data: bytes) -> dict:
    root = etree.fromstring(data)
    inv = {"source": "cii"}
    doc = next(iter(_findall_local(root, "ExchangedDocument")), None)
    inv["invoice_id"] = _first_text(doc if doc is not None else root, "ID")
    # IssueDateTime/DateTimeString
    issue = next(iter(_findall_local(root, "IssueDateTime")), None)
    inv["issued_date"] = parse_date(issue.itertext().__next__() if issue is not None else None) \
        or parse_date(_first_text(root, "DateTimeString"))

    summ = next(iter(_findall_local(root, "SpecifiedTradeSettlementHeaderMonetarySummation")), None)
    if summ is not None:
        inv["amount"] = parse_money(_first_text(summ, "GrandTotalAmount")
                                    or _first_text(summ, "DuePayableAmount"))
        inv["total_ht"] = parse_money(_first_text(summ, "TaxBasisTotalAmount")
                                      or _first_text(summ, "LineTotalAmount"))
        inv["tva_amount"] = parse_money(_first_text(summ, "TaxTotalAmount"))

    # Échéance
    due = next(iter(_findall_local(root, "DueDateDateTime")), None)
    if due is not None:
        inv["due_date"] = parse_date(next(due.itertext(), None))

    seller = next(iter(_findall_local(root, "SellerTradeParty")), None)
    buyer = next(iter(_findall_local(root, "BuyerTradeParty")), None)
    inv["_supplier"] = _first_text(seller, "Name") if seller is not None else None
    inv["_customer"] = _first_text(buyer, "Name") if buyer is not None else None
    inv["_supplier_id"] = (_first_text(seller, "ID") if seller is not None else None)
    inv["_customer_id"] = (_first_text(buyer, "ID") if buyer is not None else None)
    return inv


# --------------------------------------------------------------------------- #
# Factur-X : extraire le XML CII embarqué d'un PDF/A-3                          #
# --------------------------------------------------------------------------- #

def extract_facturx_xml(pdf_path: Path) -> bytes | None:
    """Renvoie l'XML CII embarqué (factur-x.xml / zugferd-invoice.xml) ou None."""
    with tempfile.TemporaryDirectory() as td:
        try:
            subprocess.run(["pdfdetach", "-saveall", "-o", td, str(pdf_path)],
                           check=True, capture_output=True, timeout=60)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            return None
        candidates = list(Path(td).glob("*.xml")) + list(Path(td).glob("*.XML"))
        # nom conventionnel d'abord
        for c in candidates:
            if c.name.lower() in {"factur-x.xml", "zugferd-invoice.xml", "xrechnung.xml", "cii.xml"}:
                return c.read_bytes()
        for c in candidates:
            data = c.read_bytes()
            if detect_xml_kind(data) in {"cii", "ubl"}:
                return data
    return None


# --------------------------------------------------------------------------- #
# Point d'entrée : essaie le fast-path structuré sur un fichier facture.        #
# --------------------------------------------------------------------------- #

def parse_structured_invoice(path: Path) -> dict | None:
    """Tente Factur-X / UBL / CII. Renvoie un dict normalisé (confiance 1.0) ou None.

    None signifie « pas de données structurées » -> l'agent devra faire l'extraction LLM.
    """
    suffix = path.suffix.lower()
    raw = None
    if suffix == ".xml":
        raw = path.read_bytes()
    elif suffix == ".pdf":
        raw = extract_facturx_xml(path)
    if not raw:
        return None
    kind = detect_xml_kind(raw)
    if kind == "ubl":
        inv = parse_ubl(raw)
    elif kind == "cii":
        inv = parse_cii(raw)
    else:
        return None
    inv["confidence"] = 1.0
    inv["source_file"] = path.name
    return inv


def finalize_type(inv: dict, client_ids: dict) -> dict:
    """Déduit `type` (in/out) et `counterparty_name` à partir des parties.

    - Si le FOURNISSEUR (vendeur) = le client -> c'est une VENTE -> type "out",
      la contrepartie est le CLIENT (acheteur).
    - Si l'ACHETEUR = le client -> c'est un ACHAT -> type "in",
      la contrepartie est le FOURNISSEUR.
    - Indéterminé -> défaut "in" (un document reçu est le plus souvent un achat),
      et on note la raison pour revue.
    client_ids : {"siren":..., "iban":..., "name":...} du client (depuis company.json).
    """
    def norm(s):
        return "".join(ch for ch in (s or "").lower() if ch.isalnum())

    cid = {norm(client_ids.get(k)) for k in ("siren", "siret", "iban") if client_ids.get(k)}
    cname = client_ids.get("name") or ""
    sup_id, cust_id = norm(inv.get("_supplier_id")), norm(inv.get("_customer_id"))

    typ, counterparty, reason = None, None, None
    if cid and sup_id and sup_id in cid:
        typ, counterparty = "out", inv.get("_customer")
    elif cid and cust_id and cust_id in cid:
        typ, counterparty = "in", inv.get("_supplier")
    elif cname and inv.get("_supplier") and name_sim_high(cname, inv["_supplier"]):
        typ, counterparty = "out", inv.get("_customer")
    elif cname and inv.get("_customer") and name_sim_high(cname, inv["_customer"]):
        typ, counterparty = "in", inv.get("_supplier")
    if typ is None:
        typ = "in"
        counterparty = inv.get("_supplier") or inv.get("_customer")
        reason = "type_indetermine"

    inv["type"] = typ
    inv["counterparty_name"] = counterparty or "(inconnu)"
    if reason:
        inv.setdefault("review_reasons", []).append(reason)
    for k in list(inv):
        if k.startswith("_"):
            del inv[k]
    return inv


def name_sim_high(a: str, b: str) -> bool:
    from normalize import name_similarity
    return name_similarity(a, b) >= 0.7
