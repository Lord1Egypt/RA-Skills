#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import statistics
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import requests

SKILL_VERSION = "0.1.1"
DERIBIT = "https://www.deribit.com/api/v2/public"
BINANCE = "https://api.binance.com/api/v3"
OKX = "https://www.okx.com/api/v5"
BYBIT = "https://api.bybit.com/v5"
PUBLIC_SOURCES = [
    "Deribit Public API: /public/get_instruments, /public/get_order_book, /public/get_book_summary_by_currency, /public/get_index_price, /public/get_book_summary_by_instrument",
    "Coinbase Public API: /v2/prices/BTC-USD/spot",
    "Binance Public API (optional): /api/v3/ticker/price",
    "OKX Public API: /api/v5/market/ticker, /api/v5/public/funding-rate",
    "Bybit Public API: /v5/market/tickers",
]


@dataclass
class OptionPoint:
    instrument: str
    expiry: dt.datetime
    option_type: str
    strike: float
    delta: Optional[float]
    mark_iv: Optional[float]
    open_interest: Optional[float]


def get(url: str, params: Dict = None, timeout: int = 12):
    r = requests.get(url, params=params or {}, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, dict) and "result" in data:
        return data["result"]
    return data


def parse_deribit_option_name(name: str) -> Tuple[Optional[dt.datetime], Optional[float], Optional[str]]:
    try:
        parts = name.split("-")
        expiry = dt.datetime.strptime(parts[1], "%d%b%y")
        strike = float(parts[2])
        side = "call" if parts[3] == "C" else "put"
        return expiry, strike, side
    except Exception:
        return None, None, None


def choose_expiries(instruments: List[Dict], n: int = 3) -> List[dt.datetime]:
    expiries = sorted({
        dt.datetime.fromtimestamp(i["expiration_timestamp"] / 1000, dt.timezone.utc).replace(tzinfo=None)
        for i in instruments if i.get("instrument_name", "").startswith("BTC-")
    })
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    return [x for x in expiries if x > now][:n]


def load_option_points(currency: str = "BTC", expiries_n: int = 3, max_books: int = 160) -> List[OptionPoint]:
    instruments = get(f"{DERIBIT}/get_instruments", {"currency": currency, "kind": "option", "expired": "false"})
    target_exp = set(choose_expiries(instruments, n=expiries_n))

    candidates = []
    for ins in instruments:
        exp = dt.datetime.fromtimestamp(ins["expiration_timestamp"] / 1000, dt.timezone.utc).replace(tzinfo=None)
        if exp in target_exp:
            candidates.append(ins)

    points: List[OptionPoint] = []
    for ins in candidates[:max_books]:
        name = ins.get("instrument_name")
        expiry, strike, side = parse_deribit_option_name(name)
        if not (expiry and strike and side):
            continue
        try:
            ob = get(f"{DERIBIT}/get_order_book", {"instrument_name": name})
            greeks = ob.get("greeks") or {}
            points.append(OptionPoint(
                instrument=name,
                expiry=expiry,
                option_type=side,
                strike=strike,
                delta=greeks.get("delta"),
                mark_iv=ob.get("mark_iv"),
                open_interest=ob.get("open_interest"),
            ))
        except Exception:
            continue
    return points


def closest(points: List[OptionPoint], predicate, target_fn):
    filt = [p for p in points if predicate(p)]
    return min(filt, key=target_fn) if filt else None


