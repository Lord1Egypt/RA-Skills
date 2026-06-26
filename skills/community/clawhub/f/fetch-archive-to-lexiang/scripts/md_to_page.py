#!/usr/bin/env python3
"""将 Markdown 图文文章分段导入乐享在线文档（page），图片内嵌到正文对应位置。

用法:
  python3 md_to_page.py <md_file> --entry-id <ENTRY_ID> [--token TOKEN] [--company-from CF]
  python3 md_to_page.py <md_file> --parent-id <PARENT_ID> --name TITLE [--space-id SID]

环境变量: LEXIANG_TOKEN, COMPANY_FROM, MCP_BASE_URL
"""
from __future__ import annotations
import requests, json, base64, re, os, sys, time, argparse

def call_mcp_tool(base_url, company_from, token, tool_name, arguments):
    url = f"{base_url}/mcp?company_from={company_from}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": tool_name, "arguments": arguments}}
    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    if resp.status_code == 401:
        sys.exit(f"❌ LEXIANG_TOKEN 已过期或无效（HTTP 401）。请重新获取 token：https://lexiangla.com/mcp")
    if resp.status_code != 200:
        return {"error": resp.status_code}
    for line in resp.text.strip().split(chr(10)):
        line = line.strip()
        if line.startswith("data:"): line = line[5:].strip()
        if not line or line == "[DONE]": continue
        try:
            data = json.loads(line)
            if "result" in data:
                for c in data["result"].get("content", []):
                    if c.get("type") == "text":
                        result = json.loads(c["text"])
                        # Detect 401 inside response body
                        if isinstance(result, dict) and result.get("error", {}).get("code") == 401:
                            sys.exit(f"❌ LEXIANG_TOKEN 已过期或无效（API 返回 401）。请重新获取 token：https://lexiangla.com/mcp")
                        return result
            return data
        except: continue
    return {}

def import_content(base_url, cf, token, entry_id, md_text, force_write=False):
    # 直接传原始 markdown，不做 base64（MCP HTTP 直连时 base64 不会被自动解码）
    return call_mcp_tool(base_url, cf, token, "entry_import_content_to_entry", {
        "entry_id": entry_id, "content": md_text, "content_type": "markdown", "force_write": force_write})

def upload_image(base_url, cf, token, entry_id, img_path, img_name):
    size = os.path.getsize(img_path)
    # Detect actual MIME type based on file content, not extension
    # Substack CDN sometimes saves JPEG files with .png extension
    try:
        import subprocess
        fmt = subprocess.check_output(["sips", "-g", "format", img_path], stderr=subprocess.DEVNULL).decode()
        if "jpeg" in fmt.lower() or "jpg" in fmt.lower():
            mime = "image/jpeg"
        else:
            mime = "image/png"
    except (subprocess.SubprocessError, FileNotFoundError):
        # Fallback to extension-based detection
        ext = img_name.rsplit(".", 1)[-1].lower()
        mime = "image/png" if ext == "png" else "image/jpeg"
    result = call_mcp_tool(base_url, cf, token, "block_apply_block_attachment_upload", {
        "entry_id": entry_id, "name": img_name, "size": str(size), "mime_type": mime})
    if "error" in result:
        print(f"    apply_upload error: {result['error']}")
        return None
    if "data" not in result:
        print(f"    apply_upload unexpected response: {str(result)[:200]}")
        return None
    sid = result["data"]["session_id"]
    upload_url = result["data"]["upload_url"]
    with open(img_path, "rb") as f:
        r = requests.put(upload_url, data=f, headers={"Content-Type": mime, "Content-Length": str(size)}, timeout=60)
    if r.status_code != 200:
        print(f"    COS PUT failed: HTTP {r.status_code}")
    return sid if r.status_code == 200 else None

def insert_image_block(base_url, cf, token, entry_id, session_id, tmp_id):
    return call_mcp_tool(base_url, cf, token, "block_create_block_descendant", {
        "entry_id": entry_id, "index": -1,
        "descendant": [{"block_id": tmp_id, "block_type": "image", "image": {"session_id": session_id}}],
        "children": [tmp_id]})

