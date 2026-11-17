#!/usr/bin/env python3
"""collect_usage_data.py — WorkBuddy Agent 使用数据采集器

从多个数据源采集 Agent 使用情况：
  1. traces/       — token 消耗、模型信息、会话时长
  2. workbuddy.db  — 会话元数据、自动化运行记录、信用消耗
  3. usage-log.json — 技能使用记录、活跃天数
  4. WorkBuddy/    — 会话产出文件、记忆日志
  5. automation API — 自动化任务配置

用法:
  python collect_usage_data.py [--days N] [--output data.json]
  默认采集最近 7 天数据，输出到 stdout

注意：本文件是 CLI 编排入口 + facade，实际实现分布在
ca_core.py / ca_sources.py / ca_sessions.py / ca_aggregate.py，由本文件统一编排并 re-export。
"""

import argparse
import calendar
import json
import os
import re
import sqlite3
import sys
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone, date
from pathlib import Path
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# 技能根目录（scripts/ 的上一级），用于导入 adapters/ 下的多 Agent 数据源适配器
_SKILL_ROOT = os.path.dirname(_HERE)
if _SKILL_ROOT not in sys.path:
    sys.path.insert(0, _SKILL_ROOT)

from ca_core import (
    ALL_CUSTOM_MODELS,
    ALL_LOCAL_MODELS,
    ALL_ROUTER_MODELS,
    CACHE_DISCOUNT,
    CUSTOM_LOCAL_PRICING,
    DB_PATH,
    DEFAULT_BLENDED_PER_MILLION,
    DEFAULT_MODEL,
    DELISTED_MODELS,
    DISCOVERED_EXTERNAL,
    DISCOVERED_LOCAL,
    DISCOVERED_ROUTER,
    DISPLAY_MERGE,
    GLM52_FAMILY,
    GLM52_RATE,
    HOME,
    LOW_CONFIDENCE,
    LOW_CONFIDENCE_BIAS,
    MEDIA_EXTS,
    MODEL_PRICING,
    MODE_RATES_META,
    ORPHAN_KEY,
    ORPHAN_LABEL,
    PERIOD_DAYS,
    PERIOD_LABELS,
    PERIOD_NEXT,
    PERIOD_SHORT,
    PER_MILLION,
    PROJECTS_DIR,
    ROUTER_ALIASES,
    ROUTER_HOSTS,
    ROUTER_VENDORS,
    SCHEDULED_PRICING,
    SESSIONS_DIR,
    SILICONFLOW_VENDOR_PREFIXES,
    SYSTEM_REMINDER_RE,
    TASK_RULES_PATH,
    TASK_TYPE_RULES,
    TIER_ALIASES,
    TIER_CANON,
    TIER_LABELS,
    TIMED_FREE,
    TRACES_DIR,
    TZ,
    UNNAMED_LABEL,
    USAGE_LOG_PATH,
    USER_CUSTOM_MODELS,
    WB_DIR,
    WORKBUDDY_SESSIONS,
    _CHEAPER_ALT,
    _PRICING,
    _PRICING_LOCAL_LOADED,
    _build_sid_to_title,
    _load_acc_product_config,
    _load_pricing_config,
    _to_num,
    call_time_of,
    canonical_tier,
    compute_cost,
    discover_custom_models,
    effective_tokens_of,
    glm52_discount_multiplier,
    is_router_like,
    is_scheduled_free,
    is_timed_free,
    iso_to_date,
    iso_to_dt,
    load_task_rules,
    low_confidence_reason,
    low_confidence_bias,
    merge_display_key,
    normalize_model,
    parse_channel,
    parse_date_range,
    price_of,
    resolve_date_range,
    resolve_model,
    score_task_types,
    token_active_session_ids,
    trace_cost,
    ts_to_date,
    ts_to_dt,
    _router_avg_unit_price,
)
from ca_sources import (
    _extract_text_from_parts,
    _find_session_jsonl,
    _recover_model_info_from_spans,
    _transform_cwd,
    collect_db_data,
    collect_session_outputs,
    collect_skill_usage,
    collect_traces,
    get_session_artifact_fingerprint,
    get_session_content,
)
from ca_sessions import (
    aggregate_task_token_stats,
    aggregate_top_tasks,
    classify_task,
    collect_task_types,
)
from ca_aggregate import (
    _detect_daily_anomalies,
    _detect_session_anomalies,
    _fmt_anom_val,
    _normalize_model_key,
    _percentile,
    aggregate_by_exec_model,
    aggregate_by_model,
    aggregate_by_session,
    aggregate_by_tier,
    aggregate_traces_by,
    build_savings_insights,
    build_savings_insights_from_official,
    detect_cost_anomalies,
)

# 绑定子模块名，便于测试按「真实定义模块」定位 monkeypatch（拆分后需要）
import ca_core
import ca_sources
import ca_sessions
import ca_aggregate


def _decide_cost_mode(
    requested,
    unconfigured,
    configured_rows,
    total_cost,
    total_effective_cost,
    has_official,
):
    """判定本次报告的计价模式，返回 "priced" 或 "tokens_only"。

    priced      ：照常输出金额（默认，历史行为）
    tokens_only ：整份报告隐藏计费维度，只讲 Token / 调用 / 耗时 / 任务
    auto（默认）：只要「没有任何可计价的模型」就自动切 tokens_only——覆盖两类数据形态：
      ① 读到了模型调用数据，但全部未配置单价；② 连模型数据都读不到（如只产出聚合 token 的源）。
      适配一切无计费能力的 Agent（千问办公、百度搭子等），不依赖每适配器写死标志位。
      三条边界必须分清，否则会误删合法内容：
      ① 限免 / 本地模型的 ¥0.00 是**已配置单价**算出来的真实结果（configured_rows 非空），
         不是「没价可算」，绝不能因此删掉成本章节；
      ② 已导入官方积分导出（L1 真值）时金额来自账单，与静态价表是否命中无关；
      ③ 只有「有未配置单价的模型 + 无任何已配置行 + 总额为 0」同时成立，
         报告才会满屏 ¥0.00 与「未配置」——这时藏起来比摊开更诚实。
    """
    if requested == "tokens-only":
        return "tokens_only"
    if requested == "priced":
        return "priced"
    # auto 决策：只认「有没有可计价的模型」，与具体是哪个适配器无关。
    #   has_priced_model = 有已配置单价的模型，或存在官方账单（L1 真值，永远有金额）
    #   任一为真 → 照常 priced；都为假且本期金额为 0 → tokens_only。
    # 这把两种无计费形态一并兜住（不再依赖 `unconfigured` 是否为空这个易漏的判据）：
    #   ① unconfigured 非空、configured_rows 空（读到模型但全未配价）
    #   ② unconfigured 与 configured_rows 都空（连模型数据都读不到）
    # 限免 / 本地模型那种「单价已配置且合法为 ¥0.00」仍算 configured_rows 非空，不误判
    # （见 test_legit_zero_cost_stays_priced）。
    has_priced_model = bool(configured_rows) or has_official
    zero_everywhere = not ((total_cost or 0) > 0 or (total_effective_cost or 0) > 0)
    if not has_priced_model and zero_everywhere:
        return "tokens_only"
    return "priced"


