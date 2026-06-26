#!/usr/bin/env python3
"""
Feishu Docs Tool - 飞书文档读写工具
Usage:
  python3 feishu_docs.py list                    # 列出最近文档
  python3 feishu_docs.py read <doc_id>           # 读取文档内容
  python3 feishu_docs.py create <title>          # 创建新文档（用户身份）
  python3 feishu_docs.py write <doc_id> <text>   # 追加文本段落
  python3 feishu_docs.py token                   # 刷新 user_access_token
  python3 feishu_docs.py code <doc_id> <text>      # 追加代码块
  python3 feishu_docs.py image <doc_id> <url>     # 从网址插入图片
"""

import json, os, sys, requests, webbrowser, time

APP_ID = os.environ.get("FEISHU_APP_ID")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET")
BASE = "https://open.feishu.cn/open-apis"
TOKEN_FILE = os.path.expanduser("~/.openclaw/.feishu_user_token")
# 笔记存放文件夹，留空则存云盘根目录
ACE_FOLDER_TOKEN = os.environ.get("FEISHU_FOLDER_TOKEN") or ""

def get_user_token():
    """读取缓存的 user_access_token，过期则自动刷新"""
    if not os.path.exists(TOKEN_FILE):
        return ""
    with open(TOKEN_FILE) as f:
        data = json.load(f)
    
    token = data.get("access_token", "")
    refresh = data.get("refresh_token", "")
    
    if token and refresh:
        # Try to refresh proactively - Feishu tokens live ~2h
        r = requests.post(f"{BASE}/authen/v1/refresh_access_token",
            json={
                "app_id": APP_ID,
                "app_secret": APP_SECRET,
                "grant_type": "refresh_token",
                "refresh_token": refresh
            })
        result = r.json()
        if result.get("code") == 0:
            d = result["data"]
            new_data = {
                "access_token": d.get("access_token", token),
                "refresh_token": d.get("refresh_token", refresh),
                "expires_in": d.get("expires_in", 6900)
            }
            with open(TOKEN_FILE, "w") as f:
                json.dump(new_data, f)
            os.chmod(TOKEN_FILE, 0o600)
            return new_data["access_token"]
    
    return token

def save_user_token(token):
    with open(TOKEN_FILE, "w") as f:
        json.dump({"access_token": token}, f)
    os.chmod(TOKEN_FILE, 0o600)

def get_app_token():
    r = requests.post(f"{BASE}/auth/v3/tenant_access_token/internal", json={
        "app_id": APP_ID, "app_secret": APP_SECRET
    })
    return r.json().get("tenant_access_token", "")

def list_docs(token, limit=10):
    r = requests.get(f"{BASE}/drive/v1/files?page_size={limit}",
        headers={"Authorization": f"Bearer {token}"})
    data = r.json()
    if data.get("code") != 0:
        return data
    files = data.get("data", {}).get("files", [])
    result = []
    for f in files:
        ft = f.get("token") or f.get("file_token", "")
        ftype = f.get("type", "")
        url_prefix = {"docx": "docx", "sheet": "sheet", "folder": "drive/folder"}.get(ftype, "file")
        result.append({
            "name": f.get("name"),
            "type": ftype,
            "id": ft,
            "url": f"https://bytedance.feishu.cn/{url_prefix}/{ft}" if ft else ""
        })
    return result

