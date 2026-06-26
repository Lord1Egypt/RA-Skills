import base64
import json
import os
import re
from typing import Any, Dict, Optional, Tuple

import requests


class CozeImageSkill:
    def __init__(
        self,
        api_token: str,
        *,
        url: str,
        project_id: str,
        session_id: str,
        timeout: int = 60,
    ) -> None:
        self.url = url
        self.project_id = project_id
        self.session_id = session_id
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

    def _build_payload(self, prompt: str) -> Dict[str, Any]:
        return {
            "content": {
                "query": {
                    "prompt": [
                        {
                            "type": "text",
                            "content": {
                                "text": prompt.strip(),
                            },
                        }
                    ]
                }
            },
            "type": "query",
            "session_id": self.session_id,
            "project_id": self.project_id,
        }

    def _find_url_in_string(self, value: str) -> Optional[str]:
        match = re.search(r"https?://\S+", value)
        if not match:
            return None
        return match.group(0).rstrip("),]}>\"'")

    def _extract_image_url(self, value: Any) -> Optional[str]:
        if isinstance(value, str):
            return self._find_url_in_string(value)

        if isinstance(value, list):
            for item in value:
                found = self._extract_image_url(item)
                if found:
                    return found
            return None

        if isinstance(value, dict):
            # Check direct URL fields
            for key in ("url", "image_url", "imageUrl"):
                nested = value.get(key)
                if isinstance(nested, str) and nested.startswith("http"):
                    return nested

            # Special handling for tool_response.result which may contain URL text
            tool_response = value.get("tool_response")
            if isinstance(tool_response, dict):
                result = tool_response.get("result")
                if isinstance(result, str):
                    # Look for URL pattern in result text (e.g., "图片生成成功，图片 URL: https://...")
                    found = self._find_url_in_string(result)
                    if found:
                        return found

            # Recurse into common nested fields
            for key in ("content", "output", "result", "data", "tool_result", "tool_response"):
                found = self._extract_image_url(value.get(key))
                if found:
                    return found

        return None

    def _stream_for_image_url(self, prompt: str) -> Tuple[str, str]:
        response = requests.post(
            self.url,
            headers=self.headers,
            json=self._build_payload(prompt),
            stream=True,
            timeout=self.timeout,
        )
        response.raise_for_status()

        answer_chunks = []

        for line in response.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data:"):
                continue

            payload = line[5:].strip()
            if not payload or payload == "[DONE]":
                continue

            try:
                event_data = json.loads(payload)
            except json.JSONDecodeError:
                continue

            content = event_data.get("content")
            if not isinstance(content, dict):
                content = event_data.get("data", {}).get("content", {})

            answer_piece = content.get("answer") if isinstance(content, dict) else None
            if isinstance(answer_piece, str):
                answer_chunks.append(answer_piece)

            if event_data.get("type") == "error":
                raise RuntimeError(str(content.get("error") if isinstance(content, dict) else "Upstream SSE returned an error event"))

            image_url = self._extract_image_url(event_data)
            if image_url:
                return image_url, "".join(answer_chunks).strip()

        assistant_text = "".join(answer_chunks).strip()
        if assistant_text:
            raise RuntimeError(f"Image URL not found in SSE response. Upstream assistant replied: {assistant_text}")
        raise RuntimeError("Image URL not found in SSE response")

    def _download_as_data_uri(self, image_url: str) -> Tuple[str, str]:
        response = requests.get(image_url, timeout=self.timeout)
        response.raise_for_status()
        mime_type = response.headers.get("Content-Type", "image/png").split(";")[0].strip()
        image_base64 = base64.b64encode(response.content).decode("utf-8")
        return f"data:{mime_type};base64,{image_base64}", mime_type

    def generate(self, prompt: str) -> Dict[str, str]:
        if not prompt or not prompt.strip():
            raise ValueError("prompt is required")

        image_url, answer_text = self._stream_for_image_url(prompt)
        image_data_uri, mime_type = self._download_as_data_uri(image_url)
        extension = mime_type.split("/")[-1] if "/" in mime_type else "png"
        result = {
            "image": image_data_uri,
            "mime_type": mime_type,
            "filename": f"generated-image.{extension}",
            "source_url": image_url,
        }
        if answer_text:
            result["answer_text"] = answer_text
        return result


def _bool_param(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def run(params: Dict[str, Any]) -> Dict[str, Any]:
    prompt = params.get("text") or params.get("prompt") or ""
    api_token = params.get("api_token") or os.environ.get("IMAGE_API_TOKEN")
    api_url = params.get("api_url") or os.environ.get("IMAGE_API_URL", "https://6fj9k4p9x3.coze.site/stream_run")
    project_id = params.get("project_id") or os.environ.get("IMAGE_API_PROJECT_ID", "7621854258107039796")
    session_id = params.get("session_id") or os.environ.get("IMAGE_API_SESSION_ID", "mT8SQeCGgTMZNBsJEiRuN")
    timeout = int(params.get("timeout") or os.environ.get("IMAGE_API_TIMEOUT", "60"))
    include_debug = _bool_param(params.get("include_debug"))
    strict_mode = _bool_param(params.get("strict"))

    try:
        if not api_token:
            raise RuntimeError("Missing IMAGE_API_TOKEN environment variable or params['api_token']")
        if not project_id:
            raise RuntimeError("Missing IMAGE_API_PROJECT_ID environment variable or params['project_id']")
        if not session_id:
            raise RuntimeError("Missing IMAGE_API_SESSION_ID environment variable or params['session_id']")

        client = CozeImageSkill(
            api_token,
            url=api_url,
            project_id=project_id,
            session_id=session_id,
            timeout=timeout,
        )
        result = client.generate(prompt)
        if include_debug:
            result["debug"] = {
                "api_url": api_url,
                "project_id": project_id,
                "session_id": session_id,
            }
        return result
    except Exception as exc:
        if strict_mode:
            raise
        return {
            "error": str(exc),
            "image": None,
            "mime_type": None,
            "filename": None,
            "source_url": None,
        }
