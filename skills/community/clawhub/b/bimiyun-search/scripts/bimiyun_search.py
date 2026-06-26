#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
比米云搜索
快速、稳定的网页搜索API，专为AI助手优化
"""

import os
import re
import sys
import json
import urllib.request
import urllib.parse
from typing import Optional


def load_key() -> Optional[str]:
    """加载比米云搜索 API 密钥"""
    # 从环境变量加载
    key = os.environ.get("BIMIYUN_API_KEY")
    if key:
        return key.strip()

    # 从 .env 文件加载
    if os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            m = re.search(r"^\s*BIMIYUN_API_KEY\s*=\s*(.+?)\s*$", txt, re.M)
            if m:
                return m.group(1).strip().strip('"').strip("'")
        except Exception:
            pass

    return None


def load_endpoint() -> str:
    """加载比米云搜索 API 端点"""
    # 从环境变量加载
    endpoint = os.environ.get("BIMIYUN_ENDPOINT")
    if endpoint:
        return endpoint.strip()

    # 从 .env 文件加载
    if os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            m = re.search(r"^\s*BIMIYUN_ENDPOINT\s*=\s*(.+?)\s*$", txt, re.M)
            if m:
                return m.group(1).strip().strip('"').strip("'")
        except Exception:
            pass

    return "https://search.bimiyun.com/api/web"


class BimiyunSearch:
    """比米云搜索核心类"""

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None):
        self.api_key = api_key or load_key()
        self.endpoint = endpoint or load_endpoint()

    def search(
        self,
        query: str,
        max_results: int = 5,
        lang: Optional[str] = None,
        safe: bool = True,
        mode: str = "fulltext",
    ) -> dict:
        """执行搜索"""
        if not self.api_key:
            raise ValueError("BIMIYUN_API_KEY 未找到")

        if lang is None:
            lang = ""

        payload = {
            "query": query,
            "lang": lang,
            "safe": safe,
            "mode": mode,
            "max_results": max_results,
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "X-Api-Key": self.api_key,
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")

        try:
            obj = json.loads(body)
        except json.JSONDecodeError as e:
            raise ValueError(f"响应解析失败: {e}") from e

        out = {"query": query, "results": []}
        organic_results = obj.get("organic") or []
        for r in organic_results:
            out["results"].append(
                {
                    "title": r.get("title"),
                    "url": r.get("link"),
                    "content": r.get("text") or r.get("snippet"),
                }
            )

        return out


def search(
    query: str,
    max_results: int = 5,
    lang: Optional[str] = None,
    safe: bool = True,
    mode: str = "fulltext",
    api_key: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> dict:
    """Execute search against Bimiyun API (convenience function)"""
    core = BimiyunSearch(api_key, endpoint)
    return core.search(query, max_results, lang, safe, mode)


def to_markdown(obj: dict) -> str:
    """格式化结果为 Markdown"""
    lines = []
    for i, r in enumerate(obj.get("results", []) or [], 1):
        title = (r.get("title") or "").strip() or r.get("url") or "(无标题)"
        url = r.get("url") or ""
        content = (r.get("content") or "").strip()
        lines.append(f"{i}. {title}")
        if url:
            lines.append(f"   {url}")
        if content:
            lines.append(f"   - {content}")
    return "\n".join(lines).strip() + "\n"


def main():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(description="比米云搜索")
    parser.add_argument("--api-key", help="比米云搜索 API 密钥")
    parser.add_argument("--query", required=True, help="搜索查询文本")
    parser.add_argument("--max-results", type=int, default=5, help="返回结果数量 (1-10)")
    parser.add_argument("--lang", default=None, help="语言代码 (默认: 自动检测)")
    parser.add_argument("--safe", action="store_false", help="禁用安全搜索 (默认: True)")
    parser.add_argument("--mode", default="fulltext", choices=["fulltext", "snippet"], help="搜索模式: fulltext | snippet")
    parser.add_argument("--format", choices=["raw", "md"], default="md", help="输出格式: raw | md")

    args = parser.parse_args()

    searcher = BimiyunSearch(args.api_key)
    result = searcher.search(
        args.query,
        args.max_results,
        args.lang,
        args.safe,
        args.mode
    )

    if args.format == "md":
        output = to_markdown(result)
        sys.stdout.buffer.write(output.encode('utf-8'))
        return

    json_str = json.dumps(result, ensure_ascii=False, default=str)
    sys.stdout.buffer.write(json_str.encode('utf-8'))
    sys.stdout.buffer.write(b'\n')


if __name__ == "__main__":
    main()
