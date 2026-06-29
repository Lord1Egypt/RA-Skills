#!/usr/bin/env python3
"""Query ChatArt account credit balance and usage history.

Usage:
    python user.py credit [--json]
    python user.py logs [--type TYPE] [--start TIME] [--end TIME] [--page N] [--size N] [--json]
"""

import argparse
import json as json_mod
import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(__file__))

from typing import Any, Optional
from shared.client import ChatArtClient, TaskStatus

CREDIT_PATH = "/web/member/user-diamond"

TASK_TYPES = [
    "image",
    "video",
]

HISTORY_ENDPOINTS = {
    "image": "/web/art/history",
    "video": "/web/video/history",
}

def cmd_credit(client: ChatArtClient, args):
    result = client.post(CREDIT_PATH)

    if args.json:
        print(json_mod.dumps(result, indent=2, ensure_ascii=False))
    else:
        credit = result.get("diamond", result)
        print(f"Credit balance: {credit}")


def cmd_logs(client: ChatArtClient, args):
    payload = {
        "page": str(args.page),
        "per_page": str(args.size),
        **({"start_time": args.start} if args.start else {}),
        **({"end_time": args.end} if args.end else {}),
    }
    logs_path = HISTORY_ENDPOINTS[args.type]
    result = client.get(logs_path, json=payload)

    if args.json:
        print(json_mod.dumps(result, indent=2, ensure_ascii=False))
        return

    page_no = args.page
    page_size = args.size
    
    # Extract data array from response
    if isinstance(result, dict):
        data_list = result.get("data", [])
        total = result.get("total", len(data_list))
        current_page = result.get("current_page", page_no)
    elif isinstance(result, list):
        data_list = result
        total = len(data_list)
        current_page = page_no
    else:
        data_list = []
        total = 0
        current_page = page_no

    if not args.quiet:
        print(
            f"Page {current_page} | {len(data_list)} items (Total: {total})",
            file=sys.stderr,
        )

    if not data_list:
        print("No records found.")
        return

    if args.type == "image":
        print_image_history(data_list)
    elif args.type == "video":
        print_video_history(data_list)



def print_image_history(result: Optional[dict] = None):
    header = f"{'Date':<16} {'TaskID':<8} {'St':<10} {'ImageURL'}"
    print(header)
    print("-" * len(header))

    for entry in result:
        if not isinstance(entry, dict):
            continue
            
        task_id = entry.get("id")
        ts = entry.get("create_at")
        is_drawing = entry.get("is_drawing", 0)
        
        # Get first image from pic_url array
        pic_urls = entry.get("pic_url", [])
        first_pic = pic_urls[0] if pic_urls and isinstance(pic_urls, list) and len(pic_urls) > 0 else {}
        pic_status = first_pic.get("status", 0) if isinstance(first_pic, dict) else 0
        image_url = first_pic.get("url", "") if isinstance(first_pic, dict) else ""
        
        # Determine status based on is_drawing and pic_status
        if is_drawing == 1 and pic_status == 1:
            status_label = "completed"
        elif is_drawing == 1 and pic_status == 0:
            status_label = "working"
        elif is_drawing == 2:
            status_label = "failed"
        elif is_drawing == 0:
            status_label = "pending"
        else:
            status_label = "unknown"
        
        error = entry.get("comment", "") or ""

        # 时间格式化
        date = datetime.datetime.fromtimestamp(ts).strftime("%y-%m-%d %H:%M") if ts else ""

        # 截断 error
        error_short = (error[:22] + "...") if error and len(error) > 25 else (error or "")

        # 显示图片或错误信息
        if image_url:
            display_text = image_url
        elif is_drawing == 2:
            display_text = error_short or "Failed"
        elif is_drawing == 1 and not image_url:
            display_text = "Processing..."
        else:
            display_text = "N/A"

        print(f"{date:<16} {task_id:<8} {status_label:<10} {display_text}")

def print_video_history(result: Optional[dict] = None):
    header = f"{'Date':<16} {'TaskID':<8} {'St':<10} {'VideoURL'}"
    print(header)
    print("-" * len(header))

    for entry in result:
        if not isinstance(entry, dict):
            continue
            
        task_id = entry.get("id")
        ts = entry.get("create_at")
        status_code = entry.get("status", 0)
        
        # Get first video from file array
        files = entry.get("file", [])
        first_file = files[0] if files and isinstance(files, list) and len(files) > 0 else {}
        file_status = first_file.get("status", 0) if isinstance(first_file, dict) else 0
        video_url = first_file.get("url", "") if isinstance(first_file, dict) else ""
        
        # Determine status label
        if status_code == 1 and file_status == 1:
            status_label = "completed"
        elif status_code == 1 and file_status == 0:
            status_label = "working"
        elif status_code == 2:
            status_label = "failed"
        elif status_code == 0:
            status_label = "pending"
        else:
            status_label = "unknown"
        
        error = entry.get("error_message", "") or entry.get("comment", "") or ""

        # 时间格式化
        date = datetime.datetime.fromtimestamp(ts).strftime("%y-%m-%d %H:%M") if ts else ""

        # 截断 error
        error_short = (error[:22] + "...") if error and len(error) > 25 else (error or "")

        # 显示视频或错误信息
        if video_url and status_code == 1:
            display_text = video_url
        elif status_code == 2:
            display_text = error_short or "Failed"
        elif status_code == 1 and not video_url:
            display_text = "Processing..."
        else:
            display_text = "N/A"

        print(f"{date:<16} {task_id:<8} {status_label:<10} {display_text}")


def main():
    parser = argparse.ArgumentParser(
        description="Chatart account credit management."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # credit command
    credit_p = sub.add_parser("credit", help="Query credit balance")
    credit_p.add_argument("--json", action="store_true",
                          help="Output full JSON response")

    logs_p = sub.add_parser("logs", help="Query credit usage history")
    logs_p.add_argument("--type", default=None, choices=TASK_TYPES,
                        help="Filter by task type")
    logs_p.add_argument("--start", default=None,
                        help="UTC start time (yyyy-MM-dd)")
    logs_p.add_argument("--end", default=None,
                        help="UTC end time (yyyy-MM-dd)")
    logs_p.add_argument("--page", type=int, default=1,
                        help="Page number (default: 1)")
    logs_p.add_argument("--size", type=int, default=20,
                        help="Items per page (default: 20)")
    logs_p.add_argument("--json", action="store_true",
                        help="Output full JSON response")
    logs_p.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress status messages on stderr")

    args = parser.parse_args()
    client = ChatArtClient()

    if args.command == "credit":
        cmd_credit(client, args)
    elif args.command == "logs":
        cmd_logs(client, args)


if __name__ == "__main__":
    main()
