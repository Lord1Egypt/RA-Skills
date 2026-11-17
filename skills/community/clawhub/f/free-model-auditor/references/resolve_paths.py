#!/usr/bin/env python3
"""Resolve WorkBuddy's two key paths for the free-model-auditor skill.

This makes the skill portable to ANY user, regardless of whether they redirected
WORKBUDDY_CONFIG_DIR / CODEBUDDY_CONFIG_DIR. It consults env vars, then falls back
to the default ~/.workbuddy location. Emits a JSON the agent can parse, plus hints
on stderr.

Two paths are resolved:
  1. CONFIG_ROOT    - where models.json lives (the custom model registry)
       precedence: $WORKBUDDY_CONFIG_DIR (dir exists)
                   -> $CODEBUDDY_CONFIG_DIR (dir exists)
                   -> ~/.workbuddy
  2. WORKSPACE_ROOT - where the audit report + daily log are written
       precedence: --workspace arg -> current working directory (agent cwd)
"""
import argparse
import json
import os
import sys

DEFAULT_HOME = os.path.expanduser("~/.workbuddy")


def resolve_config_root():
    """Return (path, source_label) for the config/data root."""
    for env in ("WORKBUDDY_CONFIG_DIR", "CODEBUDDY_CONFIG_DIR"):
        v = os.environ.get(env, "")
        if v and os.path.isdir(v):
            return os.path.normpath(v), env
    return os.path.normpath(DEFAULT_HOME), "DEFAULT(~/.workbuddy)"


def resolve_workspace_root(override=None):
    """Return (path, source_label) for the workspace/output root."""
    if override:
        return os.path.normpath(override), "--workspace"
    return os.path.normpath(os.getcwd()), "cwd(agent workspace)"


def main():
    ap = argparse.ArgumentParser(
        description="Resolve WorkBuddy config + workspace paths for free-model-auditor")
    ap.add_argument("--workspace", default=None,
                    help="Override workspace root (else use agent cwd)")
    args = ap.parse_args()

    cr, cr_src = resolve_config_root()
    wr, wr_src = resolve_workspace_root(args.workspace)
    models = os.path.join(cr, "models.json")
    mem = os.path.join(wr, ".workbuddy", "memory")

    info = {
        "config_root": cr,
        "config_root_source": cr_src,
        "models_json": models,
        "models_json_exists": os.path.isfile(models),
        "workspace_root": wr,
        "workspace_root_source": wr_src,
        "memory_dir": mem,
        "memory_dir_exists": os.path.isdir(mem),
    }
    print(json.dumps(info, ensure_ascii=False, indent=2))

    notes = []
    if not info["models_json_exists"]:
        notes.append(
            "WARN: models.json not found at resolved config_root. "
            "Confirm WORKBUDDY_CONFIG_DIR/CODEBUDDY_CONFIG_DIR, or ask the user for the path.")
    if not info["memory_dir_exists"]:
        notes.append(
            "INFO: .workbuddy/memory not present under workspace; it will be created for the daily log.")
    if notes:
        print("\n".join(notes), file=sys.stderr)


if __name__ == "__main__":
    main()
