#!/usr/bin/env python3

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests


DEFAULT_BASE_URL = "https://api.mybrandmetrics.com"


def resolve_config_path(explicit_path: str | None) -> Path:
    if explicit_path:
        return Path(explicit_path).expanduser()

    env_path = os.environ.get("FACEBOOK_PAGES_CONFIG")
    if env_path:
        return Path(env_path).expanduser()

    script_dir = Path(__file__).resolve().parent
    workspace_root = script_dir.parent.parent.parent
    return workspace_root / "config.json"


def load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        return {}

    try:
        return json.loads(config_path.read_text())
    except json.JSONDecodeError as exc:
        print(f"Error: could not decode JSON from {config_path}: {exc}", file=sys.stderr)
        sys.exit(1)


def resolve_settings(args: argparse.Namespace, config: dict[str, Any]) -> dict[str, Any]:
    fb_config = config.get("facebook_pages", {})
    access_token = (
        getattr(args, "access_token", None)
        or os.environ.get("MBM_ACCESS_TOKEN")
        or os.environ.get("FACEBOOK_PAGES_ACCESS_TOKEN")
        or fb_config.get("access_token")
        or fb_config.get("authorization_token")
    )
    api_key = (
        getattr(args, "api_key", None)
        or os.environ.get("MBM_API_KEY")
        or os.environ.get("FACEBOOK_PAGES_API_KEY")
        or fb_config.get("api_key")
    )
    base_url = (
        getattr(args, "base_url", None)
        or os.environ.get("MBM_BASE_URL")
        or fb_config.get("base_url")
        or DEFAULT_BASE_URL
    )
    page_id = (
        getattr(args, "page_id", None)
        or os.environ.get("FACEBOOK_PAGES_PAGE_ID")
        or fb_config.get("page_id")
    )
    account_id = (
        getattr(args, "account_id", None)
        or os.environ.get("FACEBOOK_PAGES_ACCOUNT_ID")
        or fb_config.get("account_id")
    )
    connection_id = (
        getattr(args, "connection_id", None)
        or os.environ.get("FACEBOOK_PAGES_CONNECTION_ID")
        or fb_config.get("connection_id")
    )

    if not access_token and not api_key:
        print(
            "Error: missing Facebook Pages credentials. Provide an access token or API key "
            "via arguments, environment variables, or config.json.",
            file=sys.stderr,
        )
        sys.exit(1)

    return {
        "access_token": access_token,
        "api_key": api_key,
        "base_url": base_url.rstrip("/"),
        "page_id": page_id,
        "account_id": account_id,
        "connection_id": connection_id,
    }


