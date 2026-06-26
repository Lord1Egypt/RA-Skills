
---

### 2. agent.py - Python执行脚本（可选，用于复杂抓取逻辑）

```python
#!/usr/bin/env python3
"""
Adaptive Web Analyzer - OpenClaw Skill Implementation
提供自适应网页抓取和AI内容分析功能
"""

import json
import re
import time
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import html2text

# 尝试导入可选依赖（如果环境中有）
try:
    from scrapling import StealthyFetcher, Fetcher
    SCRAPLING_AVAILABLE = True
except ImportError:
    SCRAPLING_AVAILABLE = False

try:
    import playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


@dataclass
class ExtractedContent:
    """提取内容的结构化数据"""
    title: str
    text: str
    metadata: Dict[str, Any]
    links: List[str]
    confidence: float  # 抓取置信度 0-1


class AdaptiveWebAnalyzer:
    """自适应网页分析器"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self._get_random_ua()
        })
        
    def _get_random_ua(self) -> str:
        """获取随机User-Agent"""
        ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        return random.choice(ua_list)
    
    def fetch_content(self, url: str, method: str = "auto", 
                     custom_headers: Optional[Dict] = None,
                     timeout: int = 30) -> str:
        """
        获取网页内容，支持多种策略
        
        Args:
            url: 目标URL或API端点
            method: 获取方式 (auto/api/static/dynamic)
            custom_headers: 自定义请求头
            timeout: 超时时间
        """
        headers = {**self.session.headers, **(custom_headers or {})}
        
        # 判断是否为API端点
        is_api = self._is_api_endpoint(url)
        
        if method == "auto":
            method = "api" if is_api else "static"
        
        # 1. API直接请求
        if method == "api":
            return self._fetch_api(url, headers, timeout)
        
        # 2. 使用Scrapling（如果可用且需要反爬）
        if SCRAPLING_AVAILABLE and method in ["static", "stealth"]:
            return self._fetch_with_scrapling(url, stealth=(method == "stealth"))
        
        # 3. 使用Playwright（如果需要动态渲染）
        if PLAYWRIGHT_AVAILABLE and method == "dynamic":
            return self._fetch_with_playwright(url, timeout)
        
        # 4. 基础requests请求
        return self._fetch_basic(url, headers, timeout)
    
    def _is_api_endpoint(self, url: str) -> bool:
        """判断URL是否为API端点"""
        api_patterns = [r'/api/', r'/v\d+/', r'\.json$', r'graphql']
        return any(re.search(pattern, url) for pattern in api_patterns)
    
    def _fetch_api(self, url: str, headers: Dict, timeout: int) -> str:
        """获取API响应"""
        resp = self.session.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        content_type = resp.headers.get('Content-Type', '')
        
        # 如果是JSON，格式化返回
        if 'json' in content_type:
            try:
                data = resp.json()
                return json.dumps(data, ensure_ascii=False, indent=2)
            except:
                pass
        return resp.text
    
    def _fetch_basic(self, url: str, headers: Dict, timeout: int) -> str:
        """基础HTTP获取"""
        time.sleep(random.uniform(1, 3))  # 礼貌延迟
        resp = self.session.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    
    def _fetch_with_scrapling(self, url: str, stealth: bool = False) -> str:
        """使用Scrapling获取（支持反爬）"""
        if stealth:
            fetcher = StealthyFetcher()
        else:
            fetcher = Fetcher()
        
        # Scrapling自动处理重试和反爬
        response = fetcher.get(url)
        return response.text
    
    def _fetch_with_playwright(self, url: str, timeout: int) -> str:
        """使用Playwright获取动态内容"""
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=self._get_random_ua(),
                viewport={'width': 1920, 'height': 1080}
            )
            page = context.new_page()
            
            page.goto(url, wait_until="networkidle", timeout=timeout*1000)
            
            # 等待关键元素（如果有）
            try:
                page.wait_for_selector("article, .content, main, [role='main']", timeout=5000)
            except:
                pass
            
            content = page.content()
            browser.close()
            return content
    
    def parse_content(self, html: str, selector_hint: Optional[str] = None) -> ExtractedContent:
        """
        自适应解析HTML内容
        
        策略优先级：
        1. 用户提供的CSS选择器提示
        2. 常见内容区域选择器（article, main, .content等）
        3. 基于文本密度的智能提取（Readability算法简化版）
        4. 全文作为后备
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # 移除噪声元素
        for tag in soup.find_all(['script', 'style', 'nav', 'footer', 'aside', 'header']):
            tag.decompose()
        
        # 提取标题
        title = self._extract_title(soup)
        
        # 尝试提取正文
        content_text = ""
        confidence = 0.0
        used_strategy = ""
        
        # 策略1: 用户提示的选择器
        if selector_hint:
            elements = soup.select(selector_hint)
            if elements:
                content_text = self._extract_text_from_elements(elements)
                confidence = 0.9
                used_strategy = "user_selector"
        
        # 策略2: 常见内容选择器
        if not content_text:
            selectors = [
                'article', 'main', '[role="main"]', 
                '.content', '.post-content', '.entry-content',
                '.article-body', '.post-body', '#content'
            ]
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    content_text = self._extract_text_from_elements(elements)
                    confidence = 0.85
                    used_strategy = f"common_selector:{selector}"
                    break
        
        # 策略3: 基于文本密度的智能提取
        if not content_text:
            content_text = self._density_based_extraction(soup)
            if content_text:
                confidence = 0.75
                used_strategy = "density_based"
        
        # 策略4: 后备：转换整个body为markdown
        if not content_text:
            h2t = html2text.HTML2Text()
            h2t.ignore_links = False
            content_text = h2t.handle(str(soup.find('body') or soup))
            confidence = 0.5
            used_strategy = "fallback_full_page"
        
        # 清理文本
        content_text = self._clean_text(content_text)
        
        # 提取元数据和链接
        metadata = self._extract_metadata(soup)
        links = self._extract_links(soup)
        
        return ExtractedContent(
            title=title,
            text=content_text,
            metadata=metadata,
            links=links,
            confidence=confidence
        )
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取页面标题"""
        # 优先使用og:title或twitter:title
        for meta in ['og:title', 'twitter:title']:
            tag = soup.find('meta', property=meta) or soup.find('meta', attrs={'name': meta})
            if tag and tag.get('content'):
                return tag['content']
        
        # 使用title标签或h1
        if soup.find('title'):
            return soup.find('title').get_text(strip=True)
        if soup.find('h1'):
            return soup.find('h1').get_text(strip=True)
        return "未找到标题"
    
    def _extract_text_from_elements(self, elements: List) -> str:
        """从元素列表中提取文本"""
        texts = []
        for el in elements:
            # 获取文本，保留段落结构
            text = el.get_text(separator='\n', strip=True)
            if text:
                texts.append(text)
        return '\n\n'.join(texts)
    
    def _density_based_extraction(self, soup: BeautifulSoup) -> str:
        """基于文本密度的内容提取（简化版Readability）"""
        paragraphs = soup.find_all('p')
        if not paragraphs:
            return ""
        
        # 计算每个父元素的文本密度
        parent_scores = {}
        for p in paragraphs:
            parent = p.find_parent(['div', 'section', 'article'])
            if parent:
                text_len = len(p.get_text(strip=True))
                if parent not in parent_scores:
                    parent_scores[parent] = 0
                parent_scores[parent] += text_len
        
        if not parent_scores:
            return ""
        
        # 选择得分最高的父元素
        best_parent = max(parent_scores, key=parent_scores.get)
        return best_parent.get_text(separator='\n', strip=True)
    
    def _clean_text(self, text: str) -> str:
        """清理文本格式"""
        # 移除多余空白
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        # 移除特殊字符
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', '', text)
        return text.strip()
    
    def _extract_metadata(self, soup: BeautifulSoup) -> Dict:
        """提取页面元数据"""
        meta = {}
        
        # 标准meta标签
        for tag in soup.find_all('meta'):
            name = tag.get('name', tag.get('property', ''))
            content = tag.get('content', '')
            if name and content:
                meta[name] = content
        
        # 作者、时间等特殊字段
        if not meta.get('author'):
            # 尝试从常见位置提取作者
            author_el = soup.find(['.author', '.byline', '[rel="author"]'])
            if author_el:
                meta['author'] = author_el.get_text(strip=True)
        
        return meta
    
    def _extract_links(self, soup: BeautifulSoup) -> List[str]:
        """提取页面中的链接"""
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            text = a.get_text(strip=True)
            if href.startswith('http'):
                links.append(f"{text}: {href}" if text else href)
        return links[:20]  # 限制数量
    
    def analyze_with_llm(self, content: ExtractedContent, 
                        analysis_type: str = "detailed") -> Dict[str, Any]:
        """
        准备发送给LLM的Prompt，返回结构化分析请求
        
        注意：实际LLM调用由OpenClaw框架处理，这里生成标准格式的Prompt
        """
        # 截断内容避免超出上下文
        max_chars = self.config.get('max_length', 8000)
        truncated_text = content.text[:max_chars]
        if len(content.text) > max_chars:
            truncated_text += f"\n\n[内容已截断，原长度: {len(content.text)}字符]"
        
        # 构建系统Prompt
        system_prompt = """你是一个专业的网页内容分析助手。请对提供的网页内容进行深度分析，并以结构化JSON格式返回分析结果。

分析要求：
1. 生成简洁准确的内容摘要（3-5句话）
2. 提取3-7个关键要点
3. 判断内容类别（技术/新闻/产品/学术/博客/其他）
4. 分析情感倾向（积极/中性/消极）
5. 识别关键实体（人物、组织、产品、地点）
6. 提供2-3个基于内容的行动建议

输出必须为标准JSON格式，包含以下字段：
{
  "summary": "内容摘要",
  "key_points": ["要点1", "要点2", "要点3"],
  "category": "内容分类",
  "sentiment": "情感倾向",
  "entities": {
    "persons": ["人物1", "人物2"],
    "organizations": ["组织1"],
    "products": ["产品1"],
    "locations": ["地点1"]
  },
  "suggested_actions": ["建议1", "建议2"]
}"""

        # 构建用户Prompt
        user_prompt = f"""请分析以下网页内容：

标题：{content.title}
抓取置信度：{content.confidence:.2f}
元数据：{json.dumps(content.metadata, ensure_ascii=False)}

正文内容：
---
{truncated_text}
---

请严格按照系统指令返回JSON格式的分析结果。"""

        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "content_stats": {
                "total_chars": len(content.text),
                "extracted_chars": len(truncated_text),
                "confidence_score": content.confidence
            },
            "source_info": {
                "title": content.title,
                "links_count": len(content.links),
                "metadata": content.metadata
            }
        }
    
    def process(self, url: str, **kwargs) -> Dict[str, Any]:
        """
        主处理流程
        
        Args:
            url: 目标URL
            method: 获取方式 (auto/api/static/dynamic/stealth)
            selector_hint: CSS选择器提示
            analysis_type: 分析类型 (summary/detailed/compare)
            custom_headers: 自定义请求头
            max_length: 最大处理长度
        """
        try:
            # 1. 获取内容
            method = kwargs.get('method', 'auto')
            headers = kwargs.get('custom_headers')
            html_content = self.fetch_content(url, method, headers)
            
            # 2. 解析内容
            selector_hint = kwargs.get('selector_hint')
            extracted = self.parse_content(html_content, selector_hint)
            
            # 3. 准备LLM分析
            analysis_type = kwargs.get('analysis_type', 'detailed')
            llm_request = self.analyze_with_llm(extracted, analysis_type)
            
            # 返回完整处理结果（包含LLM请求参数，供OpenClaw调用）
            return {
                "status": "success",
                "source_url": url,
                "fetch_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "content_extraction": {
                    "title": extracted.title,
                    "text_preview": extracted.text[:500] + "..." if len(extracted.text) > 500 else extracted.text,
                    "confidence": extracted.confidence,
                    "metadata": extracted.metadata,
                    "links_sample": extracted.links[:5]
                },
                "llm_analysis_request": llm_request,
                "next_step": "请使用上述system_prompt和user_prompt调用LLM完成分析"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error_type": type(e).__name__,
                "error_message": str(e),
                "suggestion": "请检查URL可访问性，或尝试使用stealth/dynamic模式"
            }


# 如果直接运行脚本（测试模式）
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python agent.py <URL> [method] [selector_hint]")
        sys.exit(1)
    
    url = sys.argv[1]
    method = sys.argv[2] if len(sys.argv) > 2 else "auto"
    selector = sys.argv[3] if len(sys.argv) > 3 else None
    
    analyzer = AdaptiveWebAnalyzer()
    result = analyzer.process(url, method=method, selector_hint=selector)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))