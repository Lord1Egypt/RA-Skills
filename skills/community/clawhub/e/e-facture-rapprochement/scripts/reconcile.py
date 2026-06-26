"""MOTEUR DE RAPPROCHEMENT — le cœur de valeur.

Entrées :
  invoices   : liste de factures normalisées (schéma `normalized invoice`)
  statements : liste de relevés normalisés (schéma `normalized statement`)
  today      : date de référence ISO (pour overdue / relances) ; défaut = aujourd'hui

Sortie : {"periods": [...]} au CONTRAT EXACT de rapprochement.json, plus une table
d'auto-contrôle. La règle d'or : AUCUNE transaction du relevé n'est oubliée.

Comptabilité de l'invariant : on compte AU NIVEAU TRANSACTION (robuste au cross-période
facture↔paiement, comme l'exige le backend). Pour CHAQUE période p :
    (transactions de p consommées par une facture) + (unmatched_bank_lines de p)
        == bank_transactions_count(p)
"""
from __future__ import annotations

from datetime import date

from normalize import (
    DATE_WINDOW_DAYS, RELANCE_STEPS, SCORE_AMBIGU_GAP, SCORE_MIN,
    SCORE_W_AMOUNT, SCORE_W_DATE, SCORE_W_LABEL, TVA_TOLERANCE_PCT,
    classify_non_billable, days_between, money_close, name_similarity,
    parse_date, period_of, ref_match,
)


# --------------------------------------------------------------------------- #
# Préparation                                                                  #
# --------------------------------------------------------------------------- #

def _flatten_transactions(statements: list[dict]) -> list[dict]:
    """Aplatit les transactions de tous les relevés, chacune taguée période + relevé."""
    txs = []
    for si, st in enumerate(statements):
        for ti, t in enumerate(st.get("transactions", [])):
            label = t.get("label") or "Ligne bancaire"
            # une catégorie posée explicitement (sidecar) prime sur la détection auto
            category = t.get("category") or classify_non_billable(label)
            txs.append({
                "uid": f"{si}:{ti}",
                "statement_idx": si,
                "date": t.get("date"),
                "period": period_of(t.get("date")),
                "amount": float(t.get("amount", 0.0)),
                "label": label,
                "invoice_ref": t.get("invoice_ref"),
                "category": category,       # non-None => NON facturable (jamais matché)
                "consumed": False,
            })
    return txs


def _expected_sign(inv_type: str) -> int:
    """type 'out' (vente) -> encaissement = CRÉDIT (+) ; 'in' (achat) -> DÉBIT (-)."""
    return +1 if inv_type == "out" else -1


def _sign_ok(inv_type: str, amount: float) -> bool:
    return (amount > 0) == (_expected_sign(inv_type) > 0) if amount != 0 else False


# --------------------------------------------------------------------------- #
# Scoring d'un appariement facture <-> transaction                             #
# --------------------------------------------------------------------------- #

def _components(inv: dict, tx: dict):
    inv_amt = abs(float(inv["amount"]))
    diff = abs(abs(tx["amount"]) - inv_amt)
    amount_score = 1.0 if money_close(tx["amount"], inv_amt) else max(0.0, 1.0 - diff / max(inv_amt, 1.0))
    label_score = name_similarity(inv.get("counterparty_name", ""), tx["label"])
    dists = [d for d in (days_between(tx["date"], inv.get("issued_date")),
                         days_between(tx["date"], inv.get("due_date"))) if d is not None]
    dmin = min(dists) if dists else None
    date_score = max(0.0, 1.0 - dmin / DATE_WINDOW_DAYS) if (dmin is not None and dmin <= DATE_WINDOW_DAYS) else 0.0
    return amount_score, label_score, date_score


def _score(inv: dict, tx: dict) -> float:
    amount_score, label_score, date_score = _components(inv, tx)
    # GARDE-FOU : le montant ne décide jamais seul -> il faut un appui libellé OU date.
    if label_score < 0.2 and date_score == 0.0:
        return 0.0
    # ACOMPTE / PAIEMENT PARTIEL : un montant nettement inférieur fait chuter amount_score,
    # mais une contrepartie franchement reconnue + une date proche restent un paiement crédible.
    # On rehausse alors le score (sans jamais dépasser un vrai match exact).
    if label_score >= 0.7 and date_score > 0.0 and abs(tx["amount"]) <= abs(float(inv["amount"])) * 1.02:
        return max(SCORE_MIN, SCORE_W_LABEL * label_score + SCORE_W_DATE * date_score
                   + SCORE_W_AMOUNT * max(amount_score, 0.5))
    return SCORE_W_AMOUNT * amount_score + SCORE_W_LABEL * label_score + SCORE_W_DATE * date_score


