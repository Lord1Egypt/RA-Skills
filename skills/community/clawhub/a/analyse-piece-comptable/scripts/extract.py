#!/usr/bin/env python3
"""
Extraction DÉTERMINISTE des champs d'un document comptable.

Usage :
  python3 extract.py <fichier.pdf>

Sortie : un objet JSON sur stdout. Champs introuvables → null.
L'appelant ne devine JAMAIS : si un champ obligatoire est null,
il classe en needs_review (et n'invente ni montant ni numéro).

  invoice :
    {"kind":"invoice","invoice_id","issue_date","due_date",
     "total_ht","tva_rate","tva_amount","total_ttc",
     "emitter","recipient","siren_found":[...]}

  bank-statement :
    {"kind":"bank-statement","holder","iban","bank",
     "period_start","period_end","opening_balance","closing_balance",
     "operations":[{"date","label","amount","invoice_ref"}]}

  autre : {"kind":"other"}

----------------------------------------------------------------------
Notes d'implémentation (v0.3) — extraction des relevés bancaires
----------------------------------------------------------------------
Le parsing du relevé n'est plus une regex unique « montant en fin de
ligne » (qui capturait le SOLDE au lieu du montant dès qu'une colonne
Solde suivait, et ignorait les colonnes Débit/Crédit séparées). Il
fonctionne désormais comme le mapping de colonnes du skill chinois :

  1. détection de l'en-tête du tableau (Date / Libellé / Débit / Crédit
     / Montant / Solde) et de la position de chaque colonne ;
  2. pour chaque ligne de données, repérage de TOUS les montants (formats
     FR « 1 234,56 » et anglo « 1,234.56 ») avec leur position ;
  3. la colonne Solde (dernier montant) est écartée, jamais confondue
     avec le montant de l'opération ;
  4. le signe est déduit, par ordre de fiabilité :
       a. variation du solde (delta) — signal le plus fiable,
       b. flag explicite CR/DB/CRÉDIT/DÉBIT,
       c. position relative aux colonnes Débit/Crédit,
       d. signe propre du token (parenthèses / « - »).
Si aucun en-tête n'est détecté, on retombe sur une heuristique
« dernier montant = solde » quand les lignes ont ≥ 2 montants.
"""

import json
import re
import subprocess
import sys

BANKS = ["BNP PARIBAS", "CRÉDIT AGRICOLE", "CREDIT AGRICOLE", "SOCIÉTÉ GÉNÉRALE",
         "SOCIETE GENERALE", "LA BANQUE POSTALE", "CIC", "LCL", "HSBC",
         "CAISSE D'ÉPARGNE", "CAISSE D'EPARGNE", "BANQUE POPULAIRE",
         "QONTO", "BOURSORAMA", "REVOLUT", "N26", "FORTUNEO", "HELLO BANK"]
BANK_TOKENS = ("BNP", "AGRICOLE", "GÉNÉRALE", "GENERALE", "POSTALE", "CIC",
               "LCL", "HSBC", "ÉPARGNE", "EPARGNE", "POPULAIRE", "QONTO",
               "BOURSORAMA", "REVOLUT", "FORTUNEO")

INVOICE_ID_RE = re.compile(
    r"\b([A-Z]{1,4}\d{0,3}-\d{2,4}-\d{2,8}(?:-\d{1,8})?|[A-Z]{2,4}\d{4,12}|\d{4}-\d{2,8})\b")

# Une date complète : 03/04/2026, 03-04-2026, 03.04.2026, 03/04/26
DATE_TOKEN = r"\d{1,2}[/.\-]\d{1,2}[/.\-]\d{2,4}"
DATE_RE = re.compile(DATE_TOKEN)
# Une date d'opération, AVEC ou SANS année : beaucoup de banques (Qonto, Crédit
# Agricole, Caisse d'Épargne, LCL…) datent en « 16/07 » ou « 26.09 » sans année
# sur la ligne — l'année vient de la période / de l'en-tête.
DATE_ANY = r"\d{1,2}[/.\-]\d{1,2}(?:[/.\-]\d{2,4})?"

# Un montant : « 1 234,56 », « 1.234,56 », « 1,234.56 », « 1234.56 », « -84,50 »,
# « (100,00) ». Exige une partie décimale à 2 chiffres pour ne pas confondre
# avec un numéro de référence ou une année.
MONEY_RE = re.compile(r"\(?-?(?:\d{1,3}(?:[ .,]\d{3})*|\d+)[.,]\d{2}\)?")
# Montant PERMISSIF : tolère l'absence de décimales (« 3600 ») ou 1 décimale
# (« 1847,2 »), en plus des formes complètes. N'est utilisé QU'EN REPLI et QUE dans
# les colonnes de montant détectées (sinon il capterait n° de chèque, réf, année).
LOOSE_MONEY_RE = re.compile(r"-?\d{1,3}(?:[ .]\d{3})+(?:,\d{1,2})?|-?\d+(?:[.,]\d{1,2})?")


# ── Helpers ───────────────────────────────────────────────────────────────

def _text_unusable(text):
    """Couche texte inexploitable : vide, trop courte, ou « explosée » caractère
    par caractère (certains PDF bancaires, ex. BNP, placent chaque glyphe →
    pdftotext rend « P | . | 1 | / »). Dans ces cas il faut OCRiser."""
    t = (text or "").strip()
    if len(t) < 80:
        return True
    words = t.split()
    if not words:
        return True
    single = sum(1 for w in words if len(w) == 1)
    return single / len(words) > 0.45


