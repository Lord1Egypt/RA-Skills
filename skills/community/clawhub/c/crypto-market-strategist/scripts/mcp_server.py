"""Read-only MCP server for BTC and ETH derivatives research and strategy analysis."""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from mcp.server.fastmcp import FastMCP

from market_context import run as market_context_run
from market_models import fit_option_surface, fit_prediction_market
from polymarket import macro_events, run as polymarket_run
from snapshot import consolidated_market_snapshot
from strategy_engine import build_strategy_inputs
from strategy_library import REGIMES, STRATEGIES, STRATEGY_BY_ID

mcp = FastMCP("Crypto Market Strategist")

_BUNDLE_ID_PATTERN = re.compile(r"^crypto-research-[0-9]{8}T[0-9]{6}Z-[a-f0-9]{8}$")
_PROHIBITED_CARD_KEYS = {
    "expiry",
    "strike",
    "long_call_strike",
    "short_call_strike",
    "long_put_strike",
    "short_put_strike",
    "position_size",
    "leverage",
    "win_rate",
    "positive_pnl_probability",
    "payoff_ratio",
    "expected_return",
}


def _output_root(output_dir: str = "") -> Path:
    if output_dir:
        return Path(output_dir).expanduser()
    return Path(os.environ.get("CRYPTO_STRATEGY_OUTPUT_DIR", Path.home() / "Documents" / "Crypto Strategy Cards"))


def _source_error(source: str, exc: Exception) -> dict:
    return {"status": "unavailable", "source": source, "error": f"{type(exc).__name__}: {exc}"}


def _strike_from_title(title: str) -> float | None:
    match = re.search(r"\$(\d[\d,]*(?:\.\d+)?)\s*(k)?\b", title, re.I)
    if not match:
        return None
    return float(match.group(1).replace(",", "")) * (1_000 if match.group(2) else 1)


def _condition_direction(title: str) -> str | None:
    text = title.lower()
    for needle, direction in (
        ("above", "above"), ("over", "above"), ("below", "below"),
        ("under", "below"), ("reach", "reach"), ("hit", "reach"), ("dip", "dip"),
    ):
        if needle in text:
            return direction
    return None


def _enrich_prediction_markets(data: dict, reference: dict | None, fit: bool = True) -> dict:
    """Add distance-to-strike context without changing contract settlement rules."""
    price = reference.get("price_usd") if reference else None
    shared = {
        "venue": reference.get("venue") if reference else None,
        "reference_type": reference.get("reference_type") if reference else None,
        "price_usd": price,
        "as_of": data.get("as_of"),
        "note": "Context only; each Polymarket rule controls settlement.",
    }
    enriched = {**data, "current_underlying_reference": shared}
    for panel in ("terminal_markets", "barrier_markets"):
        rows = []
        for row in data.get(panel, []):
            strike = _strike_from_title(row.get("market_title", ""))
            rows.append({
                **row,
                "current_price_context": {
                    "current_price_usd": price,
                    "parsed_strike_usd": strike,
                    "strike_distance_pct_from_current": round((strike / price - 1) * 100, 4) if strike and price else None,
                    "parsed_condition_direction": _condition_direction(row.get("market_title", "")),
                },
            })
        enriched[panel] = rows
    if fit:
        enriched["prediction_market_dossier"] = fit_prediction_market(enriched)
    return enriched


def _add_record(records, record_id, source, asset, kind, pointer, summary):
    records.append({
        "id": record_id,
        "source": source,
        "asset": asset,
        "kind": kind,
        "pointer": pointer,
        "summary": summary,
    })


