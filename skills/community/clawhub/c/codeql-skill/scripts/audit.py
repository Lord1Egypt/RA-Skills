#!/usr/bin/env python3
"""
[AUDIT] CodeQL SARIF 二次分析脚本
用法: python3 audit.py <results.sarif> [--output exp.md]

流程:
  1. 解析 SARIF findings
  2. 按攻击面入口优先排序
  3. 按漏洞族分组，提取 source→sink 证据链
  4. 输出 exp.md（含 POC 模板）
"""

import json
import sys
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# ── 漏洞族映射 ───────────────────────────────────────────────────
VULN_FAMILIES = {
    "sql":            ["sql-injection", "SqlInjection", "query-injection"],
    "deserialize":    ["unsafe-deserialization", "Deserialization", "readObject"],
    "cmd-injection":  ["command-injection", "CommandInjection", "process-injection"],
    "path-traversal": ["path-traversal", "PathTraversal", "zip-slip"],
    "xxe":            ["xxe", "XxeLocal", "XxeRemote", "xml-injection"],
    "ssrf":           ["ssrf", "ServerSideRequestForgery", "request-forgery"],
    "xss":            ["xss", "Xss", "cross-site-scripting", "DomBasedXss"],
    "unauth":         ["missing-auth", "broken-auth", "authorization"],
}

# ── 攻击面优先级（入口类型关键词） ──────────────────────────────
SURFACE_PRIORITY = [
    ("HTTP 入口",   ["Servlet", "Controller", "Router", "Handler", "Endpoint", "RestController"]),
    ("RPC 入口",    ["Service", "Provider", "Consumer", "Dubbo", "Thrift", "grpc"]),
    ("文件上传",    ["upload", "multipart", "FileWrite", "FileUpload"]),
    ("认证边界",    ["login", "auth", "token", "session", "password", "credential"]),
    ("内部调度",    ["scheduler", "job", "task", "consumer", "listener", "cron"]),
    ("其他",        []),
]

SEVERITY_ORDER = {"error": 0, "warning": 1, "note": 2, "none": 3}


def parse_sarif(sarif_path: str) -> list[dict]:
    """解析 SARIF 文件，提取结构化 findings"""
    with open(sarif_path) as f:
        data = json.load(f)

    findings = []
    for run in data.get("runs", []):
        rules = {r["id"]: r for r in run.get("tool", {}).get("driver", {}).get("rules", [])}

        for result in run.get("results", []):
            rule_id = result.get("ruleId", "unknown")
            rule    = rules.get(rule_id, {})

            # 提取位置
            locs = result.get("locations", [])
            primary_loc = ""
            if locs:
                pl = locs[0].get("physicalLocation", {})
                uri  = pl.get("artifactLocation", {}).get("uri", "")
                line = pl.get("region", {}).get("startLine", "?")
                primary_loc = f"{uri}:{line}"

            # 提取数据流路径（source→sink 证据链）
            flow_steps = []
            for cf in result.get("codeFlows", []):
                for tf in cf.get("threadFlows", []):
                    for loc in tf.get("locations", []):
                        pl = loc.get("location", {}).get("physicalLocation", {})
                        uri  = pl.get("artifactLocation", {}).get("uri", "")
                        line = pl.get("region", {}).get("startLine", "?")
                        msg  = loc.get("location", {}).get("message", {}).get("text", "")
                        flow_steps.append(f"{uri}:{line}  ← {msg}")

            findings.append({
                "rule_id":   rule_id,
                "severity":  result.get("level", "warning"),
                "message":   result.get("message", {}).get("text", ""),
                "location":  primary_loc,
                "flow":      flow_steps,
                "rule_name": rule.get("name", rule_id),
                "rule_desc": rule.get("shortDescription", {}).get("text", ""),
            })

    return findings


def classify_surface(location: str) -> str:
    for label, keywords in SURFACE_PRIORITY:
        if any(kw.lower() in location.lower() for kw in keywords):
            return label
    return "其他"


def classify_family(rule_id: str) -> str:
    for family, keywords in VULN_FAMILIES.items():
        if any(kw.lower() in rule_id.lower() for kw in keywords):
            return family
    return "other"


def render_exp_md(findings: list[dict], sarif_path: str) -> str:
    """生成 exp.md 报告"""
    lines = []
    lines.append(f"# 安全审计报告\n")
    lines.append(f"- **扫描来源**: `{sarif_path}`")
    lines.append(f"- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"- **发现数量**: {len(findings)} 个\n")
    lines.append("---\n")

    # ── 攻击面清单（Rule 1）──────────────────────────────────────
    lines.append("## 攻击面清单\n")
    surface_groups = defaultdict(list)
    for f in findings:
        surface_groups[classify_surface(f["location"])].append(f)

    for label, _ in SURFACE_PRIORITY:
        count = len(surface_groups.get(label, []))
        if count:
            lines.append(f"- **{label}**: {count} 个 finding")
    lines.append("")

    # ── 按漏洞族分组输出（Rule 2）────────────────────────────────
    family_groups = defaultdict(list)
    for f in findings:
        family_groups[classify_family(f["rule_id"])].append(f)

    # 按严重程度排序
    sorted_findings = sorted(findings, key=lambda x: SEVERITY_ORDER.get(x["severity"], 9))

    vuln_idx = 1
    for family, items in sorted(family_groups.items()):
        lines.append(f"## 漏洞族: {family.upper()}\n")

        for f in sorted(items, key=lambda x: SEVERITY_ORDER.get(x["severity"], 9)):
            severity_label = f["severity"].upper()
            lines.append(f"### [VULN-{vuln_idx:03d}] {f['rule_name']} — `{f['location']}`\n")
            lines.append(f"**严重程度**: {severity_label}  ")
            lines.append(f"**规则**: `{f['rule_id']}`  ")
            lines.append(f"**描述**: {f['rule_desc'] or f['message']}\n")

            # Rule 3: source→sink 证据链
            lines.append("#### 证据链\n")
            if f["flow"]:
                lines.append("```")
                for i, step in enumerate(f["flow"]):
                    prefix = "SOURCE" if i == 0 else ("SINK  " if i == len(f["flow"]) - 1 else f"FLOW  ")
                    lines.append(f"{prefix}  {step}")
                lines.append("```\n")
            else:
                lines.append("> ⚠️ `[SUSPICIOUS - 待验证]` SARIF 中无完整数据流，需人工确认 source→sink 路径\n")

            # Rule 4: POC 模板
            lines.append("#### POC (待填写)\n")
            lines.append("```http")
            lines.append("# TODO: 根据证据链填写实际请求")
            lines.append("GET /your-endpoint?param=<payload> HTTP/1.1")
            lines.append("Host: target.example.com")
            lines.append("```\n")

            lines.append("#### 修复方案\n")
            lines.append("> TODO: 研发根据漏洞类型补充修复代码\n")
            lines.append("---\n")
            vuln_idx += 1

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="CodeQL SARIF 二次分析")
    parser.add_argument("sarif", help="SARIF 文件路径")
    parser.add_argument("--output", "-o", default="exp.md", help="输出报告路径")
    args = parser.parse_args()

    print(f"📖 解析 SARIF: {args.sarif}")
    findings = parse_sarif(args.sarif)
    print(f"✔ 发现 {len(findings)} 个 finding")

    print("⏳ 按攻击面 + 漏洞族分析...")
    report = render_exp_md(findings, args.sarif)

    Path(args.output).write_text(report, encoding="utf-8")
    print(f"✅ 报告生成完成 → {args.output}")
    print(f"   下一步: 人工补全 POC 和修复方案")


if __name__ == "__main__":
    main()
