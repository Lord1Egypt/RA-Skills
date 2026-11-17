"""capability-list — enumerate all 27 subcommands.

26 API operations mapped 1:1 to Blog System API v1.0.0 endpoints, plus
this ``capability-list`` command itself. Command names use flat
kebab-case (verb-noun style).

The output dict contains only ``commands`` and ``total`` — there is no
``version`` or ``skill`` field.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

COMMANDS: List[Dict[str, str]] = [
    # Articles (7)
    {"module": "articles", "name": "list-articles",
     "description": "分页列出文章 (GET /api/articles)"},
    {"module": "articles", "name": "create-article",
     "description": "创建文章 (POST /api/articles)"},
    {"module": "articles", "name": "get-article",
     "description": "获取文章详情及评论 (GET /api/articles/{id})"},
    {"module": "articles", "name": "update-article",
     "description": "更新文章 (PUT /api/articles/{id})"},
    {"module": "articles", "name": "delete-article",
     "description": "删除文章，支持软删除 (DELETE /api/articles/{id})"},
    {"module": "articles", "name": "restore-article",
     "description": "恢复软删除的文章 (POST /api/articles/{id}/restore)"},
    {"module": "articles", "name": "top-articles",
     "description": "获取热门文章 (GET /api/articles/heat/top)"},
    # Labels (2)
    {"module": "labels", "name": "list-labels",
     "description": "列出所有标签 (GET /api/lables)"},
    {"module": "labels", "name": "create-label",
     "description": "创建标签 (POST /api/lables)"},
    # Users (2)
    {"module": "users", "name": "list-users",
     "description": "列出所有用户 (GET /api/users)"},
    {"module": "users", "name": "create-user",
     "description": "创建用户 (POST /api/users)"},
    # Comments (3)
    {"module": "comments", "name": "create-comment",
     "description": "创建评论 (POST /api/comments)"},
    {"module": "comments", "name": "list-comments",
     "description": "列出文章评论 (GET /api/comments/{aid})"},
    {"module": "comments", "name": "delete-comment",
     "description": "删除评论 (DELETE /api/comments/{comment_id})"},
    # Messages (4)
    {"module": "messages", "name": "list-messages",
     "description": "列出留言及回复 (GET /api/messages)"},
    {"module": "messages", "name": "create-message",
     "description": "创建留言 (POST /api/messages)"},
    {"module": "messages", "name": "reply-message",
     "description": "回复留言 (POST /api/messages/reply)"},
    {"module": "messages", "name": "delete-message",
     "description": "删除留言 (DELETE /api/messages/{message_id})"},
    # Moods (3)
    {"module": "moods", "name": "list-moods",
     "description": "列出说说 (GET /api/moods)"},
    {"module": "moods", "name": "create-mood",
     "description": "创建说说 (POST /api/moods)"},
    {"module": "moods", "name": "delete-mood",
     "description": "删除说说 (DELETE /api/moods/{mood_id})"},
    # Uploads (4)
    {"module": "uploads", "name": "upload-file",
     "description": "上传单个文件 (POST /api/upload, multipart file)"},
    {"module": "uploads", "name": "upload-files",
     "description": "批量上传文件 (POST /api/upload/multiple, multipart files)"},
    {"module": "uploads", "name": "list-uploads",
     "description": "列出已上传文件 (GET /api/uploads/list)"},
    {"module": "uploads", "name": "delete-upload",
     "description": "删除已上传文件 (DELETE /api/uploads/{filename})"},
    # Health (1)
    {"module": "health", "name": "health-check",
     "description": "健康检查 (GET /health)"},
    # Meta (1)
    {"module": "meta", "name": "capability-list",
     "description": "列出全部 27 个子命令"},
]


def list_commands() -> Tuple[Dict[str, Any], str]:
    """Return the capability list (data dict + kind tag)."""
    data: Dict[str, Any] = {"commands": COMMANDS, "total": len(COMMANDS)}
    return data, "capability_list"
