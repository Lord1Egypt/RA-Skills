#!/usr/bin/env python3
"""印象笔记客户端 — 直接使用 Thrift 接口，兼容 Python 3.14"""
import os
import sys
import json
import hashlib
import argparse
import base64
import ssl
import certifi

# 设置 SSL 证书路径（解决 Python 3.14 的证书问题）
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

from thrift.transport.THttpClient import THttpClient
from thrift.protocol.TBinaryProtocol import TBinaryProtocol

# 直接导入 SDK 中的 thrift 接口定义
from evernote.edam.type.ttypes import Note, Notebook
from evernote.edam.notestore import NoteStore
from evernote.edam.notestore.ttypes import NoteFilter
from evernote.edam.error.ttypes import EDAMSystemException, EDAMUserException, EDAMNotFoundException


class YinxiangClient:
    """印象笔记客户端"""
    
    PROD_HOST = "app.yinxiang.com"
    SANDBOX_HOST = "sandbox.yinxiang.com"
    
    def __init__(self, token=None, sandbox=False):
        self.token = token or self._load_token()
        if not self.token:
            raise ValueError("未配置 YINXIANG_TOKEN，请在 .env 文件中设置")
        
        self.host = self.SANDBOX_HOST if sandbox else self.PROD_HOST
        self.sandbox = sandbox
        self._note_store = None
    
    @staticmethod
    def _load_token():
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        if k.strip() == "YINXIANG_TOKEN":
                            return v.strip()
        return os.environ.get("YINXIANG_TOKEN", "")
    
    @property
    def note_store(self):
        if self._note_store is None:
            # Token 格式: S=s9:U=xxx... → userId = s9
            user_id = self.token.split(':')[0].split('=')[-1] if '=' in self.token else ""
            note_store_url = f"https://{self.host}/edam/note/{user_id}"
            
            http_client = THttpClient(note_store_url)
            http_client.setCustomHeaders({"Authorization": self.token})
            protocol = TBinaryProtocol(http_client)
            self._note_store = NoteStore.Client(protocol)
        return self._note_store
    
    def create_note(self, title, content, notebook_guid=None, tags=None, resources=None):
        note = Note()
        note.title = title
        
        if not content.strip().startswith('<?xml'):
            content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>{content}</en-note>'''
        note.content = content
        
        if notebook_guid:
            note.notebookGuid = notebook_guid
        if tags:
            note.tagNames = tags
        if resources:
            note.resources = resources
        
        return self.note_store.createNote(self.token, note)
    
    def get_note(self, guid, with_content=True):
        return self.note_store.getNote(self.token, guid, with_content, True, False, False)
    
    def update_note(self, note):
        return self.note_store.updateNote(self.token, note)
    
    def delete_note(self, guid):
        self.note_store.deleteNote(self.token, guid)
    
    def search_notes(self, query, max_results=20, offset=0):
        nf = NoteFilter()
        nf.words = query
        nf.maxResults = max_results
        nf.offset = offset
        return self.note_store.findNotes(self.token, nf, offset, max_results)
    
    def list_notebooks(self):
        return self.note_store.listNotebooks(self.token)
    
    def list_tags(self):
        return self.note_store.listTags(self.token)


def print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="印象笔记 CLI")
    parser.add_argument("--sandbox", action="store_true", help="使用沙盒环境")
    sub = parser.add_subparsers(dest="cmd")
    
    # create
    c = sub.add_parser("create", help="创建笔记")
    c.add_argument("title", help="标题")
    c.add_argument("content", help="内容（纯文本或 ENML）")
    c.add_argument("--notebook", help="笔记本 GUID")
    c.add_argument("--tags", help="标签，逗号分隔")
    
    # search
    s = sub.add_parser("search", help="搜索笔记")
    s.add_argument("query", help="搜索关键词")
    s.add_argument("--max", type=int, default=20, help="最大结果数")
    
    # get
    g = sub.add_parser("get", help="获取笔记详情")
    g.add_argument("guid", help="笔记 GUID")
    
    # delete
    d = sub.add_parser("delete", help="删除笔记（移入回收站）")
    d.add_argument("guid", help="笔记 GUID")
    
    # notebooks
    sub.add_parser("notebooks", help="列出笔记本")
    
    # tags
    sub.add_parser("tags", help="列出标签")
    
    args = parser.parse_args()
    
    if not args.cmd:
        parser.print_help()
        sys.exit(0)
    
    try:
        client = YinxiangClient(sandbox=args.sandbox)
    except ValueError as e:
        print_json({"success": False, "error": str(e)})
        sys.exit(1)
    
    try:
        if args.cmd == "create":
            tags = [t.strip() for t in args.tags.split(',')] if args.tags else None
            content = args.content
            if not content.strip().startswith('<'):
                content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                content = content.replace('\n', '<br/>')
            note = client.create_note(args.title, content,
                                      notebook_guid=args.notebook, tags=tags)
            print_json({"success": True, "guid": note.guid, "title": note.title,
                         "url": f"https://app.yinxiang.com/Home.action#n={note.guid}",
                         "created": note.created})
        
        elif args.cmd == "search":
            result = client.search_notes(args.query, args.max)
            notes = []
            for n in result.notes:
                notes.append({"guid": n.guid, "title": n.title,
                              "url": f"https://app.yinxiang.com/Home.action#n={n.guid}"})
            print_json({"success": True, "total": result.totalNotes, "notes": notes})
        
        elif args.cmd == "get":
            note = client.get_note(args.guid)
            # 提取纯文本内容
            content = note.content or ""
            import re
            text = re.sub(r'<[^>]+>', '', content)
            text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            text = text.strip()
            print_json({"success": True, "guid": note.guid, "title": note.title,
                         "content_text": text, "content_enml": note.content,
                         "created": note.created, "updated": note.updated,
                         "notebookGuid": note.notebookGuid,
                         "url": f"https://app.yinxiang.com/Home.action#n={note.guid}"})
        
        elif args.cmd == "delete":
            client.delete_note(args.guid)
            print_json({"success": True, "guid": args.guid, "message": "已移入回收站"})
        
        elif args.cmd == "notebooks":
            nbs = client.list_notebooks()
            print_json({"success": True, "notebooks": [
                {"guid": nb.guid, "name": nb.name, "default": nb.defaultNotebook}
                for nb in nbs
            ]})
        
        elif args.cmd == "tags":
            tags = client.list_tags()
            print_json({"success": True, "tags": [
                {"guid": t.guid, "name": t.name} for t in tags
            ]})
    
    except EDAMUserException as e:
        print_json({"success": False, "error": f"用户错误: {e.parameter} - {e.errorCode}"})
        sys.exit(1)
    except EDAMSystemException as e:
        err_map = {1: "未知错误", 2: "内部错误", 3: "数据受限",
                   4: "认证过期", 5: "权限不足", 6: "配额超限",
                   7: "无效认证", 8: "服务暂时不可用"}
        print_json({"success": False, "error": f"系统错误: {err_map.get(e.errorCode, e.errorCode)}"})
        sys.exit(1)
    except Exception as e:
        print_json({"success": False, "error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
