#!/usr/bin/env python3
"""Upload image to COS, call /claw/generate, output structured JSON for agent follow-up."""

import argparse
import json
import os

# Load environment variables from ~/.openclaw/.env
def _load_env_file():
    env_path = os.path.expanduser("~/.openclaw/.env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    if key not in os.environ:
                        os.environ[key] = value


_load_env_file()

from claw_auth import claw_post, sign_url
from cos_uploader import upload_file_to_cos

CLAW_BASE_URL = os.getenv("CLAW_BASE_URL", "https://leewow.com")
CLAW_PATH_PREFIX = os.getenv("CLAW_PATH_PREFIX", "")
CLAW_SK = os.getenv("CLAW_SK", "")


def generate_preview(image_path: str, template_id: int,
                     design_theme: str = "", aspect_ratio: str = "3:4") -> dict:
    """Upload image and trigger generation. Returns dict with task info."""
    if not CLAW_SK:
        return {"error": "CLAW_SK environment variable is not set."}

    if not os.path.exists(image_path):
        return {"error": f"Image file not found: {image_path}"}

    # Ensure image is in workspace directory
    workspace_dir = os.path.expanduser("~/.openclaw/workspace")
    abs_image_path = os.path.abspath(image_path)
    if not abs_image_path.startswith(workspace_dir):
        return {"error": f"Image must be in workspace directory: {workspace_dir}"}

    try:
        image_url = upload_file_to_cos(image_path, key_prefix="prod-h5-generation-upload/claw-skill")
    except Exception as e:
        return {"error": f"Failed to upload image: {e}"}

    url = f"{CLAW_BASE_URL}{CLAW_PATH_PREFIX}/claw/generate"
    payload = {
        "templateId": template_id,
        "imageUrl": image_url,
        "designTheme": design_theme,
        "aspectRatio": aspect_ratio,
    }

    try:
        resp = claw_post(CLAW_SK, url, json_data=payload, timeout=30)
        data = resp.json()
    except Exception as e:
        return {"error": f"Failed to call generate API: {e}"}

    if data.get("code") != 0:
        return {"error": f"API returned: {data.get('message', 'Unknown error')}"}

    result = data.get("data", {})
    result["_success"] = True
    return result


def _safe_result(result: dict) -> dict:
    """Build safe output for the agent.

    The browse step returns final markdown directly. Generate returns task state only,
    so the agent can continue to poll with get_generation_status.
    """
    if "error" in result:
        return result

    task_id = result.get("taskId", "unknown")
    preview_url = result.get("previewUrl")

    out = {
        "taskId": task_id,
        "status": result.get("status", "PENDING"),
        "estimatedSeconds": result.get("estimatedSeconds", 45),
        "templateId": result.get("templateId"),
    }

    if preview_url and CLAW_SK:
        out["purchaseUrl"] = sign_url(CLAW_SK, preview_url)

    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-path", type=str, required=True)
    parser.add_argument("--template-id", type=int, required=True)
    parser.add_argument("--design-theme", type=str, default="")
    parser.add_argument("--aspect-ratio", type=str, default="3:4")
    parser.add_argument("--json", action="store_true", help="(compat) always outputs safe JSON")
    args = parser.parse_args()

    result = generate_preview(args.image_path, args.template_id, args.design_theme, args.aspect_ratio)
    print(json.dumps(_safe_result(result), ensure_ascii=False, indent=2))
