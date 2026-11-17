#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vision-bridge-mcp - 给不读图的文本模型(如 glm-4-flash)桥接读图能力。

作为 Claude Code 的 MCP server (stdio JSON-RPC) 运行，提供 read_image 工具。
当 glm-4-flash 在对话里遇到图片路径时，调用 read_image，本 server 把图片发给
读图后端、拿到文字描述后回填，从而让「纯文本模型」也能"看"图。

读图后端优先级（对应方案顺序）：
  方案2: 智谱 glm-4.1v-thinking-flash (OpenAI 格式, 免费, 需 ZHIPU_API_KEY)
  方案1: Kilo Omni (nvidia/nemotron-3-nano-omni, 免 key, apiKey=anonymous)
智谱失败(过载/报错/未配 key)自动回退 Kilo。

零依赖：仅用 Python 标准库。日志写 stderr（不污染 stdio JSON-RPC）。

部署：
  1. 设置环境变量 ZHIPU_API_KEY=你的智谱 key（https://open.bigmodel.cn 注册获取）
     —— 不设置也能用，只是会直接走 Kilo 兜底，没有智谱高质量读图。
  2. 在 Claude Code 的 settings.json 增加 mcpServers 条目（见 free-llm-installer SKILL.md
     「场景 F：给不读图的模型加读图桥接」），command 指向本文件。
  3. 重启 Claude Code。模型遇到图片路径会自动调 read_image 完成"看图"。
"""
import base64
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request

# --------------------------------------------------------------------------
# 配置
# --------------------------------------------------------------------------
# 智谱 key 必须从环境变量读取，切勿硬编码进仓库（会泄露）。
ZHIPU_KEY = os.environ.get("ZHIPU_API_KEY", "")
ZHIPU_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
ZHIPU_MODEL = "glm-4.1v-thinking-flash"

KILO_URL = "https://api.kilo.ai/api/gateway/v1/chat/completions"
KILO_MODEL = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
CTX = ssl.create_default_context()

PROMPT = ("请一句话简要描述这张图片的内容，包括图中文字、图表、物体、布局。"
          "直接回答，不要解释你在做什么，不要推理过程。")


def _media_type(path):
    ext = os.path.splitext(path)[1].lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
    }.get(ext, "image/png")


def _clean(text):
    """智谱 thinking 模型会把描述包在 <think>/<answer>/<|begin_of_box|> 里，提取纯文本。"""
    # 去掉 <think>...</think>
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    # 优先提取 <|begin_of_box|>...<|end_of_box|> 之间的答案
    m = re.search(r"<\|begin_of_box\|>(.*?)<\|end_of_box\|>", text, flags=re.S)
    if m:
        return m.group(1).strip()
    # 去掉标签
    text = re.sub(r"<\|begin_of_box\|>|<\|end_of_box\|>|<answer>|</answer>", "", text)
    # thinking 模型会在 <answer> 里写大量自我辩论，取最后一个短句作为有效描述
    parts = re.split(r"[。\n]", text)
    clean = [p.strip() for p in parts if p.strip() and len(p.strip()) < 200
             and not p.strip().startswith(("注", "最终", "再检查", "重新", "好了", "现在", "确认"))
             and "废话" not in p and "简洁" not in p]
    if clean:
        return clean[-1]
    return text.strip()[:300]


def _post(url, headers, payload):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), headers=headers
    )
    with urllib.request.urlopen(req, timeout=90, context=CTX) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def zhipu_describe(b64, media_type):
    """方案2: 智谱 glm-4.1v-thinking-flash，OpenAI 多模态格式，不带 tools。"""
    if not ZHIPU_KEY:
        raise RuntimeError("未设置环境变量 ZHIPU_API_KEY，跳过智谱读图")
    payload = {
        "model": ZHIPU_MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url",
                 "image_url": {"url": f"data:{media_type};base64,{b64}"}},
            ],
        }],
        "max_tokens": 800,
    }
    headers = {
        "Authorization": f"Bearer {ZHIPU_KEY}",
        "Content-Type": "application/json",
        "User-Agent": UA,
    }
    d = _post(ZHIPU_URL, headers, payload)
    return _clean(d["choices"][0]["message"]["content"])


def kilo_describe(b64, media_type):
    """方案1: Kilo Omni，免 key，OpenAI 多模态格式。"""
    payload = {
        "model": KILO_MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url",
                 "image_url": {"url": f"data:{media_type};base64,{b64}"}},
            ],
        }],
        "max_tokens": 800,
    }
    headers = {
        "Authorization": "Bearer anonymous",
        "Content-Type": "application/json",
        "User-Agent": UA,
    }
    d = _post(KILO_URL, headers, payload)
    return d["choices"][0]["message"]["content"].strip()


def describe(b64, media_type):
    """先智谱(方案2)，失败回退 Kilo(方案1)。"""
    try:
        return "[智谱 glm-4.1v] " + zhipu_describe(b64, media_type)
    except Exception as e:
        err = f"{type(e).__name__}: {str(e)[:120]}"
        try:
            return "[Kilo omni 回退] " + kilo_describe(b64, media_type)
        except Exception as e2:
            return f"[读图失败] 智谱: {err}; Kilo: {type(e2).__name__}: {str(e2)[:120]}"


# --------------------------------------------------------------------------
# MCP 协议 (stdio JSON-RPC)
# --------------------------------------------------------------------------
TOOLS = [{
    "name": "read_image",
    "description": ("读取并描述一张本地图片的内容（图中文字、图表、物体、布局）。"
                    "当对话中提到图片文件路径、或需要'看'某张图时使用。"
                    "模型本身不读图，本工具通过读图后端把图片翻译成文字描述。"),
    "inputSchema": {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "图片文件的绝对路径"}
        },
        "required": ["path"],
    },
}]


def call_tool(name, args):
    if name != "read_image":
        return {"isError": True, "content": [{"type": "text",
                "text": f"未知工具: {name}"}]}
    path = args.get("path", "")
    if not path or not os.path.isfile(path):
        return {"isError": True, "content": [{"type": "text",
                "text": f"文件不存在或路径为空: {path}"}]}
    try:
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        mt = _media_type(path)
        desc = describe(b64, mt)
        return {"isError": False, "content": [{"type": "text", "text": desc}]}
    except Exception as e:
        return {"isError": True, "content": [{"type": "text",
                "text": f"读图异常: {type(e).__name__}: {str(e)[:200]}"}]}


def handle(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "vision-bridge", "version": "1.0.0"},
        }}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = req.get("params", {})
        result = call_tool(params.get("name", ""), params.get("arguments", {}))
        return {"jsonrpc": "2.0", "id": rid, "result": result}
    # notifications/initialized 等无 id 通知：不响应
    return None


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = handle(req)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
