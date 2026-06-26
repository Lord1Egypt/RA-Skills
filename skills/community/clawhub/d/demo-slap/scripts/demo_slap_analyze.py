#!/usr/bin/env python3
"""Submit a CS2 demo for analysis and poll until highlights are ready.

Outputs highlight metadata as JSON to stdout when done.
Writes progress to state.json.
"""
import sys
import time
import json
import argparse
import os

from demo_slap_common import api_demo_slap, write_state, append_log, DATA_DIR, write_highlights

POLL_INTERVAL = 60  # seconds


def resolve_steam_id(username):
    """Resolve Steam64 ID from username via steam_ids.json."""
    steam_ids_file = os.path.join(DATA_DIR, "steam_ids.json")
    if not os.path.exists(steam_ids_file):
        return None
    with open(steam_ids_file, "r") as f:
        data = json.load(f)
    return data.get(username)


def run_analyze(replay_url, steam_id=None, chat_id=None):
    print(f"✅ Demo URL: {replay_url}")
    print(f"🚀 Submitting to Demo-Slap for analysis...")

    write_state(
        "analyzing",
        op="analyze",
        progress="submitting",
        replay_url=replay_url,
        chat_id=chat_id,
        clip_urls={},
        highlights_count=0,
    )

    res = api_demo_slap("POST", "/public-api/analyze/url", {"url": replay_url})
    if not res["success"]:
        write_state("error", op="analyze", error=f"Submit failed: {res}")
        print(f"❌ Analysis submission failed: {res}")
        sys.exit(1)

    job_id = res["data"]["jobId"]
    print(f"⏳ JobID: {job_id}")
    write_state("analyzing", op="analyze", job_id=job_id, progress="polling 0", chat_id=chat_id)
    append_log(f"ANALYZE started job={job_id} url={replay_url} chat_id={chat_id}")

    poll_count = 0
    max_polls = 30  # 30 minutes max

    while poll_count < max_polls:
        poll_count += 1
        time.sleep(POLL_INTERVAL)

        status_res = api_demo_slap("GET", f"/public-api/analyze/{job_id}/status")
        if not status_res["success"]:
            write_state("error", op="analyze", job_id=job_id, error=f"Status check failed: {status_res}")
            print(f"❌ Status check failed: {status_res}")
            sys.exit(1)

        status = status_res["data"].get("status", "unknown")
        print(f"📊 Poll {poll_count}/{max_polls}: status={status}")
        write_state(
            "analyzing",
            op="analyze",
            job_id=job_id,
            progress=f"polling {poll_count}/{max_polls} status={status}",
            chat_id=chat_id,
        )

        if status == "done":
            break
        elif status in ("error", "failed"):
            write_state("error", op="analyze", job_id=job_id, error="Analysis failed on server")
            print("❌ Analysis failed on server.")
            sys.exit(1)
    else:
        write_state("error", op="analyze", job_id=job_id, error="Timeout: max polls reached")
        print("❌ Timeout: analysis did not complete in time.")
        sys.exit(1)

    # Fetch highlights
    print("✅ Analysis complete! Fetching highlights...")
    data_res = api_demo_slap("GET", f"/public-api/analyze/{job_id}/data")
    if not data_res["success"]:
        write_state("error", op="analyze", job_id=job_id, error=f"Fetch data failed: {data_res}")
        print(f"❌ Failed to fetch data: {data_res}")
        sys.exit(1)

    highlights = data_res["data"].get("highlights", [])

    # Filter by steam ID
    if steam_id:
        highlights = [h for h in highlights if h.get("steamId") == steam_id]

    write_highlights(highlights)

    if not highlights:
        write_state(
            "done",
            op="analyze",
            last_completed_op="analyze",
            job_id=job_id,
            chat_id=chat_id,
            highlights_count=0,
        )
        print("❌ No highlights found.")
        sys.exit(0)

    write_state(
        "done",
        op="analyze",
        last_completed_op="analyze",
        job_id=job_id,
        chat_id=chat_id,
        highlights_count=len(highlights),
    )
    append_log(f"ANALYZE done job={job_id} highlights={len(highlights)} chat_id={chat_id}")

    # Output JSON to stdout
    print(f"\n===HIGHLIGHTS_JSON_START===")
    print(json.dumps(highlights, indent=2, ensure_ascii=False))
    print(f"===HIGHLIGHTS_JSON_END===")
    print(f"\nJobID: {job_id}")
    print(f"Total highlights: {len(highlights)}")

    # Notify OpenClaw via system event (fallback)
    import subprocess
    event_text = f"[demo-slap] Analysis done. JobID: {job_id}. Highlights: {len(highlights)}. ChatID: {chat_id}. Watchdog should send highlights from highlights.json."
    try:
        subprocess.run(["openclaw", "system", "event", "--text", event_text, "--mode", "now"], check=True)
    except Exception as e:
        print(f"⚠️  System event failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a CS2 demo via Demo-Slap API")
    parser.add_argument("--url", required=True, help="Demo download URL")
    parser.add_argument("--steam-id", help="Filter highlights by Steam64 ID")
    parser.add_argument("--username", help="Filter highlights by username (resolves to Steam64 ID)")
    parser.add_argument("--chat-id", help="Originating chat ID for notifications (e.g. telegram:182314856)")
    args = parser.parse_args()

    steam_id = args.steam_id
    if not steam_id and args.username:
        steam_id = resolve_steam_id(args.username)
        if not steam_id:
            print(f"❌ Unknown username '{args.username}'")
            sys.exit(1)

    run_analyze(args.url, steam_id=steam_id, chat_id=args.chat_id)
