#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查找阿里邮箱员工邮箱脚本 - OpenClaw Skill
支持命令行参数和环境变量配置
"""

import os
import requests
import time
import sys
import json
from pathlib import Path


class AliMailAction:
    def __init__(self):
        self._load_config_fallback()
        # 实时读取环境变量，自动处理前后空格
        self.cid = os.getenv("ALIMAIL_CLIENT_ID")
        self.secret = os.getenv("ALIMAIL_CLIENT_SECRET")
        self.base = "https://alimail-cn.aliyuncs.com"
        self._token = None
        self._exp = 0

    def _load_config_fallback(self):
        """
        If environment variables are missing, try to load from openclaw.json
        如果环境变量缺失，尝试从 openclaw.json 加载
        """
        if not os.getenv("ALIMAIL_CLIENT_ID"):
            config_path = Path.home() / ".openclaw" / "openclaw.json"
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        # Ensure the path matches your JSON structure
                        # 确保路径匹配您的 JSON 结构：skills -> entries -> alimail -> env
                        env_cfg = config.get("skills", {}).get("entries", {}).get("alimail", {}).get("env", {})
                        if env_cfg:
                            os.environ["ALIMAIL_CLIENT_ID"] = env_cfg.get("ALIMAIL_CLIENT_ID", "")
                            os.environ["ALIMAIL_CLIENT_SECRET"] = env_cfg.get("ALIMAIL_CLIENT_SECRET", "")
                except Exception as e:
                    # Debug print to stderr so it doesn't break JSON output
                    print(f"DEBUG: Failed to load config file: {e}", file=sys.stderr)

    def _auth(self):
        if not self.cid or not self.secret:
            return "ERROR: Missing ALIMAIL_CLIENT_ID or ALIMAIL_CLIENT_SECRET in Settings"

        if self._token and time.time() < self._exp:
            return self._token

        url = f"{self.base}/oauth2/v2.0/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.cid,
            "client_secret": self.secret
        }

        try:
            # 必须使用 data= 发送 application/x-www-form-urlencoded 格式
            resp = requests.post(url, data=payload, timeout=10)
            if resp.status_code != 200:
                return f"AUTH_ERROR ({resp.status_code}): {resp.text}"

            data = resp.json()
            self._token = data.get("access_token")
            # 预留 60 秒缓冲区
            self._exp = time.time() + int(data.get("expires_in", 3600)) - 60
            return self._token
        except Exception as e:
            return f"AUTH_EXCEPTION: {str(e)}"

    def run(self, name):
        token = self._auth()
        if "ERROR" in str(token) or "EXCEPTION" in str(token):
            return {"status": "auth_failed", "details": token}

        url = f"{self.base}/v2/users"
        params = {"filter": f"(name=*{name})", "size": 10}
        headers = {"Authorization": f"Bearer {token}"}

        try:

            res = requests.get(url, params=params, headers=headers, timeout=10)
            res.raise_for_status()
            data = res.json()
            # 数据清洗：确保返回的是 AI 易读的英文 Key 结构
            refined = [
                {
                    "name": u.get("name"),
                    "email": u.get("email"),
                    "employeeNo": u.get("employeeNo")
                } for u in data.get("users", [])
            ]
            return {"users": refined, "total": data.get("total", 0)}
        except Exception as e:
            return {"status": "api_failed", "details": str(e)}


def handler(name):
    # 兼容处理：尝试从 args 或 args['params'] 中获取 name
    # name = args.get("name") or args.get("params", {}).get("name")
    if not name:
        return {"status": "error", "message": "Parameter 'name' is required"}

    client = AliMailAction()
    return client.run(name)


if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print({"status": "error", "message": "Parameter 'name' is required"})
        sys.exit(1)
    # asyncio.sleep(2)  # 异步等待2秒
    result = handler(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
