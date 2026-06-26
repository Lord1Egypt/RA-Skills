"""
Facebook Graph API client for Page management.

Handles all HTTP communication with the Facebook Graph API v21.0.
Every public method returns a dict on success or raises FacebookAPIError on failure.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

import httpx

logger = logging.getLogger("fb-page-publisher")

BASE_URL = "https://graph.facebook.com/v21.0"

PAGE_INSIGHT_METRICS = {
    "impressions": "page_impressions",
    "reach": "page_impressions_unique",
    "engagement": "page_post_engagements",
    "views": "page_views_total",
}

POST_FIELDS = (
    "id,message,created_time,permalink_url,"
    "shares,likes.limit(0).summary(true),"
    "comments.limit(0).summary(true)"
)

COMMENT_FIELDS = "id,from,message,created_time,like_count"


class FacebookAPIError(Exception):
    """Raised when the Facebook Graph API returns an error response."""

    def __init__(self, message: str, error_code: int | None = None, error_subcode: int | None = None):
        self.error_code = error_code
        self.error_subcode = error_subcode
        super().__init__(message)


class FacebookClient:
    """HTTP client wrapping the Facebook Graph API v21.0."""

    def __init__(self, page_id: str, access_token: str) -> None:
        if not page_id or not page_id.strip():
            raise ValueError("page_id must be a non-empty string")
        if not access_token or not access_token.strip():
            raise ValueError("access_token must be a non-empty string")

        self.page_id = page_id.strip()
        self.access_token = access_token.strip()
        self._client = httpx.AsyncClient(
            base_url=BASE_URL,
            timeout=httpx.Timeout(30.0, connect=10.0),
            headers={"User-Agent": "fb-page-publisher/1.0.0"},
        )

    def _auth_params(self) -> dict[str, str]:
        return {"access_token": self.access_token}

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        merged_params = {**self._auth_params(), **(params or {})}

        response = await self._client.request(
            method,
            endpoint,
            params=merged_params,
            data=data,
        )

        try:
            body = response.json()
        except Exception:
            response.raise_for_status()
            return {}

        if "error" in body:
            err = body["error"]
            raise FacebookAPIError(
                message=err.get("message", "Unknown Facebook API error"),
                error_code=err.get("code"),
                error_subcode=err.get("error_subcode"),
            )

        response.raise_for_status()
        return body

    # -- Posts --

    async def create_post(self, message: str) -> dict[str, Any]:
        if not message or not message.strip():
            raise ValueError("message must be a non-empty string")

        result = await self._request(
            "POST",
            f"/{self.page_id}/feed",
            data={"message": message.strip()},
        )
        logger.info("Created post %s", result.get("id"))
        return result

    async def upload_photo(self, photo_url: str, caption: str | None = None) -> dict[str, Any]:
        if not photo_url or not photo_url.strip():
            raise ValueError("photo_url must be a non-empty string")

        payload: dict[str, str] = {"url": photo_url.strip()}
        if caption and caption.strip():
            payload["caption"] = caption.strip()

        result = await self._request(
            "POST",
            f"/{self.page_id}/photos",
            data=payload,
        )
        logger.info("Uploaded photo %s (post %s)", result.get("id"), result.get("post_id"))
        return result

    async def schedule_post(self, message: str, scheduled_time: str) -> dict[str, Any]:
        if not message or not message.strip():
            raise ValueError("message must be a non-empty string")

        try:
            dt = datetime.fromisoformat(scheduled_time)
        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"Invalid datetime format: '{scheduled_time}'. "
                "Use ISO 8601 format, e.g. '2026-03-10T09:00:00'."
            ) from exc

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        diff_seconds = (dt - now).total_seconds()

        if diff_seconds < 600:
            raise ValueError(
                "Scheduled time must be at least 10 minutes in the future. "
                f"Provided: {scheduled_time}"
            )

        if diff_seconds > 15_552_000:
            raise ValueError(
                "Scheduled time must be within 6 months from now. "
                f"Provided: {scheduled_time}"
            )

        unix_timestamp = int(dt.timestamp())

        result = await self._request(
            "POST",
            f"/{self.page_id}/feed",
            data={
                "message": message.strip(),
                "published": "false",
                "scheduled_publish_time": str(unix_timestamp),
            },
        )
        logger.info("Scheduled post %s for %s", result.get("id"), scheduled_time)
        return result

    # -- Insights --

    async def get_insights(self, metric: str = "all", period: str = "day") -> dict[str, Any]:
        valid_periods = {"day", "week", "days_28"}
        if period not in valid_periods:
            raise ValueError(f"period must be one of {valid_periods}, got '{period}'")

        if metric == "all":
            metric_names = ",".join(PAGE_INSIGHT_METRICS.values())
        elif metric in PAGE_INSIGHT_METRICS:
            metric_names = PAGE_INSIGHT_METRICS[metric]
        else:
            raise ValueError(
                f"metric must be one of {list(PAGE_INSIGHT_METRICS.keys())} or 'all', "
                f"got '{metric}'"
            )

        return await self._request(
            "GET",
            f"/{self.page_id}/insights",
            params={"metric": metric_names, "period": period},
        )

    # -- Read Posts --

    async def get_posts(self, limit: int = 10) -> dict[str, Any]:
        limit = max(1, min(100, limit))
        return await self._request(
            "GET",
            f"/{self.page_id}/posts",
            params={"fields": POST_FIELDS, "limit": str(limit)},
        )

    # -- Delete --

    async def delete_post(self, post_id: str) -> dict[str, Any]:
        if not post_id or not post_id.strip():
            raise ValueError("post_id must be a non-empty string")

        result = await self._request("DELETE", f"/{post_id.strip()}")
        logger.info("Deleted post %s", post_id)
        return result

    # -- Comments --

    async def get_comments(self, post_id: str, limit: int = 25) -> dict[str, Any]:
        if not post_id or not post_id.strip():
            raise ValueError("post_id must be a non-empty string")

        limit = max(1, min(100, limit))
        return await self._request(
            "GET",
            f"/{post_id.strip()}/comments",
            params={"fields": COMMENT_FIELDS, "limit": str(limit)},
        )

    async def reply_comment(self, comment_id: str, message: str) -> dict[str, Any]:
        if not comment_id or not comment_id.strip():
            raise ValueError("comment_id must be a non-empty string")
        if not message or not message.strip():
            raise ValueError("message must be a non-empty string")

        result = await self._request(
            "POST",
            f"/{comment_id.strip()}/comments",
            data={"message": message.strip()},
        )
        logger.info("Replied to comment %s with comment %s", comment_id, result.get("id"))
        return result

    # -- Lifecycle --

    async def close(self) -> None:
        await self._client.aclose()
