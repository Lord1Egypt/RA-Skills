#!/usr/bin/env python3
"""通用大文档上传到乐享知识库脚本。

解决核心问题：
- MCP connector 工具参数有大小限制（~30K字符），无法直接传入大文档内容
- 分块追加方式会触发限频、顺序错乱、重试消耗 token
- 本脚本通过 HTTP 直接调用 MCP API 上传，无大小限制

支持两种模式：
1. 有 LEXIANG_TOKEN：直接调用 entry_import_content 创建在线文档（最佳体验）
2. 无 LEXIANG_TOKEN：通过预签名 URL 上传 .md 文件（降级方案，内容完整）

用法：
  # 模式1：有 token，创建在线文档（page类型，可直接阅读）
  LEXIANG_TOKEN=xxx COMPANY_FROM=yyy python3 upload_doc_to_lexiang.py \\
      doc.md --parent-id <目录ID> --name "文档标题" --space-id <SPACE_ID>

  # 模式2：无 token，通过 Agent MCP connector 上传（由 Agent 调用）
  python3 upload_doc_to_lexiang.py doc.md --mode presigned-url \\
      --upload-url "<从file_apply_upload获取的url>" \\
      --session-id "<session_id>"

  # 模式3：仅输出上传指令（供 Agent 解析执行）
  python3 upload_doc_to_lexiang.py doc.md --mode instructions \\
      --parent-id <目录ID> --name "文档标题"

适用场景：
- 播客转录文字稿（40K-150K字符）
- 长文章抓取转存（20K-100K字符）
- PDF 提取后的大段文字
- 任何超过 30K 字符的 Markdown 文档
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path


def call_mcp_tool(base_url: str, company_from: str, token: str, tool_name: str, arguments: dict) -> dict:
    """直接通过 HTTP 调用乐享 MCP API（绕过 Agent 工具参数限制）。"""
    import requests
    
    url = f"{base_url}/mcp?company_from={company_from}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    }
    
    resp = requests.post(url, headers=headers, json=payload, timeout=180)
    
    if resp.status_code == 401:
        print("❌ LEXIANG_TOKEN 已过期或无效（HTTP 401）")
        print("   请重新获取: https://lexiangla.com/mcp")
        return {"error": "token_expired", "code": 401}
    
    if resp.status_code != 200:
        return {"error": f"http_{resp.status_code}", "body": resp.text[:500]}
    
    # 解析 SSE/JSON 响应
    for line in resp.text.strip().split("\n"):
        line = line.strip()
        if line.startswith("data:"):
            line = line[5:].strip()
        if not line or line == "[DONE]":
            continue
        try:
            data = json.loads(line)
            if "result" in data:
                for c in data["result"].get("content", []):
                    if c.get("type") == "text":
                        return json.loads(c["text"])
            return data
        except (json.JSONDecodeError, KeyError):
            continue
    
    return {"error": "no_response"}


def upload_as_online_doc(
    md_path: Path,
    parent_id: str,
    name: str,
    space_id: str,
    token: str,
    company_from: str,
    base_url: str,
) -> dict:
    """模式1：通过 MCP API 直接创建在线文档（page类型）。
    
    核心优势：
    - HTTP POST body 无大小限制，60K/100K/200K 字符都能一次传入
    - 创建的是在线文档（page），用户可直接阅读、编辑、评论
    - 支持完整 Markdown 格式渲染
    """
    print(f"📤 上传模式: 在线文档 (entry_import_content)")
    print(f"   文件: {md_path.name} ({md_path.stat().st_size / 1024:.1f} KB)")
    
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    print(f"   内容: {len(content)} 字符")
    
    # 直接调用 entry_import_content
    result = call_mcp_tool(base_url, company_from, token, "entry_import_content", {
        "name": name,
        "content": content,
        "content_type": "markdown",
        "parent_id": parent_id,
        "space_id": space_id,
    })
    
    if "error" in result:
        print(f"❌ 在线文档创建失败: {result}")
        return result
    
    entry_id = result.get("data", {}).get("entry", {}).get("id", "")
    if entry_id:
        print(f"✅ 在线文档创建成功!")
        print(f"   entry_id: {entry_id}")
        print(f"   链接: https://lexiangla.com/pages/{entry_id}?company_from={company_from}")
    
    return result


def upload_as_file(
    md_path: Path,
    parent_id: str,
    token: str,
    company_from: str,
    base_url: str,
) -> dict:
    """模式1降级：通过预签名 URL 上传 .md 文件。
    
    当 entry_import_content 失败时的降级方案。
    产生 entry_type=file，排版略差但内容完整。
    """
    import requests
    
    print(f"📤 降级模式: 文件上传 (pre-signed URL)")
    
    file_size = md_path.stat().st_size
    
    # Step 1: 申请上传
    result = call_mcp_tool(base_url, company_from, token, "file_apply_upload", {
        "parent_entry_id": parent_id,
        "name": md_path.name,
        "size": str(file_size),
        "mime_type": "text/markdown",
        "upload_type": "PRE_SIGNED_URL",
    })
    
    session = result.get("data", {}).get("session", {})
    session_id = session.get("session_id", "")
    objects = session.get("objects", [])
    upload_url = objects[0].get("upload_url", "") if objects else ""
    
    if not upload_url:
        print(f"❌ 获取上传URL失败: {result}")
        return {"error": "no_upload_url"}
    
    # Step 2: PUT 上传
    print(f"   PUT {file_size} bytes...")
    with open(md_path, "rb") as f:
        resp = requests.put(upload_url, data=f, headers={
            "Content-Type": "text/markdown",
            "Content-Length": str(file_size),
        }, timeout=60)
    
    if resp.status_code != 200:
        print(f"❌ 文件上传失败: HTTP {resp.status_code}")
        return {"error": f"upload_http_{resp.status_code}"}
    
    # Step 3: 确认
    commit_result = call_mcp_tool(base_url, company_from, token, "file_commit_upload", {
        "session_id": session_id,
    })
    
    entry_id = commit_result.get("data", {}).get("entry", {}).get("id", "")
    if entry_id:
        print(f"✅ 文件上传成功!")
        print(f"   entry_id: {entry_id}")
        print(f"   链接: https://lexiangla.com/pages/{entry_id}?company_from={company_from}")
    
    return commit_result


def output_agent_instructions(md_path: Path, parent_id: str, name: str) -> dict:
    """模式3：输出供 Agent 执行的 MCP 操作指令。
    
    当没有 LEXIANG_TOKEN 时，输出 Agent 需要执行的具体步骤。
    Agent 读取这些指令后按序执行即可。
    """
    file_size = md_path.stat().st_size
    
    instructions = {
        "mode": "agent_instructions",
        "description": "Agent 请按以下步骤通过 MCP connector 上传大文档",
        "file_path": str(md_path),
        "file_size": file_size,
        "file_name": name + ".md" if not name.endswith(".md") else name,
        "parent_id": parent_id,
        "steps": [
            {
                "step": 1,
                "tool": "file_apply_upload",
                "params": {
                    "parent_entry_id": parent_id,
                    "name": name + ".md" if not name.endswith(".md") else name,
                    "size": str(file_size),
                    "mime_type": "text/markdown",
                    "upload_type": "PRE_SIGNED_URL",
                },
                "extract": "session_id, upload_url from response.data.session"
            },
            {
                "step": 2,
                "tool": "bash_curl",
                "command_template": f'curl -X PUT "{{upload_url}}" -H "Content-Type: text/markdown" -H "Content-Length: {file_size}" --data-binary @{md_path}',
                "expect": "HTTP 200"
            },
            {
                "step": 3,
                "tool": "file_commit_upload",
                "params_template": {"session_id": "{session_id}"},
                "extract": "entry_id from response.data.entry.id"
            }
        ],
        "notes": [
            "此方式产生 entry_type=file（非在线文档），但内容完整不截断",
            "每步都是小参数调用，不会触发 MCP 参数大小限制",
            "如需在线文档格式，请配置 LEXIANG_TOKEN 后用模式1重新上传"
        ]
    }
    
    print(json.dumps(instructions, ensure_ascii=False, indent=2))
    return instructions


def main():
    parser = argparse.ArgumentParser(
        description="通用大文档上传到乐享知识库（绕过 MCP connector 参数大小限制）")
    parser.add_argument("md_path", help="Markdown 文件路径")
    parser.add_argument("--parent-id", help="目标目录 entry_id")
    parser.add_argument("--name", help="文档标题")
    parser.add_argument("--space-id", default="", help="知识库 space_id")
    parser.add_argument("--mode", choices=["auto", "online-doc", "file", "instructions"],
                        default="auto",
                        help="上传模式: auto(自动选择), online-doc(在线文档), file(文件上传), instructions(输出Agent指令)")
    parser.add_argument("--token", default=os.environ.get("LEXIANG_TOKEN", ""))
    parser.add_argument("--company-from", default=os.environ.get("COMPANY_FROM", ""))
    parser.add_argument("--base-url", default=os.environ.get("MCP_BASE_URL", "https://mcp.lexiang-app.com"))
    
    # 预签名 URL 模式的参数（Agent 直接传入）
    parser.add_argument("--upload-url", help="预签名上传URL（模式2）")
    parser.add_argument("--session-id", help="上传会话ID（模式2）")
    
    args = parser.parse_args()
    md_path = Path(args.md_path)
    
    if not md_path.exists():
        sys.exit(f"❌ 文件不存在: {md_path}")
    
    name = args.name or md_path.stem
    
    print(f"{'='*60}")
    print(f"📄 大文档上传: {md_path.name}")
    print(f"   大小: {md_path.stat().st_size / 1024:.1f} KB")
    print(f"   标题: {name}")
    print(f"{'='*60}")
    
    # 模式选择
    if args.mode == "instructions" or (args.mode == "auto" and not args.token):
        if not args.parent_id:
            sys.exit("❌ --parent-id 必须指定")
        return output_agent_instructions(md_path, args.parent_id, name)
    
    if not args.token or not args.company_from:
        print("⚠️ 未设置 LEXIANG_TOKEN 或 COMPANY_FROM")
        print("   切换到 instructions 模式...")
        if not args.parent_id:
            sys.exit("❌ --parent-id 必须指定")
        return output_agent_instructions(md_path, args.parent_id, name)
    
    if not args.parent_id:
        sys.exit("❌ --parent-id 必须指定")
    
    # 有 token，执行上传
    if args.mode in ("auto", "online-doc"):
        result = upload_as_online_doc(
            md_path, args.parent_id, name, args.space_id,
            args.token, args.company_from, args.base_url,
        )
        if "error" not in result:
            return result
        
        if args.mode == "online-doc":
            sys.exit(f"❌ 在线文档创建失败: {result}")
        
        print("⚠️ 在线文档创建失败，降级为文件上传...")
    
    # 文件上传模式
    result = upload_as_file(
        md_path, args.parent_id,
        args.token, args.company_from, args.base_url,
    )
    return result


if __name__ == "__main__":
    main()
