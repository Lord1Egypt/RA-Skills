import time
from typing import Any, Dict, Optional

from toolkit.api_client import VolcengineAPIClient
from toolkit.config import ConfigManager


def _extract_vision_summary(response: Dict[str, Any]) -> str:
    output = response.get("output", [])
    if isinstance(output, list):
        for item in output:
            if not isinstance(item, dict):
                continue
            if item.get("type") == "summary_text" and item.get("text"):
                return str(item["text"])
            content = item.get("content", [])
            if isinstance(content, list):
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") in ("output_text", "text") and block.get("text"):
                        return str(block["text"])
    return ""


def run_smoke_test(
    client: Optional[Any] = None,
    image_prompt: str = "赛博朋克风格的城市夜景",
    video_prompt: str = "镜头向上升，天空中飞行汽车呼啸而过",
    poll_interval: float = 5.0,
    max_polls: int = 24,
) -> Dict[str, Any]:
    owned_client = client is None
    if owned_client:
        client = VolcengineAPIClient(ConfigManager())

    result: Dict[str, Any] = {
        "ok": False,
        "step": "start",
        "image": {},
        "vision": {},
        "video": {},
    }

    try:
        result["step"] = "image_generation"
        image_response = client.post(
            "/images/generations",
            json={
                "model": "doubao-seedream-4-0-250828",
                "prompt": image_prompt,
                "size": "1024x1024",
                "response_format": "url",
            },
        )
        image_url = ((image_response.get("data") or [{}])[0]).get("url")
        if not image_url:
            result["error"] = "image url missing in response"
            return result
        result["image"] = {"url": image_url}

        result["step"] = "vision_understanding"
        vision_response = client.post(
            "/responses",
            json={
                "model": "doubao-seed-1-6-vision-250815",
                "input": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_image", "image_url": image_url},
                            {"type": "input_text", "text": "用一句话描述这张图"},
                        ],
                    }
                ],
            },
        )
        result["vision"] = {"summary": _extract_vision_summary(vision_response)}

        result["step"] = "video_generation"
        video_create_response = client.post(
            "/contents/generations/tasks",
            json={
                "model": "doubao-seedance-1-5-pro-251215",
                "content": [
                    {
                        "type": "text",
                        "text": f"{video_prompt} --duration 5 --watermark true",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                ],
            },
        )
        task_id = video_create_response.get("id")
        if not task_id:
            result["error"] = "video task id missing in response"
            return result

        result["video"] = {"task_id": task_id, "status": "running", "url": None}

        for _ in range(max_polls):
            task_response = client.get(f"/contents/generations/tasks/{task_id}")
            status = task_response.get("status", "unknown")
            content = task_response.get("content") or {}
            video_url = content.get("video_url")
            result["video"] = {"task_id": task_id, "status": status, "url": video_url}

            if status in ("succeeded", "failed", "cancelled"):
                result["ok"] = status == "succeeded"
                if not result["ok"]:
                    result["error"] = task_response.get("error") or f"video task ended with status: {status}"
                return result

            time.sleep(poll_interval)

        result["step"] = "video_polling"
        result["error"] = "video task polling timeout"
        return result
    except Exception as exc:
        result["error"] = str(exc)
        return result
    finally:
        if owned_client:
            client.close()
