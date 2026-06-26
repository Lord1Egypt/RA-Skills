#!/usr/bin/env python3
"""
DeepResearch Agent API 调用脚本（单阶段自动模式）

自动完成全流程：创建会话 → 发起查询 → 跳过澄清 → 获取大纲 → 自动确认 → 生成报告

用法:
    python deepresearch.py run \
        --query "研究小米汽车发展历程" \
        --api-key "bce-v3/ALTAK-..." \
        --version lite

    或使用 agent_id（与 version 都可选，同时提供时以 agent_id 为准，都不提供默认 version=lite）:
    python deepresearch.py run \
        --query "研究小米汽车发展历程" \
        --api-key "bce-v3/ALTAK-..." \
        --agent-id "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

    → stdout 输出 JSON:
    {
      "conversation_id": "...",
      "outline": {"title": "...", "sub_chapters": [...]},
      "outline_preview": "标题：...\n章节结构：\n  1. ...",
      "files": {
        "md": {"filename": "report_xxx.md", "download_url": "https://..."},
        "html": {"filename": "report_xxx.html", "download_url": "https://..."}
      }
    }

参数可通过环境变量提供:
    export QIANFAN_API_KEY="bce-v3/ALTAK-..."
"""

import argparse
import json
import os
import sys
import time

# 禁用输出缓冲，确保 print 立即显示（等同于 python -u 或 PYTHONUNBUFFERED=1）
sys.stdout.reconfigure(line_buffering=True)

try:
    import requests
except ImportError:
    print("缺少依赖: pip install requests", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://qianfan.baidubce.com/v2"
IDLE_TIMEOUT = 3600  # 60 分钟空闲超时
VALID_VERSIONS = ("lite", "standard", "pro")


# ── 参数解析 ──────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(description="DeepResearch Agent API 调用工具（单阶段自动模式）")
    subparsers = parser.add_subparsers(dest="phase", help="执行阶段")
    subparsers.required = True

    # ── 单阶段: run ──
    p_run = subparsers.add_parser("run", help="一键执行完整流程：查询 → 大纲 → 自动确认 → 报告")
    p_run.add_argument("--query", required=True, help="研究问题")
    p_run.add_argument("--api-key", default=os.environ.get("QIANFAN_API_KEY"),
                       help="千帆 API Key（或设置环境变量 QIANFAN_API_KEY）")
    p_run.add_argument("--agent-id", default=os.environ.get("QIANFAN_AGENT_ID"),
                       help="深度研究 Agent ID（可选，提供时优先于 --version）")
    p_run.add_argument("--version", default=None, choices=VALID_VERSIONS,
                       help="版本选择：lite（轻量版，默认）、standard（标准版）、pro（高级版）。都不提供时默认 lite")
    p_run.add_argument("--clarification-wait", type=int, default=10,
                       help="发送跳过澄清前的等待秒数（默认 10s）")

    return parser.parse_args()


def check_api_key(args):
    if not args.api_key:
        print("缺少必要参数：--api-key / QIANFAN_API_KEY", file=sys.stderr)
        sys.exit(1)


# ── HTTP 工具 ─────────────────────────────────────────────

def make_headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept-Encoding": "identity",  # 禁用 gzip，确保 SSE 正常接收
    }


def build_id_params(agent_id=None, version=None):
    """构建 agent_id 或 version 参数。agent_id 优先，都未提供时默认 version=lite"""
    if agent_id:
        return {"agent_id": agent_id}
    return {"version": version or "lite"}


# ── Step 1: 创建会话 ──────────────────────────────────────

def create_conversation(api_key, agent_id=None, version=None):
    print("[Step 1] 创建会话...", file=sys.stderr)
    body = build_id_params(agent_id, version)
    resp = requests.post(
        f"{BASE_URL}/agent/deepresearch/create",
        headers=make_headers(api_key),
        json=body,
        timeout=30,
    )
    resp.raise_for_status()
    conversation_id = resp.json()["result"]["conversation_id"]
    print(f"         conversation_id: {conversation_id}", file=sys.stderr)
    return conversation_id


# ── SSE 流读取 ────────────────────────────────────────────