# --------------------------------------------------------------------------- #
# Application d'un match (statut, montants)                                     #
# --------------------------------------------------------------------------- #

def _settle(inv: dict, paid_abs: float, matched_uids: list[str]):
    inv_amt = abs(float(inv["amount"]))
    inv["bank_matched"] = True
    inv["matched_tx"] = matched_uids
    if money_close(paid_abs, inv_amt):
        inv["status"] = "paid"
        inv["amount_paid"] = round(inv_amt, 2)
        inv["amount_remaining"] = 0
    elif paid_abs < inv_amt:
        inv["status"] = "partial"
        inv["amount_paid"] = round(paid_abs, 2)
        inv["amount_remaining"] = round(inv_amt - paid_abs, 2)
    else:  # trop-perçu
        inv["status"] = "paid"
        inv["amount_paid"] = round(inv_amt, 2)
        inv["amount_remaining"] = 0
        inv["overpaid_by"] = round(paid_abs - inv_amt, 2)


# --------------------------------------------------------------------------- #
# Passes de rapprochement                                                      #
# --------------------------------------------------------------------------- #

def _match(invoices: list[dict], txs: list[dict]):
    # Init des champs facture
    for inv in invoices:
        inv.setdefault("bank_matched", False)
        inv.setdefault("status", "unpaid")
        inv.setdefault("amount_paid", 0)
        inv.setdefault("amount_remaining", round(abs(float(inv["amount"])), 2))
        inv.setdefault("anomalies", [])

    def pool(inv):
        # les opérations non facturables (salaire/impôt/frais/retrait…) ne sont JAMAIS candidates
        return [t for t in txs if not t["consumed"] and not t["category"]
                and _sign_ok(inv["type"], t["amount"])]

    # PASSE 1 — référence facture explicite (la plus fiable, gère les paiements multiples).
    for inv in invoices:
        if inv["bank_matched"]:
            continue
        refs = [t for t in pool(inv)
                if (t["invoice_ref"] and ref_match(inv["invoice_id"], t["invoice_ref"]))
                or ref_match(inv["invoice_id"], t["label"])]
        if refs:
            for t in refs:
                t["consumed"] = True
            _settle(inv, sum(abs(t["amount"]) for t in refs), [t["uid"] for t in refs])

    # PASSE 2 — fuzzy 1 facture <-> 1 transaction (montant + libellé + date pondérés).
    for inv in sorted([i for i in invoices if not i["bank_matched"]],
                      key=lambda i: abs(float(i["amount"])), reverse=True):
        cands = sorted(((_score(inv, t), t) for t in pool(inv)), key=lambda x: x[0], reverse=True)
        cands = [(s, t) for s, t in cands if s >= SCORE_MIN]
        if not cands:
            continue
        if len(cands) >= 2 and (cands[0][0] - cands[1][0]) < SCORE_AMBIGU_GAP:
            # ambigu : on départage par la date, sinon on n'écrit rien (match_ambigu).
            best_by_date = sorted(
                cands[:2],
                key=lambda x: min([d for d in (days_between(x[1]["date"], inv.get("issued_date")),
                                               days_between(x[1]["date"], inv.get("due_date")))
                                   if d is not None] or [9999]))
            if best_by_date[0][0] - best_by_date[1][0] == 0:
                continue  # toujours ambigu -> laisser la facture en attente
            best = best_by_date[0][1]
        else:
            best = cands[0][1]
        best["consumed"] = True
        _settle(inv, abs(best["amount"]), [best["uid"]])

    # PASSE 3 — paiement groupé : 1 transaction solde plusieurs factures de même contrepartie/sens.
    remaining = [i for i in invoices if not i["bank_matched"]]
    by_cp: dict[tuple, list] = {}
    for inv in remaining:
        by_cp.setdefault((inv["type"], (inv.get("counterparty_name") or "").lower()), []).append(inv)
    for (typ, _cp), group in by_cp.items():
        if len(group) < 2:
            continue
        target = round(sum(abs(float(i["amount"])) for i in group), 2)
        for t in txs:
            if t["consumed"] or t["category"] or not _sign_ok(typ, t["amount"]):
                continue
            if money_close(t["amount"], target) and any(
                name_similarity(g.get("counterparty_name", ""), t["label"]) >= 0.45 for g in group
            ):
                t["consumed"] = True
                for g in group:
                    _settle(g, abs(float(g["amount"])), [t["uid"]])
                break