def compute_surface_metrics(points: List[OptionPoint]) -> Dict:
    if not points:
        return {}

    by_exp: Dict[dt.datetime, List[OptionPoint]] = {}
    for p in points:
        by_exp.setdefault(p.expiry, []).append(p)
    first_exp = sorted(by_exp.keys())[0]
    chain = by_exp[first_exp]

    atm_call = closest(chain, lambda p: p.option_type == "call" and p.delta is not None and p.mark_iv is not None, lambda p: abs((p.delta or 0.0) - 0.5))
    atm_put = closest(chain, lambda p: p.option_type == "put" and p.delta is not None and p.mark_iv is not None, lambda p: abs(abs(p.delta or 0.0) - 0.5))
    atm_ivs = [x.mark_iv for x in [atm_call, atm_put] if x and x.mark_iv is not None]
    atm_iv = statistics.mean(atm_ivs) if atm_ivs else None

    c25 = closest(chain, lambda p: p.option_type == "call" and p.delta is not None and p.mark_iv is not None, lambda p: abs((p.delta or 0.0) - 0.25))
    p25 = closest(chain, lambda p: p.option_type == "put" and p.delta is not None and p.mark_iv is not None, lambda p: abs(abs(p.delta or 0.0) - 0.25))
    c15 = closest(chain, lambda p: p.option_type == "call" and p.delta is not None and p.mark_iv is not None, lambda p: abs((p.delta or 0.0) - 0.15))
    p15 = closest(chain, lambda p: p.option_type == "put" and p.delta is not None and p.mark_iv is not None, lambda p: abs(abs(p.delta or 0.0) - 0.15))

    rr25 = (c25.mark_iv - p25.mark_iv) if (c25 and p25 and c25.mark_iv is not None and p25.mark_iv is not None) else None
    rr15 = (c15.mark_iv - p15.mark_iv) if (c15 and p15 and c15.mark_iv is not None and p15.mark_iv is not None) else None

    put_oi = sum((p.open_interest or 0.0) for p in chain if p.option_type == "put")
    call_oi = sum((p.open_interest or 0.0) for p in chain if p.option_type == "call")

    return {
        "front_expiry": first_exp.isoformat() + "Z",
        "atm_iv_pct": round(atm_iv, 2) if atm_iv is not None else None,
        "rr_25d": round(rr25, 2) if rr25 is not None else None,
        "rr_15d": round(rr15, 2) if rr15 is not None else None,
        "put_call_oi_ratio": round((put_oi / call_oi), 3) if call_oi > 0 else None,
    }


def compute_volume_split(currency: str = "BTC") -> Dict:
    summaries = get(f"{DERIBIT}/get_book_summary_by_currency", {"currency": currency, "kind": "option"})
    put, call = 0.0, 0.0
    for s in summaries:
        ins = s.get("instrument_name", "")
        v = s.get("volume_usd") or 0.0
        if ins.endswith("-P"):
            put += v
        elif ins.endswith("-C"):
            call += v
    total = put + call
    return {
        "put_volume_usd": round(put, 2),
        "call_volume_usd": round(call, 2),
        "put_buy_share_proxy": round((put / total) * 100, 2) if total > 0 else None,
    }


def compute_deribit_core() -> Dict:
    idx = get(f"{DERIBIT}/get_index_price", {"index_name": "btc_usd"})
    perp = get(f"{DERIBIT}/get_book_summary_by_instrument", {"instrument_name": "BTC-PERPETUAL"})
    funding_8h, basis = None, None
    if isinstance(perp, list) and perp:
        p = perp[0]
        funding_8h = p.get("current_funding")
        if p.get("mid_price") and idx.get("index_price"):
            basis = (p["mid_price"] - idx["index_price"]) / idx["index_price"] * 100
    return {
        "deribit_index_price": idx.get("index_price"),
        "deribit_funding_8h": round(funding_8h, 6) if funding_8h is not None else None,
        "deribit_perp_basis_pct": round(basis, 4) if basis is not None else None,
    }


