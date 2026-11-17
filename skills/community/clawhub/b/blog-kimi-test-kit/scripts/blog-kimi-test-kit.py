#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""blog-kimi-test-kit — Blog REST API management CLI tool

Capabilities:
  health-check           — GET /health, check API health
  list-articles          — GET /api/articles, list articles
  create-article         — POST /api/articles, create article
  get-article            — GET /api/articles/{article_id}, get article by ID
  update-article         — PUT /api/articles/{article_id}, update article
  delete-article         — DELETE /api/articles/{article_id}, delete article
  restore-article        — POST /api/articles/{article_id}/restore, restore article
  top-articles           — GET /api/articles/heat/top, get top articles
  list-labels            — GET /api/labels, list labels
  create-label           — POST /api/lables, create label
  list-users             — GET /api/users, list users
  create-user            — POST /api/users, create user
  create-comment         — POST /api/comments, create comment
  list-comments          — GET /api/comments/{aid}, list comments by article
  delete-comment         — DELETE /api/comments/{comment_id}, delete comment
  list-messages          — GET /api/messages, list messages
  create-message         — POST /api/messages, create message
  reply-message          — POST /api/messages/reply, reply to message
  delete-message         — DELETE /api/messages/{message_id}, delete message
  list-moods             — GET /api/moods, list moods
  create-mood            — POST /api/moods, create mood
  delete-mood            — DELETE /api/moods/{mood_id}, delete mood
  upload-file            — POST /api/upload, upload single file
  upload-files           — POST /api/upload/multiple, upload multiple files
  list-uploads           — GET /api/uploads/list, list uploads
  delete-upload          — DELETE /api/uploads/{filename}, delete upload
  admin-delete-articles  — POST /admin/api/delete, admin delete articles

