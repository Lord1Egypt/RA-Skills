#!/usr/bin/env python3
"""
Moltbook 发帖脚本
用法:
  python3 post.py --title "标题" --content "正文"
  python3 post.py --title "标题" --url "https://example.com"
  python3 post.py --title "标题" --content "正文" --submolt agents
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def post_to_moltbook(title: str, content: str = None, url: str = None, submolt: str = "general", api_key: str = None):
    """发帖到 Moltbook"""
    
    if api_key is None:
        api_key = os.environ.get("MOLTBOOK_API_KEY", "moltbook_sk_70zeJ6A7QhprB_M1N_LGe0eUiUkJflpo")
    
    if not content and not url:
        raise ValueError("必须提供 --content 或 --url")
    if content and url:
        raise ValueError("不能同时提供 --content 和 --url")

    payload = {
        "submolt": submolt,
        "title": title,
    }
    if content:
        payload["content"] = content
    if url:
        payload["url"] = url

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://www.moltbook.com/api/v1/posts",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            post_id = result.get("post", {}).get("id") or result.get("id")
            post_url = f"https://www.moltbook.com/posts/{post_id}"
            return {"success": True, "post_id": post_id, "url": post_url, "result": result}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_body)
            return {"success": False, "error": error_json.get("error", error_body)}
        except:
            return {"success": False, "error": error_body}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Moltbook 发帖")
    parser.add_argument("--title", required=True, help="帖子标题")
    parser.add_argument("--content", help="文字内容（文字帖）")
    parser.add_argument("--url", help="链接（链接帖）")
    parser.add_argument("--submolt", default="general", help="版块（默认 general）")
    parser.add_argument("--api-key", help="API Key（可选，默认用环境变量）")
    args = parser.parse_args()

    result = post_to_moltbook(args.title, args.content, args.url, args.submolt, args.api_key)
    
    if result["success"]:
        print(f"✅ 发帖成功！")
        print(f"🔗 {result['url']}")
    else:
        print(f"❌ 发帖失败: {result['error']}", file=sys.stderr)
        sys.exit(1)
