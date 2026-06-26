#!/usr/bin/env python3
"""读取乐享知识库中已存储的 PDF：调用 entry_describe_ai_parse_content 获取
完整、丰富的解析内容（含 markdown 结构 + 图片标题/描述/链接），并生成图片清单。

这是「乐享内 PDF 翻译归档」流程最关键的一步——拿到完整原文解析，
后续翻译和转存才能顺畅进行。

用法：
    python3 lexiang_pdf_parse.py <entry_id> [--out-dir DIR] [--download-pdf]

输出（默认写到 ./<safe_title>/）：
    parsed_raw.md       解析出的完整 markdown 原文（含 [IMAGE] 块、页码注释）
    images.json         图片清单：index / page / title / desc / asset_link / context
    meta.json           条目元信息：title / parent_id / space_id / file_id / extension
    paper.pdf           （--download-pdf 时）原始 PDF，供 pymupdf 提取图表

依赖：标准库 only。Token 从 ~/.cursor/mcp.json 读取，company_from 从 skill config.json 读取。
"""
import json
import os
import re
import sys
import urllib.request

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_token():
    """从 ~/.cursor/mcp.json 读取乐享 MCP token（去掉 Bearer 前缀）。"""
    p = os.path.expanduser("~/.cursor/mcp.json")
    d = json.load(open(p))
    auth = d["mcpServers"]["lexiang"]["headers"]["Authorization"]
    return auth if auth.lower().startswith("bearer ") else "Bearer " + auth


def load_company_from():
    cfg = os.path.join(SKILL_DIR, "config.json")
    if os.path.exists(cfg):
        d = json.load(open(cfg))
        cf = d.get("lexiang", {}).get("target_space", {}).get("company_from")
        if cf:
            return cf
    return os.environ.get("LEXIANG_COMPANY_FROM", "")


def mcp_call(name, arguments, token, company_from):
    url = f"https://mcp.lexiang-app.com/mcp?company_from={company_from}"
    body = {
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    }
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": token},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode())
    inner = json.loads(result["result"]["content"][0]["text"])
    return inner


def build_image_inventory(content):
    """解析 [IMAGE]...[/IMAGE] 块，关联页码与上下文。"""
    lines = content.split("\n")
    cur_page, imgs, i, n = 0, [], 0, len(lines)
    while i < n:
        ln = lines[i]
        m = re.search(r'page-number", "value": (\d+)', ln)
        if m:
            cur_page = int(m.group(1))
        if ln.strip() == "[IMAGE]":
            link = title = desc = ""
            j = i + 1
            while j < n and lines[j].strip() != "[/IMAGE]":
                if lines[j].startswith("图片链接"):
                    link = lines[j].split("：", 1)[-1].strip()
                elif lines[j].startswith("图片标题"):
                    title = lines[j].split("：", 1)[-1].strip()
                elif lines[j].startswith("图片描述"):
                    desc = lines[j].split("：", 1)[-1].strip()
                j += 1
            ctx, k = "", j + 1
            while k < n and k < j + 6:
                t = lines[k].strip()
                if t and t != "[IMAGE]":
                    ctx = t[:80]
                    break
                k += 1
            imgs.append({
                "index": len(imgs), "page": cur_page, "title": title,
                "desc": desc, "asset_link": link, "context": ctx,
            })
            i = j + 1
        else:
            i += 1
    return imgs


def safe(name):
    return re.sub(r'[\\/:*?"<>|]', "_", name).strip()[:80] or "lexiang_pdf"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    entry_id = sys.argv[1]
    out_dir = None
    download_pdf = "--download-pdf" in sys.argv
    if "--out-dir" in sys.argv:
        out_dir = sys.argv[sys.argv.index("--out-dir") + 1]

    token = load_token()
    company_from = load_company_from()
    if not company_from:
        print("ERROR: company_from 未找到（检查 skill config.json 或 LEXIANG_COMPANY_FROM）")
        sys.exit(2)

    entry = mcp_call("entry_describe_entry", {"entry_id": entry_id}, token, company_from)
    e = entry["data"]["entry"]
    title = e.get("name", entry_id)
    meta = {
        "entry_id": entry_id, "title": title, "parent_id": e.get("parent_id"),
        "space_id": e.get("space_id"), "file_id": e.get("target_id"),
        "extension": e.get("extension"), "entry_type": e.get("entry_type"),
    }

    out_dir = out_dir or safe(title)
    os.makedirs(out_dir, exist_ok=True)

    parse = mcp_call("entry_describe_ai_parse_content", {"entry_id": entry_id}, token, company_from)
    content = parse["data"]["content"]
    open(os.path.join(out_dir, "parsed_raw.md"), "w").write(content)

    imgs = build_image_inventory(content)
    json.dump(imgs, open(os.path.join(out_dir, "images.json"), "w"), ensure_ascii=False, indent=2)
    json.dump(meta, open(os.path.join(out_dir, "meta.json"), "w"), ensure_ascii=False, indent=2)

    if download_pdf and meta["file_id"]:
        dl = mcp_call("file_download_file", {"file_id": meta["file_id"], "expire_seconds": 3600}, token, company_from)
        url = dl["data"]["url"]
        pdf_path = os.path.join(out_dir, "paper.pdf")
        with urllib.request.urlopen(url, timeout=300) as r, open(pdf_path, "wb") as f:
            f.write(r.read())
        print(f"  PDF downloaded -> {pdf_path} ({os.path.getsize(pdf_path)} bytes)")

    print(f"Title      : {title}")
    print(f"Parent dir : {meta['parent_id']}  (转存回此目录)")
    print(f"Parsed     : {out_dir}/parsed_raw.md  ({len(content)} chars)")
    print(f"Images     : {len(imgs)} 个 [IMAGE] 标记 -> {out_dir}/images.json")
    n_head = len(re.findall(r"(?m)^#{1,4}\s", content))
    print(f"Headings   : {n_head} 个标题")
    print("\n下一步：剔除装饰性图片→对真数据图表用 pymupdf 卡片裁剪→降级冗余标题为加粗正文→")
    print("       默认用当前模型逐块翻译为中英对照（标题单行双语 'EN / 中文'），再用 md_to_page.py 转存回 parent_id。")


if __name__ == "__main__":
    main()