def _research_index(packet: dict) -> dict:
    """Build a compact index over complete raw observations."""
    records = []
    asset = packet["asset"]
    data = packet["data"]
    base = "/data"
    deribit = data.get("deribit_market_snapshot", {})
    if deribit.get("surface_dossier"):
        _add_record(records, f"deribit:{asset}:surface-dossier", "Deribit", asset, "surface_dossier", f"{base}/deribit_market_snapshot/surface_dossier", "Fitted complete option surface")
    for position, row in enumerate(deribit.get("surface_inventory", {}).get("expiry_grid", [])):
        expiry = row.get("expiry_timestamp")
        _add_record(records, f"deribit:{asset}:expiry:{expiry}", "Deribit", asset, "option_expiry", f"{base}/deribit_market_snapshot/surface_inventory/expiry_grid/{position}", str(row.get("expiry")))
    for expiry, rows in deribit.get("expiry_slices", {}).items():
        for position, row in enumerate(rows):
            name = row.get("instrument_name")
            _add_record(records, f"deribit:{asset}:option:{name}", "Deribit", asset, "option_contract", f"{base}/deribit_market_snapshot/expiry_slices/{expiry}/{position}", str(name))
    for position, row in enumerate(deribit.get("dated_futures_curve", [])):
        name = row.get("instrument_name")
        _add_record(records, f"deribit:{asset}:future:{name}", "Deribit", asset, "dated_future", f"{base}/deribit_market_snapshot/dated_futures_curve/{position}", str(name))

    prediction = data.get("polymarket_crypto_markets", {})
    if prediction.get("prediction_market_dossier"):
        _add_record(records, f"polymarket:{asset}:probability-dossier", "Polymarket", asset, "prediction_market_dossier", f"{base}/polymarket_crypto_markets/prediction_market_dossier", "Rule-aware probability dossier")
    for panel in ("terminal_markets", "barrier_markets"):
        for position, row in enumerate(prediction.get(panel, [])):
            token = row.get("token_id")
            _add_record(records, f"polymarket:{asset}:contract:{token}", "Polymarket", asset, row.get("market_type", panel), f"{base}/polymarket_crypto_markets/{panel}/{position}", str(row.get("market_title")))

    _add_record(records, f"hyperliquid:{asset}:technical", "Hyperliquid", asset, "technical_context", f"{base}/perp_technical_snapshot", "Trend and realized-volatility context")
    _add_record(records, f"hyperliquid:{asset}:carry", "Hyperliquid", asset, "perpetual_carry", f"{base}/perp_carry_snapshot", "Funding, basis, open interest, and volume")
    context = data.get("hyperliquid_context", {})
    if context.get("realized_volatility_dossier"):
        _add_record(records, f"hyperliquid:{asset}:realized-volatility", "Hyperliquid", asset, "realized_volatility", f"{base}/hyperliquid_context/realized_volatility_dossier", "Multi-horizon OHLC realized volatility")
    if context.get("price_level_dossier"):
        _add_record(records, f"hyperliquid:{asset}:price-levels", "Hyperliquid", asset, "price_levels", f"{base}/hyperliquid_context/price_level_dossier", "ATR-scaled support, resistance, and breakout levels")
    if context.get("daily_ohlcv"):
        _add_record(records, f"hyperliquid:{asset}:daily-ohlcv", "Hyperliquid", asset, "ohlcv_series", f"{base}/hyperliquid_context/daily_ohlcv", "Complete daily OHLCV collection")
    if context.get("four_hour_ohlcv"):
        _add_record(records, f"hyperliquid:{asset}:4h-ohlcv", "Hyperliquid", asset, "ohlcv_series", f"{base}/hyperliquid_context/four_hour_ohlcv", "Complete four-hour OHLCV collection")

    macro = data.get("polymarket_macro_events", {})
    for position, row in enumerate(macro.get("events", [])):
        slug = row.get("event_slug")
        _add_record(records, f"polymarket:macro:event:{slug}", "Polymarket", "macro", "macro_event", f"{base}/polymarket_macro_events/events/{position}", str(row.get("event_title")))
    for position, row in enumerate(macro.get("markets", [])):
        token = row.get("token_id")
        _add_record(records, f"polymarket:macro:contract:{token}", "Polymarket", "macro", "macro_contract", f"{base}/polymarket_macro_events/markets/{position}", str(row.get("market_title")))
    return {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "record_count": len(records),
        "records": records,
    }


