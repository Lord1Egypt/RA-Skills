#!/usr/bin/env python
"""Probe Abel CAP server verbs with no third-party dependencies."""

from __future__ import annotations

import sys
import argparse
import json
import os
import uuid
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_BASE_URL = "https://cap.abel.ai/api"
CAP_VERSION = "0.2.2"
TEXT_TRUNCATE_EXACT_KEYS = {
    "description",
    "summary",
    "content",
    "message",
    "details",
}
GLOBAL_OPTIONS = {
    "--base-url": True,
    "--api-key": True,
    "--env-file": True,
    "--pick-fields": True,
    "--max-description-chars": True,
    "--compact": False,
}
COMMANDS = {
    "auth-status",
    "capabilities",
    "normalize-node",
    "methods",
    "observe",
    "observe-dual",
    "neighbors",
    "paths",
    "markov-blanket",
    "intervene-do",
    "traverse-parents",
    "traverse-children",
    "abel-markov-blanket",
    "counterfactual-preview",
    "intervene-time-lag",
    "verb",
    "route",
}

SUPPORTED_NODE_SUFFIXES = {"price", "volume"}
COMMON_CRYPTO_ALIASES = {
    "BTC",
    "ETH",
    "SOL",
    "XRP",
    "DOGE",
    "ADA",
    "AVAX",
}
KNOWN_MACRO_NODE_IDS = {
    "15YearFixedRateMortgageAverage",
    "30YearFixedRateMortgageAverage",
    "3MonthOr90DayRatesAndYieldsCertificatesOfDeposit",
    "CPI",
    "GDP",
    "commercialBankInterestRateOnCreditCardPlansAllAccounts",
    "consumerSentiment",
    "durableGoods",
    "federalFunds",
    "industrialProductionTotalIndex",
    "inflation",
    "inflationRate",
    "initialClaims",
    "newPrivatelyOwnedHousingUnitsStartedTotalUnits",
    "nominalPotentialGDP",
    "realGDP",
    "realGDPPerCapita",
    "retailMoneyFunds",
    "retailSales",
    "smoothedUSRecessionProbabilities",
    "totalNonfarmPayroll",
    "totalVehicleSales",
    "treasuryRateYear10",
    "unemploymentRate",
}
KNOWN_MACRO_NODE_ID_MAP = {node_id.lower(): node_id for node_id in KNOWN_MACRO_NODE_IDS}
ENV_FILE_BASENAMES = (".env.skill", ".env.skills")
ENV_FALLBACK_BASENAME = ".env"


def _candidate_env_files(path: str) -> list[Path]:
    env_path = Path(path).expanduser()
    candidates = [env_path]
    if env_path.name in ENV_FILE_BASENAMES:
        for basename in ENV_FILE_BASENAMES:
            candidate = env_path.with_name(basename)
            if candidate not in candidates:
                candidates.append(candidate)
        fallback_candidate = env_path.with_name(ENV_FALLBACK_BASENAME)
        if fallback_candidate not in candidates:
            candidates.append(fallback_candidate)
    return candidates


def _read_env_file_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def _load_env_file(path: str) -> None:
    for candidate in _candidate_env_files(path):
        if not candidate.exists():
            continue
        for key, value in _read_env_file_values(candidate).items():
            if key and key not in os.environ:
                os.environ[key] = value
        return


def _resolve_base_url(value: str | None) -> str:
    return (value or DEFAULT_BASE_URL).strip()


