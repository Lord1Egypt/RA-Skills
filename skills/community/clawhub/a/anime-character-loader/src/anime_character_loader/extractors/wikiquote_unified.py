"""
Wikiquote Unified Fetcher - 统一台词抓取器

四层策略：
1. yurippe API      - 专用动漫台词API（结构化JSON）
2. Wiki API + Browser - MediaWiki API + Camofox（通用Wiki抓取）
3. Smart Excerpt    - 从角色描述提取（兜底素材）
4. Local DB         - 本地数据库（最终兜底）

Author: Clawra
"""

import hashlib
import json
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class QuoteItem:
    """单条台词/摘录"""
    text: str
    speaker: str = "unknown"
    context: str = ""  # 章节/场景
    section: str = ""  # 来源section
    quote_id: str = ""
    confidence: float = 0.0
    source_url: str = ""
    source_type: str = ""  # yurippe | wiki | excerpt | local
    is_original_quote: bool = True  # True=原始台词, False=描述摘录
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "speaker": self.speaker,
            "context": self.context,
            "section": self.section,
            "quote_id": self.quote_id,
            "confidence": self.confidence,
            "source_url": self.source_url,
            "source_type": self.source_type,
            "is_original_quote": self.is_original_quote,
        }


@dataclass
class QuoteResult:
    """抓取结果"""
    character: str
    work: str
    source_type: str  # yurippe | wiki | excerpt | local | mixed
    source_url: str
    quotes: List[QuoteItem] = field(default_factory=list)
    fetched_at: float = field(default_factory=time.time)
    note: str = ""  # 使用提示
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "character": self.character,
            "work": self.work,
            "source_type": self.source_type,
            "source_url": self.source_url,
            "quotes": [q.to_dict() for q in self.quotes],
            "fetched_at": self.fetched_at,
            "quote_count": len(self.quotes),
            "note": self.note,
        }


# ==================== Layer 1: Yurippe API ====================

class YurippeClient:
    """yurippe.vercel.app 动漫台词API客户端"""
    
    BASE_URL = "https://yurippe.vercel.app/api"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (WikiquoteFetcher/1.0)',
            'Accept': 'application/json',
        })
    
    def fetch_by_character(self, character: str) -> List[QuoteItem]:
        """按角色名获取台词"""
        try:
            url = f"{self.BASE_URL}/quotes"
            params = {"character": character}
            
            logger.info(f"[Yurippe] 查询角色: {character}")
            resp = self.session.get(url, params=params, timeout=10)
            
            if resp.status_code != 200:
                logger.warning(f"[Yurippe] HTTP {resp.status_code}")
                return []
            
            data = resp.json()
            if not isinstance(data, list):
                logger.warning(f"[Yurippe] 返回格式错误")
                return []
            
            quotes = []
            for item in data:
                text = item.get("quote", "").strip()
                if not text:
                    continue
                
                quote_id = hashlib.md5(text.encode()).hexdigest()[:8]
                quotes.append(QuoteItem(
                    text=text,
                    speaker=item.get("character", character),
                    context=item.get("show", ""),
                    quote_id=quote_id,
                    confidence=0.95,  # API数据置信度高
                    source_url=f"{self.BASE_URL}/quotes?character={quote(character)}",
                    source_type="yurippe",
                    is_original_quote=True,
                ))
            
            logger.info(f"[Yurippe] 找到 {len(quotes)} 条台词")
            return quotes
            
        except Exception as e:
            logger.warning(f"[Yurippe] 请求失败: {e}")
            return []
    
    def fetch_by_anime(self, anime_title: str) -> List[QuoteItem]:
        """按作品名获取台词（如果有API支持）"""
        # yurippe 目前似乎没有按作品查询的端点
        return []


# ==================== Layer 2: Wiki API + Browser ====================