def fetch_cross_exchange() -> Dict:
    data = {
        "spot": {},
        "funding": {},
        "availability": {"spot_sources": 0, "funding_sources": 0},
        "data_gaps": [],
    }

    try:
        t = get(f"{BINANCE}/ticker/price", {"symbol": "BTCUSDT"})
        data["spot"]["binance"] = float(t.get("price"))
    except Exception:
        data["data_gaps"].append("binance_spot_unavailable")

    try:
        cb = get("https://api.coinbase.com/v2/prices/BTC-USD/spot")
        data["spot"]["coinbase"] = float(cb["data"]["amount"])
    except Exception:
        data["data_gaps"].append("coinbase_spot_unavailable")

    try:
        okx_t = get(f"{OKX}/market/ticker", {"instId": "BTC-USDT"})
        if okx_t and isinstance(okx_t.get("data"), list) and okx_t["data"]:
            data["spot"]["okx"] = float(okx_t["data"][0]["last"])
        else:
            data["data_gaps"].append("okx_spot_unavailable")
    except Exception:
        data["data_gaps"].append("okx_spot_unavailable")

    try:
        okx_f = get(f"{OKX}/public/funding-rate", {"instId": "BTC-USDT-SWAP"})
        if okx_f and isinstance(okx_f.get("data"), list) and okx_f["data"]:
            data["funding"]["okx"] = float(okx_f["data"][0]["fundingRate"])
        else:
            data["data_gaps"].append("okx_funding_unavailable")
    except Exception:
        data["data_gaps"].append("okx_funding_unavailable")

    try:
        by_t = get(f"{BYBIT}/market/tickers", {"category": "linear", "symbol": "BTCUSDT"})
        if by_t.get("retCode") == 0 and by_t.get("result", {}).get("list"):
            item = by_t["result"]["list"][0]
            data["spot"]["bybit"] = float(item["lastPrice"])
            if item.get("fundingRate") is not None:
                data["funding"]["bybit"] = float(item["fundingRate"])
            else:
                data["data_gaps"].append("bybit_funding_unavailable")
        else:
            data["data_gaps"].append("bybit_spot_unavailable")
    except Exception:
        data["data_gaps"].append("bybit_spot_unavailable")

    data["availability"]["spot_sources"] = len(data["spot"])
    data["availability"]["funding_sources"] = len(data["funding"])

    spots = list(data["spot"].values())
    if len(spots) >= 2:
        mean_spot = statistics.mean(spots)
        spread_bp = (max(spots) - min(spots)) / mean_spot * 10000
        data["spot_dispersion_bp"] = round(spread_bp, 2)
    else:
        data["spot_dispersion_bp"] = None
        data["data_gaps"].append("insufficient_spot_sources_for_dispersion")

    data["data_gaps"] = sorted(set(data["data_gaps"]))
    return data


def summarize_funding_regime(deribit_funding: Optional[float], xfund: Dict) -> Dict:
    vals = [v for v in [deribit_funding] + list(xfund.values()) if v is not None]
    if not vals:
        return {"mean": None, "neg_ratio": None, "regime": "unknown"}
    neg = sum(1 for v in vals if v < 0)
    mean = statistics.mean(vals)
    neg_ratio = neg / len(vals)
    regime = "bearish" if neg_ratio >= 0.6 else "mixed" if neg_ratio >= 0.3 else "bullish_or_neutral"
    return {"mean": round(mean, 6), "neg_ratio": round(neg_ratio, 2), "regime": regime}


def risk_label(metrics: Dict, event_mode: str = "normal") -> Tuple[str, List[str], int]:
    score = 0
    reasons = []

    rr15 = metrics.get("rr_15d")
    rr25 = metrics.get("rr_25d")
    atm = metrics.get("atm_iv_pct")
    put_share = metrics.get("put_buy_share_proxy")
    funding_regime = metrics.get("funding_regime", {}).get("regime")
    dispersion = metrics.get("spot_dispersion_bp")

    rr15_th = -7 if event_mode == "high-alert" else -8
    rr25_th = -4.5 if event_mode == "high-alert" else -5
    atm_th = 52 if event_mode == "high-alert" else 55
    put_th = 56 if event_mode == "high-alert" else 58
    dispersion_th = 15 if event_mode == "high-alert" else 20

    if rr15 is not None and rr15 < rr15_th:
        score += 2
        reasons.append("15d risk reversal deeply negative")
    if rr25 is not None and rr25 < rr25_th:
        score += 2
        reasons.append("25d risk reversal negative")
    if atm is not None and atm > atm_th:
        score += 1
        reasons.append("front ATM IV elevated")
    if put_share is not None and put_share > put_th:
        score += 1
        reasons.append("put-side volume dominance")
    if funding_regime == "bearish":
        score += 1
        reasons.append("multi-venue funding regime bearish")
    if dispersion is not None and dispersion > dispersion_th:
        score += 1
        reasons.append("cross-exchange spot dispersion elevated")

    red_th = 5 if event_mode == "high-alert" else 6
    amber_th = 2 if event_mode == "high-alert" else 3

    if score >= red_th:
        return "RED", reasons, score
    if score >= amber_th:
        return "AMBER", reasons, score
    return "GREEN", reasons, score


