"""
SEO Fix Generator — 根据扫描结果生成优化代码
输出可直接粘贴到 WordPress 的修复建议
"""
import json
import hashlib
from typing import List, Dict, Any
try:
    from .seo import PageMeta, SEOReport
except ImportError:
    from seo import PageMeta, SEOReport  # noqa: F401

class SEOMetaGenerator:
    """
    根据扫描结果生成 SEO 优化内容
    """
    
    # Google 建议的标题和描述长度
    TITLE_MIN, TITLE_MAX = 30, 60
    DESC_MIN, DESC_MAX = 120, 160
    
    def __init__(self, page: PageMeta):
        self.page = page
    
    def suggest_title(self) -> str:
        """建议优化后的 title"""
        current = self.page.title or ""
        if self.page.h1:
            # 用 H1 作为基础
            title = self.page.h1[0]
        else:
            title = current
        
        title = title.strip()
        
        # 截断到合适长度
        if len(title) < self.TITLE_MIN:
            # 扩展：加上品牌名
            title = f"{title} | Auto Site"
        
        if len(title) > self.TITLE_MAX:
            title = title[:self.TITLE_MAX-3] + "..."
        
        return title
    
    def suggest_description(self) -> str:
        """建议 meta description"""
        # 从内容中提取前 155 个字符
        if self.page.h2s:
            # 用前两个 H2 构建描述
            desc_parts = []
            for h2 in self.page.h2s[:2]:
                desc_parts.append(h2.strip())
            desc = " - ".join(desc_parts)
        else:
            desc = self.page.title or ""
        
        desc = desc.strip()
        
        # 确保长度合适
        if len(desc) < self.DESC_MIN:
            desc = f"{desc}. Learn more about this topic on our site."
        
        if len(desc) > self.DESC_MAX:
            # 在句子边界截断
            desc = desc[:self.DESC_MAX-3].rsplit(".", 1)[0] + "."
        
        return desc
    
    def suggest_og_tags(self) -> Dict[str, str]:
        """生成 OG tags"""
        tags = {}
        
        title = self.suggest_title()
        desc = self.suggest_description()
        
        tags["og:title"] = title
        tags["og:description"] = desc
        tags["og:type"] = "article"
        tags["og:url"] = self.page.url
        tags["og:site_name"] = "Auto Site"
        
        return tags
    
    def suggest_schema_org(self) -> Dict[str, Any]:
        """生成 Schema.org JSON-LD"""
        url = self.page.url
        title = self.suggest_title()
        desc = self.suggest_description()
        
        return {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": desc,
            "url": url,
            "datePublished": "",
            "author": {
                "@type": "Organization",
                "name": "Auto Site"
            }
        }


class SEODiff:
    """
    生成 WordPress SEO 修复差异
    """
    
    def __init__(self, page: PageMeta, generator: SEOMetaGenerator):
        self.page = page
        self.gen = generator
    
    def generate_wpseo_fixes(self) -> List[Dict[str, str]]:
        """
        生成 Yoast SEO / Rank Math 可导入的 SEO 数据
        返回可导入到 WordPress SEO 插件的数据
        """
        fixes = []
        
        # Title
        suggested_title = self.gen.suggest_title()
        if suggested_title and suggested_title != self.page.title:
            fixes.append({
                "type": "title",
                "url": self.page.url,
                "current": self.page.title or "(empty)",
                "suggested": suggested_title,
                "priority": "HIGH",
                "wpcli": f"wp post meta update {self._extract_id()} _yoast_wpseo_title '{suggested_title}'"
                         if 'p=' in self.page.url else None
            })
        
        # Meta description
        suggested_desc = self.gen.suggest_description()
        if suggested_desc and suggested_desc != self.page.meta_description:
            fixes.append({
                "type": "meta_description",
                "url": self.page.url,
                "current": (self.page.meta_description or "(empty)")[:60],
                "suggested": suggested_desc[:60],
                "priority": "HIGH",
                "wpcli": f"wp post meta update {self._extract_id()} _yoast_wpseo_metadesc '{suggested_desc}'"
                         if 'p=' in self.page.url else None
            })
        
        # Alt tags for images
        if self.page.images_without_alt > 0:
            fixes.append({
                "type": "image_alt",
                "url": self.page.url,
                "current": f"{self.page.images_without_alt} images missing alt",
                "suggested": "Add descriptive alt text to all images",
                "priority": "MEDIUM",
                "note": "Example: <img src='...' alt='keyword - product description'>"
            })
        
        # Schema.org
        if not self.page.schema_org:
            schema = self.gen.suggest_schema_org()
            fixes.append({
                "type": "schema",
                "url": self.page.url,
                "current": "(missing)",
                "suggested": json.dumps(schema, ensure_ascii=False),
                "priority": "LOW",
                "note": "Add JSON-LD script in <head> or use Schema Pro plugin"
            })
        
        return fixes
    
    def _extract_id(self) -> str:
        """从 URL 提取文章 ID"""
        import re
        match = re.search(r'p=(\d+)', self.page.url)
        return match.group(1) if match else ""


def generate_full_fixes(report: SEOReport) -> Dict[str, Any]:
    """
    对整个报告生成所有修复建议
    """
    all_fixes = []
    high_priority = []
    medium_priority = []
    low_priority = []
    
    for page in report.pages:
        if "404" in [i for i in page.issues]:
            continue  # 跳过 404 页面
        
        gen = SEOMetaGenerator(page)
        diff = SEODiff(page, gen)
        fixes = diff.generate_wpseo_fixes()
        
        for fix in fixes:
            fix["page_title"] = page.title or page.url
            all_fixes.append(fix)
            
            if fix["priority"] == "HIGH":
                high_priority.append(fix)
            elif fix["priority"] == "MEDIUM":
                medium_priority.append(fix)
            else:
                low_priority.append(fix)
    
    return {
        "total_fixes": len(all_fixes),
        "high_priority": high_priority,
        "medium_priority": medium_priority,
        "low_priority": low_priority,
        "fixes": all_fixes,
        "estimated_hours": len(high_priority) * 0.1 + len(medium_priority) * 0.05,
    }


def export_wpcli_commands(report: SEOReport) -> str:
    """
    导出可批量执行的 WP-CLI 命令
    """
    fixes = generate_full_fixes(report)
    
    output = "# Auto-Claw SEO 修复命令\n"
    output += f"# 站点: {report.site_url}\n"
    output += f"# 生成时间: 2026-03-24\n"
    output += "# 执行前请备份!\n\n"
    
    for fix in fixes.get("high_priority", []):
        if fix.get("wpcli"):
            output += f"# {fix['page_title']}\n"
            output += f"# {fix['url']}\n"
            output += f"{fix['wpcli']}\n\n"
    
    return output
