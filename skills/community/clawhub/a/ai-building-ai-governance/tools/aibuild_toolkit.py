# -*- coding: utf-8 -*-
"""AI 造 AI 治理与安全 - 本地工具（零依赖，Python 标准库）

命令：
  form      形态识别（输入系统描述，判断 AI 造 AI 形态与能力等级）
  risk      风险清单（按形态输出独特风险与缓释）
  checklist 治理检查清单（按阶段 design/develop/deploy/review）
  synthetic 合成数据合规要点
  verify    产物验证清单
"""
import argparse
import sys

# ---------------- 形态关键词库 ----------------
FORM_RULES = [
    {
        "id": "coding",
        "name": "编码智能体（AI 造软件）",
        "level": "基础",
        "autonomy": "中-高",
        "keywords": ["编码", "写代码", "生成代码", "编程", "提交", "代码库", "PR", "补全", "Copilot", "agent 写", "代码审查"],
    },
    {
        "id": "synthetic",
        "name": "合成数据与蒸馏（AI 造训练数据/模型）",
        "level": "进阶",
        "autonomy": "中",
        "keywords": ["合成数据", "蒸馏", "训练数据", "生成数据", "标注", "数据增强", "微调", "教师模型", "学生模型"],
    },
    {
        "id": "research",
        "name": "AI 研究自动化（AI Scientist）",
        "level": "高阶",
        "autonomy": "高",
        "keywords": ["研究", "实验", "论文", "Scientist", "科研", "假设", "文献", "自动化实验"],
    },
    {
        "id": "selfimprove",
        "name": "自我改进与递归提升（RSI）",
        "level": "前沿",
        "autonomy": "极高",
        "keywords": ["自我改进", "自蒸馏", "自奖励", "递归", "自我提升", "self-improvement", "self-rewarding", "RSI", "改进自己", "自主升级"],
    },
]

# ---------------- 风险库 ----------------
RISK_LIB = {
    "coding": [
        ("代码质量", "幻觉代码：错误 API/算法，需强制 Review + 自动化测试 + SAST"),
        ("供应链投毒", "诱导安装恶意依赖（依赖混淆），需 lockfile + 私有源 + SBOM 扫描"),
        ("越权破坏", "自主执行 rm/push --force/改生产配置，需沙箱 + 命令白名单 + 高危人工确认"),
        ("许可证合规", "生成代码可能带 GPL 等传染性许可证，需 CI 许可证扫描 + 采购条款核查"),
        ("提示注入", "代码库中的恶意指令（间接注入），需将代码库视为不可信输入 + 动作分级审批"),
    ],
    "synthetic": [
        ("模型坍缩", "合成占比过高逐代退化，需控制占比（建议≤30%）+ 真实数据锚点 + 漂移监测"),
        ("错误放大", "教师模型的系统性错误被复制放大，需合成数据质量门禁 + 人工抽样校验"),
        ("版权与条款", "API 输出用于训练/蒸馏可能违约（2026 主流条款禁止），需条款核查 + 专门授权"),
        ("隐私泄漏", "模型记忆真实个体信息，需成员推断测试 + 相似度检查"),
        ("标识义务", "合成内容用于生成式服务需标识，衔接内容标识办法/欧盟 Article 50"),
    ],
    "research": [
        ("科研诚信", "幻觉引用/自动填充数据（p-hacking 自动化），需引用校验 + 原始数据存档 + 人工复核"),
        ("监督缺失", "自主循环无人闸门导致错误假设放大，需每个研究循环设人工检查点"),
        ("双用途风险", "加速危险领域研究（生物/化学/武器），需领域风险分级 + 高危禁自动化"),
        ("知识产权", "AI 生成论文署名/权属规则，需按期刊政策披露 AI 参与度（主流共识 AI 不作为作者）"),
    ],
    "selfimprove": [
        ("目标漂移", "优化表面指标偏离真实目标（自奖励易奖励黑客），需奖励函数人审 + 多指标交叉验证"),
        ("能力突然跃升", "递归改进致能力非线性跃升超出治理预期，需能力阈值监控 + 跃升熔断"),
        ("退化循环", "自训练无新鲜数据强化偏见/错误，需真实数据锚点 + 外部基准对照"),
        ("失控边界", "无上限自主改进可能绕过安全对齐，需能力/资源/权限三层封顶 + 人工闸门"),
    ],
}

# ---------------- 分阶段检查清单 ----------------
CHECKLISTS = {
    "design": [
        "明确 AI 造 AI 形态与自主度，登记台账（形态/负责人/风险级）",
        "评估风险等级：编码/合成数据默认中风险，研究自动化高风险，自我改进极高风险",
        "设定能力边界：任务范围、可访问资源、输出权力（不可由 AI 自行修改）",
        "蒸馏/API 输出用于训练前，核查服务条款并留存记录",
        "确定人工闸门点：哪些动作必须人工批准",
    ],
    "develop": [
        "编码智能体：沙箱隔离 + 命令白名单 + 高危操作两阶段提交",
        "供应链锁定：lockfile + 哈希校验 + 私有源优先 + 依赖扫描",
        "合成数据：来源记录（工具/版本/配置可复现）+ 质量门禁 + 占比控制",
        "合成数据合规：成员推断测试 + 版权来源审计 + 标识评估",
        "自奖励/自蒸馏训练：奖励函数人审 + 双人评审",
    ],
    "deploy": [
        "上线前重跑安全评测（蒸馏学生模型不豁免）",
        "能力监控与熔断：能力评测跳变、自我扩权行为、目标漂移检测",
        "内容标识：AI 生成内容按标识办法/Article 50 执行",
        "审计日志：改进链/变更链全记录（谁改了什么、依据什么、人批了什么）",
        "供应商评估：AI 造 AI 工具/模型的采购合同责任条款核查",
    ],
    "review": [
        "月度复盘：质量指标（AI 代码采纳率/引入 bug 率/合规违规数）",
        "事故复盘：任何越权/注入/坍缩事件走根因分析闭环",
        "能力体检：自我改进系统的能力与行为偏离检查",
        "治理委员会议程：AI 造 AI 项目季度审阅",
        "知识更新：前沿风险（RSI 等）跟踪，更新风险库",
    ],
}

