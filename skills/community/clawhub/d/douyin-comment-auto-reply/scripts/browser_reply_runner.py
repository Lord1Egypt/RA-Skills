#!/usr/bin/env python3
import argparse, json, shlex, subprocess, sys, time
from pathlib import Path


def run(cmd: str):
    print(f"$ {cmd}")
    subprocess.run(cmd, shell=True, check=True)


def main():
    p = argparse.ArgumentParser(description="Run Douyin comment replies via agent-browser CLI")
    p.add_argument("drafts_json", help="JSON file from batch_comment_drafts.py")
    p.add_argument("--url", required=True, help="Douyin creator comment management URL")
    p.add_argument("--reply-box-selector", required=True, help="CSS selector for reply textbox")
    p.add_argument("--submit-selector", required=True, help="CSS selector for submit/reply button")
    p.add_argument("--session-name", default="douyin-comment-auto-reply")
    p.add_argument("--max-replies", type=int, default=20)
    p.add_argument("--force-review", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--wait-ms", type=int, default=1200)
    p.add_argument("--browser-cmd", default="npx -y agent-browser", help="agent-browser command prefix")
    args = p.parse_args()

    drafts = json.loads(Path(args.drafts_json).read_text(encoding="utf-8"))
    sendable = []
    for item in drafts:
        action = item.get("suggested_action", "")
        if action in {"public_reply", "public_reply_plus_dm"}:
            sendable.append(item)
        elif action == "public_reply_review" and args.force_review:
            sendable.append(item)

    sendable = sendable[: args.max_replies]
    print(f"Loaded {len(sendable)} sendable replies")
    if not sendable:
        return

    open_cmd = f"{args.browser_cmd} --session-name {shlex.quote(args.session_name)} open {shlex.quote(args.url)}"
    wait_cmd = f"{args.browser_cmd} --session-name {shlex.quote(args.session_name)} wait --load networkidle"
    run(open_cmd)
    run(wait_cmd)

    log = []
    for idx, item in enumerate(sendable, 1):
        reply = item.get("public_reply", "").strip()
        if not reply:
            continue
        print(f"[{idx}/{len(sendable)}] replying to: {item.get('comment','')}")
        fill_cmd = f"{args.browser_cmd} --session-name {shlex.quote(args.session_name)} fill {shlex.quote(args.reply_box_selector)} {shlex.quote(reply)}"
        click_cmd = f"{args.browser_cmd} --session-name {shlex.quote(args.session_name)} click {shlex.quote(args.submit_selector)}"
        if args.dry_run:
            print(fill_cmd)
            print(click_cmd)
        else:
            run(fill_cmd)
            run(click_cmd)
            time.sleep(args.wait_ms / 1000)
        log.append({
            "comment": item.get("comment", ""),
            "reply": reply,
            "suggested_action": item.get("suggested_action", ""),
        })

    out = Path(args.drafts_json).with_suffix(".sent-log.json")
    out.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"sent log: {out}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}", file=sys.stderr)
        sys.exit(e.returncode or 1)