class FacebookPagesClient:
    def __init__(self, settings: dict[str, Any]) -> None:
        self.base_url = settings["base_url"]
        self.page_id = settings.get("page_id")
        self.account_id = settings.get("account_id")
        self.connection_id = settings.get("connection_id")
        headers = {}
        if settings.get("access_token"):
            headers["Authorization"] = f"Bearer {settings['access_token']}"
        elif settings.get("api_key"):
            headers["X-API_KEY"] = settings["api_key"]
        self.headers = headers

    def _request(self, method: str, path: str, *, params=None, json_body=None) -> dict[str, Any]:
        response = requests.request(
            method,
            f"{self.base_url}{path}",
            headers=self.headers,
            params=params,
            json=json_body,
            timeout=300,
        )
        if response.ok:
            return response.json()

        print(f"Error: HTTP {response.status_code}", file=sys.stderr)
        print(response.text, file=sys.stderr)
        sys.exit(1)

    def _target_params(self, args: argparse.Namespace, require_any: bool = False) -> dict[str, Any]:
        page_id = getattr(args, "page_id", None) or self.page_id
        account_id = getattr(args, "account_id", None) or self.account_id
        connection_id = getattr(args, "connection_id", None) or self.connection_id

        if require_any and not any([page_id, account_id, connection_id]):
            print(
                "Error: provide page_id, account_id, or connection_id for this operation.",
                file=sys.stderr,
            )
            sys.exit(1)

        payload = {}
        if page_id:
            payload["page_id"] = page_id
        if account_id:
            payload["account_id"] = account_id
        if connection_id:
            payload["connection_id"] = connection_id
        return payload

    def connect(self) -> dict[str, Any]:
        return self._request("POST", "/auth/facebook_pages/connect")

    def list_connections(self) -> dict[str, Any]:
        return self._request(
            "GET",
            "/explorer/connections",
            params={"source_key": "facebook_pages"},
        )

    def list_accounts(self) -> dict[str, Any]:
        return self._request(
            "GET",
            "/explorer/accounts",
            params={"source_key": "facebook_pages"},
        )

    def publish_post(self, args: argparse.Namespace) -> dict[str, Any]:
        if not args.message and not args.link:
            print("Error: publish-post requires --message or --link.", file=sys.stderr)
            sys.exit(1)
        body = self._target_params(args, require_any=True)
        body.update(
            {
                "message": args.message,
                "link": args.link,
                "picture": args.picture,
                "published": not args.unpublished,
            }
        )
        return self._request("POST", "/facebook/pages/posts", json_body=body)

    def publish_photo(self, args: argparse.Namespace) -> dict[str, Any]:
        body = self._target_params(args, require_any=True)
        body.update(
            {
                "url": args.url,
                "caption": args.caption,
                "published": not args.unpublished,
            }
        )
        return self._request("POST", "/facebook/pages/photos", json_body=body)

    def publish_video(self, args: argparse.Namespace) -> dict[str, Any]:
        body = self._target_params(args, require_any=True)
        body.update(
            {
                "url": args.url,
                "caption": args.caption,
                "published": not args.unpublished,
            }
        )
        return self._request("POST", "/facebook/pages/videos", json_body=body)

    def feed(self, args: argparse.Namespace) -> dict[str, Any]:
        params = self._target_params(args, require_any=True)
        params.update(
            {
                "fields": args.fields,
                "limit": args.limit,
                "after": args.after,
                "before": args.before,
            }
        )
        return self._request("GET", "/facebook/pages/feed", params=compact_dict(params))

    def comments(self, args: argparse.Namespace) -> dict[str, Any]:
        if not args.object_id and not args.post_id:
            print("Error: comments requires --object-id or --post-id.", file=sys.stderr)
            sys.exit(1)
        params = self._target_params(args, require_any=True)
        params.update(
            {
                "object_id": args.object_id,
                "post_id": args.post_id,
                "fields": args.fields,
                "limit": args.limit,
                "after": args.after,
                "before": args.before,
            }
        )
        return self._request("GET", "/facebook/pages/comments", params=compact_dict(params))

    def comment_create(self, args: argparse.Namespace) -> dict[str, Any]:
        body = self._target_params(args, require_any=True)
        body.update({"object_id": args.object_id, "message": args.message})
        return self._request("POST", "/facebook/pages/comments", json_body=body)

    def comment_update(self, args: argparse.Namespace) -> dict[str, Any]:
        if args.message is None and args.hide is None:
            print("Error: comment-update requires --message or --hide/--unhide.", file=sys.stderr)
            sys.exit(1)
        body = self._target_params(args, require_any=True)
        body.update(
            {
                "comment_id": args.comment_id,
                "message": args.message,
                "hide": args.hide,
            }
        )
        return self._request("PATCH", "/facebook/pages/comments", json_body=compact_dict(body))

    def comment_delete(self, args: argparse.Namespace) -> dict[str, Any]:
        params = self._target_params(args, require_any=True)
        return self._request(
            "DELETE",
            f"/facebook/pages/comments/{args.comment_id}",
            params=compact_dict(params),
        )

    def insights(self, args: argparse.Namespace) -> dict[str, Any]:
        params = self._target_params(args, require_any=True)
        params.update(
            {
                "metrics": args.metrics,
                "period": args.period,
                "since": args.since,
                "until": args.until,
            }
        )
        return self._request("GET", "/facebook/pages/insights", params=compact_dict(params))

    def post_insights(self, args: argparse.Namespace) -> dict[str, Any]:
        params = self._target_params(args, require_any=False)
        params.update({"post_id": args.post_id, "object_id": args.object_id, "metrics": args.metrics})
        return self._request("GET", "/facebook/pages/posts/insights", params=compact_dict(params))