# --------------------------------------------------------------------------- #
# Classification des transactions non rapprochées (§5)                          #
# --------------------------------------------------------------------------- #

def _unmatched_line(tx: dict) -> dict:
    # DÉBIT (sortant) sans facture -> facture_manquante ; CRÉDIT entrant -> paiement_orphelin.
    typ = "facture_manquante" if tx["amount"] < 0 else "paiement_orphelin"
    return {
        "type": typ,
        "label": tx["label"],
        "amount": round(tx["amount"], 2),  # SIGNÉ
        "date": tx["date"],
        "invoice_ref": tx["invoice_ref"],
    }


def _excluded_line(tx: dict) -> dict:
    # Opération NON facturable : sortie à part, jamais comptée en manquante/orpheline.
    return {
        "label": tx["label"],
        "amount": round(tx["amount"], 2),  # SIGNÉ
        "date": tx["date"],
        "invoice_ref": tx["invoice_ref"],
        "category": tx["category"],
    }


# --------------------------------------------------------------------------- #
# Anomalies factures + relances                                                #
# --------------------------------------------------------------------------- #

def _tva_anomaly(inv: dict) -> dict | None:
    ht, tva = inv.get("total_ht"), inv.get("tva_amount")
    rate = inv.get("tva_rate_pct")
    if ht in (None, 0) or tva is None or not rate:
        return None
    expected = ht * (rate / 100.0)
    if expected <= 0:
        return None
    disc = abs(tva - expected) / expected
    if disc > TVA_TOLERANCE_PCT:
        return {"type": "tva_incorrecte", "discrepancy_pct": round(disc * 100, 1),
                "total_ht": ht, "tva_declared": tva, "tva_expected": round(expected, 2),
                "tva_rate_pct": rate}
    return None


def _apply_status_and_anomalies(invoices: list[dict], today: str):
    today_d = date.fromisoformat(today)
    for inv in invoices:
        # overdue : non soldée + échéance dépassée
        if inv["status"] in ("unpaid",) and inv.get("due_date"):
            dd = parse_date(inv["due_date"])
            if dd and date.fromisoformat(dd) < today_d:
                inv["status"] = "overdue"
        # anomalie TVA
        tva = _tva_anomaly(inv)
        if tva and not any(a.get("type") == "tva_incorrecte" for a in inv["anomalies"]):
            inv["anomalies"].append(tva)
        # anomalie retard
        if inv["status"] == "overdue":
            dl = days_between(today, inv.get("due_date")) or 0
            if not any(a.get("type") == "invoice_overdue" for a in inv["anomalies"]):
                inv["anomalies"].append({"type": "invoice_overdue", "days_late": dl})


def _relance_step(days_late: int):
    for limit, step in RELANCE_STEPS:
        if days_late <= limit:
            return step
    return "escalation"


def _build_relances(invoices: list[dict], today: str) -> list[dict]:
    out = []
    for inv in invoices:
        if inv["status"] not in ("overdue", "partial"):
            continue
        if not inv.get("due_date"):
            continue
        dl = days_between(today, inv["due_date"])
        if dl is None or dl <= 0:
            continue
        rel = {
            "invoice_id": inv["invoice_id"],
            "counterparty": inv.get("counterparty_name"),
            "amount": abs(float(inv["amount"])),
            "due_date": inv["due_date"],
            "days_late": dl,
            "step": _relance_step(dl),
            "status": inv["status"],
        }
        if inv["status"] == "partial":
            rel["amount_remaining"] = inv.get("amount_remaining", 0)
            rel["note"] = f"Solde restant dû : {inv.get('amount_remaining', 0):.2f} €"
        out.append(rel)
    return out


