#!/usr/bin/env python3
"""export_exchange.py — 运营段：语义资产交换导出（ai-data-delivery v0.0.5）

RULE-CONSUME-01 的交付面：发给甲方/其他系统时，模型、字典、gold 集要作为"一个版本化
整体"导出，带 sha256 清单——对方可验完整性，后续可对账版本漂移。

用法：
  python export_exchange.py --model semantic.yaml --out exchange/ \
      [--cases cases.json] [--dictionary dictionary.md]
产物：
  exchange/semantic.yaml        模型原样拷贝
  exchange/dictionary.md        口径字典（不给 --dictionary 则现场生成）
  exchange/cases.json           gold 用例（可选）
  exchange/manifest.json        版本/时间戳/每文件 sha256
退出码：0 成功；2 用法错误。
"""
import argparse
import datetime
import hashlib
import json
import os
import shutil
import sys

import yaml
from _contract import load

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description="语义资产交换导出")
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True, help="导出目录")
    ap.add_argument("--cases", default=None)
    ap.add_argument("--dictionary", default=None, help="不给则现场生成")
    ap.add_argument("--report", action="append", default=[], help="附带报告（必须绑定当前模型）")
    ap.add_argument("--session", help="补齐会话，必须与当前模型一致")
    ap.add_argument("--visualization", help="附带只读 HTML")
    args = ap.parse_args()

    if os.path.isdir(args.out) and os.listdir(args.out):
        ap.error("导出目录必须为空，防止混入旧版/未列入清单的文件")
    from _contract import binding_errors, load, object_digest
    for path in args.report:
        errors = binding_errors(load(path), args.model)
        if errors:
            ap.error(f"报告 {path} 失效：{errors}")
    if args.session and object_digest(load(args.session)["model"]) != object_digest(load(args.model)):
        ap.error("session 与当前模型不一致")
    os.makedirs(args.out, exist_ok=True)
    m = load(args.model)
    files = []

    dst = os.path.join(args.out, "semantic.yaml")
    shutil.copyfile(args.model, dst)
    files.append(dst)

    dic = args.dictionary
    if not dic:
        dic = os.path.join(args.out, "dictionary.md")
        import gen_dictionary
        rc = gen_dictionary.main(["--model", args.model, "--out", dic])
        if rc != 0:
            raise SystemExit(rc)
    else:
        shutil.copyfile(dic, os.path.join(args.out, "dictionary.md"))
        dic = os.path.join(args.out, "dictionary.md")
    files.append(dic)

    if args.cases:
        dst = os.path.join(args.out, "cases" + os.path.splitext(args.cases)[1])
        shutil.copyfile(args.cases, dst)
        files.append(dst)

    for index, path in enumerate(args.report):
        dst = os.path.join(args.out, f"evidence-{index + 1}.json")
        from _contract import write
        write(dst, load(path))
        files.append(dst)
    for path, name in ((args.session, "session.json"), (args.visualization, "model.html")):
        if path:
            dst = os.path.join(args.out, name)
            if name == "session.json":
                from _contract import write
                write(dst, load(path))
            else:
                shutil.copyfile(path, dst)
            files.append(dst)
    manifest = {
        "contract": "ai-data-delivery/1.0",
        "status": "exported_not_certified",
        "model_sha256": sha256(args.model),
        "limitations": ["not an Ossie/OWL adapter", "hashes prove file integrity, not business correctness", "HTML is a static view, not runtime lineage"],
        "name": m.get("name", "?"),
        "version": m.get("version", "?"),
        "exported_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "files": [{"path": os.path.basename(f), "bytes": os.path.getsize(f),
                   "sha256": sha256(f)} for f in files],
    }
    with open(os.path.join(args.out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print(f"导出完成 → {args.out}（版本 {manifest['version']}，{len(files)} 个文件）")
    for it in manifest["files"]:
        print(f"  {it['path']:20s} {it['bytes']:>8d} B  {it['sha256'][:16]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
