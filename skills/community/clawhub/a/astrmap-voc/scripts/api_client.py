"""
CustomerInsights API Client
用于 AI Agent 调用评论获取和分析接口

Author: Zhang Di
Email: dizflyme@qq.com
Date: 2025-03-25
LastEditors: Zhang Di
LastEditTime: 2026-03-27
Description: 全球电商客户洞察 API 客户端封装
"""

__version__ = "1.0.0"

import argparse
import json
import os
from typing import Any, Dict, Optional

# 使用 requests 库以确保 macOS 证书兼容性
try:
    import requests
except ImportError:
    raise ImportError("请安装 requests 库: pip install requests")

# API 配置
_BASE_URL = "https://api.astrmap.com"
_WEBSITE_URL = "https://www.astrmap.com"


def _get_api_key() -> str:
    """延迟读取 API Key，避免模块导入时固化环境变量"""
    return os.environ.get("CUSTOMER_INSIGHTS_API_KEY", "")


class CustomerInsightsClient:
    """CustomerInsights API 客户端"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _get(self, url: str, timeout: int = 30, auth: bool = False) -> dict:
        """GET 请求

        Args:
            url: 请求 URL
            timeout: 超时时间（秒）
            auth: 是否需要认证，默认 False（用于 download-config.json 等公开接口）
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
        """POST 请求"""
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

    # ==================== 设备管理 ====================

    def check_device_online(self) -> Dict[str, Any]:
        """检查用户端点是否在线

        响应 (v2.2): {is_alive: bool, endpoint_id: str|None,
        endpoint_type: str|None, status: str}
        """
        return self._post("/api/v1/external/device/status", {})

    # ==================== 下载管理 ====================

    def get_download_links(self) -> Dict[str, Any]:
        """获取浏览器扩展下载链接

        从官网下载配置获取最新下载链接。
        注：网站已不再提供桌面客户端下载，downloads 中现仅有 extension 一项。

        Returns:
            Dict[str, Any]: 含 extension 的下载信息（若配置中不存在则为空 url）
        """
        config_url = f"{_WEBSITE_URL}/download-config.json"
        config = self._get(config_url)

        downloads = config.get("downloads", {}) or {}
        extension_info = downloads.get("extension") or {}

        return {
            "extension": {
                "name": extension_info.get("name_zh") or extension_info.get("name_en") or "Chrome 扩展",
                "url": extension_info.get("url") or "",
                "version": extension_info.get("version") or "",
                "size": extension_info.get("size") or "",
            },
        }

    # ==================== 任务管理 ====================

    def create_task(self, submit_content: str, site: str = "US", platform: str = "amazon", is_auto: bool = True) -> str:
        """创建任务

        Args:
            submit_content: ASIN 或产品 URL
            site: 站点代码，默认 US
            platform: 平台，默认 amazon
            is_auto: 是否自动模式，True=自动分析，False=仅采集（需手动触发分析）
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
            raise Exception("创建任务失败：API 响应中缺少 task_id")
        return task_id

    def trigger_analysis(self, task_id: str) -> Dict[str, Any]:
        """手动触发仅采集任务的 AI 分析流程"""
        return self._post(f"/api/v1/external/task/{task_id}/trigger-analysis", {})

    def get_task_detail(self, task_id: str) -> Dict[str, Any]:
        """查询任务详情"""
        return self._post("/api/v1/external/task/detail", {"task_id": task_id})

    def get_task_list(
        self,
        page: int = 1,
        page_size: int = 20,
        search_keyword: str = "",
        filter_monitoring: bool = False,
    ) -> Dict[str, Any]:
        """获取任务列表"""
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
        """为终态任务创建增量获取"""
        return self._post("/api/v1/external/task/incremental", {"task_id": task_id})

    def rename_task(self, task_id: str, name: str) -> Dict[str, Any]:
        """重命名任务（仅更新任务名称）"""
        return self._post(
            "/api/v1/external/task/rename",
            {"task_id": task_id, "name": name},
        )

    # ==================== 分析结果 ====================

    def get_ai_insights(self, task_id: str) -> Dict[str, Any]:
        """获取 AI 洞察"""
        return self._post("/api/v1/external/analysis/insights", {"task_id": task_id})

    def get_basic_statistics(self, task_id: str) -> Dict[str, Any]:
        """获取基础统计"""
        return self._post("/api/v1/external/analysis/statistics", {"task_id": task_id})

    def get_representative_reviews(self, task_id: str, polarity: str = "negative", limit: int = 5) -> Dict[str, Any]:
        """获取代表性评论"""
        return self._post(
            "/api/v1/external/analysis/representative-reviews",
            {"task_id": task_id, "polarity": polarity, "limit": limit},
        )

    def get_sentiment_reviews(
        self, task_id: str, polarity: str = "negative", page: int = 1, page_size: int = 20
    ) -> Dict[str, Any]:
        """获取情感评价列表 - 支持 polarity 参数"""
        return self._post(
            "/api/v1/external/analysis/sentiment-reviews",
            {"task_id": task_id, "polarity": polarity, "page": page, "page_size": page_size},
        )

    def get_negative_reviews(self, task_id: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """获取差评列表（向后兼容，默认 polarity=negative）"""
        return self._post(
            "/api/v1/external/analysis/sentiment-reviews",
            {"task_id": task_id, "polarity": "negative", "page": page, "page_size": page_size},
        )

    def get_category_tag_distribution(self, task_id: str, polarity: str = "negative") -> Dict[str, Any]:
        """获取分类标签分布 - 三层嵌套结构"""
        return self._post(
            f"/api/v1/external/analysis/category-tag-distribution/{task_id}",
            {"polarity": polarity},
        )

    def get_trend(self, task_id: str, filter_data: str = "30", filter_product: str = "all") -> Dict[str, Any]:
        """获取评论趋势"""
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
        """获取原始评论"""
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
        """获取评论概览"""
        return self._post("/api/v1/external/analysis/comments-overview", {"task_id": task_id})

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
        """获取标签/分类关联的评论

        Args:
            task_id: 任务ID
            association_type: 关联类型，"tag" 或 "category"
            normalized_tag: 标准化标签名（tag模式）
            category: 标签分类（tag/category模式）
            dimension: 维度（category模式）
            polarity: 情感筛选（category模式）：negative/positive/all
            page: 页码
            page_size: 每页数量
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


    # ==================== 商品信息 ====================

    def get_product_detail(
        self,
        task_id: str = None,
        asin: str = None,
        site: str = "US",
    ) -> Dict[str, Any]:
        """获取商品信息（完整字段，含 bullets / description，供二次分析）

        两种查询方式（二选一）：
        - task_id：按任务查，返回该任务下所有商品
        - asin + site：按商品直查，无需先建任务
          ⚠️ 服务端会校验归属：该 ASIN 必须出现在您的某个任务中，
             否则返回错误（商品数据按 (platform, site, asin) 全局存储）

        Args:
            task_id: 任务ID（与 asin 二选一）
            asin: 商品 ASIN（与 task_id 二选一）
            site: 站点，默认 US

        Returns:
            含 products 数组，每项包含标题/品牌/评分/星级分布/分类树/
            价格/bullets/描述/A+ 图片等完整字段
        """
        if not task_id and not asin:
            raise ValueError("task_id 与 asin 至少提供一个")
        data = {}
        if task_id:
            data["task_id"] = task_id
        if asin:
            data["asin"] = asin
            data["site"] = site or "US"
        return self._post("/api/v1/external/product/detail", data)

    # ==================== 账户管理 ====================

    def get_points(self) -> int:
        """获取积分余额"""
        result = self._post("/api/v1/external/account/points", {})
        return result.get("available_points", 0)


