#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_meddev_toolkit.py — AI 医疗器械全球合规本地工具包
仅使用 Python 标准库，零网络、零数据采集。

命令：
  classify --product "<产品描述>"  三地分类判定（FDA/欧盟/NMPA）
  path     --region <us|eu|cn>     注册路径推荐
  estimate --region <us|eu|cn> --class <I|II|III>   费用与周期估算
  change   --desc "<变更描述>"     变更触发判定（需否重新注册）
  compare                          三地总对比表
  --help                           查看帮助
"""

import argparse
import sys

VERSION = "1.0.0"

# ---------------------------------------------------------------- classify

# 高风险/医疗决策关键词：Rule 11 与 FDA 功能性框架判定参考
CRITICAL_DECISION = ["恶性肿瘤", "癌症", "ICU", "急救", "生命支持", "胰岛素", "自动给药",
                     "自主诊断", "致死", "不可逆"]
HIGH_RISK_DECISION = ["诊断", "治疗", "用药", "处方", "检测", "筛查", "监护", "辅助诊断"]
INFO_ONLY = ["存储", "显示", "传输", "管理", "整理", "报告生成", "排版"]

# NMPA 数据本地化强相关场景
LOCAL_DATA_SCENES = ["肺结节", "病理", "影像", "心电", "脑", "眼底"]


def classify(product):
    if not product or not product.strip():
        print("错误：产品描述不能为空。示例：--product \"CT肺结节AI辅助诊断软件，用于辅助医生阅片\"")
        return 2
    p = product

    # 是否构成 SaMD（医疗目的）
    if any(k in p for k in INFO_ONLY) and not any(k in p for k in CRITICAL_DECISION + HIGH_RISK_DECISION):
        print("提示：描述偏「信息管理/展示类」，可能不构成 SaMD 或属最低风险类，请对照 01 模块确认医疗目的。")

    # FDA 功能性风险
    if any(k in p for k in CRITICAL_DECISION):
        fda = "Class III（生命攸关/高风险）→ PMA 或 De Novo"
    elif any(k in p for k in HIGH_RISK_DECISION):
        fda = "Class II（临床诊断/治疗信息，直接影响）→ 510(k) 或 De Novo"
    else:
        fda = "Class I-IIa（非直接临床决策）→ 一般控制/510(k) 评估"

    # 欧盟 Rule 11
    if any(k in p for k in CRITICAL_DECISION):
        eu = "Class III（Rule 11：高公共卫生/患者风险决策信息）"
    elif any(k in p for k in HIGH_RISK_DECISION):
        eu = "Class IIb（Rule 11：高患者风险决策信息）"
    else:
        eu = "Class IIa/I（Rule 11：其他临床决策信息）"

    # NMPA
    if any(k in p for k in ["自主诊断", "生命支持", "自动给药"]):
        cn = "Class III（高风险管理，自主诊断最高证据要求）"
    elif any(k in p for k in HIGH_RISK_DECISION):
        cn = "多为 Class III（AI 诊断软件通常归 III 类，NMPA 注册）"
    else:
        cn = "Class I/II（备案或省级注册，需分类界定确认）"

    print("=" * 62)
    print("三地分类判定（初步，正式以监管机构分类为准）")
    print("=" * 62)
    print(f"产品：{p}")
    print("-" * 62)
    print(f"【美国 FDA】{fda}")
    print(f"【欧盟 MDR】{eu}  (+ AI Act 高风险义务 2028-08-02 起)")
    print(f"【中国 NMPA】{cn}")

    if any(k in p for k in LOCAL_DATA_SCENES) and "诊断" in p or "筛查" in p:
        print("-" * 62)
        print("⚠️ 数据本地化提示：此类诊断场景在中国 Class III 通常需 1,000+ 例中国患者")
        print("   数据在境内医院验证、境内服务器存储（见 04 模块）。")
    print("-" * 62)
    print("建议下一步：path 命令看目标市场路径，estimate 估费用周期。")
    return 0


# ---------------------------------------------------------------- path

PATHS = {
    "us": [
        "产品画像与功能性风险定级（Class I/II/III）",
        "检索实质等同产品（510(k) 数据库）",
        "路径选择：有等同→510(k)；创新中低风险→De Novo；高风险→PMA",
        "Q-Sub 预提交：与 FDA 沟通策略 + PCCP 方案（70-90 天安排会议）",
        "准备：IEC 62304 软件生命周期 + QMSR 体系（2026-02 起）+ 数据/算法文档",
        "网络安全：SBOM + 漏洞管理 + 渗透测试（缺失=RTA）",
        "提交 510(k)/De Novo/PMA → 审评（90-150 天+）→ 企业注册",
        "上市后：漂移监控 + 不良事件 + PCCP 计划内更新",
    ],
    "eu": [
        "Rule 11 分类判定（临床决策影响 → Class I/IIa/IIb/III）",
        "锁定公告机构（⚠️ 提前 18-24 个月，双重审核能力机构稀缺）",
        "ISO 13485 QMS（含 AI 生命周期管理要素）",
        "技术文件：CER + 算法文档 + 数据文档",
        "AI Act 高风险义务准备（2028-08-02 前：风险管理/数据治理/日志/人工监督）",
        "网络安全：MDR Annex I 17.2",
        "公告机构审核 → CE 标志（MDR + AI Act 一并）",
        "EUDAMED 注册 + UDI → 上市 → PMCF + PSUR",
    ],
    "cn": [
        "分类界定（NMPA 分类界定申请，1-2 个月）",
        "数据准备：全国多地域多级医院代表性数据 + 标注规范",
        "算法文档 + 检测（第三方检测所，3-6 个月）",
        "临床评价：同品种比对 或 前瞻性多中心临床（Class III 常需）",
        "注册申报（含软件文档、网络安全）→ 技术审评",
        "生产体系核查 → 批准（18-36 个月；创新通道约 12 个月）",
        "上市后：变更注册管理（核心算法变更触发）+ 漂移监控",
    ],
}


def path(region):
    if region not in PATHS:
        print("错误：--region 仅支持 us（美国）/ eu（欧盟）/ cn（中国）。")
        return 2
    names = {"us": "美国 FDA", "eu": "欧盟 MDR+AI Act", "cn": "中国 NMPA"}
    print(f"{'=' * 62}")
    print(f"{names[region]} 注册路径推荐")
    print(f"{'=' * 62}")
    for i, s in enumerate(PATHS[region], 1):
        print(f"  {i}. {s}")
    print("\n[说明] 详细要求见 references 02/03/04 模块；正式申报以监管机构最新指南为准。")
    return 0


# ---------------------------------------------------------------- estimate

ESTIMATES = {
    "us": {
        "I":   {"cost": "官方费用：多数豁免/约 $2.6k；测试咨询 $3-10 万", "time": "3-6 个月"},
        "II":  {"cost": "510(k) 官方 $24,655-26,067（小企业约 $6.2-6.5k）＋测试/临床/咨询 $8-50 万", "time": "9-15 个月（510(k) 平均 142 天）"},
        "III": {"cost": "PMA 官方 $547,889-579,272（小企业约 $14-15 万）＋临床 $50-500 万", "time": "12-24 个月"},
    },
    "eu": {
        "I":   {"cost": "自我声明（Class I 无公告机构费）；技术文件成本 €2-5 万", "time": "6-12 个月"},
        "IIa": {"cost": "公告机构初始 €30,000-60,000＋年度 €10,000-20,000＋临床/咨询 €5-20 万", "time": "15-24 个月"},
        "IIb": {"cost": "公告机构初始 €50,000-100,000＋年度 €15,000-30,000＋临床/咨询 €10-40 万", "time": "18-30 个月"},
        "III": {"cost": "公告机构初始 €80,000-150,000＋年度 €20,000-40,000＋临床/咨询 €20-70 万", "time": "24-36 个月"},
    },
    "cn": {
        "I":   {"cost": "备案制（规费免费）＋检测 ¥5-15 万", "time": "3-8 个月"},
        "II":  {"cost": "检测 ¥5-15 万＋临床 ¥50-200 万＋咨询 ¥20-50 万（总计约 ¥75-265 万）", "time": "18-24 个月"},
        "III": {"cost": "检测 ¥10-30 万＋临床 ¥100-500 万＋咨询 ¥50-150 万（总计约 ¥160-680 万）", "time": "18-36 个月（创新通道约 12 个月）"},
    },
}


def estimate(region, cls):
    if region not in ESTIMATES:
        print("错误：--region 仅支持 us / eu / cn。")
        return 2
    if cls not in ESTIMATES[region]:
        print(f"错误：--class 仅支持 {', '.join(ESTIMATES[region].keys())}。")
        return 2
    names = {"us": "美国 FDA", "eu": "欧盟", "cn": "中国 NMPA"}
    d = ESTIMATES[region][cls]
    print(f"{'=' * 62}")
    print(f"{names[region]} Class {cls} 费用与周期估算")
    print(f"{'=' * 62}")
    print(f"费用：{d['cost']}")
    print(f"周期：{d['time']}")
    print("\n[说明] 公开渠道估算区间，仅作预算参考；FDA 费率按财年调整（可申请小企业减免约 75%），")
    print("       欧盟公告机构报价差异大（建议取 3 家报价），NMPA 费用随临床方案浮动。申报前复核。")
    return 0


# ---------------------------------------------------------------- change

MAJOR_CHANGE_KW = ["重新训练", "权重", "架构", "预期用途", "适应症", "扩大", "新增人群",
                   "训练数据", "数据源", "敏感度", "特异性", "性能", "运行环境", "平台",
                   "大版本", "核心算法"]
MINOR_CHANGE_KW = ["bug", "Bug", "界面", "UI", "文案", "文档", "修复", "优化", "显示"]


def change(desc):
    if not desc or not desc.strip():
        print("错误：变更描述不能为空。示例：--desc \"模型权重重新训练，预期用途不变\"")
        return 2
    major_hit = [k for k in MAJOR_CHANGE_KW if k in desc]
    minor_hit = [k for k in MINOR_CHANGE_KW if k in desc]

    print("=" * 62)
    print("变更触发判定（参考 06 模块框架，正式以监管意见为准）")
    print("=" * 62)
    print(f"变更描述：{desc}")
    print("-" * 62)

    # 明确轻微变更词且无重大变更词
    if minor_hit and not major_hit:
        print("判定：【轻微变更】→ 企业体系控制（记录 + 回归测试），无需立即申报。")
    elif major_hit:
        print("判定：【重大变更】→ 需重新注册 / 变更注册（或按 PCCP 预定计划执行）。")
        print(f"命中重大变更特征：{'、'.join(major_hit)}")
        print("-" * 62)
        print("分市场动作：")
        print("  · 美国：若在 PCCP 批准范围内 → 按计划执行；否则提交新 510(k)/补充申报")
        print("  · 欧盟：评估是否影响 CE 符合性 → 公告机构沟通（可能需要变更评估）")
        print("  · 中国：核心算法权重重训通常触发变更注册；创新通道可评估灵活方案")
    else:
        print("判定：【需人工复核】未命中明确关键词，请对照 06 模块变更分类框架逐项核对。")
    return 0


# ---------------------------------------------------------------- compare

COMPARE_ROWS = [
    ("AI 诊断软件类别", "多为 Class II", "多为 IIb/III", "多为 Class III"),
    ("审评时间（中风险）", "9-15 个月", "15-30 个月", "18-24 个月"),
    ("官方费用（中风险）", "$2.5-2.6 万（小企业减 75%）", "0（公告机构费另计）", "0（检测/临床另计）"),
    ("变更机制", "PCCP（最灵活）", "PACMP（日本）类比", "变更注册（保守）"),
    ("数据本地化", "无强制", "GDPR 合规", "1,000+ 例中国数据、境内存储"),
    ("网络安全", "SBOM 强制（否则 RTA）", "MDR 17.2 + CRA", "建议（趋严）"),
    ("临床证据", "文献/等同/研究", "CER + PMCF", "多中心临床（III 类常需）"),
    ("高风险义务节点", "随时（PMA/De Novo）", "AI Act 2028-08-02", "按产品风险"),
]


def compare():
    print("=" * 68)
    print("AI 医疗器械三地合规总对比")
    print("=" * 68)
    print(f"{'维度':<14s} {'美国 FDA':<22s} {'欧盟':<22s} {'中国 NMPA':<20s}")
    print("-" * 68)
    for dim, us, eu, cn in COMPARE_ROWS:
        print(f"{dim:<14s} {us:<22s} {eu:<22s} {cn:<20s}")
    print("-" * 68)
    print("详细：references/07-三地对比与出海策略.md ｜ 出海优先级决策见该模块 §3")
    return 0


# ---------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(
        prog="ai_meddev_toolkit",
        description=f"AI 医疗器械全球合规本地工具包 v{VERSION}（零网络、零数据采集，仅标准库）",
    )
    sub = parser.add_subparsers(dest="command")

    p_classify = sub.add_parser("classify", help="三地分类判定")
    p_classify.add_argument("--product", required=True, help="产品描述")

    p_path = sub.add_parser("path", help="注册路径推荐")
    p_path.add_argument("--region", required=True, choices=["us", "eu", "cn"], help="us=美国 / eu=欧盟 / cn=中国")

    p_estimate = sub.add_parser("estimate", help="费用与周期估算")
    p_estimate.add_argument("--region", required=True, choices=["us", "eu", "cn"], help="us=美国 / eu=欧盟 / cn=中国")
    p_estimate.add_argument("--class", dest="cls", required=True, help="风险类别 I/II/III")

    p_change = sub.add_parser("change", help="变更触发判定")
    p_change.add_argument("--desc", required=True, help="变更描述")

    sub.add_parser("compare", help="三地总对比表")

    args = parser.parse_args()

    if args.command == "classify":
        return classify(args.product)
    if args.command == "path":
        return path(args.region)
    if args.command == "estimate":
        return estimate(args.region, args.cls)
    if args.command == "change":
        return change(args.desc)
    if args.command == "compare":
        return compare()

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
