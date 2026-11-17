#!/usr/bin/env python3
"""Native meme ingest tool — classify user images into the local pack + caption.

Uses the agent-expression scripts (classify-and-add + index caption) so the
model can call ``add_meme`` instead of shelling out. After ingest, the image
is searchable via ``search_meme``.
"""

from __future__ import annotations

import importlib.util
import logging
import os
import re
from pathlib import Path

logger = logging.getLogger(__name__)

_TAG_RE = re.compile(r"^[a-z][a-z0-9_-]{0,31}$")


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
    """Resolve agent-expression scripts directory (see search_meme_tool)."""
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


def _load_module(name: str, filename: str):
    path = _scripts_dir() / filename
    if not path.is_file():
        raise FileNotFoundError(f"{filename} not found: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _clear_proxy_env() -> None:
    for k in (
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "http_proxy",
        "https_proxy",
        "all_proxy",
    ):
        os.environ.pop(k, None)


def check_add_meme_requirements() -> bool:
    try:
        scripts = _scripts_dir()
        mdb = _load_module("ae_meme_db", "meme_db.py")
        pack = mdb.default_pack_dir()
        return (
            (scripts / "classify-and-add-meme.py").is_file()
            and (scripts / "add-meme.py").is_file()
            and pack.is_dir()
        )
    except Exception:
        return False


def _assert_safe_source(source: str) -> str:
    """Allow http(s) URLs or local files under data home / common tmp."""
    source = (source or "").strip()
    if not source:
        raise ValueError("image_path is required")
    if source.startswith(("http://", "https://")):
        return source

    path = Path(source).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f"local file not found: {path}")

    home = _data_home()
    allowed_roots = [
        home,
        Path("~/.hermes").expanduser().resolve(),
        Path("~/.agent-expression").expanduser().resolve(),
    ]
    try:
        mdb = _load_module("ae_meme_db_safe", "meme_db.py")
        allowed_roots.append(mdb.default_pack_dir().resolve())
        allowed_roots.extend(mdb.system_temp_roots())
    except Exception:
        import tempfile

        allowed_roots.append(Path(tempfile.gettempdir()).resolve())
    ok = False
    for root in allowed_roots:
        try:
            path.relative_to(root)
            ok = True
            break
        except ValueError:
            continue
    if not ok:
        raise ValueError(
            f"refusing path outside data home/tmp: {path}"
        )
    return str(path)


def _parse_add_stdout(lines: list[str]) -> dict:
    """Parse add-meme stdout like ADDED\\ttag\\t/path or EXISTS\\t/path."""
    dest = ""
    tag = ""
    status = ""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if parts[0] in {"ADDED", "CREATED_CATEGORY+ADDED", "EXISTS"}:
            status = parts[0]
            if parts[0] == "EXISTS" and len(parts) >= 2:
                dest = parts[1]
            elif len(parts) >= 3:
                tag = parts[1]
                dest = parts[2]
            elif len(parts) >= 2:
                dest = parts[-1]
    return {"status": status, "tag": tag, "path": dest}


def _vision_once(
    *,
    cl,
    data_url: str,
    catalog: list[dict[str, str]],
    vision: dict[str, str],
    force_tag: str = "",
    want_caption: bool = True,
) -> dict:
    """Single vision call: classify (+ optional caption/keywords)."""
    import json
    import re
    import urllib.error
    import urllib.request

    cat_lines = "\n".join(
        f"- {c['tag']}: {c['desc']} (n={c['count']})" for c in catalog
    ) or "(no categories yet)"

    if force_tag:
        prompt = f"""这张表情包已指定分类 tag={force_tag}。用一两句中文写检索描述。
只输出一个 JSON，不要 markdown：
{{"tag":"{force_tag}","create":false,"desc":"","reason":"forced","caption":"一句话画面+情绪","keywords":"空格分隔关键词3到8个"}}
要求：写清主体、情绪/用途；有文字就摘关键词。禁止长评构图。"""
    else:
        caption_block = ""
        if want_caption:
            caption_block = (
                ',"caption":"一句话画面+情绪","keywords":"空格分隔关键词3到8个"'
            )
        prompt = f"""你在给表情包自动打标签{"并写检索描述" if want_caption else ""}。只输出一个 JSON，不要 markdown。

已有分类（优先选用）：
{cat_lines}

规则：
1. 尽量选已有 tag；只有都不贴切才新建。
2. tag 必须匹配 ^[a-z][a-z0-9_-]{{0,31}}$
3. 新建时 create=true，并给一句中文 desc（场景说明）；选已有时 create=false，desc 可空。
4. 不要选 color / givemoney，除非画面明显是调情或讨钱。
5. 可爱卖萌偏 happy/meow/like/shy；无语 sigh；生气 angry；委屈 sad；困惑 confused。
{"6. caption 写清主体+情绪/用途；keywords 3～8 个空格分隔；有文字就摘关键词。" if want_caption else ""}

输出格式：
{{"tag":"happy","create":false,"desc":"","reason":"一句话中文理由"{caption_block}}}
"""

    body = {
        "model": vision["model"],
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": data_url}},
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        "temperature": 0.2,
    }
    url = vision["base_url"].rstrip("/") + "/chat/completions"
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {vision['api_key']}",
            "Content-Type": "application/json",
            "User-Agent": "hermes-agent-expression/add-meme-tool",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:400]
        raise RuntimeError(f"vision HTTP {e.code}: {detail}") from e

    text = (
        (((payload.get("choices") or [{}])[0].get("message") or {}).get("content"))
        or ""
    ).strip()
    if not text:
        raise RuntimeError("empty vision response")
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            raise RuntimeError(f"vision did not return JSON: {text[:300]}")
        data = json.loads(m.group(0))

    tag = str(data.get("tag") or force_tag or "").strip().lower()
    if not _TAG_RE.match(tag):
        raise RuntimeError(f"invalid tag from vision: {tag!r}")

    create = bool(data.get("create"))
    desc = str(data.get("desc") or "").strip()
    reason = str(data.get("reason") or "").strip()
    known = {c["tag"] for c in catalog}
    if force_tag:
        tag = force_tag
        create = tag not in known
        if create and not desc:
            desc = f"自定义分类 {tag}"
    elif tag not in known:
        create = True
        if not desc:
            desc = reason or f"自定义分类 {tag}"
    else:
        create = False

    return {
        "tag": tag,
        "create": create,
        "desc": desc,
        "reason": reason,
        "caption": str(data.get("caption") or "").strip(),
        "keywords": str(data.get("keywords") or "").strip(),
    }


