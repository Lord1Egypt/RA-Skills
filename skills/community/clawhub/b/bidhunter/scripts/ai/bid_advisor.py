#!/usr/bin/env python3
"""
bid_advisor.py - Generate bidding strategy suggestions (BidHunter v2.5).

Uses the structured extraction from a bid document + the user's own
qual_rules (capabilities / red_alerts) to produce a strategy brief:
  - 资质自检（我方能力 vs 门槛，标红缺口）
  - 评分得分点（按权重排优先级）
  - 报价/商务策略提示
  - 时间节点与风险提醒

COMPLIANCE BOUNDARY (v2.5): the assistant ONLY informs and advises.
It does NOT auto-fill quotes, forge qualifications, or write the technical
proposal. Every suggestion is clearly marked "仅供参考，最终决策人工确认".

Usage:
  python3 bid_advisor.py <招标文件.pdf|docx|txt>
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from doc_parser import parse as parse_doc
from clause_extractor import extract
from minimax_client import MiniMaxClient, ConfigError

RULES_PATH = os.path.join(os.path.dirname(HERE), "qual_rules.json")
MAX_CHARS = 9000
SYSTEM = (
    "你是资深招投标顾问。基于『招标文件结构化信息』与『投标方自身资质能力』，"
    "输出投标策略建议。只输出 JSON："
    "self_check(资质自检数组, 每项含 item(门槛), our_capable(布尔, 我方是否具备), gap(缺口说明)),"
    "score_focus(评分得分点数组, 字符串),"
    "pricing_tips(报价/商务策略提示数组, 字符串),"
    "timeline(关键时间节点数组, 字符串),"
    "risks(风险提醒数组, 字符串)。"
    "所有内容仅供参考，不代替人工决策，不虚构资质。"
)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 bid_advisor.py <file>", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"文件不存在: {path}", file=sys.stderr)
        sys.exit(1)

    text, backend = parse_doc(path)
    if not text:
        print("⚠️ 未能提取文本，请安装解析依赖：pip install PyPDF2 python-docx", file=sys.stderr)
        sys.exit(1)

    # v2.8: extract() now returns (result, meta) and reads the WHOLE document
    # via segmentation. The old call `clauses = extract(text)` received a tuple
    # and json.dumps'd it, so the strategy brief was built from a stringified
    # tuple — i.e. silently broken.
    try:
        clauses, meta = extract(text)
    except Exception as e:
        print(f"条款抽取失败: {e}", file=sys.stderr)
        sys.exit(1)

    # load our capabilities
    our_caps = []
    red_alerts = []
    try:
        with open(RULES_PATH, "r", encoding="utf-8") as f:
            rules = json.load(f)
        for e in rules.get("entities", {}).values():
            our_caps += e.get("capabilities", [])
        red_alerts = rules.get("red_alerts", [])
    except Exception:
        pass

    # v2.8: no API key no longer means "no output". The rule engine already
    # produced a usable brief (deadline, budget, method, requirements, risk
    # tendency). Only the advisory layer degrades, and it says so.
    advice = {}
    ai_used = False
    try:
        client = MiniMaxClient.from_config()
        prompt = (
            f"招标文件结构化信息：{json.dumps(clauses, ensure_ascii=False)}\n"
            f"我方资质能力词：{json.dumps(our_caps, ensure_ascii=False)}\n"
            f"我方红色预警（不可投类型）：{json.dumps(red_alerts, ensure_ascii=False)}\n"
            "请生成投标策略建议。"
        )
        raw = client.chat(prompt, system=SYSTEM, json_mode=True)
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw[raw.find("{"): raw.rfind("}") + 1]
        advice = json.loads(raw)
        ai_used = True
    except ConfigError as e:
        print(f"⚠️ 未配置 AI key（{e}）——以下为规则引擎版简报，"
              f"策略建议部分留空。", file=sys.stderr)
    except Exception as e:
        print(f"⚠️ 策略生成失败（{e}）——以下为规则引擎版简报。", file=sys.stderr)

    print("=" * 54)
    print(f"🧠 投标策略建议 · {os.path.basename(path)}")
    print("=" * 54)
    print(f"\n📄 读取覆盖度：{meta.get('coverage_pct','?')}% · "
          f"{meta.get('segments',0)} 个片段 · backend={backend} · "
          f"{'AI+规则' if meta.get('used_ai') else '仅规则引擎（未配 AI key）'}")

    if clauses.get("evaluation_method"):
        print(f"📌 评标办法：{clauses['evaluation_method']}")
    if clauses.get("bid_deadline"):
        print(f"⏰ 投标截止：{clauses['bid_deadline']}")
    if clauses.get("budget_yuan"):
        print(f"💰 预算/控制价：{clauses['budget_yuan']:,} 元")
    if clauses.get("has_risk_tendency"):
        print("⚠️ 含排他/内定倾向条款线索，建议人工复核")

    sc = clauses.get("score_conservation") or {}
    if sc.get("checked") and sc.get("verdict") == "MISMATCH":
        print(f"🚨 评分项分值不平：{sc.get('reason')} —— {sc.get('action','')}")
    elif sc.get("checked"):
        print(f"✅ 评分项分值守恒：{sc.get('reason')}")

    print("\n【资质自检】")
    if advice.get("self_check"):
        for item in advice["self_check"]:
            mark = "✅" if item.get("our_capable") else "❌ 缺口"
            print(f"  {mark} {item.get('item','')}  {item.get('gap','')}")
    else:
        for r in (clauses.get("qualification_requirements") or [])[:12]:
            tag = "必须" if r.get("mandatory") else "一般"
            print(f"  · [{tag}] {str(r.get('item',''))[:70]}")
        print("  （以上为招标文件要求原文摘录，『我方是否具备』须对照"
              "qual_rules.json 与实际资料判断）")
    print("\n【评分得分点】")
    si = clauses.get("score_items") or []
    if si:
        print("  评分项（来自招标文件原文抽取，含分值）：")
        for s in si:
            sc_txt = f"{s.get('score')}分" if s.get("score") is not None else "分值未识别"
            print(f"    · {s.get('name','')}  [{sc_txt}]")
    for s in advice.get("score_focus", []):
        print(f"  · {s}")
    print("\n【报价/商务策略】")
    for s in advice.get("pricing_tips", []):
        print(f"  · {s}")
    if not advice.get("pricing_tips"):
        print("  · 未配置 AI key，无策略建议")
        print("  · 报价须另跑：bidhunter.py quote check（四道算式卡）")
    print("\n【关键时间节点】")
    for s in advice.get("timeline", []):
        print(f"  · {s}")
    print("\n【风险提醒】")
    for s in advice.get("risks", []):
        print(f"  · {s}")
    unv = clauses.get("unverified") or []
    if unv:
        print("\n【未确认字段 · 严禁脑补，须人工核实】")
        print("  " + "、".join(unv))
    print("\n" + "=" * 54)
    print("⚠️ 以上为 AI 建议，仅供参考；最终投标决策与资质真实性由人工确认。")
    print("💡 接着可跑：bidhunter.py gap scan <标书>  出待补材料清单")
    print("=" * 54)


if __name__ == "__main__":
    main()