def stream_sse(api_key, payload, label="", early_stop=None):
    """
    发送 POST /run 并读取 SSE 流，返回所有事件列表。
    early_stop: callable(event) -> bool，返回 True 时提前退出
    """
    events = []
    last_data_time = time.time()

    with requests.post(
        f"{BASE_URL}/agent/deepresearch/run",
        headers=make_headers(api_key),
        json=payload,
        stream=True,
        timeout=None,  # 不设整体超时，通过 IDLE_TIMEOUT 控制
    ) as resp:
        resp.raise_for_status()

        pending_data: list = []
        buf = b""

        def _process_event(raw_json: str) -> bool:
            """解析并处理一个完整 SSE 事件，返回 True 表示需要退出循环"""
            nonlocal events
            if raw_json == "[DONE]":
                return True
            try:
                event = json.loads(raw_json)
            except json.JSONDecodeError:
                return False
            events.append(event)
            _print_event_progress(event, label)
            if event.get("status") == "interrupt":
                return True
            for content in event.get("content", []):
                ev_info = content.get("event") or {}
                if ev_info.get("is_end") and ev_info.get("is_stop"):
                    return True
            if early_stop and early_stop(event):
                return True
            return False

        done = False
        for chunk in resp.iter_content(chunk_size=4096):
            if not chunk:
                continue
            last_data_time = time.time()
            buf += chunk

            while b"\n" in buf:
                if time.time() - last_data_time > IDLE_TIMEOUT:
                    raise TimeoutError(f"SSE 空闲超时（{IDLE_TIMEOUT}s 无数据）")

                line_bytes, buf = buf.split(b"\n", 1)
                line = line_bytes.rstrip(b"\r").decode("utf-8", errors="replace")

                if not line:
                    if pending_data:
                        raw = "".join(pending_data)
                        pending_data.clear()
                        if _process_event(raw):
                            done = True
                            break
                    continue

                if line.startswith("data: "):
                    pending_data.append(line[6:])
                elif line.startswith("data:"):
                    pending_data.append(line[5:])

            if done:
                break

        if not done and pending_data:
            raw = "".join(pending_data)
            _process_event(raw)

    return events


def _print_event_progress(event, label):
    """打印所有收到的 SSE 事件（输出到 stderr，不干扰 stdout 的 JSON 输出）"""
    prefix = f"[{label}] " if label else ""
    role = event.get("role", "")
    status = event.get("status", "")
    contents = event.get("content", [])
    if not contents:
        print(f"  {prefix}[SSE] role={role} status={status} | (no content)", file=sys.stderr, flush=True)
        return
    for content in contents:
        ev_info = content.get("event") or {}
        ename = ev_info.get("name", "")
        estatus = ev_info.get("status", "")
        ctype = content.get("type", "")
        text = content.get("text")
        if isinstance(text, dict):
            text_str = json.dumps(text, ensure_ascii=False)
        elif isinstance(text, str):
            text_str = text
        else:
            text_str = str(text)
        if len(text_str) > 200:
            text_str = text_str[:200] + "..."
        print(f"  {prefix}[SSE] role={role} status={status} | type={ctype} event.name={ename!r} event.status={estatus!r} | text={text_str}", file=sys.stderr, flush=True)


# ── 事件解析工具 ──────────────────────────────────────────

def has_clarification(events):
    """判断是否出现了需求澄清事件"""
    for event in events:
        if event.get("role") == "assistant":
            for content in event.get("content", []):
                ev_info = content.get("event") or {}
                if ev_info.get("name") == "/chat/chat_agent":
                    return True
    return False


def extract_interrupt_id(events):
    """从事件流中提取 interrupt_id（text.data 是嵌套 JSON 字符串，需二次解析）"""
    for event in events:
        if event.get("status") == "interrupt":
            for content in event.get("content", []):
                if content.get("type") == "json":
                    ev_info = content.get("event") or {}
                    if ev_info.get("name") == "/toolcall/interrupt":
                        text = content.get("text") or {}
                        data_str = text.get("data", "")
                        if data_str:
                            try:
                                inner = json.loads(data_str)
                                if inner.get("interrupt_id"):
                                    return inner["interrupt_id"]
                            except json.JSONDecodeError:
                                pass
    return None


def extract_structured_outline(events):
    """从事件流中提取 structured_outline（text.data 是嵌套 JSON 字符串，需二次解析）。

    服务端推送顺序：
      1. status=preparing，event.name=/toolcall/structured_outline（title 为空，占位）
      2. status=done，    event.name=/toolcall/structured_outline（title 非空，完整大纲）
      3. status=interrupt，event.name=/toolcall/interrupt（等待用户确认）

    脚本收到 interrupt 时 break，因此 done 事件必须在 interrupt 之前到达才能被收集到。
    正常情况下 done 先于 interrupt，所以这里只需找 title 非空的事件即可。
    """
    for event in events:
        for content in event.get("content", []):
            if content.get("type") != "json":
                continue
            ev_info = content.get("event") or {}
            if ev_info.get("name") != "/toolcall/structured_outline":
                continue
            text = content.get("text") or {}
            data_str = text.get("data", "")
            if not data_str:
                continue
            try:
                outline = json.loads(data_str)
            except json.JSONDecodeError:
                continue
            if outline.get("title"):
                return outline
    return None


def extract_files(events):
    """从事件流中提取生成的文件信息"""
    files = {}
    for event in events:
        for content in event.get("content", []):
            if content.get("type") == "files":
                text = content.get("text") or {}
                filename = text.get("filename", "")
                if filename.endswith(".md") and "md" not in files:
                    files["md"] = text
                elif filename.endswith(".html") and "html" not in files:
                    files["html"] = text
    return files