def resolve_cap_endpoint(base_url: str) -> str:
    parsed = urllib.parse.urlsplit(base_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid base URL: {base_url!r}")
    path = parsed.path.rstrip("/")
    if path.endswith("/echo"):
        endpoint_path = f"{path}/api/v1/cap"
    else:
        endpoint_path = f"{path}/cap"
    return urllib.parse.urlunsplit(
        (parsed.scheme, parsed.netloc, endpoint_path, "", "")
    )


def _cap_endpoint(base_url: str) -> str:
    return resolve_cap_endpoint(base_url)


def _resolve_headers(api_key: str | None) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    token = _resolve_api_token(api_key)
    if not token:
        return headers
    if token.lower().startswith("bearer "):
        headers["Authorization"] = token
    else:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _resolve_api_token(api_key: str | None) -> str:
    return (
        api_key or os.getenv("CAP_API_KEY") or os.getenv("ABEL_API_KEY") or ""
    ).strip()


def _resolve_auth_status(api_key: str | None, env_file: str) -> dict[str, Any]:
    if (api_key or "").strip():
        return {
            "auth_ready": True,
            "auth_source": "--api-key",
            "oauth_required": False,
        }

    for env_var in ("CAP_API_KEY", "ABEL_API_KEY"):
        if (os.getenv(env_var) or "").strip():
            return {
                "auth_ready": True,
                "auth_source": "session",
                "oauth_required": False,
            }

    for candidate in _candidate_env_files(env_file):
        values = _read_env_file_values(candidate)
        if any((values.get(key) or "").strip() for key in ("CAP_API_KEY", "ABEL_API_KEY")):
            return {
                "auth_ready": True,
                "auth_source": candidate.name,
                "oauth_required": False,
            }

    return {
        "auth_ready": False,
        "auth_source": "missing",
        "oauth_required": True,
    }


def _extract_path(obj: Any, path: str) -> tuple[bool, Any]:
    current = obj
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return False, None
        current = current[part]
    return True, current


def _set_path(obj: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    cursor = obj
    for part in parts[:-1]:
        nxt = cursor.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cursor[part] = nxt
        cursor = nxt
    cursor[parts[-1]] = value


def _apply_pick_fields(result: dict[str, Any], pick_fields: str) -> dict[str, Any]:
    fields = [item.strip() for item in pick_fields.split(",") if item.strip()]
    if not fields:
        return result
    out: dict[str, Any] = {}
    for key in ("ok", "status_code", "verb", "request_id"):
        if key in result:
            out[key] = result[key]
    if result.get("ok") is False:
        for key in ("message", "error", "response_payload"):
            if key in result:
                out[key] = result[key]
    for path in fields:
        ok, value = _extract_path(result, path)
        if ok:
            _set_path(out, path, value)
    return out


def _should_truncate_text_field(key: str) -> bool:
    normalized = key.strip().lower()
    if not normalized:
        return False
    if normalized in TEXT_TRUNCATE_EXACT_KEYS:
        return True
    return "description" in normalized


def _truncate_text(value: str, max_chars: int) -> str:
    if max_chars <= 0 or len(value) <= max_chars:
        return value
    return f"{value[:max_chars]}..."


def _truncate_description_fields(obj: Any, max_chars: int) -> Any:
    if max_chars <= 0:
        return obj
    if isinstance(obj, dict):
        transformed: dict[str, Any] = {}
        for key, value in obj.items():
            if isinstance(value, str) and _should_truncate_text_field(key):
                transformed[key] = _truncate_text(value, max_chars)
            else:
                transformed[key] = _truncate_description_fields(value, max_chars)
        return transformed
    if isinstance(obj, list):
        return [_truncate_description_fields(item, max_chars) for item in obj]
    return obj


def _route_to_verb(route: str) -> str:
    normalized = route.strip().strip("/")
    if not normalized:
        raise ValueError("Route alias cannot be empty.")
    if "/" not in normalized:
        return normalized.strip(".")
    return ".".join(segment for segment in normalized.split("/") if segment)


def _build_payload(verb: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "cap_version": CAP_VERSION,
        "request_id": str(uuid.uuid4()),
        "verb": verb,
    }
    if params is not None:
        payload["params"] = params
    return payload


def _looks_like_ticker(value: str) -> bool:
    if not value:
        return False
    if len(value) > 6 and value != value.upper():
        return False
    allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.")
    upper = value.upper()
    return all(char in allowed for char in upper)


def _normalize_public_node_id(value: str, *, default_suffix: str = "price") -> str:
    raw = value.strip()
    if not raw:
        raise ValueError("Node input cannot be empty.")

    if default_suffix not in SUPPORTED_NODE_SUFFIXES:
        raise ValueError(
            f"Unsupported default suffix {default_suffix!r}; expected one of {sorted(SUPPORTED_NODE_SUFFIXES)}."
        )

    normalized = raw.upper()
    ticker, separator, suffix = normalized.rpartition(".")
    if separator:
        if not ticker or not suffix:
            raise ValueError(
                "Node input must use '<ticker>.<field>' when a dot is present."
            )
        suffix = suffix.lower()
        if suffix not in SUPPORTED_NODE_SUFFIXES:
            raise ValueError(
                "Abel public node ids currently support only '<ticker>.price' or '<ticker>.volume'."
            )
        return f"{ticker}.{suffix}"

    ticker, separator, suffix = normalized.rpartition("_")
    if separator:
        if not ticker or not suffix:
            raise ValueError(
                "Node input must use Abel public node ids like '<ticker>.price' or '<ticker>.volume'."
            )
        suffix = suffix.lower()
        if suffix == "close":
            return f"{ticker}.price"
        if suffix == "volume":
            return f"{ticker}.volume"
        if suffix == "close_price":
            raise ValueError(
                "Use Abel public node ids like '<ticker>.price' or '<ticker>.volume'."
            )
        raise ValueError(
            "Abel public node ids currently support only '<ticker>.price' or '<ticker>.volume'."
        )

    if _looks_like_ticker(raw):
        if normalized in COMMON_CRYPTO_ALIASES:
            return f"{normalized}USD.{default_suffix}"
        return f"{normalized}.{default_suffix}"

    raise ValueError(
        "Input does not look like a ticker or public node id. Map the proxy phrase to a ticker first, then probe '<ticker>.price' or '<ticker>.volume'."
    )
def _normalize_graph_capable_node_id(value: str, *, default_suffix: str = "price") -> str:
    raw = value.strip()
    if not raw:
        raise ValueError("Node input cannot be empty.")

    macro_node_id = KNOWN_MACRO_NODE_ID_MAP.get(raw.lower())
    if macro_node_id is not None:
        return macro_node_id

    return _normalize_public_node_id(raw, default_suffix=default_suffix)


def _strip_public_node_suffix(value: str) -> str:
    raw = value.strip()
    if not raw:
        raise ValueError("Node input cannot be empty.")

    normalized = raw.upper()
    ticker, separator, suffix = normalized.rpartition(".")
    if separator and suffix.lower() in SUPPORTED_NODE_SUFFIXES:
        return ticker

    ticker, separator, suffix = normalized.rpartition("_")
    if separator:
        suffix = suffix.lower()
        if suffix in {"close", "close_price", "volume"}:
            return ticker

    return raw


def _normalize_dual_anchor_nodes(value: str) -> dict[str, str]:
    base_value = _strip_public_node_suffix(value)
    return {
        "price": _normalize_public_node_id(base_value, default_suffix="price"),
        "volume": _normalize_public_node_id(base_value, default_suffix="volume"),
    }


def _json_or_text(raw: bytes) -> Any:
    text = raw.decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}


def _post_cap(
    base_url: str, verb: str, params: dict[str, Any] | None, headers: dict[str, str]
) -> dict[str, Any]:
    payload = _build_payload(verb, params)
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        _cap_endpoint(base_url),
        data=data,
        method="POST",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=20.0) as response:
            parsed = _json_or_text(response.read())
            if isinstance(parsed, dict):
                return {"ok": True, "status_code": response.status, **parsed}
            return {"ok": True, "status_code": response.status, "response": parsed}
    except urllib.error.HTTPError as exc:
        parsed = _json_or_text(exc.read())
        message = str(exc)
        error: dict[str, Any] | None = None
        if isinstance(parsed, dict):
            error_payload = parsed.get("error")
            if isinstance(error_payload, dict):
                error = error_payload
                message = error_payload.get("message") or message
            elif isinstance(parsed.get("message"), str):
                message = parsed["message"]
        return {
            "ok": False,
            "status_code": exc.code,
            "message": message,
            "error": error,
            "response_payload": parsed,
        }
    except urllib.error.URLError as exc:
        return {
            "ok": False,
            "status_code": -1,
            "message": str(exc.reason),
            "error": None,
            "response_payload": {},
        }