def build_72h_plan(metrics: Dict, horizon_hours: int = 72, event_mode: str = "normal") -> Dict:
    if event_mode == "high-alert":
        skew_cond = "RR15 <= -10 OR RR25 <= -7"
        iv_cond = "Front ATM IV >= 57"
        flow_cond = "Put volume proxy >= 56%"
        liq_cond = "Spot dispersion > 15bp"
        skew_now = bool((metrics.get("rr_15d") is not None and metrics["rr_15d"] <= -10) or (metrics.get("rr_25d") is not None and metrics["rr_25d"] <= -7))
        iv_now = bool(metrics.get("atm_iv_pct") is not None and metrics["atm_iv_pct"] >= 57)
        flow_now = bool(metrics.get("put_buy_share_proxy") is not None and metrics["put_buy_share_proxy"] >= 56)
        liq_now = bool(metrics.get("spot_dispersion_bp") is not None and metrics["spot_dispersion_bp"] > 15)
    else:
        skew_cond = "RR15 <= -12 OR RR25 <= -8"
        iv_cond = "Front ATM IV >= 60"
        flow_cond = "Put volume proxy >= 57%"
        liq_cond = "Spot dispersion > 20bp"
        skew_now = bool((metrics.get("rr_15d") is not None and metrics["rr_15d"] <= -12) or (metrics.get("rr_25d") is not None and metrics["rr_25d"] <= -8))
        iv_now = bool(metrics.get("atm_iv_pct") is not None and metrics["atm_iv_pct"] >= 60)
        flow_now = bool(metrics.get("put_buy_share_proxy") is not None and metrics["put_buy_share_proxy"] >= 57)
        liq_now = bool(metrics.get("spot_dispersion_bp") is not None and metrics["spot_dispersion_bp"] > 20)

    checks = [
        {"id": "options_skew_panic", "condition": skew_cond, "now": skew_now, "meaning": "Downside tail hedging remains stressed"},
        {"id": "vol_regime_hot", "condition": iv_cond, "now": iv_now, "meaning": "Short-term panic premium still rich"},
        {"id": "flow_put_dominance", "condition": flow_cond, "now": flow_now, "meaning": "Defensive flow still dominates"},
        {"id": "funding_bearish_confirm", "condition": "Funding regime = bearish", "now": metrics.get("funding_regime", {}).get("regime") == "bearish", "meaning": "Perp carry confirms downside bias"},
        {"id": "liquidity_stress", "condition": liq_cond, "now": liq_now, "meaning": "Cross-venue liquidity stress / dislocation"},
    ]

    fired = sum(1 for c in checks if c["now"])
    if fired >= 4:
        action = "DEFENSIVE"
    elif fired >= 2:
        action = "CAUTIOUS"
    else:
        action = "PROBING"

    return {
        "horizon_hours": horizon_hours,
        "event_mode": event_mode,
        "checks": checks,
        "fired": fired,
        "suggested_action": action,
    }


def confidence_score(metrics: Dict) -> Dict:
    score = 0
    avail = metrics.get("availability", {})
    if metrics.get("rr_15d") is not None and metrics.get("rr_25d") is not None:
        score += 30
    if metrics.get("atm_iv_pct") is not None:
        score += 15
    if metrics.get("put_buy_share_proxy") is not None:
        score += 15
    score += min(20, (avail.get("spot_sources", 0) * 5 + avail.get("funding_sources", 0) * 5))

    signal_count = 0
    signal_count += 1 if metrics.get("rr_15d") is not None and metrics["rr_15d"] < -8 else 0
    signal_count += 1 if metrics.get("rr_25d") is not None and metrics["rr_25d"] < -5 else 0
    signal_count += 1 if metrics.get("put_buy_share_proxy") is not None and metrics["put_buy_share_proxy"] > 58 else 0
    signal_count += 1 if metrics.get("funding_regime", {}).get("regime") == "bearish" else 0
    score += 20 if signal_count >= 3 else 10 if signal_count >= 2 else 0

    if metrics.get("degraded_mode"):
        score -= 10
    if avail.get("spot_sources", 0) < 2:
        score -= 10
    if avail.get("funding_sources", 0) == 0:
        score -= 10

    score = max(0, min(100, score))
    level = "high" if score >= 75 else "medium" if score >= 50 else "low"
    return {"score": score, "level": level}


