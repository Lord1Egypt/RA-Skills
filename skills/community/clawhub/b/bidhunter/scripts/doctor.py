#!/usr/bin/env python3
"""
doctor.py - One-click diagnostics for BidHunter (BidHunter v1.5, A6).

Detects common misconfigurations and runtime issues, prints a human-readable
report with error codes and the exact next step for each. Exit code 0 = healthy,
1 = warnings, 2 = errors blocking operation.

Error codes:
  E001  rules file missing
  E002  rules not customized (still example placeholders)
  E003  rule health check failed
  E004  no cache / cache empty (never fetched)
  E005  push configured but test failed
  W001  push not configured (optional)
  W002  no high-priority regions set
  W003  budget/industry priority empty (A4 underused)
  W004  ai module missing MINIMAX key

Usage:
  python3 doctor.py [--rules <path>] [--fix-suggest]
"""
import json
import os
import sys
import subprocess
import argparse
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_DEFAULT = os.path.join(SCRIPT_DIR, "qual_rules.json")
CACHE_DIR = os.path.join(SCRIPT_DIR, "bid_cache")
PUSH_CFG = os.path.expanduser("~/.config/bidhunter/push.json")


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr)


def load_rules(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"__error__": str(e)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules", default=RULES_DEFAULT)
    ap.add_argument("--fix-suggest", action="store_true")
    args = ap.parse_args()

    issues = []
    warnings = []

    # E001 rules missing
    if not os.path.exists(args.rules):
        print(f"[E001] 规则文件不存在: {args.rules}")
        print("   → 下一步: cp scripts/qual_rules.json 你的目录，按营业执照填 entities")
        sys.exit(2)
    rules = load_rules(args.rules)
    if "__error__" in rules:
        print(f"[E001] 规则文件无法读取: {rules['__error__']}")
        sys.exit(2)

    # E002 not customized (example placeholders still present)
    entities = rules.get("entities", {})
    sample_markers = ["示例", "主体A", "主体B", "entity_a", "entity_b"]
    raw = json.dumps(rules, ensure_ascii=False)
    initialized = bool(rules.get("_initialized"))
    if any(m in raw for m in sample_markers) and not initialized:
        issues.append(("E002",
            "规则库仍是示例占位（entity_a/entity_b/示例），未替换为你的真实主体",
            "→ 一键生成：python3 bidhunter.py init（三问自动生成，约 1 分钟）\n"
            "   或手动编辑 qual_rules.json 的 entities，按营业执照经营范围填真实能力词\n"
            "   仍然卡住？python3 bidhunter.py feedback --type 2"))
    elif initialized:
        caps = []
        for e in entities.values():
            if isinstance(e, dict):
                caps += e.get("capabilities", []) or []
        if not caps:
            warnings.append(("W005", "规则库已初始化但能力词为空，匹配不会命中任何标的",
                             "→ 重跑 python3 bidhunter.py init 补填主营能力词，"
                             "或手改 qual_rules.json 的 entities.main.capabilities"))

    # E003 rule health
    try:
        r = subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "qual_check.py"),
                            "--validate-rules", args.rules],
                           capture_output=True, text=True)
        if r.returncode != 0:
            issues.append(("E003", "规则健康检查未通过",
                           "→ 运行: python3 qual_check.py --validate-rules qual_rules.json 看具体项"))
    except Exception as e:
        issues.append(("E003", f"无法运行健康检查: {e}", "→ 检查 Python 环境"))

    # E004 cache
    if not os.path.isdir(CACHE_DIR) or not any(
        f.startswith("bid_") for f in os.listdir(CACHE_DIR)
    ):
        issues.append(("E004", "尚无采集缓存，从未成功运行过采集",
                       "→ 运行: bash pipeline.sh  （首次会拉取当天公告）"))
    else:
        latest = sorted([f for f in os.listdir(CACHE_DIR) if f.startswith("bid_")])[-1]
        d = latest.replace("bid_", "").replace(".jsonl", "")
        try:
            dt = datetime.strptime(d, "%Y-%m-%d")
            if dt < datetime.now() - timedelta(days=3):
                warnings.append(("W004c", f"缓存较旧（{d}），可能已过期",
                                 "→ 运行 pipeline.sh --fresh 重新采集"))
        except Exception:
            pass

    # push
    if not os.path.exists(PUSH_CFG):
        warnings.append(("W001", "未配置推送通道（可选）",
                         "→ 运行: python3 config_wizard.py 配置钉钉/企微/邮件"))
    else:
        try:
            r = subprocess.run([sys.executable, os.path.join(SCRIPT_DIR, "push_manager.py"),
                                "test"], capture_output=True, text=True, timeout=30)
            if r.returncode != 0:
                issues.append(("E005", "推送通道测试失败",
                               "→ 运行: python3 push_manager.py test 看失败通道；重跑 config_wizard.py"))
        except Exception as e:
            issues.append(("E005", f"无法测试推送: {e}", "→ 检查 ~/.config/bidhunter/push.json"))

    # W002 regions
    if not rules.get("region_priority", {}).get("high"):
        warnings.append(("W002", "未设置重点地区（region_priority.high 为空）",
                         "→ 在 qual_rules.json 填重点跟标地区，如 [\"天津\",\"青岛\"]"))

    # W003 A4 priority
    if not rules.get("industry_priority") and not rules.get("budget_priority"):
        warnings.append(("W003", "未设置行业/预算优先级（A4 多维筛选未充分利用）",
                         "→ 在 qual_rules.json 加 industry_priority / budget_priority"))

    # W004 ai key
    if not os.environ.get("MINIMAX_API_KEY") and not os.path.exists(
            os.path.expanduser("~/.config/bidhunter/ai.json")):
        warnings.append(("W004", "未配置 MiniMax API Key（v2.0 AI 速读不可用）",
                         "→ 在 ~/.config/bidhunter/ai.json 写入 {\"api_key\":\"...\",\"group_id\":\"...\"}"))

    # Print report
    print("=" * 52)
    print(f" BidHunter 诊断报告  {datetime.now():%Y-%m-%d %H:%M}")
    print("=" * 52)
    if not issues and not warnings:
        print("✅ 一切正常，可以正常使用。")
        print("=" * 52)
        sys.exit(0)
    for code, msg, step in issues:
        print(f"[❌ {code}] {msg}\n   {step}")
    for code, msg, step in warnings:
        print(f"[⚠️  {code}] {msg}\n   {step}")
    print("=" * 52)
    if args.fix_suggest:
        print("建议依次处理上面的 ❌ 项；⚠️ 为可选增强。")
    sys.exit(2 if issues else 1)


if __name__ == "__main__":
    main()
