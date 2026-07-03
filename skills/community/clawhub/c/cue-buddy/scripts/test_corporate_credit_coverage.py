#!/usr/bin/env python3
"""Corporate-credit template ↔ capabilities API coverage probe.

Real-buddy validation per docs/tool_capabilities_api_2026_05_20.md §9 +
references/examples/corporate-credit.md.

The buddy author flow (`+author`) needs to translate template
``search_plan`` dimensions (e.g. ``[[主体核验]] 公开身份信息`` covered by
工商登记 / 上市公司公告 / SEC 文件 / 纳税信用) into supported supervisor
categories so it can warn when a required evidence source has no tool
support. This script exercises that mapping by:

1. Spinning the backend capabilities route in-process (same hermetic
   pattern as test_capabilities_client.py).
2. For each dimension declared in corporate-credit.md ``search_plan``,
   querying the API with key terms drawn from the 数据路由 list.
3. Printing the resulting category set so we can eyeball: is every
   dimension actually backed by ≥1 supervisor category?

Output is human-readable — this is a probe, not an assertion suite. The
single hard check is that the bare-no-filter call works (sanity).
"""

from __future__ import annotations

import os
import socket
import sys
import threading
import time
import urllib.request
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

# Resolve the backend repo path from CUE_BACKEND_DIR (set it to your local
# backend checkout). Only runs where the backend is present; CI/others skip.
_backend_env = os.environ.get("CUE_BACKEND_DIR")
_BACKEND_DIR = Path(_backend_env) if _backend_env else None
if not _BACKEND_DIR or not _BACKEND_DIR.exists():
    print("[skip] backend repo not found — set CUE_BACKEND_DIR to run this test", file=sys.stderr)
    sys.exit(0)
sys.path.insert(0, str(_BACKEND_DIR))


# Coverage map: dimension → list of probe terms drawn from the template's
# 数据路由 / 执行动作 lines. Mix Chinese + bilingual to cover q matching.
COVERAGE = {
    "主体核验 / 公开身份信息": [
        "工商",
        "公告",
        "披露易",
        "SEC",
        "纳税",
    ],
    "财务实证 / 三年财务与审计意见": [
        "财报",
        "营收",
        "评级",
        "现金流",
        "负债率",
    ],
    "行业景气 / 监管与行业风向": [
        "证监会",
        "金融监管总局",  # 2023 改组后新名 (issue #39 Gap 1)
        "银保监会",       # 旧名保留,看 catalog 是否仍命中
        "行业协会",       # 已知 gap (issue #39 Gap 2)
        "OFAC",
        "制裁",
        "研报",
    ],
    "经营动态 / 司法 / 舆情 / 合规": [
        "司法",
        "舆情",
        "处罚",
        "诉讼",
        "新闻",
    ],
}


def _start_minimal_backend() -> str:
    """Boot a fresh FastAPI on a free port, mount only tools router."""
    try:
        import uvicorn
        from fastapi import FastAPI
    except ImportError as e:
        # codex r2 finding: 默认 exit 2 = "未验证",防 CI false-pass。
        # Dev box 跳过显式 CUE_SKILL_TEST_SKIP_OK=1。
        if os.environ.get("CUE_SKILL_TEST_SKIP_OK") == "1":
            print(
                f"[skip-ok] uvicorn + fastapi missing ({e}) — "
                f"CUE_SKILL_TEST_SKIP_OK=1 set, exiting 0",
                file=sys.stderr,
            )
            sys.exit(0)
        print(
            f"[NOT VERIFIED] coverage probe not exercised — "
            f"uvicorn + fastapi missing ({e}).\n"
            f"       install: pip install uvicorn fastapi (or run in the backend .venv)\n"
            f"       to silence in non-CI dev env: export CUE_SKILL_TEST_SKIP_OK=1",
            file=sys.stderr,
        )
        sys.exit(2)

    from src.api.routes.tools import router as tools_router  # noqa: E402

    app = FastAPI()
    app.include_router(tools_router)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    server = uvicorn.Server(
        uvicorn.Config(
            app, host="127.0.0.1", port=port, log_level="error", access_log=False
        )
    )
    threading.Thread(target=server.run, daemon=True).start()
    base = f"http://127.0.0.1:{port}"
    deadline = time.time() + 5
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"{base}/openapi.json", timeout=1).read()
            return base
        except Exception:
            time.sleep(0.1)
    raise RuntimeError("backend did not start")


def main() -> int:
    base = _start_minimal_backend()
    # cue_api.DEFAULT_BASE 形态是 https://cuecue.cn/api(末尾带 /api),所以 path
    # 内只写 /tools/capabilities;本地 minimal app 没自动 /api 前缀,补一下让 URL
    # 拼对应到 router 注册的 /api/tools/capabilities。
    os.environ["CUE_API_BASE"] = base + "/api"
    os.environ["CUE_API_KEY"] = "sk-test"
    from cue_api import capabilities  # noqa: E402

    summary = capabilities()
    if summary is None or not isinstance(summary, dict):
        print(f"[FAIL] bare GET returned {summary!r}")
        return 2
    catalog_size = summary["source_counts"]["catalog_tools"]
    total_categories = summary["counts"]["categories"]
    print(
        f"\n=== capabilities surface: {catalog_size} tools / "
        f"{total_categories} categories ===\n"
    )

    overall_categories_seen: set[str] = set()
    overall_uncovered_terms: list[tuple[str, str]] = []

    for dim, terms in COVERAGE.items():
        print(f"## {dim}")
        dim_categories: set[str] = set()
        for term in terms:
            payload = capabilities(q=term)
            cats = sorted({t["category"] for t in payload["tools"]})
            tool_count = payload["counts"]["returned_tools"]
            if cats:
                dim_categories.update(cats)
                print(f"  q={term!r:14}  →  {tool_count:3d} tools / {len(cats)} cats: {cats}")
            else:
                print(f"  q={term!r:14}  →  0 tools  ← ⚠️  no coverage")
                overall_uncovered_terms.append((dim, term))
        overall_categories_seen.update(dim_categories)
        print(f"  ───── dimension summary: {len(dim_categories)} cats reached: {sorted(dim_categories)}\n")

    print("=" * 60)
    print(f"overall coverage:  {len(overall_categories_seen)} / {total_categories} categories reached")
    print(f"reached: {sorted(overall_categories_seen)}")
    print()
    if overall_uncovered_terms:
        print(f"uncovered probe terms ({len(overall_uncovered_terms)}):")
        for dim, term in overall_uncovered_terms:
            print(f"  - {dim!r:50}  term {term!r}")
        print()
        print("These represent template-declared data sources with NO matching")
        print("supervisor category at q= substring level. Either:")
        print("  (a) the API/catalog truly lacks this capability (real gap)")
        print("  (b) the term wording doesn't match any trigger/display_name")
        print("      (try wider synonyms / category= filter)")
    else:
        print("✓ every probe term has ≥1 backing category — corporate-credit")
        print("  template fully supported by current researcher surface.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