def _call_verb(
    args: argparse.Namespace, verb: str, params: dict[str, Any] | None = None
) -> dict[str, Any]:
    return _post_cap(
        _resolve_base_url(args.base_url),
        verb,
        params,
        _resolve_headers(args.api_key),
    )


def _coerce_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.isdigit() or (stripped.startswith("-") and stripped[1:].isdigit()):
            return int(stripped)
    return None


def _extract_paths_verdict(payload: Any) -> bool | None:
    if isinstance(payload, dict):
        for key in (
            "path_exists",
            "has_path",
            "reachable",
            "connected",
            "is_connected",
        ):
            value = payload.get(key)
            if isinstance(value, bool):
                return value

        for key in ("path_count", "paths_count", "num_paths", "count"):
            count = _coerce_int(payload.get(key))
            if count is not None:
                return count > 0

        for key in ("paths", "path", "results"):
            value = payload.get(key)
            if isinstance(value, list):
                return len(value) > 0

        for key in ("result", "data", "response", "response_payload"):
            if key in payload:
                verdict = _extract_paths_verdict(payload[key])
                if verdict is not None:
                    return verdict

        for value in payload.values():
            verdict = _extract_paths_verdict(value)
            if verdict is not None:
                return verdict
        return None

    if isinstance(payload, list):
        return len(payload) > 0

    return None


