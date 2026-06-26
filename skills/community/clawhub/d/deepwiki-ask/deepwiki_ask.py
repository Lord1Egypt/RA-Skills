#!/usr/bin/env python3
"""
DeepWiki Ask - 提问查询仓库。通过 DeepWiki MCP 查询仓库信息。

Usage:
    python deepwiki_ask.py -r owner/repo -q "question"
    python deepwiki_ask.py -r owner/repo -q -          # 从 stdin 读问题 (UTF-8)
    python deepwiki_ask.py -r owner/repo -q @file.txt  # 从文件读问题 (UTF-8)
"""

import sys
import json
import argparse
import os
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, Dict, Any

if sys.platform == 'win32':
    try:
        os.system('chcp 65001 >nul 2>&1')
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"

DEFAULT_CONFIG = {
    "request_timeout_seconds": 120,
    "request_max_retries": 3,
}

CONFIG_VALIDATION = {
    "request_timeout_seconds": {"min": 10, "max": 600},
    "request_max_retries": {"min": 0, "max": 10},
}


def _print_json(data):
    """UTF-8 安全 JSON 输出。"""
    text = json.dumps(data, ensure_ascii=False, indent=2)
    try:
        sys.stdout.buffer.write(text.encode("utf-8"))
        sys.stdout.buffer.write(b"\n")
        sys.stdout.buffer.flush()
    except (AttributeError, OSError):
        print(text)


def load_config() -> dict:
    config = DEFAULT_CONFIG.copy()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
            for k in DEFAULT_CONFIG:
                if k in loaded and isinstance(loaded[k], (int, float)):
                    lim = CONFIG_VALIDATION.get(k, {})
                    if lim and (loaded[k] < lim["min"] or loaded[k] > lim["max"]):
                        continue
                    config[k] = loaded[k]
        except (json.JSONDecodeError, OSError):
            pass
    return config


def save_default_config():
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)


class DeepWikiMCPClient:
    """
    DeepWiki MCP 客户端
    使用 MCP 协议与 DeepWiki 服务器通信

    MCP 协议流程:
    1. initialize - 初始化连接
    2. notifications/initialized - 通知已初始化
    3. tools/call - 调用工具
    """

    def __init__(self, timeout: int = 120, max_retries: int = 3):
        self.base_url = "https://mcp.deepwiki.com/mcp"
        self.request_id = 0
        self.initialized = False
        self.timeout = timeout
        self.max_retries = max_retries

    def _make_request(self, method: str, params: dict = None) -> dict:
        """发送 MCP JSON-RPC 请求"""
        self.request_id += 1

        payload = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }

        data = json.dumps(payload).encode('utf-8')
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/event-stream',
            'User-Agent': 'DeepWiki-Ask/1.0',
        }

        req = urllib.request.Request(
            self.base_url,
            data=data,
            headers=headers,
            method='POST'
        )

        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    content_type = response.headers.get('Content-Type', '')
                    raw_data = response.read().decode('utf-8')

                    if 'text/event-stream' in content_type:
                        return self._parse_sse_response(raw_data)
                    else:
                        return json.loads(raw_data)

            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8') if e.fp else ''
                last_error = f"HTTP {e.code}: {e.reason}"
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
            except urllib.error.URLError as e:
                last_error = str(e)
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)
            except json.JSONDecodeError as e:
                last_error = f"JSON 解析错误: {e}"
                break
            except Exception as e:
                last_error = str(e)
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)

        return {"error": f"Request failed after {self.max_retries + 1} attempts: {last_error}"}

    def _parse_sse_response(self, data: str) -> dict:
        """解析 SSE 格式的响应"""
        result = {}
        for line in data.split('\n'):
            if line.startswith('data:'):
                try:
                    result = json.loads(line[5:].strip())
                except json.JSONDecodeError:
                    pass
        return result

    def initialize(self) -> dict:
        """
        初始化 MCP 连接
        必须在调用其他方法之前执行
        """
        result = self._make_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "roots": {"listChanged": True},
                "sampling": {}
            },
            "clientInfo": {
                "name": "deepwiki-ask",
                "version": "1.0.0"
            }
        })

        if "result" in result:
            self.initialized = True
            self._send_initialized_notification()

        return result

    def _send_initialized_notification(self):
        """发送初始化完成通知"""
        self._make_request("notifications/initialized", {})

    def list_tools(self) -> dict:
        """获取可用的工具列表"""
        if not self.initialized:
            self.initialize()
        return self._make_request("tools/list")

    def read_wiki_structure(self, repo: str) -> dict:
        """
        获取仓库文档结构

        参数:
            repo: 仓库名称 (格式: owner/repo)
        """
        if not self.initialized:
            self.initialize()

        return self._make_request("tools/call", {
            "name": "read_wiki_structure",
            "arguments": {
                "repoName": repo
            }
        })

    def read_wiki_contents(self, repo: str, topic: str = None) -> dict:
        """
        获取文档内容

        参数:
            repo: 仓库名称 (格式: owner/repo)
            topic: 可选的主题
        """
        if not self.initialized:
            self.initialize()

        arguments = {"repoName": repo}
        if topic:
            arguments["topic"] = topic

        return self._make_request("tools/call", {
            "name": "read_wiki_contents",
            "arguments": arguments
        })

    def ask_question(self, repo: str, question: str) -> dict:
        """
        向 AI 提问关于仓库的问题

        参数:
            repo: 仓库名称 (格式: owner/repo)
            question: 要问的问题
        """
        if not self.initialized:
            self.initialize()

        return self._make_request("tools/call", {
            "name": "ask_question",
            "arguments": {
                "repoName": repo,
                "question": question
            }
        })


