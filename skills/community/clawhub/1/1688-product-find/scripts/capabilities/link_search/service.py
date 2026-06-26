# -*- coding: utf-8 -*-
"""
链接搜索能力实现
解析商品链接，提取商品主图后搜索同款
"""

import os
import re
import ssl
import gzip
import urllib.request
import urllib.error
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urlparse, parse_qs

from _http import search_products
from _errors import ServiceError

# 通用请求头
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}


class LinkParser:
    """链接解析器"""
    
    # 平台 URL 模板
    PLATFORM_URL_TEMPLATES = {
        "1688": "https://detail.1688.com/offer/{product_id}.html",
        "taobao": "https://item.taobao.com/item.htm?id={product_id}",
        "tmall": "https://detail.tmall.com/item.htm?id={product_id}"
    }
    
    # 商品 ID 正则规则
    PRODUCT_ID_PATTERNS = {
        "1688": r"^\d{6,12}$",
        "taobao": r"^[a-zA-Z0-9]{8,12}$",
        "tmall": r"^[a-zA-Z0-9]{8,12}$"
    }
    
    def parse(self, url_or_id: str) -> Dict[str, str]:
        """
        解析商品链接或 ID
        
        Args:
            url_or_id: 商品链接或纯 ID
            
        Returns:
            包含 platform, product_id, canonical_url 的字典
        """
        # 尝试匹配纯 ID
        if self._is_pure_id(url_or_id):
            return self._parse_pure_id(url_or_id)
        
        # 解析 URL
        return self._parse_url(url_or_id)
    
    def _is_pure_id(self, text: str) -> bool:
        """判断是否是纯 ID"""
        if "://" in text or "." in text:
            return False
        return True
    
    def _parse_pure_id(self, product_id: str) -> Dict[str, str]:
        """解析纯商品 ID"""
        # 1688: 6-12 位纯数字
        if re.match(self.PRODUCT_ID_PATTERNS["1688"], product_id):
            return {
                "platform": "1688",
                "product_id": product_id,
                "canonical_url": self.PLATFORM_URL_TEMPLATES["1688"].format(
                    product_id=product_id
                )
            }
        
        # 淘宝/天猫：8-12 位字母数字
        if re.match(self.PRODUCT_ID_PATTERNS["taobao"], product_id):
            return {
                "platform": "taobao",
                "product_id": product_id,
                "canonical_url": self.PLATFORM_URL_TEMPLATES["taobao"].format(
                    product_id=product_id
                )
            }
        
        raise ValueError(f"无法识别的商品 ID 格式：{product_id}")
    
    def _parse_url(self, url: str) -> Dict[str, str]:
        """解析商品 URL"""
        parsed = urlparse(url)
        
        # 1688
        if "1688.com" in parsed.netloc:
            match = re.search(r'/offer/(\d+)', parsed.path)
            if match:
                product_id = match.group(1)
                return {
                    "platform": "1688",
                    "product_id": product_id,
                    "canonical_url": self.PLATFORM_URL_TEMPLATES["1688"].format(
                        product_id=product_id
                    )
                }
            raise ValueError(f"无效的 1688 链接：{url}")
        
        # 淘宝
        elif "taobao.com" in parsed.netloc or "tb.cn" in parsed.netloc:
            qs = parse_qs(parsed.query)
            if "id" in qs:
                product_id = qs["id"][0]
                return {
                    "platform": "taobao",
                    "product_id": product_id,
                    "canonical_url": self.PLATFORM_URL_TEMPLATES["taobao"].format(
                        product_id=product_id
                    )
                }
            raise ValueError(f"无效的淘宝链接：{url}")
        
        # 天猫
        elif "tmall.com" in parsed.netloc:
            qs = parse_qs(parsed.query)
            if "id" in qs:
                product_id = qs["id"][0]
                return {
                    "platform": "tmall",
                    "product_id": product_id,
                    "canonical_url": self.PLATFORM_URL_TEMPLATES["tmall"].format(
                        product_id=product_id
                    )
                }
            raise ValueError(f"无效的天猫链接：{url}")
        
        else:
            raise ValueError(f"不支持的电商平台：{parsed.netloc}")