def _cmd_capabilities(args: argparse.Namespace) -> dict[str, Any]:
    return _call_verb(args, "meta.capabilities")


def _cmd_auth_status(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "ok": True,
        "status_code": 0,
        **_resolve_auth_status(args.api_key, args.env_file),
    }


def _cmd_normalize_node(args: argparse.Namespace) -> dict[str, Any]:
    normalized = _normalize_graph_capable_node_id(
        args.input_value,
        default_suffix=args.default_suffix,
    )
    return {
        "ok": True,
        "status_code": 0,
        "input": args.input_value,
        "normalized_node_id": normalized,
        "default_suffix": args.default_suffix,
    }


def _cmd_methods(args: argparse.Namespace) -> dict[str, Any]:
    params: dict[str, Any] = {}
    if args.verbs:
        params["verbs"] = args.verbs
    if args.detail != "compact":
        params["detail"] = args.detail
    if args.include_examples:
        params["include_examples"] = True
    return _call_verb(args, "meta.methods", params or None)


def _cmd_observe(args: argparse.Namespace) -> dict[str, Any]:
    return _call_verb(
        args,
        "observe.predict",
        {
            "target_node": _normalize_public_node_id(
                args.target_node,
                default_suffix=args.default_suffix,
            )
        },
    )


def _cmd_observe_dual(args: argparse.Namespace) -> dict[str, Any]:
    anchors = _normalize_dual_anchor_nodes(args.target_node)
    price_result = _call_verb(
        args,
        "extensions.abel.observe_predict_resolved_time",
        {"target_node": anchors["price"]},
    )
    volume_result = _call_verb(
        args,
        "extensions.abel.observe_predict_resolved_time",
        {"target_node": anchors["volume"]},
    )

    if price_result.get("ok") and volume_result.get("ok"):
        recommended_primary_anchor = "both"
        recommendation_reason = (
            "Both price and volume observations materialized; keep both in the first pass."
        )
    elif price_result.get("ok"):
        recommended_primary_anchor = "price"
        recommendation_reason = (
            "Price observation materialized while volume did not; continue on price and note the missing volume surface."
        )
    elif volume_result.get("ok"):
        recommended_primary_anchor = "volume"
        recommendation_reason = (
            "Volume observation materialized while price did not; continue on volume and note the missing price surface."
        )
    else:
        recommended_primary_anchor = "none"
        recommendation_reason = (
            "Neither price nor volume materialized; fall back to structural discovery or remap the anchor."
        )

    return {
        "ok": bool(price_result.get("ok") or volume_result.get("ok")),
        "status_code": 0,
        "input": args.target_node,
        "anchors": anchors,
        "recommended_primary_anchor": recommended_primary_anchor,
        "recommendation_reason": recommendation_reason,
        "price_observe": price_result,
        "volume_observe": volume_result,
    }


