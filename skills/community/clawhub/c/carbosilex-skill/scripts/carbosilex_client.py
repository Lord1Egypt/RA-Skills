#!/usr/bin/env python3
"""
CarboSilex137 Platform CLI Client for OpenClaw Agents.

A comprehensive CLI tool that enables AI agents to interact with the
CarboSilex137 decentralized freelance marketplace API.

Usage:
    python carbosilex_client.py <command> [options]

Environment Variables:
    CARBOSILEX_API_URL: Base URL for the CarboSilex API (default: https://api.carbosilex137.com/api/v1)
    CARBOSILEX_API_KEY: API key (sent as X-API-Key) for authenticated endpoints

Examples:
    python carbosilex_client.py list-jobs --category CODE --min-budget 500
    python carbosilex_client.py job-feed --skills "python,solidity"
    python carbosilex_client.py submit-proposal --job-id <uuid> --cover-letter "..."
"""

import argparse
import json
import os
import sys
from typing import Any, Optional
from urllib.parse import urljoin

try:
    import httpx
except ImportError:
    # Minimal urllib-based shim so this client runs where httpx is absent
    # (e.g. the OpenClaw agent container, which ships only the stdlib). It
    # implements just the surface this script uses: Client.get/post (with
    # params/json/headers), a response with status_code/json()/text/
    # raise_for_status(), and HTTPStatusError carrying .response.
    import json as _json
    import urllib.error as _ue
    import urllib.request as _ur
    from urllib.parse import urlencode

    class _ShimResponse:
        def __init__(self, status_code, body, url):
            self.status_code = status_code
            self._body = body
            self.text = (body or b"").decode("utf-8", "replace")
            self.url = url

        def json(self):
            return _json.loads(self._body or b"{}")

        def raise_for_status(self):
            if self.status_code >= 400:
                raise httpx.HTTPStatusError(
                    f"HTTP {self.status_code}", response=self
                )

    class _ShimClient:
        def __init__(self, timeout=30):
            self.timeout = timeout

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def _send(self, method, url, headers=None, json=None, params=None):
            if params:
                clean = {k: v for k, v in params.items() if v is not None}
                if clean:
                    url += ("&" if "?" in url else "?") + urlencode(clean, doseq=True)
            data = _json.dumps(json).encode("utf-8") if json is not None else None
            req = _ur.Request(url, data=data, headers=headers or {}, method=method)
            try:
                with _ur.urlopen(req, timeout=self.timeout) as r:
                    return _ShimResponse(r.getcode(), r.read(), url)
            except _ue.HTTPError as e:
                return _ShimResponse(e.code, e.read(), url)

        def get(self, url, headers=None, params=None):
            return self._send("GET", url, headers=headers, params=params)

        def post(self, url, headers=None, json=None, params=None):
            return self._send("POST", url, headers=headers, json=json, params=params)

        def patch(self, url, headers=None, json=None, params=None):
            return self._send("PATCH", url, headers=headers, json=json, params=params)

    class httpx:  # noqa: N801 - stand-in for the httpx module
        Client = _ShimClient
        Response = _ShimResponse

        class HTTPStatusError(Exception):
            def __init__(self, message, response=None):
                super().__init__(message)
                self.response = response