def read_doc(token, doc_id):
    r = requests.get(f"{BASE}/docx/v1/documents/{doc_id}/blocks/{doc_id}",
        headers={"Authorization": f"Bearer {token}"})
    title_data = r.json()
    title = ""
    if title_data.get("code") == 0:
        block = title_data.get("data", {}).get("block", {})
        page = block.get("page", {})
        els = page.get("elements", [])
        title = "".join(e.get("text_run", {}).get("content", "") for e in els)

    all_text = []
    page_token = None
    while True:
        url = f"{BASE}/docx/v1/documents/{doc_id}/blocks/{doc_id}/children?page_size=50"
        if page_token:
            url += f"&page_token={page_token}"
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        data = r.json()
        if data.get("code") != 0:
            break
        items = data.get("data", {}).get("items", [])
        for i, item in enumerate(items):
            bt = item.get("block_type", 0)
            if bt == 2:
                els = item.get("text", {}).get("elements", [])
                txt = "".join(e.get("text_run", {}).get("content", "") for e in els)
                all_text.append(txt)
            elif bt == 3:
                els = item.get("heading1", {}).get("elements", [])
                txt = "".join(e.get("text_run", {}).get("content", "") for e in els)
                all_text.append(f"# {txt}")
            elif bt == 4:
                els = item.get("heading2", {}).get("elements", [])
                txt = "".join(e.get("text_run", {}).get("content", "") for e in els)
                all_text.append(f"## {txt}")
            elif bt == 5:
                els = item.get("heading3", {}).get("elements", [])
                txt = "".join(e.get("text_run", {}).get("content", "") for e in els)
                all_text.append(f"### {txt}")
        page_token = data.get("data", {}).get("page_token")
        if not page_token:
            break
    return {"title": title, "content": all_text, "url": f"https://bytedance.feishu.cn/docx/{doc_id}"}

def create_doc(token, title):
    # Create document
    r = requests.post(f"{BASE}/docx/v1/documents",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"title": title})
    data = r.json()
    if data.get("code") != 0:
        return data
    
    doc = data.get("data", {}).get("document", {})
    doc_id = doc.get("document_id")
    
    # Move to Ace folder
    if ACE_FOLDER_TOKEN:
        requests.post(f"{BASE}/drive/v1/files/{doc_id}/move",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"type": "docx", "folder_token": ACE_FOLDER_TOKEN})
    
    return {
        "id": doc_id,
        "title": doc.get("title"),
        "url": f"https://bytedance.feishu.cn/docx/{doc_id}"
    }

def write_text(token, doc_id, text):
    """Write plain text paragraph."""
    r = requests.post(f"{BASE}/docx/v1/documents/{doc_id}/blocks/{doc_id}/children",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"children": [{"block_type": 2, "text": {"elements": [{"text_run": {"content": text}}]}}]})
    return r.json().get("code") == 0

def write_styled_text(token, doc_id, elements):
    """Write paragraph with styled elements.
    elements: list of (text, style_dict) tuples.
    style_dict keys: bold, italic, inline_code, text_color, background_color
    text_color/background_color: 0-9 (飞书颜色索引)
    """
    children = []
    for content, style in elements:
        el = {"text_run": {"content": content}}
        if style:
            el["text_run"]["text_element_style"] = {k: v for k, v in style.items() if v}
        children.append(el)
    r = requests.post(f"{BASE}/docx/v1/documents/{doc_id}/blocks/{doc_id}/children",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"children": [{"block_type": 2, "text": {"elements": children}}]})
    return r.json().get("code") == 0

def write_heading(token, doc_id, text, level=2):
    """Append a heading block. level: 2=H2 (数字序号+标题), 3=H3 (短标题)"""
    bt = {2: 4, 3: 5}.get(level, 4)
    key = {2: "heading2", 3: "heading3"}.get(level, "heading2")
    r = requests.post(f"{BASE}/docx/v1/documents/{doc_id}/blocks/{doc_id}/children",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"children": [{"block_type": bt, key: {"elements": [{"text_run": {"content": text}}]}}]})
    return r.json().get("code") == 0

