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

def ai_picture_book_task_query(api_key: str, task_id: str):
    url = f"{BASE_URL}/tools/ai_picture_book/query"
    url, headers = resolve_sandbox_url(api_key, url)
    task_ids = task_id.split(",")
    params = {
        "task_ids": task_ids,
    }
    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()
    result = response.json()
    datas = []
    if "code" in result:
        raise RuntimeError(result["detail"])
    if "errno" in result and result["errno"] != 0:
        raise RuntimeError(result["errmsg"])
    if "data" in result and len(result["data"]) > 0:
        for item in result["data"]:
            if item["result"]:
                bosUrl = item["result"].get("video_bos_url", "")
                del item["result"]
                item["video_bos_url"] = bosUrl
            datas.append(item)
    return datas


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="查询AI绘本生成任务状态")
    parser.add_argument("--task_id", required=True, help="任务ID")
    parser.add_argument("--api_key", default=os.environ.get("BAIDU_API_KEY"), help="API Key")
    args = parser.parse_args()
    task_id = args.task_id
    api_key = args.api_key

    try:
        results = ai_picture_book_task_query(api_key, task_id)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
