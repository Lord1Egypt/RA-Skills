# -*- coding: utf-8 -*-
"""
tools/validate_params.py
参数校验工具 (Parameter Validator)
版本: 1.0.0

功能：依据模块契约校验入参，输出错误/警告清单，便于调用前自检。

用法(在项目根目录执行)：
  python tools/validate_params.py --module m01 --params '{"industry_description":"x","five_forces":{...}}'
  python tools/validate_params.py --module m01 --params-file params.json

松耦合：仅通过 common.loader.load_skill 取用模块契约。
"""
import os
import sys
import json
import argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from common.loader import load_skill      # noqa: E402
from common.interface import validate_params  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="校验技能模块入参")
    ap.add_argument("--module", required=True, help="模块编号")
    ap.add_argument("--params", help="入参 JSON 字符串")
    ap.add_argument("--params-file", help="入参 JSON 文件路径")
    args = ap.parse_args()

    if args.params_file:
        with open(args.params_file, "r", encoding="utf-8") as f:
            params = json.load(f)
    else:
        params = json.loads(args.params or "{}")

    entry = load_skill(args.module)
    contract = entry["contract"]
    # 复制一份避免被默认值修改影响展示
    import copy
    params_copy = copy.deepcopy(params)
    errors = validate_params(contract, params_copy)

    print("模块: %s (%s)" % (contract.module_id, contract.module_name))
    print("契约参数数: %d" % len(contract.parameters))
    if errors:
        print("校验结果: 不通过")
        for e in errors:
            print("  - %s" % e)
        return 1
    print("校验结果: 通过 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
