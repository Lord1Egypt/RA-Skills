#!/usr/bin/env python3
"""Verify a generated project against the DSL analysis that produced it.

Turns the skill's quality red-lines from self-discipline into checks:

1. structure    app/workflow/{context,runner,definition}.py + blocks/ exist
2. coverage     every analysis node id appears exactly once in DEFINITION
3. references   every {{#node.var#}} in node configs points at a defined node
4. env          .env.example covers every env/secret the DSL needs
5. compile      python -m compileall on the project app/
6. handlers     build_handlers() registers every non-engine node

Usage:
    python verify_project.py --analysis analysis.json --project <project_dir>

Exit code 0 when all checks pass, 1 otherwise. Needs pyyaml only for
reading the analysis JSON's companions; analysis itself is JSON.
"""

import argparse
import ast
import importlib.util
import json
import os
import re
import sys

VAR_RE = re.compile(r"\{\{\s*#([^#]+)#\s*\}\}")
# node types executed natively by the template engine (no handler needed)
ENGINE_TYPES = {"start", "iteration-start", "loop-start", "end", "answer",
                "if-else", "question-classifier", "iteration", "loop"}


def load_definition(project_dir):
    """Import DEFINITION + build_handlers as a package import (relative
    imports inside definition.py need the package context). Imports only
    app.workflow.definition — app.main (fastapi) is never touched."""
    wf_dir = os.path.join(project_dir, "app", "workflow")
    for fname in ("context.py", "runner.py", "definition.py"):
        if not os.path.isfile(os.path.join(wf_dir, fname)):
            return None, None, f"missing app/workflow/{fname}"
    sys.path.insert(0, project_dir)
    try:
        for mod_name in list(sys.modules):
            if mod_name == "app" or mod_name.startswith("app."):
                del sys.modules[mod_name]  # avoid stale cache between runs
        mod = importlib.import_module("app.workflow.definition")
        return mod.DEFINITION, mod.build_handlers(), None
    except Exception as e:  # noqa: BLE001
        return None, None, f"import definition.py failed: {type(e).__name__}: {e}"
    finally:
        sys.path.pop(0)


def walk_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from walk_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_strings(v)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--analysis", required=True)
    ap.add_argument("--project", required=True)
    args = ap.parse_args()

    with open(args.analysis, encoding="utf-8") as f:
        analysis = json.load(f)

    results = []  # (check, ok, detail)

    # 1. structure
    blocks_dir = os.path.join(args.project, "app", "workflow", "blocks")
    has_blocks = os.path.isdir(blocks_dir) and any(
        fn.endswith(".py") and fn != "__init__.py"
        for fn in os.listdir(blocks_dir))
    results.append(("structure", has_blocks,
                    "blocks/ has at least one handler module" if has_blocks
                    else "app/workflow/blocks/ missing or empty"))

    # 2/6 need definition import
    definition, handlers, err = load_definition(args.project)

    # 2. coverage (static parse of analysis vs definition)
    if err:
        results.append(("coverage", False, err))
        results.append(("references", False, "skipped: definition unavailable"))
        results.append(("handlers", False, "skipped: definition unavailable"))
    else:
        dsl_ids = [n["id"] for n in analysis["nodes"]]
        def_ids = list(definition["nodes"].keys())
        missing = [i for i in dsl_ids if i not in def_ids]
        extra_dupes = len(def_ids) != len(set(def_ids))
        results.append(("coverage", not missing and not extra_dupes,
                        f"{len(def_ids)}/{len(dsl_ids)} DSL nodes defined"
                        + (f"; MISSING: {missing}" if missing else "")))

        # 3. references: every {{#node.var#}} in analysis configs resolves
        # to a node that exists in the definition
        bad_refs = set()
        for s in walk_strings([n.get("config", {}) for n in analysis["nodes"]]):
            for m in VAR_RE.finditer(s):
                ref = m.group(1).strip()
                if ref.startswith(("env.", "secret.")) or ref == "context":
                    continue
                if "." in ref:
                    nid = ref.split(".", 1)[0]
                    if nid != "sys" and nid not in definition["nodes"]:
                        bad_refs.add(ref)
        results.append(("references", not bad_refs,
                        "all variable refs resolve" if not bad_refs
                        else f"refs to undefined nodes: {sorted(bad_refs)}"))

        # 6. handlers: every non-engine node (incl. iteration children) has one
        need_handler = [nid for nid, n in definition["nodes"].items()
                        if n["type"] not in ENGINE_TYPES]
        unhandled = [nid for nid in need_handler if nid not in handlers]
        results.append(("handlers", not unhandled,
                        f"{len(need_handler)} handlers registered"
                        + (f"; MISSING: {unhandled}" if unhandled else "")))

    # 4. env coverage
    env_example = os.path.join(args.project, ".env.example")
    needed = set()
    for v in analysis["external_requirements"].get("environment_variables", []):
        needed.add(v["name"])
    for ref in analysis["external_requirements"].get("secret_variable_refs", []):
        m = re.match(r"\{\{\s*#(?:env|secret)\.([^#]+)#\s*\}\}", ref)
        if m:
            needed.add(m.group(1).strip())
    if os.path.isfile(env_example):
        with open(env_example, encoding="utf-8") as f:
            present = set(re.findall(r"^\s*#?\s*([A-Z0-9_]+)\s*=", f.read(),
                                     re.MULTILINE))
        missing_env = sorted(needed - present)
        results.append(("env", not missing_env,
                        f"{len(needed)} vars covered" if not missing_env
                        else f"missing in .env.example: {missing_env}"))
    else:
        results.append(("env", not needed,
                        ".env.example missing" if needed else "no env vars needed"))

    # 5. compile
    import compileall
    app_dir = os.path.join(args.project, "app")
    ok = compileall.compile_dir(app_dir, quiet=2) if os.path.isdir(app_dir) else False
    results.append(("compile", bool(ok), "compileall app/ passed" if ok
                    else "compile errors under app/"))

    # report
    width = max(len(c) for c, _, _ in results)
    all_ok = True
    print(f"\nverify_project: {args.project}")
    for check, ok, detail in results:
        all_ok &= ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {check:<{width}}  {detail}")
    print(f"\n{'ALL CHECKS PASSED' if all_ok else 'VERIFICATION FAILED'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
