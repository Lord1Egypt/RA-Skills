#!/usr/bin/env python3
"""
Convert Markdown to Feishu document blocks and insert into a document.

Usage:
    python3 md2blocks.py <doc_token> <markdown_file_or_-> [--after <block_id>] [--replace]

Arguments:
    doc_token       Target document token
    markdown_file   Path to markdown file, or "-" to read from stdin
    --after ID      Insert after this block ID (appends to root if omitted)
    --replace       Delete all existing content before inserting

Reads Feishu app credentials from ~/.openclaw/openclaw.json
"""
import json, sys, os, argparse, urllib.request, urllib.error

def get_credentials():
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    with open(config_path) as f:
        d = json.load(f)
    c = d["channels"]["feishu"]
    return c.get("appId", ""), c.get("appSecret", "")

def get_token(app_id, app_secret):
    payload = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=payload, headers={"Content-Type": "application/json"}, method="POST"
    )
    return json.loads(urllib.request.urlopen(req).read())["tenant_access_token"]

def api_call(token, method, url, body=None):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=utf-8"}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        return json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"HTTP {e.code}: {error_body[:500]}", file=sys.stderr)
        sys.exit(1)

def convert_markdown(token, markdown):
    url = "https://open.feishu.cn/open-apis/docx/v1/documents/blocks/convert"
    resp = api_call(token, "POST", url, {"content_type": "markdown", "content": markdown})
    if resp.get("code") != 0:
        print(f"Convert error: {resp.get('msg')}", file=sys.stderr)
        sys.exit(1)
    return resp["data"]

def clean_blocks(blocks):
    """Remove merge_info from table blocks (required before insertion)."""
    for block in blocks:
        if block.get("block_type") == 31 and "table" in block:
            prop = block["table"].get("property", {})
            if "merge_info" in prop:
                del prop["merge_info"]
    return blocks

def get_doc_children(token, doc_token):
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{doc_token}"
    resp = api_call(token, "GET", url)
    if resp.get("code") != 0:
        return []
    return resp.get("data", {}).get("block", {}).get("children", [])

def delete_blocks_by_range(token, doc_token, start_index, end_index):
    """Delete blocks by index range [start_index, end_index)."""
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{doc_token}/children/batch_delete"
    resp = api_call(token, "DELETE", url, {"start_index": start_index, "end_index": end_index})
    if resp.get("code") != 0:
        print(f"Delete error: {resp.get('msg')}", file=sys.stderr)
    return resp

def insert_descendants(token, doc_token, parent_id, children_ids, descendants, index=None):
    """Insert blocks using the descendant API (supports tables and nested blocks).
    
    IMPORTANT: index must be in the request body, NOT as a query parameter.
    Passing index as ?index=N in the URL is silently ignored by the API.
    """
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{parent_id}/descendant"
    body = {
        "children_id": children_ids,
        "descendants": descendants
    }
    if index is not None:
        body["index"] = index
    resp = api_call(token, "POST", url, body)
    if resp.get("code") != 0:
        print(f"Insert error (code={resp.get('code')}): {resp.get('msg')}", file=sys.stderr)
        sys.exit(1)
    children = resp.get("data", {}).get("children", [])
    print(f"SUCCESS: Inserted {len(children)} top-level blocks")
    return children

def find_block_index(token, doc_token, after_block_id):
    children = get_doc_children(token, doc_token)
    for i, child_id in enumerate(children):
        if child_id == after_block_id:
            return i + 1
    print(f"WARNING: Block {after_block_id} not found, appending", file=sys.stderr)
    return None

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to Feishu doc blocks")
    parser.add_argument("doc_token", help="Target document token")
    parser.add_argument("markdown_file", help="Markdown file path or '-' for stdin")
    parser.add_argument("--after", help="Insert after this block ID")
    parser.add_argument("--replace", action="store_true", help="Replace all existing content")
    args = parser.parse_args()

    if args.markdown_file == "-":
        markdown = sys.stdin.read()
    else:
        with open(args.markdown_file) as f:
            markdown = f.read()

    if not markdown.strip():
        print("ERROR: Empty markdown content", file=sys.stderr)
        sys.exit(1)

    app_id, app_secret = get_credentials()
    token = get_token(app_id, app_secret)

    # Convert markdown to blocks
    convert_data = convert_markdown(token, markdown)
    blocks = clean_blocks(convert_data.get("blocks", []))
    first_level_ids = convert_data.get("first_level_block_ids", [])

    print(f"Converted: {len(first_level_ids)} top-level blocks, {len(blocks)} total blocks")

    # Handle --replace
    if args.replace:
        children = get_doc_children(token, args.doc_token)
        if children:
            print(f"Deleting {len(children)} existing blocks...")
            delete_blocks_by_range(token, args.doc_token, 0, len(children))

    # Determine insertion index
    index = None
    if args.after:
        index = find_block_index(token, args.doc_token, args.after)

    # Insert using descendant API
    insert_descendants(token, args.doc_token, args.doc_token, first_level_ids, blocks, index)

if __name__ == "__main__":
    main()
