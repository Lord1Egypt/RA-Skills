import os
import sys
import requests
import json
import argparse
from typing import Dict, Any, Tuple
from urllib.parse import urlparse

BASE_URL = "https://qianfan.baidubce.com/v2"

def resolve_sandbox_url(api_key: str, original_url: str) -> Tuple[str, Dict[str, str]]:
    """若当前在沙盒环境中，将目标 URL 替换为代理 URL，并返回需要附加的 headers。"""
    session_id = os.environ.get("DUMATE_SESSION_ID")
    scheduler_url = os.environ.get("DUMATE_SCHEDULER_URL")

    headers = {
        "Content-Type": "application/json",
    }
    if not session_id or not scheduler_url:
        if not api_key:
            raise ValueError("未设置 API Key，请通过环境变量 BAIDU_API_KEY 设置或使用")
        headers.update({
            "Authorization": f"Bearer {api_key}",
            "X-Appbuilder-From": "openclaw",
        })
        return original_url, headers

    parsed = urlparse(original_url)
    proxy_url = f"{scheduler_url}/api/qianfanproxy{parsed.path}"
    if parsed.query:
        proxy_url += f"?{parsed.query}"

    headers.update({
        "Host": parsed.netloc,
        "X-Dumate-Session-Id": session_id,
        "X-Appbuilder-From": "desktop",
    })
    return proxy_url, headers

def ai_picture_book_task_create(api_key: str, method: int, content):
    url = f"{BASE_URL}/tools/ai_picture_book/task_create"
    url, headers = resolve_sandbox_url(api_key, url)
    params = {
        "method": method,
        "input_type": "1",
        "input_content": content,
    }
    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()
    result = response.json()
    if "code" in result:
        raise RuntimeError(result["detail"])
    if "errno" in result and result["errno"] != 0:
        raise RuntimeError(result["errmsg"])
    return result["data"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="创建AI绘本任务")
    parser.add_argument("--content", required=True, help="输入文字内容，绘本内容，故事或描述")
    parser.add_argument("--method", required=True, type=int, choices=[9, 10], help="绘本类型，9-静态绘本或10-动态绘本")
    parser.add_argument("--api_key", default=os.environ.get("BAIDU_API_KEY"), help="API Key")
    args = parser.parse_args()
    content = args.content
    method = args.method
    api_key = args.api_key

    try:
        results = ai_picture_book_task_create(api_key, method, content)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
