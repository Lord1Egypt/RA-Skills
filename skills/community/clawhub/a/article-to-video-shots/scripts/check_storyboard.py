#!/usr/bin/env python3
"""分镜脚本体检

用法：
    python3 check_storyboard.py 分镜.md
    python3 check_storyboard.py 分镜1.md 分镜2.md --strict
    python3 check_storyboard.py 分镜.md --json

E 级为必须修改的硬伤，W 级为建议检查的提醒。默认只有 E 级会让退出码变成 1，
加了 --strict 之后 W 级也算失败，方便接流水线。
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from storyboard_lib import check, load_avoid_words, parse, read_global  # noqa: E402


def inspect(path, speech_rate, strict):
    content = path.read_text(encoding="utf-8")
    shots = parse(content)
    style_cn, style_en = read_global(content, "全局风格前缀")
    avoid = load_avoid_words()
    errors, warnings, stats = check(shots, style_cn, style_en, speech_rate, avoid)
    if not shots:
        errors.append("E0 没有解析到任何镜头，请检查标题是否为「## 镜头 N」格式")
    failed = bool(errors) or (strict and bool(warnings))
    return {
        "file": str(path),
        "errors": errors,
        "warnings": warnings,
        "stats": stats,
        "passed": not failed,
    }


def main():
    ap = argparse.ArgumentParser(description="分镜脚本体检")
    ap.add_argument("files", nargs="+", help="一个或多个分镜 Markdown 文件")
    ap.add_argument("--speech-rate", type=float, default=4.5, help="中文口播语速，汉字每秒，默认 4.5")
    ap.add_argument("--strict", action="store_true", help="把提醒也当作失败")
    ap.add_argument("--json", action="store_true", help="输出机器可读的 JSON")
    args = ap.parse_args()

    results = []
    for f in args.files:
        path = Path(f)
        if not path.exists():
            results.append({"file": f, "errors": ["E0 文件不存在"], "warnings": [], "stats": {}, "passed": False})
            continue
        results.append(inspect(path, args.speech_rate, args.strict))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            s = r["stats"]
            print(f"文件 {Path(r['file']).name}")
            if s:
                print(f"镜头 {s['shots']} 个，总时长 {s['total']} 秒，口播语速按 {s['speech_rate']} 字每秒估算")
            print()
            if r["errors"]:
                print(f"错误 {len(r['errors'])} 项，必须修改")
                for e in r["errors"]:
                    print(f"  {e}")
            else:
                print("错误 0 项")
            print()
            if r["warnings"]:
                print(f"提醒 {len(r['warnings'])} 项，建议看看")
                for w in r["warnings"]:
                    print(f"  {w}")
            else:
                print("提醒 0 项")
            print()

    failed = [r for r in results if not r["passed"]]
    if failed:
        print(f"{len(failed)}/{len(results)} 个文件未通过")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
