from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# 强制 stdout/stderr 使用 UTF-8，避免 Windows 默认 codepage 导致中文输出乱码
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from loguru import logger


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

import dataworks_client as client
from acceptance_rate_constants import (
    ASSET_BUCKET_DRAG_ABSOLUTE_THRESHOLD,
    ASSET_BUCKET_DRAG_RELATIVE_THRESHOLD,
    ASSET_FACTOR_TABLE_COLUMNS,
    CAPITAL_BUCKET_TABLE_COLUMNS,
    CAPITAL_TOTAL_DROP_ABSOLUTE_THRESHOLD,
    FACTOR_LABELS,
    FUNDING_CONTRACTION_ABSOLUTE_THRESHOLD,
    FUNDING_CONTRACTION_RELATIVE_THRESHOLD,
    FUNDING_SUPPORTED_FACTORS,
    FUNDING_ENTITY,
    MAIN_ENTITY,
    METRIC_ACCEPTANCE_RATE,
    METRIC_FUNDING_AMOUNT,
    METRIC_ROUTING_AMOUNT,
    METRIC_ROUTING_COUNT,
    MODEL_SET_NAME,
    PRIMARY_CUSTOMER_GROUP_DECLINE_THRESHOLD,
    PRIMARY_GROUP_SLICE_TABLE_COLUMNS,
    PRIMARY_STRUCTURAL_DOMINANCE_THRESHOLD,
    PRIMARY_STRUCTURAL_MEANINGFUL_DECLINE,
    SUPPORTED_GRANULARITIES,
    TARGET_CUSTOMER_GROUPS,
    TERMINAL_REASON_TEXT,
)
DEBUG_LOG_FILE = CURRENT_DIR / "acceptance_rate_analysis_debug.txt"
# 生产默认关闭：不写调试日志文件，stdout JSON 不含 debug_query / funding_debug 等大字段。
# 本地排查可设置环境变量 ACCEPTANCE_RATE_ANALYSIS_DEBUG=1（或 true/yes）开启。
ENABLE_ANALYSIS_DEBUG_OUTPUT = os.getenv("ACCEPTANCE_RATE_ANALYSIS_DEBUG", "").strip().lower() in (
    "1",
    "true",
    "yes",
)
TOKEN_SOURCE_PAGE_URL = "https://data.jirongyunke.net/data-pc-bdopr-fe/hoc-inquiry/index"


def configure_stdio() -> None:
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8")
            except Exception:
                continue


def configure_debug_logging() -> None:
    if not ENABLE_ANALYSIS_DEBUG_OUTPUT:
        return
    DEBUG_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(
        DEBUG_LOG_FILE,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | {name}:{function}:{line} - {message}",
        encoding="utf-8",
        mode="a",
    )
    run_session_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    logger.info("========== 调试会话开始 run_session_id={} log_file={} ==========", run_session_id, str(DEBUG_LOG_FILE))




def log_stage_event(stage: str, event: str, **fields: Any) -> None:
    if fields:
        logger.info(
            "[{}] {} {}",
            stage,
            event,
            json.dumps(fields, ensure_ascii=False, sort_keys=True, default=str),
        )
    else:
        logger.info("[{}] {}", stage, event)


def load_token_from_known_locations() -> str | None:
    """从当前进程可见的环境变量加载 token，未找到时返回 None。"""
    for env_name in (
        "BIGDATA_ACCESS_TOKEN",
        "bigdata_access_token",
        "DATAWORKS_METRIC_QUERY_ACCESS_KEY",
        "dataworks_metric_query_access_key",
    ):
        value = os.getenv(env_name)
        if value:
            return value

    if os.name == "nt":
        persisted_token = _load_token_from_windows_user_environment()
        if persisted_token:
            return persisted_token
    else:
        persisted_token = _load_token_from_unix_profile()
        if persisted_token:
            return persisted_token

    return None


def _set_process_access_token(token: str) -> None:
    os.environ["BIGDATA_ACCESS_TOKEN"] = token


def _broadcast_windows_environment_change() -> None:
    try:
        import ctypes

        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            "Environment",
            SMTO_ABORTIFHUNG,
            5000,
            None,
        )
    except Exception as exc:
        logger.warning("广播 Windows 环境变量变更失败：{}", exc)


def _persist_access_token_windows(token: str) -> None:
    import winreg

    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE) as registry_key:
        winreg.SetValueEx(registry_key, "BIGDATA_ACCESS_TOKEN", 0, winreg.REG_SZ, token)
    _broadcast_windows_environment_change()


def _load_token_from_windows_user_environment() -> str | None:
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ) as registry_key:
            for env_name in (
                "BIGDATA_ACCESS_TOKEN",
                "bigdata_access_token",
                "DATAWORKS_METRIC_QUERY_ACCESS_KEY",
                "dataworks_metric_query_access_key",
            ):
                try:
                    value, _ = winreg.QueryValueEx(registry_key, env_name)
                except FileNotFoundError:
                    continue
                normalized_value = str(value).strip()
                if normalized_value:
                    return normalized_value
    except Exception as exc:
        logger.warning("读取 Windows 用户级环境变量 BIGDATA_ACCESS_TOKEN 失败：{}", exc)
    return None


def _unix_profile_path() -> Path:
    shell_path = os.getenv("SHELL", "")
    shell_name = Path(shell_path).name.lower()
    home_dir = Path.home()
    if shell_name == "zsh":
        return home_dir / ".zshrc"
    if shell_name == "bash":
        return home_dir / ".bashrc"
    return home_dir / ".profile"


def _persist_access_token_unix(token: str) -> None:
    profile_path = _unix_profile_path()
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    if profile_path.exists():
        existing_text = profile_path.read_text(encoding="utf-8")
        lines = existing_text.splitlines()
    else:
        existing_text = ""
        lines = []

    export_line = f"export BIGDATA_ACCESS_TOKEN={shlex.quote(token)}"
    updated_lines: list[str] = []
    replaced = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("export BIGDATA_ACCESS_TOKEN="):
            updated_lines.append(export_line)
            replaced = True
        else:
            updated_lines.append(line)
    if not replaced:
        if updated_lines and updated_lines[-1].strip():
            updated_lines.append("")
        updated_lines.append(export_line)

    new_text = "\n".join(updated_lines)
    if new_text and not new_text.endswith("\n"):
        new_text += "\n"
    if new_text != existing_text:
        profile_path.write_text(new_text, encoding="utf-8")


def _load_token_from_unix_profile() -> str | None:
    profile_path = _unix_profile_path()
    if not profile_path.exists():
        return None

    try:
        lines = profile_path.read_text(encoding="utf-8").splitlines()
    except Exception as exc:
        logger.warning("读取 shell profile 中的 BIGDATA_ACCESS_TOKEN 失败：{}", exc)
        return None

    pattern = re.compile(r"^\s*export\s+BIGDATA_ACCESS_TOKEN=(.+?)\s*$")
    for line in reversed(lines):
        matched = pattern.match(line)
        if not matched:
            continue
        raw_value = matched.group(1).strip()
        try:
            parsed_values = shlex.split(raw_value)
        except ValueError:
            parsed_values = [raw_value.strip("'\"")]
        if parsed_values:
            normalized_value = str(parsed_values[0]).strip()
            if normalized_value:
                return normalized_value
    return None


def persist_access_token_for_future_sessions(token: str) -> None:
    if os.name == "nt":
        _persist_access_token_windows(token)
        return
    _persist_access_token_unix(token)


def persist_access_token(token: str) -> str:
    normalized_token = str(token).strip()
    if not normalized_token:
        return ""

    _set_process_access_token(normalized_token)
    try:
        persist_access_token_for_future_sessions(normalized_token)
    except Exception as exc:
        logger.warning("持久化 BIGDATA_ACCESS_TOKEN 失败，将继续使用当前进程环境变量：{}", exc)
    else:
        logger.info("BIGDATA_ACCESS_TOKEN 已写入当前进程，并持久化到后续新会话可读取的位置。")
    return normalized_token


def resolve_access_token(explicit_token: str | None) -> str:
    """
    解析access token，优先级：
    1. 显式传入的token
    2. 当前终端环境变量中的token
    3. 抛出错误，提示用户从浏览器 Cookie 获取 token 值
    """
    if explicit_token:
        return persist_access_token(explicit_token)

    token = load_token_from_known_locations()
    if token:
        return token

    raise ValueError(
        "未找到 BIGDATA_ACCESS_TOKEN。这个值通常来自浏览器 Cookie `bigdata_access_token`。\n"
        f"1. 打开 {TOKEN_SOURCE_PAGE_URL}\n"
        "2. 按 F12 打开开发者工具，在 Network 中点开任意一个请求\n"
        "3. 在 Cookies / Request Cookies 中找到 `bigdata_access_token`，复制它的值\n"
        "4. 将该值通过命令行参数传入：--access-token <YOUR_TOKEN>；脚本收到显式 token 后会自动写入后续会话可复用的位置\n"
        "5. 或先在环境变量中设置 `BIGDATA_ACCESS_TOKEN`，再执行脚本\n"
        "   - PowerShell: $env:BIGDATA_ACCESS_TOKEN='<YOUR_TOKEN>'\n"
        "   - PowerShell 持久化到新会话: [System.Environment]::SetEnvironmentVariable('BIGDATA_ACCESS_TOKEN', '<YOUR_TOKEN>', 'User')\n"
        "   - Linux / macOS: export BIGDATA_ACCESS_TOKEN='<YOUR_TOKEN>'\n"
        "   - Linux / macOS 持久化到新会话: 将 `export BIGDATA_ACCESS_TOKEN='<YOUR_TOKEN>'` 写入 `~/.bashrc`、`~/.zshrc` 或 `~/.profile`\n"
        "只需要传 `bigdata_access_token` 的值本身，不要把整段 Cookie 请求头一起传入。"
    )




# 第一阶段起，统一改走抽离后的 helper 实现，确保阶段逻辑只依赖外置模块。
from acceptance_rate_support import (
    _aggregate_records,
    _aggregate_slice_map,
    _normalized_metric_rows,
    _project_sensitive_to_factor,
    _query_rows,
    _asset_bucket_decision_reason,
    _asset_factor_decision_reason,
    _build_asset_display,
    _build_asset_display_r12,
    _build_asset_slice_context,
    _build_asset_thresholds,
    _build_capital_bucket_table_markdown,
    _build_capital_display,
    _build_factor_results,
    _build_range_results,
    _bucket_match,
    _current_slice_from_primary,
    _finalize_capital_trace,
    _format_number_or_dash,
    finalize_asset_trace,
    finalize_funding_trace,
    apply_final_attribution_to_funding_trace,
    compute_asset_dimension_pattern,
    compute_asset_raw_volume_gate,
    compute_asset_r12_pattern_info,
    _prepare_asset_records,
    _records_for_factor,
    bold_md,
    bucket_key,
    bucket_label_for_value,
    bucket_value_matches,
    build_capital_total_judgement,
    build_context,
    build_customer_group_judgement,
    build_customer_group_summary_text,
    build_distribution_judgement,
    build_empty_asset_display,
    build_empty_capital_display,
    build_empty_primary_display,
    build_factor_dimension_trace,
    build_funding_dimensions,
    build_funding_rules,
    build_global_progress_line,
    build_main_dimensions,
    build_main_rules,
    build_markdown_table,
    build_period_debug_snapshot,
    build_primary_continue_analysis_scope_markdown,
    build_primary_overall_summary_markdown,
    build_primary_analysis_sequence,
    build_workflow_overview_markdown,
    build_slice_status_summary,
    build_status_line,
    primary_continue_analysis_scope_text,
    build_query_window_label,
    build_reason,
    build_root_cause,
    build_slice_key,
    build_slice_display,
    business_view,
    conclusion_tag_for_reason,
    resolve_slice_index_from_primary,
    status_token_for_reason,
    customer_group_threshold,
    factor_bucket_value,
    factor_label_for_key,
    format_asset_dimension_hit,
    format_amount_human,
    format_bp,
    format_percent,
    format_percent_or_dash,
    format_wan,
    format_wan_or_dash,
    format_yes_no,
    json_dumps,
    normalize_boundary,
    normalize_range_factor_items,
    normalize_cp_dj,
    normalize_funding_kequn_tag,
    normalize_granularity,
    normalize_slice_component,
    normalize_text,
    parse_slice_key,
    parse_age_upper_bound,
    parse_allow_bucket,
    parse_allowed_provinces,
    parse_datetime_text,
    primary_impact_accept_amount_formula_text,
    round_float,
    safe_div,
    select_primary_drill_down_candidates,
    slice_key_matches,
    split_primary_records_by_granularity_bucket,
    stage_analysis_step,
    selected_customer_groups,
    sort_primary_slices,
    time_dimension_name,
    to_float,
    union_time_range,
    unsupported_granularity_error,
    validate_granularity_window,
    weighted_median,
)


