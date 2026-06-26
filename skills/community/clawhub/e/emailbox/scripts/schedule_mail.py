#!/usr/bin/env python3
"""Emailbox - Schedule email sending with 12+ provider support.

Supports: schedule emails for future delivery, process queue, list/cancel scheduled.
Uses only Python standard library + subprocess (to call send_mail.py).

Usage:
  # Schedule an email for specific time
  python3 schedule_mail.py --schedule --at "2026-04-19 09:00" --to user@example.com --subject "Meeting" --body "Reminder"

  # Schedule an email in N minutes
  python3 schedule_mail.py --schedule --in 30 --to user@example.com --subject "Follow up" --body "Please review"

  # Process the queue (send any due emails)
  python3 schedule_mail.py --process-queue

  # List scheduled emails
  python3 schedule_mail.py --list-scheduled

  # Cancel a scheduled email
  python3 schedule_mail.py --cancel <schedule_id>
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

QUEUE_DIR = Path.home() / ".emailbox" / "queue"
SCRIPTS_DIR = Path(__file__).parent


def get_schedule_id():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + uuid.uuid4().hex[:8]


def write_schedule(schedule_id, scheduled_time, email_data):
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    schedule_file = QUEUE_DIR / f"{schedule_id}.json"
    schedule_info = {
        "id": schedule_id,
        "scheduled_time": scheduled_time,
        "status": "pending",
        "created_at": datetime.datetime.now().isoformat(),
        "email": email_data,
    }
    with open(schedule_file, "w", encoding="utf-8") as f:
        json.dump(schedule_info, f, ensure_ascii=False, indent=2)
    return str(schedule_file)


def parse_time(time_str):
    for fmt in ["%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S"]:
        try:
            return datetime.datetime.strptime(time_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse time: {time_str}. Use format: YYYY-MM-DD HH:MM")


def setup_system_scheduler(schedule_id, scheduled_time, schedule_file):
    """Print instructions for the user to manually set up scheduling.
    
    This function does NOT modify crontab or system scheduler automatically.
    Users must explicitly confirm and add any entries themselves.
    """
    send_script = SCRIPTS_DIR / "send_mail.py"
    schedule_script = SCRIPTS_DIR / "schedule_mail.py"
    python_path = sys.executable

    return False, (
        "Emailbox does NOT modify your system scheduler automatically.\n"
        "To process scheduled emails, choose ONE of these options:\n\n"
        "1. Manual processing:\n"
        f"   {python_path} {schedule_script} --process-queue\n\n"
        "2. Add to crontab manually (review before adding!):\n"
        f"   crontab -l > ~/crontab_backup.txt\n"
        f"   crontab -e\n"
        f"   # Add this line:\n"
        f"   * * * * * {python_path} {schedule_script} --process-queue\n\n"
        "3. Use --process-queue in your own automation pipeline."
    )


def cmd_schedule(args):
    if args.at:
        scheduled_time = parse_time(args.at)
    elif args.in_minutes:
        scheduled_time = datetime.datetime.now() + datetime.timedelta(minutes=args.in_minutes)
    else:
        print("error: specify --at 'YYYY-MM-DD HH:MM' or --in MINUTES")
        sys.exit(1)

    if scheduled_time < datetime.datetime.now():
        print(f"error: scheduled time is in the past: {scheduled_time}")
        sys.exit(1)

    body_text = args.body
    if args.body_file:
        with open(args.body_file, "r", encoding="utf-8") as f:
            body_text = f.read()

    body_html = args.html_body
    if args.html_file:
        with open(args.html_file, "r", encoding="utf-8") as f:
            body_html = f.read()

    email_data = {
        "to": args.to,
        "subject": args.subject,
    }
    if body_text:
        email_data["body"] = body_text
    if body_html:
        email_data["html_body"] = body_html
    if args.cc:
        email_data["cc"] = args.cc
    if args.bcc:
        email_data["bcc"] = args.bcc
    if args.attach:
        email_data["attach"] = args.attach
    if args.from_addr:
        email_data["from_addr"] = args.from_addr
    if args.provider:
        email_data["provider"] = args.provider
    if args.reply_to:
        email_data["reply_to"] = args.reply_to
    if args.forward_from:
        email_data["forward_from"] = args.forward_from
    if args.forward_date:
        email_data["forward_date"] = args.forward_date
    if args.forward_to:
        email_data["forward_to"] = args.forward_to
    if args.forward_cc:
        email_data["forward_cc"] = args.forward_cc
    if args.forward_subject:
        email_data["forward_subject"] = args.forward_subject
    if args.importance:
        email_data["importance"] = args.importance
    if args.receipt:
        email_data["receipt"] = True

    schedule_id = get_schedule_id()
    schedule_file = write_schedule(schedule_id, scheduled_time.isoformat(), email_data)

    print("Email scheduled / 邮件已加入定时发送队列")
    print(f"  Schedule ID: {schedule_id}")
    print(f"  Scheduled: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  To: {args.to}")
    print(f"  Subject: {args.subject}")
    print(f"  Config: {schedule_file}")

    ok, msg = setup_system_scheduler(schedule_id, scheduled_time, schedule_file)
    if ok:
        print(f"  System scheduler: {msg}")
    else:
        print(f"  Warning: {msg}")


def cmd_process_queue():
    if not QUEUE_DIR.exists():
        print("Schedule queue is empty / 定时队列为空")
        return

    now = datetime.datetime.now()
    processed = 0
    failed = 0

    for schedule_file in sorted(QUEUE_DIR.glob("*.json")):
        with open(schedule_file, "r", encoding="utf-8") as f:
            info = json.load(f)

        if info.get("status") != "pending":
            continue

        scheduled_time = datetime.datetime.fromisoformat(info["scheduled_time"])
        if scheduled_time > now:
            continue

        email_data = info["email"]

        send_args = [sys.executable, str(SCRIPTS_DIR / "send_mail.py")]
        send_args.extend(["--to", email_data["to"]])
        send_args.extend(["--subject", email_data["subject"]])

        if email_data.get("body"):
            body_file = str(schedule_file).replace(".json", ".body.txt")
            with open(body_file, "w", encoding="utf-8") as f:
                f.write(email_data["body"])
            send_args.extend(["--body-file", body_file])

        if email_data.get("html_body"):
            html_file = str(schedule_file).replace(".json", ".html")
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(email_data["html_body"])
            send_args.extend(["--html-file", html_file])

        for key, flag in [("cc", "--cc"), ("bcc", "--bcc"), ("from_addr", "--from-addr"),
                          ("provider", "--provider"), ("reply_to", "--reply-to"),
                          ("importance", "--importance")]:
            if email_data.get(key):
                send_args.extend([flag, str(email_data[key])])

        if email_data.get("forward_from"):
            send_args.extend(["--forward-from", email_data["forward_from"]])
        if email_data.get("forward_date"):
            send_args.extend(["--forward-date", email_data["forward_date"]])
        if email_data.get("forward_to"):
            send_args.extend(["--forward-to", email_data["forward_to"]])
        if email_data.get("forward_cc"):
            send_args.extend(["--forward-cc", email_data["forward_cc"]])
        if email_data.get("forward_subject"):
            send_args.extend(["--forward-subject", email_data["forward_subject"]])
        if email_data.get("receipt"):
            send_args.append("--receipt")

        if email_data.get("attach"):
            send_args.append("--attach")
            for att in email_data["attach"]:
                send_args.append(str(att))

        result = subprocess.run(send_args, capture_output=True, text=True)

        if result.returncode == 0:
            info["status"] = "sent"
            info["sent_at"] = datetime.datetime.now().isoformat()
            with open(schedule_file, "w", encoding="utf-8") as f:
                json.dump(info, f, ensure_ascii=False, indent=2)
            processed += 1
            print(f"  Sent: {info['id']} -> {email_data['to']}")
        else:
            info["status"] = "failed"
            info["error"] = result.stderr or result.stdout
            info["retry_count"] = info.get("retry_count", 0) + 1
            with open(schedule_file, "w", encoding="utf-8") as f:
                json.dump(info, f, ensure_ascii=False, indent=2)
            failed += 1
            print(f"  Failed: {info['id']} -> {email_data['to']}")

    print(f"\nQueue processed: {processed} sent, {failed} failed / 队列处理完成: {processed} 已发送, {failed} 失败")


def cmd_process_one(schedule_id):
    schedule_file = QUEUE_DIR / f"{schedule_id}.json"
    if not schedule_file.exists():
        print(f"Schedule not found: {schedule_id}")
        sys.exit(1)

    with open(schedule_file, "r", encoding="utf-8") as f:
        info = json.load(f)

    email_data = info["email"]
    send_args = [sys.executable, str(SCRIPTS_DIR / "send_mail.py")]
    send_args.extend(["--to", email_data["to"]])
    send_args.extend(["--subject", email_data["subject"]])

    if email_data.get("body"):
        body_file = str(schedule_file).replace(".json", ".body.txt")
        with open(body_file, "w", encoding="utf-8") as f:
            f.write(email_data["body"])
        send_args.extend(["--body-file", body_file])

    if email_data.get("html_body"):
        html_file = str(schedule_file).replace(".json", ".html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(email_data["html_body"])
        send_args.extend(["--html-file", html_file])

    for key, flag in [("cc", "--cc"), ("bcc", "--bcc"), ("from_addr", "--from-addr"),
                      ("provider", "--provider"), ("reply_to", "--reply-to"),
                      ("importance", "--importance")]:
        if email_data.get(key):
            send_args.extend([flag, str(email_data[key])])

    if email_data.get("forward_from"):
        send_args.extend(["--forward-from", email_data["forward_from"]])
    if email_data.get("forward_date"):
        send_args.extend(["--forward-date", email_data["forward_date"]])
    if email_data.get("forward_to"):
        send_args.extend(["--forward-to", email_data["forward_to"]])
    if email_data.get("forward_cc"):
        send_args.extend(["--forward-cc", email_data["forward_cc"]])
    if email_data.get("forward_subject"):
        send_args.extend(["--forward-subject", email_data["forward_subject"]])
    if email_data.get("receipt"):
        send_args.append("--receipt")

    if email_data.get("attach"):
        send_args.append("--attach")
        for att in email_data["attach"]:
            send_args.append(str(att))

    result = subprocess.run(send_args, capture_output=True, text=True)

    if result.returncode == 0:
        info["status"] = "sent"
        info["sent_at"] = datetime.datetime.now().isoformat()
        with open(schedule_file, "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        print("Email sent / 邮件发送成功")
    else:
        info["status"] = "failed"
        info["error"] = result.stderr or result.stdout
        with open(schedule_file, "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        print("Email send failed / 邮件发送失败")
        print(result.stderr or result.stdout)


def cmd_list_scheduled():
    if not QUEUE_DIR.exists():
        print("Schedule queue is empty / 定时队列为空")
        return

    now = datetime.datetime.now()
    pending = []
    for schedule_file in sorted(QUEUE_DIR.glob("*.json")):
        with open(schedule_file, "r", encoding="utf-8") as f:
            info = json.load(f)
        pending.append(info)

    if not pending:
        print("Schedule queue is empty / 定时队列为空")
        return

    print(f"Scheduled Emails / 定时邮件队列 ({len(pending)} emails)")
    print("=" * 70)
    for info in pending:
        scheduled_time = datetime.datetime.fromisoformat(info["scheduled_time"])
        remaining = scheduled_time - now
        status_icon = {"sent": "Sent", "pending": "Pending", "failed": "Failed", "cancelled": "Cancelled"}.get(info["status"], info["status"])
        print(f"  [{status_icon}] ID: {info['id']}")
        print(f"    To: {info['email'].get('to', 'N/A')}")
        print(f"    Subject: {info['email'].get('subject', 'N/A')}")
        print(f"    Scheduled: {info['scheduled_time']}")
        if info["status"] == "pending":
            if remaining.total_seconds() > 0:
                print(f"    Remaining: {remaining}")
            else:
                print(f"    Overdue by: {-remaining}")
        elif info["status"] == "sent":
            print(f"    Sent at: {info.get('sent_at', 'N/A')}")
        elif info["status"] == "failed":
            print(f"    Error: {info.get('error', 'N/A')}")
        print("-" * 70)


def cmd_cancel(schedule_id):
    schedule_file = QUEUE_DIR / f"{schedule_id}.json"
    if not schedule_file.exists():
        print(f"Schedule not found: {schedule_id}")
        sys.exit(1)

    with open(schedule_file, "r", encoding="utf-8") as f:
        info = json.load(f)

    info["status"] = "cancelled"
    with open(schedule_file, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    print("Schedule cancelled / 已取消定时邮件")
    print(f"  ID: {schedule_id}")
    print(f"  To: {info['email'].get('to', 'N/A')}")
    print(f"  Subject: {info['email'].get('subject', 'N/A')}")
    print(f"  If you added a crontab entry for this schedule, remove it manually with: crontab -e")


def main():
    parser = argparse.ArgumentParser(description="Emailbox - Schedule email sending")
    parser.add_argument("--schedule", action="store_true", help="Schedule a new email")
    parser.add_argument("--process-queue", action="store_true", help="Process due scheduled emails")
    parser.add_argument("--process-one", help="Process a specific schedule by ID")
    parser.add_argument("--list-scheduled", action="store_true", help="List scheduled emails")
    parser.add_argument("--cancel", help="Cancel a scheduled email by ID")

    parser.add_argument("--at", help="Send at specific time (YYYY-MM-DD HH:MM)")
    parser.add_argument("--in", dest="in_minutes", type=int, help="Send in N minutes")

    parser.add_argument("--to", help="Recipients (comma-separated)")
    parser.add_argument("--subject", help="Email subject")
    parser.add_argument("--body", help="Plain text body")
    parser.add_argument("--body-file", help="File path for plain text body")
    parser.add_argument("--html-body", help="HTML body (inline)")
    parser.add_argument("--html-file", help="File path for HTML body")
    parser.add_argument("--cc", help="CC recipients")
    parser.add_argument("--bcc", help="BCC recipients")
    parser.add_argument("--attach", nargs="*", help="Files to attach")
    parser.add_argument("--from-addr", help="Sender email")
    parser.add_argument("--provider", help="Force provider")
    parser.add_argument("--reply-to", help="Original Message-ID for reply")
    parser.add_argument("--forward-from", help="Original sender for forward header")
    parser.add_argument("--forward-date", help="Original date for forward header")
    parser.add_argument("--forward-to", help="Original recipients for forward header")
    parser.add_argument("--forward-cc", help="Original CC for forward header")
    parser.add_argument("--forward-subject", help="Original subject for forward header")
    parser.add_argument("--importance", choices=["high", "normal", "low"], help="Email priority")
    parser.add_argument("--receipt", action="store_true", help="Request read receipt")

    args = parser.parse_args()

    if args.schedule:
        if not args.to or not args.subject:
            print("error: --to and --subject are required for scheduling")
            sys.exit(1)
        if not args.at and not args.in_minutes:
            print("error: specify --at 'YYYY-MM-DD HH:MM' or --in MINUTES")
            sys.exit(1)
        cmd_schedule(args)
    elif args.process_queue:
        cmd_process_queue()
    elif args.process_one:
        cmd_process_one(args.process_one)
    elif args.list_scheduled:
        cmd_list_scheduled()
    elif args.cancel:
        cmd_cancel(args.cancel)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()