def add_table(token, doc_id, headers, rows):
    """Create a table with bold headers and data rows.
    headers: list of header strings
    rows: list of lists, each inner list is one data row
    """
    nrows = len(rows) + 1
    ncols = len(headers)
    r = requests.post(f"{BASE}/docx/v1/documents/{doc_id}/blocks/{doc_id}/children",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"children": [{"block_type": 31, "table": {"property": {"row_size": nrows, "column_size": ncols}}}]})
    result = r.json()
    if result.get("code") != 0:
        return False, result.get("msg", "")
    cells = result["data"]["children"][0]["table"]["cells"]
    all_content = headers + [item for row in rows for item in row]
    for i, (cid, ct) in enumerate(zip(cells, all_content)):
        is_header = i < ncols
        r2 = requests.get(f"{BASE}/docx/v1/documents/{doc_id}/blocks/{cid}",
            headers={"Authorization": f"Bearer {token}"})
        children = r2.json().get("data", {}).get("block", {}).get("children", [])
        el = {"text_run": {"content": ct, "text_element_style": {"bold": is_header}}}
        if children:
            # PATCH first child with content
            chid = children[0]
            requests.patch(f"{BASE}/docx/v1/documents/{doc_id}/blocks/{chid}",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json={"update_text_elements": {"elements": [el]}})
            # Delete extra children (fewer races with PATCH-first approach)
            for ch in children[1:]:
                requests.delete(f"{BASE}/docx/v1/documents/{doc_id}/blocks/{ch}",
                    headers={"Authorization": f"Bearer {token}"})
        else:
            requests.post(f"{BASE}/docx/v1/documents/{doc_id}/blocks/{cid}/children",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json={"children": [{"block_type": 2, "text": {"elements": [el]}}]})
        time.sleep(0.06)
    return True, ""

def insert_image(token, doc_id, image_url=None, image_data=None):
    """Insert an image into a Feishu doc. 3-step process:
    1. Create empty image block
    2. Upload image linked to block id
    3. PATCH with replace_image to bind token
    Returns (success, image_block_id or error_msg)
    """
    import io
    # Step 1: Create empty image block
    payload = {"index": -1, "children": [{"block_type": 27, "image": {}}]}
    r = requests.post(f"{BASE}/docx/v1/documents/{doc_id}/blocks/{doc_id}/children",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, json=payload)
    result = r.json()
    if result.get("code") != 0:
        return False, f"Step1 fail: {result.get('msg')}"
    block_id = result["data"]["children"][0]["block_id"]
    time.sleep(0.3)

    # Step 2: Upload image (download if URL provided)
    if image_url and not image_data:
        img_r = requests.get(image_url, timeout=15)
        image_data = img_r.content
    if not image_data:
        return False, "No image data"
    files = {"file": ("image.png", io.BytesIO(image_data), "image/png")}
    data = {"file_name": "image.png", "parent_type": "docx_image", "parent_node": block_id, "size": str(len(image_data))}
    r2 = requests.post(f"{BASE}/drive/v1/medias/upload_all",
        headers={"Authorization": f"Bearer {token}"}, data=data, files=files)
    result2 = r2.json()
    if result2.get("code") != 0:
        return False, f"Step2 fail: {result2.get('msg')}"
    file_token = result2["data"]["file_token"]
    time.sleep(0.3)

    # Step 3: PATCH with replace_image
    patch = {"replace_image": {"token": file_token}}
    r3 = requests.patch(f"{BASE}/docx/v1/documents/{doc_id}/blocks/{block_id}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, json=patch)
    result3 = r3.json()
    if result3.get("code") != 0:
        return False, f"Step3 fail: {result3.get('msg')}"
    return True, block_id

def write_code(token, doc_id, text):
    """Append code block. Note: do NOT include 'style' field - Feishu API rejects it."""
    r = requests.post(f"{BASE}/docx/v1/documents/{doc_id}/blocks/{doc_id}/children",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"children": [{"block_type": 14, "code": {
            "elements": [{"text_run": {"content": text}}], "wrap": True}}]})
    return r.json().get("code") == 0