class ProductImageExtractor:
    """商品主图提取器"""
    
    def extract_main_image(self, url: str, platform: str = "1688") -> Optional[str]:
        """
        尝试从商品页面静默提取主图
        
        Args:
            url: 商品链接
            platform: 平台标识 (1688/taobao/tmall)
            
        Returns:
            商品主图 URL，如果无法获取则返回 None
        """
        try:
            html = self._fetch_page_content(url)
            
            if platform == "1688":
                return self._extract_1688_main_image(html)
            elif platform in ("taobao", "tmall"):
                return self._extract_taobao_main_image(html)
            
            return None
        except Exception:
            return None
    
    def _fetch_page_content(self, url: str) -> str:
        """获取网页内容"""
        req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
        
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            content_encoding = response.headers.get('Content-Encoding', '')
            data = response.read()
            
            if 'gzip' in content_encoding:
                data = gzip.decompress(data)
            
            charset = 'utf-8'
            content_type = response.headers.get('Content-Type', '')
            if 'charset=' in content_type:
                charset = content_type.split('charset=')[-1].split(';')[0].strip()
            
            return data.decode(charset, errors='ignore')
    
    def _normalize_image_url(self, img_url: str) -> str:
        """规范化图片 URL"""
        if not img_url:
            return ''
        
        img_url = img_url.strip()
        
        # 补全协议
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        
        # 阿里系图片：去除尺寸后缀获取原图
        if 'alicdn.com' in img_url:
            img_url = re.sub(r'_\d+x\d+\.[a-zA-Z]+$', '', img_url)
            img_url = re.sub(r'_\.webp$', '', img_url)
            img_url = re.sub(r'\?.*$', '', img_url)
        
        return img_url
    
    def _is_video_url(self, url: str) -> bool:
        """判断是否是视频 URL"""
        if not url:
            return False
        url_lower = url.lower()
        video_indicators = ['.mp4', '.mov', '.avi', '.webm', 'video', 'cloud.video']
        return any(indicator in url_lower for indicator in video_indicators)
    
    def _is_valid_product_image(self, img_url: str) -> bool:
        """判断是否是有效的商品主图（排除小图标、logo 等）"""
        if not img_url:
            return False
        
        url_lower = img_url.lower()
        
        # 排除明确的非商品图
        exclude_keywords = [
            'icon', 'logo', 'sprite', 'avatar', 'badge', 'btn', 'button',
            'loading', 'placeholder', 'background', 'banner', 'ad_', 'advert',
            'cms/upload', '/tfs/',
        ]
        for keyword in exclude_keywords:
            if keyword in url_lower:
                return False
        
        # 排除太小的图片（通过 URL 中的尺寸判断）
        # tps-width-height 格式
        tps_match = re.search(r'tps-(\d+)-(\d+)', url_lower)
        if tps_match:
            width, height = int(tps_match.group(1)), int(tps_match.group(2))
            if width < 400 or height < 400:
                return False
            ratio = width / height if height > 0 else 0
            if ratio > 3 or ratio < 0.33:
                return False
        
        # _widthxheight 格式
        size_match = re.search(r'[_-](\d+)x(\d+)', url_lower)
        if size_match:
            width, height = int(size_match.group(1)), int(size_match.group(2))
            if width < 400 or height < 400:
                return False
            ratio = width / height if height > 0 else 0
            if ratio > 3 or ratio < 0.33:
                return False
        
        # XXX-width-height 格式
        suffix_match = re.search(r'-(\d+)-(\d+)\.[a-z]+$', url_lower)
        if suffix_match:
            width, height = int(suffix_match.group(1)), int(suffix_match.group(2))
            if width < 400 or height < 400:
                return False
        
        return True
    
    def _extract_1688_main_image(self, html: str) -> Optional[str]:
        """
        从 1688 商品页面提取主图
        
        1688 主图位置：页面左侧商品图片轮播区域的第一张静态图片
        - 主图通常在 ibank 目录下（cbu01.alicdn.com/img/ibank/）
        """
        # 方法 1: 优先从 ibank 图片 URL 中提取
        ibank_pattern = r'(https?:)?//cbu01\.alicdn\.com/img/ibank/[^"\s\'\)]+\.(jpg|jpeg|png|webp)'
        for m in re.finditer(ibank_pattern, html, re.IGNORECASE):
            img_url = m.group(0)
            normalized = self._normalize_image_url(img_url)
            if not self._is_video_url(normalized) and self._is_valid_product_image(normalized):
                return normalized
        
        # 方法 2: 从 JSON 数据中提取 images 数组
        json_patterns = [
            r'"offerDetail"\s*:\s*\{[^}]*"images"\s*:\s*\[([^\]]+)\]',
            r'"images"\s*:\s*\["([^"]+)"',
        ]
        
        for pattern in json_patterns:
            match = re.search(pattern, html)
            if match:
                content = match.group(1)
                img_pattern = r'(https?:)?//[^"\s,\]]+\.(jpg|jpeg|png|webp)'
                for img_match in re.finditer(img_pattern, content, re.IGNORECASE):
                    img_url = img_match.group(0)
                    normalized = self._normalize_image_url(img_url)
                    if not self._is_video_url(normalized) and self._is_valid_product_image(normalized):
                        return normalized
        
        # 方法 3: 从 cbu01.alicdn.com 提取其他商品图
        cbu_pattern = r'(https?:)?//cbu01\.alicdn\.com/[^"\s\'\)]+\.(jpg|jpeg|png|webp)'
        for m in re.finditer(cbu_pattern, html, re.IGNORECASE):
            img_url = m.group(0)
            normalized = self._normalize_image_url(img_url)
            if not self._is_video_url(normalized) and self._is_valid_product_image(normalized):
                return normalized
        
        # 方法 4: 从 img.alicdn.com/imgextra 提取
        imgextra_pattern = r'(https?:)?//img\.alicdn\.com/imgextra/[^"\s\'\)]+\.(jpg|jpeg|png|webp)'
        for m in re.finditer(imgextra_pattern, html, re.IGNORECASE):
            img_url = m.group(0)
            normalized = self._normalize_image_url(img_url)
            if not self._is_video_url(normalized) and self._is_valid_product_image(normalized):
                return normalized
        
        return None
    
    def _extract_taobao_main_image(self, html: str) -> Optional[str]:
        """
        从淘宝/天猫商品页面提取主图
        
        淘宝/天猫主图位置：页面左侧商品图片展示区域的主图
        - 主图通常在 JSON 数据的 pic 或 images 字段中
        """
        # 方法 1: 从 JSON 数据中提取主图 pic 字段
        pic_patterns = [
            r'"pic"\s*:\s*"([^"]+)"',
            r'"picUrl"\s*:\s*"([^"]+)"',
            r'"mainPic"\s*:\s*"([^"]+)"',
            r'"images"\s*:\s*\["([^"]+)"',
        ]
        
        for pattern in pic_patterns:
            match = re.search(pattern, html)
            if match:
                img_url = match.group(1)
                if img_url and not self._is_video_url(img_url):
                    normalized = self._normalize_image_url(img_url)
                    if self._is_valid_product_image(normalized):
                        return normalized
        
        # 方法 2: 从主图展示区域提取 alicdn 大图
        main_img_pattern = r'(https?:)?//img\.alicdn\.com/[^"\s\'\)]+\.(jpg|jpeg|png|webp)'
        for m in re.finditer(main_img_pattern, html, re.IGNORECASE):
            img_url = m.group(0)
            if self._is_valid_product_image(img_url):
                return self._normalize_image_url(img_url)
        
        # 方法 3: 从 gw.alicdn.com 提取（天猫常用）
        gw_pattern = r'(https?:)?//gw\.alicdn\.com/[^"\s\'\)]+\.(jpg|jpeg|png|webp)'
        for m in re.finditer(gw_pattern, html, re.IGNORECASE):
            img_url = m.group(0)
            if self._is_valid_product_image(img_url):
                return self._normalize_image_url(img_url)
        
        return None


