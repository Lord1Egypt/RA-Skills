#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布权属证明生成器（本地 · 无网络）

为待发布包生成「权属证明五件套」证据包，证明该作品属于我们（SynomosAI / SynomosAI）：
  1. 著作权 ©
  2. 知识版权声明
  3. 免责声明（AS IS）
  4. 发布时间戳
  5. 作品指纹（包内容 SHA-256）

产出（写入包目录或指定 --out 目录）：
  - ATTESTATION.md     人类可读权属证明（可直接随包发布 / 嵌入 SKILL.md 末尾）
  - manifest.json      机器可读证据（逐文件哈希 + 包指纹 + 时间戳）

设计红线：
  - 纯本地计算，绝不发起任何网络请求、绝不上传。
  - 可信时间戳锚定（RFC3161 TSA / 区块链）为扩展点：需外部服务且须经确认，
    本工具不自动调用，仅在 ATTESTATION 中给出「如何加强」的说明。
  - 品牌署名默认「SynomosAI」，不在任何产物里写个人真名 / 在职公司 / 内部路径。
  - 指纹只哈希「已通过反逆向门」的对外文件；内部实现资产不进包，自然不进指纹。

用法：
  python publish_attest.py <包目录或 zip>
      [--name 包名] [--version 版本]
      [--author "SynomosAI"]
      [--out 输出目录] [--year 2026]
  python publish_attest.py <包目录或 zip> --verify
      # 用已有 manifest.json 校验：文件集 / 各文件哈希 / 包指纹 是否一致（篡改即报错）
"""
import argparse
import datetime
import hashlib
import json
import os
import sys
import zipfile

SKIP_NAMES = {"ATTESTATION.md", "manifest.json", ".DS_Store", "Thumbs.db"}

TEMPLATE = """# 权属证明与许可声明

> 本声明置于每个对外发布物的显著位置（SKILL.md 末尾 / 文档头部 / 包根）。
> 品牌署名统一用「{author}」，不得出现个人真名、在职公司或内部路径。

## 1. 著作权 ©
© {year} {author}. 保留所有权利。
本作品（含软件代码与文档）的著作权归 {author} 所有。

## 2. 知识版权声明
本作品所汇集的方法论、对比分析、结构化知识与合成内容（"知识内容"），
其编排与原创表达归 {author} 所有。未经书面许可，不得复制、转载、摘编、转售，
或用于训练任何模型 / 商业系统。
（软件代码依随附 LICENSE 的许可条款使用；本知识版权声明不限制 LICENSE 已授予的权利。）

## 3. 免责声明（AS IS）
本作品按「现状」提供，不提供任何明示或暗示的担保，包括但不限于适销性、
特定用途适用性及非侵权担保。使用风险由使用者自行承担，因使用本作品所致
任何直接或间接损失，作者不承担责任。

## 4. 发布时间戳
- 发布时间（UTC）：{ts_utc}
- 发布时间（本地）：{ts_local}

## 5. 作品指纹（内容哈希）
- 包指纹 SHA-256：{pkg_fp}
- 本指纹由发布包内全部文件的哈希按确定顺序合成，可作为该版本
  「于上述时间由 {author} 发布」的完整性标识。篡改任一文件即导致指纹变化。
- 加强权属：可将本指纹锚定至可信时间戳服务（RFC3161 TSA）或区块链，
  形成不可抵赖的「在先发表」证据（该步骤需外部服务，须经确认后单独执行）。

