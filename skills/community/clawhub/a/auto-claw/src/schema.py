"""
Schema.org Generator — WordPress 结构化数据自动生成
为文章/产品/本地商家生成符合 Google 标准的 JSON-LD
支持类型：Article, Product, LocalBusiness, Organization, FAQPage, BreadcrumbList
"""
import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class SchemaData:
    """单个页面的 Schema.org 数据"""
    page_url: str
    page_type: str  # article/product/local/org/faq
    json_ld: Dict[str, Any] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    injection_code: str = ""  # 可直接注入 HTML 的代码
    
    def is_valid(self) -> bool:
        return bool(self.json_ld.get("@context")) and bool(self.json_ld.get("@type"))

class SchemaGenerator:
    """
    Schema.org 结构化数据生成器
    
    支持的 Schema 类型：
    - Article: 博客文章
    - Product: WooCommerce 产品
    - LocalBusiness: 本地商家
    - Organization: 组织
    - FAQPage: 常见问题
    - BreadcrumbList: 面包屑导航
    - WebSite: 网站
    """
    
    CONTEXT = "https://schema.org"
    
    def __init__(self, site_name: str, site_url: str, logo_url: str = ""):
        self.site_name = site_name
        self.site_url = site_url.rstrip("/")
        self.logo_url = logo_url
        self.generated: List[SchemaData] = []
    
    def detect_page_type(self, url: str, title: str = "", content: str = "", h1s: List[str] = None) -> str:
        """根据 URL 和内容类型检测页面 Schema 类型"""
        url_lower = url.lower()
        
        if "/product/" in url_lower or "/shop/" in url_lower:
            return "product"
        elif "/faq" in url_lower or "question" in url_lower:
            return "faq"
        elif "/about" in url_lower:
            return "organization"
        elif "/contact" in url_lower or "/location" in url_lower:
            return "local"
        elif "/blog/" in url_lower or "/post/" in url_lower or h1s:
            return "article"
        else:
            return "article"  # 默认
    
    def generate_article(self, url: str, title: str, description: str = "", 
                          author: str = "", published_date: str = "",
                          modified_date: str = "", image_url: str = "",
                          publisher_name: str = "", publisher_logo: str = "") -> SchemaData:
        """生成 Article Schema"""
        schema = SchemaData(page_url=url, page_type="article")
        
        data = {
            "@context": self.CONTEXT,
            "@type": "Article",
            "headline": title[:110],
            "url": url,
        }
        
        if description:
            data["description"] = description[:200]
        
        if author:
            data["author"] = {"@type": "Person", "name": author}
        
        if published_date:
            data["datePublished"] = published_date
        
        if modified_date:
            data["dateModified"] = modified_date
        
        if image_url:
            data["image"] = {"@type": "ImageObject", "url": image_url}
        
        if publisher_name:
            pub = {"@type": "Organization", "name": publisher_name}
            if publisher_logo:
                pub["logo"] = {"@type": "ImageObject", "url": publisher_logo}
            data["publisher"] = pub
        
        # 必填字段检查
        if not title:
            schema.issues.append("Missing headline/title")
        if not url:
            schema.issues.append("Missing URL")
        
        schema.json_ld = data
        schema.injection_code = self._wrap_script(data)
        
        return schema
    
    def generate_product(self, url: str, name: str, description: str = "",
                         sku: str = "", brand: str = "", price: str = "",
                         currency: str = "USD", availability: str = "InStock",
                         image_url: str = "", rating: str = "",
                         review_count: str = "") -> SchemaData:
        """生成 Product Schema（WooCommerce）"""
        schema = SchemaData(page_url=url, page_type="product")
        
        data = {
            "@context": self.CONTEXT,
            "@type": "Product",
            "name": name[:100],
            "url": url,
        }
        
        if description:
            data["description"] = description[:500]
        
        if sku:
            data["sku"] = sku
        
        if brand:
            data["brand"] = {"@type": "Brand", "name": brand}
        
        if price:
            data["offers"] = {
                "@type": "Offer",
                "price": price,
                "priceCurrency": currency,
                "availability": f"https://schema.org/{availability}",
            }
        
        if image_url:
            data["image"] = image_url
        
        if rating:
            data["aggregateRating"] = {
                "@type": "AggregateRating",
                "ratingValue": rating,
                "reviewCount": review_count or "1"
            }
        
        schema.json_ld = data
        schema.injection_code = self._wrap_script(data)
        
        return schema
    
    def generate_faq(self, url: str, title: str, faqs: List[Dict[str, str]]) -> SchemaData:
        """
        生成 FAQPage Schema
        faqs = [{"question": "...", "answer": "..."}, ...]
        """
        schema = SchemaData(page_url=url, page_type="faq")
        
        qas = []
        for faq in faqs:
            q = faq.get("question", "")
            a = faq.get("answer", "")
            if q and a:
                qas.append({
                    "@type": "Question",
                    "name": q[:200],
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": a[:1000]
                    }
                })
        
        data = {
            "@context": self.CONTEXT,
            "@type": "FAQPage",
            "mainEntity": qas
        }
        
        schema.json_ld = data
        schema.injection_code = self._wrap_script(data)
        
        return schema
    
    def generate_breadcrumb(self, url: str, items: List[Dict[str, str]]) -> SchemaData:
        """
        生成 BreadcrumbList Schema
        items = [{"name": "Home", "url": "/"}, {"name": "Category", "url": "/category"}]
        """
        schema = SchemaData(page_url=url, page_type="breadcrumb")
        
        path_items = []
        for i, item in enumerate(items):
            path_items.append({
                "@type": "ListItem",
                "position": i + 1,
                "name": item.get("name", ""),
                "item": self.site_url + item.get("url", "")
            })
        
        data = {
            "@context": self.CONTEXT,
            "@type": "BreadcrumbList",
            "itemListElement": path_items
        }
        
        schema.json_ld = data
        schema.injection_code = self._wrap_script(data)
        
        return schema
    
    def generate_website(self, search_url: str = "") -> SchemaData:
        """生成 WebSite Schema"""
        schema = SchemaData(page_url=self.site_url, page_type="website")
        
        data = {
            "@context": self.CONTEXT,
            "@type": "WebSite",
            "name": self.site_name,
            "url": self.site_url,
        }
        
        if search_url:
            data["potentialAction"] = {
                "@type": "SearchAction",
                "target": {
                    "@type": "EntryPoint",
                    "urlTemplate": search_url
                },
                "query-input": "required name=search_term_string"
            }
        
        schema.json_ld = data
        schema.injection_code = self._wrap_script(data)
        
        return schema
    
    def generate_organization(self, name: str, url: str = "", logo: str = "",
                             same_as: List[str] = None, contact_info: Dict = None) -> SchemaData:
        """生成 Organization Schema"""
        schema = SchemaData(page_url=url or self.site_url, page_type="organization")
        
        data = {
            "@context": self.CONTEXT,
            "@type": "Organization",
            "name": name,
            "url": url or self.site_url,
        }
        
        if logo or self.logo_url:
            data["logo"] = {"@type": "ImageObject", "url": logo or self.logo_url}
        
        if same_as:
            data["sameAs"] = same_as
        
        if contact_info:
            data["contactPoint"] = {
                "@type": "ContactPoint",
                **contact_info
            }
        
        schema.json_ld = data
        schema.injection_code = self._wrap_script(data)
        
        return schema
    
    def _wrap_script(self, data: Dict) -> str:
        """包装成 HTML <script> 标签"""
        return f'<script type="application/ld+json">\n{json.dumps(data, ensure_ascii=False, indent=2)}\n</script>'
    
    def generate_for_wordpress_page(self, url: str, title: str, page_content: str = "",
                                   h1s: List[str] = None, images: List[str] = None) -> List[SchemaData]:
        """
        为 WordPress 页面生成所有需要的 Schema
        自动检测页面类型，生成对应的 Schema
        """
        results = []
        
        # 1. WebSite（首页）
        if url == self.site_url or url == self.site_url + "/":
            website_schema = self.generate_website()
            results.append(website_schema)
            
            org_schema = self.generate_organization(
                name=self.site_name,
                url=self.site_url,
                logo=self.logo_url
            )
            results.append(org_schema)
        
        # 2. 检测页面类型
        page_type = self.detect_page_type(url, title, page_content, h1s)
        
        # 3. 根据类型生成
        if page_type == "article":
            # 提取第一段作为 description
            desc = ""
            if page_content:
                paragraphs = re.findall(r'<p[^>]*>([^<]+)</p>', page_content)
                if paragraphs:
                    desc = re.sub(r'<[^>]+>', '', paragraphs[0])[:200]
            
            article_schema = self.generate_article(
                url=url,
                title=title,
                description=desc,
                image_url=images[0] if images else ""
            )
            results.append(article_schema)
        
        elif page_type == "faq":
            # 从内容中提取 Q&A
            faqs = self._extract_faqs(page_content)
            if faqs:
                faq_schema = self.generate_faq(url, title, faqs)
                results.append(faq_schema)
        
        # 4. Breadcrumb（所有页面除了首页）
        if url != self.site_url and "/" in url.replace(self.site_url, ""):
            crumb_items = self._generate_breadcrumb_items(url)
            if len(crumb_items) > 1:
                breadcrumb = self.generate_breadcrumb(url, crumb_items)
                results.append(breadcrumb)
        
        self.generated.extend(results)
        return results
    
    def _extract_faqs(self, content: str) -> List[Dict[str, str]]:
        """从页面内容中提取 FAQ"""
        faqs = []
        
        # 尝试匹配 FAQ 格式
        patterns = [
            r'<h3[^>]*>([^<]*[??][^<]*)</h3>\s*<p[^>]*>([^<]+)</p>',
            r'<strong[^>]*>([^<]*[??][^<]*)</strong>\s*([^\n]+)',
            r'Q:\s*([^\n]+)\s*A:\s*([^\n]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if len(match) >= 2:
                    q = re.sub(r'<[^>]+>', '', match[0]).strip()
                    a = re.sub(r'<[^>]+>', '', match[1]).strip()
                    if q and a and len(q) > 5:
                        faqs.append({"question": q[:200], "answer": a[:500]})
        
        return faqs[:10]  # 最多10个
    
    def _generate_breadcrumb_items(self, url: str) -> List[Dict[str, str]]:
        """根据 URL 生成面包屑路径"""
        items = [{"name": "首页", "url": "/"}]
        
        path = url.replace(self.site_url, "").strip("/")
        if not path:
            return items
        
        parts = path.split("/")
        current_path = ""
        
        for part in parts[:-1]:  # 不包含最后一节（当前页面）
            current_path += "/" + part
            name = part.replace("-", " ").replace("_", " ").title()
            items.append({"name": name, "url": current_path})
        
        return items
    
    def export_injection_code(self, schemas: List[SchemaData]) -> str:
        """生成所有 Schema 的合并注入代码"""
        all_scripts = []
        for s in schemas:
            if s.injection_code:
                all_scripts.append(s.injection_code)
        
        return "\n\n".join(all_scripts)
    
    def validate_schema(self, schema: SchemaData) -> bool:
        """验证 Schema 是否符合 Google 结构化数据指南"""
        issues = []
        
        # 必填字段
        if not schema.json_ld.get("@context"):
            issues.append("Missing @context")
        if not schema.json_ld.get("@type"):
            issues.append("Missing @type")
        
        # Article 必填
        if schema.page_type == "article":
            if not schema.json_ld.get("headline"):
                issues.append("Article missing headline")
            if not schema.json_ld.get("datePublished"):
                issues.append("Article missing datePublished")
        
        # Product 必填
        if schema.page_type == "product":
            if not schema.json_ld.get("name"):
                issues.append("Product missing name")
            offers = schema.json_ld.get("offers", {})
            if not offers.get("price"):
                issues.append("Product missing price")
        
        schema.issues = issues
        return len(issues) == 0
