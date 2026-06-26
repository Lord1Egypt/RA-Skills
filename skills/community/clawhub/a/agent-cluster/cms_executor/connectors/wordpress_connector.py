"""
WordPress Connector — WordPress REST API

支持：
- Posts / Pages CRUD
- Media 上传
- Categories / Tags
- SEO 元数据（Yoast / RankMath）
- 自定义文章类型
"""

from __future__ import annotations

import base64
import logging
from typing import Any

import httpx

from .base_connector import (
    BaseCMSConnector,
    CMSCredentials,
    CMSPlatform,
    CMSResource,
    CMSResourceType,
    CMSResult,
    CMSOperation,
    CMSOperationType,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WordPressConnector(BaseCMSConnector):
    """
    WordPress REST API 连接器

    API Reference: https://developer.wordpress.org/rest-api/
    
    支持认证方式：
    - Application Password（推荐）
    - JWT Token（需插件）
    - Cookie Authentication（仅管理后台）
    """

    platform = CMSPlatform.WORDPRESS

    def __init__(self, credentials: CMSCredentials):
        super().__init__(credentials)
        self._capabilities = [
            "create_post", "read_post", "update_post", "delete_post",
            "create_page", "read_page", "update_page", "delete_page",
            "upload_media", "manage_categories", "manage_tags",
            "update_seo", "custom_post_types",
        ]

    def _build_client(self) -> httpx.AsyncClient:
        """构建带 WordPress Basic Auth 的客户端"""
        headers = {
            "User-Agent": "M-A3-CMS-Executor/WordPress",
            "Content-Type": "application/json",
            **self.credentials.extra_headers,
        }
        # WordPress Basic Auth: username:app_password (base64)
        if self.credentials.api_key:
            auth_value = base64.b64encode(
                self.credentials.api_key.encode()
            ).decode()
            headers["Authorization"] = f"Basic {auth_value}"
        elif self.credentials.oauth_token:
            headers["Authorization"] = f"Bearer {self.credentials.oauth_token}"

        return httpx.AsyncClient(
            base_url=self.credentials.api_base,
            headers=headers,
            timeout=httpx.Timeout(self.credentials.timeout),
            follow_redirects=True,
        )

    async def _do_health_check(self, client: httpx.AsyncClient) -> bool:
        try:
            resp = await client.get("/wp-json/wp/v2/users/me")
            return resp.status_code == 200
        except Exception:
            return False

    async def _do_read(self, client: httpx.AsyncClient, resource_id: str) -> dict:
        """
        读取 WordPress 资源
        
        resource_id 格式: "posts/123" | "pages/456" | "media/789"
        """
        parts = resource_id.split("/", 1)
        post_type = parts[0] if len(parts) > 1 else "posts"
        post_id = parts[-1]
        resp = await client.get(f"/wp-json/wp/v2/{post_type}/{post_id}")
        resp.raise_for_status()
        return resp.json()

    async def _do_list(
        self, client: httpx.AsyncClient, filters: dict, page: int, per_page: int
    ) -> dict:
        params = {
            "page": page,
            "per_page": min(per_page, 100),
            **{k: v for k, v in filters.items() if v is not None},
        }
        resp = await client.get("/wp-json/wp/v2/posts", params=params)
        resp.raise_for_status()
        total = int(resp.headers.get("X-WP-Total", 0))
        total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
        return {"items": resp.json(), "total": total, "total_pages": total_pages}

    async def _do_create(self, client: httpx.AsyncClient, data: dict) -> dict:
        resp = await client.post("/wp-json/wp/v2/posts", json=data)
        resp.raise_for_status()
        return resp.json()

    async def _do_update(self, client: httpx.AsyncClient, resource_id: str, data: dict) -> dict:
        parts = resource_id.split("/", 1)
        post_type = parts[0] if len(parts) > 1 else "posts"
        post_id = parts[-1]
        resp = await client.post(f"/wp-json/wp/v2/{post_type}/{post_id}", json=data)
        resp.raise_for_status()
        return resp.json()

    async def _do_delete(self, client: httpx.AsyncClient, resource_id: str, soft: bool) -> dict:
        parts = resource_id.split("/", 1)
        post_type = parts[0] if len(parts) > 1 else "posts"
        post_id = parts[-1]
        params = {"force": not soft} if not soft else {}
        resp = await client.delete(
            f"/wp-json/wp/v2/{post_type}/{post_id}",
            params=params,
        )
        resp.raise_for_status()
        # DELETE 返回 200，body 是被删除的资源
        return resp.json()

    async def _do_upload_media(self, client: httpx.AsyncClient, file_path: str, metadata: dict) -> dict:
        import mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        with open(file_path, "rb") as f:
            file_content = f.read()
        files = {"file": (file_path.split("/")[-1], file_content, mime_type or "application/octet-stream")}
        data_fields = {k: str(v) for k, v in metadata.items()}
        resp = await client.post("/wp-json/wp/v2/media", files=files, data=data_fields)
        resp.raise_for_status()
        return resp.json()

    def _normalize_read_response(self, raw: dict, resource_id: str) -> CMSResource:
        """将 WordPress REST API 响应归一化为 CMSResource"""
        slug = raw.get("slug", "")
        link = raw.get("link", "")
        status = raw.get("status", "draft")
        post_type = raw.get("type", "post")
        resource_type_map = {
            "post": CMSResourceType.POST,
            "page": CMSResourceType.PAGE,
            "attachment": CMSResourceType.MEDIA,
        }
        resource_type = resource_type_map.get(post_type, CMSResourceType.OTHER)

        # SEO 元数据（Yoast / RankMath 兼容）
        seo_meta = {}
        if "_yoast_wpseo_title" in raw or "yoast_head_json" in raw:
            seo_meta["title"] = raw.get("_yoast_wpseo_title", raw.get("yoast_head_json", {}).get("title", ""))
            seo_meta["description"] = raw.get("_yoast_wpseo_metadesc", raw.get("yoast_head_json", {}).get("description", ""))
        if "rank_math_title" in raw:
            seo_meta["title"] = raw.get("rank_math_title", "")
            seo_meta["description"] = raw.get("rank_math_description", "")

        # Categories & Tags
        categories = [str(c) for c in raw.get("categories", [])]
        tags = [str(t) for t in raw.get("tags", [])]

        # Rendered content (WP 5.0+ Gutenberg 使用 rendered body)
        content = raw.get("content", {}).get("rendered", "") if isinstance(raw.get("content"), dict) else raw.get("content", "")
        excerpt = raw.get("excerpt", {}).get("rendered", "") if isinstance(raw.get("excerpt"), dict) else raw.get("excerpt", "")

        return CMSResource(
            resource_id=resource_id,
            resource_type=resource_type,
            platform=self.platform,
            title=raw.get("title", {}).get("rendered", "") if isinstance(raw.get("title"), dict) else raw.get("title", ""),
            content=content,
            slug=slug,
            status=status,
            metadata={
                "author": raw.get("author"),
                "comment_status": raw.get("comment_status"),
                "ping_status": raw.get("ping_status"),
                "featured_media": raw.get("featured_media"),
                "menu_order": raw.get("menu_order"),
                "template": raw.get("template"),
            },
            seo_title=seo_meta.get("title", ""),
            seo_description=seo_meta.get("description", ""),
            tags=tags,
            categories=categories,
            created_at=raw.get("date", ""),
            updated_at=raw.get("modified", ""),
            url=link,
            raw=raw,
        )

    def to_platform_format(self, data: dict, operation: str) -> dict:
        """将通用 CMS 数据转换为 WordPress REST API 格式"""
        wp_data = {}
        if "title" in data:
            wp_data["title"] = data["title"]
        if "content" in data:
            wp_data["content"] = data["content"]
        if "slug" in data:
            wp_data["slug"] = data["slug"]
        if "status" in data:
            wp_data["status"] = data["status"]  # publish, draft, private
        if "categories" in data:
            wp_data["categories"] = data["categories"]
        if "tags" in data:
            wp_data["tags"] = data["tags"]
        if "featured_media" in data:
            wp_data["featured_media"] = data["featured_media"]
        if "seo_title" in data:
            wp_data["_yoast_wpseo_title"] = data["seo_title"]
        if "seo_description" in data:
            wp_data["_yoast_wpseo_metadesc"] = data["seo_description"]
        # Meta fields
        for key in ["author", "date", "comment_status"]:
            if key in data:
                wp_data[key] = data[key]
        return wp_data

    # ── WordPress 专属方法 ─────────────────────────────────────────────────

    async def get_seo_metadata(self, resource_id: str) -> dict:
        """获取 SEO 元数据（Yoast / RankMath）"""
        result = await self.read(resource_id)
        if result.success:
            raw = result.raw_response or {}
            return {
                "yoast": {
                    "title": raw.get("_yoast_wpseo_title", ""),
                    "description": raw.get("_yoast_wpseo_metadesc", ""),
                    "focus_keyword": raw.get("_yoast_wpseo_focuskw", ""),
                },
                "rankmath": {
                    "title": raw.get("rank_math_title", ""),
                    "description": raw.get("rank_math_description", ""),
                    "focus_keyword": raw.get("rank_math_focus_keyword", ""),
                },
            }
        return {}

    async def update_seo(self, resource_id: str, seo_data: dict) -> CMSResult:
        """批量更新 SEO 元数据"""
        wp_data = {}
        if "yoast_title" in seo_data:
            wp_data["_yoast_wpseo_title"] = seo_data["yoast_title"]
        if "yoast_description" in seo_data:
            wp_data["_yoast_wpseo_metadesc"] = seo_data["yoast_description"]
        if "yoast_keyword" in seo_data:
            wp_data["_yoast_wpseo_focuskw"] = seo_data["yoast_keyword"]
        if "rankmath_title" in seo_data:
            wp_data["rank_math_title"] = seo_data["rankmath_title"]
        if "rankmath_description" in seo_data:
            wp_data["rank_math_description"] = seo_data["rankmath_description"]
        return await self.update(resource_id, wp_data, CMSResourceType.POST)

    async def bulk_update_seo(self, post_ids: list[str], seo_batch: list[dict]) -> list[CMSResult]:
        """批量更新 SEO 元数据（幂等执行）"""
        results = []
        for post_id, seo_data in zip(post_ids, seo_batch):
            result = await self.update_seo(post_id, seo_data)
            results.append(result)
        return results
