#!/usr/bin/env python3
"""Canvas LMS API client with auth, pagination, rate limiting, and write gating.

Usage as library:
    from canvas_api import CanvasClient, load_canvas_credentials
    base_url, token = load_canvas_credentials()
    client = CanvasClient(base_url, token)
    courses = list(client.get_paginated("/api/v1/courses"))

Usage as CLI:
    python3 canvas_api.py courses [--active]
    python3 canvas_api.py query <course_id> pages [--search <term>]
    python3 canvas_api.py query <course_id> assignments [--upcoming] [--search <term>]
    python3 canvas_api.py query <course_id> announcements
    python3 canvas_api.py query <course_id> files
    python3 canvas_api.py query <course_id> modules
    python3 canvas_api.py query <course_id> discussions
    python3 canvas_api.py query <course_id> quizzes
    python3 canvas_api.py query <course_id> enrollments
    python3 canvas_api.py query <course_id> syllabus
    python3 canvas_api.py validate
"""

import json
import re
import sys
import time
from pathlib import Path
from typing import Generator, Optional, Union
from urllib.parse import urljoin, urlparse, parse_qs

import requests


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

from paths import CANVAS_CREDENTIALS

DEFAULT_CREDENTIALS_PATH = CANVAS_CREDENTIALS
RATE_LIMIT_BUFFER = 50          # pause when remaining drops below this
BACKOFF_BASE_SECONDS = 10       # first retry wait on 403
BACKOFF_MAX_RETRIES = 3
DEFAULT_PER_PAGE = 100
RETRYABLE_STATUS_CODES = {500, 502, 503, 504}


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class CanvasAPIError(Exception):
    """Raised on non-recoverable Canvas API errors."""

    def __init__(self, status_code: int, message: str, endpoint: str = ""):
        self.status_code = status_code
        self.endpoint = endpoint
        super().__init__(f"Canvas API {status_code} on {endpoint}: {message}")


class CanvasPermissionError(Exception):
    """Raised when a write operation is denied."""
    pass


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_canvas_credentials(cred_path: Optional[Path] = None) -> tuple:
    """Load (base_url, access_token) from canvas.json.

    Raises FileNotFoundError if file missing, KeyError if malformed.
    """
    path = cred_path or DEFAULT_CREDENTIALS_PATH
    if not path.exists():
        raise FileNotFoundError(f"Canvas credentials not found at {path}")
    data = json.loads(path.read_text())
    base_url = data["canvas_base_url"].rstrip("/")
    token = data["access_token"]
    if not base_url or not token:
        raise ValueError(f"Canvas credentials incomplete in {path}")
    return base_url, token


def validate_credentials(base_url: str, access_token: str) -> bool:
    """Quick ping to verify credentials work. Returns True on success."""
    try:
        client = CanvasClient(base_url, access_token, write_mode="deny")
        result = client.get("/api/v1/users/self")
        return isinstance(result, dict) and "id" in result
    except (CanvasAPIError, requests.RequestException):
        return False


def slugify_course_name(course_code: str) -> str:
    """Convert 'BU.520.710.42.SP26' -> 'bu-520-710-42-sp26'."""
    slug = course_code.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def _parse_link_header(header: str) -> dict:
    """Parse Link header into {rel: url} dict."""
    links = {}
    for part in header.split(","):
        match = re.match(r'\s*<([^>]+)>\s*;\s*rel="([^"]+)"', part.strip())
        if match:
            links[match.group(2)] = match.group(1)
    return links


# ---------------------------------------------------------------------------
# Canvas Client
# ---------------------------------------------------------------------------

