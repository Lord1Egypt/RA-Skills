#!/usr/bin/env python3
import sys
import argparse
import os
import requests
import time
from minimax_client import MinimaxClient, get_standard_path


def main():
    parser = argparse.ArgumentParser(description="Generate video using MiniMax Hailuo-02")
    parser.add_argument("prompt", help="Text prompt for video generation")
    parser.add_argument("--model", default="MiniMax-Hailuo-02", help="Model name")
    parser.add_argument("--project", help="Project name for sub-directory storage")
    parser.add_argument("--output-dir", help="Override output root directory")
    parser.add_argument("--estimate", action="store_true", help="Only estimate cost, don't execute")
    args = parser.parse_args()

    try:
        client = MinimaxClient()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(client.get_budget_report(args.model))
    if args.estimate:
        sys.exit(0)

    data = {
        "model": args.model,
        "prompt": args.prompt,
        "response_format": "url"
    }

    print(f"Creating video task: {args.prompt}...")
    resp = client.post("video_generation", data)

    if resp.get("base_resp", {}).get("status_code") == 0:
        task_id = resp.get("task_id")
        print(f"✅ Task created! Task ID: {task_id}")
        print("⚠️ 视频链接有效期仅 9 小时，请生成完成后立即下载！")
        print("Polling for completion (this may take a few minutes)...")

        while True:
            status_resp = client.get(f"query_video_generation?task_id={task_id}")
            if status_resp.get("base_resp", {}).get("status_code") == 0:
                file_id = status_resp.get("file_id")
                if file_id:
                    print(f"Video generation complete! File ID: {file_id}")
                    video_url = status_resp.get("video_url")
                    if video_url:
                        target_dir, filename_base = get_standard_path("VID", project=args.project, prompt_slug=args.prompt, output_dir=args.output_dir)
                        filepath = os.path.join(target_dir, f"{filename_base}.mp4")

                        vid_data = requests.get(video_url).content
                        with open(filepath, 'wb') as f:
                            f.write(vid_data)

                        client.print_saved_result(filepath, "Video", project=args.project)
                        print("⚠️ 若平台同时返回临时下载链接，请尽快校验并保存。")
                        print(f"MEDIA:{filepath}")
                    else:
                        print(f"Video ready but download URL not in query response. Resp: {status_resp}")
                    break
                else:
                    print("Still processing...")
            else:
                print(f"Polling status: {status_resp}")
            time.sleep(30)
    else:
        print(f"Error: {resp}")


if __name__ == "__main__":
    main()
