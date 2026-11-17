#!/usr/bin/env python3
"""
minimax_client.py - Minimal OpenAI-compatible client for MiniMax (BidHunter v2.0).

Zero third-party deps (uses urllib only). Reads config from
  ~/.config/bidhunter/ai.json  ->  {"api_key":"...","group_id":"...","model":"...","base_url":"..."}

Usage (library):
  from minimax_client import MiniMaxClient
  c = MiniMaxClient.from_config()
  text = c.chat(system="你是招投标分析助手", user="提取以下招标文件的资质门槛...", json_mode=True)

If no API key is configured, chat() raises a clear ConfigError so callers can
gracefully tell the user to run the config step.
"""
import os
import sys
import json
import urllib.request
import urllib.error

DEFAULT_BASE = "https://api.minimaxi.com/v1/chat/completions"
DEFAULT_MODEL = "MiniMax-M2.7"
CFG_PATH = os.path.expanduser("~/.config/bidhunter/ai.json")


class ConfigError(Exception):
    pass


class MiniMaxClient:
    def __init__(self, api_key, group_id=None, model=DEFAULT_MODEL, base_url=DEFAULT_BASE):
        self.api_key = api_key
        self.group_id = group_id
        self.model = model
        self.base_url = base_url

    @classmethod
    def from_config(cls, path=CFG_PATH):
        if not os.path.exists(path):
            raise ConfigError(
                f"未找到 AI 配置: {path}\n请创建该文件：{{\"api_key\":\"你的MiniMaxKey\",\"group_id\":\"可选\"}}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception as e:
            raise ConfigError(f"AI 配置文件无法解析: {e}")
        key = cfg.get("api_key")
        if not key:
            raise ConfigError("AI 配置缺少 api_key")
        return cls(
            api_key=key,
            group_id=cfg.get("group_id"),
            model=cfg.get("model", DEFAULT_MODEL),
            base_url=cfg.get("base_url", DEFAULT_BASE),
        )

    def chat(self, user, system="你是一个严谨的招投标分析助手。", json_mode=False, temperature=0.2):
        if not self.api_key:
            raise ConfigError("api_key 为空")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "BidHunter/2.0",
        }
        if self.group_id:
            payload["group_id"] = self.group_id
        req = urllib.request.Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            raise ConfigError(f"MiniMax API HTTP {e.code}: {body[:300]}")
        except urllib.error.URLError as e:
            raise ConfigError(f"无法连接 MiniMax API: {e}")
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise ConfigError(f"MiniMax 返回格式异常: {str(data)[:300]}")


if __name__ == "__main__":
    try:
        c = MiniMaxClient.from_config()
    except ConfigError as e:
        print(f"配置错误: {e}", file=sys.stderr)
        sys.exit(2)
    out = c.chat(sys.stdin.read() if not sys.argv[1:] else sys.argv[1])
    print(out)