def extract_text(result: Any) -> str:
    if isinstance(result, dict):
        content = result.get("content", [])
        if content and isinstance(content, list):
            texts = [item.get("text", "") for item in content
                     if isinstance(item, dict) and item.get("type") == "text"]
            return "\n".join(texts)
        if "result" in result.get("structuredContent", {}):
            return result["structuredContent"]["result"]
    return str(result)


def ask(repo: str, question: str, config: dict) -> str:
    if "/" not in repo:
        raise ValueError(f"Invalid repo format: {repo}. Expected: owner/repo")

    timeout = config.get("request_timeout_seconds", 120)
    max_retries = config.get("request_max_retries", 3)

    client = DeepWikiMCPClient(timeout=timeout, max_retries=max_retries)

    init_result = client.initialize()
    if "error" in init_result:
        raise Exception(f"MCP 初始化失败: {init_result['error']}")

    data = client.ask_question(repo, question)

    if "error" in data:
        raise Exception(data["error"])

    raw_result = data.get("result", {})
    if config.get("_debug"):
        print("DEBUG raw MCP result:", json.dumps(raw_result, ensure_ascii=False, indent=2), file=sys.stderr)

    answer = extract_text(raw_result)
    if not answer or answer.strip() == "{}":
        answer = (
            "【请求已成功到达 DeepWiki】MCP 返回空结果。可能：该问题在知识库无匹配，或仓库未在 MCP 侧索引。"
            "可尝试更泛化的问题，或访问 https://deepwiki.com/{} 浏览文档。"
        ).format(repo)
    return answer


def get_structure(repo: str, config: dict) -> str:
    if "/" not in repo:
        raise ValueError(f"Invalid repo format: {repo}. Expected: owner/repo")

    timeout = config.get("request_timeout_seconds", 120)
    max_retries = config.get("request_max_retries", 3)

    client = DeepWikiMCPClient(timeout=timeout, max_retries=max_retries)

    init_result = client.initialize()
    if "error" in init_result:
        raise Exception(f"MCP 初始化失败: {init_result['error']}")

    data = client.read_wiki_structure(repo)

    if "error" in data:
        raise Exception(data["error"])

    raw_result = data.get("result", {})
    return extract_text(raw_result)


