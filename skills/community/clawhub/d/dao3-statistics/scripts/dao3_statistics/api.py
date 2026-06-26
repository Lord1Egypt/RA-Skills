import json
from typing import Any, Dict, Optional

import urllib.error
import urllib.request

API_BASE_URL = "https://code-api-pc.dao3.fun"


def create_auth_headers(token: str, user_agent: str) -> Dict[str, str]:
    return {
        "Authorization": token,
        "user-agent": user_agent,
        "x-dao-ua": user_agent,
    }


def make_api_request(endpoint: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    try:
        request = urllib.request.Request(
            f"{API_BASE_URL}{endpoint}",
            method="GET",
            headers=headers or {},
        )
        with urllib.request.urlopen(request, timeout=30.0) as resp:
            raw = resp.read()
            text = raw.decode("utf-8", errors="replace")
            try:
                return json.loads(text)
            except Exception:
                return {"raw": text}
    except urllib.error.HTTPError as e:
        body = None
        try:
            raw = e.read()
            text = raw.decode("utf-8", errors="replace")
            try:
                body = json.loads(text)
            except Exception:
                body = text
        except Exception:
            body = None

        return {
            "error": "API请求失败",
            "endpoint": endpoint,
            "status_code": getattr(e, "code", None),
            "message": str(e),
            "response": body,
        }
    except urllib.error.URLError as e:
        return {
            "error": "API请求失败",
            "endpoint": endpoint,
            "message": str(e),
        }
    except Exception as e:
        return {
            "error": "API请求失败",
            "endpoint": endpoint,
            "message": str(e),
        }


def to_json_str(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False)
