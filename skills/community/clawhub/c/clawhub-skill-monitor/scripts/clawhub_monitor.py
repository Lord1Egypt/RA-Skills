#!/usr/bin/env python3
"""
ClawHub Skill Monitor - fetch skills for a ClawHub user/owner from the real public API.

What this script can do reliably today:
- list published skills for a given ownerHandle (username)
- return package name, display name, version, updated time, summary, official flag, etc.
- optionally enrich each package with package detail data from /api/v1/packages/{name}

What the current public API does NOT appear to expose:
- install count
- download count
- user rating / star score
- review count

So this script never fabricates those metrics. It returns them as null / unavailable.
"""

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    requests = None
    import urllib.request
    import urllib.parse

CLAWHUB_BASE_URL = "https://clawhub.ai"
PACKAGES_ENDPOINT = "/api/v1/packages"
PACKAGE_DETAIL_ENDPOINT = "/api/v1/packages/{name}"
DEFAULT_PAGE_SIZE = 50
MAX_PAGES = 20


class ClawHubAPIError(Exception):
    pass


class ClawHubFetcher:
    def __init__(self, base_url: str = CLAWHUB_BASE_URL, timeout: int = 20):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = None
        if requests is not None:
            self.session = requests.Session()
            self.session.headers.update(
                {
                    "User-Agent": "ClawHub-Skill-Monitor/2.0",
                    "Accept": "application/json",
                }
            )

    def _get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}{path}"
        if requests is not None:
            resp = self.session.get(url, params=params, timeout=self.timeout)
            if not resp.ok:
                raise ClawHubAPIError(f"HTTP {resp.status_code}: {resp.text[:300]}")
            return resp.json()

        query = f"?{urllib.parse.urlencode(params)}" if params else ""
        req = urllib.request.Request(url + query, headers={"Accept": "application/json", "User-Agent": "ClawHub-Skill-Monitor/2.0"})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def fetch_user_skills(
        self,
        username: str,
        include_details: bool = False,
        max_pages: int = MAX_PAGES,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Fetch all public skills for a given ownerHandle.

        We cannot currently server-filter by owner on the public list endpoint,
        so we page through public skills and filter client-side by ownerHandle.
        """
        cursor = None
        pages_scanned = 0
        matched: List[Dict[str, Any]] = []
        total_seen = 0

        while pages_scanned < max_pages:
            params: Dict[str, Any] = {
                "family": "skill",
                "limit": page_size,
            }
            if cursor:
                params["cursor"] = cursor

            data = self._get_json(PACKAGES_ENDPOINT, params=params)
            items = data.get("items", [])
            total_seen += len(items)
            pages_scanned += 1

            for item in items:
                owner_handle = item.get("ownerHandle")
                if owner_handle == username:
                    normalized = self._normalize_skill(item)
                    if include_details:
                        detail = self.fetch_package_detail(normalized["name"])
                        normalized["package_detail"] = detail
                    matched.append(normalized)

            cursor = data.get("nextCursor")
            if not cursor:
                break

        matched.sort(key=lambda x: (x.get("updated_at") or "", x.get("name") or ""), reverse=True)

        scan_meta = {
            "owner_handle": username,
            "pages_scanned": pages_scanned,
            "packages_seen": total_seen,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "public_metric_support": {
                "installs": False,
                "downloads": False,
                "rating": False,
                "reviews": False,
            },
        }
        return matched, scan_meta

    def fetch_package_detail(self, package_name: str) -> Dict[str, Any]:
        data = self._get_json(PACKAGE_DETAIL_ENDPOINT.format(name=package_name))
        package = data.get("package") or {}
        owner = data.get("owner") or {}
        return {
            "package": package,
            "owner": owner,
        }

    def _normalize_skill(self, item: Dict[str, Any]) -> Dict[str, Any]:
        name = item.get("name") or "unknown"
        owner_handle = item.get("ownerHandle")
        updated_at = _millis_to_iso(item.get("updatedAt"))
        created_at = _millis_to_iso(item.get("createdAt"))
        latest_version = item.get("latestVersion")

        return {
            "name": name,
            "display_name": item.get("displayName") or name,
            "author": owner_handle,
            "owner_handle": owner_handle,
            "summary": item.get("summary") or "",
            "latest_version": latest_version,
            "channel": item.get("channel"),
            "is_official": item.get("isOfficial"),
            "executes_code": item.get("executesCode"),
            "verification_tier": item.get("verificationTier"),
            "capability_tags": item.get("capabilityTags") or [],
            "created_at": created_at,
            "updated_at": updated_at,
            "url": f"{CLAWHUB_BASE_URL}/skills?q={name}",
            # Real-time metrics currently not exposed in the public API.
            "installs": None,
            "downloads": None,
            "stars": None,
            "reviews": None,
            "metrics_available": False,
            "metrics_note": "ClawHub public API currently does not expose installs/downloads/rating/reviews for packages.",
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }


def _millis_to_iso(value: Any) -> Optional[str]:
    if value in (None, ""):
        return None
    try:
        return datetime.fromtimestamp(int(value) / 1000, tz=timezone.utc).isoformat()
    except Exception:
        return None


def format_table(skills: List[Dict[str, Any]], username: str) -> str:
    if not skills:
        return f"No public skills found for user '{username}' in scanned ClawHub results."

    name_width = min(max(max(len(s['name']) for s in skills), len("Skill Name")), 32)
    version_width = max(8, len("Version"))

    lines = []
    lines.append(f"┌{'─' * name_width}┬{'─' * version_width}┬──────────────┬──────────┐")
    lines.append(f"│ {'Skill Name'.ljust(name_width)} │ {'Version'.ljust(version_width)} │ Updated      │ Metrics   │")
    lines.append(f"├{'─' * name_width}┼{'─' * version_width}┼──────────────┼──────────┤")

    for skill in skills:
        name = skill['name'][:name_width].ljust(name_width)
        version = str(skill.get('latest_version') or '-')[0:version_width].ljust(version_width)
        updated = (skill.get('updated_at') or '-')[:12].ljust(12)
        metrics = 'N/A'.ljust(8)
        lines.append(f"│ {name} │ {version} │ {updated} │ {metrics} │")

    lines.append(f"└{'─' * name_width}┴{'─' * version_width}┴──────────────┴──────────┘")
    lines.append(f"\n📦 Total: {len(skills)} skills")
    lines.append("📉 Public metrics: installs / downloads / rating / reviews are currently unavailable from ClawHub public API")
    return "\n".join(lines)


def format_text(skills: List[Dict[str, Any]], username: str, meta: Dict[str, Any]) -> str:
    if not skills:
        return (
            f"未在已扫描的 ClawHub 公共结果中找到用户 {username} 的 skill。\n"
            f"已扫描页数：{meta.get('pages_scanned')}，已查看包数：{meta.get('packages_seen')}。"
        )

    lines = [f"📦 ClawHub skills for {username}", "=" * 50, ""]
    for idx, skill in enumerate(skills, 1):
        lines.append(f"{idx}. {skill['display_name']} ({skill['name']})")
        lines.append(f"   版本: {skill.get('latest_version') or '-'}")
        lines.append(f"   更新时间: {skill.get('updated_at') or '-'}")
        lines.append(f"   官方: {'是' if skill.get('is_official') else '否'}")
        if skill.get('summary'):
            lines.append(f"   简介: {skill['summary']}")
        lines.append("   安装量/下载量/评分/评论: 当前 ClawHub 公共 API 未暴露")
        lines.append("")

    lines.append(f"已扫描页数: {meta.get('pages_scanned')}")
    lines.append(f"已查看包数: {meta.get('packages_seen')}")
    return "\n".join(lines)


def export_csv(skills: List[Dict[str, Any]], output_file: str) -> None:
    fieldnames = [
        "name",
        "display_name",
        "owner_handle",
        "latest_version",
        "channel",
        "is_official",
        "executes_code",
        "created_at",
        "updated_at",
        "summary",
        "installs",
        "downloads",
        "stars",
        "reviews",
        "metrics_available",
        "metrics_note",
        "url",
        "fetched_at",
    ]
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in skills:
            writer.writerow({k: row.get(k) for k in fieldnames})


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch public skills for a ClawHub user")
    parser.add_argument("username", help="ClawHub ownerHandle / username")
    parser.add_argument("--format", "-f", choices=["text", "json", "table"], default="table")
    parser.add_argument("--export", "-e", help="Export results to CSV")
    parser.add_argument("--details", action="store_true", help="Fetch package detail for each matched skill")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE)
    parser.add_argument("--max-pages", type=int, default=MAX_PAGES)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    fetcher = ClawHubFetcher()

    try:
        skills, meta = fetcher.fetch_user_skills(
            args.username,
            include_details=args.details,
            max_pages=args.max_pages,
            page_size=args.page_size,
        )
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False, indent=2))
        return 1

    result = {
        "success": len(skills) > 0,
        "has_results": len(skills) > 0,
        "username": args.username,
        "total_skills": len(skills),
        "supports_live_metrics": False,
        "live_metrics_note": "ClawHub public API currently exposes package metadata but does not expose installs/downloads/rating/reviews.",
        "scan_meta": meta,
        "skills": skills,
    }

    if args.export:
        export_csv(skills, args.export)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.format == "text":
        print(format_text(skills, args.username, meta))
    else:
        print(format_table(skills, args.username))

    return 0


if __name__ == "__main__":
    sys.exit(main())
