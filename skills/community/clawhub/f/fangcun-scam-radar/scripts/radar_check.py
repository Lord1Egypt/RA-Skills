#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
防割特征自检（scam-radar）—— 纯标准库零依赖

用途：把用户口述的营销事实逐项过"五特征"自检，输出：
  1. 命中特征清单（只陈述"命中了什么"）
  2. 核对提示（低风险核对项 / 存疑 / 高度存疑 —— 这是核对结果分级，不是定性）
  3. 对应官方查验路径

硬约束：
1. 绝不输出"是骗局/是诈骗/是杀猪盘/快跑"等定性词（输出前自扫，命中即告警）。
2. 不荐任何替代产品，只给正规渠道判断标准。
3. 缺数据优雅降级：没勾的特征按"未提供"处理，不猜。

用法：
    python radar_check.py --input case.json [--output report.md]
    （省略 --input 时用 --demo 跑内置示例；省略 --output 打印 stdout）

case.json 结构：
{
  "channel": "荐股群 / 私信老师 / 低价理财课 / 理财App / 其他",
  "claims": {
    "guaranteed_profit": true,      // 对方承诺保本/稳赚/固定高收益
    "high_return": true,            // 宣称收益显著高于常规（如年化>10%仍"保本"）
    "show_screenshot": false,       // 晒他人收益截图诱导
    "no_license_proof": true,       // 索要资质证明时含糊/拒绝/给"海外牌照"
    "no_risk_test": true,           // 不做风险测评直接带买
    "personal_account": true,       // 要求转账到个人账户或不明App充值
    "no_third_custody": true,       // 资金无银行第三方存管
    "low_price_ladder": false,      // 低价课引流→话术升级卖高价课/贷款买课
    "recruit_refund": false,        // 拉人头返佣/发展下级可退费
    "urgency_pressure": true        // 制造紧迫感（名额有限/今天不买明天涨）
  }
}
"""

import argparse
import json
import sys
from pathlib import Path

# Windows 控制台中文输出兜底（--demo / stdout 模式）
if sys.stdout and hasattr(sys.stdout, "buffer"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 特征定义：(key, 特征名, 所属五特征维度, 官方查验指引)
FEATURES = [
    ("guaranteed_profit", "承诺保本/稳赚/固定收益", "收益表述",
     "常识核对：收益与风险成正比是基本规律，「保本+高收益」本身是矛盾表述。正规机构从不承诺收益。"),
    ("high_return", "宣称收益显著高于常规水平", "收益表述",
     "对照常识：宣称收益越高，风险与可疑度越高，请核对产品底层是什么、在哪监管。"),
    ("show_screenshot", "晒他人收益截图诱导", "收益表述",
     "常识核对：收益截图可任意伪造，不构成任何资质或业绩证明。"),
    ("no_license_proof", "资质证明含糊/拒绝/称海外牌照", "持牌",
     "官方查验：证监会官网「监管对象」公示、中国证券业协会/基金业协会官网查询机构名。查无即无资质。"),
    ("no_risk_test", "不做风险测评直接带买", "流程",
     "正规开户流程必须先做风险测评；跳过测评属违规展业信号。"),
    ("personal_account", "要求转入个人账户/不明App充值", "资金去向",
     "正规投资资金走银行第三方存管、进自己名下账户。要求转个人账户的，立即停止。"),
    ("no_third_custody", "资金无第三方存管", "资金去向",
     "官方查验：向你的开户银行核实是否存在对应存管协议。"),
    ("low_price_ladder", "低价引流→升级话术→卖高价课/贷款买课", "收费模式",
     "官方提示：监管与消协多次提示此类「网络理财课程陷阱」套路。已付费且遭诱导贷款的，保留凭证可向消协/监管部门投诉。"),
    ("recruit_refund", "拉人头返佣/发展下级可退费", "收费模式",
     "常识核对：「拉人头返佣」具备传销典型特征，可向市场监管部门 12315 咨询。"),
    ("urgency_pressure", "制造紧迫感（名额有限/过时不候）", "流程",
     "常识核对：正规产品不会用倒计时逼单。紧迫感是防你冷静核实的常用手法。"),
    ("crypto_involved", "涉及虚拟币/USDT/境外交易所", "监管禁区",
     "监管事实：境内虚拟货币相关业务活动属非法金融活动（央行等十部门 2021 年 9 月通知），参与不受法律保护；境内无任何合法虚拟币交易平台。"),
    ("forex_margin", "涉境外外汇/贵金属保证金平台", "监管禁区",
     "监管事实：境内依法批准的外汇零售保证金交易业务不存在；宣称英国/塞浦路斯等境外牌照不受境内法律保护，牌照需到该国监管官网核实（多为伪造）。"),
    ("withdraw_fee", "出金被要求先缴保证金/解冻费/税", "监管禁区",
     "常识核对：正规平台出金不收「解冻费/保证金」。出现此要求属于典型收割信号，应立即停止追加资金并考虑报案。"),
]

# 监管禁区特征 key：境内本就非法/无牌照可查的业务，命中即"高度存疑"
RED_LINE_KEYS = {"crypto_involved", "forex_margin", "withdraw_fee"}

# 五特征维度 → 核对提示分级规则
DIM_WEIGHT = {"持牌": 2, "资金去向": 2, "收益表述": 1, "收费模式": 1, "流程": 1, "监管禁区": 3}

# 定性词黑名单：输出前自扫，命中即告警（工具绝不下定性）
_QUALITATION_BLOCKLIST = [
    "是骗局", "是诈骗", "是杀猪盘", "是传销", "是坑", "就是骗子",
    "赶紧跑", "快跑", "立即退出", "马上报警抓", "一定被骗",
    "这是假的", "全是假的",
    # 荐股/承诺变体（防输出文件带出"替用户决定"的词形）
    "应该买", "该买哪个", "肯定翻倍", "保证追回", "帮你追回", "帮你追",
]


def check(case):
    """执行特征核对。返回 (hits, missing, score, red_hit)。"""
    claims = case.get("claims") or {}
    hits, missing = [], []
    score = 0
    red_hit = False
    for key, name, dim, guide in FEATURES:
        v = claims.get(key)
        if v is True:
            hits.append((name, dim, guide))
            score += DIM_WEIGHT.get(dim, 1)
            if key in RED_LINE_KEYS:
                red_hit = True
        elif v is False:
            pass  # 明确否认 → 不命中
        else:
            missing.append(name)
    return hits, missing, score, red_hit


def level_of(score, n_hits, red_hit=False):
    """核对分级（这是核对结果，不是对个案的定性）。

    监管禁区特征（虚拟币/外汇保证金/出金缴费）境内本就无合法牌照可查，
    命中任一条即为"高度存疑"——与 SKILL.md「命中即高度存疑」承诺一致。
    """
    if red_hit:
        return "高度存疑（命中监管禁区特征，境内无合法牌照可查，强烈建议立即停止投入并走官方查验/报案路径）"
    if n_hits == 0:
        return "低风险核对项"
    if score >= 4 or n_hits >= 3:
        return "高度存疑（强烈建议完成全部官方查验后再做任何决定）"
    return "存疑（建议先走官方查验路径核实）"


def render(case, hits, missing, score, red_hit=False):
    lines = []
    add = lines.append
    channel = case.get("channel", "未说明渠道")

    add("【防割特征自检报告】")
    add("")
    add("> 通用识别特征 + 官方查验路径，不构成对任何具体产品/平台的定性或投资建议。")
    add("> 工具只列「你描述的命中事实」，结论由你自己下。")
    add("")
    add(f"- 渠道：{channel}")
    add(f"- 核对结果：**{level_of(score, len(hits), red_hit)}**")
    add("")

    if hits:
        add("## 命中特征（按你口述的事实）")
        add("")
        for name, dim, guide in hits:
            add(f"- **{name}**（维度：{dim}）")
            add(f"  - 核对/查验：{guide}")
        add("")
    else:
        add("## 命中特征")
        add("")
        add("- 你描述的情况未命中本工具的特征清单。这不代表没有风险，")
        add("  建议仍按下方「标准查验流程」走一遍，尤其是查持牌。")
        add("")

    if missing:
        add("## 信息待补")
        add("")
        add(f"以下 {len(missing)} 条特征你还没确认（不确定 ≠ 没有，建议向对方问清，"
            "答完回来补上重跑）：")
        add("")
        add("；".join(missing))
        add("")

    add("## 标准查验流程（无论命中多少，建议都走一遍）")
    add("")
    add("1. **查持牌**：证监会官网「监管对象」公示 / 中国证券业协会 / 中国证券投资基金业协会官网，搜机构全名。")
    add("2. **查投顾资质**：基金业协会「基金投顾机构名录」——名录外任何「智能投顾/老师带单」均无资质。")
    add("3. **查 App 来源**：只从官方应用商店下载；工信部 ICP 备案查询核对网站主体。")
    add("4. **核对资金路径**：确认资金走银行第三方存管、进入自己名下账户；任何「转给个人/充值到陌生App」都应停止。")
    add("")
    add("## 如果钱已经转出")
    add("")
    add("- 立即拨打 96110（全国反诈专线）或 110，说明情况，争取紧急止付；")
    add("- 联系你的银行/支付平台申请冻结或止付；")
    add("- 用国家反诈中心 App 举报并保留聊天记录、转账凭证。")
    add("- （工具不评估能否追回，以警方与银行处理为准。）")
    add("")
    add("---")
    add("*生成工具：scam-radar。以上为通用识别特征与官方查验路径，不构成对任何具体产品/平台的定性或投资建议；判断权在你，具体以持牌机构与官方信息为准。*")
    return "\n".join(lines) + "\n"


def compliance_scan(text):
    """输出前自扫定性词。返回命中列表 [(word, line_no)]。"""
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        for w in _QUALITATION_BLOCKLIST:
            if w in line:
                hits.append((w, i))
    return hits


DEMO = {
    "channel": "荐股群（示例）",
    "claims": {
        "guaranteed_profit": True,
        "high_return": True,
        "show_screenshot": True,
        "no_license_proof": True,
        "no_risk_test": True,
        "personal_account": True,
        "no_third_custody": True,
        "low_price_ladder": False,
        "recruit_refund": False,
        "urgency_pressure": True,
    },
}

# ---- 常见场景预设（--scenario 一键跑；特征按该场景的典型表现预设，跑完仍需用户逐项确认） ----
SCENARIOS = {
    "stockgroup": ("荐股群/老师带单（典型预设）", {
        "guaranteed_profit": True, "high_return": True, "show_screenshot": True,
        "no_license_proof": True, "no_risk_test": True, "personal_account": True,
        "no_third_custody": True, "low_price_ladder": None, "recruit_refund": None,
        "urgency_pressure": True,
    }),
    "cheapcourse": ("9元/免费理财课（典型预设）", {
        "guaranteed_profit": None, "high_return": None, "show_screenshot": None,
        "no_license_proof": None, "no_risk_test": None, "personal_account": None,
        "no_third_custody": None, "low_price_ladder": True, "recruit_refund": None,
        "urgency_pressure": True,
    }),
    "unknownapp": ("陌生理财App（典型预设）", {
        "guaranteed_profit": True, "high_return": True, "show_screenshot": True,
        "no_license_proof": True, "no_risk_test": True, "personal_account": True,
        "no_third_custody": True, "low_price_ladder": None, "recruit_refund": None,
        "urgency_pressure": True,
    }),
    "insurancemixed": ("保障当理财卖（典型预设）", {
        "guaranteed_profit": True, "high_return": None, "show_screenshot": None,
        "no_license_proof": None, "no_risk_test": None, "personal_account": None,
        "no_third_custody": None, "low_price_ladder": True, "recruit_refund": None,
        "urgency_pressure": True,
    }),
}


def main():
    ap = argparse.ArgumentParser(description="防割特征自检（只列事实+查验路径，不下定性）")
    ap.add_argument("--input", "-i", default=None, help="case.json 路径")
    ap.add_argument("--output", "-o", default=None, help="输出 report.md（缺省打印 stdout）")
    ap.add_argument("--demo", action="store_true", help="跑内置示例（荐股群全特征命中）")
    ap.add_argument("--scenario", "-s", choices=sorted(SCENARIOS), default=None,
                    help="常见场景预设：" + ", ".join(f"{k}({v[0]})" for k, v in sorted(SCENARIOS.items())))
    args = ap.parse_args()

    if args.demo:
        case = DEMO
    elif args.scenario:
        name, claims = SCENARIOS[args.scenario]
        case = {"channel": name, "claims": claims}
    elif args.input:
        p = Path(args.input)
        if not p.exists():
            print(f"[ERROR] 输入文件不存在: {p}", file=sys.stderr)
            sys.exit(2)
        try:
            case = json.loads(p.read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"[ERROR] 输入不是合法 UTF-8 JSON（带 BOM 的 Windows 存档也支持）: {e}", file=sys.stderr)
            sys.exit(2)
    else:
        ap.print_help()
        sys.exit(2)

    # ---- 输入结构统一校验（含 AI 代填出错的情况，优雅报错不崩溃）----
    if not isinstance(case, dict):
        print("[ERROR] case.json 根必须是对象（dict）。", file=sys.stderr)
        sys.exit(2)
    if not isinstance(case.get("claims"), dict):
        print(f"[ERROR] claims 字段必须是对象（{{特征名: true/false/null}}），收到的是"
              f" {type(case.get('claims')).__name__}。"
              "用户口述特征无法自动解析——请按 interview.md 十问逐条确认后整理为 JSON 对象；"
              "不确定的特征直接省略或写 null。", file=sys.stderr)
        sys.exit(2)

    hits, missing, score, red_hit = check(case)
    report = render(case, hits, missing, score, red_hit)

    qhits = compliance_scan(report)
    if qhits:
        print("[COMPLIANCE WARNING] 输出含定性词，禁止交付：", file=sys.stderr)
        for w, ln in qhits:
            print(f"  - 行{ln} 命中: {w}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"[OK] 报告已写入: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