def _tsv_to_layout(tsv):
    """Reconstruit un texte aligné en COLONNES à partir des coordonnées (boîtes
    englobantes) des mots données par tesseract en TSV. But : restituer la
    géométrie du tableau (donc les colonnes Débit/Crédit, repérables ensuite par
    position) au lieu d'un texte à plat qui perdrait l'alignement — c'est ce qui
    permet de déterminer le signe d'un montant scanné par sa COLONNE, pas par son
    libellé."""
    from collections import defaultdict
    words = []   # (line_key, top, left, text)
    for row in tsv.splitlines():
        f = row.split("\t")
        if len(f) < 12 or f[0] != "5":          # niveau 5 = mot
            continue
        try:
            left, top, width = int(f[6]), int(f[7]), int(f[8])
            conf = float(f[10])
        except ValueError:
            continue
        text = f[11]
        if not text.strip() or conf < 30:
            continue
        words.append(((int(f[2]), int(f[3]), int(f[4])), top, left, width, text))
    if not words:
        return ""
    # largeur d'un caractère ≈ médiane de (largeur_mot / nb_caractères)
    ratios = sorted(w / len(t) for _, _, _, w, t in words if len(t) >= 2)
    cw = max(ratios[len(ratios) // 2] if ratios else 14.0, 1.0)
    lines = defaultdict(list)
    tops = {}
    for key, top, left, width, text in words:
        lines[key].append((left, text))
        tops[key] = min(tops.get(key, top), top)
    out = []
    for key in sorted(lines, key=lambda k: tops[k]):
        s = ""
        for left, text in sorted(lines[key]):
            col = int(round(left / cw))
            if col < len(s):
                col = len(s) + 1
            s += " " * (col - len(s)) + text
        out.append(s)
    return "\n".join(out)


def ocr_pdf(path, dpi=300, max_pages=10):
    """OCR déterministe (tesseract -l fra) via rasterisation pdftoppm. Utilisé
    quand la couche texte est inexploitable (PDF scanné ou texte explosé).
    Sortie TSV (coordonnées) → texte aligné en colonnes pour préserver le
    tableau. Renvoie '' si l'OCR n'est pas disponible."""
    import os
    import tempfile
    out = []
    with tempfile.TemporaryDirectory() as td:
        prefix = os.path.join(td, "p")
        try:
            subprocess.run(["pdftoppm", "-png", "-r", str(dpi), "-l", str(max_pages),
                            str(path), prefix], capture_output=True, timeout=180)
        except Exception:
            return ""
        for png in sorted(f for f in os.listdir(td) if f.endswith(".png")):
            try:
                r = subprocess.run(
                    ["tesseract", os.path.join(td, png), "stdout", "-l", "fra", "--psm", "6", "tsv"],
                    capture_output=True, text=True, errors="ignore", timeout=120)
                out.append(_tsv_to_layout(r.stdout))
            except Exception:
                continue
    return "\n".join(out)


def _normalize(text):
    """Normalise les caractères de la zone à usage privé (U+E000–U+F8FF) en
    espaces : certaines polices bancaires (ex. Crédit Agricole) y mappent le
    glyphe d'espace → « Anciensoldeau » casserait toute la lecture."""
    return re.sub("[\ue000-\uf8ff]", " ", text) if text else text


def pdftext(path):
    """Texte du PDF. `-layout` préserve les colonnes (idéal pour les relevés).
    Repli sur `-raw`, puis OCR si la couche texte est inexploitable."""
    best = ""
    for args in (["-layout"], ["-raw"], []):
        try:
            r = subprocess.run(["pdftotext", *args, str(path), "-"],
                               capture_output=True, text=True, errors="ignore", timeout=30)
        except Exception:
            continue
        out = _normalize(r.stdout)
        if out and not _text_unusable(out):
            return out
        best = best or out
    # couche texte inexploitable → OCR (déterministe, tesseract)
    ocr = ocr_pdf(path)
    if ocr and not _text_unusable(ocr):
        return ocr
    return best or ocr


def parse_money(s):
    """Parse un montant FR ou anglo en float signé. None si illisible."""
    if s is None:
        return None
    s = s.replace("\xa0", " ").strip()
    neg = s.startswith("-") or (s.startswith("(") and s.rstrip().endswith(")"))
    m = re.search(r"\d[\d .,]*\d|\d", s)
    if not m:
        return None
    tok = m.group(0).replace(" ", "")
    if "," in tok and "." in tok:
        # le dernier séparateur est le décimal
        if tok.rfind(",") > tok.rfind("."):
            tok = tok.replace(".", "").replace(",", ".")
        else:
            tok = tok.replace(",", "")
    elif "," in tok:
        # virgule décimale si « ,d » ou « ,dd » en fin et une seule virgule, sinon
        # milliers (« 1 847,2 » et « 1 847,20 » sont décimaux ; « 1,234 » = milliers).
        if tok.count(",") == 1 and re.search(r",\d{1,2}$", tok):
            tok = tok.replace(",", ".")
        else:
            tok = tok.replace(",", "")
    elif "." in tok:
        # point décimal seulement si « .d »/« .dd » unique en fin, sinon milliers
        if not (tok.count(".") == 1 and re.search(r"\.\d{1,2}$", tok)):
            tok = tok.replace(".", "")
    try:
        v = round(float(tok), 2)
    except ValueError:
        return None
    return -v if (neg and v > 0) else v


def amount_after(label_re, text, lookahead=2, last=False):
    """Montant associé à un label. Sur la ligne du label : le montant le plus
    à droite (colonne total). Sinon, regarde jusqu'à `lookahead` lignes en
    dessous (cas « Total TTC » suivi du montant à la ligne suivante).
    `last=True` → renvoie le montant du DERNIER label correspondant (utile pour
    un solde de clôture quand ouverture et clôture portent le même libellé
    « Solde au … »)."""
    lines = text.splitlines()
    result = None
    for i, line in enumerate(lines):
        if not re.search(label_re, line, re.IGNORECASE):
            continue
        for j in range(i, min(i + 1 + lookahead, len(lines))):
            found = [parse_money(m.group(0))
                     for m in MONEY_RE.finditer(lines[j].replace("\xa0", " "))]
            found = [f for f in found if f is not None]
            if found:
                result = found[-1] if j == i else found[0]
                break
        if result is not None and not last:
            return result
    return result


def iso_date(s):
    m = re.match(r"(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2,4})", s.strip())
    if not m:
        return None
    d, mo, y = m.group(1), m.group(2), int(m.group(3))
    if y < 100:
        y += 2000
    try:
        return f"{y:04d}-{int(mo):02d}-{int(d):02d}"
    except ValueError:
        return None


def date_after(label_re, text):
    for line in text.splitlines():
        if re.search(label_re, line, re.IGNORECASE):
            m = DATE_RE.search(line)
            if m:
                return iso_date(m.group(0))
    return None


def first_date(text):
    m = DATE_RE.search(text)
    return iso_date(m.group(0)) if m else None


def extract_invoice_ref(label):
    """N° de facture cité dans un libellé bancaire. Deux formes reconnues :
      (a) marqueur explicite « REF/FACT/FACTURE <id> » → on capte l'id qui suit ;
      (b) numéro préfixé collé « FAC-2024-012 » / « FA-2024-… » → on capte le tout.
    On EXIGE un marqueur ou le préfixe FAC/FA : un mandat SEPA d'un autre préfixe
    (BMS-…, URK…) n'est donc PAS pris pour une réf facture (→ pas de fausse
    'facture_manquante'). Garde-fou final : pas un n° de TVA/SIREN/SIRET."""
    m = re.search(r"\b(?:R[ÉE]F|FACTURE|FACT)\b[\s.:#/\-]+([A-Za-z]{0,4}-?\d[\dA-Za-z\-/]{2,})",
                  label, re.IGNORECASE)
    if not m:
        m = re.search(r"\b((?:FACT?|FA)-?\d[\dA-Za-z\-/]{2,})", label, re.IGNORECASE)
    if not m:
        return None
    ref = m.group(1).strip(" .:;-/")
    return ref if not _is_bad_invoice_id(ref) else None


def siren_list(text):
    return re.findall(r"\b\d{3}\s?\d{3}\s?\d{3}\b", text)


def printed_totals(text):
    """Totaux imprimés « Total des opérations <débit> <crédit> » d'un relevé.
    Permettent de réconcilier via les TOTAUX, sans dépendre du signe de chaque
    ligne (utile quand des colonnes dérivent entre pages). → (débit, crédit)."""
    for line in text.splitlines():
        if re.search(r"TOTAL\s*DES\s*OP[ÉE]RATIONS", line, re.I):
            amts = [parse_money(m.group(0)) for m in MONEY_RE.finditer(line.replace("\xa0", " "))]
            amts = [a for a in amts if a is not None]
            if len(amts) >= 2:
                return abs(amts[-2]), abs(amts[-1])
    return None


def _is_bad_invoice_id(cand):
    """True si `cand` ne peut pas être un n° de facture : mot réservé, trop court,
    purement numérique court, n° de TVA intracom (FR+11 chiffres) ou SIREN/SIRET
    (9 / 14 chiffres). Ces derniers figurent en en-tête et seraient capturés à tort."""
    if not cand or len(cand) < 3:
        return True
    u = cand.upper()
    if u in ("TVA", "SIRET", "SIREN", "HT", "TTC", "FR", "BIC", "IBAN"):
        return True
    if re.match(r"^\d{1,3}$", cand):
        return True
    if re.match(r"^FR\d{11}$", u):          # TVA intracommunautaire
        return True
    if re.match(r"^\d{9}$|^\d{14}$", cand):  # SIREN / SIRET
        return True
    return False


# ── Classification ────────────────────────────────────────────────────────

def looks_like_statement(t):
    up = t.upper()
    if "RELEVÉ DE COMPTE" in up or "RELEVE DE COMPTE" in up or "ACCOUNT STATEMENT" in up:
        return True
    if "RELEVÉ BANCAIRE" in up or "EXTRAIT DE COMPTE" in up:
        return True
    if "SOLDE D'OUVERTURE" in up or "SOLDE DE CLÔTURE" in up or "SOLDE DE CLOTURE" in up:
        return True
    if any(b in up for b in BANKS) and ("RELEVÉ" in up or "RELEVE" in up):
        return True
    # « Relevé » (même minuscule) + un mot de compte → relevé (ex. Caisse d'Épargne)
    if ("RELEV" in up) and ("COMPTE" in up or re.search(r"OP[ÉE]RATION", up) or "IBAN" in up):
        return True
    # IBAN + nom de banque + table d'opérations probable
    if "IBAN" in up and any(b in up for b in BANKS) and ("SOLDE" in up or "OP" in up):
        return True
    return False


def has_invoice_guard(t):
    """Vrai si le document est clairement une pièce commerciale (facture, ticket,
    reçu de don/fiscal, quittance…) et NON un relevé bancaire — même quand un bloc
    RIB/IBAN y figure. Un reçu de don imprime souvent le RIB du bénéficiaire, ce
    qui déclenchait à tort `looks_like_statement` (« RELEV… » + IBAN) et envoyait
    le doc vers l'extracteur de relevé (→ « aucune_operation » → vision inutile)."""
    up = t.upper()
    title = any(k in up for k in (
        "FACTURE", "INVOICE", "BON DE FACTURATION", "TICKET",
        "RECU DE DON", "REÇU DE DON", "RECU FISCAL", "REÇU FISCAL",
        "QUITTANCE", "NOTE DE FRAIS"))
    ident = ("SIRET" in up) or ("TVA" in up)
    total = any(k in up for k in ("TOTAL TTC", "NET À PAYER", "NET A PAYER", "TOTAL HT"))
    return title and (ident or total)


def is_ticket(t):
    """Ticket de caisse : pièce sans n° de facture, total imprimé en pied
    (« TOTAL 50,00 EUR ») et marqueurs caisse (carte bancaire, « merci de votre
    visite »…). Traité comme une facture, mais avec son propre template."""
    up = t.upper()
    return bool(re.search(r"\bTICKET\b|TICKET DE CAISSE|MERCI DE VOTRE VISITE", up)
                or ("CARTE BANCAIRE" in up and "TOTAL HT" in up and "TOTAL TTC" not in up))


def looks_like_expense(t):
    """Note de frais : pièce de remboursement d'un salarié (déplacement, repas…).
    Distincte d'une facture commerciale — routée AVANT looks_like_invoice (qui
    matche aussi « NOTE DE FRAIS ») pour lui appliquer son propre template."""
    up = t.upper()
    keys = ("NOTE DE FRAIS", "NOTES DE FRAIS", "FRAIS PROFESSIONNELS",
            "FRAIS DE DÉPLACEMENT", "FRAIS DE DEPLACEMENT",
            "REMBOURSEMENT DE FRAIS", "EXPENSE REPORT")
    return any(k in up for k in keys)


def looks_like_invoice(t):
    up = t.upper()
    score = 0
    if "FACTURE" in up or "INVOICE" in up or "BON DE FACTURATION" in up or "BILL" in up:
        score += 1
    # autres pièces commerciales assimilées à une facture (templates dédiés)
    if ("RECU DE DON" in up or "REÇU DE DON" in up or "RECU FISCAL" in up or "REÇU FISCAL" in up
            or "TICKET" in up or "QUITTANCE" in up or "NOTE DE FRAIS" in up or "AVOIR" in up):
        score += 1
    if "SIRET" in up or re.search(r"N°?\s*TVA", up) or "SIREN" in up:
        score += 1
    if "FACTURÉ À" in up or "FACTURE A" in up or "DESTINATAIRE" in up or "BILL TO" in up or "\nCLIENT" in up:
        score += 1
    if "TOTAL TTC" in up or "NET À PAYER" in up or "TOTAL HT" in up or "NET A PAYER" in up or re.search(r"^\s*TOTAL\b", up, re.M):
        score += 1
    return score >= 2


# ── Extraction facture ────────────────────────────────────────────────────

def company_before_siret(text):
    """Première ligne « réelle » = nom du vendeur (avant le 1er SIRET)."""
    seen_lines = text.splitlines()
    for l in seen_lines[:15]:
        chunk = re.split(r"\s{2,}", l.strip())[0].strip().strip(":")
        if not chunk or len(chunk) < 3:
            continue
        if re.match(r"(FACTURE|INVOICE|BON DE FACTURATION)\b", chunk, re.I):
            continue
        if re.search(r"^\d", chunk):
            continue
        if not re.search(r"[A-Za-zÀ-ÿ]{3,}", chunk):
            continue
        return chunk
    return None


def recipient_block(text):
    lines = text.splitlines()
    label_re = re.compile(r"FACTUR[ÉE]\s*[ÀA]\b|DESTINATAIRE\b|BILL\s*TO\b|^\s*CLIENT\b", re.I)
    for i, l in enumerate(lines):
        if not label_re.search(l):
            continue
        after = label_re.split(l)[-1].strip().lstrip(":").strip()
        candidates = ([after] if after else []) + [lines[j].strip() for j in range(i + 1, min(i + 5, len(lines)))]
        for c in candidates:
            parts = [p.strip() for p in re.split(r"\s{2,}", c) if p.strip()]
            for p in reversed(parts):  # le destinataire est dans la colonne de droite
                if len(p) < 3:
                    continue
                if re.match(r"(ÉCHÉANCE|ECHEANCE|SIRET|N°|TVA|RÈGLEMENT|REGLEMENT)\b", p, re.I):
                    continue
                if re.match(r"^[\d\s/.,€-]+$", p):
                    continue
                if re.search(r"[A-Za-zÀ-ÿ]{3,}", p):
                    return p
    return None


def extract_invoice(text):
    inv_id = None
    # Ordre des patterns : du plus strict (forme structurée) au plus large.
    # Critique : « FACTURE … N° X » avec N° optionnel matchait à tort le N de
    # « Numérix » (sur la ligne d'après FACTURE), d'où la capture « umérix »
    # observée en prod. → On exige `N°` strict et un id structuré en tête.
    for pat in (
        # 1) Forme structurée standard : "N° F1-2026-0001", "N° F-2026-03-007"
        #    (3e segment optionnel : année-mois-séquence comme F-2026-03-007)
        r"\bN\s*[°O]\s*([A-Z]{1,4}\d{0,3}[\-/]\d{2,4}[\-/]\d{2,8}(?:[\-/]\d{1,8})?)\b",
        # 2) "FACTURE … N° X" avec X structuré (filet pour layouts exotiques)
        r"\bFACTURE\b[\s\S]{0,200}?\bN\s*[°O]\s*([A-Z]{1,4}\d{0,3}[\-/]\d{2,4}[\-/]\d{2,8}(?:[\-/]\d{1,8})?)\b",
        # 3) "Facture : X" / "Facture # X" — séparateur explicite
        r"\bFACTURE\s*[:#]\s*([A-Za-z0-9][\w\-/]{2,})",
        # 4) "Réf. facture : X"
        r"\bR[ÉE]F\.?\s*FACTURE\s*[:\-]?\s*([A-Za-z0-9][\w\-/]{2,})",
        # 5) Filet de sécurité : "N° X" forme compacte sans tirets
        r"\bN\s*[°O]\s*([A-Z]{2,4}\d{4,12})\b",
    ):
        m = re.search(pat, text, re.I)
        if m:
            inv_id = m.group(1).strip().strip(".:,")
            break
    if not inv_id:
        # Filet : 1er identifiant structuré qui n'est PAS un n° de TVA / SIREN /
        # SIRET (ils apparaissent en en-tête et seraient sinon capturés à tort).
        for m in INVOICE_ID_RE.finditer(text):
            cand = m.group(1)
            if not _is_bad_invoice_id(cand):
                inv_id = cand
                break
    if inv_id and _is_bad_invoice_id(inv_id):
        inv_id = None

    # `last=True` : sur une facture, « Total HT » apparaît en EN-TÊTE de colonne
    # PUIS en ligne récapitulative (« Total HT : 4 050,00 »). On veut le total
    # récap (le dernier), pas un montant de ligne attrapé sous l'en-tête.
    total_ttc = amount_after(r"NET\s*[ÀA]\s*PAYER|TOTAL\s*TTC|MONTANT\s*TTC|TOTAL\s*[ÀA]\s*PAYER", text, last=True)
    total_ht = amount_after(r"TOTAL\s*HT|SOUS-?TOTAL\s*HT|MONTANT\s*HT|TOTAL\s*H\.?T\.?|BASE\s*HT", text, last=True)
    tva_amount = amount_after(r"(?<!N°\s)(?<!N° )\b(?:TVA|T\.V\.A\.|MONTANT\s*TVA)\b(?!\s*INTRA)", text, last=True)

    tva_rate = None
    mr = re.search(r"TVA\s*\(?\s*([\d,\.]+)\s*%", text, re.I) or re.search(r"TAUX\s*(?:TVA)?\s*:?\s*([\d,\.]+)\s*%", text, re.I)
    if mr:
        try:
            tva_rate = round(float(mr.group(1).replace(",", ".")) / 100, 4)
        except ValueError:
            pass
    up = text.upper()
    if tva_rate is None and ("TVA NON APPLICABLE" in up or "EXONÉR" in up or "EXONER" in up
                             or "ART. 261" in up or "ART 261" in up or "ART. 293" in up or "ART 293" in up):
        tva_rate = 0.0
        if tva_amount is None:
            tva_amount = 0.0

    # Multi-taux : plusieurs taux de TVA distincts cités sur des lignes « TVA … % »
    # (ex. resto 10 % + 20 %). Le contrôle mono-taux (HT × taux) serait alors faux —
    # on le neutralise en aval (évite une anomalie tva_incorrecte BLOQUANTE à tort).
    # Détection bornée au contexte TVA pour ne pas confondre avec une remise « -10 % ».
    _vat_rates = set()
    for _l in text.splitlines():
        if re.search(r"TVA|T\.V\.A", _l, re.I):
            for _r in re.findall(r"(\d{1,2}(?:[.,]\d{1,2})?)\s*%", _l):
                _vat_rates.add(_r.replace(",", "."))
    tva_multi = len(_vat_rates) > 1

    # ── Template TICKET DE CAISSE ─────────────────────────────────────────
    # Un ticket n'a pas de « TOTAL TTC » : le net est une ligne « TOTAL 50,00 EUR »
    # (à NE PAS confondre avec « Total HT » / « TVA »). On prend la DERNIÈRE ligne
    # TOTAL (le récap en pied), puis on retombe sur HT + TVA si besoin.
    if total_ttc is None:
        for line in text.splitlines():
            u = line.upper()
            if "TOTAL" not in u or "SOUS-TOTAL" in u or "SOUS TOTAL" in u:
                continue
            if re.search(r"TOTAL\s*(?:H\.?T|TVA|T\.V\.A)", u):
                continue
            m = re.search(r"([\d  ]{1,12}[.,]\d{2})\s*(?:EUR|€)?\s*$", line)
            if m:
                val = parse_money(m.group(1))
                if val is not None:
                    total_ttc = val          # la dernière ligne TOTAL gagne
    if total_ttc is None and total_ht is not None and tva_amount is not None:
        total_ttc = round(total_ht + tva_amount, 2)   # repli arithmétique HT + TVA

    issue_date = date_after(r"\bDATE\b\s*:", text) or date_after(r"\bDATE\b", text) or first_date(text)

    # Ticket sans n° : id de suivi déterministe (émetteur + date + montant).
    # Le rapprochement Pass 2 matche sur montant + contrepartie, pas sur ce n°,
    # donc un id synthétique suffit à tracer/réconcilier le ticket sans vision.
    if not inv_id and total_ttc is not None and is_ticket(text):
        emit = company_before_siret(text) or "TICKET"
        slug = re.sub(r"[^A-Za-z0-9]+", "", emit)[:12].upper() or "TICKET"
        inv_id = f"TCK-{slug}-{issue_date or '0000-00-00'}-{total_ttc:.2f}"

    return {
        "kind": "invoice",
        "invoice_id": inv_id,
        "issue_date": issue_date,
        "due_date": date_after(r"ÉCHÉANCE|ECHEANCE|[ÀA]\s*RÉGLER\s*AVANT|[ÀA]\s*REGLER\s*AVANT|DATE\s*LIMITE", text),
        "total_ht": total_ht,
        "tva_rate": tva_rate,
        "tva_amount": tva_amount,
        "tva_multi": tva_multi,
        "total_ttc": total_ttc,
        "emitter": company_before_siret(text),
        "recipient": recipient_block(text),
        "siren_found": siren_list(text),
    }


# ── Extraction note de frais ──────────────────────────────────────────────
# Greffé depuis le module `analyse-piece-comptable` de Thomas. Une note de frais
# est rattachée à un CLIENT (l'employeur, dont on tient les comptes) ; le
# bénéficiaire est le salarié remboursé. Côté rapprochement, elle se comporte
# comme un achat (type "in") : un décaissement (remboursement / paiement carte).

_LEGAL_FORMS = ("SARL", "SASU", "SAS", "EURL", "SELARL", "SCOP", "EIRL",
                "SCI", "SNC", "SA")


def company_on_document(text):
    """Société émettrice de la note (= entité dont on tient les comptes).
    Priorité à une ligne portant une forme juridique, sinon le bloc avant le SIRET."""
    lf = re.compile(r"\b(" + "|".join(_LEGAL_FORMS) + r")\b")
    for l in text.splitlines()[:15]:
        for chunk in re.split(r"\s{2,}", l.strip()):
            chunk = chunk.strip(" :")
            if len(chunk) < 4 or not re.search(r"[A-Za-zÀ-ÿ]{3,}", chunk):
                continue
            if lf.search(chunk.upper()):
                return chunk
    return company_before_siret(text)


def expense_beneficiary(text):
    """Le salarié / bénéficiaire remboursé (à ne pas confondre avec la société)."""
    for l in text.splitlines():
        m = re.search(r"\b(?:SALARI[ÉE]|B[ÉE]N[ÉE]FICIAIRE|COLLABORATEUR|EMPLOY[ÉE]"
                      r"|NOM\s+DU\s+SALARI[ÉE])\b\s*:?\s*(.+)", l, re.I)
        if m:
            val = re.split(r"\s{2,}", m.group(1).strip())[0].strip(" :")
            if val and re.search(r"[A-Za-zÀ-ÿ]{3,}", val):
                return val
    return None


def extract_expense(text):
    total = amount_after(r"TOTAL\s*[ÀA]\s*REMBOURSER|NET\s*[ÀA]\s*REMBOURSER|"
                         r"MONTANT\s*[ÀA]\s*REMBOURSER|TOTAL\s*DES\s*FRAIS|"
                         r"TOTAL\s*NOTE\s*DE\s*FRAIS|TOTAL\s*[ÀA]\s*PAYER", text, last=True)
    total_ht = amount_after(r"TOTAL\s*HT|MONTANT\s*HT", text, last=True)
    tva_amount = amount_after(r"(?<!N°\s)(?<!N° )\bTVA\b(?!\s*INTRA)", text, last=True)

    tva_rate = None
    mr = re.search(r"TVA\s*\(?\s*([\d,\.]+)\s*%", text, re.I)
    if mr:
        try:
            tva_rate = round(float(mr.group(1).replace(",", ".")) / 100, 4)
        except ValueError:
            pass

    # période (« Du … au … ») si présente, sinon date de soumission / 1re date.
    period_start = period_end = None
    mp = re.search(r"DU\s+(" + DATE_TOKEN + r")\s+AU\s+(" + DATE_TOKEN + r")", text, re.I)
    if mp:
        period_start, period_end = iso_date(mp.group(1)), iso_date(mp.group(2))
    submit = date_after(r"DATE\s+DE\s+SOUMISSION|SOUMISSION|DATE\s+D[''’]?\s*[ÉE]MISSION", text)
    issue = submit or period_end or first_date(text)

    m = re.search(r"SIRET\s*:?\s*([\d ]{14,20})", text)
    siret = m.group(1).strip() if m else None

    return {
        "kind": "note-de-frais",
        "company": company_on_document(text),
        "beneficiary": expense_beneficiary(text),
        "siret": siret,
        "siren_found": siren_list(text),
        "total_ht": total_ht,
        "tva_rate": tva_rate,
        "tva_amount": tva_amount,
        "total_ttc": total,
        "issue_date": issue,
        "period_start": period_start,
        "period_end": period_end,
    }


# ── Titulaire du relevé (nom du client) ───────────────────────────────────

# Mots qui trahissent un SLOGAN / TITRE de document / mention légale — jamais un
# nom de titulaire. (ex. Crédit Mutuel : « Une banque qui appartient à ses
# clients ».) On rejette tout candidat qui en contient un.
_HOLDER_REJECT = {
    "qui", "que", "qu", "vous", "votre", "vos", "nos", "notre", "est", "sont",
    "êtes", "etes", "appartient", "change", "ainsi", "pour", "avec", "sans",
    "tout", "toute", "tous", "toutes", "ses", "son", "mes", "mon", "ma", "ce",
    "cette", "ces", "une", "un", "merci", "bienvenue", "euros", "page",
    "relevé", "releve", "compte", "comptes", "extrait", "extraits", "banque",
    "banques", "agence", "conseiller", "client", "clients", "période", "periode",
    "société", "societe",  # « societe » seul = bruit ; les vraies sociétés ont SAS/SARL/…
    # bloc « contacts/coordonnées » de la banque (ni un nom, ni un slogan)
    "envoi", "contacts", "contact", "téléphone", "telephone", "fax", "internet",
    "mobile", "www", "espace", "messagerie", "distance", "code", "coût", "cout",
    "appel", "local", "horaires", "ouvert", "lundi", "samedi",
}
_HOLDER_HEADER = re.compile(
    r"^(RELEV|EXTRAIT|COMPTE|IBAN|BIC|PÉRIODE|PERIODE|SOLDE|ANCIEN\s|NOUVEAU\s|"
    r"DATE|VALEUR|LIBELL|MONTANT|OP[ÉE]RATION|D[ÉE]BIT|CR[ÉE]DIT|TITULAIRE|"
    r"ÉDIT|EDIT|PAGE)")
_HOLDER_CIVILITY = re.compile(r"^(M\.|MME|MLLE|MR|MONSIEUR|MADAME|MADEMOISELLE|M\s|MM\b)", re.I)
_HOLDER_COMPANY = re.compile(r"\b(SAS|SASU|SARL|EURL|SA|SCI|SNC|SCP|SELARL|EIRL|EI|SCM|SCEA|GAEC)\b")
_CIV_PREFIX = re.compile(r"^(?:M\.?|MR\.?|MME\.?|MLLE\.?|MM\.?|MONSIEUR|MADAME|MADEMOISELLE)\s+", re.I)


def _strip_civility(name):
    """Retire la civilité de tête (M / Mme / Monsieur…) : elle ne doit JAMAIS
    entrer dans le slug client (« m-ibrahim ») ni casser le rapprochement de noms
    (« M IBRAHIM » vs « IBRAHIM TAWFIK »). Garde le nom seul."""
    if not name:
        return name
    out = _CIV_PREFIX.sub("", name).strip()
    return out or name        # ne renvoie pas vide si le nom n'était QUE la civilité


def _clean_holder(p):
    """Retire le bruit collé à un nom : code client (« : 12345678 »), réf d'envoi
    (« n°7 »), pagination (« p. 1/3 »). Renvoie le nom nettoyé."""
    p = re.sub(r"\s*[:\-–]\s*\d[\d ]{2,}.*$", "", p)        # « Nom : 12345678 »
    p = re.sub(r"\bn[°ºo]\s*\d.*$", "", p, flags=re.I)       # « envoi n°7 … »
    p = re.sub(r"\bp\.?\s*\d+\s*/\s*\d+.*$", "", p, flags=re.I)  # « p. 1/3 »
    return p.strip(" .:;-–\t")


def _looks_like_holder(p):
    """`p` ressemble-t-il à un nom de titulaire (personne/société) plutôt qu'à un
    slogan / titre / mention légale / coordonnée bancaire ? Conservateur : dans le
    doute → False (le doc ira en `_incomplet` au lieu de créer un client fantôme)."""
    pu = p.upper()
    if len(p) < 4 or len(p) > 45:
        return False
    if not re.search(r"[A-Za-zÀ-ÿ]{3,}", p):
        return False
    if _HOLDER_HEADER.match(pu) or "RELEV" in pu or "EXTRAIT" in pu:
        return False
    if pu in (b.upper() for b in BANKS) or any(tok in pu for tok in BANK_TOKENS):
        return False
    if re.search(r"\d{4,}", p) or re.search(r"\d+\s*/\s*\d+", p):  # code client / pagination résiduels
        return False
    if "€" in p or re.search(r"\bEUR\b", pu) or re.search(r"[+\-]?\d+[.,]\d{2}", p):
        return False                         # montant / solde, pas un nom
    if re.match(r"^\s*\d", p) or re.search(r"\b\d{5}\b", p) or re.search(
            r"\b(RUE|AVENUE|AV|BD|BLD|BOULEVARD|IMPASSE|ALL[ÉE]E|CHEMIN|PLACE|"
            r"ROUTE|QUAI|RESIDENCE|R[ÉE]SIDENCE|CEDEX|Z[AI]|BP)\b", pu):
        return False                         # adresse (n° de rue, code postal, voie), pas un nom
    if len(re.findall(r"\b(?:M|MR|MME|MLLE|MONSIEUR|MADAME|MADEMOISELLE)\b\.?", pu)) >= 2:
        return False                         # 2+ civilités = noms jumelés (OCR brouillé) → ambigu, pas un titulaire unique
    if len(p.split()) > 5 or re.search(r"\bVOT\b", pu):
        return False                         # trop long / fragment « Vot(re) » = ligne brouillée
    words = re.findall(r"[A-Za-zÀ-ÿ0-9'&.\-]+", p)
    if any(re.fullmatch(r"\d+", w) for w in words):
        return False                         # token purement numérique (indicatif/guichet/code) → pas un nom
    if _HOLDER_COMPANY.fullmatch(pu.strip()):
        return False                         # « SARL » / « SA » seul = forme juridique, pas un nom
    low = {w.lower().strip(".'-") for w in words}
    if low & _HOLDER_REJECT:                 # un mot-outil/slogan/coordonnée présent → pas un nom
        return False
    # signaux forts : civilité (M./Mme) ou forme sociétaire (SAS/SARL…) → accepté même en 1 token
    if _HOLDER_CIVILITY.match(p) or _HOLDER_COMPANY.search(pu):
        return True
    # sinon : ≥2 mots ET « casse de nom » — chaque mot significatif commence par une
    # majuscule (NOM PRENOM, Société Dupont). Élimine les fragments de phrase/slogan
    # en minuscules (« modification s'appliquera », « périodicité mensuelle »).
    soft = {"du", "de", "des", "la", "le", "les", "et", "à", "d", "l", "aux", "au"}
    sig = [w for w in words if w.lower().strip(".'-") not in soft]
    return len(words) >= 2 and bool(sig) and all(w[:1].isupper() for w in sig if w[:1].isalpha())


_TXN_START = re.compile(r"^\s*\d{1,2}[/.]\d{1,2}([/.]\d{2,4})?\s")        # 1re ligne d'opération
_TXN_HEADER = re.compile(r"(D[ÉE]BIT.*CR[ÉE]DIT|CR[ÉE]DIT.*D[ÉE]BIT|DATE.*LIBELL)", re.I)


def _header_zone(text):
    """Lignes d'en-tête, AVANT le tableau d'opérations (où se trouve le titulaire ;
    au-delà commencent les contreparties de transactions qu'il ne faut pas confondre
    avec lui). Borne haute de sécurité : 60 lignes."""
    lines = text.splitlines()
    cut = len(lines)
    for i, l in enumerate(lines):
        if _TXN_START.match(l) or _TXN_HEADER.search(l):
            cut = i
            break
    return lines[:min(cut, 15)]


def _extract_holder(text):
    """(holder, candidats) — nom du titulaire du relevé.

    Retourne (nom, []) quand on est SÛR (ancre fiable, ou candidat unique), sinon
    (None, [candidats]) pour que l'appelant DEMANDE à l'utilisateur plutôt que
    d'inventer un client. Ancres fiables (haute confiance) :
      - TITULAIRE(S) (du compte) : X
      - X - COMPTE COURANT/CHEQUE/PRO ...
    Sinon, heuristique bornée à l'en-tête (avant le tableau d'opérations), avec
    rejet des slogans / titres / coordonnées bancaires."""
    h, cands = _extract_holder_raw(re.sub("[-]", " ", text))   # glyphes zone privée (ex. Crédit Agricole) -> espace
    return _strip_civility(h), [_strip_civility(c) for c in cands]


def _extract_holder_raw(text):
    # Ancre 1 : ligne « Titulaire(s) (du compte) : X ». On prend la PLUS LONGUE
    # occurrence valide : certains PDF tronquent le nom a une occurrence (« M IBRAHIM »)
    # et le donnent complet a une autre (« M IBRAHIM TAWFIK »).
    best = None
    for m in re.finditer(r"TITULAIRE\(?S?\)?\s*(?:DU\s*COMPTE)?\s*[:\-]?\s{1,}(\S.+)", text, re.I):
        cand = _clean_holder(re.split(r"\s{2,}|\t", m.group(1).strip())[0])
        if _looks_like_holder(cand) and (best is None or len(cand) > len(best)):
            best = cand
    if best:
        return best, []

    # Ancre 2 : « X - COMPTE COURANT/CHEQUE/PRO/DEPOT »
    mc = re.search(r"^\s*([A-ZÀ-Ÿ][\w&.'\- ]{3,40}?)\s*[-–]\s*COMPTE\s+"
                   r"(?:COURANT|CH[ÈE]QUE|PRO|PROFESSIONNEL|D[ÉE]P[ÔO]T|JOINT)",
                   text, re.I | re.M)
    if mc:
        cand = _clean_holder(mc.group(1).strip())
        if _looks_like_holder(cand):
            return cand, []

    # Heuristique bornee a l'en-tete : collecte de candidats distincts
    persons, companies, generics = [], [], []
    name_chunk = re.compile(r"[A-ZÀ-Ÿ][A-Za-zÀ-ÿ'\-]+(?:\s+[A-ZÀ-Ÿ][A-Za-zÀ-ÿ'\-]+)*$")
    for line in _header_zone(text):
        chunks = [x.strip() for x in re.split(r"\s{2,}", line) if x.strip()]
        k = 0
        while k < len(chunks):
            p = _clean_holder(chunks[k])
            j = k + 1
            while (j < len(chunks) and name_chunk.match(chunks[j])
                   and not re.search(r"\d", chunks[j]) and len(p) + len(chunks[j]) < 44):
                p = p + " " + chunks[j].strip()
                j += 1
            if _looks_like_holder(p):
                if _HOLDER_CIVILITY.match(p):
                    persons.append(p)
                elif _HOLDER_COMPANY.search(p.upper()):
                    companies.append(p)
                else:
                    generics.append(p)
                k = j
                continue
            k += 1

    # Un candidat « générique » (ni civilité ni forme sociétaire) n'est fiable que
    # s'il est dans un VRAI bloc adresse (code postal / IBAN à proximité) : c'est là
    # que figure le titulaire, jamais un slogan. Sinon → on préfère demander.
    header = "\n".join(_header_zone(text))
    has_addr = bool(re.search(r"\b\d{5}\b", header)) or "IBAN" in header.upper()

    # priorite personne (civilite) > societe > generique ; nom le plus complet d'abord
    for label, bucket in (("strong", persons), ("strong", companies), ("generic", generics)):
        uniq = sorted(dict.fromkeys(bucket), key=len, reverse=True)
        if not uniq:
            continue
        if label == "generic" and not has_addr:
            return None, uniq           # générique sans bloc adresse → suspect (slogan ?) → demander
        if len(uniq) == 1:
            return uniq[0], []
        base = uniq[0].lower()
        if all(u.lower() in base for u in uniq):
            return uniq[0], []          # variantes du meme nom -> le plus complet
        return None, uniq               # noms distincts -> demander a l'user
    return None, []


# ── Extraction relevé bancaire ────────────────────────────────────────────

def detect_columns(lines):
    """Repère la ligne d'en-tête du tableau d'opérations et la position
    (index caractère) de chaque colonne connue. Retourne {} si absente."""
    pats = {
        "date":    re.compile(r"\bDATE\b", re.I),
        "value":   re.compile(r"VALEUR", re.I),
        "label":   re.compile(r"LIBELL|OP[ÉE]RATIONS?|NATURE|D[ÉE]SIGNATION|D[ÉE]TAIL|R[ÉE]F[ÉE]RENCE", re.I),
        "debit":   re.compile(r"D[ÉE]BIT|RETRAIT|D[ÉE]PENSES?", re.I),
        "credit":  re.compile(r"CR[ÉE]DIT|VERSEMENTS?|RECETTES?|ENCAISSEMENTS?", re.I),
        "amount":  re.compile(r"MONTANT", re.I),
        "balance": re.compile(r"SOLDE|BALANCE", re.I),
    }
    best = {}
    for line in lines:
        cols = {}
        for name, pat in pats.items():
            m = pat.search(line)
            if m:
                cols[name] = m.start()
        # en-tête valide : colonnes Débit ET Crédit (le mot « Date » peut être
        # sur la ligne précédente, ex. Crédit Agricole), ou Date + Montant/Solde.
        has_dc = "debit" in cols and "credit" in cols
        strong = has_dc or ("date" in cols and ("amount" in cols or "balance" in cols))
        if strong and len(cols) > len(best):
            best = cols
    return best


def _trailing_flag(line):
    m = re.search(r"(?:^|\s)(CR[ÉE]DIT|CREDIT|D[ÉE]BIT|DEBIT|CR|DB)\s*€?\s*$", line.strip(), re.I)
    if not m:
        return None
    return "D" if m.group(1)[0].upper() == "D" else "C"


def _doc_year(text):
    """Année de référence du document : première date complète rencontrée.
    Pas de `\\b` en tête : certaines dates sont collées à un mot (« au26.09.2022 »)."""
    m = re.search(r"\d{1,2}[/.\-]\d{1,2}[/.\-](\d{4}|\d{2})\b", text)
    if not m:
        return None
    y = int(m.group(1))
    return y + 2000 if y < 100 else y


def _section_sign(norm):
    """Signe d'une section pour les relevés groupés par nature (ex. Crédit
    Mutuel : « VIREMENTS REÇUS … Sous-total : +2 099,30 € »). On n'utilise QUE
    le « Sous-total : +/- » explicite : se fier aux mots-clés (PRÉLÈVEMENTS,
    CARTE…) forcerait à tort le signe de relevés non sectionnés (ex. CIC)."""
    m = re.search(r"SOUS-?TOTAL\s*:?\s*([+\-])\s*\d", norm, re.I)
    if m:
        return 1 if m.group(1) == "+" else -1
    return None


def _infer_credit_x(raw):
    """Frontière de la colonne Crédit INFÉRÉE par géométrie, quand le relevé n'a
    pas d'en-tête « Débit/Crédit » mais place quand même débits et crédits dans
    deux bandes de position distinctes (cas fréquent des relevés scannés/OCR, ex.
    Banque Postale). On cherche le plus grand écart entre les bords droits des
    montants : si la séparation est nette, c'est la frontière débit | crédit."""
    edges = sorted(o["monies"][-1][0] + o["monies"][-1][1] for o in raw if o["monies"])
    if len(edges) < 4:
        return None
    best_gap, mid = 0.0, None
    for i in range(len(edges) - 1):
        g = edges[i + 1] - edges[i]
        if g > best_gap:
            best_gap, mid = g, (edges[i] + edges[i + 1]) / 2.0
    if mid is None or best_gap < 6:
        return None
    left = sum(1 for e in edges if e < mid)
    right = sum(1 for e in edges if e >= mid)
    return mid if left >= 1 and right >= 1 else None


# ── Profils par banque (comme les mappings du skill chinois) ────────────────
# Chaque profil ajuste, par-dessus le moteur générique : détection et patterns de
# solde ouverture/clôture. Le SIGNE est toujours déterminé par la GÉOMÉTRIE du
# tableau (colonne Débit/Crédit), jamais par les libellés — y compris pour les
# relevés scannés, où l'OCR reconstruit les colonnes (cf. `_tsv_to_layout` +
# `_infer_credit_x`). `close_last` : prendre le DERNIER solde correspondant.
_OPEN_DEFAULT = (r"SOLDE\s*D[''’]?\s*OUVERTURE|ANCIEN\s*SOLDE|SOLDE\s*PR[ÉE]C[ÉE]DENT|"
                 r"SOLDE\s*INITIAL|SOLDE\s*(?:CR[ÉE]DITEUR|D[ÉE]BITEUR)?\s*AU\s*\d|SOLDE\s*AU\s*\d")
_CLOSE_DEFAULT = r"SOLDE\s*DE\s*CL[ÔO]TURE|NOUVEAU\s*SOLDE|SOLDE\s*FINAL|SOLDE\s*[ÀA]\s*NOUVEAU"

BANK_PROFILES = [
    {"name": "qonto", "detect": r"QONTO|QNTOFRP", "sign": "auto"},
    {"name": "cic", "detect": r"\bC\.?I\.?C\.?\b|CR[ÉE]DIT\s*INDUSTRIEL|CMCIFRPP", "sign": "auto",
     "open": r"SOLDE\s*CR[ÉE]DITEUR\s*AU", "close": r"SOLDE\s*CR[ÉE]DITEUR\s*AU", "close_last": True},
    {"name": "credit-mutuel", "detect": r"CR[ÉE]DIT\s*MUTUEL|CMBRFR|\bCCM\b", "sign": "auto",
     "open": r"ANCIEN\s*SOLDE", "close": r"NOUVEAU\s*SOLDE"},
    {"name": "credit-agricole", "detect": r"CR[ÉE]DIT\s*AGRICOLE|AGRICOLE", "sign": "auto",
     "open": r"ANCIEN\s*SOLDE", "close": r"NOUVEAU\s*SOLDE"},
    {"name": "societe-generale", "detect": r"SOCI[ÉE]T[ÉE]\s*G[ÉE]N[ÉE]RALE", "sign": "auto",
     "open": r"SOLDE\s*PR[ÉE]C[ÉE]DENT", "close": r"NOUVEAU\s*SOLDE\s*AU"},
    {"name": "caisse-epargne", "detect": r"CAISSE.{0,4}[ÉE]PARGNE", "sign": "auto",
     "open": r"SOLDE\s*PR[ÉE]C[ÉE]DENT", "close": r"NOUVEAU\s*SOLDE\s*AU"},
    {"name": "lcl", "detect": r"\bLCL\b|CR[ÉE]DIT\s*LYONNAIS", "sign": "auto",
     "open": r"ANCIEN\s*SOLDE|SOLDE\s*PR[ÉE]C[ÉE]DENT|SOLDE\s*AU\s*\d", "close": r"SOLDE\s*EN\s*EUROS|NOUVEAU\s*SOLDE", "close_last": True},
    {"name": "banque-postale", "detect": r"BANQUE\s*POSTALE|LA\s*BANQUE\s*POSTALE",
     "open": r"ANCIEN\s*SOLDE", "close": r"NOUVEAU\s*SOLDE"},
    {"name": "bnp", "detect": r"BNP\s*PARIBAS|BNPAFRPP",
     "open": r"SOLDE\s*CR[ÉE]DITEUR\s*AU|ANCIEN\s*SOLDE", "close": r"NOUVEAU\s*SOLDE|SOLDE\s*CR[ÉE]DITEUR\s*AU", "close_last": True},
]


def match_profile(text):
    up = text.upper()
    for p in BANK_PROFILES:
        if re.search(p["detect"], up):
            return p
    return None


def _op_date_iso(lead_str, default_year):
    """Date d'opération en ISO depuis la zone de dates en tête de ligne.
    Année : celle d'une date complète présente (ex. la date valeur), sinon
    `default_year` (période / année du document). None si rien d'inférable."""
    dates = re.findall(DATE_ANY, lead_str)
    if not dates:
        return None
    year = None
    for d in dates:
        full = re.match(r"\d{1,2}[/.\-]\d{1,2}[/.\-](\d{2,4})$", d)
        if full:
            year = int(full.group(1))
            year = year + 2000 if year < 100 else year
            break
    fm = re.match(r"(\d{1,2})[/.\-](\d{1,2})", dates[0])
    day, mon = int(fm.group(1)), int(fm.group(2))
    if year is None:
        year = default_year
    if year is None or not (1 <= mon <= 12 and 1 <= day <= 31):
        return None
    return f"{year:04d}-{mon:02d}-{day:02d}"


def _explicit_sign(norm, pos):
    """Signe +/- explicite COLLÉ au montant (ex. Qonto « + 20.00 EUR »). On ne
    saute qu'au plus 2 espaces : sinon un « + » du libellé séparé du montant par
    le blanc de colonne (ex. CIC « PARCOURS.J+      3,00 ») serait pris à tort."""
    j, gap = pos - 1, 0
    while j >= 0 and norm[j] == " " and gap < 2:
        j -= 1
        gap += 1
    if j >= 0 and norm[j] == "+":
        return 1
    if j >= 0 and norm[j] == "-":
        return -1
    return None


def _is_section_or_total(norm):
    up = norm.upper()
    return bool(re.search(r"SOUS-?TOTAL|SOLDE|TOTAL\s+DES|REPORT|ANCIEN\s+SOLDE|NOUVEAU\s+SOLDE", up))


def _op_line_count(lines):
    n = 0
    for l in lines:
        norm = l.replace("\xa0", " ")
        if re.match(r"\s*(?:\S{1,2}\s+)?" + DATE_ANY, norm) and MONEY_RE.search(norm):
            n += 1
    return n


def first_account_region(text, open_re, close_re):
    """Relevés MULTI-COMPTES (Banque Postale, Caisse d'Épargne…) : un même PDF
    enchaîne plusieurs comptes (CCP puis Livret, etc.), chacun avec son solde
    d'ouverture/clôture. On ne réconcilie que le PREMIER compte → on borne les
    lignes d'opérations entre son solde d'ouverture et sa clôture / « Total des
    opérations ». Si la zone ne contient pas d'opérations (cas d'un récap de
    soldes en tête, ex. Qonto), on garde tout le texte."""
    lines = text.splitlines()
    io = next((i for i, l in enumerate(lines) if re.search(open_re, l, re.I)), None)
    if io is None:
        return text
    close_pat = f"(?:{close_re})|TOTAL\\s+DES\\s+OP[ÉE]RATIONS?"
    ic = next((i for i in range(io + 1, len(lines)) if re.search(close_pat, lines[i], re.I)), None)
    if ic is None:
        return text
    region = lines[io:ic + 1]
    return "\n".join(region) if _op_line_count(region) >= 1 else text


def _loose_column_amounts(norm, lead_end, cols):
    """Repli pour relevés SANS décimales : récupère les montants entiers/1-décimale
    UNIQUEMENT dans les colonnes de montant détectées (Débit/Crédit/Montant/Solde) et
    s'ils sont isolés (pas collés à une lettre/réf/date). Tout ce qui est à GAUCHE des
    colonnes de montant (libellé, réf, n° de chèque) est ignoré. Vide si pas de colonnes
    détectées (on préfère alors la vision plutôt qu'un nombre attrapé au hasard)."""
    amount_cols = [cols[k] for k in ("debit", "amount", "credit", "balance") if k in cols]
    if not amount_cols:
        return []
    zone = min(amount_cols) - 3
    out = []
    for m in LOOSE_MONEY_RE.finditer(norm):
        if m.start() < max(lead_end, zone):
            continue                       # à gauche des colonnes de montant → libellé/réf
        b = norm[m.start() - 1] if m.start() > 0 else " "
        a = norm[m.end()] if m.end() < len(norm) else " "
        if b.isalnum() or b in "-/.," or a.isalnum() or a in "-/":
            continue                       # collé à lettre/réf/date → pas un montant isolé
        v = parse_money(m.group(0))
        if v is not None:
            out.append((m.start(), len(m.group(0)), v))
    return out


def parse_operations(text, cols, default_year=None):
    lines = text.splitlines()
    has_dc = "debit" in cols and "credit" in cols
    credit_x = cols.get("credit")

    raw = []
    section = None  # signe de la section courante (relevés groupés par nature)
    for line in lines:
        norm = line.replace("\xa0", " ")
        # tolère un préfixe parasite (1-2 caractères de filigrane vertical sur le
        # bord gauche, ex. CIC/Crédit Mutuel) avant la date d'opération.
        pre = re.match(r"\s*(?:\S{1,2}\s+)?", norm)
        start = pre.end() if pre else 0
        dm = re.match(r"(" + DATE_ANY + r")", norm[start:])
        if not dm:
            sec = _section_sign(norm)
            if sec is not None:
                section = sec
            # ligne de détail (2e ligne d'un libellé) : on l'accroche à l'op
            # précédente si elle ne porte ni date, ni montant, ni en-tête/total —
            # et SI elle ne ressemble pas à un pied/haut de page (URL, « Page »,
            # titulaire, mentions légales), qui pollueraient le libellé.
            elif raw and norm.strip() and not MONEY_RE.search(norm) and not _is_section_or_total(norm):
                extra = norm.strip()
                junk = re.search(r"WWW\.|HTTP|\bPAGE\b|TITULAIRE|GARANTIE|PROTECTION\s+DES|"
                                 r"R[ÉE]LEV[ÉE]|" + DATE_ANY, extra, re.I)
                if 2 <= len(extra) <= 45 and re.search(r"[A-Za-zÀ-ÿ]{3,}", extra) and not junk:
                    raw[-1]["label"] = (raw[-1]["label"] + " " + extra).strip()
            continue
        # dates en tête (1-2) calculées AVANT les montants : les dates pointées
        # (« 26.09 », « 26.03 » — Crédit Agricole, LCL, BNP) ressemblent à des
        # montants ; on ne garde que les montants situés APRÈS la zone de dates.
        lead = re.match(r"(?:\s*" + DATE_ANY + r"){1,2}", norm[start:])
        lead_end = start + (lead.end() if lead else dm.end())
        date = _op_date_iso(norm[start:lead_end], default_year)
        if not date:
            continue
        monies = [(m.start(), len(m.group(0)), parse_money(m.group(0)))
                  for m in MONEY_RE.finditer(norm) if m.start() >= lead_end]
        monies = [(pos, ln, v) for pos, ln, v in monies if v is not None]
        if not monies:
            # repli « relevé sans décimales » : montants entiers/1-décimale, captés
            # seulement dans les colonnes de montant (le gate reste le filet de sûreté).
            monies = _loose_column_amounts(norm, lead_end, cols)
        if not monies:
            continue
        label = norm[lead_end:monies[0][0]].strip()
        raw.append({"date": date, "norm": norm, "label": label, "monies": monies,
                    "flag": _trailing_flag(norm), "section": section})

    has_balance = "balance" in cols
    if not cols:
        multi = sum(1 for o in raw if len(o["monies"]) >= 2)
        has_balance = bool(raw) and multi >= max(1, len(raw) // 2)

    # pas d'en-tête Débit/Crédit ni colonne Solde → tenter d'inférer la frontière
    # de la colonne Crédit par la GÉOMÉTRIE des montants (relevés scannés/OCR).
    if not has_dc and not has_balance and credit_x is None:
        credit_x = _infer_credit_x(raw)

    ops = []
    prev_bal = None
    for o in raw:
        monies = o["monies"]
        bal = None
        txtoks = monies
        if has_balance and len(monies) >= 2:
            bal = monies[-1][2]
            txtoks = monies[:-1]
        if not txtoks:
            continue
        pos, ln, val = txtoks[-1] if (has_dc or credit_x is not None) else txtoks[0]
        mag = abs(val)

        # signe, par ordre de fiabilité décroissante — toujours GÉOMÉTRIQUE
        sign = None
        if bal is not None and prev_bal is not None:                       # 1. delta de solde
            delta = round(bal - prev_bal, 2)
            if abs(abs(delta) - mag) <= max(0.02, mag * 0.001):
                sign = -1 if delta < 0 else 1
        if sign is None:
            sign = _explicit_sign(o["norm"], pos)                          # 2. signe +/- explicite
        if sign is None and val < 0:                                       # 3. parenthèses / « - »
            sign = -1
        if sign is None and o.get("section") is not None:                  # 4. section (sous-total +/-)
            sign = o["section"]
        if sign is None and credit_x is not None:                          # 5. colonne Crédit (en-tête ou inférée)
            sign = 1 if (pos + ln) >= credit_x else -1
        if sign is None and o["flag"]:                                     # 6. flag CR/DB
            sign = -1 if o["flag"] == "D" else 1
        if sign is None:
            sign = 1

        ops.append({
            "date": o["date"],
            "label": o["label"],
            "amount": round(sign * mag, 2),
            "invoice_ref": extract_invoice_ref(o["label"]),
        })
        if bal is not None:
            prev_bal = bal

    return ops


def extract_statement(text):
    up = text.upper()
    bank = next((b for b in BANKS if b in up), None)

    m = re.search(r"IBAN\s*:?\s*([A-Z]{2}[A-Z0-9 ]{10,32})", text)
    iban = m.group(1).strip() if m else None

    period_start = period_end = None
    mp = re.search(r"P[ÉE]RIODE\s*:?\s*(" + DATE_TOKEN + r")\s*[—\-–à]+\s*(" + DATE_TOKEN + r")", text, re.I)
    if not mp:
        mp = re.search(r"DU\s+(" + DATE_TOKEN + r")\s+AU\s+(" + DATE_TOKEN + r")", text, re.I)
    if mp:
        period_start, period_end = iso_date(mp.group(1)), iso_date(mp.group(2))

    profile = match_profile(text)
    # le pattern de la banque est PRIORITAIRE (essayé en premier), le défaut
    # n'est qu'un repli : sinon un « SOLDE AU » générique d'un récap en tête peut
    # primer sur le vrai « SOLDE PRÉCÉDENT » du compte (ex. Caisse d'Épargne).
    open_primary = profile.get("open") if profile else None
    close_primary = profile.get("close") if profile else None
    close_last = bool(profile and profile.get("close_last"))

    def _bal(primary, default, last=False):
        v = amount_after(primary, text, last=last) if primary else None
        return v if v is not None else amount_after(default, text, last=last)

    opening = _bal(open_primary, _OPEN_DEFAULT)
    closing = _bal(close_primary, _CLOSE_DEFAULT, last=close_last)
    if closing is None:
        # repli : le DERNIER « Solde au … » (≠ ouverture)
        closing = amount_after(r"SOLDE\s*(?:CR[ÉE]DITEUR|D[ÉE]BITEUR)?\s*AU\s*\d|SOLDE\s*AU\s*\d",
                               text, last=True)
        if closing is not None and closing == opening:
            closing = None
    open_re = open_primary or _OPEN_DEFAULT
    close_re = close_primary or _CLOSE_DEFAULT

    # Titulaire : logique forte partagée (ancres fiables « Titulaire : X » / « X -
    # COMPTE COURANT », rejet slogans/titres/adresses/coordonnées, strip civilité ;
    # candidats renvoyés si ambigu → l'appelant DEMANDE plutôt que d'inventer un client).
    holder, holder_candidates = _extract_holder(text)

    cols = detect_columns(text.splitlines())
    default_year = (int(period_start[:4]) if period_start else None) or _doc_year(text)
    # multi-comptes : ne parser que les opérations du premier compte (cohérent
    # avec opening/closing). detect_columns reste sur le texte complet (en-tête).
    ops_text = first_account_region(text, open_re, close_re)
    operations = parse_operations(ops_text, cols, default_year)

    return {
        "kind": "bank-statement",
        "holder": holder,
        "holder_candidates": holder_candidates,
        "iban": iban,
        "bank": bank,
        "period_start": period_start,
        "period_end": period_end,
        "opening_balance": opening,
        "closing_balance": closing,
        "operations": operations,
    }


# ── Main ──────────────────────────────────────────────────────────────────

def statement_reconcile_reasons(result):
    """Gate de réconciliation d'un relevé : `ouverture + Σ opérations = clôture`.
    Renvoie la liste des raisons d'échec (vide = le relevé est arithmétiquement
    cohérent). Source unique, réutilisée pour l'extraction géométrique ET pour
    contrôler un sidecar vision (un relevé relu en vision DOIT lui aussi tomber
    juste, sinon les signes/montants sont encore faux)."""
    reasons = []
    ops = result.get("operations") or []
    ob, cb = result.get("opening_balance"), result.get("closing_balance")
    if not ops:
        reasons.append("aucune_operation")
    elif ob is not None and cb is not None:
        s = round(sum(o["amount"] for o in ops if o.get("amount") is not None), 2)
        if abs(round(ob + s, 2) - cb) > max(1.0, abs(cb) * 0.005):
            reasons.append("solde_non_reconcilie")
    else:
        # pas de solde d'ouverture+clôture imprimés → impossible de vérifier les signes
        reasons.append("solde_non_verifiable")
    return reasons


def assess_confidence(result, text):
    """Ajoute `needs_vision` (bool), `confidence` ('high'|'low') et `vision_reason`.

    Le script déterministe ne réussit pas toujours : PDF scanné (aucune couche
    texte), layout brouillon, champ obligatoire manquant, ou — pour un relevé —
    solde qui ne se reconcilie pas (`ouverture + Σ opérations ≠ clôture`), signe
    d'amounts mal lus. Dans ces cas on bascule sur la lecture VISION (le modèle
    lit les pages rasterisées) plutôt que de forcer un résultat regex douteux.
    Champs purement additifs : `main.py` ne lit que les clés qu'il connaît."""
    reasons = []
    if _text_unusable(text):
        reasons.append("no_text_layer")  # PDF scanné / photo / texte explosé

    kind = result.get("kind")
    if kind == "note-de-frais":
        # Une note de frais n'a pas de n° de facture : seul le total à rembourser
        # est obligatoire. Gate arithmétique HT+TVA=TTC si les trois sont lus.
        if result.get("total_ttc") is None:
            reasons.append("total_ttc_absent")
        ht, tva, ttc = result.get("total_ht"), result.get("tva_amount"), result.get("total_ttc")
        if ht is not None and tva is not None and ttc is not None:
            if abs(round(ht + tva, 2) - ttc) > max(0.02, abs(ttc) * 0.01):
                reasons.append("total_incoherent")
    elif kind == "invoice":
        if not result.get("invoice_id"):
            reasons.append("invoice_id_absent")
        if result.get("total_ttc") is None:
            reasons.append("total_ttc_absent")
        # Gate arithmétique facture : si HT, TVA et TTC sont TOUS lus, ils doivent
        # vérifier HT + TVA = TTC. Sinon, un montant a été mal capté (ex. regex qui
        # attrape un sous-total au lieu du TTC) → on ne truste pas en silence, on
        # bascule en vision. (Si HT ou TVA manquent — facture mono-montant, auto-
        # entrepreneur exonéré — pas de contrôle possible, donc pas de faux positif.)
        ht, tva, ttc = result.get("total_ht"), result.get("tva_amount"), result.get("total_ttc")
        if ht is not None and tva is not None and ttc is not None:
            if abs(round(ht + tva, 2) - ttc) > max(0.02, abs(ttc) * 0.01):
                reasons.append("total_incoherent")
    elif kind == "bank-statement":
        # contrôle de justesse : ouverture + Σ opérations doit donner la clôture
        # (sinon signes/montants mal lus → vision). Source unique : voir ci-dessus.
        reasons.extend(statement_reconcile_reasons(result))
    else:
        reasons.append("type_indetermine")

    result["needs_vision"] = bool(reasons)
    result["confidence"] = "low" if reasons else "high"
    if reasons:
        result["vision_reason"] = reasons
    return result


def classify_and_extract(text):
    if not text.strip():
        return assess_confidence({"kind": "other", "error": "no text extracted"}, text)
    if looks_like_statement(text) and not has_invoice_guard(text):
        return assess_confidence(extract_statement(text), text)
    # Note de frais AVANT facture : « NOTE DE FRAIS » déclenche aussi looks_like_invoice.
    if looks_like_expense(text):
        return assess_confidence(extract_expense(text), text)
    if looks_like_invoice(text):
        return assess_confidence(extract_invoice(text), text)
    if looks_like_statement(text):
        return assess_confidence(extract_statement(text), text)
    return assess_confidence({"kind": "other"}, text)


def vision_skeleton(cur):
    """Squelette de sidecar `<pdf>.vision.json` pré-rempli à partir de l'extraction
    regex `cur` — à corriger par la passe vision. Réutilisé par `extract.py
    --vision-kit` et par `resolve_vision.py`."""
    kind = cur.get("kind")
    if kind == "invoice":
        return {k: cur.get(k) for k in (
            "kind", "invoice_id", "issue_date", "due_date", "total_ht",
            "tva_rate", "tva_amount", "total_ttc", "emitter", "recipient")}
    if kind == "bank-statement":
        return {
            "kind": "bank-statement", "holder": cur.get("holder"), "bank": cur.get("bank"),
            "opening_balance": cur.get("opening_balance"), "closing_balance": cur.get("closing_balance"),
            "operations": cur.get("operations") or [
                {"date": "AAAA-MM-JJ", "label": "", "amount": 0.0, "invoice_ref": None}],
        }
    return {"kind": "bank-statement | invoice  (choisir d'après l'image)"}


def render_pages(pdf_path, out_dir, dpi=200, max_pages=10):
    """Rasterise les pages du PDF en PNG (pour lecture VISION quand le texte
    n'est pas exploitable). Retourne la liste triée des chemins générés.
    Nécessite `pdftoppm` (poppler) — déjà requis par `pdftotext`."""
    import os
    os.makedirs(out_dir, exist_ok=True)
    prefix = os.path.join(out_dir, "page")
    try:
        subprocess.run(["pdftoppm", "-png", "-r", str(dpi), "-l", str(max_pages),
                        str(pdf_path), prefix], capture_output=True, timeout=120)
    except Exception:
        return []
    return sorted(os.path.join(out_dir, f) for f in os.listdir(out_dir)
                  if f.startswith("page") and f.endswith(".png"))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(json.dumps({"kind": "other", "error": "usage: extract.py <pdf> [--images <dir>]"}))
        return
    pdf = args[0]
    # Mode rasterisation : `extract.py <pdf> --images <dir>` → PNG par page,
    # à donner ensuite au modèle vision quand le script signale needs_vision.
    if "--images" in sys.argv:
        i = sys.argv.index("--images")
        out_dir = sys.argv[i + 1] if i + 1 < len(sys.argv) else "."
        imgs = render_pages(pdf, out_dir)
        print(json.dumps({"images": imgs}, ensure_ascii=False))
        return
    # Kit pour la passe VISION : images des pages + squelette de sidecar
    # pré-rempli (au bon schéma) à corriger puis sauver en <pdf>.vision.json.
    if "--vision-kit" in sys.argv:
        i = sys.argv.index("--vision-kit")
        out_dir = sys.argv[i + 1] if i + 1 < len(sys.argv) else "."
        cur = classify_and_extract(pdftext(pdf))
        imgs = render_pages(pdf, out_dir)
        print(json.dumps({
            "sidecar_path": str(pdf) + ".vision.json",
            "images": imgs,
            "current_extraction": cur,
            "skeleton": vision_skeleton(cur),
            "_help": "Lire les images, corriger le squelette (montants signés crédit +/débit −, "
                     "champs illisibles = null, JAMAIS inventés), sauver tel quel en `sidecar_path`. "
                     "Relevé : vérifier ouverture + Σ montants = clôture avant de sauver.",
        }, ensure_ascii=False, indent=2))
        return
    out = classify_and_extract(pdftext(pdf))
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
