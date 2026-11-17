#!/usr/bin/env python3
"""Sync meme pack files into SQLite and caption missing rows via vision."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import importlib.util

_SCRIPTS = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("meme_db", _SCRIPTS / "meme_db.py")
mdb = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(mdb)

_spec2 = importlib.util.spec_from_file_location("classify_add", _SCRIPTS / "classify-and-add-meme.py")
cl = importlib.util.module_from_spec(_spec2)
assert _spec2.loader is not None
_spec2.loader.exec_module(cl)

JSON_RE = re.compile(r"\{[^{}]*\}", re.DOTALL)


def _clear_proxy_env() -> None:
    for k in (
        "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
        "http_proxy", "https_proxy", "all_proxy",
    ):
        os.environ.pop(k, None)


def vision_caption(path: Path, tag: str, vision: dict[str, str]) -> dict[str, str]:
    data_url = cl.image_to_data_url(path)
    prompt = f"""用一两句中文描述这张表情包，方便以后检索。当前分类标签是 {tag}。
只输出一个 JSON，不要 markdown：
{{"caption":"一句话画面+情绪","keywords":"空格分隔的关键词3到8个"}}
要求：写清主体（角色/物体）、情绪或用途（开心/无语/嘲讽/卖萌/生气等）；有文字就摘关键词。禁止长评构图光影。"""

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
            "User-Agent": "agent-expression/index-memes",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    text = (
        (((payload.get("choices") or [{}])[0].get("message") or {}).get("content"))
        or ""
    ).strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        m = JSON_RE.search(text)
        if not m:
            raise RuntimeError(f"bad vision JSON: {text[:200]}")
        data = json.loads(m.group(0))
    caption = str(data.get("caption") or "").strip()
    keywords = str(data.get("keywords") or "").strip()
    if not caption:
        raise RuntimeError(f"empty caption: {text[:200]}")
    return {"caption": caption, "keywords": keywords}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Index meme pack into SQLite + caption via vision")
    p.add_argument("--pack", help="Meme pack root")
    p.add_argument("--sync-only", action="store_true", help="Only sync file paths, no vision")
    p.add_argument("--limit", type=int, default=0, help="Caption at most N missing images (0=all)")
    p.add_argument("--workers", type=int, default=2, help="Parallel caption workers")
    p.add_argument("--tag", default="", help="Only caption this tag")
    p.add_argument("--force", action="store_true", help="Re-caption even if caption exists")
    args = p.parse_args(argv)

    _clear_proxy_env()
    pack_dir = Path(args.pack).expanduser() if args.pack else mdb.default_pack_dir()
    if not pack_dir.is_dir():
        print(f"ERROR: pack not found: {pack_dir}", file=sys.stderr)
        return 1

    conn = mdb.connect(pack_dir)
    sync = mdb.sync_files(conn, pack_dir)
    st = mdb.stats(conn)
    print(
        f"SYNC scanned={sync['scanned']} touched≈{sync['added']} deleted={sync['deleted']} "
        f"total={st['total']} captioned={st['captioned']}",
        flush=True,
    )
    if args.sync_only:
        return 0

    vision = cl.load_vision_config()
    if not vision.get("api_key"):
        print("ERROR: no vision api key", file=sys.stderr)
        return 2

    if args.force:
        rows = list(conn.execute("SELECT path, tag, file_name FROM memes ORDER BY tag, file_name"))
    else:
        rows = mdb.needs_caption(conn)
    if args.tag:
        rows = [r for r in rows if r["tag"] == args.tag]
    if args.limit and args.limit > 0:
        rows = rows[: args.limit]

    if not rows:
        print("Nothing to caption.", flush=True)
        return 0

    print(f"CAPTIONING {len(rows)} images with workers={args.workers}…", flush=True)
    ok = fail = 0

    def work(row) -> tuple[str, dict | None, str | None]:
        path = mdb.from_store_path(pack_dir, row["path"])
        try:
            meta = vision_caption(path, row["tag"], vision)
            return str(path), meta, None
        except Exception as e:
            return str(path), None, str(e)

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futs = {ex.submit(work, r): r for r in rows}
        for i, fut in enumerate(as_completed(futs), 1):
            path_s, meta, err = fut.result()
            row = futs[fut]
            if err or not meta:
                fail += 1
                print(f"FAIL [{i}/{len(rows)}] {row['tag']}/{row['file_name']}: {err}", flush=True)
                continue
            mdb.upsert_meme(
                conn,
                path=Path(path_s),
                tag=row["tag"],
                caption=meta["caption"],
                keywords=meta["keywords"],
            )
            conn.commit()
            ok += 1
            print(
                f"OK [{i}/{len(rows)}] {row['tag']}/{row['file_name']}: {meta['caption'][:60]}",
                flush=True,
            )

    st = mdb.stats(conn)
    print(f"DONE ok={ok} fail={fail} captioned={st['captioned']}/{st['total']}", flush=True)
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