class CanvasClient:
    """Thin wrapper around Canvas REST API with auth, pagination,
    rate limiting, retry logic, and write permission gating."""

    def __init__(self, base_url: str, access_token: str,
                 write_mode: str = "confirm",
                 rate_limit_buffer: int = RATE_LIMIT_BUFFER):
        """
        Args:
            base_url: Canvas instance URL (e.g. https://your-canvas-instance.instructure.com)
            access_token: Bearer token
            write_mode: "confirm" (prompt user), "allow" (auto), "deny" (block)
            rate_limit_buffer: pause when X-Rate-Limit-Remaining < this
        """
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token
        self.write_mode = write_mode
        self.rate_limit_buffer = rate_limit_buffer

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        })

    # -- internal -----------------------------------------------------------

    def _check_rate_limit(self, response: requests.Response):
        """Sleep if rate limit is getting low."""
        remaining = response.headers.get("X-Rate-Limit-Remaining")
        if remaining is not None:
            try:
                if float(remaining) < self.rate_limit_buffer:
                    print(f"[canvas_api] Rate limit low ({remaining}), sleeping 5s...",
                          file=sys.stderr)
                    time.sleep(5)
            except ValueError:
                pass

    def _request(self, method: str, url: str, params: dict = None,
                 data: dict = None, json_body: dict = None,
                 stream: bool = False) -> requests.Response:
        """Core HTTP method with rate limiting, retries on transient errors,
        and exponential backoff on rate limits."""
        if url.startswith("/"):
            url = self.base_url + url

        last_error = None

        for attempt in range(BACKOFF_MAX_RETRIES + 1):
            # Network-level errors (timeout, connection reset)
            try:
                resp = self.session.request(
                    method, url, params=params, data=data, json=json_body,
                    stream=stream, timeout=60,
                )
            except (requests.Timeout, requests.ConnectionError) as e:
                last_error = e
                if attempt < BACKOFF_MAX_RETRIES:
                    wait = BACKOFF_BASE_SECONDS * (2 ** attempt)
                    print(f"[canvas_api] Network error ({type(e).__name__}), "
                          f"retrying in {wait}s (attempt {attempt + 1})...",
                          file=sys.stderr)
                    time.sleep(wait)
                    continue
                raise CanvasAPIError(
                    0, f"Network error after {BACKOFF_MAX_RETRIES} retries: {e}",
                    endpoint=url)

            # Rate limit hit — retry with backoff
            if resp.status_code == 403:
                body = resp.text.lower()
                if "rate limit" in body or "throttled" in body:
                    if attempt < BACKOFF_MAX_RETRIES:
                        wait = BACKOFF_BASE_SECONDS * (3 ** attempt)
                        print(f"[canvas_api] Rate limited, waiting {wait}s "
                              f"(attempt {attempt + 1}/{BACKOFF_MAX_RETRIES})...",
                              file=sys.stderr)
                        time.sleep(wait)
                        continue

            # Server errors — retry with backoff
            if resp.status_code in RETRYABLE_STATUS_CODES:
                if attempt < BACKOFF_MAX_RETRIES:
                    wait = BACKOFF_BASE_SECONDS * (2 ** attempt)
                    print(f"[canvas_api] Server error {resp.status_code}, "
                          f"retrying in {wait}s (attempt {attempt + 1})...",
                          file=sys.stderr)
                    time.sleep(wait)
                    continue

            # Check remaining budget
            self._check_rate_limit(resp)

            # Raise on non-success
            if resp.status_code >= 400:
                raise CanvasAPIError(
                    resp.status_code,
                    resp.text[:500],
                    endpoint=url,
                )

            return resp

        raise CanvasAPIError(
            getattr(resp, 'status_code', 0) if 'resp' in dir() else 0,
            "Max retries exceeded",
            endpoint=url)

    def _check_write_permission(self, action_description: str) -> bool:
        """Gate write operations based on write_mode."""
        if self.write_mode == "deny":
            raise CanvasPermissionError(
                f"Write operations disabled: {action_description}")
        if self.write_mode == "confirm":
            try:
                response = input(f"\n[canvas_api] Write permission required:\n"
                                 f"  {action_description}\n"
                                 f"  Proceed? [y/N] ")
                return response.strip().lower() in ("y", "yes")
            except (EOFError, KeyboardInterrupt):
                return False
        return True  # "allow" mode

    # -- public API ---------------------------------------------------------

    def get(self, endpoint: str, params: dict = None) -> Union[dict, list]:
        """Single-page GET, returns parsed JSON."""
        resp = self._request("GET", endpoint, params=params)
        return resp.json()

    def get_paginated(self, endpoint: str, params: dict = None,
                      per_page: int = DEFAULT_PER_PAGE) -> Generator[dict, None, None]:
        """Yield individual items across all pages.

        Handles Link header pagination automatically. Yields dicts from
        list responses; yields single dict if response is an object.
        """
        params = dict(params or {})
        params["per_page"] = per_page

        url = endpoint if endpoint.startswith("http") else self.base_url + endpoint

        while url:
            resp = self._request("GET", url, params=params)
            data = resp.json()

            if isinstance(data, list):
                yield from data
            elif isinstance(data, dict):
                # Some endpoints return a single object
                yield data
            else:
                print(f"[canvas_api] Unexpected JSON type from {url}: "
                      f"{type(data).__name__}", file=sys.stderr)

            # Follow pagination
            link_header = resp.headers.get("Link", "")
            links = _parse_link_header(link_header)
            url = links.get("next")
            # After first request, params are encoded in the Link URL
            params = None

    def post(self, endpoint: str, data: dict = None,
             json_body: dict = None, action_description: str = "") -> dict:
        """Write operation — gated by write_mode."""
        desc = action_description or f"POST {endpoint}"
        if not self._check_write_permission(desc):
            raise CanvasPermissionError(f"User denied: {desc}")
        resp = self._request("POST", endpoint, data=data, json_body=json_body)
        return resp.json()

    def put(self, endpoint: str, data: dict = None,
            json_body: dict = None, action_description: str = "") -> dict:
        """Write operation — gated by write_mode."""
        desc = action_description or f"PUT {endpoint}"
        if not self._check_write_permission(desc):
            raise CanvasPermissionError(f"User denied: {desc}")
        resp = self._request("PUT", endpoint, data=data, json_body=json_body)
        return resp.json()

    def delete(self, endpoint: str, action_description: str = "") -> dict:
        """Write operation — gated by write_mode."""
        desc = action_description or f"DELETE {endpoint}"
        if not self._check_write_permission(desc):
            raise CanvasPermissionError(f"User denied: {desc}")
        resp = self._request("DELETE", endpoint)
        return resp.json()

    def download_file(self, file_obj: dict, dest_path: Path) -> Path:
        """Download a Canvas file to local path.

        Handles Canvas's redirect chain (API URL -> file URL -> S3).
        Retries on transient network errors.

        Args:
            file_obj: File object from Canvas API (must have 'url' key)
            dest_path: Local destination path
        Returns:
            The dest_path on success
        """
        file_url = file_obj.get("url")
        if not file_url:
            raise CanvasAPIError(0, "File object has no 'url' field", "download")

        dest_path.parent.mkdir(parents=True, exist_ok=True)

        for attempt in range(BACKOFF_MAX_RETRIES + 1):
            try:
                # Canvas file URLs redirect to the actual file (often S3)
                # Use a fresh request (no auth header needed for the redirect target)
                resp = requests.get(file_url, stream=True, timeout=120)
                resp.raise_for_status()

                with open(dest_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)

                return dest_path
            except (requests.Timeout, requests.ConnectionError) as e:
                if attempt < BACKOFF_MAX_RETRIES:
                    wait = BACKOFF_BASE_SECONDS * (2 ** attempt)
                    print(f"[canvas_api] Download failed ({type(e).__name__}), "
                          f"retrying in {wait}s...", file=sys.stderr)
                    time.sleep(wait)
                    continue
                raise CanvasAPIError(
                    0, f"Download failed after retries: {e}",
                    endpoint=file_url)

    # -- convenience methods ------------------------------------------------

    def get_courses(self, enrollment_state: str = "active",
                    include: list = None) -> list:
        """List all courses for the current user."""
        params = {"enrollment_state": enrollment_state}
        if include:
            for i, val in enumerate(include):
                params[f"include[{i}]"] = val
        return list(self.get_paginated("/api/v1/courses", params=params))

    def get_course(self, course_id: int, include: list = None) -> dict:
        """Get a single course."""
        params = {}
        if include:
            params["include[]"] = include
        return self.get(f"/api/v1/courses/{course_id}", params=params)

    def get_modules(self, course_id: int, include_items: bool = True) -> list:
        """List modules for a course."""
        params = {}
        if include_items:
            params["include[]"] = "items"
        return list(self.get_paginated(
            f"/api/v1/courses/{course_id}/modules", params=params))

    def get_pages(self, course_id: int) -> list:
        """List all pages for a course."""
        return list(self.get_paginated(
            f"/api/v1/courses/{course_id}/pages"))

    def get_page(self, course_id: int, page_url: str) -> dict:
        """Get a single page with body."""
        return self.get(f"/api/v1/courses/{course_id}/pages/{page_url}")

    def get_assignments(self, course_id: int) -> list:
        """List all assignments for a course."""
        return list(self.get_paginated(
            f"/api/v1/courses/{course_id}/assignments"))

    def get_announcements(self, course_id: int) -> list:
        """List announcements for a course."""
        return list(self.get_paginated(
            "/api/v1/announcements",
            params={"context_codes[]": f"course_{course_id}"}))

    def get_discussion_topics(self, course_id: int) -> list:
        """List discussion topics for a course."""
        return list(self.get_paginated(
            f"/api/v1/courses/{course_id}/discussion_topics"))

    def get_discussion_entries(self, course_id: int, topic_id: int) -> list:
        """Get entries for a discussion topic."""
        return list(self.get_paginated(
            f"/api/v1/courses/{course_id}/discussion_topics/{topic_id}/entries"))

    def get_files(self, course_id: int) -> list:
        """List all files for a course."""
        return list(self.get_paginated(
            f"/api/v1/courses/{course_id}/files"))

    def get_quizzes(self, course_id: int) -> list:
        """List quizzes for a course."""
        return list(self.get_paginated(
            f"/api/v1/courses/{course_id}/quizzes"))

    def get_enrollments(self, course_id: int) -> list:
        """List enrollments for a course."""
        return list(self.get_paginated(
            f"/api/v1/courses/{course_id}/enrollments"))

    def get_syllabus(self, course_id: int) -> dict:
        """Get course with syllabus body."""
        return self.get(
            f"/api/v1/courses/{course_id}",
            params={"include[]": "syllabus_body"})

    def get_submissions(self, course_id: int, assignment_id: int) -> list:
        """List submissions for an assignment."""
        return list(self.get_paginated(
            f"/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions"))

    def get_calendar_events(self, course_id: int) -> list:
        """List calendar events for a course."""
        return list(self.get_paginated(
            "/api/v1/calendar_events",
            params={"context_codes[]": f"course_{course_id}", "type": "event"}))


