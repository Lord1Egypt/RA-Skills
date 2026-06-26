#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Runtime entry for the clawfeedradar skill.

This script is a thin, auditable wrapper around the upstream
`clawfeedradar` Python package and its CLI (`clawfeedradar.cli`). It is
invoked by the ClawHub skill runtime with a JSON payload on stdin and
returns a JSON response on stdout.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import sysconfig
from pathlib import Path
from typing import Any, Dict


def _workspace_root() -> Path:
  return Path(__file__).resolve().parent.parent


def _site_packages(prefix: Path) -> Path:
  vars_map = {"base": str(prefix), "platbase": str(prefix)}
  return Path(sysconfig.get_path("purelib", vars=vars_map))


def _build_env() -> dict[str, str]:
  env = os.environ.copy()
  prefix = _workspace_root() / "skills" / "clawfeedradar" / ".venv"
  site_packages = _site_packages(prefix)
  if site_packages.exists():
    pythonpath = env.get("PYTHONPATH", "")
    paths = [p for p in pythonpath.split(os.pathsep) if p] if pythonpath else []
    if str(site_packages) not in paths:
      paths.insert(0, str(site_packages))
      env["PYTHONPATH"] = os.pathsep.join(paths)
  return env


def _extract_next_lines(stdout: str, stderr: str) -> list[str]:
  lines = (stderr or "").splitlines() + (stdout or "").splitlines()
  next_lines: list[str] = []
  capture = False
  for line in lines:
    if line.startswith("NEXT:"):
      capture = True
      content = line[len("NEXT:") :].strip()
      if content:
        next_lines.append(content)
      continue
    if capture:
      if not line.strip():
        capture = False
        continue
      if line.startswith(("ERROR:", "WARN:", "INFO:", "NEXT:")):
        capture = False
        continue
      next_lines.append(line.rstrip())
  return next_lines


def _classify_error(output_text: str) -> str:
  text = output_text.lower()
  if "embedding" in text and "missing" in text:
    return "missing_embedding"
  if "scrape" in text and "failed" in text:
    return "scrape_failed"
  if "git" in text and "publish" in text:
    return "git_publish_failed"
  if "permission denied" in text or "read-only file system" in text:
    return "permission"
  return "other"


def _run_cli(args: list[str]) -> Dict[str, Any]:
  cmd = [sys.executable, "-m", "clawfeedradar.cli"] + args
  proc = subprocess.run(
    cmd,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env=_build_env(),
  )
  output_text = f"{proc.stderr}\n{proc.stdout}"
  next_lines = _extract_next_lines(proc.stdout, proc.stderr)
  if proc.returncode != 0:
    error_kind = _classify_error(output_text)
    result: Dict[str, Any] = {
      "ok": False,
      "error": "clawfeedradar_cli_failed",
      "error_kind": error_kind,
      "exit_code": proc.returncode,
      "stdout": proc.stdout,
      "stderr": proc.stderr,
    }
    if next_lines:
      result["next"] = next_lines
    return result

  try:
    data = json.loads(proc.stdout)
  except Exception:
    data = {"raw": proc.stdout}
  result = {"ok": True, "data": data}
  if next_lines:
    result["next"] = next_lines
  return result


def handle_run_once(payload: Dict[str, Any]) -> Dict[str, Any]:
  source_url = payload["source_url"]
  max_source_items = payload.get("max_source_items")
  max_items = payload.get("max_items")
  score_threshold = payload.get("score_threshold")
  source_lang = payload.get("source_lang")
  target_lang = payload.get("target_lang")
  enable_preview = payload.get("enable_preview", True)
  preview_words = payload.get("preview_words")
  root = payload.get("root")

  args: list[str] = ["run", "--url", source_url, "--json"]
  if max_source_items is not None:
    args += ["--max-source-items", str(max_source_items)]
  if max_items is not None:
    args += ["--max-items", str(max_items)]
  if score_threshold is not None:
    args += ["--score-threshold", str(score_threshold)]
  if source_lang:
    args += ["--source-lang", source_lang]
  if target_lang:
    args += ["--target-lang", target_lang]
  if not enable_preview:
    args.append("--no-preview")
  if preview_words is not None:
    args += ["--preview-words", str(preview_words)]
  if root:
    args += ["--root", root]

  return _run_cli(args)


def handle_schedule_from_sources_json(payload: Dict[str, Any]) -> Dict[str, Any]:
  sources_file = payload["sources_file"]
  root = payload.get("root")

  args: list[str] = [
    "schedule-from-sources-json",
    "--sources",
    sources_file,
    "--json",
  ]
  if root:
    args += ["--root", root]

  return _run_cli(args)


def main() -> None:
  try:
    payload = json.load(sys.stdin)
  except Exception as e:
    json.dump({"ok": False, "error": f"invalid_json:{e}"}, sys.stdout)
    return

  action = payload.get("action")
  if action == "run_once":
    result = handle_run_once(payload)
  elif action == "schedule_from_sources_json":
    result = handle_schedule_from_sources_json(payload)
  else:
    result = {
      "ok": False,
      "error": f"unknown_action:{action}",
      "available_actions": ["run_once", "schedule_from_sources_json"],
    }

  json.dump(result, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
  main()
