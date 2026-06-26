#!/usr/bin/env python3
"""生成题库：提取资料供对话框模型出题，或将已生成 JSON 导出为 Excel。

Agent 出题流程见 ../generation-guide.md。
禁止在此脚本中调用 app/services/ai_generator.py 本地模板出题。
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from _quizai_root import quizai_root

ROOT = quizai_root()
SCRIPTS = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser(
        description="提取资料（供对话框模型出题）或导出 JSON 题库"
    )
    parser.add_argument("inputs", nargs="+", help="资料文件路径")
    parser.add_argument("-o", "--output", required=True, help="输出 .xlsx 路径")
    parser.add_argument(
        "--json",
        help="对话框模型已生成的题库 JSON；提供则直接导出，跳过提取",
    )
    parser.add_argument(
        "--extract-out",
        default="data/material-extract.txt",
        help="资料文本输出路径（默认 data/material-extract.txt）",
    )
    args = parser.parse_args()

    json_path = args.json
    if json_path:
        export_script = SCRIPTS / "export_question_bank.py"
        cmd = [
            sys.executable,
            str(export_script),
            json_path,
            "-o",
            args.output,
        ]
        return subprocess.call(cmd)

    extract_script = SCRIPTS / "extract_material.py"
    extract_out = Path(args.extract_out)
    if not extract_out.is_absolute():
        extract_out = ROOT / extract_out

    cmd = [sys.executable, str(extract_script), *args.inputs, "-o", str(extract_out)]
    code = subprocess.call(cmd)
    if code != 0:
        return code

    print()
    print("=== 下一步（对话框模型出题）===")
    print(f"1. 阅读资料文本: {extract_out}")
    print("2. 按 generation-guide.md 规范，在对话中生成题库 JSON")
    print(f"3. 保存 JSON 后执行:")
    print(
        f'   python {SCRIPTS / "export_question_bank.py"} '
        f'"data/generated-bank.json" -o "{args.output}"'
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