def get_contents(repo: str, topic: str, config: dict) -> str:
    if "/" not in repo:
        raise ValueError(f"Invalid repo format: {repo}. Expected: owner/repo")

    timeout = config.get("request_timeout_seconds", 120)
    max_retries = config.get("request_max_retries", 3)

    client = DeepWikiMCPClient(timeout=timeout, max_retries=max_retries)

    init_result = client.initialize()
    if "error" in init_result:
        raise Exception(f"MCP 初始化失败: {init_result['error']}")

    data = client.read_wiki_contents(repo, topic)

    if "error" in data:
        raise Exception(data["error"])

    raw_result = data.get("result", {})
    return extract_text(raw_result)


def main():
    parser = argparse.ArgumentParser(description="DeepWiki 提问查询仓库")
    parser.add_argument("-r", "--repo", help="仓库 owner/repo")
    parser.add_argument("-q", "--question", help="问题；'-' 从 stdin，'@path' 从文件 (UTF-8)")
    parser.add_argument("--structure", action="store_true", help="获取文档结构")
    parser.add_argument("--contents", action="store_true", help="获取文档内容")
    parser.add_argument("--topic", help="指定文档主题 (配合 --contents 使用)")
    parser.add_argument("--json", action="store_true", help="输出 JSON 供 Agent 解析")
    parser.add_argument("--debug", action="store_true", help="将 MCP 原始 result 输出到 stderr")
    args = parser.parse_args()

    save_default_config()
    config = load_config()
    if getattr(args, "debug", False):
        config["_debug"] = True

    if not args.repo:
        out = {"status": "error", "message": "请提供 -r owner/repo"}
        _print_json(out) if args.json else print("Error:", out["message"])
        sys.exit(1)

    question = None
    if args.question:
        question = args.question
        if question == "-":
            question = sys.stdin.read().strip()
            if not question:
                out = {"status": "error", "message": "标准输入为空"}
                _print_json(out) if args.json else print("Error:", out["message"])
                sys.exit(1)
        elif question.startswith("@"):
            path = Path(question[1:].strip())
            if not path.exists():
                out = {"status": "error", "message": f"文件不存在: {path}"}
                _print_json(out) if args.json else print("Error:", out["message"])
                sys.exit(1)
            with open(path, "r", encoding="utf-8") as f:
                question = f.read().strip()
            if not question:
                out = {"status": "error", "message": "问题文件为空"}
                _print_json(out) if args.json else print("Error:", out["message"])
                sys.exit(1)

    if not args.json:
        print("=" * 60)
        print("DeepWiki 仓库问答")
        print("=" * 60)
        print(f"Repo: {args.repo}")

    try:
        if args.structure:
            if not args.json:
                print("Mode: 获取文档结构")
                print("=" * 60)
                print("Structure:")
                print("-" * 60)
            result = get_structure(args.repo, config)
        elif args.contents:
            if not args.json:
                print(f"Mode: 获取文档内容 (topic: {args.topic or '全部'})")
                print("=" * 60)
                print("Contents:")
                print("-" * 60)
            result = get_contents(args.repo, args.topic, config)
        elif question:
            if not args.json:
                print(f"Question: {question}")
                print("=" * 60)
                print("Answer:")
                print("-" * 60)
            result = ask(args.repo, question, config)
        else:
            out = {"status": "error", "message": "请提供 -q 问题，或使用 --structure/--contents"}
            _print_json(out) if args.json else print("Error:", out["message"])
            sys.exit(1)

        if args.json:
            _print_json({
                "status": "success",
                "repo": args.repo,
                "mode": "structure" if args.structure else ("contents" if args.contents else "question"),
                "question": question,
                "result": result
            })
        else:
            print(result)
            print("-" * 60)

    except (ValueError, Exception) as e:
        if args.json:
            _print_json({"status": "error", "repo": args.repo, "message": str(e)})
        else:
            print("Error:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