def build_task_classifier_with_consent(args, _stderr=None):
    """按 --task-classifier 与出站确认门禁构造任务分类器（TP4 合规）。

    仅当 args.task_classifier == "llm" 且显式确认（--task-classifier-llm-ack
    或环境变量 AAR_TASK_LLM_ACK=1）时，才构建会将会话派生文本外传的 LLM 分类器；
    否则返回 None，调用方据此走内置加权启发式、零出站。

    默认离线路径（heuristic）完全不受影响：直接返回 None，不打印任何警告。
    """
    if args.task_classifier != "llm":
        return None
    endpoint = args.task_llm_endpoint
    ack = bool(getattr(args, "task_classifier_llm_ack", False)) or \
        os.environ.get("AAR_TASK_LLM_ACK") == "1"
    stderr = _stderr if _stderr is not None else sys.stderr
    if not ack:
        print(
            "[WARN] ⚠ 出站传输未确认：--task-classifier llm 本会把会话派生文本"
            "（会话标题 / 对话内容摘要等）\n"
            f"       发送至你提供的端点 {endpoint or '(未提供)'}，该内容会离开本机。\n"
            "       未检测到 --task-classifier-llm-ack 或 AAR_TASK_LLM_ACK=1，"
            "已自动回退本地启发式分类，不做任何出站传输。",
            file=stderr,
        )
        return None
    print(
        "[WARN] ⚠ 已确认出站：--task-classifier llm 将把会话派生文本"
        f"（会话标题 / 对话内容摘要等）发送至端点 {endpoint}（该内容会离开本机）。",
        file=stderr,
    )
    try:
        from task_classifier_llm import build_llm_classifier

        return build_llm_classifier(
            endpoint,
            args.task_llm_model,
            api_key=args.task_llm_api_key,
        )
    except (ValueError, ImportError) as e:
        print(f"[WARN] LLM 分类器不可用（{e}），回退加权启发式", file=stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="WorkBuddy Agent 使用数据采集器")
    parser.add_argument(
        "--period",
        choices=["day", "week", "month", "year"],
        default="week",
        help="时间窗口预设：day=今天 / week=最近7天 / month=最近30天 / year=最近365天（默认 week）",
    )
    parser.add_argument(
        "--days", type=int, help="自定义滚动天数，覆盖 --period（如 --days 14）"
    )
    parser.add_argument(
        "--start", type=str, help="绝对起始日期 YYYY-MM-DD（与 --end 搭配）"
    )
    parser.add_argument(
        "--end", type=str, help="绝对结束日期 YYYY-MM-DD（与 --start 搭配）"
    )
    parser.add_argument(
        "--output", "-o", type=str, help="输出 JSON 文件路径（默认 stdout）"
    )
    parser.add_argument(
        "--realtime", action="store_true", help="实时采集模式（立即采集最新数据）"
    )
    parser.add_argument(
        "--lookup-pricing",
        choices=["offline", "online"],
        default="offline",
        help="缺失单价模型的处理：offline=仅提示如何补写（默认，纯本地）；"
        "online=尝试联网检索（需 --pricing-api 指向你自己的定价镜像，"
        "否则仅生成可点击的搜索链接）。联网结果一律标注「网络估算价，仅供参考」",
    )
    # 安全边界：--pricing-api 只接受用户显式传入的 URL，不内置任何默认端点；
    # 不传则完全离线。URL 仅来自命令行参数，绝不接受从 trace / 会话内容派生的 URL（防 SSRF）。
    parser.add_argument(
        "--pricing-api",
        type=str,
        default=None,
        help='online 模式可选：指向一个返回 {"models": {模型名: {input,output}}} 的 JSON 端点，'
        "用于补全缺失模型单价（取自你自己的定价镜像，避免抓第三方页面）",
    )
    parser.add_argument(
        "--source",
        choices=["workbuddy", "claude-code", "codex", "qwenwork", "dumate"],
        default="workbuddy",
        help="数据源：workbuddy=默认（WorkBuddy traces/workbuddy.db/usage-log），"
        "claude-code=读取 ~/.claude/projects/ 下的 Claude Code 会话 JSONL（P2-1 适配器 MVP）。"
        "claude-code 模式无需 WorkBuddy 环境，成本按 pricing.json 中 Claude 模型估算价计算。"
        "codex=读取 ~/.codex/sessions/ 下的 OpenAI Codex CLI rollout JSONL，"
        "无需 WorkBuddy 环境，成本按 pricing.json 中 OpenAI 模型估算价计算。"
        "qwenwork=读取千问办公（~/.qwenworkcn/projects 转录 + logs/runs 调用日志 + "
        "agents.db 会话元信息），无需 WorkBuddy 环境；"
        "千问办公上游不回传 token，故 token 为字符估算、成本未计价；"
        "dumate=百度搭子（DuMate）数据源：读 ~/.workbuddy/（与 WorkBuddy 同布局），"
        "可用 DUMATE_HOME 环境变量覆盖数据目录",
    )
    parser.add_argument(
        "--cost-mode",
        choices=["auto", "tokens-only", "priced"],
        default="auto",
        help="计费维度：auto=默认，本期**一个单价都没命中**时自动切 tokens_only；"
        "tokens-only=强制整份报告隐藏金额（只讲 Token / 调用 / 耗时 / 任务），"
        "适合按积分订阅计费、没有公开单 token 刊例价的数据源（如千问办公）；"
        "priced=无论如何都按现状输出金额（与历史行为一致）。"
        "注意：限免 / 本地模型那种「单价已配置且合法为 0」的情况不会被 auto 误判",
    )
    parser.add_argument(
        "--task-classifier",
        choices=["heuristic", "llm"],
        default="heuristic",
        help="任务类型分类器：heuristic=默认加权启发式（离线、零依赖）；"
        "llm=可选增强，须同时提供 --task-llm-endpoint（本地 Ollama 或自有 OpenAI 兼容端点），"
        "调用失败自动回退启发式",
    )
    # 安全边界：--task-llm-endpoint 只接受用户显式传入的 URL，不内置任何默认端点；
    # 不传则完全离线。URL 仅来自命令行参数，绝不接受从 trace / 会话内容派生的 URL（防 SSRF）。
    parser.add_argument(
        "--task-llm-endpoint",
        type=str,
        default=None,
        help="LLM 分类器的 OpenAI 兼容 /v1 根地址（如本地 Ollama http://localhost:11434/v1）",
    )
    parser.add_argument(
        "--task-llm-model",
        type=str,
        default=None,
        help="LLM 分类器使用的模型名（如本地 Ollama 的 qwen2.5:7b）",
    )
    parser.add_argument(
        "--task-llm-api-key",
        type=str,
        default=None,
        help="LLM 端点的 API Key（本地端点可省略）",
    )
    parser.add_argument(
        "--task-classifier-llm-ack",
        action="store_true",
        default=False,
        help="确认启用 --task-classifier llm 的出站传输：会话派生文本将被发送至你提供的"
        "自有端点（OpenAI 兼容）。未设置时，即便传了 --task-classifier llm 也只走本地启发式、"
        "不做任何出站传输。也可设置环境变量 AAR_TASK_LLM_ACK=1 等效确认。",
    )
    parser.add_argument(
        "--import-official",
        type=str,
        default=None,
        metavar="XLSX",
        help="导入官方用量导出（官网下载的 request-usage-*.xlsx），作为**成本真值（L1）**对账源。"
        "纯本地只读解析，不联网、不上传。不传时成本为静态价表估算（L2）。"
        "仅支持 --source workbuddy",
    )
    parser.add_argument(
        "--official-sheet",
        type=str,
        default=None,
        help="官方导出工作表名（默认取第一个工作表；官方固定为 'Usage Details'）",
    )
    args = parser.parse_args()

    # 官方导出只对 WorkBuddy 源有意义：claude-code / codex 没有官方积分账单可对
    if args.import_official and args.source != "workbuddy":
        print(
            f"[ERROR] --import-official 仅支持 --source workbuddy（当前 --source {args.source}）",
            file=sys.stderr,
        )
        sys.exit(2)

    if args.realtime:
        # 实时模式：立即采集最新数据（今天）
        start_date, end_date, period_key, period_label = resolve_date_range(
            period="day"
        )
        print(
            f"[INFO] 实时模式：采集范围 {start_date} ~ {end_date}（当日）",
            file=sys.stderr,
        )
    else:
        # 记录显式指定的参数，用于提示用户实际生效的参数
        explicit_params = []
        if args.start and args.end:
            explicit_params.append("--start/--end")
        if args.days is not None:
            explicit_params.append(f"--days {args.days}")
        if (
            args.period != "week" or explicit_params
        ):  # 只有显式指定了非默认值，或其他参数覆盖时才提示
            if args.period != "week" and not (args.days or args.start):
                explicit_params.append(f"--period {args.period}")

        try:
            start_date, end_date, period_key, period_label = resolve_date_range(
                period=args.period, days=args.days, start=args.start, end=args.end
            )
        except ValueError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(2)

        # 详细提示：显式指定参数 vs 默认值
        if explicit_params:
            print(
                f"[INFO] 采集范围[{period_label}]：{start_date} ~ {end_date}（生效参数：{', '.join(explicit_params)}）",
                file=sys.stderr,
            )
        else:
            print(
                f"[INFO] 采集范围[{period_label}]：{start_date} ~ {end_date}（默认一周，可用 --period/--days/--start/--end 自定义）",
                file=sys.stderr,
            )

    # 任务分类器：默认启发式零依赖、完全离线；
    # --task-classifier llm 仅在显式确认出站（--task-classifier-llm-ack / AAR_TASK_LLM_ACK=1）
    # 时才构建会外传文本的 LLM 分类器，否则自动回退本地启发式（TP4 合规）。
    task_classifier = build_task_classifier_with_consent(args)

    # 该数据源是否在语义上支持计费维度（默认支持；qwenwork 源会置 False）
    cost_supported = True
    # 数据源自己声明的 meta 补充（single_channel / background_runs / 采集来源标注等），
    # 由适配器算好、这里整体并入 result["meta"]，避免每加一个源就改一次 meta 字面量
    source_meta = {}

    # 采集各数据源：先取会话（sessions.model 含带通道前缀的原始模型标识符，
    # 是「接口通道」的真相源），据其构建 session_id→raw_model 映射，再采集 trace 并关联通道。
    if args.source == "claude-code":
        # ── Claude Code 数据源（P2-1 适配器 MVP）──
        # 无需 WorkBuddy 环境，直接读 ~/.claude/projects/ 下的会话 JSONL；
        # 适配器产出与 WorkBuddy 同源的 trace / sessions，任务类型已预分类。
        from adapters.claude_code import collect_claude_code

        traces, db_data = collect_claude_code(start_date, end_date)
        sid_to_rawmodel = {
            s["id"]: (s.get("model") or "default") for s in db_data["sessions"]
        }
        skill_usage = {"skills": {}, "active_days": sorted({t["date"] for t in traces})}
        outputs, memory_logs = ([], {})
        # 适配器已基于对话文本预分类 task_type（复用 classify_task，与 WorkBuddy 同源）；
        # 若启用 LLM 分类器则基于 _dialogue_text 重分类，否则直接收口预分类结果。
        if task_classifier is not None:
            task_types = collect_task_types(
                db_data["sessions"], classifier=task_classifier
            )
        else:
            task_types = {
                s["id"]: s.get("task_type", "其他") for s in db_data["sessions"]
            }
        print(
            f"[INFO] Claude Code 数据源：{len(traces)} 条 trace / {len(db_data['sessions'])} 个会话",
            file=sys.stderr,
        )
    elif args.source == "codex":
        # ── OpenAI Codex CLI 数据源 ──
        # 无需 WorkBuddy 环境，直接读 ~/.codex/sessions/ 下的 rollout JSONL（按日期分目录）；
        # 适配器产出与 WorkBuddy 同源的 trace / sessions，任务类型已预分类。
        from adapters.codex import collect_codex

        traces, db_data = collect_codex(start_date, end_date)
        sid_to_rawmodel = {
            s["id"]: (s.get("model") or "default") for s in db_data["sessions"]
        }
        skill_usage = {"skills": {}, "active_days": sorted({t["date"] for t in traces})}
        outputs, memory_logs = ([], {})
        # 适配器已基于对话文本预分类 task_type（复用 classify_task，与 WorkBuddy 同源）；
        # 若启用 LLM 分类器则基于 _dialogue_text 重分类，否则直接收口预分类结果。
        if task_classifier is not None:
            task_types = collect_task_types(
                db_data["sessions"], classifier=task_classifier
            )
        else:
            task_types = {
                s["id"]: s.get("task_type", "其他") for s in db_data["sessions"]
            }
        print(
            f"[INFO] Codex CLI 数据源：{len(traces)} 条 trace / {len(db_data['sessions'])} 个会话",
            file=sys.stderr,
        )
    elif args.source == "qwenwork":
        # ── 千问办公（QwenWork）数据源 ──
        # 无需 WorkBuddy 环境：读 ~/.qwenworkcn/projects 转录 + logs/runs 调用日志 +
        # agents.db 会话元信息。千问办公上游不回传 token（实测 1167 条
        # model.response.completed 的四个 token 字段全为 0），故 token 为字符估算、
        # 档位无公开刊例价 → 成本不计价；调用次数 / 耗时 / 标题 / 档位为真实值。
        from adapters.qwenwork import collect_qwenwork, SUPPORTS_COST

        # 能力声明（不是「这次恰好没单价」）：千问办公在语义上不支持计费维度，
        # 报告端据此压制「缺失单价 + 补价 stub」整块。见 generate_report._show_unconfigured_block
        cost_supported = SUPPORTS_COST
        traces, db_data = collect_qwenwork(start_date, end_date)
        sid_to_rawmodel = {
            s["id"]: (s.get("model") or "default") for s in db_data["sessions"]
        }
        skill_usage = db_data.get("skill_usage") or {
            "skills": {},
            "active_days": sorted({t["date"] for t in traces}),
        }
        outputs = db_data.get("outputs") or []
        # memory_logs 保持空：千问办公的记忆写进 awareness/*.md（由 file-history 快照承载），
        # 没有 WorkBuddy 那种「按日期归集的会话记忆日志目录」可映射，硬凑会造假结构。
        memory_logs = {}
        source_meta.update(db_data.get("_meta") or {})
        if task_classifier is not None:
            task_types = collect_task_types(
                db_data["sessions"], classifier=task_classifier
            )
        else:
            task_types = {
                s["id"]: s.get("task_type", "其他") for s in db_data["sessions"]
            }
        _est = sum(1 for t in traces if t.get("_tokens_estimated"))
        print(
            f"[INFO] 千问办公数据源：{len(traces)} 条 trace / "
            f"{len(db_data['sessions'])} 个会话"
            f"（{_est}/{len(traces)} 条 token 为字符估算，档位无刊例价故未计价）",
            file=sys.stderr,
        )
    elif args.source == "dumate":
        # ── 百度搭子（DuMate）数据源 ──
        # 百度搭子桌面客户端（qianfan-desktop-app）的数据落点与 WorkBuddy
        # 完全一致（~/.workbuddy：traces/ + workbuddy.db + usage-log.json +
        # 会话目录），因此适配器复用同一采集链路，仅显式声明数据源身份，
        # 并支持 DUMATE_HOME 环境变量覆盖数据目录（测试 / 多账号 / 未来迁移）。
        from adapters.dumate import collect_dumate, SUPPORTS_COST, DUMATE_HOME

        # 能力声明：百度搭子与 WorkBuddy 同布局，token 为上游真值 -> 支持计费
        cost_supported = SUPPORTS_COST
        traces, db_data = collect_dumate(start_date, end_date)
        sid_to_rawmodel = {
            s["id"]: (s.get("model") or "default") for s in db_data["sessions"]
        }
        skill_usage = db_data.get("skill_usage") or {
            "skills": {},
            "active_days": sorted({t["date"] for t in traces}),
        }
        outputs = db_data.get("outputs") or []
        memory_logs = db_data.get("memory_logs") or {}
        # 任务类型：与 WorkBuddy 源同一条路径（collect_task_types，默认启发式加权），
        # 有 LLM 分类器时当作 classifier 传入，没有就不传。
        # ⚠️ 不要再走「收口适配器预分类结果」的老路：dumate 适配器不做任何预分类，
        # 会话 dict 里也没有 task_type 键，直接收口会把全部会话塌成「其他」。
        task_types = collect_task_types(db_data["sessions"], classifier=task_classifier)
        source_meta.update(
            {
                "dumate_home": str(DUMATE_HOME),
                # 实测结论：百度搭子默认 home 与 WorkBuddy 同在 ~/.workbuddy 这棵树下，
                # 但并没有往 ~/.workbuddy 写用量数据（db/trace 里无归属字段可区分），
                # 因此只声明「目录布局同源」，不再声称数据可区分。
                "dumate_home_is_workbuddy": True,
            }
        )
        print(
            f"[INFO] 百度搭子数据源：{len(traces)} 条 trace / "
            f"{len(db_data['sessions'])} 个会话"
            f"（数据目录 {DUMATE_HOME}）",
            file=sys.stderr,
        )
    else:
        # ── WorkBuddy 默认数据源 ──
        db_data = collect_db_data(start_date, end_date)
        sid_to_rawmodel = {
            s["id"]: (s.get("model") or "default") for s in db_data["sessions"]
        }
        traces = collect_traces(start_date, end_date, sid_to_rawmodel)

        # 补全会话：窗口内有 trace 但创建于窗口外的会话，确保 token 统计能关联到任务类型
        try:
            trace_sids = {t.get("session_id") for t in traces if t.get("session_id")}
            existing_ids = {s["id"] for s in db_data["sessions"]}
            missing = trace_sids - existing_ids
            if missing:
                # 只读打开：采集器只读 sessions 表，不需要写权限——可写连接会因 WAL
                # 模式生成/持有 -wal -shm 文件，客户端持锁时读数会抛 SQLITE_BUSY。
                cdb = sqlite3.connect(
                    f"file:{DB_PATH.as_posix()}?mode=ro", uri=True
                )
                try:
                    cdb.row_factory = sqlite3.Row
                    ph = ",".join("?" * len(missing))
                    for r in cdb.execute(
                        f"SELECT * FROM sessions WHERE id IN ({ph}) AND deleted_at IS NULL",
                        list(missing),
                    ).fetchall():
                        db_data["sessions"].append(
                            {
                                "id": r["id"],
                                "cwd": r["cwd"],
                                "title": r["title"] or "",
                                "custom_title": r["custom_title"] or "",
                                "status": r["status"],
                                "created_at": r["created_at"],
                                "created_date": ts_to_date(r["created_at"]),
                                "updated_at": r["updated_at"],
                                "mode": r["mode"],
                                "model": r["model"],
                                "is_background_automation": bool(
                                    r["is_background_automation"]
                                ),
                            }
                        )
                finally:
                    cdb.close()
        except (sqlite3.Error, OSError) as e:
            print(f"[WARN] supplementary sessions query: {e}", file=sys.stderr)

        # 修复：补全会话后，把跨窗口长会话并入 sid_to_rawmodel 并重采 trace——
        # 否则这些会话的 sid 在映射里缺失，raw_model 会退化成 trace 执行模型名，
        # 导致通道误判（如 hy3 网关会话里的 deepseek-v4-pro 被错归、或反之）。
        for s in db_data["sessions"]:
            sid_to_rawmodel.setdefault(s["id"], s.get("model") or "default")
        traces = collect_traces(start_date, end_date, sid_to_rawmodel)

        skill_usage = collect_skill_usage(start_date, end_date)
        outputs, memory_logs = collect_session_outputs(start_date, end_date)

        # 任务类型分类：默认加权启发式；--task-classifier llm 时走可选 LLM 增强
        task_types = collect_task_types(db_data["sessions"], classifier=task_classifier)

    # 汇总
    if args.days is not None:
        meta_days = args.days
    elif args.start and args.end:
        try:
            meta_days = (
                datetime.strptime(args.end, "%Y-%m-%d")
                - datetime.strptime(args.start, "%Y-%m-%d")
            ).days + 1
        except (ValueError, TypeError):
            meta_days = PERIOD_DAYS.get(period_key, 7)
    else:
        meta_days = PERIOD_DAYS.get(period_key, 7)

    result = {
        "meta": {
            "start_date": start_date,
            "end_date": end_date,
            "period": period_key,
            "period_label": period_label,
            "days": meta_days,
            "generated_at": datetime.now(TZ).isoformat(),
            "is_realtime": args.realtime,
            "source": args.source,
            # 成本口径："estimate"=静态价表估算（L2，默认）；
            # 传入 --import-official 后置为 "official"（L1 真值，取官方导出「积分」字段）。
            "cost_source": "estimate",
            # 数据源能力声明（由适配器显式给出）：False 时报告端压制
            # 「缺失单价模型 + pricing.local.json 补价 stub」整块
            "cost_supported": cost_supported,
            # 适配器自行声明的补充 meta（single_channel / background_runs / 采集来源）
            **source_meta,
        },
        "traces": traces,
        "sessions": db_data["sessions"],
        "automation_runs": db_data["automation_runs"],
        "session_credits": db_data["session_credits"],
        "skill_usage": skill_usage,
        "outputs": outputs,
        "memory_logs": {
            k: [{"file": v["file"], "session_dir": v["session_dir"]} for v in vals]
            for k, vals in memory_logs.items()
        },
        "task_types": task_types,
    }

    # token 口径标记：WorkBuddy / claude-code / codex 的 token 是上游回传的真值，
    # 成本才是估算（L2）；千问办公源连 token 都是本地字符估算，
    # 显式落一个 meta 位，避免读者把估算 token 当成账单口径引用。
    if args.source == "qwenwork":
        result["meta"]["tokens_source"] = "estimated"

    # 统计摘要
    total_tokens = sum(t["total_tokens"] for t in traces)
    total_input = sum(t["input_tokens"] for t in traces)
    total_output = sum(t["output_tokens"] for t in traces)
    total_cached = sum(t["cached_tokens"] for t in traces)
    total_effective = sum(t.get("effective_tokens", 0) for t in traces)
    total_credits = sum(c["used"] for c in db_data["session_credits"])
    # 活跃天数 = 窗口内产生 token 活动的日期（仅统计 trace 日期）。
    # 不计入会话创建日：窗口外创建、但窗口内有 trace 的会话已被纳入 token 聚合，
    # 若把其创建日也算进 active_days 会虚高"活跃天数"（如 --days 7 却显示 12 天）。
    active_days = set(t["date"] for t in traces)

    # 计算总成本
    total_cost = sum(t["total_cost"] for t in traces)
    total_input_cost = sum(t["input_cost"] for t in traces)
    total_output_cost = sum(t["output_cost"] for t in traces)
    total_effective_cost = round(sum(t.get("effective_cost", 0.0) for t in traces), 2)

    # 请求数反推（估算）：trace 是 generation 粒度，与官方「请求数」差一个量级
    # （实测约 11.9x）。按 session_id + 时间窗聚类启发式反推「估算请求数」：同一会话内
    # 两次 trace 间隔超过阈值（默认 15 分钟）视为新的用户请求；无 session_id 的 trace
    # 每条算 1 次。这是估算值，口径与官方「请求数」不同，仅用于对照，不等同请求数。
    def _parse_started_at(v):
        """started_at 在多层数据源里格式不统一：WorkBuddy trace 是 Unix 毫秒时间戳，
        claude-code / codex 等适配器是 ISO 8601 字符串。统一解析为带时区 datetime。"""
        if v is None or v == "":
            return None
        if isinstance(v, (int, float)):
            return ts_to_dt(v)
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return None
            try:
                return ts_to_dt(int(s))  # 数值毫秒时间戳
            except ValueError:
                pass
            try:
                return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(
                    timezone(timedelta(hours=8))
                )
            except ValueError:
                return None
        return None

    def _cluster_requests(trs, gap_min=15):
        by_sid = {}
        solo = 0
        for t in trs:
            sid = (t.get("session_id") or "").strip()
            dt = _parse_started_at(t.get("started_at"))
            if not sid or dt is None:
                solo += 1
                continue
            by_sid.setdefault(sid, []).append(dt)
        req = solo
        for dts in by_sid.values():
            dts.sort()
            prev = None
            for d in dts:
                if prev is None or (d - prev).total_seconds() > gap_min * 60:
                    req += 1
                prev = d
        return req

    estimated_request_count = _cluster_requests(traces, gap_min=15)
    # 缓存占比：缓存命中 token 占输入 token 的比例（越高说明越多重复上下文被廉价复用）
    cache_rate = (total_cached / total_input * 100) if total_input else 0

    # —— 计价口径的三个透明度计数（报告据此出文案，勿在渲染层硬编码比例）——
    # 1) 未知模型：raw_model 与 exec_model 都是字面量 "default"，即采集器根本不知道
    #    实际调了哪个模型。这批 cost 已在ca_sources 里强制记 0（不按 DEFAULT_MODEL 编造）。
    unknown_model_traces = sum(1 for t in traces if t.get("is_unknown_model"))
    # 2) 档位名（fast-model 等）：是「路由档位」不是真模型名，单价来自倍率锚定估算。
    #    同时给出按 hy3 刊例价的对照金额，供报告显式标注两种口径的差额。
    tier_traces = [t for t in traces if t.get("is_tier_name")]
    tier_name_cost = round(sum(t.get("total_cost", 0.0) for t in tier_traces), 4)
    tier_alt_hy3_cost = round(
        sum(t.get("alt_hy3_cost") or 0.0 for t in tier_traces), 4)
    # 3) 失败调用：选「单独成列」而非剔除——失败调用同样消耗了 token / 可能计费，
    #    从 token 与成本里剔除会掩盖真实消耗；只在「有效调用」口径里排除，另立 error 列。
    error_traces = sum(1 for t in traces if t.get("is_error"))

    result["summary"] = {
        "total_traces": len(traces),
        # 有效调用 = 总 trace - 失败调用。total_traces 保留原样（历史口径不动），
        # 报告要谈「调用次数」时用total_effective_traces 并同时披露 error_traces。
        "total_effective_traces": len(traces) - error_traces,
        "error_traces": error_traces,
        "unknown_model_traces": unknown_model_traces,
        "total_sessions": len(db_data["sessions"]),
        "total_tokens": total_tokens,
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "total_cached_tokens": total_cached,
        "total_effective_tokens": total_effective,
        "cache_rate": round(cache_rate, 1),
        "total_credits_used": total_credits,
        "active_days": sorted(active_days),
        "active_day_count": len(active_days),
        "total_automation_runs": len(db_data["automation_runs"]),
        "successful_automation_runs": sum(
            1 for r in db_data["automation_runs"] if r["result_success"]
        ),
        "total_outputs": len(outputs),
        "skills_used": len(skill_usage["skills"]),
        "task_type_distribution": {},
        "total_cost": total_cost,
        "total_input_cost": total_input_cost,
        "total_output_cost": total_output_cost,
        "total_effective_cost": round(total_effective_cost, 2),
        # generation 聚类反推的「估算请求数」（口径与官方请求数不同，仅对照用）
        "estimated_request_count": estimated_request_count,
        "request_estimate_gap_minutes": 15,
    }

    # 任务类型分布（D5：仅统计本期**有 token 活动**的会话，避免历史空会话虚高 §5；
    # 与 §一 会话总数补充、§4.2 分布同源 → ca_core.token_active_session_ids）
    _traced_ids = token_active_session_ids(traces)
    for s in db_data["sessions"]:
        if s.get("id") not in _traced_ids:
            continue
        tt = s.get("task_type", "其他")
        result["summary"]["task_type_distribution"][tt] = (
            result["summary"]["task_type_distribution"].get(tt, 0) + 1
        )

    # 任务 token 消耗统计（按任务类型聚合 traces）
    result["task_token_stats"] = aggregate_task_token_stats(traces, db_data["sessions"])

    # Top N 最吃 token 的任务对话框（按会话聚合）
    result["top_tasks"] = aggregate_top_tasks(traces, db_data["sessions"], top_n=10)

    # 按实际执行模型聚合（计费维度 / 账单口径：hy3 路由到的付费模型在此体现，与概览总额一致）→ §3.1
    result["model_stats"] = aggregate_by_exec_model(traces)
    # 按入口 / 配置模型聚合（使用分布维度：auto / hy3 / custom-local 等入口）→ §3.2
    result["model_exec_stats"] = aggregate_by_model(traces)
    # 按档位（路由三档）聚合 → §3.4
    result["tier_stats"] = aggregate_by_tier(traces)

    # ── 官方用量导出（成本真值 L1）──
    # 本地 trace 的静态价表估算（L2）在数学上无法表达「服务端时段减免 / 用户免费额度」，
    # 且存在图像模型 / minimax-m3 等盲区；导入官方导出后，报告切 L1 并以「积分」字段为成本真值。
    # 未导入时保持 L2，输出完全一致（零回归）。
    if args.import_official:
        try:
            from adapters.official_usage import (
                OfficialUsageError,
                collect_official_usage,
                reconcile_with_trace,
            )

            official = collect_official_usage(
                args.import_official,
                start_date=start_date,
                end_date=end_date,
                sheet=args.official_sheet,
            )
        except (OfficialUsageError, ImportError) as e:
            print(f"[ERROR] 官方用量导出导入失败：{e}", file=sys.stderr)
            sys.exit(2)

        # L1 真值模式：§4.4 省钱建议改用官方真实积分（official.by_model），
        # 而非 trace 估算的 effective_cost。官方积分已是成本真值，折扣 / 时段模型给出
        # 「迁走」建议不会误导用户多花钱，故不过滤低置信度（low_confidence_filter=False）。
        # 归并变体（hy3-x→hy3 等）使 §4.4 与 §3.5 对账口径一致。
        result["savings_insights"] = build_savings_insights_from_official(
            official["by_model"], alias_map=dict(DISPLAY_MERGE)
        )

        # 被报告窗口过滤掉的行数（导出通常是「最近30日」，报告窗口可能只有 7 天）
        _all_rows = official["meta"].get("parsed_rows", 0) or 0
        official["meta"]["rows_in_window"] = official["totals"]["requests"]
        official["meta"]["rows_out_of_window"] = max(
            0, _all_rows - official["totals"]["requests"]
        )

        result["official_usage"] = official
        # 官方侧先按 display_merge 归拢（hy3-x → hy3 等），与 trace 侧显示口径对齐。
        # 否则变体会因精确匹配不上而被误判成「trace 盲区」——实测 30 日会虚报 410.95 积分。
        result["reconciliation"] = reconcile_with_trace(
            official, result["model_stats"], alias_map=dict(DISPLAY_MERGE)
        )
        result["meta"]["cost_source"] = "official"
        result["meta"]["official_import"] = {
            "file": official["meta"]["file"],
            "sheet": official["meta"]["sheet"],
            "window": official["meta"]["window"],
            "rows_total": _all_rows,
            "rows_in_window": official["totals"]["requests"],
            "rows_out_of_window": official["meta"]["rows_out_of_window"],
            "columns": sorted(official["meta"]["columns"]),
        }
        result["summary"]["total_cost_official"] = official["totals"]["credits"]
        result["summary"]["official_requests"] = official["totals"]["requests"]
        result["summary"]["official_free_requests"] = official["totals"][
            "free_requests"
        ]
        print(
            f"[INFO] 官方导出已导入：{official['totals']['requests']} 请求 / "
            f"{official['totals']['credits']:.2f} 积分（窗口 {official['meta']['window']['first']}"
            f" ~ {official['meta']['window']['last']}）→ 成本口径 L1 真值",
            file=sys.stderr,
        )
        if official["meta"]["rows_out_of_window"]:
            print(
                f"[WARN] 官方导出共 {_all_rows} 行，其中 "
                f"{official['meta']['rows_out_of_window']} 行不在报告窗口 "
                f"{start_date}~{end_date} 内，已排除",
                file=sys.stderr,
            )
        if official["totals"]["requests"] == 0:
            print(
                f"[WARN] 官方导出在窗口 {start_date}~{end_date} 内没有记录，"
                f"对账章节可能为空",
                file=sys.stderr,
            )

    # 收集本期「未配置单价」的模型名（排除路由别名 auto，其本就无单一单价），供报告给出可补写片段
    unconfigured = set()
    for stats in (result["model_stats"], result["model_exec_stats"]):
        for m in stats:
            # 已下架官方模型不算「缺失单价」——它们本就无需用户补写，仅标注即可
            if (
                not m.get("configured")
                and m.get("model") not in ROUTER_ALIASES
                and not m.get("is_delisted")
            ):
                unconfigured.add(m["model"])
    # 「入口维度」与「执行维度」可能对同一个底层模型各记一次（如 `qwenwork:flash`
    # 与 `flash`），而补价只需在 pricing.local.json 写一条裸名（price_of 会剥通道前缀
    # 查表）→ 一律折成裸名去重，避免报告里出现「flash、qwenwork:flash」这种重复提示。
    unconfigured = {m.split(":", 1)[-1] if ":" in m else m for m in unconfigured}
    result["meta"]["unconfigured_models"] = sorted(unconfigured)
    # 档位名计价口径：fast-model / balanced-model / deep-model 是路由档位而非真模型名，
    # 单价来自 pricing.json 的「倍率锚定法」估算。报告必须显式标注该口径，并同时给出
    # 「按 hy3 刊例价」的对照金额——同一批调用在两种口径下金额不同，不能只报一个数。
    result["meta"]["tier_pricing_basis"] = {
        "note": "档位名（fast-model 等）为路由档位，非真实模型名；单价为倍率锚定估算值",
        "tier_traces": len(tier_traces),
        "tier_cost": tier_name_cost,
        "alt_hy3_cost": tier_alt_hy3_cost,
    }

    cost_mode = _decide_cost_mode(
        requested=args.cost_mode,
        unconfigured=unconfigured,
        configured_rows=[
            m
            for st in (result["model_stats"], result["model_exec_stats"])
            if st
            for m in st
            if m.get("configured")
        ],
        total_cost=total_cost,
        total_effective_cost=total_effective_cost,
        has_official=str(result["meta"].get("cost_source") or "") == "official",
    )
    result["meta"]["cost_mode"] = cost_mode
    if cost_mode == "tokens_only":
        print(
            "[INFO] 计价模式=tokens_only：本期无任何命中单价（未配置："
            + "、".join(sorted(unconfigured)[:6])
            + ("…" if len(unconfigured) > 6 else "")
            + "），报告将隐藏金额维度；要出金额请在 scripts/pricing.local.json 补单价，"
            "或加 --cost-mode priced 强制保留现状。",
            file=sys.stderr,
        )
    # 限时免费截止日（来自 pricing.json 的 timed_free），供报告渲染「限时免费至 X」标签，
    # 避免在渲染器里硬编码日期——用户改了 pricing.json 后标签会自动跟随。
    result["meta"]["timed_free"] = dict(TIMED_FREE)
    # 成本置信度：模型名 -> 「静态估算与实际计费存在系统性偏差」的原因。
    # 供报告把受服务端时段 / 配额减免影响的模型标为低置信度、不参与成本结论。
    # 同样来自 pricing.json（可用 pricing.local.json 覆盖），渲染层不硬编码。
    result["meta"]["low_confidence"] = dict(LOW_CONFIDENCE)
    # 成本置信度偏差方向（机读）：模型名 -> over/under/mixed，供报告渲染 ⚠↑/⚠↓。
    result["meta"]["low_confidence_bias"] = dict(LOW_CONFIDENCE_BIAS)
    # 是否加载了本地定价覆盖（pricing.local.json），供报告透明提示。
    result["meta"]["pricing_local_loaded"] = bool(_PRICING_LOCAL_LOADED)
    # 档位维度元信息：档位估算标记、官方倍率缓存是否生效、最终档位单价表。
    # 供报告 §3.4 透明标注「估算值」并提示可配置。
    result["meta"]["mode_rates"] = dict(MODE_RATES_META.get("rates", {}))
    result["meta"]["mode_cost_estimated"] = bool(
        MODE_RATES_META.get("auto_estimate", False)
    )
    result["meta"]["mode_config_cache_loaded"] = bool(
        MODE_RATES_META.get("config_cache_loaded", False)
    )
    result["meta"]["mode_config_cache_path"] = MODE_RATES_META.get("config_cache_path")
    result["meta"]["mode_config_cache_mtime"] = MODE_RATES_META.get(
        "config_cache_mtime"
    )

    # 可选联网检索（--lookup-pricing online）：仅生成搜索链接，或拉取用户自有定价镜像。
    # ⚠️ 联网拿到的单价一律视为「网络估算价，仅供参考」，绝不用于权威成本总额。
    pricing_lookup = {
        "mode": args.lookup_pricing,
        "api": args.pricing_api,
        "network_estimates": {},
        "search_links": {},
    }
    if args.lookup_pricing == "online" and unconfigured:
        for model in sorted(unconfigured):
            pricing_lookup["search_links"][model] = (
                "https://duckduckgo.com/html/?q="
                + urllib.parse.quote(f"{model} API pricing")
            )
    # ── 安全守卫（防 SSRF + 默认离线）──
    # 仅当用户「显式传入 --pricing-api <URL>」时才拉取**用户自己的**定价镜像；
    # URL 只来自命令行参数，绝不从 trace / 会话内容派生。目标不可达时由
    # fetch_remote_pricing 统一接 urllib 自身异常并优雅降级（修复 SDI-4）。
    if args.lookup_pricing == "online" and args.pricing_api and unconfigured:
        pricing_lookup["network_estimates"] = fetch_remote_pricing(args.pricing_api, unconfigured)
    result["meta"]["pricing_lookup"] = pricing_lookup

    # 成本深度分析：每会话成本 / 省钱杠杆（cost_anomalies 依赖 daily_tokens，在下方构建后计算）
    result["session_stats"] = aggregate_by_session(traces, db_data["sessions"])
    # 省钱洞察基于计费维度（exec_model）找真实付费贵模型，给出更便宜替代与预计月省。
    # L1 真值模式已在上方 import-official 块用官方真实积分构造并写入 savings_insights；
    # 此处仅当尚未构造（L2 估算模式）时补算，避免覆盖 L1 真值版。
    if "savings_insights" not in result:
        result["savings_insights"] = build_savings_insights(result["model_stats"])

    # 每日 token 统计
    daily_tokens = {}
    for t in traces:
        d = t["date"]
        if d not in daily_tokens:
            daily_tokens[d] = {
                "total": 0,
                "input": 0,
                "output": 0,
                "cached": 0,
                "calls": 0,
                "total_cost": 0,
                "input_cost": 0,
                "output_cost": 0,
                "effective": 0,
                "effective_cost": 0,
            }
        daily_tokens[d]["total"] += t["total_tokens"]
        daily_tokens[d]["input"] += t["input_tokens"]
        daily_tokens[d]["output"] += t["output_tokens"]
        daily_tokens[d]["cached"] += t["cached_tokens"]
        daily_tokens[d]["calls"] += t["call_count"]
        daily_tokens[d]["total_cost"] += t["total_cost"]
        daily_tokens[d]["input_cost"] += t["input_cost"]
        daily_tokens[d]["output_cost"] += t["output_cost"]
        daily_tokens[d]["effective"] += t.get("effective_tokens", 0)
        daily_tokens[d]["effective_cost"] += t.get("effective_cost", 0.0)
    result["daily_tokens"] = daily_tokens

    # 成本异常检测（依赖 daily_tokens 与 session_stats，故置于每日统计之后）
    result["cost_anomalies"] = detect_cost_anomalies(
        result["daily_tokens"], result["session_stats"]
    )

    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output_json, encoding="utf-8")
        print(f"[OK] 数据已保存到 {args.output}", file=sys.stderr)
    else:
        print(output_json)


