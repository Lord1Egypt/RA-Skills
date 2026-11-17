"""Hermes plugin: geo_scan — answer-engine readiness audit (no API key, stdlib).

The engine is `geo_scan.py` next to this file; the repo root IS the plugin
directory, so there is exactly one copy of the scoring code. The engine path is
fixed; there is no override and no fallback location.
"""
from __future__ import annotations

import json
import time
import urllib.parse
from pathlib import Path

__version__ = "1.2.7"

_MAX_PAGES = 25
_DEFAULT_PAGES = 8
_BUDGET_SECONDS = 90  # the scan runs synchronously inside an agent turn


def _confined_out_dir(raw: str | None) -> Path:
    """Resolve out_dir and keep it inside ~/.hermes/cache or the working directory.

    The tool's contract is 'writes two report files under out_dir'. The caller picks
    out_dir; this keeps that pick inside the two places an agent session legitimately
    writes to, so a prompt-injected out_dir cannot drop a file into ~/.ssh or onto a
    git-tracked tree the user never named.
    """
    cwd = Path.cwd().resolve()
    cache = (Path.home() / ".hermes" / "cache").resolve()
    default = cache / "scratch" / "geo-scan"
    if not raw:
        return default
    if ".." in Path(raw).parts:
        raise ValueError(f"out_dir must not contain '..': {raw}")
    target = Path(raw).expanduser()
    if target.is_symlink():
        raise ValueError(f"out_dir must not be a symlink: {raw}")
    target = target.resolve()
    for root in (cwd, cache):
        if target == root or root in target.parents:
            return target
    raise ValueError(f"out_dir must be under {cache} or the working directory ({cwd})")


def _load_engine():
    """Import the engine as a plain submodule of this plugin package.

    A static relative import — no file-path spec, no exec_module, no fallback
    locations — so nothing outside the installed plugin package can be executed.
    Hermes loads this directory as a package (it sets __path__ to the plugin
    dir), which is what makes `from . import geo_scan` resolve.
    """
    from . import geo_scan  # noqa: PLC0415 - the engine is this package's submodule
    return geo_scan


def _normalise(url: str) -> str:
    url = (url or "").strip()
    if not url:
        raise ValueError("url is required")
    return url if "://" in url else "https://" + url


def _handle_geo_scan(params: dict) -> str:
    try:
        engine = _load_engine()
    except Exception as e:  # noqa: BLE001
        return json.dumps({"ok": False, "error": f"engine load failed: {e}"})

    try:
        root = _normalise(params.get("url", ""))
    except ValueError as e:
        return json.dumps({"ok": False, "error": str(e)})

    try:
        pages = int(params.get("pages", _DEFAULT_PAGES))
    except (TypeError, ValueError):
        pages = _DEFAULT_PAGES
    pages = max(1, min(_MAX_PAGES, pages))

    try:
        # public_only=True and never anything else: every address is validated at
        # connect time and the validated address is what the socket dials, so a
        # prompt-injected agent cannot use this tool to probe the LAN — not by
        # literal IP, not by a host that rebinds to one, not through a proxy.
        findings = engine.scan(root, max_pages=pages, budget=_BUDGET_SECONDS, public_only=True)
    except Exception as e:  # noqa: BLE001
        return json.dumps({"ok": False, "error": f"scan failed for {root}: {e}",
                           "hint": "site unreachable, blocked, private address, or not a URL"})

    result = {
        "ok": True,
        "tool": "geo_scan",
        "version": findings.get("version"),
        "root": findings.get("root", root),
        "score": findings.get("score"),
        "grade": findings.get("grade"),
        "axes": [
            {"id": c["id"], "name": c["name"], "score": c["score"], "max": c["max"],
             "status": c["status"], "evidence": c["evidence"]}
            for c in findings.get("checks", [])
        ],
        "actions": [{"priority": p, "action": a} for p, a in findings.get("actions", [])],
        "pages_sampled": len(findings.get("pages", [])),
        "pages": [
            {"url": p.get("url"), "words": p.get("words"), "h1": p.get("h1"),
             "schema": p.get("schema_types"), "figures": p.get("stat_hits"),
             "quotable": p.get("quotable_hits")}
            for p in findings.get("pages", [])[:12]
        ],
        "signals": findings.get("signals", {}),
        "notes": findings.get("notes", [])[:10],
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }

    if params.get("save"):
        try:
            out_dir = _confined_out_dir(params.get("out_dir"))
            out_dir.mkdir(parents=True, exist_ok=True)
            slug = urllib.parse.urlparse(root).netloc.replace("www.", "_")
            stamp = time.strftime("%Y%m%d-%H%M")
            md_path = out_dir / f"geo-scan-{slug}-{stamp}.md"
            json_path = out_dir / f"geo-scan-{slug}-{stamp}.json"
            md_path.write_text(engine.to_md(findings), encoding="utf-8")
            slim = {k: v for k, v in findings.items() if k != "pages"}
            slim["pages"] = [{k: v for k, v in p.items() if k != "title"}
                             for p in findings.get("pages", [])]
            json_path.write_text(json.dumps(slim, indent=1), encoding="utf-8")
            result["report_md"] = str(md_path)
            result["report_json"] = str(json_path)
        except Exception as e:  # noqa: BLE001
            result["save_error"] = str(e)

    return json.dumps(result, ensure_ascii=False)


def register(ctx):
    description = (
        "Audit a public website's answer-engine readiness (ChatGPT search / Perplexity / "
        "Claude / Gemini / AI Overviews): 0-100 across crawler access for search agents, "
        "machine readability, snippet permissions, structure, quotability and freshness, "
        "each with its evidence, plus a prioritised fix list. No API key. Scanning is "
        "read-only: robots.txt-obedient HTTP(S) GETs at one per second or the site's "
        "Crawl-delay, max 90 s, public hosts only; ftp:, file: and every other scheme are "
        "refused before a socket opens. When save=true the tool additionally writes two "
        "report files (Markdown + JSON) into out_dir, which must sit under "
        "~/.hermes/cache or the working directory (default ~/.hermes/cache/scratch/geo-scan)."
    )
    ctx.register_tool(
        name="geo_scan",
        toolset="geo_scan",
        description=description,
        # the registry shows the model {**schema, "name": name}: name/description/parameters
        schema={
            "name": "geo_scan",
            "description": description,
            "parameters": {
                "type": "object",
                "required": ["url"],
                "properties": {
                    "url": {"type": "string",
                            "description": "Site or page to audit (https://example.com)"},
                    "pages": {"type": "integer",
                              "description": f"Pages to sample, 1-{_MAX_PAGES} (default {_DEFAULT_PAGES})"},
                    "save": {"type": "boolean",
                             "description": "Also write the full Markdown + JSON report to disk"},
                    "out_dir": {"type": "string",
                                "description": "Directory for saved reports (default: scratch/geo-scan)"},
                },
            },
        },
        handler=_handle_geo_scan,
    )
