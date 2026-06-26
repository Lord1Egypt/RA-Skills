# -*- coding: utf-8 -*-
"""
商品比价能力实现

基于商品图片搜索同款商品，自动选出代表性商品进行纵向对比。
选品策略：销量最高、价格最低、综合最优各选 1 款（去重），不足时按相似度补齐。
"""

import json
import logging
from typing import Dict, List, Any

from _errors import ServiceError
from _image import ImagePreprocessor
from capabilities.image_search.service import ImageSearchExecutor

# 复用 link_search 的链接解析和主图提取能力
from capabilities.link_search.service import LinkParser, ProductImageExtractor

logger = logging.getLogger("1688_compare")


# ── 选品策略 ─────────────────────────────────────────────────────────────────

def _count_service_tags(product: dict) -> int:
    """统计商品的服务标签 + 卖点标签总数，作为服务质量的量化指标"""
    count = 0
    for key in ("service_infos", "selling_points"):
        for item in (product.get(key) or []):
            try:
                data = json.loads(item) if isinstance(item, str) else item
                if data.get("value"):
                    count += 1
            except (json.JSONDecodeError, AttributeError):
                continue
    return count


def _select_top(products: List[Dict], limit: int = 3) -> List[Dict]:
    """
    从候选商品中按三个维度各选 1 款（独立评估），去重合并标签后返回。
    当同一商品赢得多个维度时，合并标签（如 "价格最低 且 综合最优"）。
    最终返回去重后的商品列表，数量可能小于 limit（1~3 款）。

    维度与标签：
      1. 销量最高 → 按 sold_count 降序
      2. 价格最低 → 按 price 升序（排除无价格）
      3. 综合最优 → 按 yx_index 降序
    """
    if not products:
        return []

    # ── 独立评估每个维度的最佳商品（不互斥） ──
    dimension_winners = []  # [(product, label)]

    # 维度 1：销量最高
    by_sales = sorted(products, key=lambda p: int(p.get("sold_count") or 0), reverse=True)
    if by_sales:
        dimension_winners.append((by_sales[0], "销量最高"))

    # 维度 2：价格最低（排除无价格）
    priced = [p for p in products if p.get("price") is not None]
    if priced:
        by_price = sorted(priced, key=lambda p: float(p["price"]))
        dimension_winners.append((by_price[0], "价格最低"))

    # 维度 3：综合最优（按 yx_index 降序）
    by_yx = sorted(products, key=lambda p: float(p.get("yx_index") or 0), reverse=True)
    if by_yx:
        dimension_winners.append((by_yx[0], "综合最优"))

    # ── 合并同一商品的多个标签 ──
    label_map: Dict[str, List[str]] = {}   # product_id -> [labels]
    ordered_products: List[Dict] = []       # 按维度优先级去重

    for product, label in dimension_winners:
        pid = product.get("product_id")
        if pid in label_map:
            label_map[pid].append(label)
        else:
            label_map[pid] = [label]
            ordered_products.append(product)

    # 设置合并后的标签
    for p in ordered_products:
        pid = p.get("product_id")
        labels = label_map.get(pid, ["推荐"])
        p["_compare_label"] = " 且 ".join(labels)

    # 直接返回维度胜出的商品（不填充），数量由实际去重结果决定
    return ordered_products[:limit]


# ── 搜索与比价 ───────────────────────────────────────────────────────────────

