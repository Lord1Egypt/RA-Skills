#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify.py - 文件完整性工具：算哈希 / 校验 / 复制后校验 / 下载后校验 / 清单管理
纯 Python 标准库，无第三方依赖。Windows / macOS / Linux 通用。

用法:
  python verify.py hash <file> [--algo md5|sha1|sha256|sha512|sha3-256|blake2b] [--json]
  python verify.py verify <file> <expected> [--algo ...] [--json]
  python verify.py copy <src> <dst> [--algo ...] [--json]
  python verify.py download <url> <dst> [--algo ...] [--expected <hash>] [--json]
  python verify.py record <dir|file> [--algo ...] [-o out.md5] [--name-only] [--json]
  python verify.py check <dir|file> -c manifest.md5 [--json]

退出码: 0=成功/校验通过, 1=校验失败/文件不符, 2=参数或 IO 错误
"""

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import sys
import time
import urllib.request
import urllib.error

CHUNK = 1024 * 1024  # 1 MB 分块读取，支持大文件

ALGORITHMS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
    "sha3-256": hashlib.sha3_256,
    "blake2b": hashlib.blake2b,
}

EXIT_OK, EXIT_MISMATCH, EXIT_ERROR = 0, 1, 2


class UserError(Exception):
    """参数/IO 类错误，退出码 2。"""


def new_hasher(algo: str):
    try:
        return ALGORITHMS[algo.lower()]()
    except KeyError:
        raise UserError(
            "不支持的算法: {}（可用: {}）".format(algo, ", ".join(sorted(ALGORITHMS)))
        )


def normalize_hash(value: str) -> str:
    """接受 hex / BASE64 两种形态，统一转小写 hex。"""
    value = value.strip()
    hex_len = {32: "md5", 40: "sha1", 56: "sha3-256", 64: "sha256", 128: "sha512"}
    if len(value) in hex_len and all(c in "0123456789abcdefABCDEF" for c in value):
        return value.lower()
    try:
        raw = base64.b64decode(value, validate=True)
        if len(raw) in (16, 20, 28, 32, 64):
            return raw.hex()
    except Exception:
        pass
    # 无法识别时原样返回小写，最终由比对结果判断
    return value.lower()


def hash_file(path: str, algo: str) -> str:
    h = new_hasher(algo)
    try:
        with open(path, "rb") as f:
            while True:
                chunk = f.read(CHUNK)
                if not chunk:
                    break
                h.update(chunk)
    except OSError as e:
        raise UserError("无法读取文件 {}: {}".format(path, e))
    return h.hexdigest()


def norm_path(p: str) -> str:
    return os.path.normpath(os.path.abspath(p))


def is_within(child: str, parent: str) -> bool:
    return os.path.commonpath([child, parent]) == parent


# ---------------------------------------------------------------- 子命令实现

def cmd_hash(args) -> int:
    path = norm_path(args.path)
    if not os.path.isfile(path):
        raise UserError("文件不存在: {}".format(path))
    digest = hash_file(path, args.algo)
    if args.json:
        print(json.dumps({"file": path, "algo": args.algo, "hash": digest,
                          "size": os.path.getsize(path)}, ensure_ascii=False))
    else:
        print("{}  {}".format(digest, path))
    return EXIT_OK


def cmd_verify(args) -> int:
    path = norm_path(args.path)
    if not os.path.isfile(path):
        raise UserError("文件不存在: {}".format(path))
    expected = normalize_hash(args.expected)
    actual = hash_file(path, args.algo)
    ok = (actual == expected)
    result = {"file": path, "algo": args.algo, "expected": expected,
              "actual": actual, "match": ok}
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        if ok:
            print("[OK]   {} {}".format(args.algo.upper(), path))
        else:
            print("[FAIL] {} {}".format(args.algo.upper(), path))
            print("  期望: {}".format(expected))
            print("  实际: {}".format(actual))
    return EXIT_OK if ok else EXIT_MISMATCH


def cmd_copy(args) -> int:
    src = norm_path(args.src)
    dst = norm_path(args.dst)
    if not os.path.isfile(src):
        if os.path.isdir(src):
            raise UserError(
                "源是目录: {}（本工具按单文件复制；目录请用 record+check 校验）".format(src))
        raise UserError("源文件不存在: {}".format(src))
    if is_within(src, dst) or is_within(dst, src):
        raise UserError("源/目标路径嵌套，拒绝复制: {} -> {}".format(src, dst))
    dst_dir = os.path.dirname(dst) or "."
    os.makedirs(dst_dir, exist_ok=True)
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    # 复制内容 + 元数据（mtime 等）
    try:
        shutil.copy2(src, dst)
    except OSError as e:
        raise UserError("复制失败: {}".format(e))
    src_hash = hash_file(src, args.algo)
    dst_hash = hash_file(dst, args.algo)
    ok = (src_hash == dst_hash)
    result = {"src": src, "dst": dst, "algo": args.algo,
              "src_hash": src_hash, "dst_hash": dst_hash, "match": ok}
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        if ok:
            print("[OK]   复制完成且 {} 一致: {}".format(args.algo.upper(), dst))
        else:
            print("[FAIL] 复制后 {} 不一致!".format(args.algo.upper()))
            print("  源:   {}".format(src_hash))
            print("  目标: {}".format(dst_hash))
    if not ok and dst != src:
        # 校验失败保留现场供排查，不静默删除
        print("  提示: 已保留损坏副本供排查: {}".format(dst))
    return EXIT_OK if ok else EXIT_MISMATCH


def cmd_download(args) -> int:
    dst = norm_path(args.dst)
    dst_dir = os.path.dirname(dst) or "."
    os.makedirs(dst_dir, exist_ok=True)
    tmp = dst + ".part-{}".format(int(time.time()))
    req = urllib.request.Request(args.url, headers={"User-Agent": "verify.py/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp, open(tmp, "wb") as f:
            while True:
                chunk = resp.read(CHUNK)
                if not chunk:
                    break
                f.write(chunk)
    except (urllib.error.URLError, OSError) as e:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise UserError("下载失败 {}: {}".format(args.url, e))
    actual = hash_file(tmp, args.algo)
    if args.expected:
        expected = normalize_hash(args.expected)
        ok = (actual == expected)
        if not ok:
            # 与期望不符：保留 .part 供排查，不落到正式路径
            print(json.dumps({"url": args.url, "algo": args.algo,
                              "expected": expected, "actual": actual,
                              "match": False, "kept_as": tmp},
                             ensure_ascii=False) if args.json else
                  "[FAIL] 下载内容与期望 {} 不一致!\n  期望: {}\n  实际: {}\n"
                  "  已保留于: {}".format(args.algo.upper(), expected, actual, tmp),
                  flush=True)
            return EXIT_MISMATCH
    os.replace(tmp, dst)
    result = {"url": args.url, "dst": dst, "algo": args.algo,
              "hash": actual, "size": os.path.getsize(dst),
              "match": True if args.expected else None}
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        note = "已校验" if args.expected else "未提供期望值，仅记录哈希"
        print("[OK]   下载完成（{}）: {}".format(note, dst))
        print("  {} {}".format(args.algo, actual))
    return EXIT_OK


def collect_files(target: str):
    """返回 (根目录, [相对路径列表])。target 可为文件或目录。"""
    target = norm_path(target)
    if os.path.isfile(target):
        return os.path.dirname(target), [os.path.basename(target)]
    if not os.path.isdir(target):
        raise UserError("路径不存在: {}".format(target))
    root = target
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for name in filenames:
            files.append(os.path.relpath(os.path.join(dirpath, name), root))
    return root, sorted(files)


def parse_manifest(manifest_path: str):
    """解析 GNU/BSD 风格清单。返回 [(algo, hash, path), ...]"""
    entries = []
    with open(manifest_path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if re.match(r"^(MD5|SHA1|SHA256|SHA512)\s*\(", line):
                # BSD 风格: MD5 (file) = hash
                algo = line.split("(", 1)[0].strip().lower()
                try:
                    _, rest = line.split("(", 1)
                    path, rest = rest.split(")", 1)
                    _, digest = rest.split("=", 1)
                except ValueError:
                    raise UserError("清单第 {} 行格式错误: {}".format(lineno, line))
                entries.append((algo, normalize_hash(digest), path.strip()))
            elif ":" in line and line.split(":", 1)[0].lower() in ALGORITHMS:
                # 本工具 JSONL/前缀风格: sha256:hash  path
                algo, rest = line.split(":", 1)
                if "  " in rest or "\t" in rest:
                    digest, path = rest.split(None, 1) if "  " in rest else \
                        rest.split("\t", 1)
                else:
                    digest, path = rest.split(" ", 1)
                entries.append((algo.lower(), normalize_hash(digest), path.strip()))
            else:
                # GNU 风格: <hash> [ *| ]<path>
                parts = line.split(None, 1)
                if len(parts) != 2:
                    raise UserError("清单第 {} 行格式错误: {}".format(lineno, line))
                digest = parts[0]
                path = parts[1].lstrip("* ")
                algo = {32: "md5", 40: "sha1", 64: "sha256", 128: "sha512"}.get(
                    len(digest))
                if algo is None:
                    raise UserError("清单第 {} 行无法识别哈希长度: {}".format(
                        lineno, line))
                entries.append((algo, digest.lower(), path))
    return entries


def cmd_record(args) -> int:
    root, files = collect_files(args.path)
    if not files:
        raise UserError("没有找到任何文件: {}".format(args.path))
    out_path = norm_path(args.output) if args.output else None
    lines = []
    for rel in files:
        digest = hash_file(os.path.join(root, rel), args.algo)
        lines.append("{}: {}  {}".format(args.algo, digest, rel.replace("\\", "/")))
    if args.json:
        print(json.dumps({"root": root, "algo": args.algo,
                          "entries": [{"path": l.split("  ", 1)[1],
                                       "hash": l.split(": ", 1)[1].split("  ")[0]}
                                      for l in lines]}, ensure_ascii=False))
        return EXIT_OK
    if out_path:
        # 清单自身若在待记录树内，则从清单中剔除
        out_rel = None
        try:
            out_rel = os.path.relpath(out_path, root).replace("\\", "/")
        except ValueError:
            pass
        kept = lines
        if out_rel:
            kept = [l for l in lines if not l.endswith("  " + out_rel)]
        with open(out_path, "w", encoding="utf-8") as f:
            for l in kept:
                f.write(l + "\n")
        print("[OK]   已记录 {} 个文件 -> {}".format(len(kept), out_path))
    else:
        print("\n".join(lines))
    return EXIT_OK


def cmd_check(args) -> int:
    if not os.path.isfile(args.manifest):
        raise UserError("清单不存在: {}".format(args.manifest))
    entries = parse_manifest(args.manifest)
    root = norm_path(args.path) if args.path else os.path.dirname(
        norm_path(args.manifest))
    if os.path.isfile(root):
        root = os.path.dirname(root)
    total, ok_cnt, fail_list, miss_list = len(entries), 0, [], []
    for algo, expected, rel in entries:
        full = os.path.normpath(os.path.join(root, rel))
        if not is_within(full, root):
            fail_list.append((rel, "路径越界（清单试图跳出根目录）"))
            continue
        if not os.path.isfile(full):
            miss_list.append(rel)
            continue
        actual = hash_file(full, algo)
        if actual == expected:
            ok_cnt += 1
        else:
            fail_list.append((rel, "期望 {} 实际 {}".format(expected, actual)))
    result = {"root": root, "total": total, "ok": ok_cnt,
              "missing": miss_list, "failed": fail_list}
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print("校验清单: {}（根目录: {}）".format(args.manifest, root))
        print("结果: {}/{} 通过, {} 缺失, {} 不匹配".format(
            ok_cnt, total, len(miss_list), len(fail_list)))
        for rel in miss_list:
            print("  [MISS] {}".format(rel))
        for rel, why in fail_list:
            print("  [FAIL] {} ({})".format(rel, why))
    return EXIT_OK if (ok_cnt == total and not fail_list) else EXIT_MISMATCH


# ---------------------------------------------------------------- CLI

def build_parser():
    p = argparse.ArgumentParser(prog="verify.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_algo(sp, default="sha256"):
        sp.add_argument("--algo", default=default,
                        choices=sorted(ALGORITHMS), help="哈希算法（默认 sha256）")
        sp.add_argument("--json", action="store_true", help="JSON 输出")

    sp = sub.add_parser("hash", help="计算文件哈希")
    sp.add_argument("path")
    add_algo(sp)

    sp = sub.add_parser("verify", help="校验文件哈希是否匹配期望值")
    sp.add_argument("path")
    sp.add_argument("expected", help="期望的 hex 或 BASE64 哈希")
    add_algo(sp)

    sp = sub.add_parser("copy", help="复制文件并做复制后双向校验")
    sp.add_argument("src")
    sp.add_argument("dst")
    add_algo(sp)

    sp = sub.add_parser("download", help="下载文件并校验哈希")
    sp.add_argument("url")
    sp.add_argument("dst")
    sp.add_argument("--expected", help="期望哈希（hex/BASE64，可选）")
    add_algo(sp)

    sp = sub.add_parser("record", help="为目录/文件生成校验清单")
    sp.add_argument("path")
    sp.add_argument("-o", "--output", help="输出清单文件（默认 stdout）")
    sp.add_argument("--name-only", action="store_true",
                    help="（保留参数，清单始终含哈希）")
    add_algo(sp, default="md5")

    sp = sub.add_parser("check", help="按清单批量校验目录")
    sp.add_argument("path", nargs="?", default=None,
                     help="待校验目录（默认清单所在目录）")
    sp.add_argument("-c", "--manifest", required=True, help="校验清单文件")
    sp.add_argument("--json", action="store_true")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    handlers = {"hash": cmd_hash, "verify": cmd_verify, "copy": cmd_copy,
                "download": cmd_download, "record": cmd_record, "check": cmd_check}
    try:
        sys.exit(handlers[args.cmd](args))
    except UserError as e:
        msg = {"error": str(e)} if args.json else "[ERROR] {}".format(e)
        print(msg, file=sys.stderr, flush=True)
        sys.exit(EXIT_ERROR)
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
