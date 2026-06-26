"""
MCP tool implementations for the Facebook Page Publisher skill.

Each function accepts primitive arguments, calls the FacebookClient,
and returns a human-readable formatted string for the AI agent.
"""

from __future__ import annotations

from datetime import datetime
from .fb_client import FacebookClient, FacebookAPIError


def _format_error(exc: Exception) -> str:
    if isinstance(exc, FacebookAPIError):
        parts = [f"Facebook API Error: {exc}"]
        if exc.error_code:
            parts.append(f"Error code: {exc.error_code}")
        if exc.error_subcode:
            parts.append(f"Error subcode: {exc.error_subcode}")
        return "\n".join(parts)
    if isinstance(exc, ValueError):
        return f"Validation Error: {exc}"
    return f"Unexpected Error: {type(exc).__name__}: {exc}"


def _format_datetime(iso_string: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        return dt.strftime("%B %d, %Y at %I:%M %p %Z")
    except Exception:
        return iso_string


def _truncate(text: str, max_length: int = 120) -> str:
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


async def create_post(client: FacebookClient, message: str) -> str:
    try:
        result = await client.create_post(message)
        post_id = result.get("id", "unknown")
        return (
            f"Post published successfully!\n"
            f"Post ID: {post_id}\n"
            f"URL: https://www.facebook.com/{post_id.replace('_', '/posts/')}\n"
            f"Content: {_truncate(message)}"
        )
    except Exception as exc:
        return _format_error(exc)


async def upload_photo_post(
    client: FacebookClient,
    photo_url: str,
    caption: str | None = None,
) -> str:
    try:
        result = await client.upload_photo(photo_url, caption)
        photo_id = result.get("id", "unknown")
        post_id = result.get("post_id", "unknown")
        lines = [
            "Photo uploaded successfully!",
            f"Photo ID: {photo_id}",
            f"Post ID: {post_id}",
            f"Image URL: {photo_url}",
        ]
        if caption:
            lines.append(f"Caption: {_truncate(caption)}")
        return "\n".join(lines)
    except Exception as exc:
        return _format_error(exc)


async def schedule_post(
    client: FacebookClient,
    message: str,
    scheduled_time: str,
) -> str:
    try:
        result = await client.schedule_post(message, scheduled_time)
        post_id = result.get("id", "unknown")
        return (
            f"Post scheduled successfully!\n"
            f"Post ID: {post_id}\n"
            f"Scheduled for: {_format_datetime(scheduled_time)}\n"
            f"Content: {_truncate(message)}\n"
            f"Note: Manage scheduled posts from your Facebook Page's Publishing Tools."
        )
    except Exception as exc:
        return _format_error(exc)


async def get_page_insights(
    client: FacebookClient,
    metric: str = "all",
    period: str = "day",
) -> str:
    try:
        result = await client.get_insights(metric, period)
        data = result.get("data", [])

        if not data:
            return f"No insight data available for metric='{metric}', period='{period}'."

        period_labels = {"day": "Daily", "week": "Weekly", "days_28": "28-Day"}
        period_label = period_labels.get(period, period)

        lines = [f"Facebook Page Insights ({period_label})", "=" * 45]

        for item in data:
            name = item.get("title", item.get("name", "Unknown Metric"))
            description = item.get("description", "")
            values = item.get("values", [])

            lines.append(f"\n{name}")
            if description:
                lines.append(f"  {description}")

            if values:
                latest = values[-1]
                value = latest.get("value", "N/A")
                end_time = latest.get("end_time", "")
                if end_time:
                    lines.append(f"  Value: {value} (as of {_format_datetime(end_time)})")
                else:
                    lines.append(f"  Value: {value}")

                if len(values) >= 2:
                    prev_value = values[-2].get("value", 0)
                    curr_value = latest.get("value", 0)
                    if isinstance(prev_value, (int, float)) and isinstance(curr_value, (int, float)):
                        if prev_value > 0:
                            change_pct = ((curr_value - prev_value) / prev_value) * 100
                            direction = "up" if change_pct > 0 else "down" if change_pct < 0 else "flat"
                            lines.append(f"  Trend: {direction} {abs(change_pct):.1f}% from previous period")

        return "\n".join(lines)
    except Exception as exc:
        return _format_error(exc)


async def get_recent_posts(client: FacebookClient, limit: int = 10) -> str:
    try:
        result = await client.get_posts(limit)
        posts = result.get("data", [])

        if not posts:
            return "No posts found on this Page."

        lines = [f"Recent Facebook Page Posts (showing {len(posts)})", "=" * 50]

        for i, post in enumerate(posts, 1):
            post_id = post.get("id", "unknown")
            message = post.get("message", "(no text)")
            created = post.get("created_time", "unknown")
            permalink = post.get("permalink_url", "")

            likes_count = post.get("likes", {}).get("summary", {}).get("total_count", 0)
            comments_count = post.get("comments", {}).get("summary", {}).get("total_count", 0)
            shares_count = post.get("shares", {}).get("count", 0)

            lines.append(f"\n--- Post #{i} ---")
            lines.append(f"ID: {post_id}")
            lines.append(f"Date: {_format_datetime(created)}")
            lines.append(f"Text: {_truncate(message, 200)}")
            lines.append(f"Likes: {likes_count} | Comments: {comments_count} | Shares: {shares_count}")
            if permalink:
                lines.append(f"Link: {permalink}")

        return "\n".join(lines)
    except Exception as exc:
        return _format_error(exc)


async def delete_post(client: FacebookClient, post_id: str) -> str:
    try:
        result = await client.delete_post(post_id)
        if result.get("success", False):
            return f"Post {post_id} has been deleted successfully."
        return f"Deletion request sent for post {post_id}, but API did not confirm success. Response: {result}"
    except Exception as exc:
        return _format_error(exc)


async def get_post_comments(
    client: FacebookClient,
    post_id: str,
    limit: int = 25,
) -> str:
    try:
        result = await client.get_comments(post_id, limit)
        comments = result.get("data", [])

        if not comments:
            return f"No comments found on post {post_id}."

        lines = [
            f"Comments on post {post_id} (showing {len(comments)})",
            "=" * 50,
        ]

        for i, comment in enumerate(comments, 1):
            comment_id = comment.get("id", "unknown")
            author = comment.get("from", {}).get("name", "Unknown User")
            message = comment.get("message", "(empty)")
            created = comment.get("created_time", "unknown")
            like_count = comment.get("like_count", 0)

            lines.append(f"\n--- Comment #{i} ---")
            lines.append(f"ID: {comment_id}")
            lines.append(f"Author: {author}")
            lines.append(f"Date: {_format_datetime(created)}")
            lines.append(f"Message: {message}")
            lines.append(f"Likes: {like_count}")

        return "\n".join(lines)
    except Exception as exc:
        return _format_error(exc)


async def reply_to_comment(
    client: FacebookClient,
    comment_id: str,
    message: str,
) -> str:
    try:
        result = await client.reply_comment(comment_id, message)
        reply_id = result.get("id", "unknown")
        return (
            f"Reply posted successfully!\n"
            f"Reply ID: {reply_id}\n"
            f"In response to comment: {comment_id}\n"
            f"Reply text: {_truncate(message)}"
        )
    except Exception as exc:
        return _format_error(exc)