Authentication: none (public API)
Exit codes: 0=success; 2=argument error; 3=missing config; 4=API failure
"""

import argparse
import glob
import json
import os
import sys

# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------

_CRED_PREFIX = "BLOG_KIMI_TEST_KIT"
_AUTH_TYPE = "none"


def _load_credentials():
    creds = {}
    creds.update(_load_from_project_knowledge())
    for k, v in os.environ.items():
        u = k.upper()
        if u.startswith(_CRED_PREFIX):
            if "BASE_URL" in u:
                creds.setdefault("base_url", v)
    return creds


def _load_from_project_knowledge():
    creds = {}
    for filepath in glob.glob(".project-info/**/*.json", recursive=True):
        try:
            with open(filepath) as f:
                data = json.load(f)
            secrets = data.get("secrets", {})
            config = data.get("config", {})
            prefix = _CRED_PREFIX + "_"
            for key, val in secrets.items():
                if key.upper().startswith(prefix):
                    if "BASE_URL" in key.upper():
                        creds.setdefault("base_url", val)
            if "base_url" not in creds:
                for key, val in config.items():
                    if key.upper() == (prefix + "BASE_URL"):
                        creds.setdefault("base_url", val)
                        break
        except Exception:
            continue
    return creds


def _get_base_url():
    creds = _load_credentials()
    base_url = creds.get("base_url", "").rstrip("/")
    if not base_url:
        print(
            "No %s_BASE_URL env var or .project-info/ config found." % _CRED_PREFIX
        )
        print("Enter API base URL (e.g. http://host:port):")
        base_url = input("> ").strip().rstrip("/")
        if not base_url:
            print("Error: API base URL cannot be empty", file=sys.stderr)
            sys.exit(3)
        if not (base_url.startswith("http://") or base_url.startswith("https://")):
            print("Error: URL must start with http:// or https://", file=sys.stderr)
            sys.exit(3)
        print(
            "Hint: export %s_BASE_URL=\"%s\" to persist."
            % (_CRED_PREFIX, base_url)
        )
    return base_url


# ---------------------------------------------------------------------------
# API client
# ---------------------------------------------------------------------------

def _build_auth(creds):
    return {}


def _api_request(method, path, payload=None, params=None, files=None):
    import requests

    base_url = _get_base_url()
    creds = _load_credentials()
    auth_result = _build_auth(creds)

    api_key_param = auth_result.pop("_api_key_param", None)
    api_key_value = auth_result.pop("_api_key_value", None)
    if api_key_param and api_key_value:
        params = dict(params or {})
        params[api_key_param] = api_key_value

    auth_kwargs = auth_result
    url = f"{base_url}{path}"

    try:
        if method == "GET":
            resp = requests.get(url, params=params, timeout=30, **auth_kwargs)
        elif method == "POST":
            resp = requests.post(
                url, json=payload, files=files, timeout=30, **auth_kwargs
            )
        elif method == "PUT":
            resp = requests.put(
                url, json=payload, files=files, timeout=30, **auth_kwargs
            )
        elif method == "PATCH":
            resp = requests.patch(url, json=payload, timeout=30, **auth_kwargs)
        elif method == "DELETE":
            resp = requests.delete(url, params=params, timeout=30, **auth_kwargs)
        else:
            print("Error: unsupported method %s" % method, file=sys.stderr)
            sys.exit(2)

        resp.raise_for_status()
        if resp.content:
            return resp.json()
        return {}
    except requests.exceptions.HTTPError as e:
        print(
            "Error: API call failed %s: %s" % (resp.status_code, e),
            file=sys.stderr,
        )
        sys.exit(4)
    except requests.exceptions.RequestException as e:
        print("Error: network request failed: %s" % e, file=sys.stderr)
        sys.exit(4)
    except ValueError:
        print(
            "Error: API returned non-JSON (possibly HTML error page)",
            file=sys.stderr,
        )
        sys.exit(4)


# ---------------------------------------------------------------------------
# Subcommand implementations
# ---------------------------------------------------------------------------

def cmd_health_check(args):
    """Check API health."""
    result = _api_request("GET", "/health")
    return result


def cmd_list_articles(args):
    """List articles with optional filters."""
    params = {}
    if args.page is not None:
        params["page"] = args.page
    if args.size is not None:
        params["size"] = args.size
    if args.lid is not None:
        params["lid"] = args.lid
    if args.keyword is not None:
        params["keyword"] = args.keyword
    result = _api_request("GET", "/api/articles", params=params)
    return result


def cmd_create_article(args):
    """Create a new article."""
    payload = {"title": args.title, "content": args.content}
    if args.uid is not None:
        payload["uid"] = args.uid
    if args.lid is not None:
        payload["lid"] = args.lid
    if args.img is not None:
        payload["img"] = args.img
    if args.heat is not None:
        payload["heat"] = args.heat
    result = _api_request("POST", "/api/articles", payload=payload)
    return result


def cmd_get_article(args):
    """Get article by ID."""
    result = _api_request("GET", "/api/articles/%s" % args.article_id)
    return result


def cmd_update_article(args):
    """Update article by ID."""
    payload = {}
    if args.title is not None:
        payload["title"] = args.title
    if args.content is not None:
        payload["content"] = args.content
    if args.lid is not None:
        payload["lid"] = args.lid
    if args.img is not None:
        payload["img"] = args.img
    if args.heat is not None:
        payload["heat"] = args.heat
    result = _api_request(
        "PUT", "/api/articles/%s" % args.article_id, payload=payload
    )
    return result


def cmd_delete_article(args):
    """Delete article by ID."""
    params = {}
    if args.soft is not None:
        params["soft"] = args.soft
    result = _api_request(
        "DELETE", "/api/articles/%s" % args.article_id, params=params
    )
    return result


def cmd_restore_article(args):
    """Restore soft-deleted article."""
    result = _api_request("POST", "/api/articles/%s/restore" % args.article_id)
    return result


def cmd_top_articles(args):
    """Get top articles."""
    params = {}
    if args.limit is not None:
        params["limit"] = args.limit
    result = _api_request("GET", "/api/articles/heat/top", params=params)
    return result


def cmd_list_labels(args):
    """List all labels."""
    result = _api_request("GET", "/api/lables")
    return result


def cmd_create_label(args):
    """Create a new label."""
    payload = {"lname": args.lname}
    result = _api_request("POST", "/api/lables", payload=payload)
    return result


def cmd_list_users(args):
    """List all users."""
    result = _api_request("GET", "/api/users")
    return result


def cmd_create_user(args):
    """Create a new user."""
    payload = {"uname": args.uname}
    if args.phone is not None:
        payload["phone"] = args.phone
    if args.pwd is not None:
        payload["pwd"] = args.pwd
    if args.email is not None:
        payload["email"] = args.email
    if args.img is not None:
        payload["img"] = args.img
    result = _api_request("POST", "/api/users", payload=payload)
    return result


def cmd_create_comment(args):
    """Create a comment."""
    payload = {"uid": args.uid, "aid": args.aid, "content": args.content}
    result = _api_request("POST", "/api/comments", payload=payload)
    return result


def cmd_list_comments(args):
    """List comments by article ID."""
    result = _api_request("GET", "/api/comments/%s" % args.aid)
    return result


def cmd_delete_comment(args):
    """Delete comment by ID."""
    result = _api_request("DELETE", "/api/comments/%s" % args.comment_id)
    return result


def cmd_list_messages(args):
    """List all messages."""
    result = _api_request("GET", "/api/messages")
    return result


def cmd_create_message(args):
    """Create a new message."""
    payload = {"uid": args.uid, "content": args.content}
    result = _api_request("POST", "/api/messages", payload=payload)
    return result


def cmd_reply_message(args):
    """Reply to a message."""
    payload = {"uid": args.uid, "mid": args.mid, "content": args.content}
    result = _api_request("POST", "/api/messages/reply", payload=payload)
    return result


def cmd_delete_message(args):
    """Delete message by ID."""
    result = _api_request("DELETE", "/api/messages/%s" % args.message_id)
    return result


def cmd_list_moods(args):
    """List all moods."""
    result = _api_request("GET", "/api/moods")
    return result


def cmd_create_mood(args):
    """Create a new mood."""
    payload = {"content": args.content}
    if args.title is not None:
        payload["title"] = args.title
    if args.src is not None:
        payload["src"] = args.src
    result = _api_request("POST", "/api/moods", payload=payload)
    return result


def cmd_delete_mood(args):
    """Delete mood by ID."""
    result = _api_request("DELETE", "/api/moods/%s" % args.mood_id)
    return result


def cmd_upload_file(args):
    """Upload a single file."""
    if not os.path.isfile(args.filepath):
        print("Error: file not found: %s" % args.filepath, file=sys.stderr)
        sys.exit(4)
    with open(args.filepath, "rb") as f:
        result = _api_request("POST", "/api/upload", files={"file": f})
    return result


def cmd_upload_files(args):
    """Upload multiple files."""
    for fp in args.filepaths:
        if not os.path.isfile(fp):
            print("Error: file not found: %s" % fp, file=sys.stderr)
            sys.exit(4)
    files = [open(fp, "rb") for fp in args.filepaths]
    try:
        result = _api_request(
            "POST", "/api/upload/multiple", files=[("file", f) for f in files]
        )
    finally:
        for f in files:
            f.close()
    return result


def cmd_list_uploads(args):
    """List all uploads."""
    result = _api_request("GET", "/api/uploads/list")
    return result


def cmd_delete_upload(args):
    """Delete upload by filename."""
    result = _api_request("DELETE", "/api/uploads/%s" % args.filename)
    return result


def cmd_admin_delete_articles(args):
    """Admin delete articles."""
    result = _api_request("POST", "/admin/api/delete")
    return result


def cmd_capability_list(args):
    """List all capabilities of this skill."""
    return {
        "capability": "capability-list",
        "skill": "blog-kimi-test-kit",
        "version": "1.0.0",
        "capabilities": [
            {
                "name": "health-check",
                "description": "Check API health",
                "command": "health-check",
            },
            {
                "name": "list-articles",
                "description": "List articles with optional filters",
                "command": "list-articles [--page PAGE] [--size SIZE] [--lid LID] [--keyword KEYWORD]",
            },
            {
                "name": "create-article",
                "description": "Create a new article",
                "command": "create-article --title TITLE --content CONTENT [--uid UID] [--lid LID] [--img IMG] [--heat HEAT]",
            },
            {
                "name": "get-article",
                "description": "Get article by ID",
                "command": "get-article --article-id ARTICLE_ID",
            },
            {
                "name": "update-article",
                "description": "Update article by ID",
                "command": "update-article --article-id ARTICLE_ID [--title TITLE] [--content CONTENT] [--lid LID] [--img IMG] [--heat HEAT]",
            },
            {
                "name": "delete-article",
                "description": "Delete article by ID",
                "command": "delete-article --article-id ARTICLE_ID [--soft SOFT]",
            },
            {
                "name": "restore-article",
                "description": "Restore soft-deleted article",
                "command": "restore-article --article-id ARTICLE_ID",
            },
            {
                "name": "top-articles",
                "description": "Get top articles",
                "command": "top-articles [--limit LIMIT]",
            },
            {
                "name": "list-labels",
                "description": "List all labels",
                "command": "list-labels",
            },
            {
                "name": "create-label",
                "description": "Create a new label",
                "command": "create-label --lname LNAME",
            },
            {
                "name": "list-users",
                "description": "List all users",
                "command": "list-users",
            },
            {
                "name": "create-user",
                "description": "Create a new user",
                "command": "create-user --uname UNAME [--phone PHONE] [--pwd PWD] [--email EMAIL] [--img IMG]",
            },
            {
                "name": "create-comment",
                "description": "Create a comment",
                "command": "create-comment --uid UID --aid AID --content CONTENT",
            },
            {
                "name": "list-comments",
                "description": "List comments by article ID",
                "command": "list-comments --aid AID",
            },
            {
                "name": "delete-comment",
                "description": "Delete comment by ID",
                "command": "delete-comment --comment-id COMMENT_ID",
            },
            {
                "name": "list-messages",
                "description": "List all messages",
                "command": "list-messages",
            },
            {
                "name": "create-message",
                "description": "Create a new message",
                "command": "create-message --uid UID --content CONTENT",
            },
            {
                "name": "reply-message",
                "description": "Reply to a message",
                "command": "reply-message --uid UID --mid MID --content CONTENT",
            },
            {
                "name": "delete-message",
                "description": "Delete message by ID",
                "command": "delete-message --message-id MESSAGE_ID",
            },
            {
                "name": "list-moods",
                "description": "List all moods",
                "command": "list-moods",
            },
            {
                "name": "create-mood",
                "description": "Create a new mood",
                "command": "create-mood --content CONTENT [--title TITLE] [--src SRC]",
            },
            {
                "name": "delete-mood",
                "description": "Delete mood by ID",
                "command": "delete-mood --mood-id MOOD_ID",
            },
            {
                "name": "upload-file",
                "description": "Upload a single file",
                "command": "upload-file --filepath FILEPATH",
            },
            {
                "name": "upload-files",
                "description": "Upload multiple files",
                "command": "upload-files --filepaths FILEPATH [FILEPATH ...]",
            },
            {
                "name": "list-uploads",
                "description": "List all uploads",
                "command": "list-uploads",
            },
            {
                "name": "delete-upload",
                "description": "Delete upload by filename",
                "command": "delete-upload --filename FILENAME",
            },
            {
                "name": "admin-delete-articles",
                "description": "Admin delete articles",
                "command": "admin-delete-articles",
            },
            {
                "name": "capability-list",
                "description": "List all capabilities of this skill",
                "command": "capability-list",
            },
        ],
    }


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def render_md(payload):
    cap = payload.get("capability", "")
    if cap == "capability-list":
        lines = [
            "## Capabilities (blog-kimi-test-kit)",
            "",
            "| Capability | Description | Command |",
            "|---|---|---|",
        ]
        for c in payload.get("capabilities", []):
            lines.append("| %s | %s | `%s` |" % (c["name"], c["description"], c["command"]))
        return "\n".join(lines)
    return json.dumps(payload, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="blog-kimi-test-kit",
        description="Blog REST API management CLI tool",
    )

    def add_common_args(p):
        p.add_argument(
            "--format",
            choices=["json", "md"],
            default="json",
            help="output format, default json",
        )

    sub = parser.add_subparsers(dest="command", help="capability commands")

    # health-check
    p_health_check = sub.add_parser("health-check", help="Check API health")
    add_common_args(p_health_check)

    # list-articles
    p_list_articles = sub.add_parser("list-articles", help="List articles with optional filters")
    p_list_articles.add_argument("--page", type=int, default=None, help="page number")
    p_list_articles.add_argument("--size", type=int, default=None, help="page size")
    p_list_articles.add_argument("--lid", type=int, default=None, help="label ID filter")
    p_list_articles.add_argument("--keyword", type=str, default=None, help="search keyword")
    add_common_args(p_list_articles)

    # create-article
    p_create_article = sub.add_parser("create-article", help="Create a new article")
    p_create_article.add_argument("--title", required=True, help="article title")
    p_create_article.add_argument("--content", required=True, help="article content")
    p_create_article.add_argument("--uid", type=int, default=None, help="user ID")
    p_create_article.add_argument("--lid", type=int, default=None, help="label ID")
    p_create_article.add_argument("--img", type=str, default=None, help="image URL")
    p_create_article.add_argument("--heat", type=int, default=None, help="heat value")
    add_common_args(p_create_article)

    # get-article
    p_get_article = sub.add_parser("get-article", help="Get article by ID")
    p_get_article.add_argument("--article-id", required=True, help="article ID")
    add_common_args(p_get_article)

    # update-article
    p_update_article = sub.add_parser("update-article", help="Update article by ID")
    p_update_article.add_argument("--article-id", required=True, help="article ID")
    p_update_article.add_argument("--title", type=str, default=None, help="article title")
    p_update_article.add_argument("--content", type=str, default=None, help="article content")
    p_update_article.add_argument("--lid", type=int, default=None, help="label ID")
    p_update_article.add_argument("--img", type=str, default=None, help="image URL")
    p_update_article.add_argument("--heat", type=int, default=None, help="heat value")
    add_common_args(p_update_article)

    # delete-article
    p_delete_article = sub.add_parser("delete-article", help="Delete article by ID")
    p_delete_article.add_argument("--article-id", required=True, help="article ID")
    p_delete_article.add_argument(
        "--soft", type=str, default=None, help="soft delete flag (true/false)"
    )
    add_common_args(p_delete_article)

    # restore-article
    p_restore_article = sub.add_parser("restore-article", help="Restore soft-deleted article")
    p_restore_article.add_argument("--article-id", required=True, help="article ID")
    add_common_args(p_restore_article)

    # top-articles
    p_top_articles = sub.add_parser("top-articles", help="Get top articles")
    p_top_articles.add_argument("--limit", type=int, default=None, help="number of top articles")
    add_common_args(p_top_articles)

    # list-labels
    p_list_labels = sub.add_parser("list-labels", help="List all labels")
    add_common_args(p_list_labels)

    # create-label
    p_create_label = sub.add_parser("create-label", help="Create a new label")
    p_create_label.add_argument("--lname", required=True, help="label name")
    add_common_args(p_create_label)

    # list-users
    p_list_users = sub.add_parser("list-users", help="List all users")
    add_common_args(p_list_users)

    # create-user
    p_create_user = sub.add_parser("create-user", help="Create a new user")
    p_create_user.add_argument("--uname", required=True, help="username")
    p_create_user.add_argument("--phone", type=str, default=None, help="phone number")
    p_create_user.add_argument("--pwd", type=str, default=None, help="password")
    p_create_user.add_argument("--email", type=str, default=None, help="email")
    p_create_user.add_argument("--img", type=str, default=None, help="image URL")
    add_common_args(p_create_user)

    # create-comment
    p_create_comment = sub.add_parser("create-comment", help="Create a comment")
    p_create_comment.add_argument("--uid", type=int, required=True, help="user ID")
    p_create_comment.add_argument("--aid", type=int, required=True, help="article ID")
    p_create_comment.add_argument("--content", required=True, help="comment content")
    add_common_args(p_create_comment)

    # list-comments
    p_list_comments = sub.add_parser("list-comments", help="List comments by article ID")
    p_list_comments.add_argument("--aid", type=int, required=True, help="article ID")
    add_common_args(p_list_comments)

    # delete-comment
    p_delete_comment = sub.add_parser("delete-comment", help="Delete comment by ID")
    p_delete_comment.add_argument("--comment-id", type=int, required=True, help="comment ID")
    add_common_args(p_delete_comment)

    # list-messages
    p_list_messages = sub.add_parser("list-messages", help="List all messages")
    add_common_args(p_list_messages)

    # create-message
    p_create_message = sub.add_parser("create-message", help="Create a new message")
    p_create_message.add_argument("--uid", type=int, required=True, help="user ID")
    p_create_message.add_argument("--content", required=True, help="message content")
    add_common_args(p_create_message)

    # reply-message
    p_reply_message = sub.add_parser("reply-message", help="Reply to a message")
    p_reply_message.add_argument("--uid", type=int, required=True, help="user ID")
    p_reply_message.add_argument("--mid", type=int, required=True, help="message ID")
    p_reply_message.add_argument("--content", required=True, help="reply content")
    add_common_args(p_reply_message)

    # delete-message
    p_delete_message = sub.add_parser("delete-message", help="Delete message by ID")
    p_delete_message.add_argument("--message-id", type=int, required=True, help="message ID")
    add_common_args(p_delete_message)

    # list-moods
    p_list_moods = sub.add_parser("list-moods", help="List all moods")
    add_common_args(p_list_moods)

    # create-mood
    p_create_mood = sub.add_parser("create-mood", help="Create a new mood")
    p_create_mood.add_argument("--content", required=True, help="mood content")
    p_create_mood.add_argument("--title", type=str, default=None, help="mood title")
    p_create_mood.add_argument("--src", type=str, default=None, help="image source")
    add_common_args(p_create_mood)

    # delete-mood
    p_delete_mood = sub.add_parser("delete-mood", help="Delete mood by ID")
    p_delete_mood.add_argument("--mood-id", type=int, required=True, help="mood ID")
    add_common_args(p_delete_mood)

    # upload-file
    p_upload_file = sub.add_parser("upload-file", help="Upload a single file")
    p_upload_file.add_argument("--filepath", required=True, help="path to file to upload")
    add_common_args(p_upload_file)

    # upload-files
    p_upload_files = sub.add_parser("upload-files", help="Upload multiple files")
    p_upload_files.add_argument(
        "--filepaths", required=True, nargs="+", help="paths to files to upload"
    )
    add_common_args(p_upload_files)

    # list-uploads
    p_list_uploads = sub.add_parser("list-uploads", help="List all uploads")
    add_common_args(p_list_uploads)

    # delete-upload
    p_delete_upload = sub.add_parser("delete-upload", help="Delete upload by filename")
    p_delete_upload.add_argument("--filename", required=True, help="filename to delete")
    add_common_args(p_delete_upload)

    # admin-delete-articles
    p_admin_delete_articles = sub.add_parser(
        "admin-delete-articles", help="Admin delete articles"
    )
    add_common_args(p_admin_delete_articles)

    # capability-list
    p_capability_list = sub.add_parser(
        "capability-list", help="List all capabilities of this skill"
    )
    add_common_args(p_capability_list)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(2)

    dispatch = {
        "health-check": cmd_health_check,
        "list-articles": cmd_list_articles,
        "create-article": cmd_create_article,
        "get-article": cmd_get_article,
        "update-article": cmd_update_article,
        "delete-article": cmd_delete_article,
        "restore-article": cmd_restore_article,
        "top-articles": cmd_top_articles,
        "list-labels": cmd_list_labels,
        "create-label": cmd_create_label,
        "list-users": cmd_list_users,
        "create-user": cmd_create_user,
        "create-comment": cmd_create_comment,
        "list-comments": cmd_list_comments,
        "delete-comment": cmd_delete_comment,
        "list-messages": cmd_list_messages,
        "create-message": cmd_create_message,
        "reply-message": cmd_reply_message,
        "delete-message": cmd_delete_message,
        "list-moods": cmd_list_moods,
        "create-mood": cmd_create_mood,
        "delete-mood": cmd_delete_mood,
        "upload-file": cmd_upload_file,
        "upload-files": cmd_upload_files,
        "list-uploads": cmd_list_uploads,
        "delete-upload": cmd_delete_upload,
        "admin-delete-articles": cmd_admin_delete_articles,
        "capability-list": cmd_capability_list,
    }

    handler = dispatch.get(args.command)
    if handler is None:
        print("Error: unknown command %s" % args.command, file=sys.stderr)
        sys.exit(2)

    try:
        payload = handler(args)
        if args.format == "md":
            print(render_md(payload))
        else:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
    except SystemExit:
        raise
    except Exception as exc:
        print("Error: %s" % exc, file=sys.stderr)
        sys.exit(4)


if __name__ == "__main__":
    main()