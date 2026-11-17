#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gdpr_toolkit.py — GDPR 出海合规本地工具包
仅使用 Python 标准库，零网络、零数据采集。

命令：
  scope     --desc "<业务描述>"    适用范围判定（域外管辖）
  legal     --desc "<处理场景>"    合法基础推荐
  rights    --right <access|erasure|portability|object|rectify|restrict>   数据主体权利速查
  transfer  --desc "<传输描述>"    跨境传输机制判定
  penalty                         罚款与通报速查
  --help                           查看帮助
"""

import argparse
import sys

VERSION = "1.0.0"

# ---------------------------------------------------------------- scope

SCOPE_RULES = [
    (["欧盟", "欧洲", "EU", "EUR", "€", "英镑", "德国", "法国", "英国", "西班牙", "意大利"],
     "可能适用：向欧盟境内主体提供商品/服务（GDPR 第 3(2)(a) 条）"),
    (["追踪", "画像", "监控", "分析行为", "广告追踪", "行为数据"],
     "可能适用：监控欧盟境内主体行为（GDPR 第 3(2)(b) 条）"),
    (["欧盟子公司", "欧洲办公室", "EU 机构", "欧洲办事处"],
     "适用：欧盟境内设立机构（GDPR 第 3(1) 条）"),
]


def scope(desc):
    if not desc or not desc.strip():
        print("错误：--desc 不能为空。示例：--desc \"中国公司运营App，向欧洲用户提供在线服务并收集其个人数据\"")
        return 2
    print("=" * 62)
    print("GDPR 适用范围判定（初步，正式以法律意见为准）")
    print("=" * 62)
    print(f"业务描述：{desc}")
    print("-" * 62)
    hit = False
    for kws, rule in SCOPE_RULES:
        if any(k in desc for k in kws):
            hit = True
            print(f"  ⚠️ {rule}")
    if not hit:
        print("  未命中明确指向欧盟的关键词——请按 01 模块判定（业务是否指向欧盟）。")
    print("-" * 62)
    print("核心判断：业务是否『指向欧盟』（语言/货币/欧盟用户占比/交付欧盟）。")
    print("若适用：首要动作=定合法基础（legal 命令）+ 隐私政策 + 跨境机制（transfer 命令）。")
    return 0


# ---------------------------------------------------------------- legal

LEGAL_RULES = [
    (["营销", "广告", "推送", "cookies", "Cookie", "个性化", "画像"],
     "同意（Consent）——营销/非必要处理须明确、知情、自由、可撤回的单独同意"),
    (["提供服务", "订单", "交付", "客户支持", "合同", "注册"],
     "合同履行（Contract）——仅限合同必需部分；非必需处理仍须同意"),
    (["法律", "法规", "报告", "税务", "审计"],
     "法律义务（Legal Obligation）——以法律要求为限"),
    (["健康", "医疗", "病历", "基因", "生物识别"],
     "特殊类别数据——须明确同意或医疗必要例外（第 9 条），且通常必做 DPIA"),
    (["防欺诈", "安全", "风控", "反洗钱"],
     "正当利益（Legitimate Interest）——须做利益平衡测试（LIA）并记录"),
]


def legal(desc):
    if not desc or not desc.strip():
        print("错误：--desc 不能为空。示例：--desc \"向欧洲用户发送营销邮件\"")
        return 2
    print("=" * 62)
    print("合法处理基础推荐（初步）")
    print("=" * 62)
    print(f"处理场景：{desc}")
    print("-" * 62)
    hit = False
    for kws, basis in LEGAL_RULES:
        if any(k in desc for k in kws):
            hit = True
            print(f"  ▶ {basis}")
    if not hit:
        print("  未命中明确场景——六项合法基础见 02 模块，按实际处理性质选择。")
    print("-" * 62)
    print("提醒：①营销须同意（ePrivacy+GDPR）②健康/生物识别=特殊类别③正当利益须 LIA 记录。")
    return 0


# ---------------------------------------------------------------- rights

RIGHTS = {
    "access": {"名称": "访问权", "内容": "获取个人数据副本 + 处理信息（目的/类别/接收方/保留期）", "时限": "1 个月（可延至 3 个月）"},
    "erasure": {"名称": "删除权（被遗忘权）", "内容": "删除个人数据（无保留必要/撤回同意/非法处理等情形）", "时限": "1 个月"},
    "portability": {"名称": "数据可携权", "内容": "以结构化机器可读格式获取并直接转移给另一控制者", "时限": "1 个月"},
    "object": {"名称": "反对权", "内容": "反对基于正当利益/直接营销的处理（营销必须停止）", "时限": "1 个月"},
    "rectify": {"名称": "更正权", "内容": "更正不准确的个人数据", "时限": "1 个月"},
    "restrict": {"名称": "限制处理权", "内容": "特定情形下限制处理（争议准确性/非法处理等）", "时限": "1 个月"},
}


def rights(right):
    if right not in RIGHTS:
        print("错误：--right 仅支持 access/erasure/portability/object/rectify/restrict。")
        return 2
    r = RIGHTS[right]
    print("=" * 62)
    print(f"数据主体权利：{r['名称']}")
    print("=" * 62)
    print(f"内容：{r['内容']}")
    print(f"响应时限：{r['时限']}")
    print("-" * 62)
    print("响应流程：身份核实 → 评估 → 执行/拒绝（说明理由）→ 记录 → 时限内完成。")
    return 0


# ---------------------------------------------------------------- transfer

TRANSFER_RULES = [
    (["日本", "英国", "韩国", "加拿大", "阿根廷", "新西兰", "瑞士", "充分性"],
     "充分性认定国家 → 无需额外措施（直接传输）"),
    (["中国", "美国", "印度", "东南亚", "总部", "国内", "境内"],
     "无充分性认定 → 需 SCC（标准合同条款）+ 传输影响评估（TIA）+ 补充措施"),
    (["集团", "子公司", "关联公司", "内部"],
     "跨国集团内部 → 可评估 BCR（约束性公司规则，须监管批准）或 SCC"),
    (["同意", "明确同意", "合同必要", "法律主张"],
     "例外情形（第 49 条）→ 慎用，仅限特定场景"),
]


def transfer(desc):
    if not desc or not desc.strip():
        print("错误：--desc 不能为空。示例：--desc \"将欧洲用户数据传输到中国总部处理\"")
        return 2
    print("=" * 62)
    print("跨境传输机制判定（初步）")
    print("=" * 62)
    print(f"传输描述：{desc}")
    print("-" * 62)
    hit = False
    for kws, mech in TRANSFER_RULES:
        if any(k in desc for k in kws):
            hit = True
            print(f"  ▶ {mech}")
    if not hit:
        print("  未命中明确目标地——机制选择见 05 模块（充分性/SCC/BCR/例外）。")
    print("-" * 62)
    print("要点：①SCC 用 2021 最新模板②补 TIA 与补充措施③中国无充分性认定④健康数据双限制。")
    return 0


# ---------------------------------------------------------------- penalty

def penalty():
    print("=" * 62)
    print("GDPR 罚款与泄露通报速查")
    print("=" * 62)
    print("【罚款两档】（第 83 条，EDPB 指引计算）")
    print("  高档次：2000 万欧元 或 全球年营业额 4%（取高者）")
    print("          ——违反合法基础/数据权利/跨境传输/儿童同意")
    print("  低档次：1000 万欧元 或 2%（取高者）")
    print("          ——违反记录/安全/DPO/认证义务")
    print("-" * 62)
    print("【泄露通报】")
    print("  监管机构：72 小时内（可延须说明）")
    print("  数据主体：高风险时无不当延误通知")
    print("  记录：所有泄露（含无需通报的）记录在案")
    print("-" * 62)
    print("响应流程：评估 → 72 小时通报 → 高风险通知个人 → 止损 → 记录 → 复盘。")
    return 0


# ---------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(
        prog="gdpr_toolkit",
        description=f"GDPR 出海合规本地工具包 v{VERSION}（零网络、零数据采集，仅标准库）",
    )
    sub = parser.add_subparsers(dest="command")

    p_scope = sub.add_parser("scope", help="适用范围判定")
    p_scope.add_argument("--desc", required=True, help="业务描述")

    p_legal = sub.add_parser("legal", help="合法基础推荐")
    p_legal.add_argument("--desc", required=True, help="处理场景")

    p_rights = sub.add_parser("rights", help="数据主体权利速查")
    p_rights.add_argument("--right", required=True, choices=["access", "erasure", "portability", "object", "rectify", "restrict"])

    p_transfer = sub.add_parser("transfer", help="跨境传输机制判定")
    p_transfer.add_argument("--desc", required=True, help="传输描述")

    sub.add_parser("penalty", help="罚款与通报速查")

    args = parser.parse_args()

    if args.command == "scope":
        return scope(args.desc)
    if args.command == "legal":
        return legal(args.desc)
    if args.command == "rights":
        return rights(args.right)
    if args.command == "transfer":
        return transfer(args.desc)
    if args.command == "penalty":
        return penalty()

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
