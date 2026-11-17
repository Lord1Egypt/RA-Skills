# -*- coding: utf-8 -*-
"""AI 可观测性与生产监控 - 本地工具（零依赖，Python 标准库）

命令：
  pillars 三大支柱要点
  metrics 核心监控指标
  alert   告警设计（分级）
  trace   调用追踪规范
  plan    落地路线
"""
import argparse
import sys

PILLARS = [
    ("日志 Logs", "事件记录：调用日志（脱敏）、错误日志、护栏拦截日志"),
    ("指标 Metrics", "聚合统计：质量/性能/成本/安全指标（实时看板）"),
    ("追踪 Traces", "调用链：一次回答从请求到返回的全链路（Span 设计）"),
    ("AI 扩展", "模型行为（幻觉/拒答）、Token 成本、护栏命中、Prompt 状态"),
    ("分层设计", "L0 基础设施 / L1 应用 / L2 AI 层（重点）/ L3 业务"),
]

METRICS = [
    ("质量", "幻觉率、拒答率、转人工率、满意度、质量评分、截断率"),
    ("性能", "TTFT、TPS、P50/P95/P99 延迟、超时率、限流率"),
    ("成本", "单次日/月成本、分场景成本、分模型成本、Token 结构"),
    ("安全", "护栏命中率、注入检测数、越狱成功率、敏感泄漏数、有害输出率"),
    ("业务", "会话数、满意度、转化率、留存（与业务共建）"),
]

ALERTS = [
    ("分级", "P1 严重（立即响应）/ P2 告警（小时级）/ P3 预警（天级）"),
    ("幻觉率", ">3% 告警，>5% 严重（高危场景收紧）"),
    ("敏感泄漏", "输出含个人信息 >0 即 P1（红线）"),
    ("错误率", ">1% 预警，>3% 告警"),
    ("延迟", "P95 超 SLO 100% 告警"),
    ("成本突增", "日成本突增 >50% 告警（先止血再查因）"),
    ("护栏失效", "命中率突降 >30% 告警"),
    ("治理", "阈值月度校准、去重聚合、分级通知、每周复盘防疲劳"),
]

TRACE = [
    ("会话 ID", "一次用户会话贯穿多次调用的关联键"),
    ("Span 设计", "request / prompt_build / model_call / guardrail / postprocess / response"),
    ("必记字段", "时间戳/会话ID/请求ID/场景ID/模型版本/Prompt版本/输入输出摘要/Tokens/耗时/结果码"),
    ("敏感过滤", "输入输出脱敏（手机号/身份证/姓名/病历），哈希/掩码/截断"),
    ("采样策略", "全量摘要 + 详情抽样（10%）+ 异常与安全问题全量"),
    ("可回溯", "从用户投诉反查到具体会话与版本（支持排查）"),
]

PLAN = [
    ("1-30 天", "定指标与 SLO；搭追踪与指标基础设施（OpenTelemetry + Prometheus/Grafana）；核心场景埋点"),
    ("31-60 天", "建看板（质量/性能/成本）；定告警规则与 runbook；护栏监控上线"),
    ("61-90 天", "抽样复核流程；灰度监控与发布门禁打通；告警复盘机制；季度校准"),
]


def cmd_pillars(args):
    print("=" * 60)
    print("可观测性三大支柱 + AI 扩展：")
    for i, (name, detail) in enumerate(PILLARS, 1):
        print(f"{i}. {name}：{detail}")
    return 0


def cmd_metrics(args):
    print("=" * 60)
    print("核心监控指标（五类）：")
    for i, (name, detail) in enumerate(METRICS, 1):
        print(f"{i}. {name}：{detail}")
    return 0


def cmd_alert(args):
    print("=" * 60)
    print("告警设计（分级 + 核心规则）：")
    for i, (name, detail) in enumerate(ALERTS, 1):
        print(f"{i}. {name}：{detail}")
    return 0


def cmd_trace(args):
    print("=" * 60)
    print("调用追踪规范：")
    for i, (name, detail) in enumerate(TRACE, 1):
        print(f"{i}. {name}：{detail}")
    return 0


def cmd_plan(args):
    print("=" * 60)
    print("落地路线（90 天）：")
    for i, (phase, detail) in enumerate(PLAN, 1):
        print(f"{i}. {phase}：{detail}")
    return 0


def main():
    p = argparse.ArgumentParser(description="AI 可观测性与生产监控本地工具（零依赖）")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("pillars", help="三大支柱要点")
    sub.add_parser("metrics", help="核心监控指标")
    sub.add_parser("alert", help="告警设计")
    sub.add_parser("trace", help="调用追踪规范")
    sub.add_parser("plan", help="落地路线")
    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return 0
    fn = {"pillars": cmd_pillars, "metrics": cmd_metrics, "alert": cmd_alert,
          "trace": cmd_trace, "plan": cmd_plan}[args.cmd]
    return fn(args)


if __name__ == "__main__":
    sys.exit(main())
