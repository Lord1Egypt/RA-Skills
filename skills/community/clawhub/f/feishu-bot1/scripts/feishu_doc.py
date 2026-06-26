"""
飞书文档操作脚本
用法:
  python feishu_doc.py create "<标题>"
  python feishu_doc.py delete <doc_token>
  python feishu_doc.py read <doc_token>
  python feishu_doc.py write <doc_token> "<markdown内容>"
  python feishu_doc.py append <doc_token> "<文本>"
  python feishu_doc.py append-block <doc_token> "<段落文本>"
  python feishu_doc.py query-block <doc_token> <block_id>
  python feishu_doc.py update-block <doc_token> <block_id> "<新文本>"
"""

import json
import sys
import urllib.request
import urllib.error

SCRIPT_DIR = __file__.rsplit("/", 1)[0] if "/" in __file__ else __file__.rsplit("\\", 1)[0]
CONFIG_PATH = SCRIPT_DIR + "/config.json"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_tenant_access_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    return result.get("tenant_access_token", "")


def create_document(title):
    config = load_config()
    token = get_tenant_access_token(config["app_id"], config["app_secret"])
    url = "https://open.feishu.cn/open-apis/docx/v1/documents"
    data = json.dumps({"title": title}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    })
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if result.get("code") != 0:
        print(json.dumps(result, ensure_ascii=False))
        return
    doc = result["data"]["document"]
    print(json.dumps({"doc_token": doc["document_id"], "doc_url": f"https://feishu.cn/docx/{doc['document_id']}"}, ensure_ascii=False))


def delete_document(doc_token):
    config = load_config()
    token = get_tenant_access_token(config["app_id"], config["app_secret"])
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}"
    req = urllib.request.Request(url, method="DELETE", headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    print(json.dumps(result, ensure_ascii=False))


def read_document(doc_token):
    config = load_config()
    token = get_tenant_access_token(config["app_id"], config["app_secret"])
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks?page_size=500"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    print(json.dumps(result, ensure_ascii=False, indent=2))


def _text_to_blocks(text):
    """将文本转为 Text Block（block_type=2）"""
    blocks = []
    for line in text.split("\n"):
        blocks.append({
            "block_type": 2,  # Text Block
            "text": {
                "elements": [{"type": "text_run", "text_run": {"content": line}}]
            }
        })
    return blocks


def write_document(doc_token, content):
    config = load_config()
    token = get_tenant_access_token(config["app_id"], config["app_secret"])

    # 获取现有 blocks
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks?page_size=500"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    if result.get("code") != 0:
        print(json.dumps(result, ensure_ascii=False))
        return

    items = result["data"]["items"]
    if not items:
        print(json.dumps({"error": "文档为空或不存在"}))
        return

    root_block_id = items[0]["block_id"]

    # 写入：新 blocks
    url2 = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{root_block_id}/children"
    blocks = _text_to_blocks(content)
    data = json.dumps({"children": blocks, "index": 0}).encode("utf-8")
    req2 = urllib.request.Request(url2, data=data, method="POST", headers={
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {token}"
    })
    with urllib.request.urlopen(req2) as resp:
        result2 = json.loads(resp.read())
    print(json.dumps(result2, ensure_ascii=False))


def append_paragraph(doc_token, text):
    config = load_config()
    token = get_tenant_access_token(config["app_id"], config["app_secret"])

    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks?page_size=500"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    if result.get("code") != 0:
        print(json.dumps(result, ensure_ascii=False))
        return

    items = result["data"]["items"]
    if not items:
        print(json.dumps({"error": "文档为空"}))
        return

    root_block_id = items[0]["block_id"]

    url2 = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{root_block_id}/children"
    blocks = _text_to_blocks(text)
    data = json.dumps({"children": blocks}).encode("utf-8")
    req2 = urllib.request.Request(url2, data=data, method="POST", headers={
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {token}"
    })
    with urllib.request.urlopen(req2) as resp:
        result2 = json.loads(resp.read())
    print(json.dumps(result2, ensure_ascii=False))


def query_block(doc_token, block_id):
    config = load_config()
    token = get_tenant_access_token(config["app_id"], config["app_secret"])
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{block_id}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    print(json.dumps(result, ensure_ascii=False, indent=2))


def update_block_text(doc_token, block_id, new_text):
    """更新指定 block 的文本内容（仅支持 Text/Heading/Bullet 等文本类 block）"""
    config = load_config()
    token = get_tenant_access_token(config["app_id"], config["app_secret"])
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{block_id}"
    data = json.dumps({
        "update_text_elements": {
            "elements": [{"type": "text_run", "text_run": {"content": new_text}}]
        }
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="PATCH", headers={
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {token}"
    })
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    print(json.dumps(result, ensure_ascii=False))


def append_block(doc_token, text):
    """追加段落 block（便捷别名）"""
    append_paragraph(doc_token, text)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        print("用法: python feishu_doc.py <command> [args...]")
        sys.exit(1)

    cmd = args[0]

    if cmd == "create" and len(args) >= 2:
        create_document(args[1])
    elif cmd == "delete" and len(args) >= 2:
        delete_document(args[1])
    elif cmd == "read" and len(args) >= 2:
        read_document(args[1])
    elif cmd == "write" and len(args) >= 3:
        write_document(args[1], args[2])
    elif cmd == "append" and len(args) >= 3:
        append_paragraph(args[1], args[2])
    elif cmd == "append-block" and len(args) >= 3:
        append_block(args[1], args[2])
    elif cmd == "query-block" and len(args) >= 3:
        query_block(args[1], args[2])
    elif cmd == "update-block" and len(args) >= 4:
        update_block_text(args[1], args[2], args[3])
    else:
        print("未知命令或参数不足")
        sys.exit(1)
