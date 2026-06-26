"""
FastMCP server for the Facebook Page Publisher skill.

Usage:
    uv run src/server.py
"""

from __future__ import annotations

import logging
import os
import sys

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from .fb_client import FacebookClient
from . import tools as tool_handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("fb-page-publisher")

load_dotenv()

FB_PAGE_ID = os.environ.get("FB_PAGE_ID", "")
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN", "")

if not FB_PAGE_ID:
    logger.error("FB_PAGE_ID environment variable is not set.")
    sys.exit(1)

if not FB_ACCESS_TOKEN:
    logger.error("FB_ACCESS_TOKEN environment variable is not set.")
    sys.exit(1)

fb_client = FacebookClient(page_id=FB_PAGE_ID, access_token=FB_ACCESS_TOKEN)

mcp = FastMCP("Facebook Page Publisher")


@mcp.tool()
async def create_post(message: str) -> str:
    """
    Create and immediately publish a text post to the Facebook Page.

    Args:
        message: The text content of the post to publish.
    """
    return await tool_handlers.create_post(fb_client, message)


@mcp.tool()
async def upload_photo_post(photo_url: str, caption: str = "") -> str:
    """
    Upload a photo to the Facebook Page with an optional caption.
    The photo must be a publicly accessible URL (https://).

    Args:
        photo_url: A publicly accessible URL pointing to the image file (JPEG, PNG, etc.).
        caption: Optional text caption to accompany the photo.
    """
    return await tool_handlers.upload_photo_post(
        fb_client, photo_url, caption if caption else None
    )


@mcp.tool()
async def schedule_post(message: str, scheduled_time: str) -> str:
    """
    Schedule a text post for future publication on the Facebook Page.
    The time must be at least 10 minutes in the future and at most 6 months ahead.

    Args:
        message: The text content of the post.
        scheduled_time: When to publish, in ISO 8601 format (e.g., '2026-03-10T09:00:00').
    """
    return await tool_handlers.schedule_post(fb_client, message, scheduled_time)


@mcp.tool()
async def get_page_insights(metric: str = "all", period: str = "day") -> str:
    """
    Retrieve engagement metrics (impressions, reach, engagement, views) for the Facebook Page.

    Args:
        metric: The metric to retrieve -- 'impressions', 'reach', 'engagement', 'views', or 'all'.
        period: Time aggregation period -- 'day', 'week', or 'days_28'.
    """
    return await tool_handlers.get_page_insights(fb_client, metric, period)


@mcp.tool()
async def get_recent_posts(limit: int = 10) -> str:
    """
    Fetch the most recent posts from the Facebook Page with engagement statistics
    (likes, comments, shares).

    Args:
        limit: Number of posts to retrieve, between 1 and 100. Defaults to 10.
    """
    return await tool_handlers.get_recent_posts(fb_client, limit)


@mcp.tool()
async def delete_post(post_id: str) -> str:
    """
    Delete a specific post from the Facebook Page. This action is irreversible.

    Args:
        post_id: The full post ID in the format 'pageId_postId' (e.g., '123456789_987654321').
    """
    return await tool_handlers.delete_post(fb_client, post_id)


@mcp.tool()
async def get_post_comments(post_id: str, limit: int = 25) -> str:
    """
    Retrieve comments on a specific Facebook Page post.

    Args:
        post_id: The full post ID in the format 'pageId_postId'.
        limit: Number of comments to retrieve, between 1 and 100. Defaults to 25.
    """
    return await tool_handlers.get_post_comments(fb_client, post_id, limit)


@mcp.tool()
async def reply_to_comment(comment_id: str, message: str) -> str:
    """
    Reply to a comment on a Facebook Page post, posting as the Page itself.

    Args:
        comment_id: The ID of the comment to reply to.
        message: The reply message text.
    """
    return await tool_handlers.reply_to_comment(fb_client, comment_id, message)


def main() -> None:
    """Run the MCP server over stdio."""
    logger.info("Starting Facebook Page Publisher MCP server...")
    logger.info("Page ID: %s", FB_PAGE_ID[:6] + "..." if len(FB_PAGE_ID) > 6 else FB_PAGE_ID)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
