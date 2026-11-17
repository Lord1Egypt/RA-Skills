#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_governance_toolkit.py — 企业 AI 治理本地工具包
仅使用 Python 标准库，零网络、零数据采集。

命令：
  classify --scenario "<场景描述>"   AI 风险分级评估（低/中/高/禁止）
  policy   --company "<公司名>" --sector "<行业>"   生成 AI 使用政策草案
  registry --company "<公司名>"     生成 AI 应用登记表模板（CSV）
  maturity --scores "a,b,c,d,e,f"   成熟度自评计分（6 维度 1-5 分）
  checklist --region <cn|eu|intl|apac>   落地行动清单
  --help                             查看帮助
"""

import argparse
import csv
import io
import sys

VERSION = "1.0.0"


# ---------------------------------------------------------------- classify
# 风险评分模型（与 references/03 模块一致）：
# 数据敏感度30% + 决策影响度30% + 自动化程度15% + 暴露范围15% + 出错危害10%

KEYWORD_BANK = {
    "data_sensitive": {
        5: ["个人信息", "隐私", "身份证", "简历", "病历", "健康", "财务数据", "客户数据", "生物识别", "人脸", "指纹", "基因"],
        3: ["内部数据", "经营数据", "销售数据", "合同", "员工", "内部"],
        1: ["公开", "公开资料", "行业报告", "百科"],
    },
    "decision_impact": {
        5: ["招聘", "简历", "候选人", "录用", "晋升", "信贷", "贷款", "保险", "定价", "医疗诊断", "治疗", "处方", "执法", "考勤", "绩效"],
        3: ["客服", "营销", "生成文案", "建议", "推荐", "回复"],
        1: ["翻译", "总结", "摘要", "排版", "纪要", "检索"],
    },
    "automation": {
        5: ["自动执行", "全自动", "无人", "自主", "agent", "Agent", "智能体", "自动回复", "自动决策"],
        3: ["半自动", "自动生成", "批量", "自动"],
        1: ["辅助", "人工", "人审", "复核"],
    },
    "exposure": {
        5: ["对外", "公众", "客户", "公开上线", "面向用户", "对外发布", "发布"],
        3: ["内部", "部门", "团队"],
        1: ["个人", "自己"],
    },
    "harm": {
        5: ["人身", "生命", "安全", "不可逆", "违法", "犯罪", "欺诈"],
        3: ["经济损失", "声誉", "投诉"],
        1: ["可回滚", "可修正", "低影响"],
    },
}

PROHIBITED_KEYWORDS = [
    "社会信用", "社会评分", "无差别", "抓取人脸", "情绪识别", "未成年人弱点",
    "非自愿亲密", "儿童性虐待", "深度伪造诽谤", "实施诈骗", "规避监管",
]

# 生命健康/金融/执法类决策：03 模块 §2 明确列为高风险场景，命中即高风险
CRITICAL_DECISION_KEYWORDS = [
    "医疗诊断", "治疗", "处方", "执法", "信贷", "贷款", "录用", "晋升",
]


def _dimension_score(text, bank):
    """按关键词词典给单个维度打分，命中高权重优先。"""
    best = 1
    for score in (5, 3, 1):
        for kw in bank.get(score, []):
            if kw in text:
                best = max(best, score)
    return best


def classify(scenario):
    if not scenario or not scenario.strip():
        print("错误：场景描述不能为空。示例：--scenario \"用AI筛选候选人简历，辅助HR做初筛\"")
        return 2

    for kw in PROHIBITED_KEYWORDS:
        if kw in scenario:
            print("=" * 60)
            print("风险分级结果：【禁止级】")
            print(f"命中禁止清单关键词：{kw}")
            print("依据：该场景违反基本法律与伦理底线，一律禁止（见 03 模块 §2）。")
            return 0

    weights = {"data_sensitive": 0.30, "decision_impact": 0.30,
               "automation": 0.15, "exposure": 0.15, "harm": 0.10}
    scores = {k: _dimension_score(scenario, KEYWORD_BANK[k]) for k in weights}
    weighted = sum(scores[k] * weights[k] for k in weights)

    if weighted >= 4.0:
        level = "高风险"
        note = "需 AI 治理委员会审批 + 专项风险评估（03 模块 §5 义务矩阵）"
    elif weighted >= 2.5:
        level = "中风险"
        note = "需部门负责人审批 + 合规备案（03 模块 §5 义务矩阵）"
    else:
        level = "低风险"
        note = "登记台账即可，年度复审（03 模块 §5 义务矩阵）"

    red_flag = (
        # 敏感数据 + 重大决策 → 高风险（如人事/信贷/医疗决策）
        (scores["data_sensitive"] >= 4 and scores["decision_impact"] >= 4)
        # 高敏数据（生物识别/健康/基因等）→ 高风险，无论决策属性
        or scores["data_sensitive"] >= 5
    )
    if red_flag and level != "高风险":
        level = "高风险"
        note = "命中高风险特征（敏感数据或重大决策），按 03 模块 §2 高风险场景处理"

    # 关键决策领域直判（医疗/金融/执法/人事晋升）
    for kw in CRITICAL_DECISION_KEYWORDS:
        if kw in scenario and level != "高风险":
            level = "高风险"
            note = f"命中关键决策领域关键词「{kw}」，03 模块 §2 高风险场景"

    print("=" * 60)
    print("AI 风险分级评估结果")
    print("=" * 60)
    print(f"场景：{scenario}")
    print(f"综合加权分：{weighted:.2f}（满分 5.00）")
    print("-" * 60)
    for k in weights:
        print(f"  {k}：{scores[k]} 分（权重 {int(weights[k]*100)}%）")
    print("-" * 60)
    print(f"风险等级：【{level}】")
    print(f"处理建议：{note}")
    return 0


# ---------------------------------------------------------------- policy
POLICY_TEMPLATE = """# {company}员工AI使用政策

