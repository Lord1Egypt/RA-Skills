"""
OpenClaw 评测客户端：从服务端 API 拉取题目，按 CLI 或 WebSocket 方式执行并收集结果。

用法：
  python main.py --limit 5

参数：
  --limit N                最多执行的题目数量，超过后不再执行
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any
from pathlib import Path

from openclawbot import get_openclaw_bot
from agent_cli import run_task_cli, get_latest_session, cleanup_agent_sessions_with_prefix
from utils import get_bench_session_id, get_temp_file, clean_temp_files, clean_benchclaw_workspace, HardwareMonitor, get_system_info
from report import generate_reports_from_dict
from server import fetch_questions, upload_results_from_dict, flush_pending_uploads
from config import (
    DEFAULT_SUBMIT_API_URL,
    DEFAULT_AGENT_ID,
    DEFAULT_TIMEOUT_SEC,
    DEFAULT_SESSION_PREFIX,
    CLIENT_VERSION,
    USE_LATEST_SESSION,
)
from session import get_openclaw_session_info, OpenClawSessionInfo, ran_under_openclaw_exec, cleanup_agent_sessions

def setup_logging() -> logging.Logger:
    """配置日志记录，默认输出到文件和控制台。"""
    logger = logging.getLogger("benchclaw")
    logger.setLevel(logging.DEBUG)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    # 文件 handler - 默认输出到 ../data/benchclaw.log
    log_file = get_temp_file("benchclaw.log")

    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # 2. 控制台 handler - 实时输出到 stdout
    class FlushStreamHandler(logging.StreamHandler):
        """自定义 handler，每条日志后立即刷新"""
        def emit(self, record):
            super().emit(record)
            self.flush()  # 立即刷新到 stdout

    # 控制台 handler
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    #console_handler = logging.StreamHandler(sys.stdout)
    console_handler = FlushStreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    logger.addHandler(console_handler)

    return logger

# 全局 logger 实例
logger = setup_logging()

def _aggregate_results(results: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """
    统计各分类得分、题数、通过数及得分率。
    返回 stats 字典，包含 category_stats 及汇总数据。
    """
    stats: dict[str, dict[str, Any]] = {}
    category_stats: dict[str, dict[str, Any]] = {}

    for r in results:
        cat = r.get("category") or "unknown"
        score = r.get("score", 0)
        accuracy_score = r.get("accuracy_score", 0)
        real_accuracy_score = r.get("real_accuracy_score", 0)
        max_accuracy_score = r.get("max_accuracy_score", 0)
        success = r.get("success", False)
        tps_score = r.get("tps_score", 0)
        category_label = r.get("category_label") or cat

        if cat not in category_stats:
            category_stats[cat] = {
                "count": 0,
                "succeeded": 0,
                "score": 0,
                "accuracy_score": 0,
                "real_accuracy_score": 0,
                "max_accuracy_score": 0,
                "tps_score": 0,
                "category_label": category_label,
            }

        category_stats[cat]["count"] += 1
        category_stats[cat]["score"] += score
        category_stats[cat]["tps_score"] += tps_score
        category_stats[cat]["accuracy_score"] += accuracy_score
        category_stats[cat]["real_accuracy_score"] += real_accuracy_score
        category_stats[cat]["max_accuracy_score"] += max_accuracy_score
        if success:
            category_stats[cat]["succeeded"] += 1

    for cat, cat_stats in category_stats.items():
        if cat_stats["max_accuracy_score"] > 0:
            cat_stats["accuracy_rate"] = round(cat_stats["accuracy_score"] / cat_stats["max_accuracy_score"] * 100, 2)
        else:
            cat_stats["accuracy_rate"] = 0.0

    stats["category_stats"] = category_stats
    stats["score"] = sum(r.get("score", 0) for r in results)
    stats["accuracy_score"] = sum(r.get("accuracy_score", 0) for r in results)
    stats["real_accuracy_score"] = sum(r.get("real_accuracy_score", 0) for r in results)
    stats["max_accuracy_score"] = sum(r.get("max_accuracy_score", 0) for r in results)
    stats["accuracy_rate"] = round(stats["accuracy_score"] / stats["max_accuracy_score"] * 100, 2) if stats["max_accuracy_score"] > 0 else 0.0
    stats["n_question_count"] = len(results)
    stats["n_success"] = sum(1 for r in results if r.get('success'))
    stats["tps_score"] = sum(r.get("tps_score", 0) for r in results)
    stats["avg_tps"] = round(
        sum(r.get("tps", 0) for r in results if r.get("tps", 0) > 0)
        / max(1, sum(1 for r in results if r.get("tps", 0) > 0)),
        2,
    )

    return stats

def print_brief_stats(stats: dict[str, dict[str, Any]]):
    lines = [
        "评测结果:",
        f"总分: {stats['score']}",
        f"准确度分: {stats['real_accuracy_score']}",
        f"速度分: {stats.get('tps_score', 0)}",
        f"准确率: {stats['accuracy_rate']}%",
        f"题目总数: {stats['n_question_count']}",
        f"成功数: {stats['n_success']}",
        f"平均 TPS: {stats.get('avg_tps', 0)} tokens/s",
        "",
        "题型分数：",
    ]

    category_stats = stats["category_stats"]
    for cat, cat_stats in sorted(category_stats.items()):
        label = cat_stats.get("category_label") or cat
        lines.append(
            f"分类:{label}({cat})"
            f" 题目数量:{cat_stats['count']}"
            f" 得分:{cat_stats['score']}"
            f" 准确度分:{cat_stats.get('real_accuracy_score', 0)}"
            f" 速度分:{cat_stats.get('tps_score', 0)}"
            f" 准确率:{cat_stats['accuracy_rate']}%"
        )
    print("\n" + "\n".join(lines) + "\n")

def _upload_results(
        summary: dict[str, Any],
        bench_session_id: str,
        hash: str
    ) -> dict[str, Any]:
    """将评测结果上传到服务端，返回排行榜数据（上传失败时返回空 dict）。"""
    if not summary.get("results"):
        logger.warning("没有结果数据，跳过上传")
        return {}
    try:
        ok, msg, leaderboard = upload_results_from_dict(summary, bench_session_id, hash, DEFAULT_SUBMIT_API_URL)
        if ok:
            logger.info(f"上传成功: {msg}")
            category_stats = summary.get("stats", {}).get("category_stats")
            _log_leaderboard(leaderboard, category_stats)
        else:
            logger.warning(f"上传失败: {msg}")
        return leaderboard if ok else {}
    except Exception as e:
        logger.warning(f"上传异常: {e}")
        return {}


def _log_leaderboard(leaderboard: dict[str, Any], category_stats: dict[str, Any] | None = None) -> None:
    """将排行榜数据输出到日志。"""
    if not leaderboard:
        return
    percentiles = leaderboard.get("percentiles") or {}
    total_pct = percentiles.get("total")
    sample_size = leaderboard.get("sample_size")
    leaderboard_url = leaderboard.get("leaderboard_url", "")

    if total_pct is not None:
        logger.info(f"🏆 太棒了，您的分数超越了全国 {total_pct}% 的用户！")

    # 用服务端返回的 category 顺序（s1~s5）对应真实分类名称
    # CATEGORY_ORDER 与 server.py 中定义一致
    from server import CATEGORY_ORDER
    cat_lines = []
    for idx, cat_key in enumerate(CATEGORY_ORDER, start=1):
        pct = percentiles.get(f"s{idx}")
        if pct is None:
            continue
        # 优先从 category_stats 取 category_label，否则 fallback 到 cat_key
        label = cat_key
        if category_stats and cat_key in category_stats:
            label = category_stats[cat_key].get("category_label") or cat_key
        cat_lines.append(f"  {label}({cat_key}): 超越 {pct}%")
    if cat_lines:
        logger.info("分类排名：\n" + "\n".join(cat_lines))

    if sample_size:
        logger.info(f"参与评测用户数：{sample_size}")
    if leaderboard_url:
        logger.info(f"完整排行榜：{leaderboard_url}")


def _generate_reports(summary: dict[str, Any]) -> None:
    """生成简要报表和详细报表，结果写入 ../data/ 目录。"""
    if not summary.get("results"):
        logger.warning("没有结果数据，跳过报表生成")
        return
    try:
        summary_path, detail_path = generate_reports_from_dict(summary)
        logger.info(f"简要报表：{summary_path}")
        logger.info(f"详细报表：{detail_path}")
    except Exception as e:
        logger.warning(f"报表生成失败: {e}")


def _load_caller_info() -> dict:
    """读取 caller_info.txt，获取触发评测的渠道和目标用户信息。"""
    caller_file = get_temp_file("caller_info.txt")
    if not os.path.exists(caller_file):
        return {}
    caller = {}
    try:
        with open(caller_file) as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    caller[k.strip()] = v.strip()
    except Exception as e:
        logger.warning(f"读取 caller_info.txt 失败: {e}")
    return caller


def _upload_to_server_enabled(caller: dict) -> bool:
    """
    是否上传榜单结果并补报历史缓存。

    caller_info.txt 中 upload_to_server=false（或 否/no/0）时仅本地评测：
    不调用提交接口、不执行 flush_pending_uploads。缺省为 true。
    """
    raw = (caller.get("upload_to_server") or "true").strip().lower()
    return raw not in ("false", "否", "no", "0")


def _safe_print(text: str) -> None:
    """Windows GBK 兼容的 print，自动替换无法编码的字符（如 emoji）。"""
    try:
        print(text, flush=True)
    except (UnicodeEncodeError, LookupError):
        # Windows GBK 等窄字符集编码，替换无法编码的字符为 '?'
        safe = text.encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8', errors='replace')
        print(safe, flush=True)


def _send_notification(message: str, caller: dict) -> None:
    """向触发评测的用户发送通知。
    - 有 channel + target（飞书/telegram 等）：通过 openclaw message send 发消息
    - 无 channel + target（TUI 或未配置）：fallback 到 stdout，TUI 用户直接可见
    """
    channel = caller.get("channel")
    target = caller.get("target")
    # webchat 是 OpenClaw 内部渠道（TUI/WebChat），不支持 CLI 发送，直接走 stdout fallback
    UNSUPPORTED_CHANNELS = {"webchat", ""}
    if not channel or not target or channel in UNSUPPORTED_CHANNELS:
        # TUI / 无渠道 fallback：输出到 stdout
        _safe_print(f"\n{'='*50}\n[NOTIFY] {message}\n{'='*50}")
        return
    try:
        from agent_cli import resolve_openclaw_cmd
        base = resolve_openclaw_cmd()
        cmd = base + ["message", "send", "--channel", channel, "--target", target, "--message", message]
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                result = subprocess.run(cmd, timeout=30, capture_output=True, text=True)
                if result.returncode == 0:
                    logger.info(f"已发送通知到 {channel}:{target}")
                    return
                else:
                    stderr = result.stderr.strip() if result.stderr else "(无错误输出)"
                    logger.warning(f"通知发送失败（第{attempt}次）returncode={result.returncode} stderr={stderr}")
            except subprocess.TimeoutExpired:
                logger.warning(f"通知发送超时（第{attempt}次，30s）")
            except Exception as e:
                logger.warning(f"通知发送异常（第{attempt}次）: {e}")
            if attempt < max_retries:
                import time as _t; _t.sleep(2)
        logger.error(f"通知发送失败，已重试{max_retries}次，fallback 到 stdout: {channel}:{target}")
        _safe_print(f"\n{'='*50}\n[NOTIFY] {message}\n{'='*50}")
    except Exception as e:
        logger.error(f"通知模块异常，fallback 到 stdout: {e}")
        _safe_print(f"\n{'='*50}\n[NOTIFY] {message}\n{'='*50}")


def main() -> int:
    # 运行前删除 bench_claw 工作区文件夹
    clean_benchclaw_workspace()
    clean_temp_files()
    cleanup_agent_sessions_with_prefix(DEFAULT_AGENT_ID, f'{DEFAULT_SESSION_PREFIX}*')
    cleanup_agent_sessions(DEFAULT_AGENT_ID, DEFAULT_SESSION_PREFIX)
    
    session_info: OpenClawSessionInfo = get_openclaw_session_info()
    logger.info(f"openclaw SessionId: {session_info.session_id}")
    logger.info(f"openclaw SessionKey: {session_info.session_key}")
    logger.info(f"openclaw Channel: {session_info.channel}")
    logger.info(f"openclaw Target: {session_info.target}")

    bot = get_openclaw_bot()
    logger.info(f"Openclaw版本: {bot.version}")
    logger.info(f"Openclaw主模型: {bot.primary_model}")
    logger.info(f"openclaw root: {bot.openclaw_root}")

    bench_session_id = get_bench_session_id()
    logger.info(f"Bench 会话 ID: {bench_session_id}")

    caller = _load_caller_info()
    upload_to_server = _upload_to_server_enabled(caller)

    # 补报上次因网络失败缓存的数据（仅在上传开启时）
    if upload_to_server:
        try:
            flushed = flush_pending_uploads()
            if flushed:
                logger.info(f"补报成功 {len(flushed)} 条历史缓存数据")
        except Exception as e:
            logger.warning(f"补报缓存数据失败: {e}")
    else:
        logger.info("upload_to_server=false：跳过历史缓存补报")

    # 下载题目
    try:
        fetch_result = fetch_questions(bench_session_id, bot.primary_model, openclaw_root=str(bot.openclaw_root))
        questions = fetch_result["questions"]
        api_session_id = fetch_result["session_id"]
        api_hash = fetch_result["hash"]
        model_cost = fetch_result.get("model_cost")
        logger.info(f"下载题目成功: 共 {len(questions)} 道题目")
        if model_cost:
            logger.info(f"模型计费信息: {model_cost}")
    except Exception as e:
        notify_msg = ""
        if isinstance(e, urllib.error.HTTPError) and e.code == 429:
            notify_msg = "⚠️ 今日评测次数已达上限(10次/24小时)，请明天再试。"
            logger.error(notify_msg)
        else:
            notify_msg = f"运行benchclaw评测失败：加载题目失败，错误信息：{e}"
            logger.error(notify_msg)

        if USE_LATEST_SESSION:
            caller["channel"] = session_info.channel
            caller["target"] = session_info.target
        _send_notification(notify_msg, caller)
        return 1

    # DEBUG
    # questions = questions[0:1]

    # 执行并收集结果（caller 已在启动时加载）
    # 如果使用最新会话作为消息推送渠道，则更新 caller 中的渠道和目标
    if USE_LATEST_SESSION:
        caller["channel"] = session_info.channel
        caller["target"] = session_info.target

    hw_monitor = HardwareMonitor()
    hw_monitor.start()
    questions_results = []
    category_buffer: dict[str, list] = {}  # 按分类缓冲，用于阶段小结

    for i, task in enumerate(questions):
        cat = task.get("category", "unknown")
        cat_label = task.get("category_label", cat)
        logger.info(f"正在测试 {task.get('id')} 类别:{cat_label} ...")

        # _send_notification(f"正在进行{cat_label}{task.get('id')}, 当前进度{i+1}/{len(questions)}，请耐心等待...", caller)
        result = run_task_cli(task, timeout_sec=DEFAULT_TIMEOUT_SEC)
        questions_results.append(result)

        status = "ok" if result.get("success") else "failed"
        logger.info(f" -> {status} (returncode={result.get('returncode')}, error={result.get('error')}, {result.get('duration_sec', 0)}s)")

        # A3: 超时提示
        if result.get("error") == "timeout":
            _send_notification(f"⚠️ {task.get('id')} 超时（>{DEFAULT_TIMEOUT_SEC}s），已自动跳过，继续下一题", caller)

        # 按分类缓冲
        if cat not in category_buffer:
            category_buffer[cat] = []
        category_buffer[cat].append(result)

        # A2: 分类完成时发阶段小结（每5题一组）
        if len(category_buffer[cat]) == 5:
            pass_count = sum(1 for r in category_buffer[cat] if r.get("success"))
            cat_score = sum(r.get("score", 0) for r in category_buffer[cat])
            # 计算已完成分类数和进度百分比
            completed_cats = len(category_buffer)
            total_cats = 5
            progress_pct = round(completed_cats / total_cats * 100)
            # 分类序号
            from server import CATEGORY_ORDER as _CAT_ORDER
            cat_idx = _CAT_ORDER.index(cat) + 1 if cat in _CAT_ORDER else completed_cats
            msg = (
                f"📊 {cat_idx}. {cat_label}完成：{pass_count}/5 通过，阶段得分 {cat_score:,}\n"
                f"已完成 {progress_pct}%（{completed_cats}/{total_cats} 个分类）"
            )
            logger.info(msg.replace('\n', ' '))
            _send_notification(msg, caller)

    logger.info(f"执行完成")
    hw_stats = hw_monitor.stop()
    sys_info = get_system_info()

    # 聚合统计
    stats = _aggregate_results(questions_results)

    # 向 stdout 输出简要评测信息
    print_brief_stats(stats)

    summary = {
        "api_session_id": api_session_id,
        "api_hash": api_hash,
        "model_name": bot.primary_model or "",
        "model_cost": model_cost,
        "hardware_stats": hw_stats,
        "sys_info": sys_info,
        "agent_name": caller.get("agent_name", ""),
        "openclaw_version": bot.version,
        "results": questions_results,
        "total": len(questions_results),
        "succeeded": sum(1 for r in questions_results if r.get("success")),
        "score": stats.get("score", 0),
        "stats": stats,
    }
    payload = json.dumps(summary, indent=2, ensure_ascii=False)

    results_file_path = get_temp_file('results.json')
    with open(results_file_path, "w", encoding="utf-8") as f:
        f.write(payload)

    # 生成报表
    _generate_reports(summary)

    # 根据 show_name 决定是否携带 openclaw_name 上报
    show_name = caller.get("show_name", "true").lower() not in ("false", "否", "no", "0")
    if not show_name:
        summary["agent_name"] = ""  # 匿名上报

    # 上报结果到服务端（upload_to_server=false 时跳过）
    if upload_to_server:
        leaderboard = _upload_results(summary, bench_session_id, api_hash)
    else:
        logger.info("upload_to_server=false：跳过结果上传（仅本地评测）")
        leaderboard = {}

    # 将排行榜写入报表（上传成功后追加）
    if leaderboard:
        summary["leaderboard"] = leaderboard
        _generate_reports(summary)

    # A4: 评测完成后通知用户
    score = stats.get("score", 0)
    succeeded = summary["succeeded"]
    total = summary["total"]
    total_duration_sec = sum(r.get("duration_sec", 0) for r in questions_results)
    duration_min = round(total_duration_sec / 60, 1)
    failed_ids = [r.get("id", r.get("question_id", "?")) for r in questions_results if not r.get("success")]
    fail_str = f"\n❌ 失败题目：{', '.join(failed_ids)}" if failed_ids else ""

    # 榜单排名信息
    rank_str = ""
    if upload_to_server and leaderboard:
        pct = leaderboard.get("percentiles", {}).get("total")
        if pct is not None:
            rank_str = f"\n🏅 榜单排名：超越了 {pct}% 的用户"

    if upload_to_server:
        completion_msg = (
            f"🏆 BenchClaw 评测完成！已上传到榜单。\n\n"
            f"📊 综合评分：{score:,} 分\n"
            f"✅ 通过：{succeeded}/{total} 题\n"
            f"⏱️ 耗时：{duration_min} 分钟{rank_str}{fail_str}\n\n"
            f"发送「报告」查看详细结果。"
        )
    else:
        completion_msg = (
            f"🏆 BenchClaw 评测完成（仅本地，未上传榜单）。\n\n"
            f"📊 综合评分：{score:,} 分\n"
            f"✅ 通过：{succeeded}/{total} 题\n"
            f"⏱️ 耗时：{duration_min} 分钟{fail_str}\n\n"
            f"发送「报告」查看 data/ 下报表；本次未向榜单服务器提交结果。"
        )
    _send_notification(completion_msg, caller)

    return 0 if summary["succeeded"] == summary["total"] else 1



if __name__ == "__main__":
    main()