## 附：文件清单与逐文件哈希
| 文件 | SHA-256 |
|---|---|
{file_rows}
"""


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _iter_files(target: str):
    """yield (rel_path, bytes). 支持目录与 zip。"""
    if os.path.isdir(target):
        for root, _dirs, files in os.walk(target):
            for fn in files:
                if fn in SKIP_NAMES:
                    continue
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, target).replace(os.sep, "/")
                with open(full, "rb") as f:
                    yield rel, f.read()
    elif zipfile.is_zipfile(target):
        with zipfile.ZipFile(target) as z:
            for info in z.infolist():
                if info.is_dir():
                    continue
                if os.path.basename(info.filename) in SKIP_NAMES:
                    continue
                with z.open(info) as f:
                    yield info.filename, f.read()
    else:
        raise SystemExit(f"[attest] 不是目录也不是 zip: {target}")


def build_manifest(target, name, version, author, year):
    files = []
    acc = hashlib.sha256()
    for rel, data in sorted(_iter_files(target), key=lambda x: x[0]):
        fh = _sha256_bytes(data)
        files.append({"path": rel, "sha256": fh})
        acc.update(rel.encode("utf-8"))
        acc.update(b"\x00")
        acc.update(fh.encode("utf-8"))
    pkg_fp = acc.hexdigest()
    now = datetime.datetime.now(datetime.timezone.utc)
    ts_utc = now.isoformat()
    ts_local = datetime.datetime.now().isoformat()
    return {
        "schema": "ownership-attestation/1.0",
        "package": name,
        "version": version,
        "author": author,
        "year": year,
        "timestamp_utc": ts_utc,
        "timestamp_local": ts_local,
        "package_fingerprint_sha256": pkg_fp,
        "files": files,
    }


def render_md(m: dict) -> str:
    rows = "\n".join(f"| {f['path']} | {f['sha256']} |" for f in m["files"])
    return TEMPLATE.format(
        author=m["author"], year=m["year"], ts_utc=m["timestamp_utc"],
        ts_local=m["timestamp_local"], pkg_fp=m["package_fingerprint_sha256"],
        file_rows=rows,
    )


def cmd_generate(target, name, version, author, year, out):
    m = build_manifest(target, name, version, author, year)
    md = render_md(m)
    out_dir = out or (target if os.path.isdir(target) else os.path.dirname(os.path.abspath(target)))
    os.makedirs(out_dir, exist_ok=True)
    md_path = os.path.join(out_dir, "ATTESTATION.md")
    json_path = os.path.join(out_dir, "manifest.json")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    print(f"[attest] 证据包已生成：")
    print(f"  ATTESTATION.md : {md_path}")
    print(f"  manifest.json  : {json_path}")
    print(f"  包指纹 SHA-256 : {m['package_fingerprint_sha256']}")
    print(f"  文件数         : {len(m['files'])}")
    print(f"  时间戳(UTC)    : {m['timestamp_utc']}")
    return m


def cmd_verify(target, manifest_path):
    if not manifest_path or not os.path.exists(manifest_path):
        # 默认在 target 同目录找
        base = target if os.path.isdir(target) else os.path.dirname(os.path.abspath(target))
        manifest_path = os.path.join(base, "manifest.json")
    if not os.path.exists(manifest_path):
        raise SystemExit(f"[attest] 找不到 manifest.json: {manifest_path}")
    with open(manifest_path, "r", encoding="utf-8") as f:
        old = json.load(f)
    cur = build_manifest(target, old["package"], old["version"], old["author"], old["year"])
    problems = []
    if cur["package_fingerprint_sha256"] != old["package_fingerprint_sha256"]:
        problems.append("包指纹 SHA-256 不一致 → 包内容已被改动")
    if len(cur["files"]) != len(old["files"]):
        problems.append(f"文件数变化：原 {len(old['files'])} → 现 {len(cur['files'])}")
    old_map = {x["path"]: x["sha256"] for x in old["files"]}
    cur_map = {x["path"]: x["sha256"] for x in cur["files"]}
    for p in set(old_map) | set(cur_map):
        if p not in old_map:
            problems.append(f"新增文件：{p}")
        elif p not in cur_map:
            problems.append(f"缺失文件：{p}")
        elif old_map[p] != cur_map[p]:
            problems.append(f"哈希变化：{p}")
    if problems:
        print("[attest] 校验失败：")
        for p in problems:
            print("  - " + p)
        raise SystemExit(1)
    print(f"[attest] 校验通过：{len(cur['files'])} 个文件与 manifest 完全一致，指纹未变。")


def main():
    ap = argparse.ArgumentParser(description="发布权属证明生成器（本地·无网络）")
    ap.add_argument("target", help="待发布包目录或 zip")
    ap.add_argument("--name", default="未命名包", help="包名")
    ap.add_argument("--version", default="0.0.0", help="版本号")
    ap.add_argument("--author", default="SynomosAI", help="署名品牌")
    ap.add_argument("--year", default=str(datetime.datetime.now().year), help="版权年份")
    ap.add_argument("--out", default=None, help="证据包输出目录（默认包目录）")
    ap.add_argument("--verify", action="store_true", help="用已有 manifest.json 校验完整性")
    args = ap.parse_args()

    if args.verify:
        cmd_verify(args.target, args.out and os.path.join(args.out, "manifest.json"))
    else:
        cmd_generate(args.target, args.name, args.version, args.author, args.year, args.out)


if __name__ == "__main__":
    main()