**版本**：v1.0 ｜ **生效日期**：{date} ｜ **发布**：AI治理委员会

## 第 1 条 目的与适用范围
为规范公司全体员工使用人工智能（AI）工具与服务的活动，防范数据泄露、合规与伦理风险，特制定本政策。
本政策适用于{company}全体员工及使用公司设备、数据或名义使用 AI 的所有人员。

## 第 2 条 允许使用的 AI 场景（白名单）
1. 通用办公辅助：文本起草、翻译、摘要、数据分析辅助（使用公司批准的工具清单内产品）；
2. 经审批的业务应用：已通过 AI 应用登记与风险评估的专用工具。

## 第 3 条 禁止行为（红线）
1. 禁止将公司机密信息、客户个人信息、未公开商业数据输入未经批准的 AI 工具；
2. 禁止使用 AI 生成涉及重大决策的内容而未加人工复核（如：合同条款、对外承诺、招聘结论、合规结论）；
3. 禁止使用 AI 生成虚假、诽谤、侵权或违反法律法规的内容；
4. 对外发布 AI 生成内容必须按国家规定完成内容标识；
5. 禁止擅自接入未经 IT/合规批准的外部 AI 服务或插件；
6. 禁止用 AI 工具处理涉密数据与受控数据。

## 第 4 条 数据分级使用要求
| 数据级别 | 示例 | 可否用于 AI 工具 |
|---|---|---|
| 公开数据 | 公开资料、行业报告 | 可用（仍需遵守工具条款） |
| 内部数据 | 内部流程、非敏感经营信息 | 仅限公司批准工具 |
| 机密数据 | 客户名单、报价、技术文档 | 禁止 |
| 个人信息 | 员工/客户个人信息 | 禁止，除非经合规专门评估 |
| 涉密/受控 | 按保密制度执行 | 禁止 |

## 第 5 条 内容审核与人工复核
1. AI 生成内容发布前必须人工审核；涉及法律、财务、对外承诺的内容须由责任部门复核；
2. AI 辅助决策（招聘筛选、信贷、营销触达等）须保留人工复核环节与记录。

## 第 6 条 登记与上报
1. 员工使用新的 AI 工具/服务前，须按《AI 应用登记与审批流程》登记；
2. 发现 AI 相关安全事件、疑似数据泄露、异常行为，立即上报信息安全负责人，不得自行处置。

## 第 7 条 违规处理
违反本政策的，视情节轻重给予警告、培训、停用权限直至纪律处分；造成损失的依法追责。

## 第 8 条 生效与修订
本政策自发布之日起生效，由 AI 治理委员会负责解释与修订，至少每年评审一次。