# ---------------------------------------------------------------------------
# CLI interface
# ---------------------------------------------------------------------------

def _cli_courses(client: CanvasClient, args: list):
    """List all courses."""
    active_only = "--active" in args
    courses = client.get_courses()
    for c in courses:
        if active_only and c.get("workflow_state") != "available":
            continue
        roles = [e["type"] for e in c.get("enrollments", [])]
        state = c.get("workflow_state", "?")
        print(f"  {c['id']:>8}  {c.get('course_code', c['name'])[:60]:<62}"
              f"  {','.join(roles):<20}  {state}")


def _cli_query(client: CanvasClient, args: list):
    """Query a specific course."""
    if len(args) < 2:
        print("Usage: canvas_api.py query <course_id> <resource> "
              "[--search <term>] [--upcoming]", file=sys.stderr)
        sys.exit(1)

    try:
        course_id = int(args[0])
    except ValueError:
        print(f"Invalid course_id: {args[0]}", file=sys.stderr)
        sys.exit(1)
    resource = args[1]
    search_term = None
    if "--search" in args:
        idx = args.index("--search")
        if idx + 1 < len(args):
            search_term = args[idx + 1].lower()

    try:
        _cli_query_resource(client, course_id, resource, search_term,
                            "--upcoming" in args)
    except CanvasAPIError as e:
        print(f"  Error: {e}", file=sys.stderr)
        sys.exit(1)