class WikiBrowserClient:
    """MediaWiki API + Camofox 通用Wiki抓取"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (WikiquoteFetcher/1.0)',
        })
    
    def fetch_from_fandom(self, character: str, work: str) -> List[QuoteItem]:
        """从 Fandom Wiki 抓取"""
        domain = self._get_fandom_domain(work)
        
        # 尝试 Quotes 子页面
        quotes_url = f"https://{domain}/wiki/{character.replace(' ', '_')}/Quotes"
        logger.info(f"[Wiki] 尝试 Quotes 页面: {quotes_url}")
        
        quotes = self._fetch_with_browser(quotes_url, character)
        if quotes:
            return quotes
        
        # 尝试主页面
        main_url = f"https://{domain}/wiki/{character.replace(' ', '_')}"
        logger.info(f"[Wiki] 尝试主页面: {main_url}")
        
        return self._fetch_with_browser(main_url, character)
    
    def fetch_from_moegirl(self, character: str) -> List[QuoteItem]:
        """从萌娘百科抓取"""
        # 处理重定向
        variants = [character, character.replace('斯潘塞', '斯宾塞')]
        
        for variant in variants:
            url = f"https://zh.moegirl.org.cn/wiki/{variant}"
            logger.info(f"[Wiki] 尝试萌娘百科: {variant}")
            
            quotes = self._fetch_with_browser(url, character)
            if quotes:
                return quotes
        
        return []
    
    def _fetch_with_browser(self, url: str, character: str) -> List[QuoteItem]:
        """使用 Camofox 抓取页面"""
        try:
            from camofox import Camofox
        except ImportError:
            logger.warning("[Wiki] Camofox 未安装，跳过浏览器模式")
            return []
        
        quotes = []
        try:
            with Camofox(headless=True) as browser:
                page = browser.new_page()
                page.goto(url, timeout=60000)
                
                # 等待内容
                try:
                    page.wait_for_selector(".mw-parser-output", timeout=15000)
                except:
                    pass
                
                # 提取 HTML
                content = page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # 解析 Quotes
                quotes = self._parse_quotes_from_soup(soup, character, url)
                
        except Exception as e:
            logger.error(f"[Wiki] 浏览器抓取失败: {e}")
        
        return quotes
    
    def _parse_quotes_from_soup(self, soup: BeautifulSoup, character: str, source_url: str) -> List[QuoteItem]:
        """从 Soup 解析台词"""
        quotes = []
        content = soup.find('div', {'class': 'mw-parser-output'})
        
        if not content:
            return quotes
        
        # 查找 Quotes section
        in_quotes_section = False
        current_section = ""
        
        for elem in content.find_all(['h2', 'h3', 'dl', 'blockquote', 'p']):
            # 检查是否是 Quotes section
            if elem.name in ['h2', 'h3']:
                section_text = elem.get_text(strip=True).lower()
                if any(k in section_text for k in ['quote', 'quotes', '台词', '名言']):
                    in_quotes_section = True
                    current_section = elem.get_text(strip=True).replace('[edit]', '').strip()
                else:
                    in_quotes_section = False
                continue
            
            if not in_quotes_section:
                continue
            
            # 提取台词
            if elem.name == 'dl':
                dts = elem.find_all('dt')
                dds = elem.find_all('dd')
                for dt, dd in zip(dts, dds):
                    speaker = dt.get_text(strip=True)
                    text = dd.get_text(strip=True)
                    if len(text) > 5:
                        quote_id = hashlib.md5(text.encode()).hexdigest()[:8]
                        quotes.append(QuoteItem(
                            text=text,
                            speaker=speaker or "unknown",
                            section=current_section,
                            quote_id=quote_id,
                            confidence=0.9,
                            source_url=source_url,
                            source_type="wiki",
                            is_original_quote=True,
                        ))
            elif elem.name == 'blockquote':
                text = elem.get_text(strip=True)
                if len(text) > 5:
                    quote_id = hashlib.md5(text.encode()).hexdigest()[:8]
                    quotes.append(QuoteItem(
                        text=text,
                        speaker="unknown",
                        section=current_section,
                        quote_id=quote_id,
                        confidence=0.8,
                        source_url=source_url,
                        source_type="wiki",
                        is_original_quote=True,
                    ))
        
        return quotes
    
    def _get_fandom_domain(self, work: str) -> str:
        """获取 Fandom 域名"""
        work_lower = work.lower()
        if 'saekano' in work_lower or '路人' in work_lower:
            return 'saekano.fandom.com'
        if 'aobuta' in work_lower or '猪头' in work_lower or 'bunny' in work_lower:
            return 'aobuta.fandom.com'
        work_slug = work_lower.replace(' ', '-').replace(':', '')
        return f'{work_slug}.fandom.com'


# ==================== Layer 3: Smart Excerpt ====================

class SmartExcerptClient:
    """从Wiki角色描述提取摘录"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    def fetch(self, character: str, work: str = "") -> List[QuoteItem]:
        """提取角色描述摘录"""
        excerpts = []
        
        # 从萌娘百科提取
        moegirl_excerpts = self._fetch_from_moegirl(character)
        excerpts.extend(moegirl_excerpts)
        
        # 从 Fandom 提取（如果work提供）
        if work:
            fandom_excerpts = self._fetch_from_fandom(character, work)
            excerpts.extend(fandom_excerpts)
        
        # 去重
        seen = set()
        unique = []
        for e in excerpts:
            if e.quote_id not in seen:
                seen.add(e.quote_id)
                unique.append(e)
        
        return unique
    
    def _fetch_from_moegirl(self, character: str) -> List[QuoteItem]:
        """从萌娘百科提取"""
        variants = [character, character.replace('斯潘塞', '斯宾塞')]
        
        for variant in variants:
            api_url = f"https://zh.moegirl.org.cn/api.php?action=parse&page={variant}&prop=text&format=json"
            
            try:
                resp = self.session.get(api_url, timeout=30)
                data = resp.json()
                
                if 'error' in data or 'parse' not in data:
                    continue
                
                html = data['parse']['text']['*']
                if 'redirectMsg' in html:
                    continue
                
                soup = BeautifulSoup(html, 'html.parser')
                target_sections = ['性格特点', '角色经历', '简介', '角色形象']
                
                excerpts = []
                for h in soup.find_all(['h2', 'h3']):
                    section_name = h.get_text(strip=True).replace('[编辑]', '').strip()
                    if any(target in section_name for target in target_sections):
                        section_excerpts = self._extract_from_section(soup, h, section_name, character, "萌娘百科")
                        excerpts.extend(section_excerpts)
                
                return excerpts
                
            except Exception as e:
                logger.warning(f"[Excerpt] 萌娘百科失败: {e}")
                continue
        
        return []
    
    def _fetch_from_fandom(self, character: str, work: str) -> List[QuoteItem]:
        """从 Fandom 提取"""
        domain = self._get_fandom_domain(work)
        api_url = f"https://{domain}/api.php?action=parse&page={character.replace(' ', '_')}&prop=text&format=json"
        
        try:
            resp = self.session.get(api_url, timeout=30)
            data = resp.json()
            
            if 'error' in data or 'parse' not in data:
                return []
            
            html = data['parse']['text']['*']
            soup = BeautifulSoup(html, 'html.parser')
            target_sections = ['Personality', 'Biography', 'Background', 'Character']
            
            excerpts = []
            for h in soup.find_all(['h2', 'h3']):
                section_name = h.get_text(strip=True).replace('[edit]', '').strip()
                if any(target.lower() in section_name.lower() for target in target_sections):
                    section_excerpts = self._extract_from_section(soup, h, section_name, character, "Fandom")
                    excerpts.extend(section_excerpts)
            
            return excerpts
            
        except Exception as e:
            logger.warning(f"[Excerpt] Fandom失败: {e}")
            return []
    
    def _extract_from_section(self, soup: BeautifulSoup, section_elem, section_name: str, 
                              character: str, wiki_type: str) -> List[QuoteItem]:
        """从章节提取"""
        excerpts = []
        
        paragraphs = []
        current = section_elem
        while current:
            current = current.find_next(['p', 'h2', 'h3'])
            if not current:
                break
            if current.name in ['h2', 'h3']:
                if section_name not in current.get_text(strip=True):
                    break
            if current.name == 'p':
                text = current.get_text(strip=True)
                if 20 < len(text) < 500:
                    paragraphs.append(text)
        
        for para in paragraphs[:3]:
            clean_text = self._clean_text(para)
            if not clean_text:
                continue
            
            quote_id = hashlib.md5(clean_text.encode()).hexdigest()[:8]
            excerpts.append(QuoteItem(
                text=clean_text,
                speaker="unknown",
                context=f"{wiki_type}角色描述",
                section=section_name,
                quote_id=quote_id,
                confidence=0.6,
                source_url="",
                source_type="excerpt",
                is_original_quote=False,  # 明确标记
            ))
        
        return excerpts
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        text = re.sub(r'\[\d+\]', '', text)
        text = re.sub(r'\[编辑[^\]]*\]', '', text)
        return ' '.join(text.split()).strip()
    
    def _get_fandom_domain(self, work: str) -> str:
        work_lower = work.lower()
        if 'saekano' in work_lower or '路人' in work_lower:
            return 'saekano.fandom.com'
        if 'aobuta' in work_lower or '猪头' in work_lower:
            return 'aobuta.fandom.com'
        return f'{work_lower.replace(" ", "-").replace(":", "")}.fandom.com'


