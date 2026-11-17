#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trace.py — 全链路可追溯工具（时间戳 + SHA-256 哈希 + 留证）

用法：
  python trace.py stamp <文件> [--salt 加盐值] [--out stamp.json]
  python trace.py check <文件> <stamp.json>

说明：
- 对任意交付物生成留证（时间戳 + sha256 + 可选加盐 + 可选指纹注释）；
- 校验时重算哈希对比，防篡改；留证可进 07 全链路 / 26 证据墙。
"""
import argparse, hashlib, json, os, time


def file_hash(path, salt=None):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    if salt:
        h.update(salt.encode())
    return h.hexdigest()


def stamp(path, salt=None, out=None):
    ts = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    digest = file_hash(path, salt)
    rec = {
        "file": os.path.basename(path),
        "sha256": digest,
        "salt": salt or "",
        "ts": ts,
        "note": "交付物留证(时间戳+哈希)，可进 07 追溯链",
    }
    text = json.dumps(rec, ensure_ascii=False, indent=2)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[stamp] 已生成留证 -> {out}")
    else:
        print(text)
    return rec


def check(path, stamp_path):
    with open(stamp_path, encoding="utf-8") as f:
        rec = json.load(f)
    now = file_hash(path, rec.get("salt") or None)
    ok = now == rec["sha256"]
    print(json.dumps({
        "file": rec["file"], "match": ok,
        "recorded_sha256": rec["sha256"], "recomputed_sha256": now,
        "stamped_at": rec["ts"],
    }, ensure_ascii=False, indent=2))
    return ok


def main():
    ap = argparse.ArgumentParser(description="全链路可追溯工具")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("stamp"); p1.add_argument("path"); p1.add_argument("--salt"); p1.add_argument("--out")
    p2 = sub.add_parser("check"); p2.add_argument("path"); p2.add_argument("stamp")
    a = ap.parse_args()
    if a.cmd == "stamp":
        stamp(a.path, a.salt, a.out)
    else:
        check(a.path, a.stamp)


if __name__ == "__main__":
    main()