def _cmd_neighbors(args: argparse.Namespace) -> dict[str, Any]:
    return _call_verb(
        args,
        "graph.neighbors",
        {
            "node_id": _normalize_public_node_id(
                args.node_id,
                default_suffix=args.default_suffix,
            ),
            "scope": args.scope,
            "max_neighbors": args.max_neighbors,
        },
    )


def _cmd_paths(args: argparse.Namespace) -> dict[str, Any]:
    params = {
        "source_node_id": _normalize_graph_capable_node_id(
            args.source_node_id,
            default_suffix=args.default_suffix,
        ),
        "target_node_id": _normalize_graph_capable_node_id(
            args.target_node_id,
            default_suffix=args.default_suffix,
        ),
        "max_paths": args.max_paths,
    }
    if args.include_edge_signs:
        params["include_edge_signs"] = True
    return _call_verb(args, "graph.paths", params)


def _cmd_markov_blanket(args: argparse.Namespace) -> dict[str, Any]:
    return _call_verb(
        args,
        "graph.markov_blanket",
        {
            "node_id": _normalize_public_node_id(
                args.node_id,
                default_suffix=args.default_suffix,
            ),
            "max_neighbors": args.max_neighbors,
        },
    )


def _cmd_intervene_do(args: argparse.Namespace) -> dict[str, Any]:
    treatment_node = _normalize_public_node_id(
        args.treatment_node,
        default_suffix=args.default_suffix,
    )
    outcome_node = _normalize_public_node_id(
        args.outcome_node,
        default_suffix=args.default_suffix,
    )

    structural_check = _call_verb(
        args,
        "graph.paths",
        {
            "source_node_id": treatment_node,
            "target_node_id": outcome_node,
            "max_paths": getattr(args, "max_paths", 3),
        },
    )
    structural_ok = _extract_paths_verdict(structural_check)

    if structural_check.get("ok") is False:
        return {
            "ok": False,
            "status_code": structural_check.get("status_code", -1),
            "verb": "intervene.do",
            "message": (
                "Structural path check failed before intervene.do; intervention skipped."
            ),
            "treatment_node": treatment_node,
            "outcome_node": outcome_node,
            "treatment_value": args.treatment_value,
            "intervention_skipped": True,
            "skip_reason": "structural_check_failed",
            "structural_check": structural_check,
        }

    if structural_ok is None:
        return {
            "ok": False,
            "status_code": structural_check.get("status_code", 0),
            "verb": "intervene.do",
            "message": (
                "Structural path check returned an unrecognized payload; intervention skipped."
            ),
            "treatment_node": treatment_node,
            "outcome_node": outcome_node,
            "treatment_value": args.treatment_value,
            "intervention_skipped": True,
            "skip_reason": "structural_check_unrecognized",
            "structural_check": structural_check,
        }

    if not structural_ok:
        return {
            "ok": False,
            "status_code": structural_check.get("status_code", 0),
            "verb": "intervene.do",
            "message": (
                "No directed path found between treatment and outcome nodes; intervention skipped."
            ),
            "treatment_node": treatment_node,
            "outcome_node": outcome_node,
            "treatment_value": args.treatment_value,
            "intervention_skipped": True,
            "skip_reason": "no_directed_path_found",
            "structural_check": structural_check,
        }

    intervention_result = _call_verb(
        args,
        "intervene.do",
        {
            "treatment_node": treatment_node,
            "treatment_value": args.treatment_value,
            "outcome_node": outcome_node,
        },
    )
    intervention_result["structural_check"] = structural_check
    intervention_result["intervention_skipped"] = False
    return intervention_result


