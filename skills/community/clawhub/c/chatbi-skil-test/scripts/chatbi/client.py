"""Streaming API client for ChatBI Agent.

Author: ChatBI Skills
Created: 2026-04-01
"""

from __future__ import annotations

import json
import sys
from typing import Iterator, Dict, Any, Optional

import requests

from chatbi.config import ChatBIConfig


class ChatBIClient:
    """ChatBI Agent 流式客户端.

    负责调用 ChatBI 流式接口，逐行解析 SSE 事件并以 dict 形式 yield。
    """

    def __init__(self, config: ChatBIConfig):
        self._config = config

    def stream_query(self, question: str) -> Iterator[Dict[str, Any]]:
        """发送问数请求并流式返回解析后的事件.

        API 返回 NDJSON 格式（每行一个 JSON 对象），而非标准 SSE。
        同时兼容 `data:` 前缀的 SSE 格式。

        使用 iter_content + 手动 buffer 拼行，避免 iter_lines 在长时间
        等待（如 SQL 执行 ~20s）时出现 InvalidChunkLength 断连问题。

        Args:
            question: 用户的自然语言查询。

        Yields:
            解析后的 JSON 字典，每个代表一个流式事件。
        """
        payload = self._config.build_payload(question, stream=True)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }

        try:
            with requests.post(
                self._config.api_url,
                headers=headers,
                json=payload,
                stream=True,
                timeout=(self._config.connect_timeout, self._config.read_timeout),
            ) as resp:
                resp.raise_for_status()

                buf = ""
                for chunk in resp.iter_content(chunk_size=8192, decode_unicode=True):
                    if not chunk:
                        continue

                    buf += chunk

                    # 逐行处理 buffer 中的完整行
                    while "\n" in buf:
                        line, buf = buf.split("\n", 1)
                        line = line.strip()
                        if not line:
                            continue

                        # 兼容标准 SSE data: 前缀格式
                        if line.startswith("data:"):
                            line = line[len("data:"):].strip()

                        if line == "[DONE]":
                            return

                        try:
                            obj = json.loads(line)
                            yield obj
                        except json.JSONDecodeError:
                            continue

                # 处理 buffer 中最后一行（无换行符结尾）
                if buf.strip():
                    line = buf.strip()
                    if line.startswith("data:"):
                        line = line[len("data:"):].strip()
                    if line and line != "[DONE]":
                        try:
                            obj = json.loads(line)
                            yield obj
                        except json.JSONDecodeError:
                            pass

        except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError) as e:
            # 长时间 SQL 执行可能导致 chunked transfer 断连
            # 此时已有的事件已经 yield 出去了，打印警告而非抛异常
            print(f"流式连接中断（已有数据已输出）: {e}", file=sys.stderr)
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}", file=sys.stderr)
            raise

    def query(self, question: str) -> Dict[str, Any]:
        """发送非流式问数请求.

        Args:
            question: 用户的自然语言查询。

        Returns:
            完整的 API 响应。
        """
        payload = self._config.build_payload(question, stream=False)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            resp = requests.post(
                self._config.api_url,
                headers=headers,
                json=payload,
                timeout=(self._config.connect_timeout, self._config.read_timeout),
            )
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}", file=sys.stderr)
            raise

    @property
    def config(self) -> ChatBIConfig:
        return self._config
