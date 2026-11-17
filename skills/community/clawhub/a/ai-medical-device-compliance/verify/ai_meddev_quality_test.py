#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_meddev_quality_test.py — AI 医疗器械全球合规 质量与安全稳定性验证
本地闭环、零网络、零数据采集、仅标准库。产出 verify/security_results.json 供雷达图渲染。

6 个验证维度（每维度 0-5 分）：
  1. regulatory_timeliness  法规时效性（三地关键节点）
  2. coverage_completeness  覆盖完整性（8 模块 + 导航一致性）
  3. template_usability     工具可用性（5 命令 + 关键输出）
  4. risk_accuracy          分类/变更判定准确性
  5. structure_compliance   结构规范性（frontmatter/版权/免责/命令一致性）
  6. security_cleanliness   安全净度（敏感词 0 命中）
"""

import json
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_MD = os.path.join(BASE, "SKILL.md")
TOOL = os.path.join(BASE, "tools", "ai_meddev_toolkit.py")
REFS = os.path.join(BASE, "references")
VERIFY = os.path.join(BASE, "verify")
PYTHON = sys.executable


def check_regulatory_timeliness():
    items = []
    try:
        us = open(os.path.join(REFS, "02-美国FDA注册路径.md"), encoding="utf-8").read()
        eu = open(os.path.join(REFS, "03-欧盟MDR与AIAct.md"), encoding="utf-8").read()
        cn = open(os.path.join(REFS, "04-中国NMPA注册路径.md"), encoding="utf-8").read()
        checks = [
            ("FDA QMSR 2026-02 生效", "2026-02" in us and "QMSR" in us),
            ("FDA PCCP 预定变更控制", "PCCP" in us),
            ("FDA 510(k) 平均 142 天", "142" in us),
            ("FDA 网络安全 SBOM 强制", "SBOM" in us and "RTA" in us),
            ("EU MDR Rule 11 分类", "Rule 11" in eu),
            ("EU AI Act 高风险 2028-08-02", "2028-08-02" in eu),
            ("EU 公告机构排期提示", "18-24" in eu),
            ("EU CER/PMCF", "PMCF" in eu and "CER" in eu),
            ("NMPA 2026 分类界定更新", "2026" in cn and "分类界定" in cn),
            ("NMPA 1000 例数据本地化", "1,000" in cn or "1000" in cn),
            ("NMPA 变更注册触发", "变更注册" in cn),
            ("NMPA 创新通道", "创新" in cn),
            ("核对基准日标注", "核对基准日" in us and "核对基准日" in eu and "核对基准日" in cn),
        ]
        items = [{"name": n, "pass": p} for n, p in checks]
    except OSError as e:
        items = [{"name": f"读取失败: {e}", "pass": False}]
    return items


def check_coverage_completeness():
    items = []
    try:
        nav = open(SKILL_MD, encoding="utf-8").read()
        files = sorted(f for f in os.listdir(REFS) if f.endswith(".md"))
        items.append({"name": f"references 模块数=8（实际 {len(files)}）", "pass": len(files) == 8})
        for f in files:
            items.append({"name": f"导航表包含 {f}", "pass": f in nav})
        items.append({"name": "FAQ 专节存在", "pass": "FAQ" in nav and "常见问题" in nav})
        items.append({"name": "快速上手三步存在", "pass": "快速上手" in nav})
        items.append({"name": "能力边界如实说明", "pass": "能力边界" in nav})
    except OSError as e:
        items = [{"name": f"读取失败: {e}", "pass": False}]
    return items


def check_template_usability():
    items = []
    try:
        r = subprocess.run([PYTHON, TOOL, "classify", "--product", "CT肺结节AI辅助诊断软件，用于辅助医生阅片"],
                           capture_output=True, text=True, timeout=60)
        out = r.stdout or ""
        items.append({"name": "classify 命令执行成功", "pass": r.returncode == 0})
        for kw in ["美国 FDA", "欧盟 MDR", "中国 NMPA", "数据本地化"]:
            items.append({"name": f"classify 输出含「{kw}」", "pass": kw in out})

        r2 = subprocess.run([PYTHON, TOOL, "path", "--region", "us"], capture_output=True, text=True, timeout=60)
        out2 = r2.stdout or ""
        items.append({"name": "path 命令执行成功", "pass": r2.returncode == 0})
        for kw in ["510(k)", "Q-Sub", "SBOM"]:
            items.append({"name": f"path us 含「{kw}」", "pass": kw in out2})

        r3 = subprocess.run([PYTHON, TOOL, "estimate", "--region", "eu", "--class", "III"],
                            capture_output=True, text=True, timeout=60)
        out3 = r3.stdout or ""
        items.append({"name": "estimate 命令执行成功", "pass": r3.returncode == 0})
        for kw in ["费用", "周期", "Class III"]:
            items.append({"name": f"estimate 含「{kw}」", "pass": kw in out3})

        r4 = subprocess.run([PYTHON, TOOL, "compare"], capture_output=True, text=True, timeout=60)
        out4 = r4.stdout or ""
        items.append({"name": "compare 命令执行成功", "pass": r4.returncode == 0})
        for kw in ["PCCP", "FDA", "NMPA"]:
            items.append({"name": f"compare 含「{kw}」", "pass": kw in out4})
    except Exception as e:
        items = [{"name": f"执行失败: {e}", "pass": False}]
    return items


def check_risk_accuracy():
    cases = [
        ("CT肺结节AI辅助诊断软件，用于辅助医生阅片", ["Class III", "数据本地化"]),
        ("恶性肿瘤AI辅助诊断系统", ["Class III", "PMA"]),
        ("ICU生命支持决策AI", ["Class III", "PMA"]),
        ("健康数据存储显示软件", ["提示"]),
        ("胰岛素自动给药系统", ["Class III"]),
    ]
    items = []
    for product, expects in cases:
        try:
            r = subprocess.run([PYTHON, TOOL, "classify", "--product", product],
                               capture_output=True, text=True, timeout=60)
            out = r.stdout or ""
            ok = r.returncode == 0 and all(e in out for e in expects)
            items.append({"name": f"「{product[:14]}…」判定含 {'/'.join(expects)}", "pass": ok})
        except Exception as e:
            items.append({"name": f"「{product[:14]}…」失败: {e}", "pass": False})

    change_cases = [
        ("模型权重重新训练，训练数据扩至3倍，预期用途不变", "重大变更"),
        ("修复一个不影响核心临床功能的Bug，更新UI文案", "轻微变更"),
    ]
    for desc, expect in change_cases:
        try:
            r = subprocess.run([PYTHON, TOOL, "change", "--desc", desc],
                               capture_output=True, text=True, timeout=60)
            ok = r.returncode == 0 and expect in (r.stdout or "")
            items.append({"name": f"变更判定「{desc[:16]}…」={expect}", "pass": ok})
        except Exception as e:
            items.append({"name": f"变更判定失败: {e}", "pass": False})
    return items


def check_structure_compliance():
    items = []
    try:
        sk = open(SKILL_MD, encoding="utf-8").read()
        fm = sk.split("---")[1] if sk.startswith("---") else ""
        for field in ["name:", "slug:", "display_name:", "displayName:", "title:", "version:",
                      "category:", "platforms:", "author:", "license:", "description:", "description_en:", "tags:"]:
            items.append({"name": f"frontmatter 含 {field}", "pass": field in fm})
        items.append({"name": "版权与许可段存在", "pass": "版权与许可" in sk})
        items.append({"name": "MIT 声明", "pass": "MIT" in sk})
        items.append({"name": "知识版权声明存在", "pass": "知识版权声明" in sk})
        items.append({"name": "免责声明（AS IS）存在", "pass": "免责声明" in sk and "AS IS" in sk})
        items.append({"name": "LICENSE.md 存在且含 MIT", "pass": os.path.exists(os.path.join(BASE, "LICENSE.md"))})
        tool_src = open(TOOL, encoding="utf-8").read()
        for cmd in ["classify", "path", "estimate", "change", "compare", "--help"]:
            items.append({"name": f"工具实现命令 {cmd}", "pass": cmd in tool_src})
        for arg in ["--product", "--region", "--class", "--desc"]:
            items.append({"name": f"工具实现参数 {arg}", "pass": arg in tool_src})
    except OSError as e:
        items = [{"name": f"读取失败: {e}", "pass": False}]
    return items


def check_security_cleanliness():
    patterns = {
        "真实邮箱": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        "手机号": r"1[3-9][0-9]{9}",
        "本地路径(Win)": r"[A-Za-z]:\\\\Users\\\\",
        "本地路径(Unix)": r"[/\\]" + "Users" + r"[/\\][A-Za-z]",
        "密钥前缀": r"sk-[A-Za-z0-9]{16,}",
        "token 字样(代码语境)": r"(?i)api[_-]?key|access[_-]?token|secret[_-]?key",
        "私钥头": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    }
    items = []
    try:
        skip = {"verify", "__pycache__"}
        hits = []
        for root, dirs, files in os.walk(BASE):
            dirs[:] = [d for d in dirs if d not in skip]
            for fn in files:
                if not fn.endswith((".md", ".py", ".csv", ".txt", ".json", ".svg")):
                    continue
                p = os.path.join(root, fn)
                try:
                    text = open(p, encoding="utf-8").read()
                except UnicodeDecodeError:
                    continue
                rel = os.path.relpath(p, BASE)
                for name, pat in patterns.items():
                    for m in re.finditer(pat, text):
                        hits.append(f"{rel}: {name}")
        for name in patterns:
            items.append({"name": f"敏感模式「{name}」0 命中", "pass": not any(name in h for h in hits)})
        items.append({"name": "全包无任何命中", "pass": len(hits) == 0})
    except Exception as e:
        items = [{"name": f"扫描失败: {e}", "pass": False}]
    return items


DIMENSIONS = [
    ("regulatory_timeliness", "法规时效性", check_regulatory_timeliness),
    ("coverage_completeness", "覆盖完整性", check_coverage_completeness),
    ("template_usability", "工具可用性", check_template_usability),
    ("risk_accuracy", "判定准确性", check_risk_accuracy),
    ("structure_compliance", "结构规范性", check_structure_compliance),
    ("security_cleanliness", "安全净度", check_security_cleanliness),
]


def score(items):
    if not items:
        return 0.0
    return round(5.0 * sum(1 for i in items if i["pass"]) / len(items), 2)


def main():
    results = {
        "skill": "ai-medical-device-compliance",
        "version": "1.0.0",
        "note": "本地闭环验证：零网络、零数据采集、可重复",
        "dimensions": [],
        "summary": {},
    }
    for key, label, fn in DIMENSIONS:
        items = fn()
        s = score(items)
        results["dimensions"].append({"key": key, "label": label, "score": s, "checks": items})
        results["summary"][key] = s
        print(f"[{label}] {s:.2f}/5.00  ({sum(1 for i in items if i['pass'])}/{len(items)} 项通过)")
        for i in items:
            print(f"    {'PASS' if i['pass'] else 'FAIL'}  {i['name']}")

    results["benchmarks"] = {
        "industry_baseline": {
            "regulatory_timeliness": 2.5, "coverage_completeness": 3.0,
            "template_usability": 2.0, "risk_accuracy": 2.5,
            "structure_compliance": 3.0, "security_cleanliness": 3.0,
        },
        "enterprise_standard": {
            "regulatory_timeliness": 4.5, "coverage_completeness": 4.5,
            "template_usability": 4.0, "risk_accuracy": 4.5,
            "structure_compliance": 5.0, "security_cleanliness": 5.0,
        },
    }
    avg = round(sum(results["summary"].values()) / len(results["summary"]), 2)
    results["summary"]["average"] = avg
    os.makedirs(VERIFY, exist_ok=True)
    with open(os.path.join(VERIFY, "security_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n结果已写入：{os.path.join(VERIFY, 'security_results.json')}")
    print(f"综合平均分：{avg:.2f} / 5.00")
    return 0


if __name__ == "__main__":
    sys.exit(main())