def add_meme_tool(
    image_path: str = "",
    tag: str = "",
    dry_run: bool = False,
    caption: bool = True,
) -> str:
    """Classify (optional) + add image to meme pack; caption for search_meme."""
    from tools.registry import tool_error, tool_result

    try:
        source = _assert_safe_source(image_path)
    except Exception as e:
        return tool_error(str(e))

    force_tag = (tag or "").strip().lower()
    if force_tag and not _TAG_RE.match(force_tag):
        return tool_error(
            "tag must match [a-z][a-z0-9_-]{0,31}",
            success=False,
        )

    try:
        cl = _load_module("hermes_classify_add", "classify-and-add-meme.py")
        am = _load_module("hermes_add_meme", "add-meme.py")
        idx = _load_module("hermes_index_memes", "index-memes.py")
        mdb = _load_module("hermes_meme_db", "meme_db.py")
    except Exception as e:
        return tool_error(f"meme scripts unavailable: {e}")

    pack_dir = am.default_pack_dir()
    if not pack_dir.is_dir():
        return tool_error(f"meme pack not found: {pack_dir}")

    try:
        tmp_dir = mdb.temp_workdir()
    except Exception:
        import tempfile

        tmp_dir = Path(tempfile.gettempdir()) / "agent-expression-meme"
        tmp_dir.mkdir(parents=True, exist_ok=True)

    try:
        local = cl.source_to_local(source, tmp_dir)
    except Exception as e:
        return tool_error(f"cannot read image: {e}")

    # Build catalog for classify
    manifest = am.load_manifest(pack_dir)
    cats = manifest.get("categories") or {}
    memes_root = pack_dir / "memes"
    names = sorted(cats.keys()) if cats else (
        sorted(p.name for p in memes_root.iterdir() if p.is_dir())
        if memes_root.is_dir()
        else []
    )
    catalog = []
    for name in names:
        meta = cats.get(name, {})
        desc = meta.get("description", "") if isinstance(meta, dict) else str(meta)
        catalog.append(
            {
                "tag": name,
                "count": str(cl.list_images_fallback(pack_dir, name)),
                "desc": desc,
            }
        )

    _clear_proxy_env()

    decision = None
    vision = None
    if force_tag and (dry_run or not caption):
        decision = {
            "tag": force_tag,
            "create": not (pack_dir / "memes" / force_tag).is_dir(),
            "desc": f"自定义分类 {force_tag}",
            "reason": "user-forced tag",
            "caption": "",
            "keywords": "",
        }
    else:
        try:
            vision = cl.load_vision_config()
            data_url = cl.image_to_data_url(local)
            decision = _vision_once(
                cl=cl,
                data_url=data_url,
                catalog=catalog,
                vision=vision,
                force_tag=force_tag,
                want_caption=bool(caption) and not dry_run,
            )
        except Exception as e:
            logger.exception("add_meme vision failed")
            return tool_error(
                f"vision failed: {e}",
                hint="pass tag= explicitly, e.g. tag='happy'",
            )

    if dry_run:
        return tool_result(
            success=True,
            dry_run=True,
            tag=decision["tag"],
            create=bool(decision.get("create")),
            reason=decision.get("reason") or "",
            caption=decision.get("caption") or "",
            source=str(local),
            instruction="dry_run only — call again without dry_run to ingest",
        )

    # Capture stdout from cmd_add
    import contextlib
    import io

    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            rc = am.cmd_add(
                pack_dir,
                decision["tag"],
                str(local),
                create=bool(decision.get("create")),
                description=decision.get("desc") or "",
            )
    except Exception as e:
        return tool_error(f"add failed: {e}")

    if rc != 0:
        return tool_error(
            f"add failed (rc={rc})",
            detail=buf.getvalue()[:300],
        )

    parsed = _parse_add_stdout(buf.getvalue().splitlines())
    dest_s = parsed.get("path") or ""
    if not dest_s:
        cat = pack_dir / "memes" / decision["tag"]
        if cat.is_dir():
            imgs = sorted(
                cat.iterdir(),
                key=lambda p: p.stat().st_mtime if p.is_file() else 0,
                reverse=True,
            )
            for p in imgs:
                if p.is_file() and p.suffix.lower() in am.IMAGE_EXTS:
                    dest_s = str(p.resolve())
                    break
    if not dest_s or not Path(dest_s).is_file():
        return tool_error("added but could not resolve destination path")

    dest = Path(dest_s)
    caption_text = decision.get("caption") or ""
    keywords = decision.get("keywords") or ""

    def _index_and_embed(cap: str, kw: str) -> None:
        conn = mdb.connect(pack_dir)
        try:
            mdb.upsert_meme(
                conn,
                path=dest,
                tag=decision["tag"],
                caption=cap,
                keywords=kw,
                keep_caption=False,
            )
            try:
                emb_mod = _load_module("hermes_meme_embed", "meme_embed.py")
                emb_mod.embed_meme_row(
                    conn,
                    path=str(dest),
                    tag=decision["tag"],
                    caption=cap,
                    keywords=kw,
                )
            except Exception as ee:
                logger.warning("embed after add_meme failed: %s", ee)
            conn.commit()
        finally:
            conn.close()

    if caption and caption_text:
        try:
            _index_and_embed(caption_text, keywords)
        except Exception as e:
            logger.warning("index upsert after add_meme failed: %s", e)
    elif caption and not caption_text:
        # Rare: model omitted caption — one cheap fallback caption call
        try:
            meta = idx.vision_caption(dest, decision["tag"], vision)
            caption_text = meta["caption"]
            keywords = meta.get("keywords") or ""
            _index_and_embed(caption_text, keywords)
        except Exception as e:
            logger.warning("caption fallback failed: %s", e)

    return tool_result(
        success=True,
        status=parsed.get("status") or "ADDED",
        tag=decision["tag"],
        path=str(dest),
        caption=caption_text,
        keywords=keywords,
        reason=decision.get("reason") or "",
        media_tag=f"MEDIA:{dest}",
        instruction=(
            "Image is now in the pack and searchable via search_meme. "
            "You may paste media_tag to send it. Do NOT use terminal to add memes."
        ),
    )


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
from tools.registry import registry  # noqa: E402

