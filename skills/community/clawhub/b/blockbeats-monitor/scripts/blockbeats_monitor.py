# 本文件是 CLI 入口，只负责解析命令并编排采集、入库、统计、日报和推送流程。

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

from blockbeats_client import BlockBeatsClient
from config import get_blockbeats_api_key, get_db_path, get_lang, get_telegram_config, get_timezone, load_config, set_config
from db import fetch_matched_items, init_db, save_daily_metric, save_report_run, store_items
from metrics import build_windows, select_important_items, summarize_metrics
from report import render_report
from telegram import send_message


def _now():
    return datetime.now(tz=get_timezone())


def _iso(dt):
    return dt.isoformat()


def command_init_db(args):
    db_path = get_db_path(args.db)
    conn = init_db(db_path)
    conn.close()
    print("数据库已初始化：%s" % db_path)


def ingest_items(db_path, now):
    """采集律动内容并写入 SQLite。"""
    conn = init_db(db_path)
    client = BlockBeatsClient(
        api_key=get_blockbeats_api_key(),
        lang=get_lang(),
    )
    items = client.fetch_all(now)
    result = store_items(conn, items, _iso(now))
    conn.close()
    return result


def command_ingest(args):
    result = ingest_items(get_db_path(args.db), _now())
    print(json.dumps(result, ensure_ascii=False, indent=2))


def build_report(db_path, now):
    """查询当前窗口和上一窗口，生成日报并保存统计表。"""
    conn = init_db(db_path)
    window_start, window_end, previous_start, previous_end = build_windows(now)
    current_rows = fetch_matched_items(conn, _iso(window_start), _iso(window_end))
    previous_rows = fetch_matched_items(conn, _iso(previous_start), _iso(previous_end))
    summaries = summarize_metrics(current_rows, previous_rows)
    important_items = select_important_items(current_rows)
    markdown = render_report(window_start, window_end, summaries, important_items)
    report_date = (window_end - timedelta(days=1)).date().isoformat()
    for summary in summaries:
        save_daily_metric(
            conn,
            report_date,
            _iso(window_start),
            _iso(window_end),
            summary["group_id"],
            summary["mention_count"],
            summary["previous_mention_count"],
        )
    conn.commit()
    conn.close()
    return markdown, window_start, window_end


def command_report(args):
    markdown, _, _ = build_report(get_db_path(args.db), _now())
    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
        print("日报已写入：%s" % args.output)
    else:
        print(markdown, end="")


def command_send_telegram(args):
    text = Path(args.text_file).read_text(encoding="utf-8")
    bot_token, chat_id = get_telegram_config()
    result = send_message(
        bot_token,
        chat_id,
        text,
    )
    print(json.dumps({"telegram_status": "sent", "message_id": result.get("result", {}).get("message_id")}, ensure_ascii=False))


def command_run_daily(args):
    db_path = get_db_path(args.db)
    now = _now()
    ingest_result = ingest_items(db_path, now)
    markdown, window_start, window_end = build_report(db_path, now)
    bot_token, chat_id = get_telegram_config()
    result = send_message(
        bot_token,
        chat_id,
        markdown,
    )
    conn = init_db(db_path)
    report_date = (window_end - timedelta(days=1)).date().isoformat()
    save_report_run(
        conn,
        report_date,
        _iso(window_start),
        _iso(window_end),
        markdown,
        telegram_status="sent:%s" % result.get("result", {}).get("message_id"),
    )
    conn.close()
    print(json.dumps({"ingest": ingest_result, "telegram_status": "sent"}, ensure_ascii=False, indent=2))


def build_parser():
    parser = argparse.ArgumentParser(description="BlockBeats 舆情监控 CLI")
    parser.add_argument("--db", help="SQLite 数据库路径；默认读取 config.toml 的 storage.db_path 或 ./data/blockbeats_monitor.sqlite")
    parser.add_argument("--config", help="TOML 配置文件路径，默认读取 ./config.toml")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-db", help="初始化 SQLite 数据库")
    init_parser.set_defaults(func=command_init_db)

    ingest_parser = subparsers.add_parser("ingest", help="采集律动内容并入库")
    ingest_parser.set_defaults(func=command_ingest)

    report_parser = subparsers.add_parser("report", help="生成过去 24h 舆情日报")
    report_parser.add_argument("--output", help="把日报写入指定文件")
    report_parser.set_defaults(func=command_report)

    tg_parser = subparsers.add_parser("send-telegram", help="推送指定日报文件到 Telegram")
    tg_parser.add_argument("--text-file", required=True, help="要推送的 Markdown 文本文件")
    tg_parser.set_defaults(func=command_send_telegram)

    daily_parser = subparsers.add_parser("run-daily", help="采集、生成日报并推送 Telegram")
    daily_parser.set_defaults(func=command_run_daily)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    # 启动时加载 TOML；业务配置只从 TOML 读取，--db 仅用于临时覆盖数据库路径。
    set_config(load_config(args.config))
    args.func(args)


if __name__ == "__main__":
    main()