# ---------------- 合成数据合规要点 ----------------
SYNTHETIC_POINTS = [
    ("来源记录", "合成工具/模型版本、生成配置、生成时间——可复现"),
    ("质量门禁", "自动校验（语法/语义）+ 人工抽样（抽检率≥1%）"),
    ("隐私测试", "成员推断测试（Membership Inference）+ 与真实数据相似度检查"),
    ("版权审计", "训练数据版权来源审计 + API 条款核查（是否允许输出用于训练）"),
    ("标识评估", "合成内容是否需显式/隐式标识（衔接内容标识办法/Article 50）"),
    ("占比控制", "合成占比建议≤30%，保留真实数据锚点"),
    ("坍缩监测", "训练中分布监测 + 上线后漂移监测，发现退化即回调占比"),
    ("数据卡", "Data Card：来源、占比、生成方法、已知局限"),
]

# ---------------- 产物验证清单 ----------------
VERIFY_POINTS = [
    ("代码产物", "自动化测试通过 + 人工 Code Review + SAST 扫描 + 许可证扫描 + 依赖哈希核对"),
    ("研究产物", "引用校验（防幻觉引用）+ 原始数据/实验记录存档 + 关键结论人工复核 + 披露声明"),
    ("模型产物", "基准对比（教师-学生差异评测）+ 安全评测重跑 + 偏见审计 + 漂移监测"),
    ("红队衔接", "关键 AI 产物复用红队测试方法论（提示注入/越权/数据泄露）"),
]


def detect_form(desc):
    """按关键词命中数判断形态（命中 ≥1 即判定，多形态取命中最多）"""
    desc_l = desc.lower()
    best = None
    best_hits = 0
    for rule in FORM_RULES:
        hits = sum(1 for kw in rule["keywords"] if kw.lower() in desc_l)
        if hits > best_hits:
            best_hits = hits
            best = rule
    return best, best_hits


def cmd_form(args):
    if not args.desc:
        print("错误：--desc 必填（系统描述）。")
        return 2
    rule, hits = detect_form(args.desc)
    print("=" * 60)
    if not rule:
        print("未命中明确形态——建议人工对照 01 模块谱系判定")
        print("提示：可包含关键词如 编码/合成数据/蒸馏/研究/自我改进/递归")
        return 0
    print(f"判定形态：{rule['name']}")
    print(f"能力等级：{rule['level']}　自主度：{rule['autonomy']}")
    print(f"关键词命中：{hits} 处")
    print("提示：见 01 模块谱系确认；用 risk --form 查看该形态风险")
    return 0


def cmd_risk(args):
    if args.form not in RISK_LIB:
        print("错误：--form 仅支持 coding / synthetic / research / selfimprove。")
        return 2
    print("=" * 60)
    print(f"形态：{args.form}　风险清单与缓释：")
    for i, (name, detail) in enumerate(RISK_LIB[args.form], 1):
        print(f"{i}. {name}：{detail}")
    return 0


def cmd_checklist(args):
    if args.phase not in CHECKLISTS:
        print("错误：--phase 仅支持 design / develop / deploy / review。")
        return 2
    print("=" * 60)
    print(f"阶段：{args.phase}　治理检查清单：")
    for i, item in enumerate(CHECKLISTS[args.phase], 1):
        print(f"{i}. {item}")
    return 0


def cmd_synthetic(args):
    print("=" * 60)
    print("合成数据合规要点（见 03 模块详解）：")
    for i, (name, detail) in enumerate(SYNTHETIC_POINTS, 1):
        print(f"{i}. {name}：{detail}")
    return 0


def cmd_verify(args):
    print("=" * 60)
    print("AI 产物验证清单（见 02/04/05 模块详解）：")
    for i, (name, detail) in enumerate(VERIFY_POINTS, 1):
        print(f"{i}. {name}：{detail}")
    return 0


def main():
    p = argparse.ArgumentParser(description="AI 造 AI 治理与安全本地工具（零依赖）")
    sub = p.add_subparsers(dest="cmd")

    p_form = sub.add_parser("form", help="形态识别")
    p_form.add_argument("--desc", required=True, help="系统描述，如：AI编码智能体，自动生成并提交代码")

    p_risk = sub.add_parser("risk", help="风险清单")
    p_risk.add_argument("--form", required=True, choices=["coding", "synthetic", "research", "selfimprove"])

    p_check = sub.add_parser("checklist", help="治理检查清单")
    p_check.add_argument("--phase", required=True, choices=["design", "develop", "deploy", "review"])

    sub.add_parser("synthetic", help="合成数据合规要点")
    sub.add_parser("verify", help="产物验证清单")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return 0
    fn = {"form": cmd_form, "risk": cmd_risk, "checklist": cmd_checklist,
          "synthetic": cmd_synthetic, "verify": cmd_verify}[args.cmd]
    return fn(args)


if __name__ == "__main__":
    sys.exit(main())