def _period_anomalies(statements: list[dict], period: str) -> list[dict]:
    """Doublons de paiement + relevés non parseables, rattachés à la période."""
    anomalies = []
    seen = {}
    for st in statements:
        for t in st.get("transactions", []):
            if period_of(t.get("date")) != period:
                continue
            key = (t.get("date"), round(float(t.get("amount", 0)), 2), (t.get("label") or "").lower())
            seen[key] = seen.get(key, 0) + 1
    for (d, amt, label), n in seen.items():
        if n >= 2:
            anomalies.append({"type": "doublon_paiement", "label": label or "Ligne bancaire",
                              "amount": amt, "date": d})
    return anomalies


# --------------------------------------------------------------------------- #
# Assemblage des périodes + invariant                                          #
# --------------------------------------------------------------------------- #

def reconcile(invoices: list[dict], statements: list[dict], today: str | None = None,
              ingestion_anomalies: list[dict] | None = None) -> dict:
    today = parse_date(today) or date.today().isoformat()
    txs = _flatten_transactions(statements)

    _match(invoices, txs)
    _apply_status_and_anomalies(invoices, today)

    # Périodes = union(périodes des transactions, périodes d'émission des factures).
    inv_period = lambda inv: period_of(inv.get("issued_date")) or period_of(inv.get("due_date"))
    periods = set(filter(None, (t["period"] for t in txs)))
    periods |= set(filter(None, (inv_period(i) for i in invoices)))
    # factures sans aucune période -> rattachées à la période la plus récente connue
    fallback = max(periods) if periods else (today[:7])
    periods.add(fallback)

    relances_all = _build_relances(invoices, today)
    ingestion_anomalies = ingestion_anomalies or []

    out_periods = []
    selfcheck = []
    for p in sorted(periods):
        p_txs = [t for t in txs if t["period"] == p]
        p_invoices = [i for i in invoices if (inv_period(i) or fallback) == p]
        consumed_in_p = [t for t in p_txs if t["consumed"]]
        leftover = [t for t in p_txs if not t["consumed"]]
        excluded = [_excluded_line(t) for t in leftover if t["category"]]
        unmatched = [_unmatched_line(t) for t in leftover if not t["category"]]
        stmt_idxs = {t["statement_idx"] for t in p_txs}

        panoms = _period_anomalies(statements, p)
        panoms += [a for a in ingestion_anomalies if a.get("period") == p]

        out_periods.append({
            "period": p,
            "locked": False,
            "bank_statements_count": len(stmt_idxs),
            "bank_transactions_count": len(p_txs),
            "invoices": [_clean_invoice(i) for i in p_invoices],
            "unmatched_bank_lines": unmatched,
            "excluded_bank_lines": excluded,
            "period_anomalies": [{k: v for k, v in a.items() if k != "period"} for a in panoms],
            "relances": [r for r in relances_all
                         if (inv_period(_find_inv(invoices, r["invoice_id"])) or fallback) == p],
        })

        somme = len(consumed_in_p) + len(unmatched) + len(excluded)
        ok = somme == len(p_txs)
        selfcheck.append({
            "period": p, "bank_transactions_count": len(p_txs),
            "matched": len(consumed_in_p), "unmatched": len(unmatched),
            "excluded": len(excluded), "somme": somme, "ok": ok,
        })

    return {"periods": out_periods, "selfcheck": selfcheck}


def _find_inv(invoices, invoice_id):
    return next((i for i in invoices if i["invoice_id"] == invoice_id), {})


_INVOICE_FIELDS = ("invoice_id", "type", "counterparty_name", "amount", "issued_date",
                   "due_date", "status", "bank_matched", "amount_paid", "amount_remaining",
                   "anomalies", "matched_tx", "overpaid_by", "source_file")


def _clean_invoice(inv: dict) -> dict:
    """Ne garde que les champs du contrat (snake_case), dans un ordre stable."""
    out = {}
    for f in _INVOICE_FIELDS:
        if f in inv and inv[f] is not None:
            out[f] = inv[f]
    out.setdefault("anomalies", [])
    return out
