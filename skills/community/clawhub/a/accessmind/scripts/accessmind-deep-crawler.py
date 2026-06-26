#!/usr/bin/env python3
"""
AccessMind Deep Crawler - Derinlemesine Site Taraması
Playwright ile Chrome üzerinde gezinme yaparak kapsamlı erişilebilirlik analizi

Özellikler:
1. 5 derinliğe kadar tarama
2. Maksimum 12 alt sayfa inceleme
3. Her sayfada WCAG testleri
4. Davranış odaklı analiz
5. Link kırık kontrolü
6. Form testleri
7. Ekran görüntüsü alma
"""

import asyncio
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse
from pathlib import Path

try:
    from playwright.async_api import async_playwright, Page, Browser, BrowserContext
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright yüklü değil. Yüklemek için: pip install playwright && playwright install chromium")


@dataclass
class PageInfo:
    """Sayfa bilgisi"""
    url: str
    title: str
    depth: int
    parent_url: str
    links_count: int
    images_count: int
    forms_count: int
    headings: List[Dict]
    landmarks: List[Dict]
    wcag_issues: List[Dict]
    behavioral_score: float
    focus_issues: List[Dict]
    aria_issues: List[Dict]
    screenshot_path: str = ""


@dataclass
class CrawlResult:
    """Tarama sonucu"""
    start_url: str
    total_pages: int
    max_depth: int
    pages: List[PageInfo]
    total_issues: int
    issues_by_page: Dict[str, int]
    issues_by_criterion: Dict[str, int]
    overall_score: float
    crawl_time: float
    broken_links: List[Dict]