ADD_MEME_SCHEMA = {
    "name": "add_meme",
    "description": (
        "Learn/ingest a user-sent image into the local meme pack: vision-classify "
        "into a tag (happy/shy/meow/…), copy into the pack, write caption so "
        "search_meme can find it later. Use when the user sends a sticker/meme "
        "and wants you to keep it, or when they say 入库/收下/学一下. "
        "image_path should be the local cache path from the inbound message "
        "(e.g. cache/images under MEME_HOME or Hermes home). Optional tag skips auto-classify. "
        "NEVER use terminal ls/cp to manage the meme pack."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "image_path": {
                "type": "string",
                "description": (
                    "Local path or http(s) URL of the image to ingest. "
                    "Prefer the cache path shown in the user message "
                    "(…/cache/images/img_….gif)."
                ),
            },
            "tag": {
                "type": "string",
                "description": (
                    "Optional forced category (happy/shy/angry/meow/…). "
                    "Omit to auto-classify with vision."
                ),
            },
            "dry_run": {
                "type": "boolean",
                "description": "If true, only classify and report tag; do not write files.",
                "default": False,
            },
            "caption": {
                "type": "boolean",
                "description": "If true (default), vision-caption after add for search_meme.",
                "default": True,
            },
        },
        "required": ["image_path"],
    },
}

registry.register(
    name="add_meme",
    toolset="meme",
    schema=ADD_MEME_SCHEMA,
    handler=lambda args, **kw: add_meme_tool(
        image_path=args.get("image_path") or "",
        tag=args.get("tag") or "",
        dry_run=bool(args.get("dry_run", False)),
        caption=bool(args.get("caption", True)),
    ),
    check_fn=check_add_meme_requirements,
    emoji="📥",
)
