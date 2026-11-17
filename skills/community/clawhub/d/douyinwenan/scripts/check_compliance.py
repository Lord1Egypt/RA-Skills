# -*- coding: utf-8 -*-
"""抖音违禁词检测脚本 — 教育类口播合规检查（2026 版）

用法:
  python check_compliance.py "文案文本"
  python check_compliance.py --file draft.txt
  python check_compliance.py --json "文案文本"

检测七类风险（2026 抖音"语义+关键词"双维度监管口径）：
  [红线] 1. 绝对化用语（广告法第九条）
  [红线] 2. 承诺效果（教育类高风险）
  [红线] 3. 引流第三方（平台红线：导流微信/QQ/线下/其他平台）
  [警告] 4. 夸大/诱导（平台限流）
  [警告] 5. 贩卖焦虑（K12 红线语境，如"清华父母""提分"）
  [警告] 6. 谐音/变体（2026 语义识别新增，如"赚米""V❤"）
  [警告] 7. 价值观红线（职业歧视/收割家长，如"文科就是服务业""不报班就落后"）

⚠️ 词库是【基线】，平台规则每季度更新，命中结果以最新平台规则为准。
   建议每次使用前搜索官方渠道（抖音电商学习中心规则中心 / 生活服务学习中心）核对新增词。

退出码：存在任一红线词返回 1，否则返回 0。
"""
import argparse
import json
import re
import sys

# 绝对化用语（广告法第九条）
ABSOLUTE_WORDS = [
    "国家级", "世界级", "最高级", "最佳", "最好", "最优", "第一", "首个",
    "唯一", "独家", "绝对", "100%", "百分百", "百分之百", "全网", "史上",
    "最便宜", "最划算", "顶级", "极致", "完美",
    "全球第一", "国际级", "官方指定", "国家认证", "行业第一", "宇宙第一",
]

# 承诺效果（教育类高风险）
PROMISE_WORDS = [
    "保过", "包过", "保录取", "包录取", "保就业", "包就业", "保证考上",
    "稳上", "稳进", "稳过", "必过", "必上", "一定能考上", "百分百录取",
    "签约保过", "不过退款", "包分配", "包上岸",
    "一把过", "包教包会", "包找工作", "保上岸", "保研", "保提分",
    "提分保证", "必考", "包拿证", "保拿证", "保证录取",
]

# 引流第三方（平台红线：导流到站外/私域）
DRAIN_WORDS = [
    "加微信", "加QQ", "加我微信", "私信领取", "私信我", "评论区扣", "扣1",
    "扣我", "加V", "加薇", "V❤", "薇❤", "VX", "wx", "加vx", "加v",
    "进群领", "进群", "线下交易", "线下报名", "其他平台", "去淘宝", "去京东",
    "点我头像", "主页领取", "主页有", "私聊", "私信回复",
]

# 夸大/诱导（平台限流）
EXAGGERATE_WORDS = [
    "速成", "三天学会", "一周精通", "零基础秒懂", "躺赚", "暴富",
    "稳赚不赔", "内部渠道", "内部消息", "走后门", "关系户", "包过名额",
    "泄露", "内幕", "绝密", "震惊", "吓死", "不看后悔", "必转",
    "逆袭", "弯道超车", "秒懂", "一学就会", "零成本",
]

# 贩卖焦虑（K12 红线语境；命中为警告，需人工判断语境）
ANXIETY_WORDS = [
    "清华父母", "哈佛父母", "清华妈妈", "哈佛妈妈", "提分", "高分秘籍",
    "别人家的孩子", "输在起跑线", "再不学就晚了", "被淘汰", "阶层固化",
]

# 谐音/变体（2026 语义识别新增；命中为警告，需人工判断）
VARIANT_WORDS = [
    "赚米", "挣W", "赚W", "米多多", "搞钱", "暴利", "日入", "月入过万",
    "年入百万", "躺平就能", "白嫖", "薅羊毛",
]

# 价值观红线（职业歧视/收割家长；命中为警告，需人工判断语境）
VALUE_WORDS = [
    "文科就是服务业", "学文科没用", "理科才有用", "学理科没用",
    "不报班就落后", "不买课就落后", "不花钱就落后", "穷人不配",
    "寒门难出贵子", "没出息", "废物", "垃圾专业",
]

