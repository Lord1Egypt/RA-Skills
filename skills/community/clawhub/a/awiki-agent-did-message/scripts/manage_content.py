"""Manage Content Pages (create, update, rename, delete, list, get).

Publish custom Markdown documents (job postings, event pages, etc.)
accessible via https://{handle}.{domain}/content/{slug}.md.

Usage:
    # Create a content page
    python scripts/manage_content.py --create --slug jd --title "Job Description" --body "# We are hiring\n\n..."

    # Create a draft page
    python scripts/manage_content.py --create --slug draft-post --title "Draft" --body "WIP" --visibility draft

    # List all content pages
    python scripts/manage_content.py --list

    # Get a specific content page
    python scripts/manage_content.py --get --slug jd

    # Update a content page
    python scripts/manage_content.py --update --slug jd --title "Updated Title" --body "New content"

    # Change visibility
    python scripts/manage_content.py --update --slug jd --visibility public

    # Rename a slug
    python scripts/manage_content.py --rename --slug jd --new-slug hiring

    # Delete a content page
    python scripts/manage_content.py --delete --slug jd

    # Read body from a file
    python scripts/manage_content.py --create --slug event --title "Event" --body-file ./event.md

[INPUT]: SDK (authenticated_rpc_call), credential_store (load identity credentials),
         logging_config
[OUTPUT]: Content page CRUD operations results with structured JSON errors
[POS]: Content Pages management script

[PROTOCOL]:
1. Update this header when logic changes
2. Check the folder's CLAUDE.md after updating
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

from utils import (
    SDKConfig,
    JsonRpcError,
    create_user_service_client,
    authenticated_rpc_call,
)
from utils.logging_config import configure_logging
from credential_store import create_authenticator


CONTENT_RPC = "/content/rpc"
logger = logging.getLogger(__name__)


async def create_page(
    credential_name: str,
    slug: str,
    title: str,
    body: str,
    visibility: str = "public",
) -> None:
    """Create a content page."""
    logger.info("Creating content page credential=%s slug=%s visibility=%s", credential_name, slug, visibility)
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(json.dumps({
            "status": "error",
            "error": f"Credential '{credential_name}' unavailable",
            "hint": "Create an identity first with setup_identity.py or register_handle.py",
        }))
        sys.exit(1)

    auth, _ = auth_result
    params = {
        "slug": slug,
        "title": title,
        "body": body,
        "visibility": visibility,
    }

    async with create_user_service_client(config) as client:
        result = await authenticated_rpc_call(
            client, CONTENT_RPC, "create", params,
            auth=auth, credential_name=credential_name,
        )
        print(json.dumps({
            "status": "ok",
            "action": "created",
            "page": result,
        }, indent=2, ensure_ascii=False))


async def update_page(
    credential_name: str,
    slug: str,
    title: str | None = None,
    body: str | None = None,
    visibility: str | None = None,
) -> None:
    """Update a content page."""
    logger.info("Updating content page credential=%s slug=%s", credential_name, slug)
    params: dict = {"slug": slug}
    if title is not None:
        params["title"] = title
    if body is not None:
        params["body"] = body
    if visibility is not None:
        params["visibility"] = visibility

    if len(params) <= 1:
        print(json.dumps({
            "status": "error",
            "error": "No fields to update",
            "hint": "Specify --title, --body, --visibility, or --body-file",
        }))
        sys.exit(1)

    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(json.dumps({
            "status": "error",
            "error": f"Credential '{credential_name}' unavailable",
            "hint": "Create an identity first",
        }))
        sys.exit(1)

    auth, _ = auth_result
    async with create_user_service_client(config) as client:
        result = await authenticated_rpc_call(
            client, CONTENT_RPC, "update", params,
            auth=auth, credential_name=credential_name,
        )
        print(json.dumps({
            "status": "ok",
            "action": "updated",
            "page": result,
        }, indent=2, ensure_ascii=False))


async def rename_page(
    credential_name: str,
    old_slug: str,
    new_slug: str,
) -> None:
    """Rename a content page slug."""
    logger.info("Renaming content page credential=%s old_slug=%s new_slug=%s", credential_name, old_slug, new_slug)
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(json.dumps({
            "status": "error",
            "error": f"Credential '{credential_name}' unavailable",
            "hint": "Create an identity first",
        }))
        sys.exit(1)

    auth, _ = auth_result
    params = {"old_slug": old_slug, "new_slug": new_slug}

    async with create_user_service_client(config) as client:
        result = await authenticated_rpc_call(
            client, CONTENT_RPC, "rename", params,
            auth=auth, credential_name=credential_name,
        )
        print(json.dumps({
            "status": "ok",
            "action": "renamed",
            "page": result,
        }, indent=2, ensure_ascii=False))


async def delete_page(credential_name: str, slug: str) -> None:
    """Delete a content page."""
    logger.info("Deleting content page credential=%s slug=%s", credential_name, slug)
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(json.dumps({
            "status": "error",
            "error": f"Credential '{credential_name}' unavailable",
            "hint": "Create an identity first",
        }))
        sys.exit(1)

    auth, _ = auth_result
    async with create_user_service_client(config) as client:
        result = await authenticated_rpc_call(
            client, CONTENT_RPC, "delete", {"slug": slug},
            auth=auth, credential_name=credential_name,
        )
        print(json.dumps({
            "status": "ok",
            "action": "deleted",
            "result": result,
        }, indent=2, ensure_ascii=False))


async def list_pages(credential_name: str) -> None:
    """List all content pages for the current Handle."""
    logger.info("Listing content pages credential=%s", credential_name)
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(json.dumps({
            "status": "error",
            "error": f"Credential '{credential_name}' unavailable",
            "hint": "Create an identity first",
        }))
        sys.exit(1)

    auth, _ = auth_result
    async with create_user_service_client(config) as client:
        result = await authenticated_rpc_call(
            client, CONTENT_RPC, "list", {},
            auth=auth, credential_name=credential_name,
        )
        print(json.dumps({
            "status": "ok",
            "action": "list",
            "pages": result.get("pages", []),
            "count": result.get("count", 0),
        }, indent=2, ensure_ascii=False))


async def get_page(credential_name: str, slug: str) -> None:
    """Get a specific content page with full body."""
    logger.info("Fetching content page credential=%s slug=%s", credential_name, slug)
    config = SDKConfig()
    auth_result = create_authenticator(credential_name, config)
    if auth_result is None:
        print(json.dumps({
            "status": "error",
            "error": f"Credential '{credential_name}' unavailable",
            "hint": "Create an identity first",
        }))
        sys.exit(1)

    auth, _ = auth_result
    async with create_user_service_client(config) as client:
        result = await authenticated_rpc_call(
            client, CONTENT_RPC, "get", {"slug": slug},
            auth=auth, credential_name=credential_name,
        )
        print(json.dumps({
            "status": "ok",
            "action": "get",
            "page": result,
        }, indent=2, ensure_ascii=False))


def main() -> None:
    configure_logging(console_level=None, mirror_stdio=True)

    parser = argparse.ArgumentParser(description="Manage Content Pages")

    # Action group
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--create", action="store_true", help="Create a content page")
    action.add_argument("--update", action="store_true", help="Update a content page")
    action.add_argument("--rename", action="store_true", help="Rename a content page slug")
    action.add_argument("--delete", action="store_true", help="Delete a content page")
    action.add_argument("--list", action="store_true", help="List all content pages")
    action.add_argument("--get", action="store_true", help="Get a content page")

    # Common params
    parser.add_argument("--slug", type=str, help="Page slug (URL identifier)")
    parser.add_argument("--title", type=str, help="Page title")
    parser.add_argument("--body", type=str, help="Page body (Markdown content)")
    parser.add_argument("--body-file", type=str, help="Read body from a file")
    parser.add_argument("--visibility", type=str, choices=["public", "draft", "unlisted"],
                        help="Page visibility (default: public)")
    parser.add_argument("--new-slug", type=str, help="New slug for rename")
    parser.add_argument("--credential", type=str, default="default",
                        help="Credential name (default: default)")

    args = parser.parse_args()
    logger.info("manage_content CLI started credential=%s", args.credential)

    # Read body from file if specified
    body = args.body
    if args.body_file:
        body_path = Path(args.body_file)
        if not body_path.exists():
            print(json.dumps({
                "status": "error",
                "error": f"File not found: {args.body_file}",
                "hint": "Check the file path",
            }))
            sys.exit(1)
        body = body_path.read_text(encoding="utf-8")

    try:
        if args.create:
            if not args.slug or not args.title:
                parser.error("--create requires --slug and --title")
            asyncio.run(create_page(
                credential_name=args.credential,
                slug=args.slug,
                title=args.title,
                body=body or "",
                visibility=args.visibility or "public",
            ))

        elif args.update:
            if not args.slug:
                parser.error("--update requires --slug")
            asyncio.run(update_page(
                credential_name=args.credential,
                slug=args.slug,
                title=args.title,
                body=body,
                visibility=args.visibility,
            ))

        elif args.rename:
            if not args.slug or not args.new_slug:
                parser.error("--rename requires --slug and --new-slug")
            asyncio.run(rename_page(
                credential_name=args.credential,
                old_slug=args.slug,
                new_slug=args.new_slug,
            ))

        elif args.delete:
            if not args.slug:
                parser.error("--delete requires --slug")
            asyncio.run(delete_page(args.credential, args.slug))

        elif args.list:
            asyncio.run(list_pages(args.credential))

        elif args.get:
            if not args.slug:
                parser.error("--get requires --slug")
            asyncio.run(get_page(args.credential, args.slug))
    except JsonRpcError as exc:
        print(json.dumps({
            "status": "error",
            "error_type": "jsonrpc",
            "code": exc.code,
            "message": exc.message,
            "data": exc.data,
        }, indent=2, ensure_ascii=False))
        raise SystemExit(1) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("manage_content CLI failed")
        print(json.dumps({
            "status": "error",
            "error_type": type(exc).__name__,
            "message": str(exc),
        }, indent=2, ensure_ascii=False))
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