class LinkSearchExecutor:
    """链接搜索执行器"""
    
    def __init__(self, platform: str = "1688"):
        self.platform = platform
        self.parser = LinkParser()
        self.image_extractor = ProductImageExtractor()
    
    def search(self, url: str, limit: int = 10,
               sort_type: str = None, score_level: str = "high",
               purchase_amount: int = 1,
               tags: str = "4306497", ic_tags: str = None) -> Dict[str, Any]:
        """
        执行链接搜索
        
        Args:
            url: 商品链接或 ID
            limit: 返回数量
            sort_type: 排序类型（price_asc/price_desc/sold_desc/yx_desc）
            score_level: 相关性档位（high/medium/low）
            purchase_amount: 采购件数
            tags: TC标（品池标签），英文逗号分隔
            ic_tags: IC标（品池标签），英文逗号分隔
            
        Returns:
            搜索结果
        """
        # 解析链接
        parsed = self.parser.parse(url)
        canonical_url = parsed["canonical_url"]
        
        # 尝试静默获取商品主图
        main_image_url = self.image_extractor.extract_main_image(canonical_url, parsed["platform"])
        
        if main_image_url:
            # 成功获取主图，调用 API 搜索
            results = self._search_via_api(main_image_url, limit, sort_type, score_level, purchase_amount,
                                              tags=tags, ic_tags=ic_tags)
            return {
                "success": True,
                "source_url": url,
                "source_image": main_image_url,
                "similar_products": results,
                "search_type": "link_search",
                "total_results": len(results)
            }
        else:
            # 无法获取主图，返回需要用户输入的信号
            return {
                "success": False,
                "source_url": url,
                "action": "need_image_url",
                "message": "无法自动获取商品主图，请手动输入商品图片 URL",
                "similar_products": [],
                "search_type": "link_search",
                "total_results": 0
            }
    
    def search_with_image(self, image_url: str, limit: int = 10,
                          sort_type: str = None, score_level: str = "high",
                          purchase_amount: int = 1,
                          tags: str = "4306497", ic_tags: str = None) -> Dict[str, Any]:
        """
        使用指定的图片 URL 搜索（当自动获取失败时使用）
        
        Args:
            image_url: 商品图片 URL
            limit: 返回数量
            sort_type: 排序类型（price_asc/price_desc/sold_desc/yx_desc）
            score_level: 相关性档位（high/medium/low）
            purchase_amount: 采购件数
            tags: TC标（品池标签），英文逗号分隔
            ic_tags: IC标（品池标签），英文逗号分隔
            
        Returns:
            搜索结果
        """
        results = self._search_via_api(image_url, limit, sort_type, score_level, purchase_amount,
                                         tags=tags, ic_tags=ic_tags)
        return {
            "success": True,
            "source_image": image_url,
            "similar_products": results,
            "search_type": "link_search",
            "total_results": len(results)
        }
    
    def _search_via_api(self, image_url: str, limit: int,
                        sort_type: str = None, score_level: str = "high",
                        purchase_amount: int = 1,
                        tags: str = "4306497", ic_tags: str = None) -> List[Dict]:
        """通过 API 搜索（使用图片 URL）"""
        request = {
            "imageUrl": image_url,
            "pageSize": limit,
            "purchaseAmount": purchase_amount
        }
        # 排序类型（可选）
        if sort_type:
            request["sortType"] = sort_type
        
        # 相关性档位（默认 high）
        if score_level:
            request["scoreLevel"] = score_level
        
        # 品池标签
        if tags:
            request["tags"] = tags
        if ic_tags:
            request["icTags"] = ic_tags
        
        return search_products(request)