if __name__ == "__main__":
    if not APP_ID or not APP_SECRET:
        print('请设置环境变量: export FEISHU_APP_ID="xxx" FEISHU_APP_SECRET="xxx"')
        sys.exit(1)

    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    
    # user token for personal space operations
    user_token = get_user_token()
    if not user_token:
        print("❌ 未获取 user_access_token，请先通过 OAuth 授权")
        sys.exit(1)

    if cmd == "list":
        docs = list_docs(user_token)
        if isinstance(docs, list):
            for d in docs:
                print(f"  📄 {d['name']}  [{d['type']}]  id={d['id']}")
                print(f"     链接: {d['url']}")
        else:
            print(f"❌ {docs.get('msg', docs)}")

    elif cmd == "read":
        doc_id = sys.argv[2] if len(sys.argv) > 2 else ""
        if not doc_id:
            print("用法: python3 feishu_docs.py read <doc_id>")
            sys.exit(1)
        doc = read_doc(user_token, doc_id)
        if "title" in doc:
            print(f"# {doc['title']}")
            print(f"链接: {doc['url']}")
            print("---")
            for line in doc["content"]:
                print(line)
        else:
            print(f"❌ {doc}")

    elif cmd == "create":
        title = sys.argv[2] if len(sys.argv) > 2 else "未命名文档"
        result = create_doc(user_token, title)
        if "id" in result:
            print(f"✅ 创建成功!")
            print(f"   标题: {result['title']}")
            print(f"   链接: {result['url']}")
        else:
            print(f"❌ {result}")

    elif cmd == "write":
        doc_id = sys.argv[2] if len(sys.argv) > 2 else ""
        text = sys.argv[3] if len(sys.argv) > 3 else ""
        if not doc_id or not text:
            print("用法: python3 feishu_docs.py write <doc_id> <text>")
            sys.exit(1)
        ok = write_text(user_token, doc_id, text)
        print(f"{'✅ 已追加' if ok else '❌ 写入失败'}")

    elif cmd == "heading":
        doc_id = sys.argv[2] if len(sys.argv) > 2 else ""
        text = sys.argv[3] if len(sys.argv) > 3 else ""
        level = int(sys.argv[4]) if len(sys.argv) > 4 else 2
        if not doc_id or not text:
            print("用法: python3 feishu_docs.py heading <doc_id> <text> [level=2]")
            sys.exit(1)
        ok = write_heading(user_token, doc_id, text, level)
        print(f"{'✅ H{level}标题已追加' if ok else '❌ 写入失败'}")

    elif cmd == "bold":
        doc_id = sys.argv[2] if len(sys.argv) > 2 else ""
        text = sys.argv[3] if len(sys.argv) > 3 else ""
        if not doc_id or not text:
            print("用法: python3 feishu_docs.py bold <doc_id> <text>")
            sys.exit(1)
        ok = write_styled_text(user_token, doc_id, [(text, {"bold": True})])
        print(f"{'✅ 加粗文本已追加' if ok else '❌ 写入失败'}")

    elif cmd == "image":
        doc_id = sys.argv[2] if len(sys.argv) > 2 else ""
        url = sys.argv[3] if len(sys.argv) > 3 else ""
        if not doc_id or not url:
            print("用法: python3 feishu_docs.py image <doc_id> <image_url>")
            sys.exit(1)
        ok, result = insert_image(user_token, doc_id, image_url=url)
        print(f"{'✅ 图片已插入' if ok else '❌ ' + result}")
        if ok:
            print(f"   块ID: {result}")

    elif cmd == "code":
        doc_id = sys.argv[2] if len(sys.argv) > 2 else ""
        text = sys.argv[3] if len(sys.argv) > 3 else ""
        if not doc_id or not text:
            print("用法: python3 feishu_docs.py code <doc_id> <text>")
            sys.exit(1)
        ok = write_code(user_token, doc_id, text)
        print(f"{'✅ 代码块已追加' if ok else '❌ 写入失败'}")

    elif cmd == "token":
        with open(TOKEN_FILE) as f:
            tok_data = json.load(f)
        print(f"access_token: {tok_data.get('access_token','?')[:20]}...")
        print(f"refresh_token: {'✅ 已存' if tok_data.get('refresh_token') else '❌ 无'}")
        print(f"过期时间: {tok_data.get('expires_in','?')}秒")

    else:
        print(__doc__)
