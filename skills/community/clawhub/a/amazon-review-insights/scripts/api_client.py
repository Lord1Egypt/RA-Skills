"""
CustomerInsights API Client
For AI Agent to call review fetching and analysis APIs

Author: Zhang Di
Email: dizflyme@qq.com
Date: 2025-03-25
LastEditors: Zhang Di
LastEditTime: 2026-04-27
Description: Global e-commerce customer insights API client wrapper
"""

__version__ = "1.0.0"

import argparse
import json
import os
from typing import Any, Dict, Optional

# Use requests library for macOS certificate compatibility
try:
    import requests
except ImportError:
    raise ImportError("Please install requests library: pip install requests")

# API Configuration
_BASE_URL = "https://api.astrmap.com"
_WEBSITE_URL = "https://www.astrmap.com"


def _get_api_key() -> str:
    """Lazy load API Key to avoid hardcoding environment variable at module import"""
    return os.environ.get("CUSTOMER_INSIGHTS_API_KEY", "")


class CustomerInsightsClient:
    """CustomerInsights API Client"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _get(self, url: str, timeout: int = 30, auth: bool = False) -> dict:
        """GET request

        Args:
            url: Request URL
            timeout: Timeout in seconds
            auth: Whether authentication is required, defaults to False (used for public endpoints like download-config.json)
        """
        headers = {}
        if auth:
            headers["Authorization"] = f"Bearer {self.api_key}"
            headers["Accept"] = "application/json"

        try:
            response = requests.get(url, timeout=timeout, headers=headers or None)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request Error: {e}")

    def _post(self, path: str, data: dict = None) -> dict:
        """POST request"""
        url = f"{_BASE_URL}{path}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = requests.post(url, json=data or {}, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            if result.get("code") != 0:
                raise Exception(f"API Error: {result.get('msg')}")
            return result.get("data", {})
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request Error: {e}")

    # ==================== Device Management ====================

    def check_device_online(self) -> Dict[str, Any]:
        """Check if device is online"""
        return self._post("/api/v1/external/device/status", {})

    # ==================== Download Management ====================

    def get_download_links(self) -> Dict[str, Any]:
        """Get desktop client download links

        Get latest download links for each platform from official website config.

        Returns:
            Dict[str, Any]: Contains download info for macos and windows
        """
        config_url = f"{_WEBSITE_URL}/download-config.json"
        config = self._get(config_url)

        downloads = config.get("downloads", {}) or {}
        macos_info = downloads.get("macos") or {}
        windows_info = downloads.get("windows") or {}

        return {
            "macos": {
                "name": macos_info.get("name_en") or "macOS Version",
                "url": macos_info.get("url") or "",
                "version": macos_info.get("version") or "",
                "size": macos_info.get("size") or "",
            },
            "windows": {
                "name": windows_info.get("name_en") or "Windows Version",
                "url": windows_info.get("url") or "",
                "version": windows_info.get("version") or "",
                "size": windows_info.get("size") or "",
            },
        }

    # ==================== Task Management ====================

    def create_task(
        self, submit_content: str, site: str = "US", platform: str = "amazon", is_auto: bool = True
    ) -> str:
        """Create task

        Args:
            submit_content: ASIN or product URL
            site: Site code, defaults to US
            platform: Platform, defaults to amazon
            is_auto: Auto mode flag, True=auto analysis, False=collection only (requires manual trigger)
        """
        data = {
            "platform": platform,
            "site": site,
            "submit_content": submit_content,
            "is_auto": is_auto,
        }
        result = self._post("/api/v1/external/task/create", data)
        task_id = result.get("task_id")
        if not task_id:
            raise Exception("Failed to create task: task_id missing from API response")
        return task_id

    def trigger_analysis(self, task_id: str) -> Dict[str, Any]:
        """Manually trigger AI analysis for collection-only tasks"""
        return self._post(f"/api/v1/external/task/{task_id}/trigger-analysis", {})

    def get_task_detail(self, task_id: str) -> Dict[str, Any]:
        """Query task details"""
        return self._post("/api/v1/external/task/detail", {"task_id": task_id})

    def get_task_list(
        self,
        page: int = 1,
        page_size: int = 20,
        search_keyword: str = "",
        filter_monitoring: bool = False,
    ) -> Dict[str, Any]:
        """Get task list"""
        return self._post(
            "/api/v1/external/task/list",
            {
                "page": page,
                "page_size": page_size,
                "search_keyword": search_keyword,
                "filter_monitoring": filter_monitoring,
            },
        )

    def create_incremental(self, task_id: str) -> Dict[str, Any]:
        """Create incremental fetch for completed task"""
        return self._post("/api/v1/external/task/incremental", {"task_id": task_id})

    # ==================== Analysis Results ====================

    def get_ai_insights(self, task_id: str) -> Dict[str, Any]:
        """Get AI insights"""
        return self._post("/api/v1/external/analysis/insights", {"task_id": task_id})

    def get_basic_statistics(self, task_id: str) -> Dict[str, Any]:
        """Get basic statistics"""
        return self._post("/api/v1/external/analysis/statistics", {"task_id": task_id})

    def get_representative_reviews(
        self, task_id: str, polarity: str = "negative", limit: int = 5
    ) -> Dict[str, Any]:
        """Get representative reviews"""
        return self._post(
            "/api/v1/external/analysis/representative-reviews",
            {"task_id": task_id, "polarity": polarity, "limit": limit},
        )

    def get_sentiment_reviews(
        self, task_id: str, polarity: str = "negative", page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get sentiment reviews list - supports polarity parameter"""
        return self._post(
            "/api/v1/external/analysis/sentiment-reviews",
            {"task_id": task_id, "polarity": polarity, "page": page, "page_size": page_size},
        )

    def get_negative_reviews(
        self, task_id: str, page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """Get negative reviews list (backward compatible, defaults to polarity=negative)"""
        return self._post(
            "/api/v1/external/analysis/sentiment-reviews",
            {"task_id": task_id, "polarity": "negative", "page": page, "page_size": page_size},
        )

    def get_category_tag_distribution(
        self, task_id: str, polarity: str = "negative"
    ) -> Dict[str, Any]:
        """Get category-tag distribution - three-level nested structure"""
        return self._post(
            f"/api/v1/external/analysis/category-tag-distribution/{task_id}",
            {"polarity": polarity},
        )

    def get_trend(
        self, task_id: str, filter_data: str = "30", filter_product: str = "all"
    ) -> Dict[str, Any]:
        """Get review trends"""
        return self._post(
            "/api/v1/external/analysis/trend",
            {
                "task_id": task_id,
                "filter_data": filter_data,
                "filter_product": filter_product,
            },
        )

    def get_comments(
        self,
        task_id: str,
        page: int = 1,
        page_size: int = 20,
        filter_star: str = "all",
        filter_verified: str = "all",
    ) -> Dict[str, Any]:
        """Get raw comments"""
        return self._post(
            "/api/v1/external/analysis/comments",
            {
                "task_id": task_id,
                "page": page,
                "page_size": page_size,
                "filter_star": filter_star,
                "filter_verified": filter_verified,
            },
        )

    def get_comments_overview(self, task_id: str) -> Dict[str, Any]:
        """Get comments overview"""
        return self._post(
            "/api/v1/external/analysis/comments-overview", {"task_id": task_id}
        )

    def get_related_comments(
        self,
        task_id: str,
        association_type: str = "tag",
        normalized_tag: str = None,
        category: str = None,
        dimension: str = None,
        polarity: str = "negative",
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Get comments associated with tag/category

        Args:
            task_id: Task ID
            association_type: Association type, "tag" or "category"
            normalized_tag: Normalized tag name (tag mode)
            category: Tag category (tag/category mode)
            dimension: Dimension (category mode)
            polarity: Sentiment filter (category mode): negative/positive/all
            page: Page number
            page_size: Items per page
        """
        data = {
            "task_id": task_id,
            "association_type": association_type,
            "page": page,
            "page_size": page_size,
        }
        if normalized_tag:
            data["normalized_tag"] = normalized_tag
        if category:
            data["category"] = category
        if dimension:
            data["dimension"] = dimension
        if polarity:
            data["polarity"] = polarity
        return self._post("/api/v1/external/analysis/related-comments", data)

    # ==================== Account Management ====================

    def get_points(self) -> int:
        """Get points balance"""
        result = self._post("/api/v1/external/account/points", {})
        return result.get("available_points", 0)


# ==================== CLI Entry Point ====================


def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser"""
    parser = argparse.ArgumentParser(
        description="AstrMap CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--api-key", "-k", default=None, help="API Key (defaults to CUSTOMER_INSIGHTS_API_KEY env var)")
    parser.add_argument(
        "--action",
        "-a",
        required=True,
        help="Action to execute: get_download_links, check_device, create_task, get_task_detail, get_task_list, create_incremental, trigger_analysis, get_ai_insights, get_basic_statistics, get_representative_reviews, get_category_tag_distribution, get_negative_reviews, get_trend, get_related_comments, get_comments, get_comments_overview, get_points",
    )

    # Action parameters
    parser.add_argument("--asin", help="ASIN or product URL (create_task)")
    parser.add_argument(
        "--site", default="US", help="Site: US/CA/DE/FR/UK/JP/IT/ES (create_task)"
    )
    parser.add_argument("--platform", default="amazon", help="Platform (create_task)")
    parser.add_argument(
        "--is-auto", type=lambda x: x.lower() == "true", default=True,
        help="Auto mode: true/false. True=auto analysis, False=collection only (create_task)"
    )
    parser.add_argument(
        "--task-id", help="Task ID (get_task_detail, create_incremental, trigger_analysis, get_xxx)"
    )
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--page-size", type=int, default=20, help="Items per page")
    parser.add_argument(
        "--filter-data", default="30", help="Data range: 30/60/all (get_trend)"
    )
    parser.add_argument(
        "--filter-product", default="all", help="Product filter: all/ASIN (get_trend)"
    )
    parser.add_argument(
        "--filter-star", default="all", help="Rating filter: 1-5/all (get_comments)"
    )
    parser.add_argument(
        "--filter-verified", default="all", help="Filter verified: all/true/false (get_comments)"
    )
    parser.add_argument(
        "--association-type", default="tag",
        help="Association type: tag/category (get_related_comments)"
    )
    parser.add_argument(
        "--normalized-tag", default=None, help="Normalized tag name (get_related_comments, tag mode)"
    )
    parser.add_argument(
        "--category", default=None, help="Tag category (get_related_comments, tag mode)"
    )
    parser.add_argument(
        "--dimension", default=None, help="Dimension (get_related_comments, category mode)"
    )
    parser.add_argument(
        "--polarity", default=None, help="Sentiment filter (get_representative_reviews, get_related_comments)"
    )
    parser.add_argument(
        "--limit", type=int, default=5, help="Number of items to return (get_representative_reviews)"
    )

    return parser


def execute(params: dict) -> dict:
    """
    Unified entry function (for AI Agent dispatch)

    :param params: Parameters passed by OpenClaw
    :return: Execution result dictionary
    """
    try:
        api_key = params.get("api_key") or _get_api_key()
        action = params.get("action", "")

        # get_download_links is a public endpoint, no API Key required
        if action != "get_download_links" and not api_key:
            return {
                "status": "error",
                "message": "Please provide an API Key. Set via CUSTOMER_INSIGHTS_API_KEY env var or pass via --api-key parameter.",
            }

        client = CustomerInsightsClient(api_key)

        # Helper function: extract task_id parameter
        def _require_task_id(params: dict) -> tuple:
            """Extract and validate task_id parameter, returns (task_id, error_response)"""
            task_id = params.get("task_id")
            if not task_id:
                return None, {"status": "error", "message": "Missing task_id parameter"}
            return task_id, None

        # Route to specific methods
        if action == "get_download_links":
            return {"status": "success", "output": client.get_download_links()}

        elif action == "check_device":
            return {"status": "success", "output": client.check_device_online()}

        elif action == "create_task":
            submit_content = params.get("submit_content") or params.get("asin", "")
            if not submit_content:
                return {
                    "status": "error",
                    "message": "Missing submit_content or asin parameter",
                }
            task_id = client.create_task(
                submit_content=submit_content,
                site=params.get("site", "US"),
                platform=params.get("platform", "amazon"),
                is_auto=params.get("is_auto", True),
            )
            return {"status": "success", "output": {"task_id": task_id}}

        elif action == "get_task_detail":
            task_id, err = _require_task_id(params)
            if err:
                return err
            return {"status": "success", "output": client.get_task_detail(task_id)}

        elif action == "get_task_list":
            return {
                "status": "success",
                "output": client.get_task_list(
                    page=params.get("page", 1),
                    page_size=params.get("page_size", 20),
                ),
            }

        elif action == "create_incremental":
            task_id, err = _require_task_id(params)
            if err:
                return err
            return {"status": "success", "output": client.create_incremental(task_id)}

        elif action == "trigger_analysis":
            task_id, err = _require_task_id(params)
            if err:
                return err
            return {"status": "success", "output": client.trigger_analysis(task_id)}

        elif action == "get_ai_insights":
            task_id, err = _require_task_id(params)
            if err:
                return err
            return {"status": "success", "output": client.get_ai_insights(task_id)}

        elif action == "get_basic_statistics":
            task_id, err = _require_task_id(params)
            if err:
                return err
            return {"status": "success", "output": client.get_basic_statistics(task_id)}

        elif action == "get_representative_reviews":
            task_id, err = _require_task_id(params)
            if err:
                return err
            return {
                "status": "success",
                "output": client.get_representative_reviews(
                    task_id,
                    polarity=params.get("polarity", "negative"),
                    limit=params.get("limit", 5),
                ),
            }

        elif action == "get_negative_reviews":
            task_id, err = _require_task_id(params)
            if err:
                return err
            return {
                "status": "success",
                "output": client.get_negative_reviews(
                    task_id,
                    page=params.get("page", 1),
                    page_size=params.get("page_size", 20),
                ),
            }

        elif action == "get_trend":
            task_id, err = _require_task_id(params)
            if err:
                return err
            return {
                "status": "success",
                "output": client.get_trend(
                    task_id,
                    filter_data=params.get("filter_data", "30"),
                    filter_product=params.get("filter_product", "all"),
                ),
            }

        elif action == "get_comments":
            task_id, err = _require_task_id(params)
            if err:
                return err
            return {
                "status": "success",
                "output": client.get_comments(
                    task_id,
                    page=params.get("page", 1),
                    page_size=params.get("page_size", 20),
                    filter_star=params.get("filter_star", "all"),
                    filter_verified=params.get("filter_verified", "all"),
                ),
            }

        elif action == "get_comments_overview":
            task_id, err = _require_task_id(params)
            if err:
                return err
            return {
                "status": "success",
                "output": client.get_comments_overview(task_id),
            }

        elif action == "get_related_comments":
            task_id, err = _require_task_id(params)
            if err:
                return err
            return {
                "status": "success",
                "output": client.get_related_comments(
                    task_id,
                    association_type=params.get("association_type", "tag"),
                    normalized_tag=params.get("normalized_tag"),
                    category=params.get("category"),
                    dimension=params.get("dimension"),
                    polarity=params.get("polarity"),
                    page=params.get("page", 1),
                    page_size=params.get("page_size", 20),
                ),
            }

        elif action == "get_points":
            return {
                "status": "success",
                "output": {"available_points": client.get_points()},
            }

        else:
            return {"status": "error", "message": f"Unknown action: {action}"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    """Command-line entry point"""
    parser = create_parser()
    args = parser.parse_args()

    params = {
        "api_key": args.api_key or _get_api_key(),
        "action": args.action,
        "submit_content": args.asin,
        "site": args.site,
        "platform": args.platform,
        "is_auto": args.is_auto,
        "task_id": args.task_id,
        "page": args.page,
        "page_size": args.page_size,
        "filter_data": args.filter_data,
        "filter_product": args.filter_product,
        "filter_star": args.filter_star,
        "filter_verified": args.filter_verified,
        "association_type": args.association_type,
        "normalized_tag": args.normalized_tag,
        "category": args.category,
        "dimension": args.dimension,
        "polarity": args.polarity,
        "limit": args.limit,
    }

    result = execute(params)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ==================== Convenience Functions (backward compatible) ====================


def check_device_online(api_key: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function: Check if device is online"""
    if api_key is None:
        api_key = _get_api_key()
    return execute({"api_key": api_key, "action": "check_device"})


def get_download_links(api_key: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function: Get desktop client download links (no API Key required)"""
    return execute({"api_key": api_key or "", "action": "get_download_links"})


def create_task(
    submit_content: str,
    site: str = "US",
    platform: str = "amazon",
    is_auto: bool = True,
    api_key: Optional[str] = None,
) -> str:
    """Convenience function: Create task

    Args:
        submit_content: ASIN or product URL
        site: Site code, defaults to US
        platform: Platform, defaults to amazon
        is_auto: Auto mode flag, True=auto analysis, False=collection only (requires manual trigger)
        api_key: API Key
    """
    if api_key is None:
        api_key = _get_api_key()
    result = execute(
        {
            "api_key": api_key,
            "action": "create_task",
            "submit_content": submit_content,
            "site": site,
            "platform": platform,
            "is_auto": is_auto,
        }
    )
    if result["status"] == "success":
        return result["output"]["task_id"]
    raise Exception(result["message"])


def trigger_analysis(task_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function: Manually trigger AI analysis for collection-only tasks"""
    if api_key is None:
        api_key = _get_api_key()
    return execute(
        {
            "api_key": api_key,
            "action": "trigger_analysis",
            "task_id": task_id,
        }
    )


def get_ai_insights(task_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function: Get AI insights"""
    if api_key is None:
        api_key = _get_api_key()
    return execute(
        {
            "api_key": api_key,
            "action": "get_ai_insights",
            "task_id": task_id,
        }
    )


def get_points(api_key: Optional[str] = None) -> int:
    """Convenience function: Get points balance"""
    if api_key is None:
        api_key = _get_api_key()
    result = execute({"api_key": api_key, "action": "get_points"})
    if result["status"] == "success":
        return result["output"]["available_points"]
    raise Exception(result["message"])


def get_task_list(
    page: int = 1,
    page_size: int = 20,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience function: Get task list"""
    if api_key is None:
        api_key = _get_api_key()
    return execute(
        {
            "api_key": api_key,
            "action": "get_task_list",
            "page": page,
            "page_size": page_size,
        }
    )


def get_task_detail(task_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function: Get task details"""
    if api_key is None:
        api_key = _get_api_key()
    return execute(
        {
            "api_key": api_key,
            "action": "get_task_detail",
            "task_id": task_id,
        }
    )


def create_incremental(task_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function: Create incremental fetch for completed task"""
    if api_key is None:
        api_key = _get_api_key()
    return execute(
        {
            "api_key": api_key,
            "action": "create_incremental",
            "task_id": task_id,
        }
    )


def get_basic_statistics(task_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function: Get basic statistics"""
    if api_key is None:
        api_key = _get_api_key()
    return execute(
        {
            "api_key": api_key,
            "action": "get_basic_statistics",
            "task_id": task_id,
        }
    )


def get_representative_reviews(
    task_id: str,
    polarity: str = "negative",
    limit: int = 5,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience function: Get representative reviews"""
    if api_key is None:
        api_key = _get_api_key()
    return execute(
        {
            "api_key": api_key,
            "action": "get_representative_reviews",
            "task_id": task_id,
            "polarity": polarity,
            "limit": limit,
        }
    )


def get_negative_reviews(
    task_id: str,
    page: int = 1,
    page_size: int = 20,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience function: Get negative reviews list"""
    if api_key is None:
        api_key = _get_api_key()
    return execute(
        {
            "api_key": api_key,
            "action": "get_negative_reviews",
            "task_id": task_id,
            "page": page,
            "page_size": page_size,
        }
    )


def get_trend(
    task_id: str,
    filter_data: str = "30",
    filter_product: str = "all",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience function: Get review trends"""
    if api_key is None:
        api_key = _get_api_key()
    return execute(
        {
            "api_key": api_key,
            "action": "get_trend",
            "task_id": task_id,
            "filter_data": filter_data,
            "filter_product": filter_product,
        }
    )


def get_comments(
    task_id: str,
    page: int = 1,
    page_size: int = 20,
    filter_star: str = "all",
    filter_verified: str = "all",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience function: Get raw comments"""
    if api_key is None:
        api_key = _get_api_key()
    return execute(
        {
            "api_key": api_key,
            "action": "get_comments",
            "task_id": task_id,
            "page": page,
            "page_size": page_size,
            "filter_star": filter_star,
            "filter_verified": filter_verified,
        }
    )


def get_comments_overview(task_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function: Get comments overview"""
    if api_key is None:
        api_key = _get_api_key()
    return execute(
        {
            "api_key": api_key,
            "action": "get_comments_overview",
            "task_id": task_id,
        }
    )


def get_related_comments(
    task_id: str,
    association_type: str = "tag",
    normalized_tag: str = None,
    category: str = None,
    dimension: str = None,
    polarity: str = "negative",
    page: int = 1,
    page_size: int = 20,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Convenience function: Get comments associated with tag/category"""
    if api_key is None:
        api_key = _get_api_key()
    return execute(
        {
            "api_key": api_key,
            "action": "get_related_comments",
            "task_id": task_id,
            "association_type": association_type,
            "normalized_tag": normalized_tag,
            "category": category,
            "dimension": dimension,
            "polarity": polarity,
            "page": page,
            "page_size": page_size,
        }
    )


if __name__ == "__main__":
    main()
