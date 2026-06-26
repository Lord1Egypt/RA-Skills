"""
SEO Analyzer — WordPress SEO 扫描与优化建议
扫描站点的 SEO 问题，生成可执行的优化报告
"""
import re
import json
import subprocess
import requests
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from urllib.parse import urljoin

@dataclass
class PageMeta:
    """单页面的 SEO metadata"""
    url: str
    title: str = ""
    meta_description: str = ""
    h1: List[str] = field(default_factory=list)
    h2s: List[str] = field(default_factory=list)
    images: List[str] = field(default_factory=list)
    images_without_alt: int = 0
    word_count: int = 0
    internal_links: List[str] = field(default_factory=list)
    external_links: List[str] = field(default_factory=list)
    canonical: str = ""
    og_tags: Dict[str, str] = field(default_factory=dict)
    schema_org: str = ""
    
    # 问题列表
    issues: List[str] = field(default_factory=list)
    score: int = 100  # 0-100
    
    def add_issue(self, severity: str, message: str):
        """添加问题"""
        self.issues.append(f"[{severity}] {message}")
        if severity == "ERROR":
            self.score -= 20
        elif severity == "WARNING":
            self.score -= 10
        elif severity == "INFO":
            self.score -= 5
        self.score = max(0, min(100, self.score))

@dataclass
class SEOReport:
    """整站 SEO 报告"""
    site_url: str
    scanned_pages: int = 0
    total_issues: int = 0
    avg_score: float = 0.0
    pages: List[PageMeta] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    opportunities: List[Dict] = field(default_factory=list)