def fetch_remote_pricing(api_url, unconfigured_models, timeout=10):
    """拉取用户自有定价镜像（仅当 --pricing-api 显式传入时调用；默认路径不调用，零网络）。

    返回 {model: {"input": float, "output": float}}；任何网络/解析异常均吞掉并返回空 dict，
    保证目标不可达时优雅降级而非崩溃（修复 SDI-4：原实现 except 只接 requests.RequestException，
    urllib 抛出的 URLError/HTTPError 会逃逸导致采集器崩溃）。URL 只来自命令行参数，不从 trace/
    会话内容派生（防 SSRF）。
    """
    network_estimates = {}
    for model in sorted(unconfigured_models):
        try:
            with urllib.request.urlopen(api_url, timeout=timeout) as resp:
                remote = json.loads(resp.read().decode("utf-8"))
            rm = (
                remote.get("models", {}).get(normalize_model(model))
                or remote.get("models", {}).get(model)
            )
            if rm and "input" in rm and "output" in rm:
                network_estimates[model] = {"input": float(rm["input"]),
                                           "output": float(rm["output"])}
        except (urllib.error.URLError, urllib.error.HTTPError, ValueError, KeyError) as e:
            print(f"[WARN] 联网检索 {model} 失败（已降级，不影响报告）：{e}", file=sys.stderr)
    return network_estimates


if __name__ == "__main__":
    main()