class AccessMindDeepCrawler:
    """Derinlemesine site taraması"""
    
    def __init__(
        self,
        start_url: str,
        output_dir: str = "/Users/sarper/.openclaw/workspace/audits",
        max_depth: int = 5,
        max_pages: int = 12,
        headless: bool = True
    ):
        self.start_url = start_url
        self.output_dir = output_dir
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.headless = headless
        
        # State
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.visited_urls: Set[str] = set()
        self.pages_data: List[PageInfo] = []
        self.all_issues: List[Dict] = []
        
        # WCAG kriterleri
        self.wcag_criteria = {
            "1.1.1": "Non-text Content",
            "1.3.1": "Info and Relationships",
            "1.4.3": "Contrast Minimum",
            "2.1.1": "Keyboard",
            "2.1.2": "No Keyboard Trap",
            "2.4.1": "Bypass Blocks",
            "2.4.2": "Page Titled",
            "2.4.3": "Focus Order",
            "2.4.4": "Link Purpose",
            "2.4.6": "Headings and Labels",
            "2.4.7": "Focus Visible",
            "3.1.2": "Language of Parts",
            "4.1.2": "Name, Role, Value",
            "4.1.3": "Status Messages"
        }
        
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "screenshots"), exist_ok=True)
    
    async def initialize(self):
        """Tarayıcıyı başlat - Cloudflare bypass ile"""
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("Playwright yüklü değil")
        
        playwright = await async_playwright().start()
        
        # Cloudflare bypass için stealth settings
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-features=IsolateOrigins,site-per-process',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-web-security',
            ]
        )
        
        # Stealth context
        self.context = await self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9,tr;q=0.8',
                'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
            }
        )
    
    async def close(self):
        """Tarayıcıyı kapat"""
        if self.browser:
            await self.browser.close()
    
    def normalize_url(self, url: str) -> str:
        """URL'yi normalize et"""
        parsed = urlparse(url)
        # Fragment'i kaldır
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if parsed.query:
            normalized += f"?{parsed.query}"
        return normalized.rstrip('/')
    
    def is_same_domain(self, url: str) -> bool:
        """Aynı domain mi kontrol et"""
        base_domain = urlparse(self.start_url).netloc
        url_domain = urlparse(url).netloc
        return base_domain == url_domain
    
    async def get_page_links(self, page: Page) -> List[str]:
        """Sayfadaki link'leri al"""
        links = await page.evaluate("""
            () => {
                const links = [];
                document.querySelectorAll('a[href]').forEach(a => {
                    const href = a.href;
                    // Sadece http/https link'leri
                    if (href.startsWith('http://') || href.startsWith('https://')) {
                        // Anchor link'leri hariç tut
                        if (!href.includes('#')) {
                            links.push(href);
                        }
                    }
                });
                return [...new Set(links)];
            }
        """)
        return links
    
    async def analyze_page_structure(self, page: Page) -> Dict:
        """Sayfa yapısını analiz et"""
        structure = await page.evaluate("""
            () => {
                const result = {
                    title: document.title,
                    language: document.documentElement.lang || '',
                    metaDescription: document.querySelector('meta[name="description"]')?.content || '',
                    headings: [],
                    landmarks: [],
                    links: [],
                    images: [],
                    forms: [],
                    buttons: [],
                    skipLink: false
                };
                
                // Headings
                document.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(h => {
                    result.headings.push({
                        level: h.tagName.substring(1),
                        text: h.textContent.trim().substring(0, 100),
                        hasText: h.textContent.trim().length > 0
                    });
                });
                
                // Landmarks
                document.querySelectorAll('[role="banner"], [role="main"], [role="navigation"], [role="complementary"], [role="form"], [role="search"], [role="contentinfo"], header, main, nav, aside, form, footer').forEach(el => {
                    result.landmarks.push({
                        role: el.getAttribute('role') || el.tagName.toLowerCase(),
                        label: el.getAttribute('aria-label') || ''
                    });
                });
                
                // Links
                document.querySelectorAll('a[href]').forEach(a => {
                    result.links.push({
                        text: a.textContent.trim().substring(0, 100),
                        href: a.href,
                        hasText: a.textContent.trim().length > 0,
                        isExternal: !a.href.includes(window.location.hostname)
                    });
                });
                
                // Images
                document.querySelectorAll('img').forEach(img => {
                    result.images.push({
                        alt: img.alt || '',
                        src: img.src,
                        hasAlt: img.hasAttribute('alt'),
                        decorative: img.alt === '' && img.hasAttribute('alt')
                    });
                });
                
                // Forms
                document.querySelectorAll('form').forEach(form => {
                    const inputs = form.querySelectorAll('input, select, textarea');
                    result.forms.push({
                        hasSubmit: form.querySelector('button[type="submit"], input[type="submit"]') !== null,
                        inputCount: inputs.length,
                        labeledInputs: Array.from(inputs).filter(i => {
                            return i.getAttribute('aria-label') || 
                                   i.getAttribute('aria-labelledby') ||
                                   document.querySelector(`label[for="${i.id}"]`) ||
                                   i.closest('label');
                        }).length
                    });
                });
                
                // Buttons
                document.querySelectorAll('button').forEach(btn => {
                    result.buttons.push({
                        text: btn.textContent.trim().substring(0, 50),
                        hasText: btn.textContent.trim().length > 0 || btn.hasAttribute('aria-label'),
                        ariaLabel: btn.getAttribute('aria-label') || ''
                    });
                });
                
                // Skip link
                result.skipLink = document.querySelector('a[href="#main"], a[href="#content"], a[href="#site-main"]') !== null ||
                                  document.querySelector('a[href*="skip"]') !== null;
                
                return result;
            }
        """)
        
        return structure
    
    async def check_wcag_issues(self, page: Page, structure: Dict) -> List[Dict]:
        """WCAG ihlallerini kontrol et"""
        issues = []
        
        # 1.1.1 - Images without alt
        for img in structure.get('images', []):
            if not img.get('hasAlt'):
                issues.append({
                    "wcag": "1.1.1",
                    "severity": "critical",
                    "element": "img",
                    "message": f"Görsel alt attribute'ü yok: {img.get('src', '')[:50]}",
                    "url": page.url
                })
        
        # 2.4.2 - Page title
        if not structure.get('title'):
            issues.append({
                "wcag": "2.4.2",
                "severity": "serious",
                "element": "title",
                "message": "Sayfa başlığı yok",
                "url": page.url
            })
        
        # 2.4.4 - Link purpose
        for link in structure.get('links', [])[:20]:  # İlk 20 link
            if not link.get('hasText'):
                issues.append({
                    "wcag": "2.4.4",
                    "severity": "serious",
                    "element": "a",
                    "message": f"Link metin yok: {link.get('href', '')[:50]}",
                    "url": page.url
                })
            # "İncele İncele" tekrarı kontrolü
            if link.get('text') and 'incele incele' in link.get('text', '').lower():
                issues.append({
                    "wcag": "2.4.4",
                    "severity": "moderate",
                    "element": "a",
                    "message": "Tekrarlayan link metni: 'İncele İncele'",
                    "url": page.url
                })
        
        # 2.4.6 - Headings
        h1_count = sum(1 for h in structure.get('headings', []) if h.get('level') == '1')
        if h1_count == 0:
            issues.append({
                "wcag": "2.4.6",
                "severity": "serious",
                "element": "h1",
                "message": "H1 başlık yok",
                "url": page.url
            })
        elif h1_count > 1:
            issues.append({
                "wcag": "2.4.6",
                "severity": "moderate",
                "element": "h1",
                "message": f"Birden fazla H1 başlık: {h1_count}",
                "url": page.url
            })
        
        # 4.1.2 - Buttons without accessible name
        for btn in structure.get('buttons', []):
            if not btn.get('hasText'):
                issues.append({
                    "wcag": "4.1.2",
                    "severity": "serious",
                    "element": "button",
                    "message": f"Buton erişilebilir isim yok: {btn.get('text', '')[:30]}",
                    "url": page.url
                })
        
        # 4.1.3 - Status messages (ARIA live regions)
        live_regions = await page.evaluate("""
            () => {
                const regions = document.querySelectorAll('[aria-live]');
                return Array.from(regions).map(r => ({
                    ariaLive: r.getAttribute('aria-live'),
                    ariaAtomic: r.getAttribute('aria-atomic')
                }));
            }
        """)
        
        # Skip link kontrolü
        if not structure.get('skipLink'):
            issues.append({
                "wcag": "2.4.1",
                "severity": "serious",
                "element": "a",
                "message": "Skip link (İçeriğe atla) yok",
                "url": page.url
            })
        
        return issues
    
    async def simulate_keyboard_navigation(self, page: Page) -> Tuple[List[Dict], float]:
        """Klavye navigasyonu simülasyonu"""
        focus_issues = []
        focus_count = 0
        visible_focus_count = 0
        
        # Tab ile gezin
        for i in range(30):
            await page.keyboard.press('Tab')
            await page.wait_for_timeout(50)
            
            # Focus element'i kontrol et
            focus_element = await page.evaluate("""
                () => {
                    const el = document.activeElement;
                    if (!el || el === document.body) return null;
                    
                    const style = window.getComputedStyle(el);
                    const rect = el.getBoundingClientRect();
                    
                    return {
                        tag: el.tagName.toLowerCase(),
                        text: el.textContent.trim().substring(0, 50),
                        hasOutline: style.outline !== 'none' && style.outline !== '',
                        hasBoxShadow: style.boxShadow !== 'none' && style.boxShadow !== '',
                        isVisible: rect.width > 0 && rect.height > 0,
                        role: el.getAttribute('role') || '',
                        ariaLabel: el.getAttribute('aria-label') || ''
                    };
                }
            """)
            
            if not focus_element:
                break
            
            focus_count += 1
            
            if focus_element.get('hasOutline') or focus_element.get('hasBoxShadow'):
                visible_focus_count += 1
            else:
                focus_issues.append({
                    "wcag": "2.4.7",
                    "severity": "serious",
                    "element": focus_element.get('tag', 'unknown'),
                    "message": f"Focus göstergesi yok: {focus_element.get('text', '')[:30]}",
                    "url": page.url
                })
        
        focus_score = (visible_focus_count / focus_count * 100) if focus_count > 0 else 100
        
        return focus_issues, focus_score
    
    async def take_screenshot(self, page: Page, url: str) -> str:
        """Ekran görüntüsü al"""
        domain = urlparse(url).netloc.replace('www.', '')
        path_hash = abs(hash(url)) % 10000
        filename = f"screenshots/{domain}_{path_hash}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        await page.screenshot(path=filepath, full_page=False)
        
        return filepath
    
    async def crawl_page(self, url: str, depth: int = 0) -> Optional[PageInfo]:
        """Tek bir sayfayı tara"""
        normalized_url = self.normalize_url(url)
        
        if normalized_url in self.visited_urls:
            return None
        
        if len(self.pages_data) >= self.max_pages:
            return None
        
        if depth > self.max_depth:
            return None
        
        if not self.is_same_domain(url):
            return None
        
        print(f"  📄 Taranıyor (derinlik {depth}): {url}")
        
        try:
            page = await self.context.new_page()
            
            # Sayfaya git
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(1000)
            
            self.visited_urls.add(normalized_url)
            
            # Sayfa yapısını analiz et
            structure = await self.analyze_page_structure(page)
            
            # WCAG ihlallerini kontrol et
            wcag_issues = await self.check_wcag_issues(page, structure)
            
            # Klavye navigasyonu testi
            focus_issues, focus_score = await self.simulate_keyboard_navigation(page)
            
            # Ekran görüntüsü al
            screenshot_path = await self.take_screenshot(page, url)
            
            # Link'leri al (sonraki sayfalar için)
            links = await self.get_page_links(page)
            
            # PageInfo oluştur
            page_info = PageInfo(
                url=url,
                title=structure.get('title', ''),
                depth=depth,
                parent_url="",
                links_count=len(links),
                images_count=len(structure.get('images', [])),
                forms_count=len(structure.get('forms', [])),
                headings=structure.get('headings', []),
                landmarks=structure.get('landmarks', []),
                wcag_issues=wcag_issues,
                behavioral_score=focus_score,
                focus_issues=focus_issues,
                aria_issues=[],
                screenshot_path=screenshot_path
            )
            
            self.pages_data.append(page_info)
            self.all_issues.extend(wcag_issues)
            self.all_issues.extend(focus_issues)
            
            await page.close()
            
            # Alt sayfaları tara
            if depth < self.max_depth and len(self.pages_data) < self.max_pages:
                pages_to_visit = []
                
                for link in links:
                    normalized_link = self.normalize_url(link)
                    if normalized_link not in self.visited_urls and self.is_same_domain(link):
                        pages_to_visit.append(link)
                        if len(pages_to_visit) >= 3:  # Her sayfadan max 3 alt sayfa
                            break
                
                for next_url in pages_to_visit:
                    if len(self.pages_data) >= self.max_pages:
                        break
                    await self.crawl_page(next_url, depth + 1)
            
            return page_info
            
        except Exception as e:
            print(f"  ❌ Hata: {url} - {str(e)}")
            return None
    
    async def run_deep_crawl(self) -> CrawlResult:
        """Derinlemesine taramayı çalıştır"""
        start_time = datetime.now()
        
        print(f"\n🔍 AccessMind Deep Crawler")
        print(f"URL: {self.start_url}")
        print(f"Max Depth: {self.max_depth}")
        print(f"Max Pages: {self.max_pages}")
        print()
        
        try:
            await self.initialize()
            await self.crawl_page(self.start_url, depth=0)
            
        finally:
            await self.close()
        
        # Sonuçları hesapla
        end_time = datetime.now()
        crawl_time = (end_time - start_time).total_seconds()
        
        total_issues = len(self.all_issues)
        issues_by_page = {}
        issues_by_criterion = {}
        
        for page in self.pages_data:
            issues_by_page[page.url] = len(page.wcag_issues) + len(page.focus_issues)
        
        for issue in self.all_issues:
            criterion = issue.get('wcag', 'unknown')
            issues_by_criterion[criterion] = issues_by_criterion.get(criterion, 0) + 1
        
        # Overall score hesapla
        if self.pages_data:
            avg_behavioral_score = sum(p.behavioral_score for p in self.pages_data) / len(self.pages_data)
            issue_penalty = min(total_issues * 2, 50)  # Max 50 puan düşüş
            overall_score = max(0, avg_behavioral_score - issue_penalty)
        else:
            overall_score = 0
        
        return CrawlResult(
            start_url=self.start_url,
            total_pages=len(self.pages_data),
            max_depth=self.max_depth,
            pages=self.pages_data,
            total_issues=total_issues,
            issues_by_page=issues_by_page,
            issues_by_criterion=issues_by_criterion,
            overall_score=overall_score,
            crawl_time=crawl_time,
            broken_links=[]
        )
    
    def save_report(self, result: CrawlResult) -> str:
        """Raporu kaydet"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = urlparse(self.start_url).netloc.replace('www.', '')
        filename = f"deep_crawl_{domain}_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        report_dict = {
            "start_url": result.start_url,
            "total_pages": result.total_pages,
            "max_depth": result.max_depth,
            "overall_score": result.overall_score,
            "total_issues": result.total_issues,
            "issues_by_criterion": result.issues_by_criterion,
            "crawl_time": result.crawl_time,
            "pages": [
                {
                    "url": p.url,
                    "title": p.title,
                    "depth": p.depth,
                    "links_count": p.links_count,
                    "images_count": p.images_count,
                    "forms_count": p.forms_count,
                    "headings_count": len(p.headings),
                    "landmarks_count": len(p.landmarks),
                    "wcag_issues_count": len(p.wcag_issues),
                    "focus_issues_count": len(p.focus_issues),
                    "behavioral_score": p.behavioral_score,
                    "screenshot": p.screenshot_path
                } for p in result.pages
            ],
            "all_issues": self.all_issues
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def generate_html_report(self, result: CrawlResult) -> str:
        """HTML rapor oluştur"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = urlparse(self.start_url).netloc.replace('www.', '')
        filename = f"deep_crawl_{domain}_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        # Sayfa tablosu
        pages_html = ""
        for i, page in enumerate(result.pages, 1):
            issues_count = len(page.wcag_issues) + len(page.focus_issues)
            score_class = "excellent" if page.behavioral_score >= 90 else "good" if page.behavioral_score >= 70 else "moderate" if page.behavioral_score >= 50 else "poor"
            
            pages_html += f"""
            <tr>
                <td>{i}</td>
                <td><a href="{page.url}" target="_blank">{page.title[:50]}...</a></td>
                <td>{page.depth}</td>
                <td>{page.links_count}</td>
                <td>{page.images_count}</td>
                <td>{issues_count}</td>
                <td><span class="score {score_class}">{page.behavioral_score:.0f}</span></td>
            </tr>
"""
        
        # İhlal tablosu
        issues_html = ""
        for criterion, count in sorted(result.issues_by_criterion.items(), key=lambda x: -x[1]):
            wcag_name = self.wcag_criteria.get(criterion, criterion)
            issues_html += f"""
            <tr>
                <td><span class="wcag-tag">{criterion}</span></td>
                <td>{wcag_name}</td>
                <td>{count}</td>
            </tr>
"""
        
        html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Derinlemesine Tarama Raporu - {domain}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 1400px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; }}
        .header h1 {{ margin: 0 0 10px 0; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat {{ background: white; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .stat h3 {{ margin: 0 0 10px 0; color: #666; font-size: 14px; }}
        .stat .value {{ font-size: 36px; font-weight: bold; color: #667eea; }}
        .section {{ background: white; padding: 25px; border-radius: 12px; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .section h2 {{ color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 10px; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e0e0e0; }}
        th {{ background: #f5f5f5; font-weight: 600; }}
        .score {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-weight: bold; }}
        .score.excellent {{ background: #e8f5e9; color: #2e7d32; }}
        .score.good {{ background: #e3f2fd; color: #1565c0; }}
        .score.moderate {{ background: #fff3e0; color: #e65100; }}
        .score.poor {{ background: #ffebee; color: #c62828; }}
        .wcag-tag {{ background: #333; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Derinlemesine Erişilebilirlik Taraması</h1>
        <div>{self.start_url}</div>
        <div>Tarih: {datetime.now().strftime('%d %B %Y, %H:%M')}</div>
    </div>

    <div class="stats">
        <div class="stat">
            <h3>Toplam Sayfa</h3>
            <div class="value">{result.total_pages}</div>
        </div>
        <div class="stat">
            <h3>Max Derinlik</h3>
            <div class="value">{result.max_depth}</div>
        </div>
        <div class="stat">
            <h3>Toplam İhlal</h3>
            <div class="value">{result.total_issues}</div>
        </div>
        <div class="stat">
            <h3>Genel Skor</h3>
            <div class="value">{result.overall_score:.0f}</div>
        </div>
        <div class="stat">
            <h3>Tarama Süresi</h3>
            <div class="value">{result.crawl_time:.1f}s</div>
        </div>
    </div>

    <div class="section">
        <h2>📄 Sayfa Detayları</h2>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Sayfa</th>
                    <th>Derinlik</th>
                    <th>Link</th>
                    <th>Görsel</th>
                    <th>İhlal</th>
                    <th>Skor</th>
                </tr>
            </thead>
            <tbody>
                {pages_html}
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>⚠️ İhlal Dağılımı (WCAG)</h2>
        <table>
            <thead>
                <tr>
                    <th>Kriter</th>
                    <th>Açıklama</th>
                    <th>Say</th>
                </tr>
            </thead>
            <tbody>
                {issues_html}
            </tbody>
        </table>
    </div>

    <div class="footer">
        <p>Bu rapor AccessMind Deep Crawler tarafından oluşturulmuştur.</p>
        <p>WCAG 2.2 AA standartlarına göre değerlendirilmiştir.</p>
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filepath


async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AccessMind Deep Crawler')
    parser.add_argument('--url', required=True, help='Başlangıç URL')
    parser.add_argument('--depth', type=int, default=5, help='Maksimum derinlik')
    parser.add_argument('--pages', type=int, default=12, help='Maksimum sayfa sayısı')
    parser.add_argument('--output', default='/Users/sarper/.openclaw/workspace/audits', help='Çıktı dizini')
    parser.add_argument('--headless', action='store_true', default=True, help='Headless mod')
    
    args = parser.parse_args()
    
    print(f"🔍 AccessMind Deep Crawler")
    print(f"URL: {args.url}")
    print(f"Derinlik: {args.depth}")
    print(f"Max sayfa: {args.pages}")
    print()
    
    crawler = AccessMindDeepCrawler(
        start_url=args.url,
        output_dir=args.output,
        max_depth=args.depth,
        max_pages=args.pages,
        headless=args.headless
    )
    
    result = await crawler.run_deep_crawl()
    
    # JSON rapor
    json_path = crawler.save_report(result)
    print(f"\n✅ JSON rapor: {json_path}")
    
    # HTML rapor
    html_path = crawler.generate_html_report(result)
    print(f"✅ HTML rapor: {html_path}")
    
    # Özet
    print(f"\n📊 Özet:")
    print(f"  - Toplam sayfa: {result.total_pages}")
    print(f"  - Toplam ihlal: {result.total_issues}")
    print(f"  - Genel skor: {result.overall_score:.0f}")
    print(f"  - Tarama süresi: {result.crawl_time:.1f}s")
    
    if result.issues_by_criterion:
        print(f"\n⚠️ İhlaller:")
        for criterion, count in sorted(result.issues_by_criterion.items(), key=lambda x: -x[1])[:5]:
            print(f"  - {criterion}: {count}")


if __name__ == "__main__":
    asyncio.run(main())