class SEOAnalyzer:
    """
    WordPress SEO 分析器
    
    功能：
    1. 扫描所有页面（首页、文章、页面、分类、标签）
    2. 检测 SEO 问题（title、meta、alt、canonical等）
    3. 生成可执行的优化建议
    4. 识别流量机会（低竞争高搜索词）
    """
    
    def __init__(self, site_url: str, wp_web_root: str = None, php_bin: str = None):
        self.site_url = site_url.rstrip("/")
        self.wp_web_root = wp_web_root
        self.php_bin = php_bin or "/www/server/php/82/bin/php"
        self.wp_cli = "/usr/local/bin/wp"
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; Auto-Claw SEO Bot/1.0)"
        })
    
    def _wp(self, args: str) -> Tuple[str, str, int]:
        """执行 WP-CLI 命令"""
        if not self.wp_web_root:
            return "", "No web root configured", 1
        cmd = f"cd {self.wp_web_root} && WP_CLI_PHP={self.php_bin} {self.wp_cli} --allow-root {args}"
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    
    def get_site_url(self) -> str:
        """获取站点URL"""
        if self.wp_web_root:
            out, _, _ = self._wp(f"option get home")
            if out:
                return out.strip().rstrip("/")
        return self.site_url
    
    def get_all_urls(self, limit: int = 50) -> List[Dict[str, str]]:
        """获取所有需要扫描的URL"""
        urls = []
        
        # 首页
        urls.append({"url": self.site_url, "type": "home", "title": ""})
        
        if not self.wp_web_root:
            return urls
        
        # 页面
        out, _, _ = self._wp(f"post list --post_type=page --post_status=publish --posts_per_page={limit} --format=json")
        if out:
            try:
                pages = json.loads(out)
                for p in pages:
                    urls.append({
                        "url": f"{self.site_url}/?p={p.get('ID')}",
                        "type": "page",
                        "title": p.get("post_title", ""),
                        "id": p.get("ID")
                    })
            except:
                pass
        
        # 文章
        out, _, _ = self._wp(f"post list --post_type=post --post_status=publish --posts_per_page={limit} --format=json")
        if out:
            try:
                posts = json.loads(out)
                for p in posts:
                    urls.append({
                        "url": f"{self.site_url}/?p={p.get('ID')}",
                        "type": "post",
                        "title": p.get("post_title", ""),
                        "id": p.get("ID")
                    })
            except:
                pass
        
        # 分类
        out, _, _ = self._wp("term list category --format=json")
        if out:
            try:
                terms = json.loads(out)
                for t in terms:
                    slug = t.get("slug", "")
                    if slug:
                        urls.append({
                            "url": f"{self.site_url}/category/{slug}",
                            "type": "category",
                            "title": t.get("name", "")
                        })
            except:
                pass
        
        return urls
    
    def scan_page(self, url: str, page_type: str = "unknown") -> PageMeta:
        """扫描单个页面的 SEO 状态"""
        meta = PageMeta(url=url)
        
        try:
            resp = self._session.get(url, timeout=10, verify=False)
            html = resp.text
            status = resp.status_code
        except Exception as e:
            meta.add_issue("ERROR", f"无法访问页面: {e}")
            return meta
        
        if status != 200:
            meta.add_issue("ERROR", f"HTTP {status}")
            return meta
        
        # ===== 提取内容 =====
        
        # Title
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        if title_match:
            meta.title = title_match.group(1).strip()
        else:
            meta.add_issue("ERROR", "缺少 <title> 标签")
        
        # Meta description
        desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if not desc_match:
            desc_match = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', html, re.IGNORECASE)
        if desc_match:
            meta.meta_description = desc_match.group(1).strip()
        else:
            meta.add_issue("ERROR", "缺少 meta description")
        
        # H1
        h1_matches = re.findall(r'<h1[^>]*>([^<]+)</h1>', html, re.IGNORECASE)
        meta.h1 = [h.strip() for h in h1_matches]
        if len(meta.h1) == 0:
            meta.add_issue("ERROR", "缺少 H1 标签")
        elif len(meta.h1) > 1:
            meta.add_issue("WARNING", f"H1 标签过多 ({len(meta.h1)} 个)")
        
        # H2
        h2_matches = re.findall(r'<h2[^>]*>([^<]+)</h2>', html, re.IGNORECASE)
        meta.h2s = [h.strip() for h in h2_matches]
        
        # Images without alt
        img_tags = re.findall(r'<img[^>]+>', html, re.IGNORECASE)
        meta.images = img_tags
        for img in img_tags:
            alt_match = re.search(r'alt=["\']([^"\']*)["\']', img, re.IGNORECASE)
            if not alt_match or not alt_match.group(1).strip():
                meta.images_without_alt += 1
        if meta.images_without_alt > 0:
            meta.add_issue("WARNING", f"{meta.images_without_alt} 个图片缺少 alt 属性")
        
        # Word count (rough)
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text)
        meta.word_count = len(text.split())
        if meta.word_count < 100:
            meta.add_issue("INFO", f"内容过少 ({meta.word_count} 字)")
        
        # Canonical
        canonical_match = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if canonical_match:
            meta.canonical = canonical_match.group(1).strip()
        
        # OG Tags
        og_tags_found = re.findall(r'<meta[^>]+property=["\']og:([^"\']+)["\'][^>]+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        for tag, content in og_tags_found:
            meta.og_tags[tag] = content.strip()
        
        # Schema.org JSON-LD
        schema_match = re.search(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.IGNORECASE | re.DOTALL)
        if schema_match:
            try:
                schema_data = json.loads(schema_match.group(1))
                meta.schema_org = schema_data.get("@type", "JSON-LD")
            except:
                meta.schema_org = "INVALID"
        
        # ===== SEO 问题检测 =====
        
        # Title 长度
        if meta.title:
            title_len = len(meta.title)
            if title_len < 30:
                meta.add_issue("WARNING", f"Title 过短 ({title_len} 字符，建议 30-60)")
            elif title_len > 60:
                meta.add_issue("WARNING", f"Title 过长 ({title_len} 字符，建议 30-60)")
        
        # Meta description 长度
        if meta.meta_description:
            desc_len = len(meta.meta_description)
            if desc_len < 120:
                meta.add_issue("WARNING", f"Meta description 过短 ({desc_len} 字符，建议 120-160)")
            elif desc_len > 160:
                meta.add_issue("WARNING", f"Meta description 过长 ({desc_len} 字符，建议 120-160)")
        else:
            meta.add_issue("ERROR", "缺少 meta description")
        
        # OG tags
        if not meta.og_tags.get("title") and meta.title:
            meta.add_issue("INFO", "缺少 OG title")
        if not meta.og_tags.get("description") and meta.meta_description:
            meta.add_issue("INFO", "缺少 OG description")
        if not meta.og_tags.get("image"):
            meta.add_issue("INFO", "缺少 OG image")
        
        # Schema.org
        if not meta.schema_org:
            meta.add_issue("INFO", "缺少 Schema.org JSON-LD 结构化数据")
        
        return meta
    
    def generate_recommendations(self, pages: List[PageMeta]) -> List[str]:
        """生成全局优化建议"""
        recs = []
        
        # 统计问题
        error_count = sum(1 for p in pages for i in p.issues if "ERROR" in i)
        warning_count = sum(1 for p in pages for i in p.issues if "WARNING" in i)
        
        if error_count > 0:
            recs.append(f"🔴 修复 {error_count} 个错误问题（影响搜索收录）")
        if warning_count > 0:
            recs.append(f"🟡 优化 {warning_count} 个警告问题（影响排名）")
        
        # 首页建议
        home = next((p for p in pages if "home" in p.url), None)
        if home:
            if not home.schema_org:
                recs.append("📋 首页添加 Organization Schema（提升品牌搜索展示）")
            if not home.og_tags.get("image"):
                recs.append("📋 首页添加 OG image（提升社交分享效果）")
        
        # 内容建议
        avg_words = sum(p.word_count for p in pages) / max(1, len(pages))
        if avg_words < 300:
            recs.append(f"📝 页面平均内容偏少 ({avg_words:.0f} 字)，建议每篇至少 300 字")
        
        return recs
    
    def run_full_scan(self, max_pages: int = 30) -> SEOReport:
        """运行完整 SEO 扫描"""
        site_url = self.get_site_url()
        report = SEOReport(site_url=site_url)
        
        print(f"🔍 开始 SEO 扫描: {site_url}")
        
        # 获取所有 URL
        urls = self.get_all_urls(limit=max_pages)
        report.scanned_pages = len(urls)
        print(f"   发现 {len(urls)} 个页面...")
        
        # 扫描每个页面
        for i, page_info in enumerate(urls):
            url = page_info["url"]
            print(f"   扫描 [{i+1}/{len(urls)}]: {url[:60]}...")
            
            meta = self.scan_page(url, page_info["type"])
            meta.title = page_info.get("title", "") or meta.title
            report.pages.append(meta)
            
            if meta.issues:
                report.total_issues += len(meta.issues)
        
        # 计算平均分
        if report.pages:
            report.avg_score = sum(p.score for p in report.pages) / len(report.pages)
        
        # 生成建议
        report.recommendations = self.generate_recommendations(report.pages)
        
        print(f"\n✅ 扫描完成!")
        print(f"   扫描页面: {report.scanned_pages}")
        print(f"   总问题: {report.total_issues}")
        print(f"   平均得分: {report.avg_score:.0f}/100")
        
        return report
    
    def export_json(self, report: SEOReport) -> str:
        """导出 JSON 格式报告"""
        data = {
            "site": report.site_url,
            "scanned_pages": report.scanned_pages,
            "total_issues": report.total_issues,
            "avg_score": report.avg_score,
            "pages": [
                {
                    "url": p.url,
                    "title": p.title[:80],
                    "score": p.score,
                    "issues": p.issues,
                    "word_count": p.word_count,
                    "images_without_alt": p.images_without_alt,
                    "has_schema": bool(p.schema_org),
                }
                for p in report.pages
            ],
            "recommendations": report.recommendations,
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
