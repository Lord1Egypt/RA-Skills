"""Helpers partagés : argent, dates, slugs, similarité de noms, constantes.

Aucune dépendance externe (stdlib uniquement) pour rester portable dans le conteneur.
"""
from __future__ import annotations

import difflib
import re
import unicodedata
from datetime import date, datetime

# --------------------------------------------------------------------------- #
# Constantes de réglage (un seul endroit pour les ajuster)                     #
# --------------------------------------------------------------------------- #

# Rapprochement
AMOUNT_TOL_ABS = 1.0        # tolérance absolue sur le montant (€)
AMOUNT_TOL_PCT = 0.01       # tolérance relative (1 %)
DATE_WINDOW_DAYS = 15       # fenêtre date facture <-> transaction (± N jours)
LABEL_SIM_MIN = 0.55        # similarité libellé/contrepartie minimale pour matcher en fuzzy
SCORE_W_AMOUNT = 0.5        # le montant ne décide JAMAIS seul : il faut libellé OU date en plus
SCORE_W_LABEL = 0.3
SCORE_W_DATE = 0.2
SCORE_MIN = 0.62            # score global minimal pour accepter un match fuzzy
SCORE_AMBIGU_GAP = 0.08     # si 2 candidats sont à moins de ce gap -> ambigu (on n'écrit rien)

# Extraction LLM : seuils de validation humaine
HUMAN_REVIEW_AMOUNT = 1000.0   # montant TTC au-dessus duquel on demande une validation humaine
HUMAN_REVIEW_CONFIDENCE = 0.75 # confiance en-dessous de laquelle on demande une validation

# TVA
TVA_TOLERANCE_PCT = 0.05    # écart toléré entre TVA déclarée et TVA attendue (5 %)

# Relances (ancienneté du retard -> step)
RELANCE_STEPS = [(30, 1), (60, 2), (90, 3)]  # au-delà de 90 j -> "escalation"


# --------------------------------------------------------------------------- #
# Slugs                                                                        #
# --------------------------------------------------------------------------- #

