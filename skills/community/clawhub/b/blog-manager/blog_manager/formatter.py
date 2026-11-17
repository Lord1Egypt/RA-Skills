"""Output formatter — render every API response as JSON + Markdown.

Each command returns the raw API response. The CLI passes it here along
with a *kind* tag that selects a dedicated Markdown renderer. A generic
fallback handles anything untagged.
"""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List


def format_output(data: Any, kind: str = "auto", title: str = "Result") -> str:
    """Return a string containing a JSON block and a Markdown section."""
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    renderer = _RENDERERS.get(kind, _render_auto)
    md = renderer(data)
    header = f"## {title}\n\n" if title else ""
    return f"{header}### JSON\n```json\n{json_str}\n```\n\n### Markdown\n{md}\n"


def _cell(val: Any) -> str:
    if val is None:
        return ""
    s = str(val).replace("|", "\\|").replace("\n", " ")
    return s if len(s) <= 60 else s[:57] + "..."


def _ok(data: Dict[str, Any]) -> str:
    return "✓" if data.get("code") == 200 else "⚠"


def _table(headers: List[str], rows: List[List[Any]]) -> str:
    if not rows:
        return "（无数据）\n"
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        lines.append("| " + " | ".join(_cell(c) for c in row) + " |")
    return "\n".join(lines) + "\n"


def _render_auto(data: Any) -> str:
    if isinstance(data, dict):
        if "data" in data and isinstance(data["data"], list):
            return _render_list_generic(data)
        if "data" in data and isinstance(data["data"], dict):
            return _render_object(data["data"])
        if "message" in data:
            return f"{_ok(data)} {data['message']}\n"
        if "status" in data:
            return _render_health(data)
        return _render_object(data)
    if isinstance(data, list):
        return _table(["Value"], [[i] for i in data])
    return f"```\n{data}\n```\n"


def _render_list_generic(data: Dict[str, Any]) -> str:
    items = data.get("data", [])
    extra = ""
    if "total" in data:
        extra = f" (共 {data.get('total')} 条"
        if "page" in data:
            extra += f"，第 {data.get('page')} 页"
        if "size" in data:
            extra += f"，每页 {data.get('size')} 条"
        extra += ")"
    if not items:
        return f"**列表**{extra}\n\n（无数据）\n"
    if isinstance(items[0], dict):
        headers = list(items[0].keys())
        rows = [[item.get(h) for h in headers] for item in items]
        return f"**列表**{extra}\n\n" + _table(headers, rows)
    return f"**列表**{extra}\n\n" + _table(["Value"], [[v] for v in items])


def _render_object(obj: Dict[str, Any]) -> str:
    if not obj:
        return "（空对象）\n"
    lines = []
    for k, v in obj.items():
        if isinstance(v, (list, dict)):
            v_str = json.dumps(v, ensure_ascii=False)
            if len(v_str) > 80:
                v_str = v_str[:77] + "..."
        else:
            v_str = str(v) if v is not None else ""
        lines.append(f"| **{k}** | {v_str} |")
    header = "| 字段 | 值 |\n|---|---|\n"
    return header + "\n".join(lines) + "\n"


def _render_articles_list(data: Dict[str, Any]) -> str:
    items: List[Dict] = data.get("data", [])
    total = data.get("total", len(items))
    page = data.get("page", "?")
    size = data.get("size", "?")
    lines = [f"**文章列表** (共 {total} 篇，第 {page} 页，每页 {size} 篇)\n"]
    if items:
        rows = [[a.get("id"), a.get("title"), a.get("uname"), a.get("lname"),
                 a.get("heat"), a.get("deleted"), a.get("createtime", "")]
                for a in items]
        lines.append(_table(["ID", "标题", "作者", "标签", "热度", "已删", "创建时间"], rows))
    else:
        lines.append("（无文章）\n")
    return "\n".join(lines)


def _render_article_get(data: Dict[str, Any]) -> str:
    payload = data.get("data", {})
    article = payload.get("article", {}) if isinstance(payload, dict) else {}
    comments: List = payload.get("comments", []) if isinstance(payload, dict) else []
    lines = ["**文章详情**\n"]
    if article:
        lines.append(_table(
            ["字段", "值"],
            [[k, v] for k, v in article.items() if k != "content"],
        ))
        content = article.get("content", "")
        if content:
            preview = content if len(content) <= 200 else content[:200] + "..."
            lines.append(f"\n**内容预览:** {preview}\n")
    else:
        lines.append("（文章不存在）\n")
    lines.append(f"\n**评论 ({len(comments)} 条)**\n")
    if comments:
        rows = [[c.get("id"), c.get("uname"), c.get("content"), c.get("createtime", "")]
                for c in comments]
        lines.append(_table(["ID", "用户", "内容", "时间"], rows))
    return "\n".join(lines)


def _render_articles_top(data: Dict[str, Any]) -> str:
    items: List[Dict] = data.get("data", [])
    lines = ["**热门文章 Top**\n"]
    if items:
        rows = [[i + 1, a.get("id"), a.get("title"), a.get("heat")]
                for i, a in enumerate(items)]
        lines.append(_table(["排名", "ID", "标题", "热度"], rows))
    else:
        lines.append("（无数据）\n")
    return "\n".join(lines)


def _render_id_response(data: Dict[str, Any]) -> str:
    payload = data.get("data", {})
    rid = ""
    if isinstance(payload, dict):
        rid = payload.get("id", payload.get("lname", ""))
    elif isinstance(payload, (int, str)):
        rid = payload
    return f"{_ok(data)} 操作成功 (id={rid})\n"


def _render_message_response(data: Dict[str, Any]) -> str:
    msg = data.get("message", "操作完成")
    return f"{_ok(data)} {msg}\n"