class CompareExecutor:
    """商品比价执行器"""

    def __init__(self, platform: str = "1688"):
        self.platform = platform
        self.preprocessor = ImagePreprocessor()
        self._search_executor = ImageSearchExecutor(platform=platform)

    def compare(self, image: str = None, url: str = None,
                query: str = None,
                limit: int = 3, sort_type: str = None,
                score_level: str = "high",
                purchase_amount: int = 1,
                tags: str = "4306497", ic_tags: str = None) -> Dict[str, Any]:
        """
        执行比价：图片预处理 → 以图搜图 → 选品 → 返回比价结构

        支持两种输入方式（二选一）：
        1. image: 商品图片 URL 或本地路径
        2. url: 商品链接或 ID（自动解析链接并提取主图）

        Args:
            image: 商品图片 URL 或本地路径
            url: 商品链接或商品 ID（1688/淘宝/天猫）
            query: 附加关键词（规格、品类等，可选）
            limit: 对比商品数量
            sort_type: 排序类型（price_asc/price_desc/sold_desc/yx_desc）
            score_level: 相关性档位（high/medium/low）
            purchase_amount: 采购件数
            tags: TC标（品池标签），英文逗号分隔
            ic_tags: IC标（品池标签），英文逗号分隔

        Returns:
            比价结果
        """
        # 输入校验：image 和 url 二选一
        if not image and not url:
            raise ValueError("必须提供 --image 或 --url 参数")

        # 如果提供了商品链接，解析链接并提取主图
        source_url = None
        if url and not image:
            image, source_url = self._extract_image_from_link(url)

        # 预处理图片（复用共享 ImagePreprocessor）
        img_info = self.preprocessor.preprocess(image)
        
        # 固定搜索 20 条候选，确保三维度选品有足够样本
        search_limit = 20

        # 构建额外参数（附加关键词）
        extra = {}
        if query:
            extra["query"] = query
        
        # 复用 ImageSearchExecutor 的搜索方法
        all_products = self._search_executor._search_via_api(
            img_info, search_limit, sort_type, score_level, purchase_amount,
            extra_params=extra if extra else None,
            tags=tags, ic_tags=ic_tags
        )

        if not all_products:
            result = {
                "success": True,
                "source_image": image,
                "compare_products": [],
                "search_type": "compare",
                "total_candidates": 0,
                "total_compared": 0,
            }
            if source_url:
                result["source_url"] = source_url
            return result

        # 过滤空数据
        valid = [p for p in all_products if p.get("title") or p.get("detail_url")]

        # 选品
        top = _select_top(valid, limit)

        result = {
            "success": True,
            "source_image": image,
            "compare_products": top,
            "search_type": "compare",
            "total_candidates": len(valid),
            "total_compared": len(top),
        }
        if source_url:
            result["source_url"] = source_url
        return result
    
    def _extract_image_from_link(self, url: str) -> tuple:
        """
        从商品链接中解析并提取主图

        Args:
            url: 商品链接或商品 ID

        Returns:
            (image_url, source_url) 元组

        Raises:
            ServiceError: 无法提取主图时抛出
        """
        parser = LinkParser()
        extractor = ProductImageExtractor()

        parsed = parser.parse(url)
        canonical_url = parsed["canonical_url"]

        main_image = extractor.extract_main_image(canonical_url, parsed["platform"])
        if not main_image:
            raise ServiceError(
                f"无法自动获取商品主图，请改用 --image 参数直接提供图片 URL\n"
                f"示例：compare --image \"图片URL\" --url \"{url}\""
            )

        logger.info("从链接提取主图: %s → %s", url, main_image)
        return main_image, canonical_url


# ========== 主入口函数 ==========

def compare_products(image: str = None, url: str = None,
                     query: str = None,
                     platform: str = "1688", limit: int = 3,
                     sort_type: str = None, score_level: str = "high",
                     purchase_amount: int = 1,
                     tags: str = "4306497", ic_tags: str = None) -> Dict[str, Any]:
    """
    商品比价主函数

    支持两种输入方式（二选一）：
    1. image: 商品图片 URL 或本地路径
    2. url: 商品链接或商品 ID（自动解析并提取主图后比价）

    Args:
        image: 商品图片 URL 或本地路径
        url: 商品链接或商品 ID（1688/淘宝/天猫）
        query: 附加关键词（规格、品类等，可选）
        platform: 目标平台
        limit: 对比商品数量
        sort_type: 排序类型（price_asc/price_desc/sold_desc/yx_desc）
        score_level: 相关性档位（high/medium/low）
        purchase_amount: 采购件数
        tags: TC标（品池标签），英文逗号分隔，默认 "4306497"
        ic_tags: IC标（品池标签），英文逗号分隔

    Returns:
        比价结果
    """
    executor = CompareExecutor(platform=platform)
    return executor.compare(image=image, url=url, query=query, limit=limit,
                            sort_type=sort_type, score_level=score_level,
                            purchase_amount=purchase_amount,
                            tags=tags, ic_tags=ic_tags)


if __name__ == "__main__":
    import os
    # 测试示例
    test_image = "/workspace/test_product.jpg"
    if os.path.exists(test_image):
        result = compare_products(test_image)
        print(f"从 {result['total_candidates']} 个同款中选出 {result['total_compared']} 款对比")
    else:
        print(f"测试图片不存在：{test_image}")