# ==================== Layer 4: Local Database ====================

class LocalDatabaseClient:
    """本地数据库客户端"""
    
    def fetch(self, character: str) -> List[QuoteItem]:
        """从本地 JSON 加载"""
        db_paths = [
            Path(__file__).parent.parent.parent / "data" / "quotes_database.json",
            Path.cwd() / "data" / "quotes_database.json",
        ]
        
        for db_path in db_paths:
            if not db_path.exists():
                continue
            
            try:
                with open(db_path, 'r', encoding='utf-8') as f:
                    db = json.load(f)
                
                for key, data in db.items():
                    if character in key or key in character:
                        quotes = []
                        for q in data.get("quotes", []):
                            text = q.get("text", "")
                            quote_id = hashlib.md5(text.encode()).hexdigest()[:8]
                            quotes.append(QuoteItem(
                                text=text,
                                speaker=q.get("speaker", "unknown"),
                                context=q.get("context", ""),
                                quote_id=quote_id,
                                confidence=0.8,
                                source_url=f"local://{db_path}#{key}",
                                source_type="local",
                                is_original_quote=True,
                            ))
                        return quotes
                        
            except Exception as e:
                logger.warning(f"[Local] 读取失败: {e}")
        
        return []


# ==================== Unified Fetcher ====================