def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def slugify(name: str) -> str:
    """Slug client : minuscules, mots séparés par tirets, sans accents ni civilité."""
    s = strip_accents(name or "").lower()
    s = re.sub(r"\b(m|mr|mme|mlle|monsieur|madame|mademoiselle)\b\.?", " ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s) or "client"


# --------------------------------------------------------------------------- #
# Argent                                                                       #
# --------------------------------------------------------------------------- #

# Accepte "1 234,56", "1.234,56", "1,234.56", "742.50", "742,5", "3600".
_MONEY_CLEAN = re.compile(r"[^\d,.\-]")


def parse_money(raw) -> float | None:
    """Parse un montant en gérant les conventions FR et US. Renvoie None si illisible."""
    if raw is None:
        return None
    if isinstance(raw, (int, float)):
        return round(float(raw), 2)
    s = str(raw).strip()
    if not s:
        return None
    neg = s.startswith("-") or s.startswith("(") or s.endswith("-")
    s = _MONEY_CLEAN.sub("", s)
    if not s or s in {"-", ".", ","}:
        return None
    s = s.lstrip("-")
    # Déterminer le séparateur décimal = le dernier ',' ou '.' présent.
    last_comma = s.rfind(",")
    last_dot = s.rfind(".")
    dec_pos = max(last_comma, last_dot)
    if dec_pos == -1:
        intpart, frac = s, ""
    else:
        sep = s[dec_pos]
        # Si le "séparateur décimal" candidat a 3 chiffres derrière -> c'est un séparateur de milliers.
        if len(s) - dec_pos - 1 == 3 and (s.count(sep) > 1 or (last_comma != -1 and last_dot != -1)):
            intpart, frac = s.replace(",", "").replace(".", ""), ""
        else:
            intpart = re.sub(r"[,.]", "", s[:dec_pos])
            frac = s[dec_pos + 1:]
    try:
        val = float(f"{intpart or '0'}.{frac or '0'}")
    except ValueError:
        return None
    return round(-val if neg else val, 2)


def money_close(a: float, b: float) -> bool:
    """Deux montants (valeurs absolues) sont-ils égaux à la tolérance près ?"""
    a, b = abs(a), abs(b)
    return abs(a - b) <= max(AMOUNT_TOL_ABS, AMOUNT_TOL_PCT * max(a, b))


# --------------------------------------------------------------------------- #
# Dates                                                                        #
# --------------------------------------------------------------------------- #

_DATE_FORMATS = [
    "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y",
    "%Y/%m/%d", "%d/%m/%y", "%Y%m%d", "%d %m %Y",
]


def parse_date(raw) -> str | None:
    """Renvoie une date ISO 'YYYY-MM-DD' ou None."""
    if not raw:
        return None
    s = str(raw).strip()[:10] if "T" in str(raw) else str(raw).strip()
    s = s.replace("T", " ").split(" ")[0]
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            continue
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else None


def period_of(iso_date: str | None) -> str | None:
    """'YYYY-MM' à partir d'une date ISO, sinon None."""
    return iso_date[:7] if iso_date and re.match(r"\d{4}-\d{2}-\d{2}", iso_date) else None


def days_between(a: str | None, b: str | None) -> int | None:
    da, db = parse_date(a), parse_date(b)
    if not da or not db:
        return None
    return abs((date.fromisoformat(da) - date.fromisoformat(db)).days)


# --------------------------------------------------------------------------- #
# Similarité de noms / libellés                                                #
# --------------------------------------------------------------------------- #

_STOP = {"sarl", "sas", "sa", "eurl", "sasu", "sci", "ei", "the", "and", "et",
         "de", "du", "des", "le", "la", "les", "vir", "virement", "prlv",
         "prelevement", "cb", "carte", "paiement", "fact", "facture", "ref"}


def _tokens(s: str) -> set[str]:
    s = strip_accents((s or "").lower())
    return {t for t in re.split(r"[^a-z0-9]+", s) if len(t) > 2 and t not in _STOP}


def name_similarity(a: str, b: str) -> float:
    """Similarité 0..1 indépendante de l'ordre/casse/civilité.

    Combine Jaccard sur tokens significatifs et ratio de séquence ; on prend le max
    pour ne pas pénaliser un libellé bancaire qui ne contient qu'un fragment du nom.
    """
    ta, tb = _tokens(a), _tokens(b)
    jacc = len(ta & tb) / len(ta | tb) if (ta or tb) else 0.0
    seq = difflib.SequenceMatcher(
        None, strip_accents((a or "").lower()), strip_accents((b or "").lower())
    ).ratio()
    # Si tous les tokens du plus court sont inclus dans l'autre -> forte similarité.
    contained = 0.0
    if ta and tb:
        small, big = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
        contained = len(small & big) / len(small)
    return max(jacc, contained * 0.95, seq * 0.8)


# --------------------------------------------------------------------------- #
# Références de facture dans un libellé bancaire                               #
# --------------------------------------------------------------------------- #

# "REF AQ-2026-041", "FACT 2026-041", "FACTURE: FA-1203", préfixe collé "FAC-2024-012".
_REF_MARKED = re.compile(
    r"\b(?:REF|R[EÉ]F[EÉ]RENCE|FACT|FACTURE|FCT|INV|INVOICE)\b[\s:#./-]*([A-Z0-9][A-Z0-9./-]{2,})",
    re.I,
)
_REF_GLUED = re.compile(r"\b(FA[CT]?-?\d{2,}[-/]?\d{0,4}[-/]?\d{0,4})\b", re.I)


def extract_invoice_ref(label: str) -> str | None:
    """Extrait une référence de facture citée dans un libellé bancaire, sinon None.

    Volontairement conservateur : on ne veut pas confondre un mandat SEPA
    (RUM, ICS, BMS-…) avec une référence de facture.
    """
    if not label:
        return None
    m = _REF_MARKED.search(label)
    if m:
        cand = m.group(1).strip(" .:-/")
        if not re.fullmatch(r"\d{1,2}", cand):  # un simple "REF 12" n'est pas une réf de facture
            return cand.upper()
    m = _REF_GLUED.search(label)
    if m:
        return m.group(1).upper()
    return None


def ref_match(invoice_id: str, label: str) -> bool:
    """Le libellé cite-t-il explicitement cet invoice_id ?"""
    if not invoice_id or not label:
        return False
    norm = lambda s: re.sub(r"[^a-z0-9]", "", strip_accents(s).lower())
    nid = norm(invoice_id)
    return len(nid) >= 4 and nid in norm(label)


# --------------------------------------------------------------------------- #
# Catégories NON FACTURABLES (sorties dans excluded_bank_lines)                #
# --------------------------------------------------------------------------- #
# Une opération non facturable n'a PAS de facture en face par nature (salaire,
# impôt, frais bancaire, retrait…). On l'écarte du matching ET des anomalies
# (sinon flot de faux "facture_manquante"/"paiement_orphelin"). Détection sur le
# libellé, insensible aux accents/casse. Ordre = du plus spécifique au plus large.
_NON_BILLABLE = [
    ("impots_taxes", [
        "dgfip", "ddfip", "tresor public", "impot", "impots", "service des impots",
        "prelevement a la source", "pas impot", "tva ", "acompte tva", "cfe", "cvae",
        "taxe fonciere", "taxe", "amende", "das2", "fisc"]),
    ("prestations_sociales", [
        "urssaf", "cpam", "caf ", "pole emploi", "retraite", "agirc", "arrco",
        "mutuelle", "prevoyance", "msa", "rsi ", "cipav", "carsat", "charges sociales",
        "cotisations sociales", "secu", "securite sociale"]),
    ("rh_charges", [
        "salaire", "salaires", "remuneration", "bulletin de paie", "paie ", "paye ",
        "acompte salaire", "acompte sur salaire", "vir salaire", "net a payer"]),
    ("frais_bancaires", [
        "frais bancaire", "frais bancaires", "frais de tenue", "tenue de compte",
        "commission", "cotisation carte", "cotisation jazz", "cotisation", "agios",
        "interets debiteurs", "abonnement", "frais carte", "frais d'incident",
        "frais de rejet", "frais virement", "frais d'opposition"]),
    ("especes", [
        "retrait", "retrait dab", "retrait especes", "retrait esp", "depot especes",
        "depot esp", "versement especes", "distributeur", "dab ", "remise especes"]),
    ("transfert_interne", [
        "virement interne", "vir interne", "compte a compte", "transfert interne",
        "vers livret", "alim. epargne", "alimentation epargne", "vir epargne",
        "livret a", "ldd"]),
    # virement_particulier : volontairement NON auto-détecté (un virement nominatif
    # peut être un vrai paiement client) ; à poser manuellement dans un sidecar si besoin.
]


def classify_non_billable(label: str) -> str | None:
    """Renvoie la famille non facturable d'un libellé, ou None si potentiellement facturable."""
    if not label:
        return None
    norm = " " + strip_accents(label.lower()) + " "
    for category, keywords in _NON_BILLABLE:
        for kw in keywords:
            if kw in norm:
                return category
    return None
