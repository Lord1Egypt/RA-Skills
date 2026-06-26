#!/usr/bin/env python3
"""
[TUNE] CodeQL 查询调优脚本
用法: python3 tune.py <query.ql> [--output optimized.ql]

功能:
  1. 解析 .ql 文件结构（metadata、import、source/sink/sanitizer 定义）
  2. 运行调优 checklist，标记问题点
  3. 输出调优报告 + 优化建议（供 Claude 二次处理）
"""

import re
import sys
import argparse
from pathlib import Path

# ── Checklist 规则 ───────────────────────────────────────────────
CHECKS = [
    {
        "id": "META-01",
        "desc": "@metadata 完整性",
        "pattern": lambda src: all(
            tag in src for tag in ["@name", "@description", "@kind", "@problem.severity", "@id"]
        ),
        "fix": "补充缺失的 @metadata 标签（@name / @description / @kind / @problem.severity / @id）",
    },
    {
        "id": "SINK-01",
        "desc": "Sink 是否只覆盖单个方法名",
        "pattern": lambda src: not (
            re.search(r'getName\(\)\s*=\s*"[^""]+"', src)
            and not re.search(r'getName\(\)\s+in\s+\[', src)
        ),
        "fix": "将单个 getName() = \"foo\" 扩展为 getName() in [\"foo\", \"fooQuery\", ...] 覆盖同族 API",
    },
    {
        "id": "SANIT-01",
        "desc": "是否缺少 isSanitizer 定义",
        "pattern": lambda src: "isSanitizer" in src,
        "fix": "添加 isSanitizer() 以排除已知安全路径（参数化查询、转义函数等），减少误报",
    },
    {
        "id": "PERF-01",
        "desc": "是否使用了 any() 在 where 子句热路径",
        "pattern": lambda src: "any(" not in src.split("where")[-1] if "where" in src else True,
        "fix": "热路径中避免 any()，改用具体类型约束或 exists()",
    },
    {
        "id": "PERF-02",
        "desc": "是否使用了无界闭包（+/* transitive closure）",
        "pattern": lambda src: not re.search(r'\w+\+\w+|\w+\*\w+', src),
        "fix": "transitive closure（+/*）在大关系上性能极差，考虑限定深度或改用 DataFlow",
    },
    {
        "id": "NOISE-01",
        "desc": "是否过滤了测试/生成代码",
        "pattern": lambda src: "test" in src.lower() or "generated" in src.lower(),
        "fix": '添加过滤: not source.getNode().getFile().getRelativePath().matches("%test%")',
    },
    {
        "id": "KIND-01",
        "desc": "path-problem 查询是否导入了 PathGraph",
        "pattern": lambda src: (
            "path-problem" not in src
            or "DataFlow::PathGraph" in src
            or "PathGraph" in src
        ),
        "fix": "@kind path-problem 必须 import DataFlow::PathGraph",
    },
]


def parse_query(source: str) -> dict:
    """提取查询结构信息"""
    info = {}

    # metadata
    info["kind"]     = re.search(r'@kind\s+(\S+)', source)
    info["severity"] = re.search(r'@problem\.severity\s+(\S+)', source)
    info["id"]       = re.search(r'@id\s+(\S+)', source)
    info["imports"]  = re.findall(r'^import\s+\S+', source, re.MULTILINE)
    info["has_taint"]    = "TaintTracking" in source
    info["has_source"]   = "isSource" in source
    info["has_sink"]     = "isSink" in source
    info["has_sanitizer"]= "isSanitizer" in source

    return {k: (v.group(1) if hasattr(v, "group") else v) for k, v in info.items()}


def run_checklist(source: str) -> list[dict]:
    results = []
    for check in CHECKS:
        passed = check["pattern"](source)
        results.append({
            "id":     check["id"],
            "desc":   check["desc"],
            "passed": passed,
            "fix":    check["fix"] if not passed else None,
        })
    return results


def render_report(path: str, info: dict, checklist: list[dict]) -> str:
    lines = []
    lines.append(f"# 查询调优报告: `{path}`\n")

    # 基本信息
    lines.append("## 查询概览\n")
    lines.append(f"- kind: `{info.get('kind', '未找到')}`")
    lines.append(f"- severity: `{info.get('severity', '未找到')}`")
    lines.append(f"- id: `{info.get('id', '未找到')}`")
    lines.append(f"- 污点追踪: {'✔' if info.get('has_taint') else '✘'}")
    lines.append(f"- isSource 定义: {'✔' if info.get('has_source') else '✘'}")
    lines.append(f"- isSink 定义: {'✔' if info.get('has_sink') else '✘'}")
    lines.append(f"- isSanitizer 定义: {'✔' if info.get('has_sanitizer') else '✘'}\n")

    # Checklist
    lines.append("## 调优 Checklist\n")
    issues = [c for c in checklist if not c["passed"]]
    passed = [c for c in checklist if c["passed"]]

    if issues:
        lines.append(f"**发现 {len(issues)} 个问题:**\n")
        for c in issues:
            lines.append(f"- ❌ `{c['id']}` {c['desc']}")
            lines.append(f"  - 建议: {c['fix']}")
    else:
        lines.append("✅ 所有检查通过\n")

    lines.append(f"\n**通过 {len(passed)}/{len(checklist)} 项检查**\n")

    lines.append("---")
    lines.append("\n> 下一步: 将此报告和原始 .ql 文件交给 Claude，按建议优化后重新运行本脚本验证。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="CodeQL 查询调优")
    parser.add_argument("query", help=".ql 文件路径")
    parser.add_argument("--output", "-o", default=None, help="报告输出路径（默认打印到终端）")
    args = parser.parse_args()

    source = Path(args.query).read_text(encoding="utf-8")
    info = parse_query(source)
    checklist = run_checklist(source)
    report = render_report(args.query, info, checklist)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"✅ 调优报告 → {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