def _cli_query_resource(client: CanvasClient, course_id: int,
                        resource: str, search_term: str = None,
                        upcoming: bool = False):
    """Execute a resource query."""
    if resource == "pages":
        pages = client.get_pages(course_id)
        for p in pages:
            title = p.get("title", "?")
            if search_term and search_term not in title.lower():
                continue
            print(f"  {p.get('url', '?'):<50}  {title}")

    elif resource == "assignments":
        assignments = client.get_assignments(course_id)
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        for a in assignments:
            due = a.get("due_at")
            if upcoming and due:
                due_dt = datetime.fromisoformat(due.replace("Z", "+00:00"))
                if due_dt < now:
                    continue
            if search_term and search_term not in a["name"].lower():
                continue
            pts = a.get("points_possible", "?")
            print(f"  {a['id']:>8}  {a['name'][:50]:<52}  "
                  f"due:{due or 'none':<26}  pts:{pts}")

    elif resource == "announcements":
        anns = client.get_announcements(course_id)
        for a in anns:
            posted = a.get('posted_at') or 'N/A'
            print(f"  {posted:<26}  {a['title'][:70]}")

    elif resource == "files":
        files = client.get_files(course_id)
        for f in files:
            size_mb = f.get("size", 0) / (1024 * 1024)
            print(f"  {f['id']:>8}  {f['display_name'][:50]:<52}  {size_mb:.1f}MB")

    elif resource == "modules":
        modules = client.get_modules(course_id)
        for m in modules:
            items = m.get("items", [])
            print(f"  Module {m.get('position', '?')}: {m['name']} "
                  f"({len(items)} items)")
            for item in items:
                print(f"    - [{item.get('type', '?')}] "
                      f"{item.get('title', '?')}")

    elif resource == "discussions":
        topics = client.get_discussion_topics(course_id)
        for d in topics:
            print(f"  {d['id']:>8}  {d['title'][:60]:<62}  "
                  f"posts:{d.get('discussion_subentry_count', '?')}")

    elif resource == "quizzes":
        quizzes = client.get_quizzes(course_id)
        for q in quizzes:
            print(f"  {q['id']:>8}  {q['title'][:50]:<52}  "
                  f"pts:{q.get('points_possible', '?')}  "
                  f"due:{q.get('due_at', 'none')}")

    elif resource == "enrollments":
        enrollments = client.get_enrollments(course_id)
        from collections import Counter
        counts = Counter(e["type"] for e in enrollments)
        print(f"  Total: {len(enrollments)}")
        for k, v in sorted(counts.items()):
            print(f"    {k}: {v}")

    elif resource == "syllabus":
        course = client.get_syllabus(course_id)
        body = course.get("syllabus_body", "")
        if body:
            print(f"  Syllabus body ({len(body)} chars):")
            print(f"  {body[:500]}...")
        else:
            print("  No syllabus body found.")

    else:
        print(f"Unknown resource: {resource}", file=sys.stderr)
        print("Available: pages, assignments, announcements, files, modules, "
              "discussions, quizzes, enrollments, syllabus", file=sys.stderr)
        sys.exit(1)


def _cli_validate():
    """Validate Canvas credentials."""
    base_url, token = load_canvas_credentials()
    print(f"  Base URL: {base_url}")
    print(f"  Token:    {token[:10]}...{token[-4:]}")
    print(f"  Validating...", end=" ", flush=True)
    if validate_credentials(base_url, token):
        print("OK")
    else:
        print("FAILED")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "validate":
        _cli_validate()
        return

    base_url, token = load_canvas_credentials()
    client = CanvasClient(base_url, token, write_mode="deny")

    if command == "courses":
        _cli_courses(client, sys.argv[2:])
    elif command == "query":
        _cli_query(client, sys.argv[2:])
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Available: courses, query, validate", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
