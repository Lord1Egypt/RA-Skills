#!/usr/bin/env python3
"""Native meme search tool — query local SQLite caption index, return real paths.

Wraps the agent-expression pack index so the model can call ``search_meme``
instead of shelling out to ``ls|shuf`` or hand-writing MEDIA paths.
"""

from __future__ import annotations

import importlib.util
import json
import logging
import os
import random
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


def _data_home() -> Path:
    for key in ("MEME_HOME", "AGENT_EXPRESSION_HOME", "HERMES_HOME"):
        v = os.environ.get(key, "").strip()
        if v:
            return Path(v).expanduser().resolve()
    hermes = Path("~/.hermes").expanduser()
    if (hermes / "meme-packs").is_dir():
        return hermes.resolve()
    return Path("~/.agent-expression").expanduser().resolve()


def _scripts_dir() -> Path:
    """Resolve agent-expression scripts directory.

    Order:
      1. MEME_SKILL_DIR / HERMES_MEME_SKILL_DIR /scripts
      2. $data_home/skills/media/agent-expression/scripts
      3. ~/.hermes/skills/… (compat)
      4. sibling ../scripts when this file lives in hermes-tools/
    """
    for key in ("MEME_SKILL_DIR", "HERMES_MEME_SKILL_DIR"):
        override = os.environ.get(key, "").strip()
        if override:
            return Path(override).expanduser().resolve() / "scripts"
    home = _data_home()
    candidates = [
        home / "skills" / "media" / "agent-expression" / "scripts",
        Path("~/.hermes").expanduser() / "skills" / "media" / "agent-expression" / "scripts",
        Path(__file__).resolve().parent.parent / "scripts",
    ]
    for c in candidates:
        if (c / "meme_db.py").is_file():
            return c
    return candidates[0]


def _load_meme_db():
    scripts = _scripts_dir()
    db_py = scripts / "meme_db.py"
    if not db_py.is_file():
        raise FileNotFoundError(f"meme_db.py not found: {db_py}")
    spec = importlib.util.spec_from_file_location("hermes_meme_db", db_py)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _load_meme_embed():
    scripts = _scripts_dir()
    py = scripts / "meme_embed.py"
    if not py.is_file():
        return None
    spec = importlib.util.spec_from_file_location("hermes_meme_embed", py)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def check_search_meme_requirements() -> bool:
    try:
        mdb = _load_meme_db()
        pack = mdb.default_pack_dir()
        return mdb.db_path_for_pack(pack).is_file()
    except Exception:
        return False


def search_meme_tool(
    query: str = "",
    tag: str = "",
    pick: bool = True,
    limit: int = 5,
) -> str:
    """Search local meme index; return JSON with absolute path(s) + MEDIA tag."""
    from tools.registry import tool_error, tool_result

    query = (query or "").strip()
    tag = (tag or "").strip()
    if not query and not tag:
        return tool_error("query or tag required — e.g. query='无语 摸鱼' or tag='shy'")

    try:
        mdb = _load_meme_db()
    except Exception as e:
        return tool_error(f"meme index unavailable: {e}")

    pack_dir = mdb.default_pack_dir()
    db_file = mdb.db_path_for_pack(pack_dir)
    if not db_file.is_file():
        return tool_error(
            f"index not found: {db_file}. Run index-memes.py --sync-only first."
        )

    mode = "fts"
    try:
        conn = mdb.connect(pack_dir)
        hits: list = []
        # Prefer vector search when query present and embeddings available
        if query:
            try:
                emb = _load_meme_embed()
                if emb is not None:
                    emb.ensure_embed_schema(conn)
                    st = emb.embed_stats(conn)
                    if st.get("embedded", 0) > 0:
                        hits = emb.search_vector(
                            conn,
                            query,
                            tag=tag or None,
                            limit=max(limit, 5),
                        )
                        if hits:
                            mode = "vector"
            except Exception as e:
                logger.warning("vector search failed, falling back to FTS: %s", e)
                hits = []

        if not hits:
            hits = mdb.search(conn, query, tag=tag or None, limit=max(limit, 5))
            mode = "fts" if query else "tag"
        if not hits and tag:
            hits = mdb.search(conn, "", tag=tag, limit=max(20, limit))
            if hits:
                random.shuffle(hits)
                hits = hits[:limit]
                mode = "tag"
        conn.close()
    except Exception as e:
        logger.exception("search_meme failed")
        return tool_error(f"search failed: {e}")

    if not hits:
        return tool_error(
            "no matches",
            success=False,
            hint="try shorter keywords (e.g. 无语) or a tag like shy/happy/angry",
        )

    # Verify paths still exist on disk
    valid = [h for h in hits if Path(h["path"]).is_file()]
    if not valid:
        return tool_error("matches found but files missing on disk")

    if pick:
        if mode == "vector":
            # Vector ranking is meaningful — take the best hit (no random dilute).
            chosen = valid[0]
        else:
            pool = valid[: min(3, len(valid))]
            chosen = random.choice(pool)
        path = chosen["path"]
        return tool_result(
            success=True,
            path=path,
            tag=chosen.get("tag") or "",
            caption=chosen.get("caption") or "",
            score=chosen.get("score"),
            mode=mode,
            media_tag=f"MEDIA:{path}",
            instruction=(
                "Paste media_tag as its own line in your reply. "
                "Do NOT invent paths. Do NOT use terminal ls|shuf."
            ),
        )

    results = [
        {
            "path": h["path"],
            "tag": h.get("tag") or "",
            "caption": h.get("caption") or "",
            "score": h.get("score", 0),
            "media_tag": f"MEDIA:{h['path']}",
        }
        for h in valid[:limit]
    ]
    return tool_result(
        success=True,
        mode=mode,
        results=results,
        instruction="Pick one media_tag and paste it as its own line. Do NOT invent paths.",
    )


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
from tools.registry import registry  # noqa: E402

SEARCH_MEME_SCHEMA = {
    "name": "search_meme",
    "description": (
        "Search the local meme/sticker pack by mood or scene (vector similarity on "
        "captions when available, else keyword). ALWAYS use this tool before sending "
        "a local expression meme. NEVER hand-write meme paths, NEVER use "
        "terminal ls|shuf|find to pick images. Pass natural Chinese like "
        "'得意傲娇' or '无语摸鱼'; optional tag filter (happy/shy/angry/…). "
        "Reply with the returned media_tag on its own line."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": (
                    "Mood/scene description or keywords. Natural phrases work "
                    "(e.g. 得意傲娇、害羞脸红、想下班). Prefer meaning over exact tags."
                ),
            },
            "tag": {
                "type": "string",
                "description": (
                    "Optional category filter: angry, baka, happy, shy, sigh, "
                    "meow, sad, like, confused, surprised, sleep, work, …"
                ),
            },
            "pick": {
                "type": "boolean",
                "description": "If true (default), return one random path among top hits.",
                "default": True,
            },
            "limit": {
                "type": "integer",
                "description": "Max candidates when pick=false (default 5).",
                "default": 5,
            },
        },
        "required": [],
    },
}

registry.register(
    name="search_meme",
    toolset="meme",
    schema=SEARCH_MEME_SCHEMA,
    handler=lambda args, **kw: search_meme_tool(
        query=args.get("query") or "",
        tag=args.get("tag") or "",
        pick=bool(args.get("pick", True)),
        limit=int(args.get("limit") or 5),
    ),
    check_fn=check_search_meme_requirements,
    emoji="🧧",
)
