# -*- coding: utf-8 -*-
"""
tools/batch_invoke.py
批量调用工具 (Batch Invoker)
版本: 1.0.0

功能：读取一个 manifest(JSON)，对其中声明的多个模块按编号批量调用，
      收集统一 SkillResult 并输出/落盘，用于回归测试与联调。

用法(在项目根目录执行)：
  python tools/batch_invoke.py --manifest tests/manifest.json --out results.json
  python tools/batch_invoke.py --module m01 --params '{"industry_description":"x","five_forces":{...}}'

松耦合：仅通过 common.loader.load_skill 取用模块公开接口。
"""
import os
import sys
import json
import argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from common.loader import load_skill  # noqa: E402


def run_one(module_id: str, params: dict) -> dict:
    entry = load_skill(module_id)
    res = entry["invoke"](params)
    return res.to_dict() if hasattr(res, "to_dict") else res


def main():
    ap = argparse.ArgumentParser(description="批量调用商业管理大师技能矩阵")
    ap.add_argument("--manifest", help="JSON 文件，键为模块编号，值为入参")
    ap.add_argument("--module", help="单次调用指定模块编号")
    ap.add_argument("--params", help="单次调用的入参 JSON 字符串")
    ap.add_argument("--out", help="结果输出 JSON 路径", default="")
    args = ap.parse_args()

    results = {}
    if args.manifest:
        with open(args.manifest, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        for mid, params in manifest.items():
            try:
                results[mid] = run_one(mid, params)
            except Exception as e:
                results[mid] = {"status": "error", "warning": str(e)}
    elif args.module:
        params = json.loads(args.params or "{}")
        results[args.module] = run_one(args.module, params)
    else:
        print("请提供 --manifest 或 --module")
        return

    text = json.dumps(results, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print("结果已写入 %s" % args.out)
    else:
        print(text)


if __name__ == "__main__":
    main()