---
*本模板由企业 AI 治理实操手册生成，使用前请由公司合规/法务复核并按实际情况修改。*
"""

SECTOR_NOTES = {
    "医疗器械": "本行业注意：AI 相关产品若作为医疗器械软件（含 AI 辅助诊断）上市，须评估医疗器械监管要求与欧盟 AI Act Annex I 高风险时间线（2028-08-02）。",
    "金融": "本行业注意：AI 决策涉及信贷/保险/定价等场景，属于欧盟 AI Act Annex III 高风险场景（2027-12-02 适用），须重点落实人工监督与可解释性。",
    "教育": "本行业注意：教育场景 AI 在欧盟属 Annex III 高风险（2027-12-02 适用），涉及未成年人的服务须额外关注中国《人工智能拟人化互动服务管理暂行办法》。",
    "制造": "本行业注意：关注《人工智能+制造专项行动实施意见》与工业数据安全要求。",
}


def policy(company, sector):
    date = "____年__月__日"
    print(POLICY_TEMPLATE.format(company=company, date=date))
    if sector and sector in SECTOR_NOTES:
        print("\n【行业提示】" + SECTOR_NOTES[sector])
    print("\n[说明] 请替换日期后，由合规/法务复核后发布。")
    return 0


# ---------------------------------------------------------------- registry
REGISTRY_FIELDS = [
    "应用编号", "应用名称", "使用部门", "使用场景", "使用方式",
    "涉及数据级别", "风险等级", "供应商/产品", "数据流向",
    "人工复核机制", "责任人", "审批状态", "审批人",
    "内容标识", "备案/评估状态", "复审日期", "备注",
]


def registry(company):
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(REGISTRY_FIELDS)
    writer.writerow(["AI-2026-001", "", "", "", "员工工具/嵌入业务系统/对外服务",
                     "公开/内部/机密/个人信息", "低/中/高/禁止", "",
                     "是否出境/是否用于训练", "是/否", "", "草稿/审批中/已批准/已驳回",
                     "", "是/否（涉对外生成时必填）", "是否需要算法备案/大模型备案/安全评估",
                     "", ""])
    print(out.getvalue(), end="")
    print(f"\n[说明] 以上为 {company} 的 AI 应用登记表模板（CSV 格式），"
          "请复制到表格软件中按字段填写；字段定义见 07 模块。")
    return 0


# ---------------------------------------------------------------- maturity
MATURITY_DIMENSIONS = ["组织", "制度", "风险", "合规", "技术", "文化"]


def maturity(scores_str):
    try:
        scores = [int(x.strip()) for x in scores_str.split(",")]
    except ValueError:
        print("错误：--scores 需为 6 个数字，用逗号分隔，如 3,4,2,5,3,4")
        return 2
    if len(scores) != 6:
        print(f"错误：需要 6 个维度评分，当前收到 {len(scores)} 个。示例：--scores 3,4,2,5,3,4")
        return 2
    if any(s < 1 or s > 5 for s in scores):
        print("错误：每个维度评分须在 1-5 之间。")
        return 2

    total = sum(scores)
    print("=" * 60)
    print("AI 治理成熟度自评结果（6 维度，每项 1-5 分）")
    print("=" * 60)
    for name, s in zip(MATURITY_DIMENSIONS, scores):
        bar = "█" * s + "░" * (5 - s)
        flag = " ← 短板" if s <= 2 else ""
        print(f"  {name}：{s} 分 {bar}{flag}")
    print("-" * 60)
    print(f"总分：{total} / 30")

    if total <= 12:
        stage = "起步期"
        advice = "建议先完成 90 天落地路线第 1-2 阶段：摸底、定责任人、发布使用政策。"
    elif total <= 23:
        stage = "建设期"
        weak = [name for name, s in zip(MATURITY_DIMENSIONS, scores) if s <= 2]
        advice = "建议补齐短板" + ("：" + "、".join(weak) + "。" if weak else "，优先政策与台账。")
    elif total <= 29:
        stage = "成型期"
        advice = "体系已运转，建议保持季度闭环，向 ISO 42001 差距分析看齐。"
    else:
        stage = "体系化"
        advice = "治理体系化运转，关注法规新变化与新技术风险（智能体、具身智能等）。"

    print(f"阶段判断：{stage}")
    print(f"改进建议：{advice}")
    print("\n[说明] 自评为主观参考，非第三方认证结论；评分请附证据（台账、审批记录等）。")
    return 0


# ---------------------------------------------------------------- checklist
CHECKLISTS = {
    "cn": [
        "对外生成式 AI 服务：完成大模型备案/登记 + 安全评估",
        "算法推荐/深度合成/生成式服务：完成算法备案",
        "AI 生成内容：落实显式+隐式双标识（2025-09-01 起强制）",
        "训练/使用数据：来源合法，个人信息按个保法合法处理",
        "涉密与重要数据：禁止用于 AI 训练与处理",
        "智能体/拟人化 AI 服务（如适用）：按 2026 新规防越权、防诱导、标识、未成年人保护",
        "员工 AI 使用：发布内部使用政策 + 数据分级",
        "个人信息自动化决策：保障拒绝权、知情权、人工复核",
        "跟踪《人工智能法》立法进展（国务院 2026 立法计划已列）",
    ],
    "eu": [
        "盘点在欧盟部署/面向欧盟用户的所有 AI 系统，按 AI Act 分级",
        "透明度义务：AI 交互告知 + 生成内容标识（2026-08-02 起，旧系统 2026-12-02 前完成）",
        "GPAI 义务（如提供通用模型）：技术文档、训练数据摘要、版权政策",
        "高风险系统：对照 Annex III（2027-12-02）与 Annex I（2028-08-02）新时间线排期",
        "高风险系统：风险管理、技术文档、符合性评估、欧盟数据库注册准备",
        "部署者义务：使用限制、人工监督、日志、AI 素养培训",
        "禁止条款自查：社会评分、无差别人脸抓取、情绪识别等（2025-02-02 起禁）",
        "非自愿亲密影像等新增禁止条款（2026-12-02 起）自查",
        "第三国提供者：确认是否需指定欧盟授权代表",
    ],
    "intl": [
        "用 NIST AI RMF 四功能（Govern/Map/Measure/Manage）做风险方法论骨架",
        "建立 AI 使用政策 + 员工守则 + 数据分级",
        "建立 AI 应用登记台账与分级审批",
        "按经营地跟踪美国州法（加州 AB 2013 训练数据透明度、德州 TRAIGA 等）",
        "评估 ISO/IEC 42001 认证必要性（客户/采购要求时启动差距分析）",
        "技术控制参考 OWASP LLM Top 10",
        "建立季度法规跟踪机制（中国/欧盟/美国）",
        "年度成熟度自评 + 治理报告",
    ],
    "apac": [
        "出海韩国：AI 基本法（2026-01-22 生效）高影响 AI 注册/年度透明度报告/人工监督/事件响应/部署前风险评估",
        "出海日本：AI 促进法（软法）+ APPI 数据合规（敏感信息、跨境传输）",
        "出海新加坡：执行模型 AI 治理框架（2026-05 Agentic AI 版）+ AI Verify 测试",
        "出海中国香港：按 PCPD 框架做隐私影响评估 + AI 决策人工复核 + 文档留痕",
        "出海澳大利亚：金融业更新 AI 供应商合同（2026-07-01 前）+ 自动化决策透明度义务（2026-12-10 生效）",
        "出海越南：AI 法（2026-03-01 生效）风险分级合规",
        "出海印度：DPDP Act + 印度 AI 治理指南（咨询性）",
        "统一底座：ISO/IEC 42001 管理体系 + 各国要求当 overlay 叠加",
        "数据合规先行：以当地数据保护法（PIPA/APPI/PDPA/PDPO）为直接约束基础层",
        "季度跟踪：韩国实施令、新加坡 MAS 指南定稿、澳洲 ADM 生效等法规变化",
    ],
}


def checklist(region):
    if region not in CHECKLISTS:
        print("错误：--region 仅支持 cn（中国）/ eu（欧盟）/ intl（国际通用）/ apac（亚太出海）。")
        return 2
    print(f"{'=' * 60}")
    region_name = {"cn": "中国", "eu": "欧盟", "intl": "国际通用", "apac": "亚太出海"}[region]
    print(f"{region_name} AI 治理落地行动清单")
    print(f"{'=' * 60}")
    for i, item in enumerate(CHECKLISTS[region], 1):
        print(f"  [ ] {i}. {item}")
    print("\n[说明] 逐项完成并留痕（截图/记录归档），作为合规审计证据。")
    return 0


# ---------------------------------------------------------------- main
def main():
    parser = argparse.ArgumentParser(
        prog="ai_governance_toolkit",
        description=f"企业 AI 治理本地工具包 v{VERSION}（零网络、零数据采集，仅标准库）",
    )
    sub = parser.add_subparsers(dest="command")

    p_classify = sub.add_parser("classify", help="AI 风险分级评估")
    p_classify.add_argument("--scenario", required=True, help="AI 使用场景描述")

    p_policy = sub.add_parser("policy", help="生成 AI 使用政策草案")
    p_policy.add_argument("--company", required=True, help="公司名称")
    p_policy.add_argument("--sector", default="", help="行业（医疗器械/金融/教育/制造等）")

    p_registry = sub.add_parser("registry", help="生成 AI 应用登记表模板")
    p_registry.add_argument("--company", required=True, help="公司名称")

    p_maturity = sub.add_parser("maturity", help="成熟度自评计分")
    p_maturity.add_argument("--scores", required=True, help="6 个维度 1-5 分，逗号分隔")

    p_checklist = sub.add_parser("checklist", help="落地行动清单")
    p_checklist.add_argument("--region", required=True, choices=["cn", "eu", "intl", "apac"],
                             help="区域：cn=中国 / eu=欧盟 / intl=国际通用 / apac=亚太出海")

    args = parser.parse_args()

    if args.command == "classify":
        return classify(args.scenario)
    if args.command == "policy":
        return policy(args.company, args.sector)
    if args.command == "registry":
        return registry(args.company)
    if args.command == "maturity":
        return maturity(args.scores)
    if args.command == "checklist":
        return checklist(args.region)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
