#!/usr/bin/env python3
"""Render highlight(s) or fragmovie via Demo-Slap API.

Polls render status every minute, outputs clip URL(s) when done.
Writes progress to state.json.
"""
import sys
import time
import json
import argparse
from demo_slap_common import api_demo_slap, write_state, append_log

POLL_INTERVAL = 60  # seconds


def run_render(job_id, highlight_ids, mode="render", chat_id=None):
    """
    mode: "render" for single highlight, "render-fragmovie" for multiple.
    """
    endpoint = mode
    payload = {"highlightIds": highlight_ids}
    if mode == "render-fragmovie":
        payload["introTitle"] = "Fragmovie"

    print(f"🚀 Submitting {mode} for job {job_id}, highlights: {highlight_ids}")
    write_state(
        "rendering",
        op="render",
        job_id=job_id,
        render_mode=mode,
        progress="submitting",
        chat_id=chat_id,
        clip_urls={},
    )

    res = api_demo_slap("POST", f"/public-api/{endpoint}/{job_id}", payload)
    if not res["success"]:
        write_state("error", op="render", job_id=job_id, error=f"Render submit failed: {res}")
        print(f"❌ Render submission failed: {res}")
        sys.exit(1)

    render_job_id = res["data"].get("jobId", job_id)
    estimated = res["data"].get("estimatedFinishAt")
    print(f"⏳ Render JobID: {render_job_id}")
    if estimated:
        print(f"⏰ Estimated finish: {estimated}")
    write_state(
        "rendering",
        op="render",
        job_id=job_id,
        render_job_id=render_job_id,
        render_mode=mode,
        progress="polling 0",
        estimated_finish=estimated,
        chat_id=chat_id,
    )
    append_log(f"RENDER started job={job_id} render_job={render_job_id} mode={mode} highlights={highlight_ids} chat_id={chat_id}")

    poll_count = 0
    max_polls = 30  # 30 minutes max

    while poll_count < max_polls:
        poll_count += 1
        time.sleep(POLL_INTERVAL)

        status_res = api_demo_slap("GET", f"/public-api/{endpoint}/{render_job_id}/status")
        if not status_res["success"]:
            write_state(
                "error",
                op="render",
                job_id=job_id,
                render_job_id=render_job_id,
                error=f"Status check failed: {status_res}",
            )
            print(f"❌ Render status check failed: {status_res}")
            sys.exit(1)

        data = status_res["data"]
        all_done = True
        has_error = False

        if isinstance(data, dict):
            if not data:
                all_done = False
            elif "status" in data and isinstance(data["status"], str):
                s = data["status"]
                all_done = (s == "done")
                has_error = (s in ("error", "failed"))
            else:
                for _, v in data.items():
                    if isinstance(v, dict) and "status" in v:
                        s = v["status"]
                        if s != "done":
                            all_done = False
                        if s in ("error", "failed"):
                            has_error = True

        # Extract ETA from first poll if not already known
        if not estimated and isinstance(data, dict):
            for v in data.values():
                if isinstance(v, dict) and "estimatedFinishAt" in v:
                    estimated = v["estimatedFinishAt"]
                    print(f"⏰ Estimated finish: {estimated}")
                    break

        status_str = json.dumps(data) if isinstance(data, dict) else str(data)
        print(f"📊 Poll {poll_count}/{max_polls}: {status_str}")
        write_state(
            "rendering",
            op="render",
            job_id=job_id,
            render_job_id=render_job_id,
            render_mode=mode,
            estimated_finish=estimated,
            chat_id=chat_id,
            progress=f"polling {poll_count}/{max_polls}",
        )

        if has_error:
            write_state("error", op="render", job_id=job_id, render_job_id=render_job_id, error="Render failed on server")
            print("❌ Render failed on server!")
            sys.exit(1)

        if all_done:
            break
    else:
        write_state("error", op="render", job_id=job_id, render_job_id=render_job_id, error="Timeout: max polls reached")
        print("❌ Timeout: render did not complete in time.")
        sys.exit(1)

    # Fetch clip URLs
    print("✅ Render complete! Fetching URLs...")
    data_res = api_demo_slap("GET", f"/public-api/{endpoint}/{render_job_id}/data")
    if not data_res["success"]:
        write_state(
            "error",
            op="render",
            job_id=job_id,
            render_job_id=render_job_id,
            error=f"Fetch data failed: {data_res}",
        )
        print(f"❌ Failed to fetch render data: {data_res}")
        sys.exit(1)

    clips = data_res["data"].get("highlightClips", {})
    if not clips:
        frag_url = data_res["data"].get("fragmovieUrl")
        if frag_url:
            clips = {"fragmovie": frag_url}

    if not clips:
        write_state("error", op="render", job_id=job_id, render_job_id=render_job_id, error="No clip URLs in response")
        print(f"❌ No URLs found in response: {data_res['data']}")
        sys.exit(1)

    # Collect all URLs
    clip_urls = {}
    for k, v in clips.items():
        url = v.get("clipUrl") if isinstance(v, dict) else v
        clip_urls[k] = url

    write_state(
        "done",
        op="render",
        last_completed_op="render",
        job_id=job_id,
        render_job_id=render_job_id,
        render_mode=mode,
        chat_id=chat_id,
        clip_urls=clip_urls,
    )
    append_log(f"RENDER done job={job_id} render_job={render_job_id} urls={clip_urls} chat_id={chat_id}")

    # Output URLs
    print(f"\n===CLIP_URLS_START===")
    for k, url in clip_urls.items():
        print(f"{k}: {url}")
    print(f"===CLIP_URLS_END===")

    # Notify OpenClaw via system event (fallback)
    import subprocess
    first_url = next(iter(clip_urls.values()))
    event_text = f"[demo-slap] Render done. JobID: {job_id}. ChatID: {chat_id}. Clip URL: {first_url}. Watchdog should send media to ChatID."
    try:
        subprocess.run(["openclaw", "system", "event", "--text", event_text, "--mode", "now"], check=True)
    except Exception as e:
        print(f"⚠️  System event failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render CS2 highlight/fragmovie via Demo-Slap API")
    parser.add_argument("job_id", help="Analyze Job ID")
    parser.add_argument("highlight_ids", nargs="+", help="Highlight ID(s) to render")
    parser.add_argument("--fragmovie", action="store_true", help="Render as fragmovie (stitch multiple)")
    parser.add_argument("--chat-id", help="Originating chat ID for notifications (e.g. telegram:182314856)")
    args = parser.parse_args()

    mode = "render-fragmovie" if args.fragmovie or len(args.highlight_ids) > 1 else "render"
    run_render(args.job_id, args.highlight_ids, mode=mode, chat_id=args.chat_id)