def compact_dict(values: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Facebook Pages via MyBrandMetrics API")
    parser.add_argument("--api-key", help="MyBrandMetrics API key")
    parser.add_argument("--access-token", help="MyBrandMetrics bearer token")
    parser.add_argument("--base-url", help="Override the MyBrandMetrics API base URL")
    parser.add_argument("--page-id", help="Facebook Page ID")
    parser.add_argument("--account-id", help="MyBrandMetrics account ID")
    parser.add_argument("--connection-id", help="MyBrandMetrics connection ID")
    parser.add_argument("--config", help="Path to config.json")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("connect", help="Start the Facebook Pages OAuth connect flow")
    subparsers.add_parser("list-connections", help="List connected Meta accounts")
    subparsers.add_parser("list-accounts", help="List available Facebook Pages")

    publish_post = subparsers.add_parser("publish-post", help="Create a Page feed post")
    publish_post.add_argument("--message", help="Post text")
    publish_post.add_argument("--link", help="Link to include in the post")
    publish_post.add_argument("--picture", help="Optional image URL for the link post")
    publish_post.add_argument("--unpublished", action="store_true", help="Create the post as unpublished")

    publish_photo = subparsers.add_parser("publish-photo", help="Create a Page photo post")
    publish_photo.add_argument("--url", required=True, help="Public image URL")
    publish_photo.add_argument("--caption", default="", help="Photo caption")
    publish_photo.add_argument("--unpublished", action="store_true", help="Create the photo post as unpublished")

    publish_video = subparsers.add_parser("publish-video", help="Create a Page video post")
    publish_video.add_argument("--url", required=True, help="Public video URL")
    publish_video.add_argument("--caption", default="", help="Video caption")
    publish_video.add_argument("--unpublished", action="store_true", help="Create the video post as unpublished")

    feed = subparsers.add_parser("feed", help="Read Page feed posts")
    feed.add_argument(
        "--fields",
        default="id,message,story,created_time,permalink_url,from",
        help="Comma-separated fields to request",
    )
    feed.add_argument("--limit", type=int, default=25, help="Feed page size")
    feed.add_argument("--after", help="Pagination cursor")
    feed.add_argument("--before", help="Pagination cursor")

    comments = subparsers.add_parser("comments", help="Read comments on a post or comment")
    comments.add_argument("--object-id", help="Target post or comment object ID")
    comments.add_argument("--post-id", help="Target post ID")
    comments.add_argument(
        "--fields",
        default="id,message,created_time,from,comment_count,like_count,can_comment,is_hidden",
        help="Comma-separated fields to request",
    )
    comments.add_argument("--limit", type=int, default=25, help="Comments page size")
    comments.add_argument("--after", help="Pagination cursor")
    comments.add_argument("--before", help="Pagination cursor")

    comment_create = subparsers.add_parser("comment-create", help="Create a comment")
    comment_create.add_argument("--object-id", required=True, help="Target post or comment object ID")
    comment_create.add_argument("--message", required=True, help="Comment text")

    comment_update = subparsers.add_parser("comment-update", help="Edit or hide a comment")
    comment_update.add_argument("--comment-id", required=True, help="Comment ID")
    comment_update.add_argument("--message", help="Updated comment text")
    visibility = comment_update.add_mutually_exclusive_group()
    visibility.add_argument("--hide", dest="hide", action="store_const", const=True, help="Hide the comment")
    visibility.add_argument("--unhide", dest="hide", action="store_const", const=False, help="Unhide the comment")
    comment_update.set_defaults(hide=None)

    comment_delete = subparsers.add_parser("comment-delete", help="Delete a comment")
    comment_delete.add_argument("--comment-id", required=True, help="Comment ID")

    insights = subparsers.add_parser("insights", help="Read Page insights")
    insights.add_argument(
        "--metrics",
        default="page_impressions,page_fans",
        help="Comma-separated insight metrics",
    )
    insights.add_argument("--period", default="day", help="Insight period")
    insights.add_argument("--since", help="Inclusive start date")
    insights.add_argument("--until", help="Inclusive end date")

    post_insights = subparsers.add_parser("post-insights", help="Read post insights")
    post_insights.add_argument("--post-id", help="Page post ID")
    post_insights.add_argument("--object-id", help="Target object ID")
    post_insights.add_argument(
        "--metrics",
        default="post_impressions,post_impressions_unique,post_engaged_users",
        help="Comma-separated insight metrics",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "post-insights" and not args.post_id and not args.object_id:
        print("Error: post-insights requires --post-id or --object-id.", file=sys.stderr)
        sys.exit(1)

    config = load_config(resolve_config_path(args.config))
    settings = resolve_settings(args, config)
    client = FacebookPagesClient(settings)

    command_map = {
        "connect": client.connect,
        "list-connections": client.list_connections,
        "list-accounts": client.list_accounts,
        "publish-post": lambda: client.publish_post(args),
        "publish-photo": lambda: client.publish_photo(args),
        "publish-video": lambda: client.publish_video(args),
        "feed": lambda: client.feed(args),
        "comments": lambda: client.comments(args),
        "comment-create": lambda: client.comment_create(args),
        "comment-update": lambda: client.comment_update(args),
        "comment-delete": lambda: client.comment_delete(args),
        "insights": lambda: client.insights(args),
        "post-insights": lambda: client.post_insights(args),
    }

    result = command_map[args.command]()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