def _render_labels_list(data: Dict[str, Any]) -> str:
    items: List[Dict] = data.get("data", [])
    lines = ["**标签列表**\n"]
    if items:
        lines.append(_table(["ID", "名称"], [[l.get("id"), l.get("lname")] for l in items]))
    else:
        lines.append("（无标签）\n")
    return "\n".join(lines)


def _render_label_create(data: Dict[str, Any]) -> str:
    payload = data.get("data", {})
    if isinstance(payload, dict) and "lname" in payload:
        return (f"{_ok(data)} 标签已创建 "
                f"(id={payload.get('id')}, name={payload.get('lname')})\n")
    return _render_id_response(data)


def _render_users_list(data: Dict[str, Any]) -> str:
    items: List[Dict] = data.get("data", [])
    lines = ["**用户列表**\n"]
    if items:
        rows = [[u.get("id"), u.get("uname"), u.get("phone"), u.get("email"),
                 u.get("img"), u.get("createtime", "")]
                for u in items]
        lines.append(_table(["ID", "用户名", "手机", "邮箱", "头像", "创建时间"], rows))
    else:
        lines.append("（无用户）\n")
    return "\n".join(lines)


def _render_comments_list(data: Dict[str, Any]) -> str:
    items: List[Dict] = data.get("data", [])
    lines = [f"**评论列表 ({len(items)} 条)**\n"]
    if items:
        rows = [[c.get("id"), c.get("uname"), c.get("content"), c.get("createtime", "")]
                for c in items]
        lines.append(_table(["ID", "用户", "内容", "时间"], rows))
    else:
        lines.append("（无评论）\n")
    return "\n".join(lines)


def _render_messages_list(data: Dict[str, Any]) -> str:
    items: List[Dict] = data.get("data", [])
    lines = [f"**留言列表 ({len(items)} 条)**\n"]
    if not items:
        lines.append("（无留言）\n")
        return "\n".join(lines)
    for m in items:
        lines.append(
            f"- **#{m.get('id')}** {m.get('uname')}: {m.get('content')} "
            f"`{m.get('createtime', '')}`"
        )
        replies: List[Dict] = m.get("replies", [])
        for r in replies:
            lines.append(
                f"  - ↳ **#{r.get('id')}** {r.get('uname')}: {r.get('content')} "
                f"`{r.get('createtime', '')}`"
            )
    return "\n".join(lines) + "\n"


def _render_moods_list(data: Dict[str, Any]) -> str:
    items: List[Dict] = data.get("data", [])
    lines = [f"**说说列表 ({len(items)} 条)**\n"]
    if items:
        rows = [[m.get("id"), m.get("title"), m.get("content"), m.get("src"),
                 m.get("createtime", "")]
                for m in items]
        lines.append(_table(["ID", "标题", "内容", "媒体", "时间"], rows))
    else:
        lines.append("（无说说）\n")
    return "\n".join(lines)


def _render_upload_single(data: Dict[str, Any]) -> str:
    payload = data.get("data", {})
    if isinstance(payload, dict):
        rows = [[k, v] for k, v in payload.items()]
        return f"{_ok(data)} 文件已上传\n\n" + _table(["字段", "值"], rows)
    return _render_id_response(data)


def _render_upload_multiple(data: Dict[str, Any]) -> str:
    items: List[Dict] = data.get("data", [])
    lines = [f"{_ok(data)} 批量上传完成 ({len(items)} 个文件)\n"]
    if items:
        rows = [[f.get("url"), f.get("filename"), f.get("type"), f.get("size")]
                for f in items]
        lines.append(_table(["URL", "文件名", "类型", "大小"], rows))
    return "\n".join(lines)


def _render_uploads_list(data: Dict[str, Any]) -> str:
    items: List[Dict] = data.get("data", [])
    lines = [f"**上传文件列表 ({len(items)} 个)**\n"]
    if items:
        rows = [[f.get("filename"), f.get("url"), f.get("type"), f.get("size")]
                for f in items]
        lines.append(_table(["文件名", "URL", "类型", "大小"], rows))
    else:
        lines.append("（无文件）\n")
    return "\n".join(lines)


def _render_health(data: Dict[str, Any]) -> str:
    status = data.get("status", "unknown")
    icon = "✅" if status == "ok" else "❌"
    rows = [[k, v] for k, v in data.items()]
    return f"{icon} **健康状态**\n\n" + _table(["字段", "值"], rows)


def _render_capability_list(data: Dict[str, Any]) -> str:
    commands: List[Dict] = data.get("commands", [])
    lines = [f"**Blog Manager — 可用子命令 ({len(commands)} 个)**\n"]
    lines.append("| # | 模块 | 子命令 | 说明 |")
    lines.append("|---|---|---|---|")
    for idx, cmd in enumerate(commands, 1):
        lines.append(
            f"| {idx} | {cmd.get('module')} | `{cmd.get('name')}` | {cmd.get('description')} |"
        )
    return "\n".join(lines) + "\n"


_RENDERERS: Dict[str, Callable[[Any], str]] = {
    "auto": _render_auto,
    "articles_list": _render_articles_list,
    "article_get": _render_article_get,
    "articles_top": _render_articles_top,
    "id_response": _render_id_response,
    "message_response": _render_message_response,
    "labels_list": _render_labels_list,
    "label_create": _render_label_create,
    "users_list": _render_users_list,
    "comments_list": _render_comments_list,
    "messages_list": _render_messages_list,
    "moods_list": _render_moods_list,
    "upload_single": _render_upload_single,
    "upload_multiple": _render_upload_multiple,
    "uploads_list": _render_uploads_list,
    "health": _render_health,
    "capability_list": _render_capability_list,
}