# ========== 主入口函数 ==========

def link_search(url: str, platform: str = "1688", limit: int = 10,
                sort_type: str = None, score_level: str = "high",
                purchase_amount: int = 1,
                tags: str = "4306497", ic_tags: str = None) -> Dict[str, Any]:
    """
    链接搜索主函数
    
    Args:
        url: 商品链接或 ID
        platform: 目标平台（可选，会自动识别）
        limit: 返回数量
        sort_type: 排序类型（price_asc/price_desc/sold_desc/yx_desc）
        score_level: 相关性档位（high/medium/low）
        purchase_amount: 采购件数
        tags: TC标（品池标签），英文逗号分隔，默认 "4306497"
        ic_tags: IC标（品池标签），英文逗号分隔
        
    Returns:
        搜索结果
    """
    executor = LinkSearchExecutor(platform=platform)
    return executor.search(url=url, limit=limit,
                           sort_type=sort_type, score_level=score_level,
                           purchase_amount=purchase_amount,
                           tags=tags, ic_tags=ic_tags)


def link_search_with_image(image_url: str, limit: int = 10,
                           sort_type: str = None, score_level: str = "high",
                           purchase_amount: int = 1,
                           tags: str = "4306497", ic_tags: str = None) -> Dict[str, Any]:
    """
    使用指定图片 URL 进行链接搜索（当自动获取主图失败时使用）
    
    Args:
        image_url: 商品图片 URL
        limit: 返回数量
        sort_type: 排序类型（price_asc/price_desc/sold_desc/yx_desc）
        score_level: 相关性档位（high/medium/low）
        purchase_amount: 采购件数
        tags: TC标（品池标签），英文逗号分隔，默认 "4306497"
        ic_tags: IC标（品池标签），英文逗号分隔
        
    Returns:
        搜索结果
    """
    executor = LinkSearchExecutor()
    return executor.search_with_image(image_url=image_url, limit=limit,
                                      sort_type=sort_type, score_level=score_level,
                                      purchase_amount=purchase_amount,
                                      tags=tags, ic_tags=ic_tags)


if __name__ == "__main__":
    # 测试示例
    test_url = "https://detail.1688.com/offer/895657286458.html"
    result = link_search(test_url)
    print(f"搜索链接：{test_url}")
    print(f"成功：{result['success']}")
    if result['success']:
        print(f"找到 {result['total_results']} 个相似商品")
    else:
        print(f"提示：{result.get('message')}")