class CarbosilexClient:
    """Client for the CarboSilex137 API.

    Provides methods for all major platform operations including
    job browsing, proposal submission, delivery management, and
    escrow status checking.

    Attributes:
        base_url: The base URL for the CarboSilex API.
        api_key: API key (sent as X-API-Key) for authenticated requests.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        """Initialize the CarboSilex client.

        Args:
            base_url: API base URL. Falls back to CARBOSILEX_API_URL env var.
            api_key: API key. Falls back to CARBOSILEX_API_KEY env var.

        Raises:
            ValueError: If no API URL is configured.
        """
        self.base_url = (
            base_url
            or os.getenv("CARBOSILEX_API_URL")
            or "https://api.carbosilex137.com/api/v1"
        )
        self.api_key = api_key or os.getenv("CARBOSILEX_API_KEY")
        if not self.api_key:
            # Per-agent fallback: read api_key.txt next to this script. Lets
            # several isolated agents share one container env yet act under
            # distinct identities (each workspace copy holds its own key file).
            try:
                _kf = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)), "api_key.txt"
                )
                if os.path.isfile(_kf):
                    with open(_kf, encoding="utf-8") as fh:
                        self.api_key = fh.read().strip() or None
            except Exception:
                pass

        if not self.base_url:
            raise ValueError(
                "CARBOSILEX_API_URL environment variable is not set. "
                "Set it to the CarboSilex API base URL, e.g.: "
                "https://api.carbosilex137.com/api/v1"
            )

    @property
    def _headers(self) -> dict[str, str]:
        """Build request headers with optional authentication."""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        return headers

    def _url(self, path: str) -> str:
        """Build full URL from path.

        Args:
            path: API endpoint path (e.g., '/jobs').

        Returns:
            Full URL string.
        """
        return f"{self.base_url.rstrip('/')}{path}"

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Process API response and handle errors.

        Args:
            response: The httpx Response object.

        Returns:
            Parsed JSON response as a dictionary.

        Raises:
            SystemExit: On HTTP errors with descriptive messages.
        """
        try:
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            try:
                detail = e.response.json().get("detail", str(e))
            except Exception:
                detail = e.response.text[:500]

            error_messages = {
                401: f"Authentication failed. Check your CARBOSILEX_API_KEY. Detail: {detail}",
                403: f"Permission denied. You don't have access to this resource. Detail: {detail}",
                404: f"Resource not found. Detail: {detail}",
                422: f"Validation error. Check your input parameters. Detail: {detail}",
                429: f"Rate limit exceeded. Wait and retry. Detail: {detail}",
                500: f"CarboSilex server error. The service may be temporarily unavailable. Detail: {detail}",
                503: f"CarboSilex service is currently unavailable. Try again later. Detail: {detail}",
            }

            message = error_messages.get(
                status,
                f"API error (HTTP {status}): {detail}",
            )
            print(f"❌ {message}", file=sys.stderr)
            sys.exit(1)

    # ============== Jobs ==============

    def list_jobs(
        self,
        category: Optional[str] = None,
        min_budget: Optional[float] = None,
        max_budget: Optional[float] = None,
        skills: Optional[str] = None,
        allow_agents: Optional[bool] = None,
        payment_type: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> dict[str, Any]:
        """List open jobs with optional filters.

        Args:
            category: Filter by category (CODE, DESIGN, WRITING, DATA, RESEARCH, AUDIT, OTHER).
            min_budget: Minimum budget in USDC.
            max_budget: Maximum budget in USDC.
            skills: Comma-separated skill tags to filter by.
            allow_agents: If True, only show jobs that accept AI agents.
            payment_type: Filter by FIXED or HOURLY.
            search: Full-text search query.
            page: Page number (1-indexed).
            per_page: Results per page (max 100).

        Returns:
            Dict with 'items', 'total', 'page', 'per_page', 'pages' keys.
        """
        params = {"page": page, "per_page": per_page}
        if category:
            params["category"] = category
        if min_budget is not None:
            params["min_budget"] = min_budget
        if max_budget is not None:
            params["max_budget"] = max_budget
        if skills:
            params["skills"] = skills
        if allow_agents is not None:
            params["allow_agents"] = allow_agents
        if payment_type:
            params["payment_type"] = payment_type
        if search:
            params["search"] = search

        # Route has a trailing slash: the bare "/jobs" 307-redirects to "/jobs/"
        # (and httpx does not follow redirects by default, so the bare path fails).
        with httpx.Client(timeout=30) as client:
            resp = client.get(self._url("/jobs/"), params=params, headers=self._headers)
        return self._handle_response(resp)

    def get_job(self, job_id: str) -> dict[str, Any]:
        """Get detailed information about a specific job.

        Args:
            job_id: UUID of the job.

        Returns:
            Complete job details including owner, budget, skills, and escrow status.
        """
        with httpx.Client(timeout=30) as client:
            resp = client.get(self._url(f"/jobs/{job_id}"), headers=self._headers)
        return self._handle_response(resp)

    def get_job_feed(
        self,
        skills: Optional[str] = None,
        min_budget: Optional[float] = None,
        limit: int = 50,
    ) -> dict[str, Any]:
        """Get agent-optimized job feed.

        Returns a simplified JSON feed designed for AI agents.

        Args:
            skills: Comma-separated skills to match against.
            min_budget: Minimum budget in USDC.
            limit: Maximum results (1-100).

        Returns:
            Dict with 'jobs', 'total', 'timestamp' keys.
        """
        params = {"limit": limit}
        if skills:
            params["skills"] = skills
        if min_budget is not None:
            params["min_budget"] = min_budget

        with httpx.Client(timeout=30) as client:
            resp = client.get(
                self._url("/jobs/feed"), params=params, headers=self._headers,
            )
        return self._handle_response(resp)

    # ============== Proposals ==============

    def submit_proposal(
        self,
        job_id: str,
        cover_letter: str,
        proposed_amount: float,
        estimated_hours: Optional[int] = None,
    ) -> dict[str, Any]:
        """Submit a proposal (bid) for a job.

        Args:
            job_id: UUID of the job to apply for.
            cover_letter: Cover letter explaining why you're the right fit.
                Must be at least 50 characters.
            proposed_amount: Your proposed price in USDC.
            estimated_hours: Estimated hours to complete the work.

        Returns:
            Created proposal details.

        Raises:
            SystemExit: If not authenticated or validation fails.
        """
        if not self.api_key:
            print("❌ Authentication required. Set CARBOSILEX_API_KEY.", file=sys.stderr)
            sys.exit(1)
        if estimated_hours is None:
            print(
                "❌ --estimated-hours is required (maps to delivery_hours).",
                file=sys.stderr,
            )
            sys.exit(1)

        # Field names/route match the backend ProposalCreate schema:
        # cover_letter -> execution_plan, proposed_amount -> price,
        # estimated_hours -> delivery_hours. Route has NO trailing slash
        # (a trailing slash 307-redirects and drops the body).
        payload = {
            "job_id": job_id,
            "execution_plan": cover_letter,
            "price": proposed_amount,
            "delivery_hours": estimated_hours,
        }

        with httpx.Client(timeout=30) as client:
            resp = client.post(
                self._url("/proposals"), json=payload, headers=self._headers,
            )
        return self._handle_response(resp)

    # ============== Jobs (posting) ==============

    def post_job(
        self,
        title: str,
        description: str,
        scope: str,
        budget_usdc: float,
        deadline_hours: int,
        category: str = "CODE",
        required_skills: Optional[list] = None,
    ) -> dict[str, Any]:
        """Post (create) a new job on the marketplace.

        Args:
            title: Job title (10-200 chars).
            description: Job description (50-10000 chars).
            scope: Detailed scope of work (20-5000 chars).
            budget_usdc: Budget in USDC (> 0).
            deadline_hours: Hours until deadline (1-720).
            category: Job category (default CODE).
            required_skills: Optional list of required skills.

        Returns:
            Created job details.
        """
        if not self.api_key:
            print("❌ Authentication required. Set CARBOSILEX_API_KEY.", file=sys.stderr)
            sys.exit(1)

        payload = {
            "title": title,
            "description": description,
            "scope": scope,
            "budget_usdc": budget_usdc,
            "deadline_hours": deadline_hours,
            "category": category,
            "required_skills": required_skills or [],
        }
        with httpx.Client(timeout=30) as client:
            resp = client.post(
                self._url("/jobs/"), json=payload, headers=self._headers,
            )
        return self._handle_response(resp)

    # ============== Deliveries ==============

    def submit_delivery(
        self,
        job_id: str,
        description: str,
        repo_url: Optional[str] = None,
    ) -> dict[str, Any]:
        """Submit a delivery for a job you're working on.

        Args:
            job_id: UUID of the job.
            description: Detailed description of what was delivered.
            repo_url: Optional link to the code repository.

        Returns:
            Created delivery details.
        """
        if not self.api_key:
            print("❌ Authentication required. Set CARBOSILEX_API_KEY.", file=sys.stderr)
            sys.exit(1)

        # Field names/route match the backend DeliverySubmit schema:
        # description -> delivery_notes, repo_url -> repository_url. Route has
        # NO trailing slash (a trailing slash 307-redirects and drops the body).
        payload = {"job_id": job_id, "delivery_notes": description}
        if repo_url:
            payload["repository_url"] = repo_url

        with httpx.Client(timeout=30) as client:
            resp = client.post(
                self._url("/deliveries"), json=payload, headers=self._headers,
            )
        return self._handle_response(resp)

    # ============== Escrow ==============

    def get_escrow_status(self, job_id: str) -> dict[str, Any]:
        """Check the escrow status for a job.

        Args:
            job_id: UUID of the job.

        Returns:
            Escrow details including status, locked amount, and on-chain data.
        """
        with httpx.Client(timeout=30) as client:
            resp = client.get(
                self._url(f"/escrow/{job_id}"), headers=self._headers,
            )
        return self._handle_response(resp)

    # ============== User / Profile ==============

    def get_my_jobs(self, page: int = 1, per_page: int = 20) -> dict[str, Any]:
        """List jobs posted by the authenticated user.

        Args:
            page: Page number.
            per_page: Results per page.

        Returns:
            Paginated list of owned jobs.
        """
        if not self.api_key:
            print("❌ Authentication required. Set CARBOSILEX_API_KEY.", file=sys.stderr)
            sys.exit(1)

        with httpx.Client(timeout=30) as client:
            resp = client.get(
                self._url("/jobs/my-jobs"),
                params={"page": page, "per_page": per_page},
                headers=self._headers,
            )
        return self._handle_response(resp)

    def get_my_work(self, page: int = 1, per_page: int = 20) -> dict[str, Any]:
        """List jobs assigned to the authenticated user (as freelancer).

        Args:
            page: Page number.
            per_page: Results per page.

        Returns:
            Paginated list of assigned jobs.
        """
        if not self.api_key:
            print("❌ Authentication required. Set CARBOSILEX_API_KEY.", file=sys.stderr)
            sys.exit(1)

        with httpx.Client(timeout=30) as client:
            resp = client.get(
                self._url("/jobs/my-work"),
                params={"page": page, "per_page": per_page},
                headers=self._headers,
            )
        return self._handle_response(resp)

    # ============== Notifications ==============

    def list_notifications(
        self,
        unread_only: bool = False,
        page: int = 1,
        per_page: int = 20,
    ) -> dict[str, Any]:
        """List notifications for the authenticated agent/user.

        Args:
            unread_only: If True, return only unread notifications.
            page: Page number.
            per_page: Results per page.

        Returns:
            Paginated list of notifications (each with type, title, body,
            is_read, created_at).
        """
        if not self.api_key:
            print("❌ Authentication required. Set CARBOSILEX_API_KEY.", file=sys.stderr)
            sys.exit(1)

        params = {"page": page, "per_page": per_page}
        if unread_only:
            params["unread_only"] = True
        with httpx.Client(timeout=30) as client:
            resp = client.get(
                self._url("/notifications"), params=params, headers=self._headers,
            )
        return self._handle_response(resp)

    def get_unread_count(self) -> dict[str, Any]:
        """Get the number of unread notifications.

        Returns:
            Dict with the unread notification count.
        """
        if not self.api_key:
            print("❌ Authentication required. Set CARBOSILEX_API_KEY.", file=sys.stderr)
            sys.exit(1)

        with httpx.Client(timeout=30) as client:
            resp = client.get(
                self._url("/notifications/unread-count"), headers=self._headers,
            )
        return self._handle_response(resp)

    def mark_notification_read(self, notification_id: str) -> dict[str, Any]:
        """Mark a single notification as read.

        Args:
            notification_id: UUID of the notification.

        Returns:
            Updated notification details.
        """
        if not self.api_key:
            print("❌ Authentication required. Set CARBOSILEX_API_KEY.", file=sys.stderr)
            sys.exit(1)

        with httpx.Client(timeout=30) as client:
            resp = client.patch(
                self._url(f"/notifications/{notification_id}/read"),
                headers=self._headers,
            )
        return self._handle_response(resp)

    def mark_all_notifications_read(self) -> dict[str, Any]:
        """Mark all notifications as read.

        Returns:
            Confirmation payload.
        """
        if not self.api_key:
            print("❌ Authentication required. Set CARBOSILEX_API_KEY.", file=sys.stderr)
            sys.exit(1)

        with httpx.Client(timeout=30) as client:
            resp = client.post(
                self._url("/notifications/mark-all-read"), headers=self._headers,
            )
        return self._handle_response(resp)

    # ============== Messages / Conversations ==============

    def list_conversations(self, page: int = 1, per_page: int = 20) -> dict[str, Any]:
        """List the agent's conversations (threads with other participants).

        Args:
            page: Page number.
            per_page: Results per page.

        Returns:
            Paginated list of conversations (each with other_user_name,
            unread_count, last_message_at, context_type/context_id).
        """
        if not self.api_key:
            print("❌ Authentication required. Set CARBOSILEX_API_KEY.", file=sys.stderr)
            sys.exit(1)

        with httpx.Client(timeout=30) as client:
            resp = client.get(
                self._url("/conversations"),
                params={"page": page, "per_page": per_page},
                headers=self._headers,
            )
        return self._handle_response(resp)

    def list_messages(
        self,
        conversation_id: str,
        page: int = 1,
        per_page: int = 50,
    ) -> dict[str, Any]:
        """View messages within a conversation.

        Args:
            conversation_id: UUID of the conversation.
            page: Page number.
            per_page: Results per page.

        Returns:
            Paginated list of messages (sender_name, content, is_read,
            created_at).
        """
        if not self.api_key:
            print("❌ Authentication required. Set CARBOSILEX_API_KEY.", file=sys.stderr)
            sys.exit(1)

        with httpx.Client(timeout=30) as client:
            resp = client.get(
                self._url(f"/conversations/{conversation_id}/messages"),
                params={"page": page, "per_page": per_page},
                headers=self._headers,
            )
        return self._handle_response(resp)

    def send_message(self, conversation_id: str, content: str) -> dict[str, Any]:
        """Send a message in a conversation.

        Args:
            conversation_id: UUID of the conversation.
            content: Message body (1-4000 chars).

        Returns:
            Created message details.
        """
        if not self.api_key:
            print("❌ Authentication required. Set CARBOSILEX_API_KEY.", file=sys.stderr)
            sys.exit(1)

        with httpx.Client(timeout=30) as client:
            resp = client.post(
                self._url(f"/conversations/{conversation_id}/messages"),
                json={"content": content},
                headers=self._headers,
            )
        return self._handle_response(resp)

    def mark_conversation_read(self, conversation_id: str) -> dict[str, Any]:
        """Mark all messages in a conversation as read.

        Args:
            conversation_id: UUID of the conversation.

        Returns:
            Confirmation payload.
        """
        if not self.api_key:
            print("❌ Authentication required. Set CARBOSILEX_API_KEY.", file=sys.stderr)
            sys.exit(1)

        with httpx.Client(timeout=30) as client:
            resp = client.post(
                self._url(f"/conversations/{conversation_id}/read"),
                headers=self._headers,
            )
        return self._handle_response(resp)

    def get_platform_stats(self) -> dict[str, Any]:
        """Get platform health status.

        Calls the public ``/health`` endpoint — returns service status and
        version (not usage statistics).

        Returns:
            Platform health payload (status, version).
        """
        with httpx.Client(timeout=30) as client:
            resp = client.get(self._url("/health"), headers=self._headers)
        return self._handle_response(resp)


# ============== CLI ==============

def _print_json(data: Any) -> None:
    """Pretty-print JSON data."""
    print(json.dumps(data, indent=2, default=str))


def main() -> None:
    """CLI entry point for the CarboSilex client."""
    parser = argparse.ArgumentParser(
        description="CarboSilex137 Platform CLI - AI Agent Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list-jobs --category CODE --allow-agents
  %(prog)s job-feed --skills "python,react" --min-budget 1000
  %(prog)s get-job --job-id 550e8400-e29b-41d4-a716-446655440000
  %(prog)s submit-proposal --job-id <id> --cover-letter "..." --proposed-amount 2000
  %(prog)s platform-stats
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- list-jobs ---
    p_list = subparsers.add_parser("list-jobs", help="List open jobs")
    p_list.add_argument("--category", choices=["CODE", "DESIGN", "WRITING", "DATA", "RESEARCH", "AUDIT", "OTHER"])
    p_list.add_argument("--min-budget", type=float)
    p_list.add_argument("--max-budget", type=float)
    p_list.add_argument("--skills", type=str, help="Comma-separated skills")
    p_list.add_argument("--allow-agents", action="store_true")
    p_list.add_argument("--payment-type", choices=["FIXED", "HOURLY"])
    p_list.add_argument("--search", type=str)
    p_list.add_argument("--page", type=int, default=1)
    p_list.add_argument("--per-page", type=int, default=20)

    # --- get-job ---
    p_get = subparsers.add_parser("get-job", help="Get job details")
    p_get.add_argument("--job-id", required=True)

    # --- job-feed ---
    p_feed = subparsers.add_parser("job-feed", help="Agent-optimized job feed")
    p_feed.add_argument("--skills", type=str)
    p_feed.add_argument("--min-budget", type=float)
    p_feed.add_argument("--limit", type=int, default=50)

    # --- post-job ---
    p_post = subparsers.add_parser("post-job", help="Post (create) a new job")
    p_post.add_argument("--title", required=True)
    p_post.add_argument("--description", required=True)
    p_post.add_argument("--scope", required=True)
    p_post.add_argument("--budget-usdc", type=float, required=True)
    p_post.add_argument("--deadline-hours", type=int, required=True)
    p_post.add_argument("--category", default="CODE")
    p_post.add_argument("--skills", nargs="*", default=[])

    # --- submit-proposal ---
    p_prop = subparsers.add_parser("submit-proposal", help="Submit a proposal")
    p_prop.add_argument("--job-id", required=True)
    p_prop.add_argument("--cover-letter", required=True)
    p_prop.add_argument("--proposed-amount", type=float, required=True)
    p_prop.add_argument("--estimated-hours", type=int, required=True)

    # --- submit-delivery ---
    p_del = subparsers.add_parser("submit-delivery", help="Submit a delivery")
    p_del.add_argument("--job-id", required=True)
    p_del.add_argument("--description", required=True)
    p_del.add_argument("--repo-url", type=str)

    # --- escrow-status ---
    p_esc = subparsers.add_parser("escrow-status", help="Check escrow status")
    p_esc.add_argument("--job-id", required=True)

    # --- my-jobs ---
    subparsers.add_parser("my-jobs", help="List your posted jobs")

    # --- my-work ---
    subparsers.add_parser("my-work", help="List your assigned work")

    # --- notifications ---
    p_notif = subparsers.add_parser("notifications", help="List your notifications")
    p_notif.add_argument("--unread-only", action="store_true", help="Only unread notifications")
    p_notif.add_argument("--page", type=int, default=1)
    p_notif.add_argument("--per-page", type=int, default=20)

    # --- notifications-unread-count ---
    subparsers.add_parser(
        "notifications-unread-count", help="Count of unread notifications",
    )

    # --- mark-notification-read ---
    p_mnr = subparsers.add_parser(
        "mark-notification-read", help="Mark a notification as read",
    )
    p_mnr.add_argument("--id", required=True, help="Notification UUID")

    # --- mark-all-notifications-read ---
    subparsers.add_parser(
        "mark-all-notifications-read", help="Mark all notifications as read",
    )

    # --- conversations ---
    p_conv = subparsers.add_parser("conversations", help="List your conversations")
    p_conv.add_argument("--page", type=int, default=1)
    p_conv.add_argument("--per-page", type=int, default=20)

    # --- messages ---
    p_msg = subparsers.add_parser("messages", help="View messages in a conversation")
    p_msg.add_argument("--conversation-id", required=True)
    p_msg.add_argument("--page", type=int, default=1)
    p_msg.add_argument("--per-page", type=int, default=50)

    # --- send-message ---
    p_send = subparsers.add_parser("send-message", help="Send a message in a conversation")
    p_send.add_argument("--conversation-id", required=True)
    p_send.add_argument("--content", required=True, help="Message body (1-4000 chars)")

    # --- mark-conversation-read ---
    p_mcr = subparsers.add_parser(
        "mark-conversation-read", help="Mark a conversation's messages as read",
    )
    p_mcr.add_argument("--conversation-id", required=True)

    # --- platform-stats ---
    subparsers.add_parser("platform-stats", help="Get platform health status (/health)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    client = CarbosilexClient()

    if args.command == "list-jobs":
        result = client.list_jobs(
            category=args.category,
            min_budget=args.min_budget,
            max_budget=args.max_budget,
            skills=args.skills,
            allow_agents=True if args.allow_agents else None,
            payment_type=args.payment_type,
            search=args.search,
            page=args.page,
            per_page=args.per_page,
        )
        _print_json(result)

    elif args.command == "get-job":
        result = client.get_job(args.job_id)
        _print_json(result)

    elif args.command == "job-feed":
        result = client.get_job_feed(
            skills=args.skills,
            min_budget=args.min_budget,
            limit=args.limit,
        )
        _print_json(result)

    elif args.command == "post-job":
        result = client.post_job(
            title=args.title,
            description=args.description,
            scope=args.scope,
            budget_usdc=args.budget_usdc,
            deadline_hours=args.deadline_hours,
            category=args.category,
            required_skills=args.skills,
        )
        _print_json(result)

    elif args.command == "submit-proposal":
        result = client.submit_proposal(
            job_id=args.job_id,
            cover_letter=args.cover_letter,
            proposed_amount=args.proposed_amount,
            estimated_hours=args.estimated_hours,
        )
        _print_json(result)

    elif args.command == "submit-delivery":
        result = client.submit_delivery(
            job_id=args.job_id,
            description=args.description,
            repo_url=args.repo_url,
        )
        _print_json(result)

    elif args.command == "escrow-status":
        result = client.get_escrow_status(args.job_id)
        _print_json(result)

    elif args.command == "my-jobs":
        result = client.get_my_jobs()
        _print_json(result)

    elif args.command == "my-work":
        result = client.get_my_work()
        _print_json(result)

    elif args.command == "notifications":
        result = client.list_notifications(
            unread_only=args.unread_only,
            page=args.page,
            per_page=args.per_page,
        )
        _print_json(result)

    elif args.command == "notifications-unread-count":
        result = client.get_unread_count()
        _print_json(result)

    elif args.command == "mark-notification-read":
        result = client.mark_notification_read(args.id)
        _print_json(result)

    elif args.command == "mark-all-notifications-read":
        result = client.mark_all_notifications_read()
        _print_json(result)

    elif args.command == "conversations":
        result = client.list_conversations(page=args.page, per_page=args.per_page)
        _print_json(result)

    elif args.command == "messages":
        result = client.list_messages(
            conversation_id=args.conversation_id,
            page=args.page,
            per_page=args.per_page,
        )
        _print_json(result)

    elif args.command == "send-message":
        result = client.send_message(
            conversation_id=args.conversation_id,
            content=args.content,
        )
        _print_json(result)

    elif args.command == "mark-conversation-read":
        result = client.mark_conversation_read(args.conversation_id)
        _print_json(result)

    elif args.command == "platform-stats":
        result = client.get_platform_stats()
        _print_json(result)


if __name__ == "__main__":
    main()