# ==================== CLI 入口 ====================


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="AstrMap CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--api-key", "-k", default=None, help="API Key（默认从环境变量 CUSTOMER_INSIGHTS_API_KEY 读取）"
    )
    parser.add_argument(
        "--action",
        "-a",
        required=True,
        help="执行的操作: get_download_links, check_device, create_task, get_task_detail, get_task_list, create_incremental, rename_task, trigger_analysis, get_ai_insights, get_basic_statistics, get_representative_reviews, get_category_tag_distribution, get_negative_reviews, get_trend, get_related_comments, get_comments, get_comments_overview, get_product_detail, get_points",
    )

    # 动作参数
    parser.add_argument("--asin", help="ASIN 或产品 URL (create_task)")
    parser.add_argument("--site", default="US", help="站点: US/CA/DE/FR/UK/JP/IT/ES (create_task)")
    parser.add_argument("--platform", default="amazon", help="平台 (create_task)")
    parser.add_argument(
        "--is-auto",
        type=lambda x: x.lower() == "true",
        default=True,
        help="是否自动模式: true/false, True=自动分析, False=仅采集 (create_task)",
    )
    parser.add_argument(
        "--task-id", help="任务 ID (get_task_detail, create_incremental, rename_task, trigger_analysis, get_xxx)"
    )
    parser.add_argument("--name", help="新任务名称 (rename_task)")
    parser.add_argument("--page", type=int, default=1, help="页码")
    parser.add_argument("--page-size", type=int, default=20, help="每页数量")
    parser.add_argument("--filter-data", default="30", help="数据范围: 30/60/all (get_trend)")
    parser.add_argument("--filter-product", default="all", help="商品筛选: all/ASIN (get_trend)")
    parser.add_argument("--filter-star", default="all", help="评分筛选: 1-5/all (get_comments)")
    parser.add_argument("--filter-verified", default="all", help="筛选已认证评论: all/true/false (get_comments)")
    parser.add_argument("--association-type", default="tag", help="关联类型: tag/category (get_related_comments)")
    parser.add_argument("--normalized-tag", default=None, help="标准化标签名 (get_related_comments, tag模式)")
    parser.add_argument("--category", default=None, help="标签分类 (get_related_comments, tag模式)")
    parser.add_argument("--dimension", default=None, help="关联维度 (get_related_comments, category模式)")
    parser.add_argument("--polarity", default=None, help="情感极性 (get_representative_reviews, get_related_comments)")
    parser.add_argument("--limit", type=int, default=5, help="返回数量 (get_representative_reviews)")

    return parser


