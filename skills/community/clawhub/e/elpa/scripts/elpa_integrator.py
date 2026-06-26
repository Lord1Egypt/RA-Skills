#!/usr/bin/env python3
"""Build ELPA online/offline weights from real validation errors."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List

EPS = 1e-9


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(payload: Dict[str, Any], path: str) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def _ewma(errors: List[float], beta: float) -> float:
    if not errors:
        return 1.0
    score = max(0.0, float(errors[0]))
    for e in errors[1:]:
        score = beta * score + (1.0 - beta) * max(0.0, float(e))
    return max(score, EPS)


def _read_errors_csv(path: str) -> List[float]:
    values: List[float] = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        use_abs = "abs_error" in headers
        use_pair = "y_true" in headers and "pred" in headers
        if not use_abs and not use_pair:
            raise ValueError(f"{path} must contain abs_error OR (y_true,pred)")
        for row in reader:
            if use_abs:
                raw = row.get("abs_error", "")
                if raw is None or str(raw).strip() == "":
                    continue
                values.append(abs(float(raw)))
            else:
                y_true = row.get("y_true", "")
                pred = row.get("pred", "")
                if y_true is None or pred is None or str(y_true).strip() == "" or str(pred).strip() == "":
                    continue
                values.append(abs(float(y_true) - float(pred)))
    if not values:
        raise ValueError(f"{path} contains no usable rows")
    return values


def _to_score(model: Dict[str, Any], beta: float) -> float:
    if "ewma_score" in model:
        return max(float(model["ewma_score"]), EPS)
    if "error_values" in model:
        errors = [abs(float(v)) for v in model["error_values"]]
        return _ewma(errors, beta=beta)
    if "error_csv" in model:
        return _ewma(_read_errors_csv(str(model["error_csv"])), beta=beta)
    raise ValueError(f"model '{model.get('name', '')}' needs one of ewma_score/error_values/error_csv")


def _weights_from_scores(scores: Dict[str, float]) -> Dict[str, float]:
    inv = {name: 1.0 / max(score, EPS) for name, score in scores.items()}
    total = sum(inv.values())
    if total <= 0.0:
        n = max(1, len(scores))
        return {name: 1.0 / n for name in scores}
    return {name: value / total for name, value in inv.items()}


def _best_model(scores: Dict[str, float]) -> str:
    if not scores:
        return ""
    return min(scores.items(), key=lambda x: x[1])[0]


def main() -> int:
    parser = argparse.ArgumentParser(description="ELPA integrator from validation errors")
    parser.add_argument("--config", required=True, help="integration config JSON")
    parser.add_argument("--output", required=True, help="output ELPA policy JSON")
    args = parser.parse_args()

    cfg = _load_json(args.config)
    beta = float(cfg.get("beta", 0.7))
    dirty_interval = int(cfg.get("dirty_interval", 3))
    amplitude_window = int(cfg.get("amplitude_window", 6))
    mutant_epsilon = cfg.get("mutant_epsilon")

    raw_models = cfg.get("models", [])
    if not isinstance(raw_models, list) or not raw_models:
        raise ValueError("config 'models' must be a non-empty list")

    online_scores: Dict[str, float] = {}
    offline_scores: Dict[str, float] = {}
    all_scores: Dict[str, float] = {}

    for raw in raw_models:
        if not isinstance(raw, dict):
            raise ValueError("each model config must be an object")
        name = str(raw.get("name", "")).strip()
        group = str(raw.get("group", "online")).strip().lower()
        if not name:
            raise ValueError("model name is required")
        if group not in {"online", "offline"}:
            raise ValueError(f"model '{name}' has invalid group '{group}'")
        score = _to_score(raw, beta=beta)
        all_scores[name] = score
        if group == "online":
            online_scores[name] = score
        else:
            offline_scores[name] = score

    if not online_scores:
        raise ValueError("at least one online model is required")
    if not offline_scores:
        raise ValueError("at least one offline model is required")

    online_weights = _weights_from_scores(online_scores)
    offline_weights = _weights_from_scores(offline_scores)

    payload = {
        "skill": "ELPA",
        "created_at": _now(),
        "beta": beta,
        "dirty_interval": dirty_interval,
        "amplitude_window": amplitude_window,
        "mutant_epsilon": mutant_epsilon,
        "online_models": list(online_scores.keys()),
        "offline_models": list(offline_scores.keys()),
        "scores": all_scores,
        "online_weights": online_weights,
        "offline_weights": offline_weights,
        "best_online_model": _best_model(online_scores),
        "best_offline_model": _best_model(offline_scores),
    }
    _save_json(payload, args.output)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