class WikiquoteUnifiedFetcher:
    """
    统一台词抓取器
    
    四层策略：
    1. yurippe API      - 专用动漫台词
    2. Wiki + Browser   - 通用Wiki抓取
    3. Smart Excerpt    - 角色描述摘录
    4. Local DB         - 本地兜底
    """
    
    def __init__(self):
        self.yurippe = YurippeClient()
        self.wiki = WikiBrowserClient()
        self.excerpt = SmartExcerptClient()
        self.local = LocalDatabaseClient()
    
    def fetch(self, character: str, work: str = "", include_excerpt: bool = True) -> QuoteResult:
        """
        统一抓取入口
        
        Args:
            character: 角色名
            work: 作品名（可选，用于Wiki域名确定）
            include_excerpt: 是否包含描述摘录（当无台词时）
        
        Returns:
            QuoteResult: 抓取结果
        """
        all_quotes = []
        sources_used = []
        
        # Layer 1: yurippe API
        logger.info("[Layer 1] 尝试 yurippe API...")
        yurippe_quotes = self.yurippe.fetch_by_character(character)
        if yurippe_quotes:
            all_quotes.extend(yurippe_quotes)
            sources_used.append("yurippe")
            logger.info(f"✓ yurippe 找到 {len(yurippe_quotes)} 条")
        
        # Layer 2: Wiki + Browser
        if len(all_quotes) < 3:  # 如果yurippe数据少，尝试Wiki
            logger.info("[Layer 2] 尝试 Wiki + Browser...")
            
            if work:
                wiki_quotes = self.wiki.fetch_from_fandom(character, work)
                if wiki_quotes:
                    all_quotes.extend(wiki_quotes)
                    sources_used.append("wiki_fandom")
                
                if len(all_quotes) < 3:
                    wiki_quotes = self.wiki.fetch_from_moegirl(character)
                    if wiki_quotes:
                        all_quotes.extend(wiki_quotes)
                        sources_used.append("wiki_moegirl")
        
        # Layer 3: Smart Excerpt（如果开启且数据不足）
        if include_excerpt and len(all_quotes) < 3:
            logger.info("[Layer 3] 尝试 Smart Excerpt...")
            excerpt_quotes = self.excerpt.fetch(character, work)
            if excerpt_quotes:
                all_quotes.extend(excerpt_quotes)
                sources_used.append("excerpt")
                logger.info(f"✓ Excerpt 找到 {len(excerpt_quotes)} 条")
        
        # Layer 4: Local DB（最终兜底）
        if len(all_quotes) < 1:
            logger.info("[Layer 4] 尝试 Local DB...")
            local_quotes = self.local.fetch(character)
            if local_quotes:
                all_quotes.extend(local_quotes)
                sources_used.append("local")
                logger.info(f"✓ Local 找到 {len(local_quotes)} 条")
        
        # 构建结果
        source_type = "mixed" if len(sources_used) > 1 else (sources_used[0] if sources_used else "none")
        
        # 生成提示
        note = self._generate_note(all_quotes, sources_used)
        
        return QuoteResult(
            character=character,
            work=work,
            source_type=source_type,
            source_url="",
            quotes=all_quotes,
            note=note,
        )
    
    def _generate_note(self, quotes: List[QuoteItem], sources: List[str]) -> str:
        """生成使用提示"""
        if not quotes:
            return "⚠️ 未找到任何数据"
        
        original_count = sum(1 for q in quotes if q.is_original_quote)
        excerpt_count = len(quotes) - original_count
        
        parts = []
        if original_count > 0:
            parts.append(f"原始台词: {original_count}条")
        if excerpt_count > 0:
            parts.append(f"角色描述: {excerpt_count}条")
        
        note = f"来源: {', '.join(sources)} | {' | '.join(parts)}"
        
        if excerpt_count > 0:
            note += "\n⚠️ 注意：包含角色描述摘录（非原始台词），仅用于辅助理解角色背景"
        
        return note


