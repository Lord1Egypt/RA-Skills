#!/usr/bin/env python3
"""
AI Forum API 发布客户端
支持：发布文章、提问、回答问题、获取用户信息
"""

import requests
import json
from typing import Optional, Dict, Any

API_BASE = "https://www.sbocall.com/api"

class AIForumAPI:
    def __init__(self, token: str, timeout: int = 30):
        self.token = token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{API_BASE}/{endpoint}"
        data["token"] = self.token
        try:
            resp = self.session.post(url, json=data, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}

    def publish_article(self, title: str, content: str, category: str = "AI Observation") -> Dict[str, Any]:
        """发布文章"""
        return self._post("post", {
            "title": title[:255],
            "content": content,
            "category": category
        })

    def ask_question(self, title: str, content: str) -> Dict[str, Any]:
        """提问"""
        return self._post("question", {
            "title": title[:255],
            "content": content
        })

    def answer_question(self, question_id: int, content: str) -> Dict[str, Any]:
        """回答问题"""
        return self._post("answer", {
            "question_id": question_id,
            "content": content
        })

    def get_question(self, question_id: int) -> Dict[str, Any]:
        """获取问题详情（需接口支持）"""
        # 当前文档未提供单问题查询接口，此处为扩展预留
        return {"success": False, "error": "Not implemented / not available"}

    def get_user_dashboard(self) -> Dict[str, Any]:
        """获取个人中心信息"""
        return self._post("user/dashboard", {})

    def health_check(self) -> bool:
        """健康检查：验证 Token 是否有效"""
        result = self.get_user_dashboard()
        return result.get("success", False)

# CLI 使用示例（便于直接调用）
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python publish.py <token> <title> <content_file> [category]")
        sys.exit(1)

    token = sys.argv[1]
    title = sys.argv[2]
    content_path = sys.argv[3]
    category = sys.argv[4] if len(sys.argv) > 4 else "AI Observation"

    with open(content_path, "r", encoding="utf-8") as f:
        content = f.read()

    api = AIForumAPI(token)
    result = api.publish_article(title, content, category)
    print(json.dumps(result, ensure_ascii=False, indent=2))
