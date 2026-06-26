#!/usr/bin/env python3
"""Plan and optionally execute real sub-model training commands for ELPA."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(payload: Dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def _build_context(cfg: Dict[str, Any], run_dir: Path, model_dir: Path, model_name: str) -> Dict[str, Any]:
    ctx: Dict[str, Any] = {}
    for k, v in cfg.items():
        if isinstance(v, (str, int, float, bool)):
            ctx[k] = v
    custom_context = cfg.get("context", {})
    if isinstance(custom_context, dict):
        for k, v in custom_context.items():
            if isinstance(v, (str, int, float, bool)):
                ctx[k] = v

    ctx["run_dir"] = str(run_dir)
    ctx["model_dir"] = str(model_dir)
    ctx["model_name"] = model_name
    ctx["dataset"] = str(cfg.get("dataset", ""))
    ctx["train_dataset"] = str(cfg.get("dataset", ""))
    ctx["val_dataset"] = str(cfg.get("val_dataset", ""))
    ctx["test_dataset"] = str(cfg.get("test_dataset", ""))
    ctx["horizon"] = int(cfg.get("horizon", 1))
    ctx["period"] = int(cfg.get("period", 24))
    ctx["seed"] = int(cfg.get("seed", 42))
    return ctx


def _render_command(template: str, context: Dict[str, Any]) -> str:
    try:
        return template.format(**context)
    except KeyError as exc:
        missing = str(exc).strip("'")
        raise ValueError(f"missing placeholder '{missing}' in context for command: {template}") from exc


def _prepare_manifest(cfg: Dict[str, Any], run_dir: Path) -> Dict[str, Any]:
    models = cfg.get("models")
    if not isinstance(models, list) or not models:
        raise ValueError("config 'models' must be a non-empty list")

    run_dir.mkdir(parents=True, exist_ok=True)
    items: List[Dict[str, Any]] = []
    for raw in models:
        if not isinstance(raw, dict):
            raise ValueError("each model config must be an object")
        name = str(raw.get("name", "")).strip()
        group = str(raw.get("group", "online")).strip().lower()
        cmd_template = str(raw.get("train_cmd", "")).strip()
        enabled = bool(raw.get("enabled", True))
        env = raw.get("env", {})
        if not name:
            raise ValueError("model 'name' is required")
        if group not in {"online", "offline"}:
            raise ValueError(f"model '{name}' has invalid group '{group}', expected online/offline")
        if not cmd_template:
            raise ValueError(f"model '{name}' missing train_cmd")
        if env and not isinstance(env, dict):
            raise ValueError(f"model '{name}' env must be object if provided")

        model_dir = run_dir / "models" / name
        model_dir.mkdir(parents=True, exist_ok=True)
        context = _build_context(cfg, run_dir=run_dir, model_dir=model_dir, model_name=name)
        command = _render_command(cmd_template, context)

        items.append(
            {
                "name": name,
                "group": group,
                "enabled": enabled,
                "train_cmd_template": cmd_template,
                "train_cmd": command,
                "model_dir": str(model_dir),
                "env": {str(k): str(v) for k, v in env.items()} if env else {},
                "status": "planned" if enabled else "disabled",
                "return_code": None,
                "stdout_log": str(model_dir / "train.stdout.log"),
                "stderr_log": str(model_dir / "train.stderr.log"),
                "started_at": None,
                "finished_at": None,
            }
        )

    return {
        "skill": "ELPA",
        "created_at": _now(),
        "run_dir": str(run_dir),
        "dataset": str(cfg.get("dataset", "")),
        "horizon": int(cfg.get("horizon", 1)),
        "period": int(cfg.get("period", 24)),
        "beta": float(cfg.get("beta", 0.7)),
        "models": items,
    }


def _execute_manifest(manifest: Dict[str, Any], continue_on_error: bool) -> None:
    for item in manifest.get("models", []):
        if not item.get("enabled", True):
            item["status"] = "disabled"
            continue

        item["status"] = "running"
        item["started_at"] = _now()
        env = os.environ.copy()
        env.update(item.get("env", {}))

        stdout_path = Path(item["stdout_log"])
        stderr_path = Path(item["stderr_log"])
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        stderr_path.parent.mkdir(parents=True, exist_ok=True)

        with stdout_path.open("w", encoding="utf-8") as out_f, stderr_path.open("w", encoding="utf-8") as err_f:
            completed = subprocess.run(
                item["train_cmd"],
                shell=True,
                cwd=item["model_dir"],
                env=env,
                stdout=out_f,
                stderr=err_f,
                check=False,
            )

        item["return_code"] = completed.returncode
        item["finished_at"] = _now()
        if completed.returncode == 0:
            item["status"] = "ok"
        else:
            item["status"] = "failed"
            if not continue_on_error:
                break


def _default_run_dir() -> Path:
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return Path(".runtime") / "elpa_runs" / stamp


def main() -> int:
    parser = argparse.ArgumentParser(description="ELPA real training orchestrator")
    parser.add_argument("--config", required=True, help="training config JSON")
    parser.add_argument("--run-dir", default="", help="output run dir (default .runtime/elpa_runs/<timestamp>)")
    parser.add_argument("--manifest-out", default="", help="manifest output path")
    parser.add_argument("--execute", action="store_true", help="actually execute training commands")
    parser.add_argument("--continue-on-error", action="store_true", help="continue when a model fails")
    args = parser.parse_args()

    cfg = _load_json(args.config)
    run_dir = Path(args.run_dir) if args.run_dir else _default_run_dir()
    manifest = _prepare_manifest(cfg, run_dir=run_dir)

    print("ELPA training plan:")
    for item in manifest["models"]:
        prefix = "[DISABLED]" if not item["enabled"] else "[PLAN]"
        print(f"{prefix} {item['name']} ({item['group']}): {item['train_cmd']}")

    if args.execute:
        _execute_manifest(manifest, continue_on_error=args.continue_on_error)
        print("\nExecution summary:")
        for item in manifest["models"]:
            status = item.get("status", "unknown")
            code = item.get("return_code")
            print(f"- {item['name']}: status={status}, return_code={code}")
    else:
        print("\nDry-run mode: no training command executed.")

    manifest_out = Path(args.manifest_out) if args.manifest_out else run_dir / "train_manifest.json"
    _save_json(manifest, manifest_out)
    print(f"Manifest written to: {manifest_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