# ==================== Public API ====================

def fetch_quotes(character: str, work: str = "", include_excerpt: bool = True) -> Dict[str, Any]:
    """
    便捷函数：统一抓取角色台词
    
    四层策略：
    1. yurippe API（专用动漫台词）
    2. Wiki API + Browser（通用Wiki抓取）
    3. Smart Excerpt（角色描述摘录）
    4. Local DB（本地兜底）
    
    Args:
        character: 角色名（如 "Eriri Spencer Sawamura" 或 "泽村·斯潘塞·英梨梨"）
        work: 作品名（如 "Saekano" 或 "路人女主"，用于Wiki域名）
        include_excerpt: 是否包含描述摘录（默认True）
    
    Returns:
        dict: 包含台词列表、来源、使用提示
    
    Example:
        >>> result = fetch_quotes("Eriri Spencer Sawamura", "Saekano")
        >>> print(result['note'])
        >>> for q in result['quotes']:
        ...     print(f"[{q['source_type']}] {q['text'][:50]}...")
    """
    fetcher = WikiquoteUnifiedFetcher()
    result = fetcher.fetch(character, work, include_excerpt)
    return result.to_dict()


if __name__ == "__main__":
    # 测试
    import logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    print("="*60)
    print("测试 1: 英梨梨 (yurippe 应该有数据)")
    print("="*60)
    result = fetch_quotes("Eriri Spencer Sawamura", "Saekano")
    print(f"\n{result['note']}\n")
    for i, q in enumerate(result['quotes'][:5], 1):
        original_mark = "📝" if q['is_original_quote'] else "📄"
        print(f"{original_mark} [{q['source_type']}] {q['text'][:60]}...")
    
    print("\n" + "="*60)
    print("测试 2: 樱岛麻衣 (可能需要excerpt)")
    print("="*60)
    result = fetch_quotes("樱岛麻衣", "青春猪头少年")
    print(f"\n{result['note']}\n")
    for i, q in enumerate(result['quotes'][:3], 1):
        original_mark = "📝" if q['is_original_quote'] else "📄"
        print(f"{original_mark} [{q['source_type']}] {q['text'][:60]}...")
