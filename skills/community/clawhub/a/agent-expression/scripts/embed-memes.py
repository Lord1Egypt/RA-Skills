#!/usr/bin/env python3
"""Backfill Zhipu embeddings for meme captions."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("meme_db", _SCRIPTS / "meme_db.py")
mdb = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(mdb)

_spec2 = importlib.util.spec_from_file_location("meme_embed", _SCRIPTS / "meme_embed.py")
emb = importlib.util.module_from_spec(_spec2)
assert _spec2.loader is not None
_spec2.loader.exec_module(emb)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Embed meme captions with Zhipu embedding-3")
    p.add_argument("--pack", help="Meme pack root")
    p.add_argument("--batch", type=int, default=emb.BATCH_SIZE, help="API batch size")
    p.add_argument("--limit", type=int, default=0, help="Max rows to embed (0=all)")
    p.add_argument("--stats", action="store_true", help="Print embed stats and exit")
    args = p.parse_args(argv)

    pack_dir = Path(args.pack).expanduser() if args.pack else mdb.default_pack_dir()
    conn = mdb.connect(pack_dir)
    emb.ensure_embed_schema(conn)
    cfg = emb.embed_config()

    if args.stats:
        st = emb.embed_stats(conn, model=cfg["model"])
        print(f"model={st['model']} embedded={st['embedded']}/{st['captioned']}")
        return 0

    if not cfg.get("api_key"):
        print(
            "ERROR: ZHIPU_API_KEY (or EMBEDDING_API_KEY) not set in env / .env",
            file=sys.stderr,
        )
        return 1

    todo = emb.rows_needing_embed(conn, model=cfg["model"])
    if args.limit and args.limit > 0:
        todo = todo[: args.limit]
    print(f"to_embed={len(todo)} model={cfg['model']} batch={args.batch}", flush=True)
    if not todo:
        print("Nothing to embed.", flush=True)
        return 0

    ok = fail = 0
    batch = max(1, int(args.batch))
    for i in range(0, len(todo), batch):
        chunk = todo[i : i + batch]
        texts = [r["text"] for r in chunk]
        try:
            vecs = emb.embed_texts(texts, cfg=cfg)
            for r, v in zip(chunk, vecs):
                emb.upsert_embedding(
                    conn,
                    path=r["path"],
                    vector=v,
                    model=cfg["model"],
                    text_hash_val=r["text_hash"],
                )
            conn.commit()
            ok += len(chunk)
            print(f"OK [{ok}/{len(todo)}] batch={len(chunk)}", flush=True)
        except Exception as e:
            fail += len(chunk)
            print(f"FAIL batch@{i}: {e}", flush=True)
            # try one-by-one
            for r in chunk:
                try:
                    v = emb.embed_texts([r["text"]], cfg=cfg)[0]
                    emb.upsert_embedding(
                        conn,
                        path=r["path"],
                        vector=v,
                        model=cfg["model"],
                        text_hash_val=r["text_hash"],
                    )
                    conn.commit()
                    ok += 1
                    fail -= 1
                    print(f"OK-1 [{ok}/{len(todo)}] {r['tag']}/{Path(r['path']).name}", flush=True)
                except Exception as e2:
                    print(f"FAIL-1 {r['path']}: {e2}", flush=True)

    st = emb.embed_stats(conn, model=cfg["model"])
    print(f"DONE ok={ok} fail={fail} embedded={st['embedded']}/{st['captioned']}", flush=True)
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
