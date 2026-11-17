#!/usr/bin/env python3
"""Blog Manager CLI — 27 subcommands for Blog System API v1.0.0.

Commands use flat kebab-case naming (verb-noun style).

Usage:
    export BLOG_MANAGER_BASE_URL=http://host:port
    python main.py <command> [options]

Run ``python main.py capability-list`` to see all 27 subcommands.
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Tuple

from blog_manager import (
    articles,
    capability,
    comments,
    health,
    labels,
    messages,
    moods,
    uploads,
    users,
)
from blog_manager.client import BlogAPIError, BlogClient, BlogConfigError
from blog_manager.formatter import format_output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="blog-manager",
        description="Blog System API v1.0.0 管理工具 (27 个子命令)",
    )
    sub = parser.add_subparsers(dest="command", required=True, metavar="<command>")

    # ---- capability-list (1) ----
    sub.add_parser("capability-list", help="列出全部 27 个子命令")

    # ---- articles (7) ----
    p = sub.add_parser("list-articles", help="分页列出文章")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--size", type=int, default=10)
    p.add_argument("--lid", type=int, default=0, help="标签 ID (0=全部)")
    p.add_argument("--keyword", type=str, default="", help="搜索关键词")

    p = sub.add_parser("create-article", help="创建文章")
    p.add_argument("--title", required=True)
    p.add_argument("--content", required=True)
    p.add_argument("--uid", type=int, default=1)
    p.add_argument("--lid", type=int, default=1)
    p.add_argument("--img", type=str, default=None)
    p.add_argument("--heat", type=int, default=0)

    p = sub.add_parser("get-article", help="获取文章详情及评论")
    p.add_argument("--id", type=int, required=True, dest="article_id")

    p = sub.add_parser("update-article", help="更新文章")
    p.add_argument("--id", type=int, required=True, dest="article_id")
    p.add_argument("--title", default=None)
    p.add_argument("--content", default=None)
    p.add_argument("--lid", type=int, default=None)
    p.add_argument("--img", default=None)
    p.add_argument("--heat", type=int, default=None)

    p = sub.add_parser("delete-article", help="删除文章 (默认软删除)")
    p.add_argument("--id", type=int, required=True, dest="article_id")
    p.add_argument(
        "--soft",
        type=str,
        default="true",
        choices=["true", "false"],
        help="软删除 (true, 默认) 或硬删除 (false)",
    )

    p = sub.add_parser("restore-article", help="恢复软删除的文章")
    p.add_argument("--id", type=int, required=True, dest="article_id")

    p = sub.add_parser("top-articles", help="获取热门文章")
    p.add_argument("--limit", type=int, default=5)

    # ---- labels (2) ----
    sub.add_parser("list-labels", help="列出所有标签")
    p = sub.add_parser("create-label", help="创建标签")
    p.add_argument("--lname", required=True, help="标签名称")

    # ---- users (2) ----
    sub.add_parser("list-users", help="列出所有用户")
    p = sub.add_parser("create-user", help="创建用户")
    p.add_argument("--uname", required=True)
    p.add_argument("--phone", default="")
    p.add_argument("--pwd", default="")
    p.add_argument("--email", default="")
    p.add_argument("--img", default="img/moren.jpg")

    # ---- comments (3) ----
    p = sub.add_parser("create-comment", help="创建评论")
    p.add_argument("--uid", type=int, required=True)
    p.add_argument("--aid", type=int, required=True)
    p.add_argument("--content", required=True)
    p = sub.add_parser("list-comments", help="列出文章评论")
    p.add_argument("--aid", type=int, required=True)
    p = sub.add_parser("delete-comment", help="删除评论")
    p.add_argument("--id", type=int, required=True, dest="comment_id")

    # ---- messages (4) ----
    sub.add_parser("list-messages", help="列出留言及回复")
    p = sub.add_parser("create-message", help="创建留言")
    p.add_argument("--uid", type=int, required=True)
    p.add_argument("--content", required=True)
    p = sub.add_parser("reply-message", help="回复留言")
    p.add_argument("--uid", type=int, required=True)
    p.add_argument("--mid", type=int, required=True)
    p.add_argument("--content", required=True)
    p = sub.add_parser("delete-message", help="删除留言")
    p.add_argument("--id", type=int, required=True, dest="message_id")

    # ---- moods (3) ----
    sub.add_parser("list-moods", help="列出说说")
    p = sub.add_parser("create-mood", help="创建说说")
    p.add_argument("--content", required=True)
    p.add_argument("--title", default="")
    p.add_argument("--src", default="")
    p = sub.add_parser("delete-mood", help="删除说说")
    p.add_argument("--id", type=int, required=True, dest="mood_id")

    # ---- uploads (4) ----
    p = sub.add_parser("upload-file", help="上传单个文件")
    p.add_argument("--file", required=True, dest="file_path", help="文件路径")
    p = sub.add_parser("upload-files", help="批量上传文件")
    p.add_argument("--files", required=True, nargs="+", dest="file_paths",
                   help="文件路径列表")
    sub.add_parser("list-uploads", help="列出已上传文件")
    p = sub.add_parser("delete-upload", help="删除已上传文件")
    p.add_argument("--filename", required=True)

    # ---- health (1) ----
    sub.add_parser("health-check", help="健康检查 (GET /health)")

    return parser


def _dispatch(
    client: BlogClient, cmd: str, args: argparse.Namespace
) -> Tuple[Any, str]:
    if cmd == "capability-list":
        return capability.list_commands()

    # articles
    if cmd == "list-articles":
        return articles.list_articles(
            client, args.page, args.size, args.lid, args.keyword
        )
    if cmd == "create-article":
        return articles.create_article(
            client, args.title, args.content, args.uid, args.lid, args.img, args.heat
        )
    if cmd == "get-article":
        return articles.get_article(client, args.article_id)
    if cmd == "update-article":
        return articles.update_article(
            client, args.article_id, args.title, args.content, args.lid, args.img, args.heat
        )
    if cmd == "delete-article":
        return articles.delete_article(
            client, args.article_id, soft=(args.soft == "true")
        )
    if cmd == "restore-article":
        return articles.restore_article(client, args.article_id)
    if cmd == "top-articles":
        return articles.top_articles(client, args.limit)

    # labels
    if cmd == "list-labels":
        return labels.list_labels(client)
    if cmd == "create-label":
        return labels.create_label(client, args.lname)

    # users
    if cmd == "list-users":
        return users.list_users(client)
    if cmd == "create-user":
        return users.create_user(
            client, args.uname, args.phone, args.pwd, args.email, args.img
        )

    # comments
    if cmd == "create-comment":
        return comments.create_comment(client, args.uid, args.aid, args.content)
    if cmd == "list-comments":
        return comments.list_comments(client, args.aid)
    if cmd == "delete-comment":
        return comments.delete_comment(client, args.comment_id)

    # messages
    if cmd == "list-messages":
        return messages.list_messages(client)
    if cmd == "create-message":
        return messages.create_message(client, args.uid, args.content)
    if cmd == "reply-message":
        return messages.reply_message(client, args.uid, args.mid, args.content)
    if cmd == "delete-message":
        return messages.delete_message(client, args.message_id)

    # moods
    if cmd == "list-moods":
        return moods.list_moods(client)
    if cmd == "create-mood":
        return moods.create_mood(client, args.content, args.title, args.src)
    if cmd == "delete-mood":
        return moods.delete_mood(client, args.mood_id)

    # uploads
    if cmd == "upload-file":
        return uploads.upload_file(client, args.file_path)
    if cmd == "upload-files":
        return uploads.upload_files(client, args.file_paths)
    if cmd == "list-uploads":
        return uploads.list_uploads(client)
    if cmd == "delete-upload":
        return uploads.delete_upload(client, args.filename)

    # health
    if cmd == "health-check":
        return health.health_check(client)

    raise ValueError(f"Unknown command: {cmd}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        client = BlogClient()
        data, kind = _dispatch(client, args.command, args)
        print(format_output(data, kind=kind, title=args.command))
    except BlogConfigError as exc:
        print(f"配置错误: {exc}", file=sys.stderr)
        sys.exit(2)
    except BlogAPIError as exc:
        print(f"API 错误: {exc}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as exc:
        print(f"文件错误: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"错误: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