def main():
    parser = argparse.ArgumentParser(description="Import markdown with images to Lexiang online doc")
    parser.add_argument("md_path", help="Markdown file path")
    parser.add_argument("--entry-id", help="Target page entry_id (overwrite)")
    parser.add_argument("--parent-id", help="Parent entry_id (create new page)")
    parser.add_argument("--name", help="Page name (for new page)")
    parser.add_argument("--space-id", default="", help="Space ID (for new page)")
    parser.add_argument("--token", default=os.environ.get("LEXIANG_TOKEN", ""))
    parser.add_argument("--company-from", default=os.environ.get("COMPANY_FROM", ""))
    parser.add_argument("--base-url", default=os.environ.get("MCP_BASE_URL", "https://mcp.lexiang-app.com"))
    parser.add_argument("--evaluation", default="", help="Evaluation text to add at top (short text, supports \\n for newline)")
    parser.add_argument("--evaluation-file", default="", help="File path containing evaluation text (long text, supports multiline)")
    args = parser.parse_args()

    if not args.token: sys.exit("Error: --token or LEXIANG_TOKEN required")
    if not args.company_from: sys.exit("Error: --company-from or COMPANY_FROM required")
    if not args.entry_id and not args.parent_id: sys.exit("Error: --entry-id or --parent-id required")

    base, cf, tok = args.base_url, args.company_from, args.token
    entry_id = args.entry_id

    if not entry_id:
        name = args.name or os.path.splitext(os.path.basename(args.md_path))[0]
        result = call_mcp_tool(base, cf, tok, "entry_create_entry", {
            "parent_entry_id": args.parent_id, "name": name, "entry_type": "page"})
        entry_id = result.get("data", {}).get("entry", {}).get("id", "")
        if not entry_id: sys.exit(f"Failed to create page: {result}")
        print(f"Created page: {entry_id}")
        # 置顶：获取父目录第一个条目，用 before 参数移到它之前（after="" 实测是末尾，不是置顶）
        children = call_mcp_tool(base, cf, tok, "entry_list_children", {
            "parent_id": args.parent_id, "limit": 2})
        first_entries = children.get("data", {}).get("entries", [])
        # 找到除自身之外的第一个条目，用 before 排在它之前（真正置顶）
        first_id = ""
        for e in first_entries:
            if e.get("id") != entry_id:
                first_id = e.get("id", "")
                break
        if first_id:
            call_mcp_tool(base, cf, tok, "entry_move_entry", {
                "entry_id": entry_id, "parent_id": args.parent_id, "before": first_id})
            print(f"Moved to top (before first entry: {first_id})")

    with open(args.md_path, "r") as f:
        content = f.read()

    # 处理评价信息（在顶部插入）
    eval_text = ""
    if args.evaluation:
        eval_text = args.evaluation.replace("\\n", "\n")
    elif args.evaluation_file:
        if os.path.exists(args.evaluation_file):
            with open(args.evaluation_file, "r", encoding="utf-8") as f:
                eval_text = f.read()
        else:
            print(f"Warning: evaluation file not found: {args.evaluation_file}")

    if eval_text:
        # 格式化为 blockquote，乐享可能自动转换为 callout 组件
        lines = eval_text.strip().split("\n")
        blockquote = "> **📝 凡哥的评价**\n>\n"
        for line in lines:
            blockquote += "> " + line + "\n"
        blockquote += "\n---\n\n"
        content = blockquote + content
        print(f"Added evaluation at top ({len(eval_text)} chars)")

    img_dir = os.path.join(os.path.dirname(os.path.abspath(args.md_path)), "images")
    # Match both naming patterns:
    #   fetch_article.py:     ![](images/img_01_1513609c.png)  (with hash)
    #   fetch_claude_blog.py: ![](images/img_01.png)           (without hash)
    #   generic:              ![alt](images/anything.ext)
    img_pattern = r"!\[[^\]]*\]\(images/([^)]+)\)"

    segments = []
    last_end = 0
    for m in re.finditer(img_pattern, content):
        text_before = content[last_end:m.start()].strip()
        if text_before: segments.append(("text", text_before))
        segments.append(("image", m.group(1)))
        last_end = m.end()
    remaining = content[last_end:].strip()
    if remaining: segments.append(("text", remaining))

    # Split long text chunks (>15K chars)
    final = []
    for t, c in segments:
        if t == "text" and len(c) > 15000:
            paras = c.split(chr(10) + chr(10))
            chunk = ""
            for p in paras:
                if len(chunk) + len(p) + 2 > 15000:
                    final.append(("text", chunk))
                    chunk = p
                else:
                    chunk = (chunk + chr(10) + chr(10) + p) if chunk else p
            if chunk: final.append(("text", chunk))
        else:
            final.append((t, c))

    print(f"Segments: {len(final)} (text+images)")

    first = True
    for i, (seg_type, seg_content) in enumerate(final):
        if seg_type == "text":
            print(f"  [{i}] text ({len(seg_content)} chars)...", end=" ")
            import_content(base, cf, tok, entry_id, seg_content, force_write=first)
            first = False
            print("OK")
        elif seg_type == "image":
            img_path = os.path.join(img_dir, seg_content)
            if not os.path.exists(img_path):
                print(f"  [{i}] image {seg_content} NOT FOUND")
                continue
            print(f"  [{i}] image {seg_content}...", end=" ")
            sid = upload_image(base, cf, tok, entry_id, img_path, seg_content)
            if sid:
                insert_image_block(base, cf, tok, entry_id, sid, f"img_{i}")
                print("OK")
            else:
                print("FAILED")
        time.sleep(0.3)

    print(f"\nDone! entry_id={entry_id}")

if __name__ == "__main__":
    main()