def action_triggers(metrics: Dict, label: str, plan: Dict) -> Dict:
    rr15 = metrics.get("rr_15d")
    rr25 = metrics.get("rr_25d")
    iv = metrics.get("atm_iv_pct")
    put = metrics.get("put_buy_share_proxy")

    reduce = []
    probe = []

    if label == "RED" or plan.get("fired", 0) >= 4:
        reduce.append("Reduce gross long exposure / tighten leverage")
    if rr15 is not None and rr15 <= -14:
        reduce.append("Keep downside hedge (put or collar) active")
    if iv is not None and iv >= 70:
        reduce.append("Avoid chasing volatility expansion")

    if rr15 is not None and rr25 is not None and rr15 > -10 and rr25 > -7:
        probe.append("Skew decompressing: allow small probe longs")
    if iv is not None and iv < 58:
        probe.append("IV normalizing: improve tactical long R/R")
    if put is not None and put < 54:
        probe.append("Flow less defensive: rebound probability improves")

    return {"de_risk_triggers": reduce, "re_risk_triggers": probe}


def beginner_explain(lang: str, payload: Dict) -> str:
    m = payload["metrics"]
    plan = payload["validation_72h"]
    label = payload["risk_label"]
    gaps = payload.get("data_gaps", [])
    degraded = payload.get("degraded_mode")

    if lang == "zh":
        tail = f" 数据缺口: {', '.join(gaps)}。" if gaps else ""
        deg = " 当前为降级模式。" if degraded else ""
        return (
            "【小白解读】\n"
            f"1) 当前市场温度：{label}。可以理解成红绿灯里的“{label}灯”。\n"
            f"2) 为什么偏谨慎：ATM波动率 {m.get('atm_iv_pct')}%（越高代表越害怕），"
            f"RR15={m.get('rr_15d')} / RR25={m.get('rr_25d')}（越负代表越多人买下跌保险），"
            f"Put占比代理 {m.get('put_buy_share_proxy')}%（越高越偏防守）。\n"
            f"3) 接下来72小时：5个风控检查触发了 {plan.get('fired')}/5。\n"
            f"4) 实操建议（非投资建议）：{plan.get('suggested_action')}。若你是小白，优先控制仓位，不要满仓抄底。"
            f"{deg}{tail}"
        )

    tail = f" Data gaps: {', '.join(gaps)}." if gaps else ""
    deg = " Degraded mode is active." if degraded else ""
    return (
        "[Beginner Explainer]\n"
        f"1) Market temperature: {label} (traffic-light style risk state).\n"
        f"2) Why cautious now: ATM IV {m.get('atm_iv_pct')}% (higher = more fear), "
        f"RR15={m.get('rr_15d')} / RR25={m.get('rr_25d')} (more negative = stronger downside hedging), "
        f"put-flow proxy {m.get('put_buy_share_proxy')}% (higher = more defensive positioning).\n"
        f"3) Next 72h: {plan.get('fired')}/5 risk checks are active.\n"
        f"4) Practical stance (not investment advice): {plan.get('suggested_action')}. For beginners, prioritize smaller size and avoid all-in bottom fishing."
        f"{deg}{tail}"
    )


def detect_language(text: str) -> str:
    return "zh" if any("\u4e00" <= c <= "\u9fff" for c in text) else "en"


