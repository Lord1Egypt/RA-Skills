#!/usr/bin/env python3
import json
import sys


def main():
    if len(sys.argv) < 6:
        print("Usage: search_report.py <route> <primary> <cross_check> <reliability> <conclusion> [key points ...]", file=sys.stderr)
        sys.exit(1)

    route = sys.argv[1]
    primary = sys.argv[2]
    cross_check = sys.argv[3]
    reliability = sys.argv[4]
    conclusion = sys.argv[5]
    points = sys.argv[6:]

    result = {
        "summary": {
            "conclusion": conclusion,
            "route": route,
            "primary": primary,
            "crossCheck": cross_check,
            "reliability": reliability,
        },
        "keyPoints": points,
        "markdown": build_markdown(route, primary, cross_check, reliability, conclusion, points),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_markdown(route, primary, cross_check, reliability, conclusion, points):
    lines = []
    lines.append("## 搜索结论")
    lines.append(conclusion)
    lines.append("")
    lines.append("## 搜索路线")
    lines.append(f"- 路由：{route}")
    lines.append(f"- 主搜索入口：{primary}")
    lines.append(f"- 交叉验证：{cross_check}")
    lines.append("")
    lines.append("## 关键信息")
    for p in points or ["无"]:
        lines.append(f"- {p}")
    lines.append("")
    lines.append("## 可靠性判断")
    lines.append(f"- {reliability}")
    return "\n".join(lines)


if __name__ == "__main__":
    main()