def _cmd_traverse_parents(args: argparse.Namespace) -> dict[str, Any]:
    return _call_verb(
        args,
        "traverse.parents",
        {
            "node_id": _normalize_public_node_id(
                args.node_id,
                default_suffix=args.default_suffix,
            ),
            "top_k": args.top_k,
        },
    )


def _cmd_traverse_children(args: argparse.Namespace) -> dict[str, Any]:
    return _call_verb(
        args,
        "traverse.children",
        {
            "node_id": _normalize_public_node_id(
                args.node_id,
                default_suffix=args.default_suffix,
            ),
            "top_k": args.top_k,
        },
    )
def _cmd_abel_markov_blanket(args: argparse.Namespace) -> dict[str, Any]:
    return _call_verb(
        args,
        "extensions.abel.markov_blanket",
        {
            "target_node": _normalize_public_node_id(
                args.target_node,
                default_suffix=args.default_suffix,
            )
        },
    )


def _cmd_counterfactual_preview(args: argparse.Namespace) -> dict[str, Any]:
    return _call_verb(
        args,
        "extensions.abel.counterfactual_preview",
        {
            "intervene_node": _normalize_public_node_id(
                args.intervene_node,
                default_suffix=args.default_suffix,
            ),
            "intervene_time": args.intervene_time,
            "observe_node": _normalize_public_node_id(
                args.observe_node,
                default_suffix=args.default_suffix,
            ),
            "observe_time": args.observe_time,
            "intervene_new_value": args.intervene_new_value,
        },
    )


def _resolve_time_lag_outcome_node(args: argparse.Namespace) -> str:
    positional_value = getattr(args, "outcome_node_positional", None)
    flag_value = getattr(args, "outcome_node", None)

    normalized_positional = None
    if positional_value:
        normalized_positional = _normalize_public_node_id(
            positional_value,
            default_suffix=args.default_suffix,
        )

    normalized_flag = None
    if flag_value:
        normalized_flag = _normalize_public_node_id(
            flag_value,
            default_suffix=args.default_suffix,
        )

    if (
        normalized_positional
        and normalized_flag
        and normalized_positional != normalized_flag
    ):
        raise ValueError(
            "Conflicting outcome node values provided via positional argument "
            "and --outcome-node."
        )

    resolved = normalized_flag or normalized_positional
    if not resolved:
        raise ValueError(
            "intervene-time-lag requires an outcome node either as the third "
            "positional argument or via --outcome-node."
        )
    return resolved


def _cmd_intervene_time_lag(args: argparse.Namespace) -> dict[str, Any]:
    return _call_verb(
        args,
        "extensions.abel.intervene_time_lag",
        {
            "treatment_node": _normalize_public_node_id(
                args.treatment_node,
                default_suffix=args.default_suffix,
            ),
            "treatment_value": args.treatment_value,
            "outcome_node": _resolve_time_lag_outcome_node(args),
            "horizon_steps": args.horizon_steps,
            "model": args.model,
        },
    )


def _cmd_verb(args: argparse.Namespace) -> dict[str, Any]:
    params = json.loads(args.params_json) if args.params_json else None
    if params is not None and not isinstance(params, dict):
        raise ValueError("--params-json must decode to a JSON object.")
    return _call_verb(args, args.verb_name, params)