def narrative(lang: str, payload: Dict) -> str:
    m = payload["metrics"]
    label = payload["risk_label"]
    conf = payload["confidence"]
    plan = payload["validation_72h"]
    reasons = payload["reasons"]
    degraded = payload.get("degraded_mode")
    gaps = payload.get("data_gaps", [])

    if lang == "zh":
        tail = f" 数据缺口: {', '.join(gaps)}。" if gaps else ""
        deg = " 当前为降级模式。" if degraded else ""
        return (
            f"风险灯号: {label}（置信度 {conf['score']}/100, {conf['level']}）。"
            f"ATM IV={m.get('atm_iv_pct')}%，RR25={m.get('rr_25d')}，RR15={m.get('rr_15d')}，"
            f"Put占比代理={m.get('put_buy_share_proxy')}%，资金费率状态={m.get('funding_regime',{}).get('regime')}。"
            f"72小时验证触发 {plan['fired']}/5，建议: {plan['suggested_action']}。"
            f"触发原因: {', '.join(reasons) if reasons else '无'}。{deg}{tail}"
        )

    tail = f" Data gaps: {', '.join(gaps)}." if gaps else ""
    deg = " Degraded mode is active." if degraded else ""
    return (
        f"Risk label: {label} (confidence {conf['score']}/100, {conf['level']}). "
        f"ATM IV={m.get('atm_iv_pct')}%, RR25={m.get('rr_25d')}, RR15={m.get('rr_15d')}, "
        f"put-volume proxy={m.get('put_buy_share_proxy')}%, funding regime={m.get('funding_regime',{}).get('regime')}. "
        f"72h validation fired {plan['fired']}/5, action: {plan['suggested_action']}. "
        f"Triggers: {', '.join(reasons) if reasons else 'none'}.{deg}{tail}"
    )


def main():
    ap = argparse.ArgumentParser(description="BTC risk radar using public options/futures data")
    ap.add_argument("--prompt", default="", help="User prompt for language detection")
    ap.add_argument("--lang", choices=["auto", "en", "zh"], default="auto")
    ap.add_argument("--horizon-hours", type=int, default=72)
    ap.add_argument("--event-mode", choices=["normal", "high-alert"], default="normal")
    ap.add_argument("--audience", choices=["pro", "beginner"], default="pro")
    ap.add_argument("--json", action="store_true", help="Output JSON only")
    ap.add_argument("--sources", action="store_true", help="Print public data sources and exit")
    ap.add_argument("--version", action="store_true", help="Print script version and exit")
    args = ap.parse_args()

    if args.version:
        print(SKILL_VERSION)
        return

    if args.sources:
        print(json.dumps({
            "version": SKILL_VERSION,
            "read_only": True,
            "authenticated": False,
            "public_sources": PUBLIC_SOURCES,
        }, ensure_ascii=False, indent=2))
        return

    points = load_option_points()
    surface = compute_surface_metrics(points)
    vols = compute_volume_split()
    deribit_core = compute_deribit_core()
    cross = fetch_cross_exchange()

    metrics = {**surface, **vols, **deribit_core, **cross}
    metrics["funding_regime"] = summarize_funding_regime(metrics.get("deribit_funding_8h"), metrics.get("funding", {}))
    degraded_mode = bool(metrics.get("data_gaps"))
    metrics["degraded_mode"] = degraded_mode

    label, reasons, score = risk_label(metrics, event_mode=args.event_mode)
    plan = build_72h_plan(metrics, horizon_hours=args.horizon_hours, event_mode=args.event_mode)
    conf = confidence_score(metrics)
    triggers = action_triggers(metrics, label, plan)

    payload = {
        "as_of_utc": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "version": SKILL_VERSION,
        "read_only": True,
        "authenticated": False,
        "sources": PUBLIC_SOURCES,
        "notes": [
            "put_buy_share_proxy uses volume split, not signed aggressor flow",
            "RR metrics are front-expiry delta-nearest approximations",
            "cross-venue endpoints may be regionally unavailable",
            "partial venue failures reduce confidence and activate degraded_mode",
        ],
        "degraded_mode": degraded_mode,
        "data_gaps": metrics.get("data_gaps", []),
        "risk_label": label,
        "risk_score": score,
        "confidence": conf,
        "reasons": reasons,
        "validation_72h": plan,
        "action_triggers": triggers,
        "metrics": metrics,
    }

    lang = detect_language(args.prompt) if args.lang == "auto" else args.lang

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        if args.audience == "beginner":
            print(beginner_explain(lang, payload))
        else:
            print(narrative(lang, payload))
        print("\n--- JSON ---")
        print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
