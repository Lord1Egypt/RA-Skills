# -*- coding: utf-8 -*-
"""AI 模型资产管理（LLMOps）- 本地工具（零依赖，Python 标准库）

命令：
  inventory 资产盘点清单（五类资产）
  modelcard 模型卡模板
  lifecycle 生命周期检查（按阶段）
  drift     漂移监控要点
  cost      成本治理清单
"""
import argparse
import sys

INVENTORY_ITEMS = [
    ("模型", "登记：名称/版本/供应商/部署方式/成本/负责人（衔接模型卡）"),
    ("Prompt", "登记：场景/版本/参数/负责人（每次改动即新版本）"),
    ("知识库", "登记：文档集版本/切块策略/更新时间/向量库快照"),
    ("评估集", "登记：版本/规模/标注人/覆盖场景（衔接 LLM 评测）"),
    ("Agent 配置", "登记：工具权限/护栏/流程编排/责任人（衔接 Agent 治理）"),
    ("清理标记", "标出无人负责/无人使用/版本混乱的资产"),
    ("季度复核", "新增/变更/废弃资产核对更新"),
]

MODELCARD_TEMPLATE = """模型卡（Model Card）模板

一、基本信息
- 模型名称/版本：____
- 类型：基座 / 微调 / 蒸馏
- 供应商/来源：____（自研/第三方 API/开源）
- 部署方式：____（API/私有化/边缘）
- 负责人/创建时间：____

二、能力与用途
- 设计用途：____
- 已评估能力边界（评测结果）：____
- 不推荐用途（禁用场景）：____

三、数据与训练
- 训练数据来源/规模/时间：____
- 微调数据说明：____
- 数据合规状态（授权/脱敏/版权）：____

四、评测表现
- 评测集与指标结果：____
- 已知失败模式与限制：____

五、安全与合规
- 安全评测结果：____
- 内容标识义务：____
- 数据出境/本地化要求：____
- 许可证/使用条款：____

六、运维信息
- 成本（单次/月）：____
- 监控指标与告警：____
- 支持渠道/升级计划：____
"""

LIFECYCLE = {
    "register": [
        "Model Card 六字段齐备（基本/能力/数据/评测/安全/运维）",
        "评测集过门禁（衔接 LLM 评测 skill）",
        "安全评测无高危（衔接红队 skill）",
        "合规核查：数据/标识/出境/条款",
        "分配资产 ID，写入台账，状态=开发中",
    ],
    "launch": [
        "上线审批（工程+安全+合规+业务）",
        "版本快照（模型+Prompt+知识库+配置）",
        "灰度发布（5%-10% 流量）",
        "观察指标 vs 基线（忠实度/满意度/报错率）",
        "放量/回滚决策，台账状态=已上线",
    ],
    "monitor": [
        "每周评测集回归（质量指标 vs 基线）",
        "业务指标监控（满意度/转人工/投诉）",
        "数据/概念漂移检测",
        "成本监控（月度预算/异常增长）",
        "告警响应流程（检测→诊断→处置→复盘）",
    ],
    "retire": [
        "确认替代方案（迁移目标明确）",
        "通知业务方（无依赖确认）",
        "数据合规处置（个人数据按法规）",
        "停流量→停服务→台账更新=已退役",
        "归档：退役原因+替代资产+评测记录",
    ],
}

DRIFT_POINTS = [
    ("业务指标", "满意度/转化/投诉/转人工率（环比上涨 >20% 告警）"),
    ("质量指标", "每周评测集回归 vs 基线（下跌 >5% 告警）"),
    ("输入漂移", "输入分布统计（主题/长度/语言变化）"),
    ("输出特征", "长度/格式/拒答率变化"),
    ("告警分级", "预警（观察）/ 告警（处置）/ 严重（立即回滚）"),
    ("响应流程", "检测→诊断（数据/概念/模型漂移）→定位→处置→复盘"),
]

COST_POINTS = [
    ("成本核算", "单次=输入Token×单价+输出Token×单价；月=Σ场景调用×单次"),
    ("分场景核算", "每业务场景/每模型单列，找成本大头"),
    ("预算控制", "70% 预警 / 80% 告警 / 100% 熔断"),
    ("路由分层", "简单任务用轻量模型（可省 30-60%）"),
    ("Prompt 瘦身", "精简上下文，去冗余指令（省输入 Token）"),
    ("缓存复用", "高频相似请求缓存（前缀/结果缓存）"),
    ("蒸馏部署", "高频固定任务用蒸馏小模型（需质量验证）"),
    ("异常检测", "单日成本突增 >50% 告警（查配置/流量异常）"),
]


def cmd_inventory(args):
    print("=" * 60)
    print("AI 资产盘点清单（五类资产）：")
    for i, (name, detail) in enumerate(INVENTORY_ITEMS, 1):
        print(f"{i}. {name}：{detail}")
    return 0


def cmd_modelcard(args):
    print("=" * 60)
    print("模型卡（Model Card）模板：")
    print(MODELCARD_TEMPLATE)
    return 0


def cmd_lifecycle(args):
    if args.phase not in LIFECYCLE:
        print("错误：--phase 仅支持 register / launch / monitor / retire。")
        return 2
    print("=" * 60)
    print(f"阶段：{args.phase}　生命周期检查：")
    for i, item in enumerate(LIFECYCLE[args.phase], 1):
        print(f"{i}. {item}")
    return 0


def cmd_drift(args):
    print("=" * 60)
    print("漂移监控要点（三类漂移：数据/概念/模型）：")
    for i, (name, detail) in enumerate(DRIFT_POINTS, 1):
        print(f"{i}. {name}：{detail}")
    return 0


def cmd_cost(args):
    print("=" * 60)
    print("成本治理清单（AI FinOps）：")
    for i, (name, detail) in enumerate(COST_POINTS, 1):
        print(f"{i}. {name}：{detail}")
    return 0


def main():
    p = argparse.ArgumentParser(description="AI 模型资产管理（LLMOps）本地工具（零依赖）")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("inventory", help="资产盘点清单")

    sub.add_parser("modelcard", help="模型卡模板")

    p_life = sub.add_parser("lifecycle", help="生命周期检查")
    p_life.add_argument("--phase", required=True, choices=["register", "launch", "monitor", "retire"])

    sub.add_parser("drift", help="漂移监控要点")
    sub.add_parser("cost", help="成本治理清单")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return 0
    fn = {"inventory": cmd_inventory, "modelcard": cmd_modelcard,
          "lifecycle": cmd_lifecycle, "drift": cmd_drift, "cost": cmd_cost}[args.cmd]
    return fn(args)


if __name__ == "__main__":
    sys.exit(main())