def _period_debug_snapshot(
    *,
    current_result: dict[str, Any] | None = None,
    baseline_result: dict[str, Any] | None = None,
    current_filter: str | dict[str, Any] | None = None,
    baseline_filter: str | dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if not ENABLE_ANALYSIS_DEBUG_OUTPUT:
        return None
    return build_period_debug_snapshot(
        current_result=current_result,
        baseline_result=baseline_result,
        current_filter=current_filter,
        baseline_filter=baseline_filter,
    )


def run_primary_stage(
    *,
    granularity: str,
    current_start: str,
    current_end: str,
    baseline_start: str,
    baseline_end: str,
    access_token: str,
    endpoint: str | None = None,
    if_irr: str | None = None,
    cp_dj_new: str | None = None,
) -> dict[str, Any]:
    normalized_granularity = normalize_granularity(granularity)
    time_dimension = time_dimension_name(normalized_granularity)
    target_customer_groups = selected_customer_groups(if_irr)

    logger.info(
        "[run_primary_stage] 开始一级诊断 granularity={} normalized={} "
        "current=[{} ~ {}] baseline=[{} ~ {}] slice_filter=[{}|{}]",
        granularity,
        normalized_granularity,
        current_start,
        current_end,
        baseline_start,
        baseline_end,
        if_irr or "",
        cp_dj_new or "",
    )

    metrics = [
        client.metric(METRIC_ACCEPTANCE_RATE),
        client.metric(METRIC_ROUTING_AMOUNT),
    ]
    dimensions = build_main_dimensions(granularity=normalized_granularity)
    context = build_context(
        granularity=granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )

    if normalized_granularity not in SUPPORTED_GRANULARITIES:
        error = unsupported_granularity_error(normalized_granularity)
        logger.warning(
            "[run_primary_stage] 粒度不支持，终止(R8) normalized_granularity={}",
            normalized_granularity,
        )
        return {
            "context": context,
            "overall": {},
            "analysis_sequence": [],
            "analysis_sequence_lookup": [],
                "customer_group_judgements": [],
            "customer_group_summary_text": "",
            "terminal_reason": "R8",
            "next_action": "stop",
            "drill_down_rule": {},
            "primary_display": build_empty_primary_display(),
            "business_view": business_view(
                headline="当前粒度暂未接入",
                summary="当前版本仅支持日粒度和周粒度的一级诊断。",
                evidence=[f"收到粒度：{normalized_granularity}。"],
            ),
            "errors": [error],
        }

    if not target_customer_groups:
        return {
            "context": context,
            "overall": {},
            "analysis_sequence": [],
            "analysis_sequence_lookup": [],
                "customer_group_judgements": [],
            "customer_group_summary_text": "当前请求的客群不在本技能支持范围内，因此第一阶段停止。",
            "terminal_reason": "R8",
            "next_action": "stop",
            "drill_down_rule": {},
            "primary_display": build_empty_primary_display(),
            "business_view": business_view(
                headline="当前客群不在分析范围内",
                summary="本技能当前只支持 01.惠选客群 与 03.精优客群。",
                evidence=[f"收到客群：{normalize_text(if_irr) or '[未指定]'}。"],
            ),
            "errors": [f"当前客群不在分析范围内：{normalize_text(if_irr) or '[未指定]'}。"],
        }

    current_window_error = validate_granularity_window(normalized_granularity, current_start, current_end)
    baseline_window_error = validate_granularity_window(normalized_granularity, baseline_start, baseline_end)
    if current_window_error or baseline_window_error:
        errors = [item for item in [current_window_error, baseline_window_error] if item]
        logger.warning(
            "[run_primary_stage] 时间窗校验失败，终止(R8) errors={}",
            errors,
        )
        return {
            "context": context,
            "overall": {},
            "analysis_sequence": [],
            "analysis_sequence_lookup": [],
                "customer_group_judgements": [],
            "customer_group_summary_text": "",
            "terminal_reason": "R8",
            "next_action": "stop",
            "drill_down_rule": {},
            "primary_display": build_empty_primary_display(),
            "business_view": business_view(
                headline="一级诊断时间窗不满足当前粒度要求",
                summary="当前时间窗跨越了多个粒度桶，暂时无法直接计算当前期与对比期。",
                evidence=errors,
            ),
            "errors": errors,
        }

    query_start, query_end = union_time_range(
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )
    query_result, query_error = _query_rows(
        access_token=access_token,
        metric_list=metrics,
        dimension_list=dimensions,
        filter_payload=build_main_rules(
            start=query_start,
            end=query_end,
            if_irr=if_irr,
            cp_dj_new=cp_dj_new,
        ),
        endpoint=endpoint,
    )

    if query_error:
        return {
            "context": context,
            "overall": {},
            "analysis_sequence": [],
            "analysis_sequence_lookup": [],
                "customer_group_judgements": [],
            "customer_group_summary_text": "",
            "terminal_reason": "R8",
            "next_action": "stop",
            "drill_down_rule": {},
            "primary_display": build_empty_primary_display(),
            "business_view": business_view(
                headline="当前无法完成一级诊断",
                summary="主数据查询失败，暂时无法判断承接率是否下降。",
                evidence=[query_error],
            ),
            "errors": [query_error],
        }

    all_records = _normalized_metric_rows(
        query_result.get("rows", []),
        [time_dimension, "if_irr", "cp_dj_new"],
    )
    current_records, baseline_records = split_primary_records_by_granularity_bucket(
        records=all_records,
        granularity=normalized_granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )

    if not current_records or not baseline_records:
        errors: list[str] = []
        if not current_records:
            errors.append(
                f"当前周期未匹配到粒度桶 {bucket_key(current_start, granularity=normalized_granularity, is_end=False)} 的数据。"
            )
        if not baseline_records:
            errors.append(
                f"对比周期未匹配到粒度桶 {bucket_key(baseline_start, granularity=normalized_granularity, is_end=False)} 的数据。"
            )
        return {
            "context": context,
            "overall": {},
            "analysis_sequence": [],
            "analysis_sequence_lookup": [],
                "customer_group_judgements": [],
            "customer_group_summary_text": "",
            "terminal_reason": "R8",
            "next_action": "stop",
            "drill_down_rule": {},
            "primary_display": build_empty_primary_display(),
            "business_view": business_view(
                headline="一级诊断数据不足",
                summary="单次查询已完成，但当前周期或对比周期没有匹配到可用于对比的周桶数据。",
                evidence=errors,
            ),
            "errors": errors,
        }

    target_customer_groups_set = set(target_customer_groups)
    current_records = [
        item for item in current_records
        if normalize_text(item.get("if_irr")) in target_customer_groups_set
    ]
    baseline_records = [
        item for item in baseline_records
        if normalize_text(item.get("if_irr")) in target_customer_groups_set
    ]

    overall_current_route_amount = sum(to_float(item.get("route_amount")) for item in current_records)
    overall_baseline_route_amount = sum(to_float(item.get("route_amount")) for item in baseline_records)
    overall_current_accepted_amount = sum(to_float(item.get("accepted_amount")) for item in current_records)
    overall_baseline_accepted_amount = sum(to_float(item.get("accepted_amount")) for item in baseline_records)
    current_rate = safe_div(overall_current_accepted_amount, overall_current_route_amount)
    baseline_rate = safe_div(overall_baseline_accepted_amount, overall_baseline_route_amount)
    overall_delta = current_rate - baseline_rate
    overall_allows_drill_down = overall_delta < 0

    # ── R2 结构迁移分解（Shift-Share Decomposition）──────────────────────────
    # 将大盘承接率变化拆解为：结构效应（路由金额份额变化）+ 性能效应（各切片承接率变化）
    # structural_effect = Σ_i((current_share_i - baseline_share_i) × baseline_rate_i)
    # performance_effect = overall_delta - structural_effect
    def _agg_all_slices(records: list[dict]) -> dict[str, dict]:
        agg: dict[str, dict] = {}
        for rec in records:
            k = f"{normalize_text(rec.get('if_irr'))}|{normalize_text(rec.get('cp_dj_new'))}"
            if k not in agg:
                agg[k] = {"route": 0.0, "accepted": 0.0}
            agg[k]["route"] += to_float(rec.get("route_amount"))
            agg[k]["accepted"] += to_float(rec.get("accepted_amount"))
        for v in agg.values():
            v["rate"] = safe_div(v["accepted"], v["route"])
        return agg

    _cur_slice_agg = _agg_all_slices(current_records)
    _bas_slice_agg = _agg_all_slices(baseline_records)
    _all_slice_keys_r2 = set(_cur_slice_agg) | set(_bas_slice_agg)
    structural_effect_r2: float = 0.0
    structural_top_movers: list[dict] = []
    for _sk in _all_slice_keys_r2:
        _c = _cur_slice_agg.get(_sk, {})
        _b = _bas_slice_agg.get(_sk, {})
        _c_route = to_float(_c.get("route"))
        _b_route = to_float(_b.get("route"))
        _b_rate = to_float(_b.get("rate")) if _b.get("rate") is not None else to_float(_c.get("rate"))
        _c_share = safe_div(_c_route, overall_current_route_amount) or 0.0
        _b_share = safe_div(_b_route, overall_baseline_route_amount) or 0.0
        _struct_contrib = (_c_share - _b_share) * (_b_rate or 0.0)
        structural_effect_r2 += _struct_contrib
        if abs(_c_share - _b_share) > 0.001:
            structural_top_movers.append({
                "slice_key": _sk,
                "current_share": round_float(_c_share, 4),
                "baseline_share": round_float(_b_share, 4),
                "share_delta": round_float(_c_share - _b_share, 4),
                "baseline_rate": round_float(_b_rate, 4),
                "structural_contribution": round_float(_struct_contrib, 6),
            })
    structural_top_movers.sort(key=lambda x: abs(to_float(x.get("structural_contribution"))), reverse=True)
    structural_effect_r2 = round_float(structural_effect_r2, 6)
    performance_effect_r2 = round_float((overall_delta or 0.0) - structural_effect_r2, 6)
    structural_ratio_r2 = safe_div(structural_effect_r2, overall_delta) if overall_delta else None
    is_structural_dominant = (
        overall_allows_drill_down
        and abs(overall_delta) >= PRIMARY_STRUCTURAL_MEANINGFUL_DECLINE
        and structural_effect_r2 < 0
        and structural_ratio_r2 is not None
        and structural_ratio_r2 >= PRIMARY_STRUCTURAL_DOMINANCE_THRESHOLD
    )
    # ─────────────────────────────────────────────────────────────────────────

    current_period_text = (
        normalize_text((context.get("current_period_label") or {}).get("text"))
        or f"{normalize_text((context.get('current_period') or {}).get('start'))[:10]}~"
        f"{normalize_text((context.get('current_period') or {}).get('end'))[:10]}"
    )
    baseline_period_text = (
        normalize_text((context.get("baseline_period_label") or {}).get("text"))
        or f"{normalize_text((context.get('baseline_period') or {}).get('start'))[:10]}~"
        f"{normalize_text((context.get('baseline_period') or {}).get('end'))[:10]}"
    )

    def build_group_slice_table_rows(
        slices: list[dict[str, Any]],
        *,
        selected_slices: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        selected_slice_keys = {
            normalize_text(item.get("slice_key"))
            for item in selected_slices
            if normalize_text(item.get("slice_key"))
        }
        for slice_item in slices:
            baseline_rate = slice_item.get("baseline_rate")
            current_rate = slice_item.get("current_rate")
            baseline_route_amount = slice_item.get("baseline_route_amount")
            current_route_amount = slice_item.get("current_route_amount")
            is_drill_down = normalize_text(slice_item.get("slice_key")) in selected_slice_keys
            delta_text = (
                format_percent(to_float(current_rate) - to_float(baseline_rate))
                if baseline_rate is not None and current_rate is not None else
                "-"
            )
            rows.append(
                {
                    "cp_dj_new": normalize_text(slice_item.get("cp_dj_new")),
                    "baseline_acceptance_rate_text": format_percent_or_dash(baseline_rate),
                    "current_acceptance_rate_text": format_percent_or_dash(current_rate),
                    # 是否下钻=是 的行加粗承接率变化，便于阅读“此行进入下钻”的关键依据
                    "acceptance_rate_delta_text": (
                        bold_md(delta_text) if is_drill_down and delta_text != "-" else delta_text
                    ),
                    "baseline_route_amount_text": (
                        format_amount_human(baseline_route_amount)
                        if baseline_route_amount is not None else
                        "-"
                    ),
                    "current_route_amount_text": (
                        format_amount_human(current_route_amount)
                        if current_route_amount is not None else
                        "-"
                    ),
                    "enter_drill_down_text": (
                        bold_md(format_yes_no(is_drill_down)) if is_drill_down else format_yes_no(is_drill_down)
                    ),
                }
            )
        return rows

    def analyze_customer_group(group_if_irr: str) -> dict[str, Any]:
        threshold = customer_group_threshold(group_if_irr)
        group_current_records = [
            item for item in current_records
            if normalize_text(item.get("if_irr")) == group_if_irr
        ]
        group_baseline_records = [
            item for item in baseline_records
            if normalize_text(item.get("if_irr")) == group_if_irr
        ]
        current_group_route_amount = sum(to_float(item.get("route_amount")) for item in group_current_records)
        baseline_group_route_amount = sum(to_float(item.get("route_amount")) for item in group_baseline_records)
        current_group_accepted_amount = sum(to_float(item.get("accepted_amount")) for item in group_current_records)
        baseline_group_accepted_amount = sum(to_float(item.get("accepted_amount")) for item in group_baseline_records)
        current_group_rate = safe_div(current_group_accepted_amount, current_group_route_amount)
        baseline_group_rate = safe_div(baseline_group_accepted_amount, baseline_group_route_amount)

        if not group_current_records or not group_baseline_records:
            summary_text = f"{group_if_irr} 当前期或对比期缺少可比承接率数据，当前先停在客群门槛判断。"
            judgement = build_customer_group_judgement(
                if_irr=group_if_irr,
                current_acceptance_rate=current_group_rate,
                baseline_acceptance_rate=baseline_group_rate,
                threshold=threshold,
                hit_threshold=False,
                hit_decline_threshold=False,
                enter_slice_analysis=False,
                group_terminal_reason="R8",
                summary_text=summary_text,
            )
            return {
                "judgement": judgement,
                "abnormal_slices": [],
                "selected_slices": [],
                        "drill_down_rule": {},
                "group_slice_rows": [],
            }

        group_delta = current_group_rate - baseline_group_rate
        hit_threshold = threshold is not None and current_group_rate < threshold
        hit_decline_threshold = (
            group_delta < 0 and abs(group_delta) > PRIMARY_CUSTOMER_GROUP_DECLINE_THRESHOLD
        )
        current_slice_map = _aggregate_slice_map(group_current_records)
        baseline_slice_map = _aggregate_slice_map(group_baseline_records)
        comparisons: list[dict[str, Any]] = []
        abnormal_slices: list[dict[str, Any]] = []
        for group_slice_key in sorted(set(current_slice_map) | set(baseline_slice_map)):
            current_item = current_slice_map.get(group_slice_key, {})
            baseline_item = baseline_slice_map.get(group_slice_key, {})
            current_slice_rate = current_item.get("acceptance_rate")
            baseline_slice_rate = baseline_item.get("acceptance_rate")
            current_slice_route = to_float(current_item.get("route_amount"))
            baseline_slice_route = to_float(baseline_item.get("route_amount"))
            current_route_share = safe_div(current_slice_route, current_group_route_amount)
            baseline_route_share = safe_div(baseline_slice_route, baseline_group_route_amount)
            delta_rate = None
            if current_item and baseline_item:
                delta_rate = to_float(current_slice_rate) - to_float(baseline_slice_rate)

            comparison = {
                "slice_key": group_slice_key,
                "slice_display": build_slice_display(
                    current_item.get("if_irr") or baseline_item.get("if_irr") or group_if_irr,
                    current_item.get("cp_dj_new") or baseline_item.get("cp_dj_new") or "",
                ),
                "if_irr": current_item.get("if_irr") or baseline_item.get("if_irr") or group_if_irr,
                "cp_dj_new": current_item.get("cp_dj_new") or baseline_item.get("cp_dj_new") or "",
                "current_rate": round_float(current_slice_rate, 6) if current_item else None,
                "baseline_rate": round_float(baseline_slice_rate, 6) if baseline_item else None,
                "delta_rate": round_float(delta_rate, 6),
                "current_route_amount": round_float(current_slice_route, 2) if current_item else None,
                "baseline_route_amount": round_float(baseline_slice_route, 2) if baseline_item else None,
                "impact_accept_amount_estimate": round_float(
                    current_slice_route * max(to_float(baseline_slice_rate) - to_float(current_slice_rate), 0.0),
                    2,
                ),
                "current_route_share": round_float(current_route_share, 6),
                "baseline_route_share": round_float(baseline_route_share, 6),
                "route_share_delta": round_float(current_route_share - baseline_route_share, 6),
            }
            comparisons.append(comparison)
            if delta_rate is not None and delta_rate < 0:
                abnormal_slices.append(comparison)

        sort_primary_slices(abnormal_slices)
        for index, item in enumerate(abnormal_slices, start=1):
            item["analysis_rank"] = index
        display_slices = [dict(item) for item in comparisons]
        sort_primary_slices(display_slices)
        if not hit_threshold and not hit_decline_threshold:
            group_slice_rows = build_group_slice_table_rows(
                display_slices,
                selected_slices=[],
            )
            summary_text = (
                f"{group_if_irr} 当前承接率 {format_percent(current_group_rate)}，"
                f"未低于 {format_percent(threshold or 0.0)} 门槛，且较对比期变化未达到 abs "
                f"{format_percent(PRIMARY_CUSTOMER_GROUP_DECLINE_THRESHOLD)}，当前不继续后续归因。"
            )
            judgement = build_customer_group_judgement(
                if_irr=group_if_irr,
                current_acceptance_rate=current_group_rate,
                baseline_acceptance_rate=baseline_group_rate,
                threshold=threshold,
                hit_threshold=False,
                hit_decline_threshold=False,
                enter_slice_analysis=False,
                group_terminal_reason="R9",
                summary_text=summary_text,
            )
            return {
                "judgement": judgement,
                "abnormal_slices": abnormal_slices,
                "selected_slices": [],
                "drill_down_rule": {},
                "group_slice_rows": group_slice_rows,
            }

        selected_slices, group_drill_down_rule = select_primary_drill_down_candidates(abnormal_slices)
        if not overall_allows_drill_down:
            selected_slices = []
            group_drill_down_rule = {
                **group_drill_down_rule,
                "selected_slice_count": 0,
                "selection_rule_text": "当前客群虽命中入口，但由于大盘承接率未下降，本次第一阶段停止，不继续进入第二阶段。",
            }
        group_slice_rows = build_group_slice_table_rows(
            display_slices,
            selected_slices=selected_slices,
        )
        group_terminal_reason: str | None = None
        if not overall_allows_drill_down and (hit_threshold or hit_decline_threshold):
            group_terminal_reason = "R1"
        elif not abnormal_slices or not selected_slices:
            group_terminal_reason = "R10"

        if hit_threshold and hit_decline_threshold:
            continue_reason_prefix = (
                f"{group_if_irr} 当前承接率 {format_percent(current_group_rate)} 已低于 {format_percent(threshold or 0.0)} 门槛，"
                f"且较对比期下降 {format_percent(abs(group_delta))}。"
            )
        elif hit_threshold:
            continue_reason_prefix = (
                f"{group_if_irr} 当前承接率 {format_percent(current_group_rate)} 已低于 {format_percent(threshold or 0.0)} 门槛。"
            )
        else:
            continue_reason_prefix = (
                f"{group_if_irr} 当前承接率 {format_percent(current_group_rate)} 虽未低于 {format_percent(threshold or 0.0)} 门槛，"
                f"但较对比期下降 {format_percent(abs(group_delta))}，已达到 abs {format_percent(PRIMARY_CUSTOMER_GROUP_DECLINE_THRESHOLD)} 的继续分析口径。"
            )

        if group_terminal_reason == "R1":
            summary_text = (
                f"{continue_reason_prefix} "
                f"{'该客群下识别到 ' + str(len(abnormal_slices)) + ' 个承接率下降切片，但' if abnormal_slices else '但'}"
                "由于大盘承接率未下降，本次停在第一阶段。"
            )
        elif group_terminal_reason == "R10":
            summary_text = f"{continue_reason_prefix} 但该客群下没有形成可继续下钻的异常切片，因此停在第一阶段。"
        else:
            summary_text = f"{continue_reason_prefix} 继续分析，识别到 {len(selected_slices)} 个可下钻异常切片（详见下方切片明细表，是否下钻见表格末列）。"

        judgement = build_customer_group_judgement(
            if_irr=group_if_irr,
            current_acceptance_rate=current_group_rate,
            baseline_acceptance_rate=baseline_group_rate,
            threshold=threshold,
            hit_threshold=hit_threshold,
            hit_decline_threshold=hit_decline_threshold,
            enter_slice_analysis=True,
            group_terminal_reason=group_terminal_reason,
            summary_text=summary_text,
        )
        return {
            "judgement": judgement,
            "abnormal_slices": abnormal_slices,
            "selected_slices": selected_slices,
            "drill_down_rule": group_drill_down_rule,
            "group_slice_rows": group_slice_rows,
        }

    group_results = [analyze_customer_group(group) for group in target_customer_groups]
    customer_group_judgements = [item["judgement"] for item in group_results]
    slice_analyzed_group_results = [
        item
        for item in group_results
        if bool(item["judgement"].get("enter_slice_analysis"))
    ]
    display_abnormal_slices = [
        dict(slice_item)
        for group_result in slice_analyzed_group_results
        for slice_item in group_result["abnormal_slices"]
    ]
    selected_slices = [
        dict(slice_item)
        for group_result in slice_analyzed_group_results
        for slice_item in group_result["selected_slices"]
    ]
    sort_primary_slices(display_abnormal_slices)
    sort_primary_slices(selected_slices)
    for index, item in enumerate(display_abnormal_slices, start=1):
        item["analysis_rank"] = index
    for index, item in enumerate(selected_slices, start=1):
        item["analysis_rank"] = index

    group_drill_down_rule_entries = [
        {
            "if_irr": group_result["judgement"].get("if_irr"),
            "abnormal_slice_count": len(group_result["abnormal_slices"]),
            **group_result["drill_down_rule"],
        }
        for group_result in slice_analyzed_group_results
        if group_result["drill_down_rule"]
    ]
    drill_down_rule = {
        "selection_scope": "per_customer_group",
        "selection_rule": "all_declining_slices_within_eligible_customer_group",
        "selection_rule_text": "命中客群入口后，该客群下所有承接率较对比期下降的切片都继续下钻。",
        "impact_accept_amount_estimate_formula_text": primary_impact_accept_amount_formula_text(),
        "group_rules": group_drill_down_rule_entries,
    }

    # 路由用队列：R2 时会清空，但下游 capital/asset 仍需按 slice_key 查找一级快照，故单独保留 lookup
    analysis_sequence_lookup = build_primary_analysis_sequence(selected_slices)
    analysis_sequence = list(analysis_sequence_lookup)

    terminal_reason: str | None = None
    next_action = "run_capital"
    if not overall_allows_drill_down:
        terminal_reason = "R1"
        next_action = "stop"
    elif is_structural_dominant:
        # R2：路由金额结构迁移是大盘下降的主因，无需进入资方桶分布诊断
        terminal_reason = "R2"
        next_action = "stop"
        analysis_sequence = []  # 不进入后续阶段
    elif not analysis_sequence:
        next_action = "stop"
        if any(item.get("group_terminal_reason") == "R8" for item in customer_group_judgements):
            terminal_reason = "R8"
        elif any(bool(item.get("hit_threshold")) or bool(item.get("hit_decline_threshold")) for item in customer_group_judgements):
            terminal_reason = "R10"
        else:
            terminal_reason = "R9"

    customer_group_summary_text = build_customer_group_summary_text(
        customer_group_judgements,
        has_selected_slices=bool(analysis_sequence),
        terminal_reason=terminal_reason,
    )

    # 组装 R2 的结构分解证据
    _structural_ratio_pct = (
        f"{round_float(structural_ratio_r2 * 100, 1)}%"
        if structural_ratio_r2 is not None
        else "-"
    )
    _r2_evidence = [
        f"大盘承接率变化：{format_percent(overall_delta)}（当期 - 对比期）。",
        f"结构效应（路由份额变化）：{format_percent(structural_effect_r2)}，占大盘下降 {_structural_ratio_pct}。",
        f"性能效应（各切片承接率变化）：{format_percent(performance_effect_r2)}，占大盘下降 {format_percent(round_float(1.0 - (structural_ratio_r2 or 0), 4))}。",
        f"触发阈值：结构效应占比 ≥ {int(PRIMARY_STRUCTURAL_DOMINANCE_THRESHOLD * 100)}%。",
    ]
    if structural_top_movers:
        _r2_evidence.append("路由份额变化最大的切片（按结构贡献绝对值排序）：")
        for _mv in structural_top_movers[:5]:
            _sign = "+" if to_float(_mv["share_delta"]) > 0 else ""
            _r2_evidence.append(
                f"  • {_mv['slice_key']}：份额 {format_percent(_mv['baseline_share'])} → {format_percent(_mv['current_share'])}"
                f"（{_sign}{format_percent(_mv['share_delta'])}），对比期承接率 {format_percent(_mv['baseline_rate'])}，"
                f"结构贡献 {format_percent(_mv['structural_contribution'])}。"
            )

    if terminal_reason == "R1":
        business = business_view(
            headline="大盘承接率未下降",
            summary="整体大盘承接率未下降，本次不继续进入资方分布诊断。",
            evidence=[customer_group_summary_text],
        )
    elif terminal_reason == "R2":
        business = business_view(
            headline="大盘承接率下降主因是 cp_dj_new 路由金额结构迁移，非审核趋严",
            summary=(
                f"大盘承接率下降 {format_percent(overall_delta)}，其中结构效应（高承接率切片路由占比减少 / 低承接率切片占比增加）"
                f"贡献了 {_structural_ratio_pct}，超过 {int(PRIMARY_STRUCTURAL_DOMINANCE_THRESHOLD * 100)}% 的触发阈值。"
                "当前归因停在第一阶段，建议重点关注路由金额结构变化原因，而非下钻资方桶分布。"
            ),
            evidence=_r2_evidence,
        )
    elif terminal_reason == "R9":
        business = business_view(
            headline="目标客群未触发继续分析条件",
            summary="本次纳入分析的目标客群既没有低于各自门槛，也没有出现达到 abs 0.3% 的明显下降，因此第一阶段停止。",
            evidence=[customer_group_summary_text],
        )
    elif terminal_reason == "R10":
        business = business_view(
            headline="目标客群已检查，但未形成继续下钻切片",
            summary="目标客群虽然命中了继续分析条件，但在客群内没有形成可继续下钻的异常切片，因此第一阶段停止。",
            evidence=[customer_group_summary_text],
        )
    elif terminal_reason == "R8":
        business = business_view(
            headline="目标客群数据不足",
            summary="本次目标客群存在缺少可比数据的情况，当前无法稳定进入后续归因。",
            evidence=[customer_group_summary_text],
        )
    else:
        business = business_view(
            headline="已定位可继续分析的异常切片",
            summary="目标客群已命中继续分析条件，且已定位到可继续下钻的客群 + cp_dj_new 异常切片，后续进入资方分布诊断。",
            evidence=[customer_group_summary_text],
        )

    group_slice_markdown_map: dict[str, str] = {}
    for group_result in group_results:
        group_label = normalize_text(group_result["judgement"].get("if_irr"))
        table_rows = list(group_result.get("group_slice_rows") or [])
        total_count = len(table_rows)
        # 标题中的“继续下钻数量”以分表内逐行“是否下钻”结果为准，
        # 避免与路由层 selected_slices 在边界数据下出现口径不一致。
        drill_down_count = sum(
            1 for row in table_rows
            if normalize_text(row.get("enter_drill_down_text")) == "是"
        )
        markdown_table = build_markdown_table(PRIMARY_GROUP_SLICE_TABLE_COLUMNS, table_rows) if table_rows else ""
        if markdown_table:
            if drill_down_count > 0 and drill_down_count < total_count:
                header_note = f"共 {total_count} 个切片，其中 {drill_down_count} 个承接率下降继续下钻"
            elif drill_down_count > 0:
                header_note = f"共 {total_count} 个切片，全部承接率下降继续下钻"
            else:
                header_note = f"共 {total_count} 个切片"
            markdown_block = f"#### {group_label}（{header_note}）\n{markdown_table}"
        else:
            markdown_block = f"#### {group_label}\n当前客群没有可展示的切片。"
        group_slice_markdown_map[group_label] = markdown_block

    def group_markdown_or_default(group_label: str) -> str:
        if group_label in group_slice_markdown_map:
            return group_slice_markdown_map[group_label]
        return f"#### {group_label}\n本次请求未纳入该客群。"

    huixuan_group_markdown = group_markdown_or_default(TARGET_CUSTOMER_GROUPS[0])
    jingyou_group_markdown = group_markdown_or_default(TARGET_CUSTOMER_GROUPS[1])

    route_amount_delta = overall_current_route_amount - overall_baseline_route_amount
    overall_judgement_text = "大盘承接率确实下降。" if overall_delta < 0 else "大盘承接率未下降。"
    customer_group_change_rows = []
    for judgement in customer_group_judgements:
        delta_text = "-"
        if judgement.get("current_acceptance_rate") is not None and judgement.get("baseline_acceptance_rate") is not None:
            delta_text = format_percent(
                to_float(judgement.get("current_acceptance_rate")) - to_float(judgement.get("baseline_acceptance_rate"))
            )
        customer_group_change_rows.append(
            {
                "if_irr": judgement.get("if_irr"),
                "baseline_acceptance_rate_text": judgement.get("baseline_acceptance_rate_text"),
                "current_acceptance_rate_text": judgement.get("current_acceptance_rate_text"),
                "acceptance_rate_delta_text": delta_text,
            }
        )
    overall_summary_markdown = build_primary_overall_summary_markdown(
        context=context,
        customer_group_rows=customer_group_change_rows,
        current_acceptance_rate=current_rate,
        baseline_acceptance_rate=baseline_rate,
        acceptance_rate_delta=overall_delta,
        current_route_amount=overall_current_route_amount,
        baseline_route_amount=overall_baseline_route_amount,
    )
    drill_down_scope_markdown = build_primary_continue_analysis_scope_markdown()
    workflow_overview_markdown = build_workflow_overview_markdown()

    # ===== 状态展示规范：一级阶段前置状态块（不再展示切片队列） =====
    slice_total_count = len(analysis_sequence)
    if terminal_reason in {"R1", "R9", "R10", "R8"} or (
        terminal_reason is None and slice_total_count == 0
    ):
        primary_status_line = build_status_line(
            slice_index=0 if slice_total_count else None,
            slice_total=slice_total_count if slice_total_count else None,
            slice_display="一级总览",
            terminal_reason=terminal_reason or "R10",
            completed_stages=[],
            conclusion_tag=conclusion_tag_for_reason(terminal_reason or "R10"),
            task_step=1,
            task_total=2,
            task_label="大盘分析+异常切片定位",
            show_slice_context=False,
            show_stage_details=False,
        )
    elif terminal_reason == "R2":
        primary_status_line = build_status_line(
            slice_index=0 if slice_total_count else None,
            slice_total=slice_total_count if slice_total_count else None,
            slice_display="一级总览",
            terminal_reason="R2",
            completed_stages=[],
            conclusion_tag=conclusion_tag_for_reason("R2"),
            task_step=1,
            task_total=2,
            task_label="大盘分析+异常切片定位",
            show_slice_context=False,
            show_stage_details=False,
        )
    else:
        # 进入下钻：S1 OK，后续阶段待定
        primary_status_line = build_status_line(
            slice_index=0 if slice_total_count else None,
            slice_total=slice_total_count if slice_total_count else None,
            slice_display="一级总览",
            terminal_reason=None,
            completed_stages=["S1"],
            conclusion_tag=f"已识别 {slice_total_count} 个异常切片，进入二级",
            task_step=1,
            task_total=2,
            task_label="大盘分析+异常切片定位",
            show_slice_context=False,
            show_stage_details=False,
        )
    primary_status_block = primary_status_line

    stage1_verbatim_markdown = "\n\n".join(
        [
            workflow_overview_markdown,
            primary_status_block,
            overall_summary_markdown,
            customer_group_summary_text,
            drill_down_scope_markdown,
            huixuan_group_markdown,
            jingyou_group_markdown,
        ]
    )

    primary_display = {
        # ===== 展示层专用字段（唯一合法用户输出来源，按 SKILL.md 顺序排列）=====
        "stage1_verbatim_markdown": stage1_verbatim_markdown,
        "overall_summary_markdown": overall_summary_markdown,
        "workflow_overview_markdown": workflow_overview_markdown,
        "drill_down_scope_markdown": drill_down_scope_markdown,
        "huixuan_group_markdown": huixuan_group_markdown,
        "jingyou_group_markdown": jingyou_group_markdown,
        # ===== 状态展示规范字段（必须作为第一阶段最后一段原样输出）=====
        "slice_queue_line": "",
        "status_line": primary_status_line,
        "stage1_status_block": primary_status_block,
        # ===== 内部路由元信息 =====
        "overall_summary": {
            "current_acceptance_rate": round_float(current_rate, 6),
            "baseline_acceptance_rate": round_float(baseline_rate, 6),
            "acceptance_rate_delta": round_float(overall_delta, 6),
            "acceptance_rate_delta_bp_text": format_bp(overall_delta),
            "current_period_text": current_period_text,
            "baseline_period_text": baseline_period_text,
            "current_acceptance_rate_text": format_percent(current_rate),
            "baseline_acceptance_rate_text": format_percent(baseline_rate),
            "acceptance_rate_delta_text": format_percent(overall_delta),
            "current_route_amount": round_float(overall_current_route_amount, 2),
            "baseline_route_amount": round_float(overall_baseline_route_amount, 2),
            "route_amount_delta": round_float(route_amount_delta, 2),
            "current_route_amount_text": format_wan(overall_current_route_amount),
            "baseline_route_amount_text": format_wan(overall_baseline_route_amount),
            "abnormal_slice_count": len(display_abnormal_slices),
            "drill_down_slice_count": len(analysis_sequence),
            "overall_judgement_text": overall_judgement_text,
            "impact_accept_amount_estimate_formula_text": primary_impact_accept_amount_formula_text(),
        },
        "structural_decomposition": {
            "structural_effect": structural_effect_r2,
            "performance_effect": performance_effect_r2,
            "structural_ratio": round_float(structural_ratio_r2, 4) if structural_ratio_r2 is not None else None,
            "structural_ratio_text": _structural_ratio_pct,
            "is_structural_dominant": is_structural_dominant,
            "dominance_threshold": PRIMARY_STRUCTURAL_DOMINANCE_THRESHOLD,
            "top_movers": structural_top_movers[:5],
        },
        "render_summary": {
            "llm_render_field": "primary_display.overall_summary_markdown",
            "llm_stage1_verbatim_field": "primary_display.stage1_verbatim_markdown",
            "llm_followup_field": "primary_display.drill_down_scope_markdown",
            "llm_group_fields": [
                "primary_display.huixuan_group_markdown",
                "primary_display.jingyou_group_markdown",
            ],
            "must_use_markdown_table_verbatim": True,
            "instruction": (
                "【强制执行】第一阶段输出优先整体复用 primary_display.stage1_verbatim_markdown。"
                "若必须拆分，只能按以下顺序逐字复制，不得改写、合并或省略："
                "① primary_display.workflow_overview_markdown；"
                "② primary_display.stage1_status_block；"
                "③ primary_display.overall_summary_markdown；"
                "④ customer_group_summary_text；"
                "⑤ primary_display.drill_down_scope_markdown；"
                "⑥ primary_display.huixuan_group_markdown；"
                "⑦ primary_display.jingyou_group_markdown。"
                "状态块中不展示切片队列，只展示切片进度与中文阶段状态。"
                "analysis_sequence 只用于路由，严禁在第一阶段正文中重新拼接统计。"
            ),
        },
    }

    trace = {
        "context": context,
        "overall": {
            "current_acceptance_rate": round_float(current_rate, 6),
            "baseline_acceptance_rate": round_float(baseline_rate, 6),
            "delta_rate": round_float(overall_delta, 6),
            "current_route_amount": round_float(overall_current_route_amount, 2),
            "baseline_route_amount": round_float(overall_baseline_route_amount, 2),
            "is_declining": overall_delta < 0,
        },
        "structural_decomposition": {
            "structural_effect": structural_effect_r2,
            "performance_effect": performance_effect_r2,
            "structural_ratio": round_float(structural_ratio_r2, 4) if structural_ratio_r2 is not None else None,
            "is_structural_dominant": is_structural_dominant,
            "top_movers": structural_top_movers[:5],
        },
        "analysis_sequence": analysis_sequence,
        "analysis_sequence_lookup": analysis_sequence_lookup,
        "customer_group_judgements": customer_group_judgements,
        "customer_group_summary_text": customer_group_summary_text,
        "terminal_reason": terminal_reason,
        "next_action": next_action,
        "drill_down_rule": drill_down_rule,
        "primary_display": primary_display,
        "business_view": business,
        "errors": [],
    }
    log_stage_event("primary", "阶段完成", trace=trace)
    return trace


def _allow_bucket_sort_key(bucket_label: str) -> tuple[int, float, str]:
    bucket_value = parse_allow_bucket(bucket_label)
    if bucket_value is None:
        return (1, float("inf"), normalize_text(bucket_label))
    return (0, bucket_value, normalize_text(bucket_label))


def _tail_bucket_summary(bucket_deltas: list[dict[str, Any]], top_n: int) -> dict[str, Any]:
    if len(bucket_deltas) <= top_n:
        return {}
    tail_items = bucket_deltas[top_n:]
    return {
        "bucket_count": len(tail_items),
        "current_route_share": round_float(sum(to_float(item.get("current_route_share")) for item in tail_items), 6),
        "baseline_route_share": round_float(sum(to_float(item.get("baseline_route_share")) for item in tail_items), 6),
        "route_share_delta": round_float(sum(to_float(item.get("route_share_delta")) for item in tail_items), 6),
    }


def _build_capital_data_quality(
    *,
    current_buckets: list[dict[str, Any]],
    baseline_buckets: list[dict[str, Any]],
) -> dict[str, Any]:
    def _summary(items: list[dict[str, Any]]) -> dict[str, Any]:
        unknown_items = [item for item in items if parse_allow_bucket(item.get("alllow_ly_cnt")) is None]
        return {
            "unknown_allow_bucket_count": len(unknown_items),
            "unknown_allow_routing_cnt": round_float(sum(to_float(item.get("route_count")) for item in unknown_items), 2),
            "unknown_allow_routing_amount": round_float(sum(to_float(item.get("route_amount")) for item in unknown_items), 2),
            "route_count_missing_bucket_count": sum(
                1
                for item in items
                if parse_allow_bucket(item.get("alllow_ly_cnt")) is not None and int(item.get("route_count_present_rows", 0)) == 0
            ),
            "route_amount_missing_bucket_count": sum(
                1
                for item in items
                if parse_allow_bucket(item.get("alllow_ly_cnt")) is not None and int(item.get("route_amount_present_rows", 0)) == 0
            ),
        }

    current_summary = _summary(current_buckets)
    baseline_summary = _summary(baseline_buckets)
    return {
        "unknown_allow_bucket_count_current": current_summary["unknown_allow_bucket_count"],
        "unknown_allow_bucket_count_baseline": baseline_summary["unknown_allow_bucket_count"],
        "unknown_allow_routing_cnt_current": current_summary["unknown_allow_routing_cnt"],
        "unknown_allow_routing_cnt_baseline": baseline_summary["unknown_allow_routing_cnt"],
        "unknown_allow_routing_amount_current": current_summary["unknown_allow_routing_amount"],
        "unknown_allow_routing_amount_baseline": baseline_summary["unknown_allow_routing_amount"],
        "route_count_missing_bucket_count_current": current_summary["route_count_missing_bucket_count"],
        "route_count_missing_bucket_count_baseline": baseline_summary["route_count_missing_bucket_count"],
        "route_amount_missing_bucket_count_current": current_summary["route_amount_missing_bucket_count"],
        "route_amount_missing_bucket_count_baseline": baseline_summary["route_amount_missing_bucket_count"],
    }


def _build_cdf_cutoff_stats(
    *,
    valid_bucket_keys: list[str],
    current_bucket_map: dict[str, dict[str, Any]],
    baseline_bucket_map: dict[str, dict[str, Any]],
    current_total_route_valid: float,
    baseline_total_route_valid: float,
) -> tuple[list[dict[str, Any]], int, int, float | None, float | None, bool]:
    cdf_cutoff_stats: list[dict[str, Any]] = []
    current_running = 0.0
    baseline_running = 0.0
    effective_cutoff_count = 0
    effective_cutoff_hit_count = 0
    max_negative_cutoff_delta: float | None = None
    has_positive_cutoff_signal = False
    reached_tail = False
    for bucket_key in valid_bucket_keys:
        current_running += safe_div(
            to_float((current_bucket_map.get(bucket_key) or {}).get("route_amount")),
            current_total_route_valid,
        )
        baseline_running += safe_div(
            to_float((baseline_bucket_map.get(bucket_key) or {}).get("route_amount")),
            baseline_total_route_valid,
        )
        cdf_delta = round_float(current_running - baseline_running, 6)
        is_effective_cutoff = not reached_tail
        if is_effective_cutoff:
            effective_cutoff_count += 1
            if to_float(cdf_delta) >= 0:
                effective_cutoff_hit_count += 1
            if max_negative_cutoff_delta is None or to_float(cdf_delta) < to_float(max_negative_cutoff_delta):
                max_negative_cutoff_delta = cdf_delta
            if to_float(cdf_delta) >= 0.05:
                has_positive_cutoff_signal = True
        cdf_cutoff_stats.append(
            {
                "bucket_label": bucket_key,
                "bucket_value": round_float(parse_allow_bucket(bucket_key), 6),
                "current_cdf_share": round_float(current_running, 6),
                "baseline_cdf_share": round_float(baseline_running, 6),
                "cdf_delta": cdf_delta,
                "is_effective_cutoff": is_effective_cutoff,
            }
        )
        if not reached_tail and current_running >= 0.995 and baseline_running >= 0.995:
            reached_tail = True
    effective_cutoff_hit_ratio = None
    if effective_cutoff_count > 0:
        effective_cutoff_hit_ratio = round_float(effective_cutoff_hit_count / effective_cutoff_count, 6)
    return (
        cdf_cutoff_stats,
        effective_cutoff_count,
        effective_cutoff_hit_count,
        effective_cutoff_hit_ratio,
        max_negative_cutoff_delta,
        has_positive_cutoff_signal,
    )


def run_capital_stage(
    *,
    granularity: str,
    current_start: str,
    current_end: str,
    baseline_start: str,
    baseline_end: str,
    slice_key: str,
    access_token: str,
    endpoint: str | None = None,
    primary_trace: dict[str, Any] | None = None,
    slice_index: int | None = None,
    slice_total: int | None = None,
) -> dict[str, Any]:
    normalized_granularity = normalize_granularity(granularity)
    log_stage_event(
        "capital",
        "开始阶段",
        slice_key=slice_key,
        granularity=normalized_granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )
    context = build_context(
        granularity=granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )

    def build_capital_failure_trace(
        *,
        headline: str,
        summary: str,
        analysis_steps: list[dict[str, Any]],
        errors: list[str],
        skipped_reason: str,
        root_type: str,
        root_message: str,
        debug_query: dict[str, Any] | None = None,
        root_details: dict[str, Any] | None = None,
        capital_total_judgement: dict[str, Any] | None = None,
        distribution_judgement: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        trace = {
            "context": context,
            "slice_key": slice_key,
            "slice_display": slice_display,
            "capital_distribution_stats": [],
            "capital_total_judgement": capital_total_judgement
            or build_capital_total_judgement(
                evaluated=False,
                threshold_absolute=CAPITAL_TOTAL_DROP_ABSOLUTE_THRESHOLD,
                skipped_reason=skipped_reason,
            ),
            "distribution_judgement": distribution_judgement
            or build_distribution_judgement(
                evaluated=False,
                skipped_reason=skipped_reason,
            ),
            "analysis_steps": analysis_steps,
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "next_action": "stop",
            "business_view": business_view(
                headline=headline,
                summary=summary,
                evidence=errors,
            ),
            "root_cause": build_root_cause(
                root_type,
                root_message,
                slice_key=slice_key,
                slice_display=slice_display,
                **(root_details or {}),
            ),
            "errors": errors,
        }
        if debug_query is not None:
            trace["debug_query"] = debug_query
        trace = _finalize_capital_trace(trace, slice_index=slice_index, slice_total=slice_total)
        log_stage_event("capital", "阶段失败", slice_key=slice_key, trace=trace)
        return trace

    if normalized_granularity not in SUPPORTED_GRANULARITIES:
        error = unsupported_granularity_error(normalized_granularity)
        trace = {
            "context": context,
            "slice_key": slice_key,
            "slice_display": slice_key,
            "capital_distribution_stats": [],
            "capital_total_judgement": build_capital_total_judgement(
                evaluated=False,
                threshold_absolute=CAPITAL_TOTAL_DROP_ABSOLUTE_THRESHOLD,
                skipped_reason="unsupported_granularity",
            ),
            "distribution_judgement": build_distribution_judgement(
                evaluated=False,
                skipped_reason="unsupported_granularity",
            ),
            "analysis_steps": [
                stage_analysis_step(
                    step="粒度校验",
                    analysis="先确认当前阶段是否支持这个粒度。",
                    evidence=[error],
                    conclusion="当前版本不支持这个粒度，第二阶段停止执行。",
                )
            ],
            "terminal_reason": "R8",
            "next_action": "stop",
            "business_view": business_view(
                headline="当前粒度暂未接入",
                summary="当前版本仅支持日粒度和周粒度的资方分布诊断。",
                evidence=[error],
            ),
            "root_cause": build_root_cause(
                "unsupported_granularity",
                "资方分布阶段收到当前版本未支持的粒度。",
                granularity=normalized_granularity,
            ),
            "errors": [error],
        }
        trace = _finalize_capital_trace(trace, slice_index=slice_index, slice_total=slice_total)
        log_stage_event("capital", "阶段失败", slice_key=slice_key, trace=trace)
        return trace
    current_period = context["current_period"]
    baseline_period = context["baseline_period"]

    if_irr, _, cp_dj_new = parse_slice_key(slice_key)
    slice_display = build_slice_display(if_irr, cp_dj_new=cp_dj_new)
    # 与一级 analysis_sequence 对齐的 N/M：缺参时用「全客群」一级结果解析，避免只跑单客群时队列长度变短
    resolved_primary_for_queue = primary_trace
    if (slice_index is None or not slice_total) and resolved_primary_for_queue is None:
        resolved_primary_for_queue = run_primary_stage(
            granularity=normalized_granularity,
            current_start=current_start,
            current_end=current_end,
            baseline_start=baseline_start,
            baseline_end=baseline_end,
            access_token=access_token,
            endpoint=endpoint,
            if_irr=None,
            cp_dj_new=None,
        )
    if (slice_index is None or not slice_total) and resolved_primary_for_queue:
        derived_index, derived_total = resolve_slice_index_from_primary(resolved_primary_for_queue, slice_key)
        if slice_index is None:
            slice_index = derived_index
        if not slice_total:
            slice_total = derived_total
    current_filter = build_main_rules(
        start=current_period["start"],
        end=current_period["end"],
        if_irr=if_irr,
        cp_dj_new=cp_dj_new,
    )
    baseline_filter = build_main_rules(
        start=baseline_period["start"],
        end=baseline_period["end"],
        if_irr=if_irr,
        cp_dj_new=cp_dj_new,
    )

    distribution_metrics = [
        client.metric(METRIC_ROUTING_COUNT),
        client.metric(METRIC_ROUTING_AMOUNT),
        client.metric(METRIC_ACCEPTANCE_RATE),
    ]
    distribution_dimensions = build_main_dimensions(granularity=normalized_granularity, include_allow=True)
    current_result, current_error = _query_rows(
        access_token=access_token,
        metric_list=distribution_metrics,
        dimension_list=distribution_dimensions,
        filter_payload=current_filter,
        endpoint=endpoint,
    )
    baseline_result, baseline_error = _query_rows(
        access_token=access_token,
        metric_list=distribution_metrics,
        dimension_list=distribution_dimensions,
        filter_payload=baseline_filter,
        endpoint=endpoint,
    )

    if current_error or baseline_error:
        return build_capital_failure_trace(
            headline="资方桶级明细查询失败",
            summary="第二阶段需要先取桶级明细，同时用于准入资方个数总量估算和全桶分布判断，但当前查询失败了。",
            analysis_steps=[
                stage_analysis_step(
                    step="资方桶级明细取数",
                    analysis="先取当前期和对比期的资方桶级明细，同时支持总量估算和全桶分布判断。",
                    evidence=[item for item in [current_error, baseline_error] if item],
                    conclusion="桶级明细查询失败，当前无法继续判断。",
                )
            ],
            errors=[item for item in [current_error, baseline_error] if item],
            skipped_reason="capital_distribution_query_error",
            root_type="query_error",
            root_message="资方桶级明细查询失败。",
            debug_query=_period_debug_snapshot(
                current_result=current_result,
                baseline_result=baseline_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            ),
            root_details={
                "current_error": current_error,
                "baseline_error": baseline_error,
            },
        )

    current_records = _normalized_metric_rows(
        current_result.get("rows", []),
        [time_dimension_name(normalized_granularity), "if_irr", "cp_dj_new", "alllow_ly_cnt"],
    )
    baseline_records = _normalized_metric_rows(
        baseline_result.get("rows", []),
        [time_dimension_name(normalized_granularity), "if_irr", "cp_dj_new", "alllow_ly_cnt"],
    )
    if not current_records or not baseline_records:
        errors: list[str] = []
        if not current_records:
            errors.append("当前周期没有拿到这组订单的资方桶级明细。")
        if not baseline_records:
            errors.append("对比周期没有拿到这组订单的资方桶级明细。")
        return build_capital_failure_trace(
            headline="资方桶级明细不完整",
            summary="第二阶段需要当前期和对比期的桶级明细来同时计算总量和分布，但当前缺少可比数据。",
            analysis_steps=[
                stage_analysis_step(
                    step="资方桶级明细取数",
                    analysis="先取当前期和对比期的资方桶级明细，同时支持总量估算和全桶分布判断。",
                    evidence=errors,
                    conclusion="当前期或对比期缺少可比桶级明细，当前无法继续判断。",
                )
            ],
            errors=errors,
            skipped_reason="capital_distribution_data_missing",
            root_type="missing_slice_data",
            root_message="资方分布阶段缺少当前期或对比期的桶级明细。",
            debug_query=_period_debug_snapshot(
                current_result=current_result,
                baseline_result=baseline_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            ),
            root_details={
                "current_row_count": len(current_records),
                "baseline_row_count": len(baseline_records),
                "current_period": current_period,
                "baseline_period": baseline_period,
            },
        )

    current_buckets = _aggregate_records(current_records, ["alllow_ly_cnt"])
    baseline_buckets = _aggregate_records(baseline_records, ["alllow_ly_cnt"])
    data_quality = _build_capital_data_quality(
        current_buckets=current_buckets,
        baseline_buckets=baseline_buckets,
    )
    current_bucket_map = {normalize_text(item["alllow_ly_cnt"]): item for item in current_buckets}
    baseline_bucket_map = {normalize_text(item["alllow_ly_cnt"]): item for item in baseline_buckets}
    current_valid_buckets = [item for item in current_buckets if parse_allow_bucket(item.get("alllow_ly_cnt")) is not None]
    baseline_valid_buckets = [item for item in baseline_buckets if parse_allow_bucket(item.get("alllow_ly_cnt")) is not None]

    if not current_valid_buckets or not baseline_valid_buckets:
        errors: list[str] = []
        if not current_valid_buckets:
            errors.append("当前周期的 alllow_ly_cnt 桶都无法解析，无法估算准入资方个数总量。")
        if not baseline_valid_buckets:
            errors.append("对比周期的 alllow_ly_cnt 桶都无法解析，无法估算准入资方个数总量。")
        return build_capital_failure_trace(
            headline="资方桶口径无法解析",
            summary="桶级明细虽然有返回，但 alllow_ly_cnt 都无法解析成可比较的资方个数桶，因此第二阶段无法继续。",
            analysis_steps=[
                stage_analysis_step(
                    step="准入资方总量估算准备",
                    analysis="先检查 alllow_ly_cnt 是否能解析成有效的资方个数桶。",
                    evidence=errors,
                    conclusion="当前期或对比期没有可解析的资方个数桶，无法进行总量估算和全桶分布判断。",
                )
            ],
            errors=errors,
            skipped_reason="capital_total_bucket_unparseable",
            root_type="capital_total_bucket_unparseable",
            root_message="alllow_ly_cnt 无法解析成有效桶值。",
            debug_query=_period_debug_snapshot(
                current_result=current_result,
                baseline_result=baseline_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            ),
            root_details={"data_quality": data_quality},
        )

    current_missing_route_count = [
        normalize_text(item.get("alllow_ly_cnt"))
        for item in current_valid_buckets
        if int(item.get("route_count_present_rows", 0)) == 0
    ]
    baseline_missing_route_count = [
        normalize_text(item.get("alllow_ly_cnt"))
        for item in baseline_valid_buckets
        if int(item.get("route_count_present_rows", 0)) == 0
    ]
    current_missing_route_amount = [
        normalize_text(item.get("alllow_ly_cnt"))
        for item in current_valid_buckets
        if int(item.get("route_amount_present_rows", 0)) == 0
    ]
    baseline_missing_route_amount = [
        normalize_text(item.get("alllow_ly_cnt"))
        for item in baseline_valid_buckets
        if int(item.get("route_amount_present_rows", 0)) == 0
    ]
    if current_missing_route_count or baseline_missing_route_count or current_missing_route_amount or baseline_missing_route_amount:
        errors: list[str] = []
        if current_missing_route_count:
            errors.append(f"当前周期以下资方桶缺少 routing_cnt：{', '.join(current_missing_route_count)}。")
        if baseline_missing_route_count:
            errors.append(f"对比周期以下资方桶缺少 routing_cnt：{', '.join(baseline_missing_route_count)}。")
        if current_missing_route_amount:
            errors.append(f"当前周期以下资方桶缺少 routing_amount：{', '.join(current_missing_route_amount)}。")
        if baseline_missing_route_amount:
            errors.append(f"对比周期以下资方桶缺少 routing_amount：{', '.join(baseline_missing_route_amount)}。")
        return build_capital_failure_trace(
            headline="资方桶关键指标缺失",
            summary="桶级明细已返回，但部分有效资方桶缺少 routing_cnt 或 routing_amount，无法稳定完成总量估算和全桶分布比较。",
            analysis_steps=[
                stage_analysis_step(
                    step="准入资方总量估算准备",
                    analysis="在计算总量和分布前，先确认有效桶同时具备 routing_cnt 与 routing_amount。",
                    evidence=errors,
                    conclusion="关键指标字段缺失，当前无法形成稳定的第二阶段判断。",
                )
            ],
            errors=errors,
            skipped_reason="capital_total_metric_missing",
            root_type="capital_total_metric_missing",
            root_message="有效资方桶缺少 routing_cnt 或 routing_amount。",
            debug_query=_period_debug_snapshot(
                current_result=current_result,
                baseline_result=baseline_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            ),
            root_details={"data_quality": data_quality},
        )

    current_route_amount_for_mean = sum(to_float(item.get("route_amount")) for item in current_valid_buckets)
    baseline_route_amount_for_mean = sum(to_float(item.get("route_amount")) for item in baseline_valid_buckets)
    weighted_mean_current_total = round_float(
        safe_div(
            sum(
                (parse_allow_bucket(item.get("alllow_ly_cnt")) or 0.0) * to_float(item.get("route_amount"))
                for item in current_valid_buckets
            ),
            current_route_amount_for_mean,
        ),
        4,
    )
    weighted_mean_baseline_total = round_float(
        safe_div(
            sum(
                (parse_allow_bucket(item.get("alllow_ly_cnt")) or 0.0) * to_float(item.get("route_amount"))
                for item in baseline_valid_buckets
            ),
            baseline_route_amount_for_mean,
        ),
        4,
    )
    capital_total_judgement = build_capital_total_judgement(
        current=weighted_mean_current_total,
        baseline=weighted_mean_baseline_total,
        threshold_absolute=CAPITAL_TOTAL_DROP_ABSOLUTE_THRESHOLD,
        evaluated=True,
        data_quality=data_quality,
    )

    # 标准化下降幅度辅助信号：将绝对下降量折算为桶值域（max - min）的比例，
    # 让用户对「2 家/单阈值」在当前渠道桶分布下的相对含义有额外判断依据。
    _all_valid_bucket_values = [
        v
        for v in (
            parse_allow_bucket(normalize_text(item.get("alllow_ly_cnt")))
            for item in current_valid_buckets + baseline_valid_buckets
        )
        if v is not None
    ]
    bucket_value_min = min(_all_valid_bucket_values) if _all_valid_bucket_values else None
    bucket_value_max = max(_all_valid_bucket_values) if _all_valid_bucket_values else None
    bucket_value_range = (
        round_float(bucket_value_max - bucket_value_min, 4)
        if bucket_value_min is not None and bucket_value_max is not None and bucket_value_max > bucket_value_min
        else None
    )
    _total_drop = capital_total_judgement.get("drop")
    normalized_drop_signal: float | None = (
        round_float(_total_drop / bucket_value_range, 4)
        if _total_drop is not None and bucket_value_range
        else None
    )

    def _normalized_signal_line() -> str:
        """生成标准化下降幅度辅助信号描述行。"""
        if bucket_value_range is None:
            return "辅助信号：桶值域不可计算（单桶或无有效桶），无法输出标准化下降比例。"
        drop_pct = f"{round_float(normalized_drop_signal * 100, 1)}%" if normalized_drop_signal is not None else "-"
        return (
            f"辅助信号（相对桶值域标准化）：桶值域 {bucket_value_min}～{bucket_value_max} 家，跨度 {bucket_value_range} 家；"
            f"当前下降幅度占桶值域 {drop_pct}。"
        )

    current_total_route_all = sum(to_float(item.get("route_amount")) for item in current_buckets)
    baseline_total_route_all = sum(to_float(item.get("route_amount")) for item in baseline_buckets)
    current_total_route_valid = sum(to_float(item.get("route_amount")) for item in current_valid_buckets)
    baseline_total_route_valid = sum(to_float(item.get("route_amount")) for item in baseline_valid_buckets)
    if current_total_route_valid <= 0 or baseline_total_route_valid <= 0:
        errors: list[str] = []
        if current_total_route_valid <= 0:
            errors.append("当前周期有效资方桶的路由金额合计为 0，无法做全桶分布判断。")
        if baseline_total_route_valid <= 0:
            errors.append("对比周期有效资方桶的路由金额合计为 0，无法做全桶分布判断。")
        return build_capital_failure_trace(
            headline="有效资方桶路由金额不足",
            summary="当前或对比周期的有效资方桶路由金额合计为 0，无法继续进行全桶分布比较。",
            analysis_steps=[
                stage_analysis_step(
                    step="准入资方总量判断",
                    analysis="先计算 Σ(准入资方个数桶值 × 路由金额) / Σ(路由金额) 得到加权均值（平均每单被几家资方准入）。",
                    evidence=[
                        f"当前期加权均值：{capital_total_judgement['current']} 家/单。",
                        f"对比期加权均值：{capital_total_judgement['baseline']} 家/单。",
                        f"下降量：{capital_total_judgement['drop']} 家/单。",
                        "口径说明：加权均值仅用于辅助说明资方变化，不作为第二阶段分叉终止条件。",
                    ],
                    conclusion="继续看 4-CDF 资方分布判断。",
                ),
                stage_analysis_step(
                    step="资方桶分布下行判断",
                    analysis="继续比较全桶路由金额分布前，先确认有效桶能形成非零分母。",
                    evidence=errors,
                    conclusion="有效资方桶路由金额不足，当前无法继续判断。",
                ),
            ],
            errors=errors,
            skipped_reason="capital_distribution_valid_route_missing",
            root_type="capital_distribution_valid_route_missing",
            root_message="有效资方桶路由金额为 0，无法形成全桶比较分母。",
            debug_query=_period_debug_snapshot(
                current_result=current_result,
                baseline_result=baseline_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            ),
            root_details={
                "capital_total_judgement": capital_total_judgement,
                "data_quality": data_quality,
            },
            capital_total_judgement=capital_total_judgement,
        )

    valid_bucket_keys = sorted(
        set(normalize_text(item.get("alllow_ly_cnt")) for item in current_valid_buckets)
        | set(normalize_text(item.get("alllow_ly_cnt")) for item in baseline_valid_buckets),
        key=_allow_bucket_sort_key,
    )
    current_valid_bucket_map = {
        normalize_text(item["alllow_ly_cnt"]): item
        for item in current_valid_buckets
    }
    baseline_valid_bucket_map = {
        normalize_text(item["alllow_ly_cnt"]): item
        for item in baseline_valid_buckets
    }
    bucket_stats: list[dict[str, Any]] = []
    for bucket_key in sorted(set(current_bucket_map) | set(baseline_bucket_map), key=_allow_bucket_sort_key):
        current_item = current_bucket_map.get(bucket_key, {})
        baseline_item = baseline_bucket_map.get(bucket_key, {})
        bucket_value = parse_allow_bucket(bucket_key)
        current_route_amount = to_float(current_item.get("route_amount"))
        baseline_route_amount = to_float(baseline_item.get("route_amount"))
        bucket_stats.append(
            {
                "alllow_ly_cnt": bucket_key,
                "bucket_value": round_float(bucket_value, 6),
                "current_route_count": round_float(to_float(current_item.get("route_count")), 2),
                "baseline_route_count": round_float(to_float(baseline_item.get("route_count")), 2),
                "current_route_amount": round_float(current_route_amount, 2),
                "baseline_route_amount": round_float(baseline_route_amount, 2),
                "current_acceptance_rate": round_float(current_item.get("acceptance_rate"), 6) if current_item else None,
                "baseline_acceptance_rate": round_float(baseline_item.get("acceptance_rate"), 6) if baseline_item else None,
                "current_route_share": round_float(safe_div(current_route_amount, current_total_route_all), 6),
                "baseline_route_share": round_float(safe_div(baseline_route_amount, baseline_total_route_all), 6),
                "route_share_delta": round_float(
                    safe_div(current_route_amount, current_total_route_all)
                    - safe_div(baseline_route_amount, baseline_total_route_all),
                    6,
                ),
                "current_route_share_valid_basis": round_float(
                    safe_div(current_route_amount, current_total_route_valid),
                    6,
                )
                if bucket_value is not None
                else None,
                "baseline_route_share_valid_basis": round_float(
                    safe_div(baseline_route_amount, baseline_total_route_valid),
                    6,
                )
                if bucket_value is not None
                else None,
            }
        )

    weighted_mean_current = safe_div(
        sum((parse_allow_bucket(item.get("alllow_ly_cnt")) or 0.0) * to_float(item.get("route_amount")) for item in current_valid_buckets),
        current_total_route_valid,
    )
    weighted_mean_baseline = safe_div(
        sum((parse_allow_bucket(item.get("alllow_ly_cnt")) or 0.0) * to_float(item.get("route_amount")) for item in baseline_valid_buckets),
        baseline_total_route_valid,
    )
    weighted_mean_delta = round_float(weighted_mean_current - weighted_mean_baseline, 6)
    weighted_median_current = weighted_median(
        [
            (to_float(parse_allow_bucket(item.get("alllow_ly_cnt"))), to_float(item.get("route_amount")))
            for item in current_valid_buckets
        ]
    )
    weighted_median_baseline = weighted_median(
        [
            (to_float(parse_allow_bucket(item.get("alllow_ly_cnt"))), to_float(item.get("route_amount")))
            for item in baseline_valid_buckets
        ]
    )
    weighted_median_delta = None
    if weighted_median_current is not None and weighted_median_baseline is not None:
        weighted_median_delta = round_float(weighted_median_current - weighted_median_baseline, 6)

    (
        cdf_cutoff_stats,
        effective_cutoff_count,
        effective_cutoff_hit_count,
        effective_cutoff_hit_ratio,
        max_negative_cutoff_delta,
        has_positive_cutoff_signal,
    ) = _build_cdf_cutoff_stats(
        valid_bucket_keys=valid_bucket_keys,
        current_bucket_map=current_valid_bucket_map,
        baseline_bucket_map=baseline_valid_bucket_map,
        current_total_route_valid=current_total_route_valid,
        baseline_total_route_valid=baseline_total_route_valid,
    )
    bucket_deltas_sorted = sorted(
        [
            {
                "bucket_label": item.get("alllow_ly_cnt"),
                "current_route_share": item.get("current_route_share"),
                "baseline_route_share": item.get("baseline_route_share"),
                "route_share_delta": item.get("route_share_delta"),
            }
            for item in bucket_stats
            if parse_allow_bucket(item.get("alllow_ly_cnt")) is not None
        ],
        key=lambda item: (
            -abs(to_float(item.get("route_share_delta"))),
            _allow_bucket_sort_key(normalize_text(item.get("bucket_label"))),
        ),
    )
    top_bucket_deltas = bucket_deltas_sorted[:5]
    tail_bucket_summary = _tail_bucket_summary(bucket_deltas_sorted, 5)
    low_bucket_share_current = {
        bucket_key: round_float(
            safe_div(
                sum(
                    to_float((current_valid_bucket_map.get(candidate_key) or {}).get("route_amount"))
                    for candidate_key in valid_bucket_keys
                    if to_float(parse_allow_bucket(candidate_key)) <= to_float(parse_allow_bucket(bucket_key))
                ),
                current_total_route_valid,
            ),
            6,
        )
        for bucket_key in ("2", "3")
        if bucket_key in current_valid_bucket_map or bucket_key in baseline_valid_bucket_map
    }
    low_bucket_share_baseline = {
        bucket_key: round_float(
            safe_div(
                sum(
                    to_float((baseline_valid_bucket_map.get(candidate_key) or {}).get("route_amount"))
                    for candidate_key in valid_bucket_keys
                    if to_float(parse_allow_bucket(candidate_key)) <= to_float(parse_allow_bucket(bucket_key))
                ),
                baseline_total_route_valid,
            ),
            6,
        )
        for bucket_key in ("2", "3")
        if bucket_key in current_valid_bucket_map or bucket_key in baseline_valid_bucket_map
    }
    low_bucket_share_delta = {
        key: round_float(to_float(low_bucket_share_current.get(key)) - to_float(low_bucket_share_baseline.get(key)), 6)
        for key in set(low_bucket_share_current) | set(low_bucket_share_baseline)
    }
    high_bucket_share_current = {
        bucket_key: round_float(
            safe_div(
                sum(
                    to_float((current_valid_bucket_map.get(candidate_key) or {}).get("route_amount"))
                    for candidate_key in valid_bucket_keys
                    if to_float(parse_allow_bucket(candidate_key)) >= to_float(parse_allow_bucket(bucket_key))
                ),
                current_total_route_valid,
            ),
            6,
        )
        for bucket_key in ("4", "5")
        if bucket_key in current_valid_bucket_map or bucket_key in baseline_valid_bucket_map
    }
    high_bucket_share_baseline = {
        bucket_key: round_float(
            safe_div(
                sum(
                    to_float((baseline_valid_bucket_map.get(candidate_key) or {}).get("route_amount"))
                    for candidate_key in valid_bucket_keys
                    if to_float(parse_allow_bucket(candidate_key)) >= to_float(parse_allow_bucket(bucket_key))
                ),
                baseline_total_route_valid,
            ),
            6,
        )
        for bucket_key in ("4", "5")
        if bucket_key in current_valid_bucket_map or bucket_key in baseline_valid_bucket_map
    }
    high_bucket_share_delta = {
        key: round_float(to_float(high_bucket_share_current.get(key)) - to_float(high_bucket_share_baseline.get(key)), 6)
        for key in set(high_bucket_share_current) | set(high_bucket_share_baseline)
    }
    central_tendency_down = weighted_mean_current < weighted_mean_baseline
    low_bucket_share_up = any(to_float(value) > 0 for value in low_bucket_share_delta.values())
    high_bucket_share_down = any(to_float(value) < 0 for value in high_bucket_share_delta.values())
    structural_shift_strength = round_float(
        sum(max(to_float(item.get("cdf_delta")), 0.0) for item in cdf_cutoff_stats if item.get("is_effective_cutoff")),
        6,
    )
    # 资方分布左移判断：四 CDF 条件须全部满足
    cdf_cond2_ok = effective_cutoff_hit_ratio is not None and effective_cutoff_hit_ratio >= 0.80
    cdf_cond3_ok = max_negative_cutoff_delta is not None and max_negative_cutoff_delta >= -0.03
    is_left_shift = (
        central_tendency_down
        and cdf_cond2_ok
        and cdf_cond3_ok
        and bool(has_positive_cutoff_signal)
    )
    if is_left_shift:
        distribution_decision_reason = (
            f"加权均值下降（{format_percent_or_dash(effective_cutoff_hit_ratio)} CDF 命中率），"
            f"最大反向偏离 {format_percent_or_dash(max_negative_cutoff_delta)}，"
            "存在 ≥5pp 正向偏移，四条件全部满足，判断资方分布已明显向低准入资方桶偏移；"
            "该信号进入最终归因候选，并继续进入资产维度阶段做客群结构/桶内承接率定位或反证。"
        )
    elif not central_tendency_down:
        distribution_decision_reason = "加权均值未下降，条件一未满足；继续进入资产维度确认是否存在客群结构或桶内承接率变化。"
    elif not cdf_cond2_ok:
        distribution_decision_reason = (
            f"CDF 命中率 {format_percent_or_dash(effective_cutoff_hit_ratio)} 未达到 80% 门槛，条件二未满足；"
            "继续进入资产维度确认是否存在客群结构或桶内承接率变化。"
        )
    elif not cdf_cond3_ok:
        distribution_decision_reason = (
            f"最大反向偏离 {format_percent_or_dash(max_negative_cutoff_delta)} 低于 -3pp，条件三未满足；"
            "继续进入资产维度确认是否存在客群结构或桶内承接率变化。"
        )
    else:
        distribution_decision_reason = "无 ≥5pp 正向 CDF 偏移，条件四未满足；继续进入资产维度确认是否存在客群结构或桶内承接率变化。"
    distribution_judgement = build_distribution_judgement(
        evaluated=True,
        weighted_mean_current=weighted_mean_current,
        weighted_mean_baseline=weighted_mean_baseline,
        weighted_mean_delta=weighted_mean_delta,
        weighted_median_current=weighted_median_current,
        weighted_median_baseline=weighted_median_baseline,
        weighted_median_delta=weighted_median_delta,
        low_bucket_share_current=low_bucket_share_current,
        low_bucket_share_baseline=low_bucket_share_baseline,
        low_bucket_share_delta=low_bucket_share_delta,
        high_bucket_share_current=high_bucket_share_current,
        high_bucket_share_baseline=high_bucket_share_baseline,
        high_bucket_share_delta=high_bucket_share_delta,
        low_bucket_share_up=low_bucket_share_up,
        high_bucket_share_down=high_bucket_share_down,
        central_tendency_down=central_tendency_down,
        structural_shift_strength=structural_shift_strength,
        is_left_shift=is_left_shift,
        cdf_cutoff_stats=cdf_cutoff_stats,
        effective_cutoff_count=effective_cutoff_count,
        effective_cutoff_hit_count=effective_cutoff_hit_count,
        effective_cutoff_hit_ratio=effective_cutoff_hit_ratio,
        max_negative_cutoff_delta=max_negative_cutoff_delta,
        has_positive_cutoff_signal=has_positive_cutoff_signal,
        top_bucket_deltas=top_bucket_deltas,
        tail_bucket_summary=tail_bucket_summary,
        decision_reason=distribution_decision_reason,
    )

    next_action = "run_asset"
    terminal_reason: str | None = None

    weighted_mean_conclusion = (
        f"准入资方加权均值较对比期变化 {capital_total_judgement['delta']} 家/单（下降量 {capital_total_judgement['drop']} 家/单）；"
        "该信号仅用于说明资方变化，不单独作为分叉终止条件，继续看 4-CDF 分布判断。"
    )
    analysis_steps: list[dict[str, Any]] = [
        stage_analysis_step(
            step="准入资方总量判断",
            analysis="先计算 Σ(准入资方个数桶值 × 路由金额) / Σ(路由金额) 得到加权均值（平均每单被几家资方准入）。",
            evidence=[
                f"当前期加权均值：{capital_total_judgement['current']} 家/单。",
                f"对比期加权均值：{capital_total_judgement['baseline']} 家/单。",
                f"下降量：{capital_total_judgement['drop']} 家/单。",
                "口径说明：加权均值仅用于辅助说明资方变化，不作为第二阶段分叉终止条件。",
                _normalized_signal_line(),
            ],
            conclusion=weighted_mean_conclusion,
        )
    ]
    distribution_evidence = [
        f"有效 cutoff 数：{effective_cutoff_count}，其中命中当前累计占比不低于对比期的 cutoff 数：{effective_cutoff_hit_count}，命中比例：{format_percent_or_dash(effective_cutoff_hit_ratio)}。",
        f"最大反向 cutoff 偏离：{format_percent_or_dash(max_negative_cutoff_delta)}。",
        f"是否出现 >=5% 的正向累计偏移：{format_yes_no(has_positive_cutoff_signal)}。",
        f"加权均值变化：{round_float(weighted_mean_delta, 6)}。",
    ]
    if weighted_median_delta is not None:
        distribution_evidence.append(f"加权中位数变化：{round_float(weighted_median_delta, 6)}。")
    for item in top_bucket_deltas[:3]:
        distribution_evidence.append(
            f"主桶 {normalize_text(item.get('bucket_label'))} 占比变化：{format_percent_or_dash(item.get('route_share_delta'))}。"
        )

    if is_left_shift:
        analysis_steps.append(
            stage_analysis_step(
                step="资方桶分布下行判断",
                analysis="总量结论只作为辅助信号，再按全桶路由金额占比的累计分布判断是否整体向低资方个数桶下行。",
                evidence=distribution_evidence,
                conclusion="全桶累计分布整体向低资方个数桶下行，继续进入资产维度阶段。",
            )
        )
        analysis_steps.append(
            stage_analysis_step(
                step="授用信通过率兜底",
                analysis="已经识别到资方分布下行，本步不再走通过率兜底。",
                evidence=[],
                conclusion="本步跳过，进入下一阶段。",
                status="skipped",
            )
        )
        business = business_view(
            headline="资方全桶分布明显下行，继续进入资产维度",
            summary=(
                "第二阶段先展示准入资方加权均值变化作为辅助结论，再看资方全桶分布；"
                "结果显示订单整体向低资方个数桶偏移，更像资产维度变化导致单笔可匹配资方减少。"
            ),
            evidence=[
                f"加权均值变化 {capital_total_judgement['delta']} 家/单（下降量 {capital_total_judgement['drop']} 家/单）。",
                f"有效 cutoff 命中比例 {format_percent_or_dash(effective_cutoff_hit_ratio)}，最大反向偏离 {format_percent_or_dash(max_negative_cutoff_delta)}。",
                f"加权均值变化 {round_float(weighted_mean_delta, 6)}。",
            ],
        )
        root_cause = build_root_cause(
            "allow_count_distribution_left_shift",
            "资方总量未明显收缩，但可匹配资方全桶分布向低桶偏移，需要继续看资产维度阶段。",
            slice_key=slice_key,
            slice_display=slice_display,
            capital_total_judgement=capital_total_judgement,
            distribution_judgement=distribution_judgement,
        )
    else:
        analysis_steps.append(
            stage_analysis_step(
                step="资方桶分布下行判断",
                analysis="总量结论只作为辅助信号，再按全桶路由金额占比的累计分布判断是否整体向低资方个数桶下行。",
                evidence=distribution_evidence,
                conclusion="没有看到稳定的全桶累计分布下行，当前不把资方分布作为主归因；继续进入资产维度确认是否由客群结构或桶内承接率变化解释。",
            )
        )
        analysis_steps.append(
            stage_analysis_step(
                step="资产维度定位准备",
                analysis="全桶分布未见明显下行时，下一步优先看资产维度是否存在客群占比变化或特殊桶承接率下降；若资产维度也无局部信号，再回到规则变更或授用信通过率排查。",
                evidence=[
                    "当前脚本已完成资方准入加权均值与 4-CDF 分布判断。",
                    "授用信通过率指标尚未接入，需在资产维度无解释时作为后续数据缺口处理。",
                ],
                conclusion="本切片继续进入第三阶段资产维度诊断。",
            )
        )
        business = business_view(
            headline="资方分布未见明显下行，继续进入资产维度",
            summary=(
                "第二阶段先展示准入资方加权均值变化作为辅助结论，再看资方全桶分布；"
                "全桶分布没有出现明确下行，因此资方分布暂不作为主归因，下一步继续看资产客群结构或桶内承接率变化。"
            ),
            evidence=[
                f"准入资方加权均值变化 {capital_total_judgement['delta']} 家/单（下降量 {capital_total_judgement['drop']} 家/单）。",
                f"有效 cutoff 命中比例 {format_percent_or_dash(effective_cutoff_hit_ratio)}，最大反向偏离 {format_percent_or_dash(max_negative_cutoff_delta)}。",
                "若资产维度仍无局部解释，再补查授用信通过率或规则变更。",
            ],
        )
        root_cause = build_root_cause(
            "credit_pass_rate_metric_unavailable",
            "总量和分布都未见明显异常，理论上应继续检查授用信通过率，但当前脚本尚未接入该指标。",
            slice_key=slice_key,
            slice_display=slice_display,
            capital_total_judgement=capital_total_judgement,
            distribution_judgement=distribution_judgement,
        )

    trace = {
        "context": context,
        "slice_key": slice_key,
        "slice_display": slice_display,
        "capital_distribution_stats": bucket_stats,
        "capital_total_judgement": capital_total_judgement,
        "distribution_judgement": distribution_judgement,
        "analysis_steps": analysis_steps,
        "terminal_reason": terminal_reason,
        "terminal_reason_text": build_reason(terminal_reason),
        "next_action": next_action,
        "business_view": business,
        "root_cause": root_cause,
        "errors": [],
    }
    trace = _finalize_capital_trace(trace, slice_index=slice_index, slice_total=slice_total)
    log_stage_event("capital", "阶段完成", slice_key=slice_key, trace=trace)
    return trace




def _finalize_funding_with_attribution(
    trace: dict[str, Any],
    *,
    asset_trace: dict[str, Any] | None,
    slice_index: int | None,
    slice_total: int | None,
) -> dict[str, Any]:
    trace = apply_final_attribution_to_funding_trace(trace, asset_trace)
    return finalize_funding_trace(trace, slice_index=slice_index, slice_total=slice_total)


def run_asset_stage(
    *,
    granularity: str,
    current_start: str,
    current_end: str,
    baseline_start: str,
    baseline_end: str,
    slice_key: str,
    access_token: str,
    endpoint: str | None = None,
    primary_trace: dict[str, Any] | None = None,
    capital_trace: dict[str, Any] | None = None,
    slice_index: int | None = None,
    slice_total: int | None = None,
) -> dict[str, Any]:
    slice_display = slice_key
    normalized_granularity = normalize_granularity(granularity)
    base_context = build_context(
        granularity=granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )

    def build_asset_failure_trace(
        *,
        context: dict[str, Any],
        headline: str,
        summary: str,
        root_cause: dict[str, Any],
        errors: list[str],
        debug_query: dict[str, Any] | None = None,
        slice_snapshot: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        trace = {
            "context": context,
            "slice_key": slice_key,
            "qualified_ranges": [],
            "asset_thresholds": {},
            "slice_context": {},
            "soft_signal_buckets": [],
            "factor_results": [],
            "range_results": [],
            "asset_display": build_empty_asset_display(),
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "next_action": "stop",
            "business_view": business_view(
                headline=headline,
                summary=summary,
                evidence=errors,
            ),
            "root_cause": root_cause,
            "errors": errors,
        }
        if debug_query is not None:
            trace["debug_query"] = debug_query
        if slice_snapshot is not None:
            trace["slice_snapshot"] = slice_snapshot
        return trace

    if normalized_granularity not in SUPPORTED_GRANULARITIES:
        error = unsupported_granularity_error(normalized_granularity)
        trace = build_asset_failure_trace(
            context=base_context,
            headline="当前粒度暂未接入",
            summary="当前版本仅支持日粒度和周粒度的资产维度诊断。",
            root_cause=build_root_cause(
                "unsupported_granularity",
                "资产维度阶段收到当前版本未支持的粒度。",
                granularity=normalized_granularity,
            ),
            errors=[error],
            slice_snapshot={},
        )
        trace = finalize_asset_trace(trace, slice_index=slice_index, slice_total=slice_total)
        log_stage_event("asset", "阶段失败", slice_key=slice_key, trace=trace)
        return trace
    if_irr, _, cp_dj_new = parse_slice_key(slice_key)
    slice_display = build_slice_display(if_irr, cp_dj_new=cp_dj_new)
    caller_supplied_progress = slice_index is not None and slice_total not in (None, 0)
    log_stage_event(
        "asset",
        "开始阶段",
        slice_key=slice_key,
        granularity=normalized_granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )
    inline_primary = primary_trace is None
    primary_trace = primary_trace or run_primary_stage(
        granularity=normalized_granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
        access_token=access_token,
        endpoint=endpoint,
        if_irr=if_irr,
    )
    # 二阶段已按全客群一级解析过 N/M 时优先沿用，避免此处仅用单客群一级队列长度偏短（如 1/1）
    if capital_trace:
        if slice_index is None:
            cap_si = capital_trace.get("slice_index")
            if cap_si is not None:
                slice_index = cap_si
        if slice_total is None or slice_total == 0:
            cap_st = capital_trace.get("slice_total")
            if cap_st:
                slice_total = cap_st
    if (slice_index is None or not slice_total) and primary_trace:
        derived_index, derived_total = resolve_slice_index_from_primary(primary_trace, slice_key)
        if slice_index is None:
            slice_index = derived_index
        if not slice_total:
            slice_total = derived_total
    # 脚本内自动跑了「单客群」一级时，analysis_sequence 只是该客群子队列（如精优 4 条），N/M 会偏成 1/4；
    # 未注入一级 JSON、也未传入二阶段 trace 时，用全客群一级再解析一次，与二阶段「全局异常切片队列」对齐（如 2/5）
    queue_primary: dict[str, Any] | None = None
    if inline_primary and not capital_trace and not caller_supplied_progress:
        queue_primary = run_primary_stage(
            granularity=normalized_granularity,
            current_start=current_start,
            current_end=current_end,
            baseline_start=baseline_start,
            baseline_end=baseline_end,
            access_token=access_token,
            endpoint=endpoint,
            if_irr=None,
            cp_dj_new=None,
        )
        q_di, q_dt = resolve_slice_index_from_primary(queue_primary, slice_key)
        if q_di is not None:
            slice_index = q_di
        if q_dt:
            slice_total = q_dt
    slice_snapshot = _current_slice_from_primary(primary_trace, slice_key)
    if not slice_snapshot and queue_primary is not None:
        slice_snapshot = _current_slice_from_primary(queue_primary, slice_key)
    # 二阶段只要数仓能按 slice_key 过滤即可跑通；三阶段必须在「一级切片队列」里命中快照。
    # 若单客群一级未收录该切片（边界阈值/与全客群一级不一致）、或注入的一级 JSON 缺行，仍缺快照则一律再跑全客群一级补查找（不论是否已传 capital_trace）。
    if not slice_snapshot:
        if queue_primary is None:
            queue_primary = run_primary_stage(
                granularity=normalized_granularity,
                current_start=current_start,
                current_end=current_end,
                baseline_start=baseline_start,
                baseline_end=baseline_end,
                access_token=access_token,
                endpoint=endpoint,
                if_irr=None,
                cp_dj_new=None,
            )
        slice_snapshot = _current_slice_from_primary(queue_primary, slice_key)
    if not slice_snapshot:
        context = primary_trace.get("context", base_context)
        seq_a = primary_trace.get("analysis_sequence") or []
        seq_l = primary_trace.get("analysis_sequence_lookup") or []
        seq_q: list[Any] = []
        if queue_primary:
            seq_q = list(queue_primary.get("analysis_sequence") or []) + list(
                queue_primary.get("analysis_sequence_lookup") or []
            )
        available_slice_keys = [
            item.get("slice_key", "")
            for item in list(seq_a) + list(seq_l) + list(seq_q)
        ]
        trace = build_asset_failure_trace(
            context=context,
            headline="没拿到这组订单的一级快照",
            summary="当前无法继续做资产维度诊断，常见原因是切片写法和一级结果不一致，或者一级诊断里本来就没有取到这组订单。",
            root_cause=build_root_cause(
                "missing_primary_snapshot",
                "资产阶段没有在一级诊断结果中找到对应切片快照。",
                requested_slice_key=slice_key,
                requested_slice_display=slice_display,
                available_slice_keys=available_slice_keys[:20],
                primary_row_count=len(available_slice_keys),
            ),
            errors=[
                f"请求切片：{slice_display}。",
                f"一级结果中的候选切片数：{len(available_slice_keys)}。",
                f"一级诊断结果中未找到切片 {slice_key}。",
            ],
            slice_snapshot={},
        )
        trace = finalize_asset_trace(trace, slice_index=slice_index, slice_total=slice_total)
        log_stage_event("asset", "阶段失败", slice_key=slice_key, trace=trace)
        return trace

    current_period = primary_trace["context"]["current_period"]
    baseline_period = primary_trace["context"]["baseline_period"]
    metrics = [
        client.metric(METRIC_ACCEPTANCE_RATE),
        client.metric(METRIC_ROUTING_AMOUNT),
    ]
    dimensions = build_main_dimensions(granularity=normalized_granularity, include_asset=True)
    current_filter = build_main_rules(
        start=current_period["start"],
        end=current_period["end"],
        if_irr=if_irr,
        cp_dj_new=cp_dj_new,
    )
    baseline_filter = build_main_rules(
        start=baseline_period["start"],
        end=baseline_period["end"],
        if_irr=if_irr,
        cp_dj_new=cp_dj_new,
    )
    current_result, current_error = _query_rows(
        access_token=access_token,
        metric_list=metrics,
        dimension_list=dimensions,
        filter_payload=current_filter,
        endpoint=endpoint,
    )
    baseline_result, baseline_error = _query_rows(
        access_token=access_token,
        metric_list=metrics,
        dimension_list=dimensions,
        filter_payload=baseline_filter,
        endpoint=endpoint,
    )

    if current_error or baseline_error:
        query_errors = [item for item in [current_error, baseline_error] if item]
        trace = build_asset_failure_trace(
            context=primary_trace["context"],
            headline="没拿到这组订单的资产维度分析结果",
            summary="当前无法完成这组订单的资产维度诊断，因为资产维度查询本身失败了。",
            root_cause=build_root_cause(
                "query_error",
                "资产维度查询失败。",
                slice_key=slice_key,
                slice_display=slice_display,
                current_error=current_error,
                baseline_error=baseline_error,
            ),
            errors=query_errors,
            debug_query=_period_debug_snapshot(
                current_result=current_result,
                baseline_result=baseline_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            ),
            slice_snapshot=slice_snapshot,
        )
        trace = finalize_asset_trace(trace, slice_index=slice_index, slice_total=slice_total)
        log_stage_event("asset", "阶段失败", slice_key=slice_key, trace=trace)
        return trace

    current_records = _prepare_asset_records(current_result.get("rows", []))
    baseline_records = _prepare_asset_records(baseline_result.get("rows", []))
    if not current_records or not baseline_records:
        errors: list[str] = []
        if not current_records:
            errors.append("当前周期没有拿到这组订单的资产维度数据。")
        if not baseline_records:
            errors.append("对比周期没有拿到这组订单的资产维度数据。")
        trace = build_asset_failure_trace(
            context=primary_trace["context"],
            headline="没拿到这组订单的资产维度数据",
            summary="当前期或对比期缺少这组订单的可比资产维度数据，暂时不能继续判断是不是资产维度变化导致下降。",
            root_cause=build_root_cause(
                "missing_slice_data",
                "资产维度阶段缺少当前期或对比期切片数据。",
                slice_key=slice_key,
                slice_display=slice_display,
                current_row_count=len(current_records),
                baseline_row_count=len(baseline_records),
                current_period=current_period,
                baseline_period=baseline_period,
            ),
            errors=errors,
            debug_query=_period_debug_snapshot(
                current_result=current_result,
                baseline_result=baseline_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            ),
            slice_snapshot=slice_snapshot,
        )
        trace = finalize_asset_trace(trace, slice_index=slice_index, slice_total=slice_total)
        log_stage_event("asset", "阶段失败", slice_key=slice_key, trace=trace)
        return trace

    current_slice_rate = to_float(slice_snapshot.get("current_rate"))
    baseline_slice_rate = to_float(slice_snapshot.get("baseline_rate"))
    current_slice_route_amount = to_float(slice_snapshot.get("current_route_amount"))
    current_slice_drag_amount = to_float(slice_snapshot.get("drag_amount"))
    asset_thresholds = _build_asset_thresholds(current_slice_drag_amount=current_slice_drag_amount)
    slice_context = _build_asset_slice_context(
        current_slice_rate=current_slice_rate,
        baseline_slice_rate=baseline_slice_rate,
        current_slice_route_amount=current_slice_route_amount,
        current_slice_drag_amount=current_slice_drag_amount,
    )

    raw_summaries, all_five_raw_gate = compute_asset_raw_volume_gate(
        current_result.get("rows", []),
        baseline_result.get("rows", []),
        current_slice_rate,
    )
    if all_five_raw_gate:
        pattern_info_r12 = compute_asset_r12_pattern_info()
        asset_display = _build_asset_display_r12(
            slice_display=slice_display,
            slice_context=slice_context,
            factor_summaries=raw_summaries,
            capital_trace=capital_trace,
        )
        trace_r12: dict[str, Any] = {
            "slice_key": slice_key,
            "slice_display": slice_display,
            "qualified_ranges": [],
            "factor_results": [],
            "range_results": [],
            "asset_thresholds": asset_thresholds,
            "slice_context": slice_context,
            "soft_signal_buckets": [],
            "asset_display": asset_display,
            "terminal_reason": "R12",
            "terminal_reason_text": build_reason("R12"),
            "next_action": "stop",
            "root_cause": build_root_cause(
                "all_factors_raw_volume_decline",
                "五个资产维度原始桶均满足体积规则普降；承接走弱更符合资方准入/规则在多桶同步传导，本技能不自动进入第四阶段资金闭环。",
                slice_key=slice_key,
                slice_display=slice_display,
                raw_volume_gate_summaries=raw_summaries,
            ),
            "context": primary_trace["context"],
            "raw_volume_gate_summaries": raw_summaries,
            **pattern_info_r12,
        }
        if capital_trace is not None:
            trace_r12["stage2_signal"] = capital_trace.get("stage2_signal")
        trace_r12 = finalize_asset_trace(trace_r12, slice_index=slice_index, slice_total=slice_total)
        log_stage_event("asset", "阶段完成", slice_key=slice_key, trace=trace_r12)
        return trace_r12

    deep_chain_factor_keys = [
        normalize_text(item.get("factor_key"))
        for item in raw_summaries
        if not item.get("raw_volume_decline")
    ]
    factor_results, hit_buckets = _build_factor_results(
        current_records=current_records,
        baseline_records=baseline_records,
        current_slice_rate=current_slice_rate,
        baseline_slice_rate=baseline_slice_rate,
        current_slice_route_amount=current_slice_route_amount,
        asset_thresholds=asset_thresholds,
        factor_keys=deep_chain_factor_keys,
    )
    range_results, qualified_ranges = _build_range_results(
        hits=hit_buckets,
        current_records=current_records,
        baseline_records=baseline_records,
        current_slice_route_amount=current_slice_route_amount,
        current_slice_rate=current_slice_rate,
        asset_thresholds=asset_thresholds,
    )
    hit_factor_results = [item for item in factor_results if item["final_decision"] == "hit"]
    strongest_hit_buckets = sorted(
        [
            dict(bucket)
            for factor_result in hit_factor_results
            for bucket in factor_result["buckets"]
            if bucket["is_hit"]
        ],
        key=lambda item: max(to_float(item["structural_impact"]), to_float(item["perf_decline_impact"])),
        reverse=True,
    )
    soft_signal_buckets = sorted(
        [
            dict(bucket)
            for factor_result in factor_results
            for bucket in factor_result["buckets"]
            if bucket.get("is_near_miss")
        ],
        key=lambda item: max(to_float(item["structural_impact"]), to_float(item["perf_decline_impact"])),
        reverse=True,
    )

    terminal_reason: str | None = None
    next_action = "run_funding"
    root_cause: dict[str, Any] | None = None
    if not hit_factor_results:
        terminal_reason = "R4b"
        next_action = "stop"
        if soft_signal_buckets:
            root_cause = build_root_cause(
                "asset_dimension_signals_below_bucket_threshold",
                "资产维度发现了若干疑似异常桶，但单桶影响承接金额估算均未达到识别门槛。",
                slice_key=slice_key,
                slice_display=slice_display,
                bucket_drag_absolute_threshold=ASSET_BUCKET_DRAG_ABSOLUTE_THRESHOLD,
                bucket_drag_relative_threshold=ASSET_BUCKET_DRAG_RELATIVE_THRESHOLD,
                bucket_drag_effective_threshold=asset_thresholds["bucket"]["effective"],
                slice_drag_amount=round_float(current_slice_drag_amount, 2),
                strongest_near_misses=[
                    {
                        "factor_label": normalize_text(item.get("factor_label")),
                        "bucket_label": normalize_text(item.get("bucket_label")),
                        "structural_impact": round_float(to_float(item.get("structural_impact")), 2),
                        "perf_decline_impact": round_float(to_float(item.get("perf_decline_impact")), 2),
                        "impact_threshold": round_float(to_float(item.get("impact_threshold")), 2),
                    }
                    for item in soft_signal_buckets[:5]
                ],
            )
        else:
            root_cause = build_root_cause(
                "no_asset_dimension_anomaly",
                "资产维度里没有发现达到识别门槛的异常桶。",
                slice_key=slice_key,
                slice_display=slice_display,
                bucket_drag_absolute_threshold=ASSET_BUCKET_DRAG_ABSOLUTE_THRESHOLD,
                bucket_drag_relative_threshold=ASSET_BUCKET_DRAG_RELATIVE_THRESHOLD,
                bucket_drag_effective_threshold=asset_thresholds["bucket"]["effective"],
                slice_drag_amount=round_float(current_slice_drag_amount, 2),
            )
    elif not qualified_ranges:
        terminal_reason = "R5"
        next_action = "stop"
        root_cause = build_root_cause(
            "asset_dimension_changes_below_range_threshold",
            "资产维度已经出现异常桶，但没有锁定到当前路由金额达到100万的最小因子范围。",
            slice_key=slice_key,
            slice_display=slice_display,
            range_route_amount_threshold=asset_thresholds["range"]["effective"],
            slice_drag_amount=round_float(current_slice_drag_amount, 2),
            strongest_hits=[
                {
                    "factor_label": normalize_text(item.get("factor_label")),
                    "bucket_label": normalize_text(item.get("bucket_label")),
                    "structural_impact": round_float(to_float(item.get("structural_impact")), 2),
                    "perf_decline_impact": round_float(to_float(item.get("perf_decline_impact")), 2),
                    "impact_threshold": round_float(to_float(item.get("impact_threshold")), 2),
                }
                for item in strongest_hit_buckets[:5]
            ],
            strongest_candidate_ranges=[
                {
                    "range_display": normalize_text(item.get("range_display")),
                    "factor_count": int(item.get("factor_count", 0)),
                    "current_route_amount": round_float(to_float(item.get("current_route_amount")), 2),
                    "route_amount_threshold": round_float(
                        to_float(item.get("route_amount_threshold")), 2
                    ),
                    "share_delta": round_float(to_float(item.get("share_delta")), 6),
                }
                for item in range_results[:5]
            ],
        )
    pattern_info = compute_asset_dimension_pattern(factor_results)
    asset_display = _build_asset_display(
        slice_display=slice_display,
        slice_context=slice_context,
        asset_thresholds=asset_thresholds,
        factor_results=factor_results,
        range_results=range_results,
        qualified_ranges=qualified_ranges,
        soft_signal_buckets=soft_signal_buckets,
        terminal_reason=terminal_reason,
        asset_dimension_pattern=pattern_info.get("asset_dimension_pattern"),
        asset_dimension_pattern_label=pattern_info.get("asset_dimension_pattern_label"),
        raw_volume_gate_summaries=raw_summaries,
    )
    trace = {
        "slice_key": slice_key,
        "qualified_ranges": qualified_ranges,
        "factor_results": factor_results,
        "asset_display": asset_display,
        "terminal_reason": terminal_reason,
        "next_action": next_action,
        "root_cause": root_cause,
        "context": primary_trace["context"],
        "raw_volume_gate_summaries": raw_summaries,
        "asset_deep_chain_factor_keys": deep_chain_factor_keys,
        **pattern_info,
    }
    if capital_trace is not None:
        trace["stage2_signal"] = capital_trace.get("stage2_signal")
    trace = finalize_asset_trace(trace, slice_index=slice_index, slice_total=slice_total)
    log_stage_event("asset", "阶段完成", slice_key=slice_key, trace=trace)
    return trace




def run_funding_stage(
    *,
    granularity: str,
    current_start: str,
    current_end: str,
    baseline_start: str,
    baseline_end: str,
    slice_key: str,
    range_id: str | None,
    range_key: str | None,
    access_token: str,
    endpoint: str | None = None,
    asset_trace: dict[str, Any] | None = None,
    capital_trace: dict[str, Any] | None = None,
    slice_index: int | None = None,
    slice_total: int | None = None,
) -> dict[str, Any]:
    normalized_granularity = normalize_granularity(granularity)
    if normalized_granularity not in SUPPORTED_GRANULARITIES:
        context = build_context(
            granularity=granularity,
            current_start=current_start,
            current_end=current_end,
            baseline_start=baseline_start,
            baseline_end=baseline_end,
        )
        error = unsupported_granularity_error(normalized_granularity)
        trace = {
            "context": context,
            "slice_key": slice_key,
            "range_id": normalize_text(range_id),
            "range_key": normalize_text(range_key),
            "range_display": "",
            "matched_projects": [],
            "funding_amount_delta": None,
            "project_count_delta": None,
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "business_view": business_view(
                headline="当前粒度暂未接入",
                summary="当前版本仅支持日粒度和周粒度的第四阶段闭环分析。",
                evidence=[error],
            ),
            "root_cause": build_root_cause(
                "unsupported_granularity",
                "第四阶段收到当前版本未支持的粒度。",
                granularity=normalized_granularity,
            ),
            "errors": [error],
        }
        trace = _finalize_funding_with_attribution(
            trace, asset_trace=None, slice_index=slice_index, slice_total=slice_total
        )
        log_stage_event("funding", "阶段失败", slice_key=slice_key, trace=trace)
        return trace
    normalized_range_id = normalize_text(range_id)
    normalized_range_key = normalize_text(range_key)
    requested_range_ref = normalized_range_key or normalized_range_id
    log_stage_event(
        "funding",
        "开始阶段",
        slice_key=slice_key,
        range_id=normalized_range_id,
        range_key=normalized_range_key,
        granularity=normalized_granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
    )
    asset_trace = asset_trace or run_asset_stage(
        granularity=granularity,
        current_start=current_start,
        current_end=current_end,
        baseline_start=baseline_start,
        baseline_end=baseline_end,
        slice_key=slice_key,
        access_token=access_token,
        endpoint=endpoint,
        capital_trace=capital_trace,
        slice_index=slice_index,
        slice_total=slice_total,
    )
    if slice_index is None:
        slice_index = asset_trace.get("slice_index")
    if not slice_total:
        slice_total = asset_trace.get("slice_total")
    qualified_ranges = asset_trace.get("qualified_ranges", [])
    if not qualified_ranges:
        abnormal_factor_labels = [
            normalize_text(item.get("factor_label"))
            for item in asset_trace.get("factor_results", [])
            if normalize_text(item.get("final_decision")) == "hit"
        ]
        evidence: list[str] = []
        if abnormal_factor_labels:
            evidence.append(f'资产维度阶段只命中了这些异常维度：{"、".join(label for label in abnormal_factor_labels if label)}。')
        evidence.append("但资产维度阶段没有产出当前路由金额达到100万、可进入第四阶段的最小因子范围。")
        if requested_range_ref:
            evidence.append(f"当前请求的范围引用：{requested_range_ref}。")
        log_stage_event(
            "funding",
            "阶段失败",
            slice_key=slice_key,
            range_id=normalized_range_id,
            range_key=normalized_range_key,
            error="资产阶段没有产出可闭环范围",
        )
        trace = {
            "slice_key": slice_key,
            "range_id": normalized_range_id,
            "range_key": normalized_range_key,
            "range_display": "",
            "matched_projects": [],
            "funding_amount_delta": None,
            "project_count_delta": None,
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "business_view": business_view(
                headline="当前不该进入资金闭环阶段",
                summary="资产维度阶段只识别到异常维度，还没有形成当前路由金额达到100万、满足第四阶段门槛的最小因子范围，因此当前不能继续往下跑。",
                evidence=evidence,
            ),
            "root_cause": build_root_cause(
                "missing_qualified_ranges",
                "资产阶段未产出可进入第四阶段的最小因子范围。",
                slice_key=slice_key,
                requested_range_id=normalized_range_id,
                requested_range_key=normalized_range_key,
                abnormal_factor_labels=[label for label in abnormal_factor_labels if label],
                asset_terminal_reason=asset_trace.get("terminal_reason"),
                asset_next_action=asset_trace.get("next_action"),
            ),
            "errors": ["资产阶段没有产出 qualified_ranges，不能继续运行 funding。"],
        }
        trace = _finalize_funding_with_attribution(
            trace, asset_trace=asset_trace, slice_index=slice_index, slice_total=slice_total
        )
        return trace

    range_item = None
    if normalized_range_key:
        range_item = next(
            (item for item in qualified_ranges if normalize_text(item.get("range_key")) == normalized_range_key),
            None,
        )
    elif normalized_range_id:
        range_item = next(
            (item for item in qualified_ranges if normalize_text(item.get("range_id")) == normalized_range_id),
            None,
        )
    if range_item is None:
        available_range_refs = [
            {
                "range_id": normalize_text(item.get("range_id")),
                "range_key": normalize_text(item.get("range_key")),
                "range_display": normalize_text(item.get("range_display")),
            }
            for item in qualified_ranges
        ]
        log_stage_event(
            "funding",
            "阶段失败",
            slice_key=slice_key,
            range_id=normalized_range_id,
            range_key=normalized_range_key,
            error=f"未在 asset trace 中找到范围 {requested_range_ref}",
        )
        trace = {
            "slice_key": slice_key,
            "range_id": normalized_range_id,
            "range_key": normalized_range_key,
            "range_display": "",
            "matched_projects": [],
            "funding_amount_delta": None,
            "project_count_delta": None,
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "business_view": business_view(
                headline="资金闭环失败",
                summary="当前请求的范围引用和资产阶段真实产出的可闭环范围对不上，无法继续做第四阶段闭环。",
                evidence=[
                    f"当前请求的范围引用：{requested_range_ref}。",
                    f"资产阶段可用范围数：{len(available_range_refs)}。",
                ],
            ),
            "root_cause": build_root_cause(
                "range_reference_mismatch",
                "资金阶段收到的范围引用与资产阶段产出的 qualified_ranges 不一致。",
                slice_key=slice_key,
                requested_range_id=normalized_range_id,
                requested_range_key=normalized_range_key,
                available_ranges=available_range_refs,
            ),
            "errors": [f"未在 asset trace 中找到范围 {requested_range_ref}。"],
        }
        trace = _finalize_funding_with_attribution(
            trace, asset_trace=asset_trace, slice_index=slice_index, slice_total=slice_total
        )
        return trace

    unsupported_items = [
        item for item in range_item["factor_items"]
        if item["factor_key"] not in FUNDING_SUPPORTED_FACTORS
    ]
    if unsupported_items:
        unsupported_labels = [item["factor_label"] for item in unsupported_items]
        unsupported_keys = [item["factor_key"] for item in unsupported_items]
        # 构建「缺少哪个资金表字段」的映射提示
        _missing_field_hints = {
            "edu_rand": "资金表缺少「金额区间」维度字段，无法映射高额区间桶",
            "reloan_price_tag": "资金表缺少「风险评级」维度字段，无法映射风险评级桶",
        }
        manual_verify_hints = []
        for key in unsupported_keys:
            hint = _missing_field_hints.get(key)
            if hint:
                manual_verify_hints.append(hint)
        manual_verify_text = (
            "建议手工交叉验证：在资金项目数据中按「"
            + "、".join(unsupported_labels)
            + "」因子手动筛选对应资方项目，对比两期放款金额和项目数变化。"
        )
        log_stage_event(
            "funding",
            "阶段失败",
            slice_key=slice_key,
            range_id=normalize_text(range_item.get("range_id")),
            range_key=normalize_text(range_item.get("range_key")),
            unsupported_factors=unsupported_labels,
        )
        evidence_lines = [
            f'未支持因子：{", ".join(unsupported_labels)}。',
        ]
        evidence_lines.extend(manual_verify_hints)
        evidence_lines.append(manual_verify_text)
        trace = {
            "slice_key": slice_key,
            "range_id": normalize_text(range_item.get("range_id")),
            "range_key": normalize_text(range_item.get("range_key")),
            "range_display": normalize_text(range_item.get("range_display")),
            "matched_projects": [],
            "funding_amount_delta": None,
            "project_count_delta": None,
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "unsupported_factors": unsupported_labels,
            "business_view": business_view(
                headline="当前范围因字段缺失暂无法自动闭环，需手工验证",
                summary=(
                    f'该最小因子范围包含当前版本资金表尚未接入对应维度字段的因子（{", ".join(unsupported_labels)}），'
                    "脚本无法自动完成敏感资方侧闭环，这不代表没有资方侧问题，需手工进一步验证。"
                ),
                evidence=evidence_lines,
            ),
            "root_cause": build_root_cause(
                "unsupported_funding_factors",
                (
                    f'资金闭环阶段缺少以下因子对应的资金表映射字段：{", ".join(unsupported_labels)}；'
                    "当前版本仅支持「身份证有效性 / 高龄 / 特殊区域」三类因子的自动闭环。"
                ),
                slice_key=slice_key,
                range_id=normalize_text(range_item.get("range_id")),
                range_key=normalize_text(range_item.get("range_key")),
                unsupported_factors=unsupported_labels,
                manual_verify_guide=manual_verify_text,
            ),
            "errors": [
                f'范围 {normalize_text(range_item.get("range_id"))} 包含当前版本资金表字段未覆盖的因子：'
                f'{", ".join(unsupported_labels)}；需手工验证。'
            ],
        }
        trace = _finalize_funding_with_attribution(
            trace, asset_trace=asset_trace, slice_index=slice_index, slice_total=slice_total
        )
        return trace

    asset_slice_key = normalize_text(asset_trace.get("slice_key")) or slice_key
    asset_if_irr, _, cp_dj_new = parse_slice_key(asset_slice_key)
    if not asset_if_irr:
        asset_if_irr = normalize_text(asset_trace.get("slice_snapshot", {}).get("if_irr"))
    if not cp_dj_new:
        cp_dj_new = normalize_text(asset_trace.get("slice_snapshot", {}).get("cp_dj_new"))
    target_cp_dj = normalize_cp_dj(cp_dj_new)
    current_period = asset_trace["context"]["current_period"]
    baseline_period = asset_trace["context"]["baseline_period"]

    metrics = [client.metric(METRIC_FUNDING_AMOUNT, "放款金额-资金项目", "simple")]
    dimensions = build_funding_dimensions()
    current_filter = build_funding_rules(
        start=current_period["start"],
        end=current_period["end"],
        kequn_tag=asset_if_irr,
    )
    baseline_filter = build_funding_rules(
        start=baseline_period["start"],
        end=baseline_period["end"],
        kequn_tag=asset_if_irr,
    )
    current_result, current_error = _query_rows(
        access_token=access_token,
        metric_list=metrics,
        dimension_list=dimensions,
        filter_payload=current_filter,
        endpoint=endpoint,
    )
    baseline_result, baseline_error = _query_rows(
        access_token=access_token,
        metric_list=metrics,
        dimension_list=dimensions,
        filter_payload=baseline_filter,
        endpoint=endpoint,
    )

    if current_error or baseline_error:
        log_stage_event(
            "funding",
            "阶段失败",
            slice_key=slice_key,
            range_id=normalize_text(range_item.get("range_id")),
            range_key=normalize_text(range_item.get("range_key")),
            errors=[item for item in [current_error, baseline_error] if item],
        )
        trace = {
            "slice_key": slice_key,
            "range_id": normalize_text(range_item.get("range_id")),
            "range_key": normalize_text(range_item.get("range_key")),
            "range_display": normalize_text(range_item.get("range_display")),
            "matched_projects": [],
            "funding_amount_delta": None,
            "project_count_delta": None,
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "business_view": business_view(
                headline="资金项目查询失败",
                summary="当前无法完成该最小因子范围的敏感资方侧闭环判断。",
                evidence=[item for item in [current_error, baseline_error] if item],
            ),
            "root_cause": build_root_cause(
                "query_error",
                "资金项目查询失败。",
                slice_key=slice_key,
                range_id=normalize_text(range_item.get("range_id")),
                range_key=normalize_text(range_item.get("range_key")),
                current_error=current_error,
                baseline_error=baseline_error,
            ),
            "errors": [item for item in [current_error, baseline_error] if item],
        }
        dq = _period_debug_snapshot(
            current_result=current_result,
            baseline_result=baseline_result,
            current_filter=current_filter,
            baseline_filter=baseline_filter,
        )
        if dq is not None:
            trace["debug_query"] = dq
        trace = _finalize_funding_with_attribution(
            trace, asset_trace=asset_trace, slice_index=slice_index, slice_total=slice_total
        )
        return trace

    def normalize_funding_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        expected_kequn_tag = normalize_text(asset_if_irr)
        query_kequn_tag = normalize_funding_kequn_tag(asset_if_irr)
        raw_detail_row_count = len(rows)
        kequn_filtered_rows: list[dict[str, Any]] = []
        for row in rows:
            row_kequn_tag = normalize_text(client.extract_row_value(row, "kequn_tag"))
            if (
                expected_kequn_tag
                and row_kequn_tag
                and normalize_slice_component(row_kequn_tag) != normalize_slice_component(expected_kequn_tag)
            ):
                continue
            kequn_filtered_rows.append(row)

        normalized: list[dict[str, Any]] = []
        for row in kequn_filtered_rows:
            normalized_cp_dj = normalize_cp_dj(client.extract_row_value(row, "cp_dj"))
            if normalized_cp_dj != target_cp_dj:
                continue
            project_row = {
                "kequn_tag": normalize_text(client.extract_row_value(row, "kequn_tag")),
                "capital_project_name": normalize_text(client.extract_row_value(row, "capital_project_name")),
                "age_range": normalize_text(client.extract_row_value(row, "age_range")),
                "allow_identity_city_prov": normalize_text(client.extract_row_value(row, "allow_identity_city_prov")),
                "chk_identity_card_effc_term_floor_days": normalize_text(client.extract_row_value(row, "chk_identity_card_effc_term_floor_days")),
                "cp_dj": normalize_text(client.extract_row_value(row, "cp_dj")),
                "funding_amount": to_float(client.extract_row_value(row, METRIC_FUNDING_AMOUNT)),
            }
            normalized.append(project_row)
        return normalized, {
            "raw_detail_row_count": raw_detail_row_count,
            "kequn_tag_filtered_row_count": len(kequn_filtered_rows),
            "cp_dj_filtered_row_count": len(normalized),
            "expected_kequn_tag": expected_kequn_tag,
            "query_kequn_tag": query_kequn_tag,
            "target_cp_dj": target_cp_dj,
        }

    current_projects, current_debug = normalize_funding_rows(current_result.get("rows", []))
    baseline_projects, baseline_debug = normalize_funding_rows(baseline_result.get("rows", []))

    def is_sensitive(project_row: dict[str, Any]) -> bool:
        return all(_project_sensitive_to_factor(project_row, factor_item) for factor_item in range_item["factor_items"])

    current_matched = [item for item in current_projects if is_sensitive(item)]
    baseline_matched = [item for item in baseline_projects if is_sensitive(item)]
    current_debug["sensitive_hit_row_count"] = len(current_matched)
    baseline_debug["sensitive_hit_row_count"] = len(baseline_matched)
    funding_debug = {
        "current": current_debug,
        "baseline": baseline_debug,
    }
    if not current_matched and not baseline_matched:
        factor_count = len(range_item.get("factor_items", []))
        factor_labels_in_range = [
            normalize_text(item.get("factor_label"))
            for item in range_item.get("factor_items", [])
            if normalize_text(item.get("factor_label"))
        ]
        if factor_count > 1:
            no_match_summary = (
                f"当前最小因子范围由 {factor_count} 个因子条件 AND 组合而成"
                f"（{'、'.join(factor_labels_in_range)}），"
                "资金项目表中未找到同时满足所有条件的敏感资方项目。"
                "这不代表该方向没有资方侧问题，可能是交叉条件过于严格导致无法自动匹配，"
                "建议分因子逐一手动查询资金项目数据核查。"
            )
        else:
            no_match_summary = (
                "当前字段条件下未识别出与该最小因子范围直接对应的敏感资方相关项目，"
                "暂时无法完成敏感资方侧闭环。"
            )
        no_match_evidence = [
            f"范围：{normalize_text(range_item.get('range_display')) or normalize_text(range_item.get('range_id'))}。",
        ]
        if factor_count > 1:
            no_match_evidence.append(
                f"建议逐因子手动核查：{'、'.join(factor_labels_in_range)}，"
                "在资金项目报表中分别筛选对应条件，比对两期放款金额和项目数。"
            )
        log_stage_event(
            "funding",
            "阶段失败",
            slice_key=slice_key,
            range_id=normalize_text(range_item.get("range_id")),
            range_key=normalize_text(range_item.get("range_key")),
            error=f'未找到与范围 {normalize_text(range_item.get("range_id"))} 匹配的敏感资方相关项目',
        )
        trace = {
            "slice_key": slice_key,
            "range_id": normalize_text(range_item.get("range_id")),
            "range_key": normalize_text(range_item.get("range_key")),
            "range_display": normalize_text(range_item.get("range_display")),
            "matched_projects": [],
            "funding_amount_delta": None,
            "project_count_delta": None,
            "terminal_reason": "R8",
            "terminal_reason_text": build_reason("R8"),
            "business_view": business_view(
                headline="未找到对应敏感资方相关项目",
                summary=no_match_summary,
                evidence=no_match_evidence,
            ),
            "root_cause": build_root_cause(
                "no_sensitive_projects_matched",
                "资金模型中没有识别到与该最小因子范围直接对应的敏感资方相关项目。",
                slice_key=slice_key,
                range_id=normalize_text(range_item.get("range_id")),
                range_key=normalize_text(range_item.get("range_key")),
                range_display=normalize_text(range_item.get("range_display")),
                factor_count=factor_count,
                **({"funding_debug": funding_debug} if ENABLE_ANALYSIS_DEBUG_OUTPUT else {}),
            ),
            "errors": [f'未找到与范围 {normalize_text(range_item.get("range_id"))} 匹配的敏感资方相关项目。'],
        }
        if ENABLE_ANALYSIS_DEBUG_OUTPUT:
            trace["funding_debug"] = funding_debug
            dq = _period_debug_snapshot(
                current_result=current_result,
                baseline_result=baseline_result,
                current_filter=current_filter,
                baseline_filter=baseline_filter,
            )
            if dq is not None:
                trace["debug_query"] = dq
        trace = _finalize_funding_with_attribution(
            trace, asset_trace=asset_trace, slice_index=slice_index, slice_total=slice_total
        )
        return trace

    grouped_projects: dict[str, dict[str, Any]] = {}
    for row in baseline_matched:
        project_name = row["capital_project_name"] or "UNKNOWN"
        grouped = grouped_projects.setdefault(
            project_name,
            {"capital_project_name": project_name, "baseline_funding_amount": 0.0, "current_funding_amount": 0.0},
        )
        grouped["baseline_funding_amount"] += row["funding_amount"]
    for row in current_matched:
        project_name = row["capital_project_name"] or "UNKNOWN"
        grouped = grouped_projects.setdefault(
            project_name,
            {"capital_project_name": project_name, "baseline_funding_amount": 0.0, "current_funding_amount": 0.0},
        )
        grouped["current_funding_amount"] += row["funding_amount"]

    matched_projects = sorted(
        [
            {
                "capital_project_name": project_name,
                "baseline_funding_amount": round_float(values["baseline_funding_amount"], 2),
                "current_funding_amount": round_float(values["current_funding_amount"], 2),
                "funding_amount_delta": round_float(values["current_funding_amount"] - values["baseline_funding_amount"], 2),
            }
            for project_name, values in grouped_projects.items()
        ],
        key=lambda item: abs(to_float(item["funding_amount_delta"])),
        reverse=True,
    )

    baseline_total = sum(to_float(item["baseline_funding_amount"]) for item in matched_projects)
    current_total = sum(to_float(item["current_funding_amount"]) for item in matched_projects)
    baseline_project_count = sum(1 for item in matched_projects if to_float(item["baseline_funding_amount"]) > 0)
    current_project_count = sum(1 for item in matched_projects if to_float(item["current_funding_amount"]) > 0)
    funding_amount_delta = current_total - baseline_total
    project_count_delta = current_project_count - baseline_project_count

    # 放款金额变化幅度（绝对值 + 相对比例）
    funding_amount_delta_ratio: float | None = (
        round_float(funding_amount_delta / baseline_total, 4) if baseline_total and baseline_total != 0 else None
    )
    funding_amount_delta_pct_text = (
        f"{round_float(funding_amount_delta_ratio * 100, 1)}%"
        if funding_amount_delta_ratio is not None
        else "-"
    )
    _fmt_amount = lambda v: f"{round_float(v / 1e4, 2)} 万" if abs(v) >= 1e4 else f"{round_float(v, 2)}"
    funding_amount_evidence = [
        f"对比期敏感资方项目放款总额：{_fmt_amount(baseline_total)}；当前期：{_fmt_amount(current_total)}。",
        # 放款金额变化是第四阶段最关键的判断依据，整行加粗便于一眼定位
        f"**放款金额变化：{_fmt_amount(funding_amount_delta)}（{'+' if funding_amount_delta >= 0 else ''}{funding_amount_delta_pct_text}）。**",
        f"对比期敏感项目数：{baseline_project_count}；当前期：{current_project_count}，变化 {'+' if project_count_delta >= 0 else ''}{project_count_delta}。",
    ]
    # 逐项目明细（最多展示 5 个，保持可读性）
    for proj in matched_projects[:5]:
        proj_name = normalize_text(proj.get("capital_project_name")) or "未知项目"
        b_amt = to_float(proj.get("baseline_funding_amount"))
        c_amt = to_float(proj.get("current_funding_amount"))
        d_amt = c_amt - b_amt
        d_pct = f"{round_float(d_amt / b_amt * 100, 1)}%" if b_amt else "-"
        funding_amount_evidence.append(
            f"  • {proj_name}：对比期 {_fmt_amount(b_amt)} → 当前期 {_fmt_amount(c_amt)}，变化 {_fmt_amount(d_amt)}（{'+' if d_amt >= 0 else ''}{d_pct}）。"
        )
    # 时间口径提示：放款日期（fk_dt）与申请日期（dt）之间存在时差，周粒度下建议交叉验证
    funding_amount_evidence.append(
        "注：资金表按放款日期（fk_dt）统计，承接率按申请日期（dt）统计，两者存在 1-7 天时差；"
        "周粒度下若结论存疑，建议结合上下周数据交叉验证。"
    )

    # R7 需同时满足三条：① 放款金额下降；② 下降量级达到门槛（绝对 ≥ 10万 或 相对 ≥ 5%）；③ 项目数未增加
    amount_decline = baseline_total - current_total
    amount_decline_ratio = (
        round_float(amount_decline / baseline_total, 4) if baseline_total > 0 else 0.0
    )
    amount_is_meaningful = (
        amount_decline >= FUNDING_CONTRACTION_ABSOLUTE_THRESHOLD
        or (baseline_total > 0 and amount_decline_ratio >= FUNDING_CONTRACTION_RELATIVE_THRESHOLD)
    )
    count_not_increased = current_project_count <= baseline_project_count
    terminal_reason = (
        "R7"
        if current_total < baseline_total and amount_is_meaningful and count_not_increased
        else "R6"
    )

    if terminal_reason == "R7":
        contraction_detail = (
            f"绝对减少 {_fmt_amount(amount_decline)}"
            + (f"（降幅 {round_float(amount_decline_ratio * 100, 1)}%）" if baseline_total > 0 else "")
        )
        business = business_view(
            headline="已闭环到敏感资方收缩",
            summary=(
                f"敏感资方项目放款金额实质性下降（{contraction_detail}），"
                f"且项目数未增加（对比期 {baseline_project_count} → 当前期 {current_project_count}），"
                "可以将承接率下降进一步闭环到敏感资方侧收缩。"
            ),
            evidence=funding_amount_evidence,
        )
    else:
        if current_total >= baseline_total:
            not_r7_reason = "放款金额未下降"
        elif not amount_is_meaningful:
            not_r7_reason = (
                f"放款金额虽有下降（{_fmt_amount(abs(funding_amount_delta))}，"
                f"降幅 {funding_amount_delta_pct_text}），但未达到实质性收缩门槛"
                f"（绝对 ≥ {_fmt_amount(FUNDING_CONTRACTION_ABSOLUTE_THRESHOLD)} 或相对 ≥ {int(FUNDING_CONTRACTION_RELATIVE_THRESHOLD * 100)}%）"
            )
        else:
            not_r7_reason = "项目数有所增加"
        business = business_view(
            headline="最小因子范围成立，但未完成敏感资方侧闭环",
            summary=(
                f"异常范围已经成立，但敏感资方侧未呈现实质性收缩（{not_r7_reason}），"
                "暂时不能把原因直接落到敏感资方变化。"
                f"放款金额变化 {_fmt_amount(funding_amount_delta)}（{'+' if funding_amount_delta >= 0 else ''}{funding_amount_delta_pct_text}），"
                "需结合项目数变化综合判断。"
            ),
            evidence=funding_amount_evidence,
        )
    trace = {
        "slice_key": slice_key,
        "if_irr": asset_if_irr,
        "range_id": normalize_text(range_item.get("range_id")),
        "range_key": normalize_text(range_item.get("range_key")),
        "range_display": normalize_text(range_item.get("range_display")),
        "matched_projects": matched_projects,
        "funding_amount_delta": round_float(funding_amount_delta, 2),
        "funding_amount_delta_ratio": funding_amount_delta_ratio,
        "funding_amount_baseline_total": round_float(baseline_total, 2),
        "funding_amount_current_total": round_float(current_total, 2),
        "project_count_delta": project_count_delta,
        "baseline_project_count": baseline_project_count,
        "current_project_count": current_project_count,
        "terminal_reason": terminal_reason,
        "terminal_reason_text": build_reason(terminal_reason),
        "business_view": business,
        "root_cause": None,
        "errors": [],
    }
    if ENABLE_ANALYSIS_DEBUG_OUTPUT:
        trace["funding_debug"] = funding_debug
        dq = _period_debug_snapshot(
            current_result=current_result,
            baseline_result=baseline_result,
            current_filter=current_filter,
            baseline_filter=baseline_filter,
        )
        if dq is not None:
            trace["debug_query"] = dq
    trace = _finalize_funding_with_attribution(
        trace, asset_trace=asset_trace, slice_index=slice_index, slice_total=slice_total
    )
    log_stage_event(
        "funding",
        "阶段完成",
        slice_key=slice_key,
        range_id=normalize_text(range_item.get("range_id")),
        range_key=normalize_text(range_item.get("range_key")),
        trace=trace,
    )
    return trace


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="承接率下降归因阶段式脚本。")
    subparsers = parser.add_subparsers(dest="command", required=True)

    primary_parser = subparsers.add_parser("primary", help="一级诊断：判断大盘、定位异常切片。")
    primary_parser.add_argument("--granularity", required=True)
    primary_parser.add_argument("--current-start", required=True)
    primary_parser.add_argument("--current-end", required=True)
    primary_parser.add_argument("--baseline-start", required=True)
    primary_parser.add_argument("--baseline-end", required=True)
    primary_parser.add_argument("--access-token", default="")
    primary_parser.add_argument("--endpoint", default="")

    capital_parser = subparsers.add_parser("capital", help="资方分布诊断。")
    capital_parser.add_argument("--granularity", required=True)
    capital_parser.add_argument("--current-start", required=True)
    capital_parser.add_argument("--current-end", required=True)
    capital_parser.add_argument("--baseline-start", required=True)
    capital_parser.add_argument("--baseline-end", required=True)
    capital_parser.add_argument("--slice-key", required=True)
    capital_parser.add_argument("--slice-index", type=int, default=0,
                                help="状态行展示用：本切片在 primary_trace.analysis_sequence 中的 1-based 序号；0 表示未提供。")
    capital_parser.add_argument("--slice-total", type=int, default=0,
                                help="状态行展示用：异常切片总数；0 表示未提供。")
    capital_parser.add_argument("--access-token", default="")
    capital_parser.add_argument("--endpoint", default="")

    asset_parser = subparsers.add_parser("asset", help="资产维度诊断。")
    asset_parser.add_argument("--granularity", required=True)
    asset_parser.add_argument("--current-start", required=True)
    asset_parser.add_argument("--current-end", required=True)
    asset_parser.add_argument("--baseline-start", required=True)
    asset_parser.add_argument("--baseline-end", required=True)
    asset_parser.add_argument("--slice-key", required=True)
    asset_parser.add_argument("--slice-index", type=int, default=0,
                              help="状态行展示用：本切片在 primary_trace.analysis_sequence 中的 1-based 序号；0 表示未提供。")
    asset_parser.add_argument("--slice-total", type=int, default=0,
                              help="状态行展示用：异常切片总数；0 表示未提供。")
    asset_parser.add_argument("--access-token", default="")
    asset_parser.add_argument("--endpoint", default="")

    funding_parser = subparsers.add_parser("funding", help="敏感资方闭环（基于资金项目映射）。")
    funding_parser.add_argument("--granularity", required=True)
    funding_parser.add_argument("--current-start", required=True)
    funding_parser.add_argument("--current-end", required=True)
    funding_parser.add_argument("--baseline-start", required=True)
    funding_parser.add_argument("--baseline-end", required=True)
    funding_parser.add_argument("--slice-key", required=True)
    funding_parser.add_argument("--range-id", default="")
    funding_parser.add_argument("--range-key", default="")
    funding_parser.add_argument("--slice-index", type=int, default=0,
                                help="状态行展示用：本切片在 primary_trace.analysis_sequence 中的 1-based 序号；0 表示未提供。")
    funding_parser.add_argument("--slice-total", type=int, default=0,
                                help="状态行展示用：异常切片总数；0 表示未提供。")
    funding_parser.add_argument("--access-token", default="")
    funding_parser.add_argument("--endpoint", default="")
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_stdio()
    configure_debug_logging()
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "command", "") == "funding" and not (normalize_text(getattr(args, "range_key", "")) or normalize_text(getattr(args, "range_id", ""))):
        parser.error("funding 阶段至少需要传入 --range-key 或 --range-id。")
    access_token = resolve_access_token(getattr(args, "access_token", "") or None)
    endpoint = getattr(args, "endpoint", "") or None
    log_meta: dict[str, Any] = {
        "command": getattr(args, "command", ""),
        "argv": argv or sys.argv[1:],
    }
    if ENABLE_ANALYSIS_DEBUG_OUTPUT:
        log_meta["debug_log_file"] = str(DEBUG_LOG_FILE)
    logger.info(
        "命令开始执行 {}",
        json.dumps(log_meta, ensure_ascii=False, default=str),
    )

    if args.command == "primary":
        result = run_primary_stage(
            granularity=args.granularity,
            current_start=args.current_start,
            current_end=args.current_end,
            baseline_start=args.baseline_start,
            baseline_end=args.baseline_end,
            access_token=access_token,
            endpoint=endpoint,
        )
    elif args.command == "capital":
        result = run_capital_stage(
            granularity=args.granularity,
            current_start=args.current_start,
            current_end=args.current_end,
            baseline_start=args.baseline_start,
            baseline_end=args.baseline_end,
            slice_key=args.slice_key,
            slice_index=getattr(args, "slice_index", 0) or None,
            slice_total=getattr(args, "slice_total", 0) or None,
            access_token=access_token,
            endpoint=endpoint,
        )
    elif args.command == "asset":
        result = run_asset_stage(
            granularity=args.granularity,
            current_start=args.current_start,
            current_end=args.current_end,
            baseline_start=args.baseline_start,
            baseline_end=args.baseline_end,
            slice_key=args.slice_key,
            slice_index=getattr(args, "slice_index", 0) or None,
            slice_total=getattr(args, "slice_total", 0) or None,
            access_token=access_token,
            endpoint=endpoint,
        )
    else:
        result = run_funding_stage(
            granularity=args.granularity,
            current_start=args.current_start,
            current_end=args.current_end,
            baseline_start=args.baseline_start,
            baseline_end=args.baseline_end,
            slice_key=args.slice_key,
            range_id=args.range_id or None,
            range_key=args.range_key or None,
            slice_index=getattr(args, "slice_index", 0) or None,
            slice_total=getattr(args, "slice_total", 0) or None,
            access_token=access_token,
            endpoint=endpoint,
        )

    print(json_dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