def _pointer_get(data: object, pointer: str) -> object:
    current = data
    for segment in (part for part in pointer.split("/") if part):
        current = current[int(segment)] if isinstance(current, list) else current[segment]
    return current


def _save_research_bundle(packet: dict, output_dir: str = "") -> dict:
    root = _output_root(output_dir) / "research-bundles"
    root.mkdir(parents=True, exist_ok=True)
    bundle_id = f"crypto-research-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid4().hex[:8]}"
    bundle_dir = root / bundle_id
    bundle_dir.mkdir()
    raw_path = bundle_dir / "raw-data.json"
    index_path = bundle_dir / "research-index.json"
    manifest_path = bundle_dir / "manifest.json"
    raw_path.write_text(json.dumps(packet, indent=2, default=str), encoding="utf-8")
    index = _research_index(packet)
    index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
    manifest = {
        "bundle_id": bundle_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "asset": packet["asset"],
        "raw_data_path": str(raw_path),
        "research_index_path": str(index_path),
        "record_count": index["record_count"],
        "collection_snapshot": True,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def _load_research_bundle(bundle_id: str, output_dir: str = "") -> tuple[dict, dict, dict]:
    if not _BUNDLE_ID_PATTERN.fullmatch(bundle_id):
        raise ValueError("research_bundle_id is invalid")
    bundle_dir = _output_root(output_dir) / "research-bundles" / bundle_id
    try:
        manifest = json.loads((bundle_dir / "manifest.json").read_text(encoding="utf-8"))
        raw = json.loads((bundle_dir / "raw-data.json").read_text(encoding="utf-8"))
        index = json.loads((bundle_dir / "research-index.json").read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError("research bundle was not found on this machine") from exc
    return manifest, raw, index


def _collect_asset(asset: str) -> dict:
    """Collect each public source independently so one outage does not erase the rest."""
    status = {}
    try:
        deribit = consolidated_market_snapshot(asset)
        status["deribit"] = "available"
    except Exception as exc:
        deribit = _source_error("Deribit public API", exc)
        status["deribit"] = "unavailable"

    try:
        context = market_context_run(asset)
        status["hyperliquid"] = "available"
    except Exception as exc:
        context = _source_error("Hyperliquid public Info API", exc)
        status["hyperliquid"] = "unavailable"

    reference = context.get("spot_reference") if status["hyperliquid"] == "available" else None
    if reference is None and deribit.get("spot_index_usd"):
        reference = {"venue": "Deribit", "reference_type": "index", "price_usd": deribit["spot_index_usd"]}

    try:
        prediction = _enrich_prediction_markets(polymarket_run(asset), reference)
        status["polymarket_crypto"] = "available"
    except Exception as exc:
        prediction = _source_error("Polymarket Gamma and CLOB APIs", exc)
        status["polymarket_crypto"] = "unavailable"

    try:
        macro = macro_events()
        status["polymarket_macro"] = "available"
    except Exception as exc:
        macro = _source_error("Polymarket Gamma and CLOB APIs", exc)
        status["polymarket_macro"] = "unavailable"

    return {
        "source_status": status,
        "deribit_market_snapshot": deribit,
        "polymarket_crypto_markets": prediction,
        "polymarket_macro_events": macro,
        "underlying_reference": reference,
        "perp_technical_snapshot": context.get("technical_snapshot", {}),
        "perp_carry_snapshot": context.get("perp_snapshot", {}),
        "hyperliquid_context": context,
    }


def _evidence_ids(index: dict, asset: str) -> list[str]:
    preferred = (
        f"deribit:{asset}:surface-dossier",
        f"hyperliquid:{asset}:technical",
        f"hyperliquid:{asset}:carry",
        f"polymarket:{asset}:probability-dossier",
    )
    available = {row["id"] for row in index.get("records", [])}
    ids = [record_id for record_id in preferred if record_id in available]
    macro = next((row["id"] for row in index.get("records", []) if row["kind"] == "macro_event"), None)
    return ids + ([macro] if macro else [])


def _walk_keys(value):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from _walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _walk_keys(nested)


def _display_name(identifier: str) -> str:
    return identifier.replace("_", " ").capitalize()


def _regime_name(identifier: str) -> str:
    return identifier.replace("_", " ").title()


def _render_mapping(value: dict, indent: int = 0) -> list[str]:
    lines = []
    prefix = "  " * indent
    for key, nested in value.items():
        label = str(key).replace("_", " ").capitalize()
        if isinstance(nested, dict):
            lines.append(f"{prefix}- {label}:")
            lines.extend(_render_mapping(nested, indent + 1) if nested else [f"{prefix}  - Unavailable"])
        elif isinstance(nested, list):
            lines.append(f"{prefix}- {label}:")
            if not nested:
                lines.append(f"{prefix}  - None")
            for item in nested:
                if isinstance(item, dict):
                    lines.append(f"{prefix}  - {json.dumps(item, sort_keys=True)}")
                else:
                    lines.append(f"{prefix}  - {item}")
        else:
            lines.append(f"{prefix}- {label}: {'Unavailable' if nested is None else nested}")
    return lines


def _render_strategy_summary(card: dict) -> str:
    """Render the complete human-readable strategy analysis for display."""
    regime = card["market_regime"]
    recommendation = card["recommended_strategy"]
    lines = [
        "Not investment advice.",
        "",
        f"# {card['asset']} Strategy Analysis",
        "",
        f"As of: {card['as_of']}",
        "",
        "## Market regime",
        "",
        f"Type: {_regime_name(regime['type'])}",
        f"Classification confidence: {round(float(regime['confidence']) * 100):d}/100",
        f"Summary: {regime['summary']}",
        "",
        "## Market evidence",
        "",
        *_render_mapping(card["market_metrics"]),
        "",
        "## Recommended strategy",
        "",
        f"Best fit: {_display_name(recommendation['strategy_id'])}",
        f"Horizon: {recommendation['horizon']}",
        f"Score: {round(float(recommendation['score'])):d}/100",
        f"Risk profile: {recommendation['risk_profile']}",
        "",
        "Recommended parameter range:",
        *_render_mapping(recommendation["recommended_parameter_range"], 1),
        "",
        "Why:",
        *[f"- {reason}" for reason in recommendation["reasons"]],
        "",
        "Use only if:",
        *[f"- {condition}" for condition in recommendation["entry_conditions"]],
        "",
        "Invalidation:",
        *[f"- {condition}" for condition in recommendation["invalidation"]],
    ]
    if recommendation["strategy_id"] == "wait":
        lines.extend(["", "Reassess when:", f"- {recommendation['reassessment_trigger']}"])
    lines.extend(["", "## Alternatives", ""])
    lines.extend(
        f"- {_display_name(item['strategy_id'])}: {round(float(item['score'])):d}/100; horizon {item['horizon']}"
        for item in card["alternatives"]
    )
    lines.extend(["", "## Complete strategy ranking", ""])
    lines.extend(
        f"- {_display_name(item['strategy_id'])}: {round(float(item['score'])):d}/100; "
        f"horizon {item['horizon_days'][0]}–{item['horizon_days'][1]} days; "
        f"regime eligible: {'yes' if item['eligible_for_regime'] else 'no'}"
        for item in card["strategy_rankings"]
    )
    lines.extend(["", "## Evidence records", ""])
    lines.extend(f"- {record_id}" for record_id in card["evidence_ids"])
    return "\n".join(lines) + "\n"


def _validate_strategy_card(card: dict, record_ids: set[str] | None = None) -> None:
    """Validate a portable, non-executable strategy card before saving it."""
    if not isinstance(card, dict):
        raise ValueError("card must be a JSON object")
    asset = str(card.get("asset", "")).upper()
    if asset not in {"BTC", "ETH"}:
        raise ValueError("card.asset must be BTC or ETH")
    if not str(card.get("as_of", "")).strip() or not isinstance(card.get("market_metrics"), dict):
        raise ValueError("card requires as_of and market_metrics")
    required_metrics = {"spot_price", "realized_volatility_by_horizon", "price_levels", "prediction_market_read", "surface_fit_quality", "option_surface_read", "futures_curve_read"}
    if not required_metrics <= set(card["market_metrics"]):
        raise ValueError("market_metrics must preserve the full fitted market read")
    if any(key in _PROHIBITED_CARD_KEYS for key in _walk_keys(card)):
        raise ValueError("card contains an exact instrument, performance claim, sizing, or leverage field")
    regime = card.get("market_regime", {})
    if regime.get("type") not in REGIMES or not 0 <= float(regime.get("confidence", -1)) <= 1 or not str(regime.get("summary", "")).strip():
        raise ValueError("market_regime must contain a predefined type, confidence, and summary")
    recommendation = card.get("recommended_strategy", {})
    strategy_id = recommendation.get("strategy_id")
    if strategy_id not in STRATEGY_BY_ID:
        raise ValueError("recommended_strategy.strategy_id is not in the strategy library")
    recommendation_fields = {
        "strategy_id", "horizon", "score", "risk_profile",
        "recommended_parameter_range", "reasons", "entry_conditions",
        "invalidation", "reassessment_trigger",
    }
    if not set(recommendation) <= recommendation_fields:
        raise ValueError("recommended_strategy contains unsupported fields")
    if not 0 <= float(recommendation.get("score", -1)) <= 100:
        raise ValueError("recommended strategy score is outside its valid range")
    for field in ("horizon", "risk_profile", "recommended_parameter_range", "reasons", "entry_conditions", "invalidation"):
        if not recommendation.get(field):
            raise ValueError(f"recommended_strategy.{field} is required")
    for field in ("reasons", "entry_conditions", "invalidation"):
        if not isinstance(recommendation[field], list) or not all(isinstance(item, str) and item.strip() for item in recommendation[field]):
            raise ValueError(f"recommended_strategy.{field} must be a non-empty list of text items")
    if recommendation["risk_profile"] != STRATEGY_BY_ID[strategy_id]["risk_profile"]:
        raise ValueError("recommended strategy risk profile does not match the library")
    if json.loads(json.dumps(recommendation["recommended_parameter_range"])) != json.loads(json.dumps(STRATEGY_BY_ID[strategy_id]["parameter_range"])):
        raise ValueError("recommended parameter range must come from the strategy library")
    if strategy_id == "wait" and not str(recommendation.get("reassessment_trigger", "")).strip():
        raise ValueError("a wait recommendation requires a specific reassessment_trigger")
    rankings = card.get("strategy_rankings")
    if not isinstance(rankings, list) or len(rankings) != len(STRATEGY_BY_ID):
        raise ValueError("strategy_rankings must contain every library strategy exactly once")
    ranking_ids = [row.get("strategy_id") for row in rankings]
    if set(ranking_ids) != set(STRATEGY_BY_ID) or len(set(ranking_ids)) != len(ranking_ids):
        raise ValueError("strategy_rankings must contain every library strategy exactly once")
    rankings_by_id = {}
    for row in rankings:
        if set(row) != {"strategy_id", "score", "horizon_days", "eligible_for_regime"}:
            raise ValueError("each strategy ranking must use the documented score-only schema")
        if (
            not 0 <= float(row.get("score", -1)) <= 100
            or not isinstance(row.get("horizon_days"), list)
            or len(row["horizon_days"]) != 2
            or not isinstance(row.get("eligible_for_regime"), bool)
        ):
            raise ValueError("each strategy ranking needs a score, horizon_days, and regime eligibility")
        rankings_by_id[row["strategy_id"]] = row
    selected_row = rankings_by_id[strategy_id]
    if float(recommendation["score"]) != float(selected_row["score"]):
        raise ValueError("recommended strategy score must match its deterministic ranking")
    alternatives = card.get("alternatives")
    if not isinstance(alternatives, list) or len(alternatives) < 2:
        raise ValueError("card must contain at least two alternatives")
    for alternative in alternatives:
        if set(alternative) != {"strategy_id", "score", "horizon"}:
            raise ValueError("each alternative must use the documented score-only schema")
        if (
            alternative.get("strategy_id") not in STRATEGY_BY_ID
            or not 0 <= float(alternative.get("score", -1)) <= 100
            or not alternative.get("horizon")
        ):
            raise ValueError("each alternative needs a library strategy, score, and horizon")
        ranking = rankings_by_id[alternative["strategy_id"]]
        if float(alternative["score"]) != float(ranking["score"]):
            raise ValueError("alternative score must match its deterministic ranking")
    alternative_ids = [alternative["strategy_id"] for alternative in alternatives]
    if strategy_id in alternative_ids or len(set(alternative_ids)) != len(alternative_ids):
        raise ValueError("alternatives must be distinct from the recommended strategy and each other")
    evidence_ids = card.get("evidence_ids")
    if not isinstance(evidence_ids, list) or not evidence_ids:
        raise ValueError("card.evidence_ids must contain raw research record IDs")
    if record_ids is not None and not set(evidence_ids) <= record_ids:
        raise ValueError("card evidence IDs must exist in the research bundle")


def _asset(value: str) -> str:
    asset = value.upper()
    if asset not in {"BTC", "ETH"}:
        raise ValueError("Choose exactly one supported asset: BTC or ETH.")
    return asset


def _packet(asset: str, **data) -> dict:
    payload = {
        "source_status": {},
        "deribit_market_snapshot": {},
        "polymarket_crypto_markets": {},
        "polymarket_macro_events": {"events": [], "markets": []},
        "underlying_reference": None,
        "perp_technical_snapshot": {},
        "perp_carry_snapshot": {},
        "hyperliquid_context": {},
    }
    payload.update(data)
    return {"asset": asset, "as_of": datetime.now(timezone.utc).isoformat(), "data": payload}


@mcp.tool()
def collect_deribit_snapshot(asset: str) -> dict:
    """Collect the complete current Deribit options and dated-futures snapshot.

    Raw contracts are saved to an immutable research bundle. The response stays
    compact and intentionally does not fit the volatility surface.
    """
    asset = _asset(asset)
    snapshot = consolidated_market_snapshot(asset, fit=False)
    packet = _packet(asset, source_status={"deribit": "available"}, deribit_market_snapshot=snapshot)
    bundle = _save_research_bundle(packet)
    return {
        "asset": asset,
        "as_of": snapshot["as_of"],
        "research_bundle": bundle,
        "spot_index_usd": snapshot.get("spot_index_usd"),
        "surface_inventory": snapshot.get("surface_inventory"),
        "dated_futures_curve": snapshot.get("dated_futures_curve"),
        "instruction": "Use fit_deribit_surface with this research_bundle_id for a fitted surface without recollecting.",
    }


@mcp.tool()
def fit_deribit_surface(asset: str, research_bundle_id: str = "") -> dict:
    """Fit and validate a Deribit SVI surface from a saved or fresh snapshot."""
    asset = _asset(asset)
    if research_bundle_id:
        manifest, raw, _ = _load_research_bundle(research_bundle_id)
        if manifest["asset"] != asset:
            raise ValueError("asset does not match the research bundle")
        snapshot = raw.get("data", {}).get("deribit_market_snapshot", {})
        if not snapshot.get("expiry_slices"):
            raise ValueError("research bundle does not contain a Deribit option snapshot")
    else:
        snapshot = consolidated_market_snapshot(asset, fit=False)
    fitted_snapshot = {**snapshot, "surface_dossier": fit_option_surface(snapshot)}
    packet = _packet(asset, source_status={"deribit": "available"}, deribit_market_snapshot=fitted_snapshot)
    bundle = _save_research_bundle(packet)
    return {"asset": asset, "as_of": snapshot.get("as_of"), "research_bundle": bundle, "surface_dossier": fitted_snapshot["surface_dossier"], "dated_futures_curve": snapshot.get("dated_futures_curve", [])}


@mcp.tool()
def analyze_market_context(asset: str) -> dict:
    """Collect Hyperliquid context and analyze trend, carry, realized volatility, and levels."""
    asset = _asset(asset)
    context = market_context_run(asset)
    packet = _packet(
        asset,
        source_status={"hyperliquid": "available"},
        underlying_reference=context.get("spot_reference"),
        perp_technical_snapshot=context.get("technical_snapshot", {}),
        perp_carry_snapshot=context.get("perp_snapshot", {}),
        hyperliquid_context=context,
    )
    bundle = _save_research_bundle(packet)
    return {
        "asset": asset,
        "as_of": context.get("as_of"),
        "research_bundle": bundle,
        "technical_snapshot": context.get("technical_snapshot"),
        "carry_snapshot": context.get("perp_snapshot"),
        "realized_volatility_dossier": context.get("realized_volatility_dossier"),
        "price_level_dossier": context.get("price_level_dossier"),
    }


@mcp.tool()
def collect_polymarket_snapshot(asset: str, reference_price_usd: float = 0) -> dict:
    """Collect active, semantically filtered crypto price markets without fitting them."""
    asset = _asset(asset)
    reference = {"venue": "caller", "reference_type": "supplied_usd", "price_usd": reference_price_usd} if reference_price_usd > 0 else None
    markets = _enrich_prediction_markets(polymarket_run(asset), reference, fit=False)
    packet = _packet(asset, source_status={"polymarket_crypto": "available"}, underlying_reference=reference, polymarket_crypto_markets=markets)
    bundle = _save_research_bundle(packet)
    return {"asset": asset, "as_of": markets.get("as_of"), "research_bundle": bundle, "event_windows": markets.get("event_windows", []), "coverage": {"terminal_contracts": len(markets.get("terminal_markets", [])), "barrier_contracts": len(markets.get("barrier_markets", []))}, "instruction": "Use fit_polymarket_probabilities with this research_bundle_id to normalize comparable terminal ladders."}


@mcp.tool()
def fit_polymarket_probabilities(asset: str, research_bundle_id: str = "", reference_price_usd: float = 0) -> dict:
    """Fit quote-quality-weighted terminal probability ladders from saved or fresh markets."""
    asset = _asset(asset)
    if research_bundle_id:
        manifest, raw, _ = _load_research_bundle(research_bundle_id)
        if manifest["asset"] != asset:
            raise ValueError("asset does not match the research bundle")
        markets = raw.get("data", {}).get("polymarket_crypto_markets", {})
        if not markets.get("terminal_markets") and not markets.get("barrier_markets"):
            raise ValueError("research bundle does not contain Polymarket crypto markets")
    else:
        reference = {"venue": "caller", "reference_type": "supplied_usd", "price_usd": reference_price_usd} if reference_price_usd > 0 else None
        markets = _enrich_prediction_markets(polymarket_run(asset), reference, fit=False)
    if reference_price_usd > 0:
        markets = {**markets, "current_underlying_reference": {"venue": "caller", "reference_type": "supplied_usd", "price_usd": reference_price_usd}}
    dossier = fit_prediction_market(markets)
    fitted_markets = {**markets, "prediction_market_dossier": dossier}
    packet = _packet(asset, source_status={"polymarket_crypto": "available"}, underlying_reference=fitted_markets.get("current_underlying_reference"), polymarket_crypto_markets=fitted_markets)
    bundle = _save_research_bundle(packet)
    return {"asset": asset, "as_of": markets.get("as_of"), "research_bundle": bundle, "prediction_market_dossier": dossier}


@mcp.tool()
def get_strategy_library(strategy_id: str = "") -> dict:
    """Return supported regimes and either the complete strategy bank or one template."""
    if strategy_id:
        if strategy_id not in STRATEGY_BY_ID:
            raise ValueError(f"unknown strategy_id: {strategy_id}")
        strategies = [STRATEGY_BY_ID[strategy_id]]
    else:
        strategies = list(STRATEGIES)
    return {
        "regimes": list(REGIMES),
        "strategies": strategies,
        "score_definition": "Setup fit from 0 to 100; not a win rate or expected return.",
    }


@mcp.tool()
def analyze_research_bundle(research_bundle_id: str) -> dict:
    """Build deterministic metrics, regime, and ranked strategies from a complete bundle."""
    manifest, raw, index = _load_research_bundle(research_bundle_id)
    analysis = build_strategy_inputs(raw.get("data", {}), raw.get("as_of") or manifest["created_at"])
    analysis["evidence_ids"] = _evidence_ids(index, manifest["asset"])
    return {"asset": manifest["asset"], "as_of": raw.get("as_of"), "research_bundle": manifest, "analysis": analysis}


@mcp.tool()
def get_crypto_strategy_inputs(asset: str) -> dict:
    """Collect one BTC or ETH market snapshot and return complete fitted strategy inputs.

    Complete Deribit, Hyperliquid, and Polymarket observations are saved to a
    queryable local bundle. The response contains fitted surface, volatility,
    levels, prediction-market, regime, and ranked setup reads. Source failures
    are isolated and reported explicitly.
    """
    asset = _asset(asset)
    packet = {"asset": asset, "as_of": datetime.now(timezone.utc).isoformat(), "data": _collect_asset(asset)}
    bundle = _save_research_bundle(packet)
    index = json.loads(Path(bundle["research_index_path"]).read_text(encoding="utf-8"))
    analysis = build_strategy_inputs(packet["data"], packet["as_of"])
    analysis["evidence_ids"] = _evidence_ids(index, asset)
    by_kind = {}
    for record in index["records"]:
        by_kind[record["kind"]] = by_kind.get(record["kind"], 0) + 1
    return {
        "asset": asset,
        "as_of": packet["as_of"],
        "research_bundle": bundle,
        "inventory": {"record_count": index["record_count"], "by_kind": by_kind},
        "analysis": analysis,
        "regime_types": REGIMES,
        "strategy_library": STRATEGIES,
        "instruction": "Preserve every ranked strategy score unchanged in the saved card. Apply market judgment when selecting the recommendation, then save it with save_strategy_card. A strategy score is setup fit, not a win rate or expected return.",
    }


@mcp.tool()
def query_research_bundle(research_bundle_id: str, record_ids: list[str] | None = None, text: str = "", limit: int = 40) -> dict:
    """Read selected records from a saved bundle without recollecting market data."""
    manifest, raw, index = _load_research_bundle(research_bundle_id)
    limit = max(1, min(int(limit), 200))
    records = index.get("records", [])
    by_id = {row["id"]: row for row in records}
    if record_ids:
        missing = [record_id for record_id in record_ids if record_id not in by_id]
        if missing:
            raise ValueError(f"unknown research record IDs: {', '.join(missing[:5])}")
        selected = [by_id[record_id] for record_id in record_ids]
    elif text.strip():
        needle = text.lower().strip()
        selected = [row for row in records if needle in json.dumps(row, sort_keys=True).lower()][:limit]
    else:
        selected = records[:limit]
    result = [{**row, "data": _pointer_get(raw, row["pointer"])} for row in selected[:limit]]
    return {"research_bundle": manifest, "returned": len(result), "total_records": len(records), "records": result}


@mcp.tool()
def save_strategy_card(card: dict, research_bundle_id: str) -> dict:
    """Validate one strategy card, save JSON, and return its display summary."""
    manifest, _, index = _load_research_bundle(research_bundle_id)
    if str(card.get("asset", "")).upper() != manifest["asset"]:
        raise ValueError("card asset does not match the research bundle")
    _validate_strategy_card(card, {row["id"] for row in index.get("records", [])})
    root = _output_root()
    root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stem = f"{card['asset'].lower()}-strategy-card-{stamp}-{uuid4().hex[:8]}"
    json_path = root / f"{stem}.json"
    payload = {**card, "research_bundle_id": research_bundle_id}
    rendered = _render_strategy_summary(card)
    saved_json = json.dumps(payload, indent=2)
    json_path.write_text(saved_json, encoding="utf-8")
    return {
        "strategy_card_json_path": str(json_path),
        "rendered_summary": rendered,
        "saved_card_json": saved_json,
        "research_bundle": manifest,
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