def _cmd_route(args: argparse.Namespace) -> dict[str, Any]:
    params = json.loads(args.params_json) if args.params_json else None
    if params is not None and not isinstance(params, dict):
        raise ValueError("--params-json must decode to a JSON object.")
    return _call_verb(args, _route_to_verb(args.route_name), params)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Probe Abel CAP server verbs as atomic operations."
    )
    default_env = str(Path(__file__).resolve().parents[1] / ".env.skill")
    parser.add_argument(
        "--base-url",
        default="",
        help=f"CAP server base URL (default: {DEFAULT_BASE_URL}).",
    )
    parser.add_argument("--api-key", default="", help="Bearer token or raw API key.")
    parser.add_argument(
        "--env-file",
        default=default_env,
        help=f"Optional env file path (default: {default_env})",
    )
    parser.add_argument(
        "--pick-fields",
        default="",
        help="Comma-separated dot paths to keep from response root.",
    )
    parser.add_argument(
        "--max-description-chars",
        type=int,
        default=0,
        help="Max chars kept for description-like text fields. 0 disables truncation.",
    )
    parser.add_argument(
        "--compact", action="store_true", help="Print compact single-line JSON."
    )
    parser.add_argument(
        "--default-suffix",
        choices=("price", "volume"),
        default="price",
        help="Default suffix to append when a bare ticker is provided.",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser(
        "auth-status",
        help="Report whether auth is ready and which source would be used.",
    ).set_defaults(func=_cmd_auth_status)

    sub.add_parser("capabilities", help="Call meta.capabilities.").set_defaults(
        func=_cmd_capabilities
    )

    normalize = sub.add_parser(
        "normalize-node",
        help="Normalize a ticker, macro id, or node candidate to probe-ready node-id form.",
    )
    normalize.add_argument("input_value")
    normalize.set_defaults(func=_cmd_normalize_node)

    methods = sub.add_parser(
        "methods",
        help="Call meta.methods, optionally narrowed to specific verbs.",
    )
    methods.add_argument(
        "verbs",
        nargs="*",
        help="Optional verb names to request through params.verbs.",
    )
    methods.add_argument(
        "--detail",
        choices=("compact", "full"),
        default="compact",
        help="Requested method metadata profile (default: compact).",
    )
    methods.add_argument(
        "--include-examples",
        action="store_true",
        help="Ask the server to include examples when supported.",
    )
    methods.set_defaults(func=_cmd_methods)

    observe = sub.add_parser("observe", help="Call observe.predict.")
    observe.add_argument("target_node")
    observe.set_defaults(func=_cmd_observe)

    observe_dual = sub.add_parser(
        "observe-dual",
        help=(
            "Probe both <ticker>.price and <ticker>.volume with "
            "extensions.abel.observe_predict_resolved_time and recommend the first-pass anchor."
        ),
    )
    observe_dual.add_argument("target_node")
    observe_dual.set_defaults(func=_cmd_observe_dual)

    neighbors = sub.add_parser("neighbors", help="Call graph.neighbors.")
    neighbors.add_argument("node_id")
    neighbors.add_argument(
        "--scope", choices=("parents", "children"), default="parents"
    )
    neighbors.add_argument("--max-neighbors", type=int, default=5)
    neighbors.set_defaults(func=_cmd_neighbors)

    paths = sub.add_parser("paths", help="Call graph.paths.")
    paths.add_argument("source_node_id")
    paths.add_argument("target_node_id")
    paths.add_argument("--max-paths", type=int, default=3)
    paths.add_argument(
        "--include-edge-signs",
        action="store_true",
        help="Request signed edges in returned path details when supported.",
    )
    paths.set_defaults(func=_cmd_paths)

    blanket = sub.add_parser("markov-blanket", help="Call graph.markov_blanket.")
    blanket.add_argument("node_id")
    blanket.add_argument("--max-neighbors", type=int, default=10)
    blanket.set_defaults(func=_cmd_markov_blanket)

    intervene_do = sub.add_parser(
        "intervene-do",
        help="Check graph.paths, then call intervene.do when supported.",
    )
    intervene_do.add_argument("treatment_node")
    intervene_do.add_argument("treatment_value", type=float)
    intervene_do.add_argument("--outcome-node", required=True)
    intervene_do.add_argument(
        "--max-paths",
        type=int,
        default=3,
        help="Maximum paths requested for the required structural check.",
    )
    intervene_do.set_defaults(func=_cmd_intervene_do)

    traverse_parents = sub.add_parser("traverse-parents", help="Call traverse.parents.")
    traverse_parents.add_argument("node_id")
    traverse_parents.add_argument("--top-k", type=int, default=10)
    traverse_parents.set_defaults(func=_cmd_traverse_parents)

    traverse_children = sub.add_parser(
        "traverse-children", help="Call traverse.children."
    )
    traverse_children.add_argument("node_id")
    traverse_children.add_argument("--top-k", type=int, default=10)
    traverse_children.set_defaults(func=_cmd_traverse_children)

    abel_blanket = sub.add_parser(
        "abel-markov-blanket", help="Call extensions.abel.markov_blanket."
    )
    abel_blanket.add_argument("target_node")
    abel_blanket.set_defaults(func=_cmd_abel_markov_blanket)

    cf_preview = sub.add_parser(
        "counterfactual-preview", help="Call extensions.abel.counterfactual_preview."
    )
    cf_preview.add_argument("--intervene-node", required=True)
    cf_preview.add_argument("--intervene-time", required=True)
    cf_preview.add_argument("--observe-node", required=True)
    cf_preview.add_argument("--observe-time", required=True)
    cf_preview.add_argument("--intervene-new-value", required=True, type=float)
    cf_preview.set_defaults(func=_cmd_counterfactual_preview)

    time_lag = sub.add_parser(
        "intervene-time-lag",
        help=(
            "Call extensions.abel.intervene_time_lag. Accepts the outcome "
            "node as either the third positional argument or --outcome-node."
        ),
    )
    time_lag.add_argument("treatment_node")
    time_lag.add_argument("treatment_value", type=float)
    time_lag.add_argument("outcome_node_positional", nargs="?", metavar="outcome_node")
    time_lag.add_argument(
        "--outcome-node",
        help="Outcome node. Optional if supplied as the third positional argument.",
    )
    time_lag.add_argument("--horizon-steps", type=int, default=24)
    time_lag.add_argument("--model", default="linear")
    time_lag.set_defaults(func=_cmd_intervene_time_lag)

    generic_verb = sub.add_parser(
        "verb", help="Call an arbitrary CAP verb with optional JSON params."
    )
    generic_verb.add_argument("verb_name")
    generic_verb.add_argument(
        "--params-json", default="", help="JSON object passed as params."
    )
    generic_verb.set_defaults(func=_cmd_verb)

    generic_route = sub.add_parser(
        "route", help="Call an arbitrary Abel route alias with optional JSON params."
    )
    generic_route.add_argument("route_name")
    generic_route.add_argument(
        "--params-json", default="", help="JSON object passed as params."
    )
    generic_route.set_defaults(func=_cmd_route)

    return parser


def _normalize_argv(argv: list[str]) -> list[str]:
    if not argv:
        return argv

    prefix: list[str] = []
    suffix: list[str] = []
    command_seen = False
    i = 0
    while i < len(argv):
        token = argv[i]
        if not command_seen and token in COMMANDS:
            command_seen = True
            suffix.append(token)
            i += 1
            continue

        if command_seen and token in GLOBAL_OPTIONS:
            prefix.append(token)
            if GLOBAL_OPTIONS[token]:
                if i + 1 >= len(argv):
                    raise ValueError(f"Missing value for {token}")
                prefix.append(argv[i + 1])
                i += 2
            else:
                i += 1
            continue

        if command_seen:
            suffix.append(token)
        else:
            prefix.append(token)
        i += 1

    return prefix + suffix


def main() -> int:
    parser = _build_parser()
    raw_argv = sys.argv[1:]
    try:
        argv = _normalize_argv(raw_argv)
    except ValueError as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "status_code": -1,
                    "message": str(exc),
                    "error": None,
                    "response_payload": {},
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1
    args = parser.parse_args(argv)
    if args.command != "auth-status":
        _load_env_file(args.env_file)

    try:
        result = args.func(args)
    except Exception as exc:  # noqa: BLE001
        result = {
            "ok": False,
            "status_code": -1,
            "message": str(exc),
            "error": None,
            "response_payload": {},
        }

    result = _truncate_description_fields(result, args.max_description_chars)
    result = _apply_pick_fields(result, args.pick_fields)

    if args.compact:
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    if result.get("ok") is False:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