# 绝对化词需排除的合法上下文（如"第一志愿"是合法表达）
SAFE_CONTEXT = ["第一志愿", "第一时间", "第一学历", "第一年", "第一轮",
                "第一次", "第一版", "第一题", "第一名"]

# 承诺词需排除的合法上下文（如"保研率""保研名额"是客观指标，非承诺）
PROMISE_SAFE_CONTEXT = ["保研率", "保研名额", "保研比例", "保研资格",
                        "保研政策", "保研名单", "保研条件"]


def check(text, wordlist):
    hits = []
    for w in wordlist:
        for m in re.finditer(re.escape(w), text):
            # 绝对化词检查安全上下文
            if w in ABSOLUTE_WORDS:
                ctx = text[max(0, m.start() - 2):m.end() + 2]
                if any(s in ctx for s in SAFE_CONTEXT):
                    continue
            # 承诺词检查安全上下文（如"保研率"是客观指标）
            if w in PROMISE_WORDS:
                ctx = text[max(0, m.start() - 2):m.end() + 4]
                if any(s in ctx for s in PROMISE_SAFE_CONTEXT):
                    continue
            start = max(0, m.start() - 10)
            end = min(len(text), m.end() + 10)
            hits.append({"word": w, "context": text[start:end].replace("\n", " ")})
    return hits


def main():
    parser = argparse.ArgumentParser(description="抖音违禁词检测（2026 版）")
    parser.add_argument("text", nargs="?", help="文案文本")
    parser.add_argument("--file", help="从文件读取")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("用法: python check_compliance.py '文案' 或 --file draft.txt")
        sys.exit(1)

    absolute = check(text, ABSOLUTE_WORDS)
    promise = check(text, PROMISE_WORDS)
    drain = check(text, DRAIN_WORDS)
    exaggerate = check(text, EXAGGERATE_WORDS)
    anxiety = check(text, ANXIETY_WORDS)
    variant = check(text, VARIANT_WORDS)
    value = check(text, VALUE_WORDS)

    redline = len(absolute) + len(promise) + len(drain)
    warning = len(exaggerate) + len(anxiety) + len(variant) + len(value)

    if args.json:
        print(json.dumps({
            "absolute": absolute, "promise": promise, "drain": drain,
            "exaggerate": exaggerate, "anxiety": anxiety, "variant": variant,
            "value": value,
            "redline_total": redline, "warning_total": warning,
            "total": redline + warning,
        }, ensure_ascii=False, indent=2))
        return

    print("--- 抖音违禁词检测（2026 版）---")
    if redline + warning == 0:
        print("通过：未检测到违禁词。")
        sys.exit(0)

    if absolute:
        print(f"\n[红线] 绝对化用语 ({len(absolute)}):")
        for h in absolute:
            print(f"  - '{h['word']}' 上下文: ...{h['context']}...")
    if promise:
        print(f"\n[红线] 承诺效果 ({len(promise)}):")
        for h in promise:
            print(f"  - '{h['word']}' 上下文: ...{h['context']}...")
    if drain:
        print(f"\n[红线] 引流第三方 ({len(drain)}):")
        for h in drain:
            print(f"  - '{h['word']}' 上下文: ...{h['context']}...")
    if exaggerate:
        print(f"\n[警告] 夸大/诱导 ({len(exaggerate)}):")
        for h in exaggerate:
            print(f"  - '{h['word']}' 上下文: ...{h['context']}...")
    if anxiety:
        print(f"\n[警告] 贩卖焦虑/K12 ({len(anxiety)}):")
        for h in anxiety:
            print(f"  - '{h['word']}' 上下文: ...{h['context']}...")
    if variant:
        print(f"\n[警告] 谐音/变体 ({len(variant)}):")
        for h in variant:
            print(f"  - '{h['word']}' 上下文: ...{h['context']}...")
    if value:
        print(f"\n[警告] 价值观红线/职业歧视 ({len(value)}):")
        for h in value:
            print(f"  - '{h['word']}' 上下文: ...{h['context']}...")

    print("\n处理建议: 红线词（绝对化/承诺/引流）必须删除或改写；警告词建议弱化或人工判断语境。")
    print(f"\n统计: 红线 {redline} 个，警告 {warning} 个。")
    sys.exit(1 if redline else 0)


if __name__ == "__main__":
    main()
