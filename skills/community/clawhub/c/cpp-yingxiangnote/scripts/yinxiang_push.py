#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 ENML 内容写入印象笔记（生产环境 app.yinxiang.com）

为什么不用官方 SDK：
  evernote3 依赖的 oauth2 包依赖 pyutil / distutils（Python 3.12 已移除），
  且内部使用已删除的 inspect.getargspec，在 Python 3.12 上完全跑不起来。
  所以这里直接使用它自带的 Thrift 生成代码（evernote.edam.*）手搓客户端。

关键点：写入时必须设置原生属性，否则客户端不把这条笔记当「超级笔记」，
标题大纲、代码块、行距等原生能力全部不生效：
  source            = yinxiang.superNote
  sourceApplication = yinxiang.win32
  author            = 你的印象笔记昵称
  applicationData[yinxiang.noteLayout] = 行距/宽度设置

用法:
  # 检查 token
  python yinxiang_push.py check --token "S=..."

  # 列出笔记本
  python yinxiang_push.py notebooks --token "S=..."

  # 新建笔记（笔记本不存在会自动创建）
  python yinxiang_push.py create --token "S=..." --notebook string \
      --title "第 5 章 string" --content note.enml

  # 覆盖已有笔记
  python yinxiang_push.py update --token "S=..." --guid <noteGuid> \
      --title "第 5 章 string" --content note.enml
"""
import argparse
import json
import os
import sys

# Windows 控制台默认 GBK，强制 UTF-8，避免输出中文时崩溃
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    import thrift.protocol.TBinaryProtocol as TBinaryProtocol
    import thrift.transport.THttpClient as THttpClient
    from evernote.edam.userstore import UserStore
    from evernote.edam.notestore import NoteStore
    from evernote.edam.type import ttypes as Types
except ImportError as e:
    print(json.dumps({
        "success": False,
        "error": "缺少依赖，请先执行: pip install evernote3 thrift",
        "detail": str(e),
    }, ensure_ascii=False))
    sys.exit(1)

DEFAULT_HOST = "app.yinxiang.com"
LAYOUT = '{"autoLayoutWidth":1,"autoLineSpace":"recommend","autoParagraphSpace":"recommend"}'


def get_token(cli_token):
    t = cli_token or os.environ.get("YINXIANG_TOKEN") or os.environ.get("YX_AUTH_TOKEN")
    if not t:
        print(json.dumps({"success": False,
                          "error": "未提供 token，请用 --token 或设置 YINXIANG_TOKEN 环境变量"},
                         ensure_ascii=False))
        sys.exit(1)
    return t.strip()


def thrift_client(cls, url):
    http = THttpClient.THttpClient(url)
    http.setCustomHeaders({"User-Agent": "c++yingxiangnote/1.0"})
    return cls(TBinaryProtocol.TBinaryProtocol(http))


def connect(token, host):
    us = thrift_client(UserStore.Client, "https://%s/edam/user" % host)
    ns_url = us.getNoteStoreUrl(token)
    ns = thrift_client(NoteStore.Client, ns_url)
    return us, ns, ns_url


def find_or_create_notebook(ns, token, name):
    for nb in ns.listNotebooks(token):
        if nb.name.strip().lower() == name.strip().lower():
            return nb.guid, False
    nb = Types.Notebook()
    nb.name = name
    created = ns.createNotebook(token, nb)
    return created.guid, True


def native_attrs(author):
    a = Types.NoteAttributes()
    a.source = "yinxiang.superNote"
    a.sourceApplication = "yinxiang.win32"
    a.author = author
    return a


def cmd_check(a, token):
    us, ns, ns_url = connect(token, a.host)
    user = us.getUser(token)
    return {"success": True, "noteStore": ns_url,
            "username": user.username, "userId": user.id,
            "notebooks": len(ns.listNotebooks(token))}


def cmd_notebooks(a, token):
    us, ns, ns_url = connect(token, a.host)
    return {"success": True,
            "notebooks": [{"name": nb.name, "guid": nb.guid}
                          for nb in ns.listNotebooks(token)]}


def cmd_create(a, token):
    us, ns, ns_url = connect(token, a.host)
    nb_guid, created_nb = find_or_create_notebook(ns, token, a.notebook)
    content = open(a.content, encoding="utf-8").read()
    note = Types.Note()
    note.title = a.title
    note.content = content
    note.notebookGuid = nb_guid
    note.attributes = native_attrs(a.author)
    r = ns.createNote(token, note)
    # 补写行距设置（必须在 updateNote 之后，否则会被覆盖）
    try:
        ns.setNoteApplicationDataEntry(token, r.guid, "yinxiang.noteLayout", LAYOUT)
    except Exception:
        pass
    return {"success": True, "guid": r.guid, "title": r.title,
            "notebookGuid": nb_guid, "notebookCreated": created_nb,
            "bytes": len(content.encode("utf-8"))}


def cmd_update(a, token):
    us, ns, ns_url = connect(token, a.host)
    content = open(a.content, encoding="utf-8").read()
    note = Types.Note()
    note.guid = a.guid
    note.title = a.title
    note.content = content
    if a.notebook:
        nb_guid, _ = find_or_create_notebook(ns, token, a.notebook)
        note.notebookGuid = nb_guid
    note.attributes = native_attrs(a.author)
    r = ns.updateNote(token, note)
    try:
        ns.setNoteApplicationDataEntry(token, a.guid, "yinxiang.noteLayout", LAYOUT)
    except Exception:
        pass
    # 回读校验
    back = ns.getNote(token, a.guid, True, False, False, False)
    return {"success": True, "guid": r.guid, "title": back.title,
            "updateSequenceNum": r.updateSequenceNum,
            "codeBlocks": back.content.count("--en-codeblock:true"),
            "headings": back.content.count("<h1") + back.content.count("<h2")
                        + back.content.count("<h3"),
            "nativeSource": back.attributes.source}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["check", "notebooks", "create", "update"])
    ap.add_argument("--token")
    ap.add_argument("--host", default=DEFAULT_HOST, help="默认 app.yinxiang.com（生产）")
    ap.add_argument("--notebook", default="string")
    ap.add_argument("--title", default="")
    ap.add_argument("--content", help="ENML 文件路径")
    ap.add_argument("--guid", help="update 时的笔记 guid")
    ap.add_argument("--author", default="wiseclock", help="印象笔记昵称，写成你的账号名")
    a = ap.parse_args()

    token = get_token(a.token)

    if a.action in ("create", "update") and not a.content:
        print(json.dumps({"success": False, "error": "--content 必填"}, ensure_ascii=False))
        sys.exit(1)
    if a.action == "create" and not a.title:
        print(json.dumps({"success": False, "error": "create 需要 --title"}, ensure_ascii=False))
        sys.exit(1)
    if a.action == "update" and not a.guid:
        print(json.dumps({"success": False, "error": "update 需要 --guid"}, ensure_ascii=False))
        sys.exit(1)

    fn = {"check": cmd_check, "notebooks": cmd_notebooks,
          "create": cmd_create, "update": cmd_update}[a.action]
    try:
        r = fn(a, token)
    except Exception as e:
        print(json.dumps({"success": False, "error": "%s: %s" % (type(e).__name__, e)},
                         ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