def execute(params: dict) -> dict:
    """
    统一入口函数（供 AI Agent 调度）

    :param params: OpenClaw 传入的参数
    :return: 执行结果字典
    """
    try:
        api_key = params.get("api_key") or _get_api_key()
        action = params.get("action", "")

        # get_download_links 是公开接口，不需要 API Key
        if action != "get_download_links" and not api_key:
            return {
                "status": "error",
                "message": "请提供 API Key。通过环境变量 CUSTOMER_INSIGHTS_API_KEY 设置，或通过 --api-key 参数传入。",
            }

        client = CustomerInsightsClient(api_key)

        # 辅助函数：提取 task_id 参数
        def _require_task_id(params: dict) -> tuple:
            """提取并校验 task_id 参数，返回 (task_id, error_response)"""
            task_id = params.get("task_id")
            if not task_id:
                return None, {"status": "error", "message": "缺少 task_id 参数"}
            return task_id, None

        # 路由到具体方法
        if action == "get_download_links":
            return {"status": "success", "output": client.get_download_links()}

        elif action == "check_device":
            return {"status": "success", "output": client.check_device_online()}

        elif action == "create_task":
            submit_content = params.get("submit_content") or params.get("asin", "")
            if not submit_content:
                return {
                    "status": "error",
                    "message": "缺少 submit_content 或 asin 参数",
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

        elif action == "rename_task":
            task_id, err = _require_task_id(params)
            if err:
                return err
            name = params.get("name")
            if not name:
                return {"status": "error", "message": "缺少 name 参数"}
            return {"status": "success", "output": client.rename_task(task_id, name)}

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
                    polarity=params.get("polarity") or "negative",
                    limit=params.get("limit", 5),
                ),
            }

        elif action == "get_category_tag_distribution":
            task_id, err = _require_task_id(params)
            if err:
                return err
            return {
                "status": "success",
                "output": client.get_category_tag_distribution(
                    task_id,
                    polarity=params.get("polarity") or "negative",
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

        elif action == "get_product_detail":
            tid = params.get("task_id")
            asin = params.get("asin")
            if not tid and not asin:
                return {
                    "status": "error",
                    "message": "请提供 task_id 或 asin（二者至少一个）",
                }
            return {
                "status": "success",
                "output": client.get_product_detail(
                    task_id=tid,
                    asin=asin,
                    site=params.get("site", "US"),
                ),
            }

        elif action == "get_points":
            return {
                "status": "success",
                "output": {"available_points": client.get_points()},
            }

        else:
            return {"status": "error", "message": f"未知操作: {action}"}

    except Exception as e:
        return {"status": "error", "message": str(e)}


def main():
    """命令行入口"""
    parser = create_parser()
    args = parser.parse_args()

    params = {
        "api_key": args.api_key or _get_api_key(),
        "action": args.action,
        "submit_content": args.asin,
        "asin": args.asin,
        "site": args.site,
        "platform": args.platform,
        "is_auto": args.is_auto,
        "task_id": args.task_id,
        "name": args.name,
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


# ==================== 便捷函数（向后兼容） ====================


def check_device_online(api_key: Optional[str] = None) -> Dict[str, Any]:
    """便捷函数：检查用户端点是否在线（CLI 名称：check_device）"""
    if api_key is None:
        api_key = _get_api_key()
    return execute({"api_key": api_key, "action": "check_device"})


def get_download_links(api_key: Optional[str] = None) -> Dict[str, Any]:
    """便捷函数：获取浏览器扩展下载链接（无需 API Key）"""
    return execute({"api_key": api_key or "", "action": "get_download_links"})


def create_task(
    submit_content: str,
    site: str = "US",
    platform: str = "amazon",
    is_auto: bool = True,
    api_key: Optional[str] = None,
) -> str:
    """便捷函数：创建任务

    Args:
        submit_content: ASIN 或产品 URL
        site: 站点代码，默认 US
        platform: 平台，默认 amazon
        is_auto: 是否自动模式，True=自动分析，False=仅采集（需手动触发分析）
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
    """便捷函数：手动触发仅采集任务的 AI 分析"""
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
    """便捷函数：获取 AI 洞察"""
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
    """便捷函数：获取积分余额"""
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
    """便捷函数：获取任务列表"""
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
    """便捷函数：获取任务详情"""
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
    """便捷函数：为终态任务创建增量获取"""
    if api_key is None:
        api_key = _get_api_key()
    return execute(
        {
            "api_key": api_key,
            "action": "create_incremental",
            "task_id": task_id,
        }
    )


def rename_task(task_id: str, name: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """便捷函数：重命名任务"""
    if api_key is None:
        api_key = _get_api_key()
    return execute(
        {
            "api_key": api_key,
            "action": "rename_task",
            "task_id": task_id,
            "name": name,
        }
    )


def get_basic_statistics(task_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """便捷函数：获取基础统计"""
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
    """便捷函数：获取代表性评论"""
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
    """便捷函数：获取差评列表"""
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
    """便捷函数：获取评论趋势"""
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
    """便捷函数：获取原始评论"""
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
    """便捷函数：获取评论概览"""
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
    """便捷函数：获取标签/分类关联的评论"""
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