def format_outline_preview(outline):
    """格式化大纲为可读预览文本"""
    lines = []
    lines.append(f"标题：{outline.get('title', '')}")
    lines.append(f"描述：{outline.get('description', '')}")
    lines.append("")
    lines.append("章节结构：")
    for i, ch in enumerate(outline.get("sub_chapters", []), 1):
        lines.append(f"  {i}. {ch.get('title', '')}")
        for sub in ch.get("sub_chapters", []):
            lines.append(f"     - {sub.get('title', '')}")
    return "\n".join(lines)


# ── 单阶段自动执行: 查询 → 大纲 → 自动确认 → 报告 ──────────

def run_full(args):
    """一键执行完整流程，输出最终结果 JSON 到 stdout"""
    check_api_key(args)
    id_params = build_id_params(args.agent_id, args.version)

    # Step 1: 创建会话
    conversation_id = create_conversation(args.api_key, args.agent_id, args.version)

    # Step 2: 发起初始查询
    print(f"\n[Step 2] 发起研究: {args.query}", file=sys.stderr)
    init_payload = {
        "query": args.query,
        **id_params,
        "conversation_id": conversation_id,
    }
    events = stream_sse(args.api_key, init_payload, label="初始查询")

    # Step 3: 自动跳过需求澄清（如有）
    if has_clarification(events):
        print(f"\n[Step 3] 检测到需求澄清，{args.clarification_wait}s 后自动跳过...", file=sys.stderr)
        time.sleep(args.clarification_wait)
        skip_payload = {
            "query": "跳过",
            **id_params,
            "conversation_id": conversation_id,
        }
        events = stream_sse(args.api_key, skip_payload, label="跳过澄清")
    else:
        print("\n[Step 3] 无需澄清，直接进入大纲提取", file=sys.stderr)

    # Step 4: 提取大纲数据
    print("\n[Step 4] 提取大纲数据...", file=sys.stderr)
    interrupt_id = extract_interrupt_id(events)
    outline = extract_structured_outline(events)

    if not interrupt_id:
        print("错误: 未找到 interrupt_id", file=sys.stderr)
        sys.exit(1)
    if not outline:
        print("错误: 未找到完整的 structured_outline（title 为空）", file=sys.stderr)
        for ev in events:
            for c in ev.get("content", []):
                evt = c.get("event") or {}
                if evt.get("name") == "/toolcall/structured_outline":
                    text = c.get("text") or {}
                    print(f"  event.status={evt.get('status')!r}  text.data={text.get('data', '')[:100]!r}", file=sys.stderr)
        sys.exit(1)

    print(f"         大纲标题: {outline.get('title')}", file=sys.stderr)
    print(f"         章节数量: {len(outline.get('sub_chapters', []))}", file=sys.stderr)
    print(f"         interrupt_id: {interrupt_id}", file=sys.stderr)

    # Step 5: 自动确认大纲，生成报告
    print("\n[Step 5] 自动确认大纲，开始生成报告...", file=sys.stderr)

    def is_html_file(event):
        for content in event.get("content", []):
            if content.get("type") == "files":
                filename = (content.get("text") or {}).get("filename", "")
                if filename.endswith(".html"):
                    return True
        return False

    confirm_payload = {
        "query": "确认",
        **id_params,
        "conversation_id": conversation_id,
        "interrupt_id": interrupt_id,
        "structured_outline": outline,
    }
    report_events = stream_sse(args.api_key, confirm_payload, label="生成报告", early_stop=is_html_file)

    # 提取文件下载链接
    files = extract_files(report_events)

    # 输出结构化 JSON 到 stdout（供 Agent 解析）
    result = {
        "conversation_id": conversation_id,
        "outline": outline,
        "outline_preview": format_outline_preview(outline),
        "files": files,
    }
    print(json.dumps(result, ensure_ascii=False))

    # 在 stderr 打印可读信息
    if files:
        if "md" in files:
            print(f"\nMarkdown 报告:", file=sys.stderr)
            print(f"  文件名: {files['md'].get('filename')}", file=sys.stderr)
            print(f"  下载:   {files['md'].get('download_url')}", file=sys.stderr)
        if "html" in files:
            print(f"\nHTML 报告:", file=sys.stderr)
            print(f"  文件名: {files['html'].get('filename')}", file=sys.stderr)
            print(f"  下载:   {files['html'].get('download_url')}", file=sys.stderr)
    else:
        print("\n未获取到报告文件（任务可能仍在后台运行）", file=sys.stderr)

    return result


# ── 入口 ──────────────────────────────────────────────────

def main():
    args = parse_args()

    start = time.time()
    try:
        if args.phase == "run":
            run_full(args)
    except KeyboardInterrupt:
        print("\n\n用户中断", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        sys.exit(1)

    elapsed = time.time() - start
    print(f"\n流程完成，耗时: {elapsed:.1f}s", file=sys.stderr)


if __name__ == "__main__":
    main()
