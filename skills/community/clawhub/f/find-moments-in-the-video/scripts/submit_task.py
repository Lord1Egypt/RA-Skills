import argparse
import json
import os
import sys
from datetime import datetime
import urllib.request
import urllib.error

# Get API Key from environment variable
API_KEY = os.environ.get("WAYIN_API_KEY")

if not API_KEY:
    print("Error: WAYIN_API_KEY environment variable is not set.", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://wayinvideo-api.wayin.ai/api/v2/clips/find-moments"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
    "x-wayinvideo-api-version": "v2",
    "user-agent": "find-moments skill"
}

def submit_task(payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(BASE_URL, data=data, headers=HEADERS, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            status = response.getcode()
            response_text = response.read().decode("utf-8")
            
            if status != 200:
                print(f"DEBUG: Response Status: {status}", file=sys.stderr)
                print(f"DEBUG: Response Text: {response_text}", file=sys.stderr)
                raise Exception(f"API request failed with status {status}: {response_text}")

            response_json = json.loads(response_text)
            data_res = response_json.get("data")

            if not data_res or ("project_id" not in data_res and "id" not in data_res):
                raise Exception(f"Unexpected response structure from submit API: {response_text}")
            return data_res.get("project_id") or data_res.get("id")
            
    except urllib.error.HTTPError as e:
        error_text = e.read().decode("utf-8")
        print(f"DEBUG: HTTP Error {e.code}: {error_text}", file=sys.stderr)
        raise Exception(f"HTTP Error {e.code}: {error_text}")
    except Exception as e:
        print(f"DEBUG: Request failed: {str(e)}", file=sys.stderr)
        raise e

def save_initial_state(prefix, project_id, submit_payload, output_dir=None):
    # Try to find workspace root if output_dir is not provided
    if not output_dir:
        current_path = os.path.abspath(__file__)
        workspace_root = None
        while True:
            parent_path = os.path.dirname(current_path)
            if parent_path == current_path: break
            if os.path.exists(os.path.join(parent_path, "AGENTS.md")):
                workspace_root = parent_path
                break
            current_path = parent_path
        
        output_dir = os.path.join(workspace_root or os.getcwd(), "api_results")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_data = {
        "_metadata": {
            "id": project_id,
            "query": submit_payload.get("query"),
            "submit_payload": submit_payload,
            "api_endpoint": BASE_URL,
            "task_submitted_at": datetime.now().isoformat(),
            "status": "SUBMITTED"
        }
    }
    
    filename = os.path.join(output_dir, f"{prefix}_{project_id}_{timestamp}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=2)
    
    return os.path.abspath(filename)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--source", default=None)
    parser.add_argument("--target", default=None)
    parser.add_argument("--name", default=None)
    parser.add_argument("--export", action="store_true", default=False)
    parser.add_argument("--ratio", choices=["RATIO_16_9", "RATIO_1_1", "RATIO_4_5", "RATIO_9_16"], default=None)
    parser.add_argument("--resolution", choices=["SD_480", "HD_720", "FHD_1080", "QHD_2K", "UHD_4K"], default="FHD_1080")
    parser.add_argument("--caption-display", choices=["none", "both", "original", "translation"], default=None)
    parser.add_argument("--cc-style-tpl", default=None)
    parser.add_argument("--ai-hook", action="store_true", default=False)
    parser.add_argument("--ai-hook-style", choices=["serious", "casual", "informative", "conversational", "humorous", "parody", "inspirational", "dramatic", "empathetic", "persuasive", "neutral", "excited", "calm"], default="serious")
    parser.add_argument("--ai-hook-pos", choices=["beginning", "end"], default="beginning")
    parser.add_argument("--top-k", type=int, default=10, help="The best K moments to return. Defaults to 10. Pass -1 to return all matching moments.")
    parser.add_argument("--save-dir", default=None, help="Directory to save the initial state JSON file.")
    args = parser.parse_args()

    # Determine caption setting
    enable_caption = False
    caption_display = args.caption_display
    
    if caption_display == "none":
        enable_caption = False
        caption_display = None
    elif caption_display:
        enable_caption = True
    else: 
        enable_caption = True
        caption_display = "translation" if args.target else "original"

    # Default caption style logic
    cc_style_tpl = args.cc_style_tpl
    if cc_style_tpl is None:
        if caption_display == "both":
            cc_style_tpl = "temp-static-2"
        else:
            cc_style_tpl = "word-focus"

    if caption_display == "both" and not (cc_style_tpl and cc_style_tpl.startswith("temp-static-")):
        print(f"ERROR: `--cc-style-tpl` can only be `temp-static-...` when `--caption-display both`", file=sys.stderr)
        sys.exit(1)

    # Non-sensitive data will be persisted for debugging; sensitive data such as API keys in environment variables will not be persisted.
    submit_payload = {
        "video_url": args.url,
        "query": args.query,
        "enable_export": args.export,
        "enable_caption": enable_caption,
        "enable_ai_reframe": True if args.ratio else False,
        "enable_ai_hook": args.ai_hook
    }
    if args.ai_hook_style: submit_payload["ai_hook_script_style"] = args.ai_hook_style
    if args.ai_hook_pos: submit_payload["ai_hook_position"] = args.ai_hook_pos
    if args.source: submit_payload["source_lang"] = args.source.lower().replace("_", "-")
    if args.target: submit_payload["target_lang"] = args.target.lower().replace("_", "-")
    if args.name: submit_payload["project_name"] = args.name
    if args.ratio: submit_payload["ratio"] = args.ratio
    if args.resolution: submit_payload["resolution"] = args.resolution
    if caption_display: submit_payload["caption_display"] = caption_display
    if cc_style_tpl: submit_payload["cc_style_tpl"] = cc_style_tpl
    if args.top_k != -1: submit_payload["limit"] = args.top_k

    try:
        project_id = submit_task(submit_payload)
        abs_path = save_initial_state("moments", project_id, submit_payload, output_dir=args.save_dir)
        print(f"SUCCESS: Task submitted. Project ID: {project_id}")
        print(f"Initial state saved to: {abs_path}")
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
