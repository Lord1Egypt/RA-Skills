"""
Fandom Hybrid 台词抓取器

三层策略：API → Playwright → Local
目标：稳定输出结构化角色台词

Author: Clawra
"""

import hashlib
import json
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import quote, unquote

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class QuoteItem:
    """单条台词，带置信度"""
    text: str
    speaker: str = "unknown"
    context: str = ""
    section: str = ""
    quote_id: str = ""
    confidence: float = 0.0
    source_url: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "speaker": self.speaker,
            "context": self.context,
            "section": self.section,
            "quote_id": self.quote_id,
            "confidence": round(self.confidence, 2),
            "source_url": self.source_url,
        }


@dataclass
class QuoteResult:
    """抓取结果"""
    character: str
    work: str
    source_type: str  # api | browser | local | cache
    source_url: str
    quotes: List[QuoteItem] = field(default_factory=list)
    fetched_at: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "character": self.character,
            "work": self.work,
            "source_type": self.source_type,
            "source_url": self.source_url,
            "quotes": [q.to_dict() for q in self.quotes],
            "fetched_at": self.fetched_at,
            "quote_count": len(self.quotes),
        }


class NetworkError(Exception):
    """网络请求失败"""
    pass


class CharacterNotFoundError(Exception):
    """角色页面不存在"""
    pass


class ParseError(Exception):
    """页面存在但无法提取有效台词"""
    pass


class FandomHybridFetcher:
    """
    Fandom Wiki 混合抓取器
    
    策略：API → Playwright → Local
    """
    
    # Fandom 域名映射
    FANDOM_DOMAINS = {
        "路人女主": "saekano.fandom.com",
        "saekano": "saekano.fandom.com",
        "冴えない": "saekano.fandom.com",
        "青春猪头": "aobuta.fandom.com",
        "aobuta": "aobuta.fandom.com",
        "兔女郎": "aobuta.fandom.com",
    }
    
    DEFAULT_DOMAIN = "fandom.com"
    REQUEST_TIMEOUT = 30
    MAX_RETRIES = 3
    CONFIDENCE_THRESHOLD = 0.7
    LOW_CONFIDENCE_THRESHOLD = 0.4
    
    def __init__(self, cache_dir: Optional[str] = None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/html',
        })
        self.cache_dir = Path(cache_dir) if cache_dir else Path(__file__).parent / ".." / ".." / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_domain(self, work: str) -> str:
        """根据作品名获取 Fandom 域名"""
        work_lower = work.lower()
        for key, domain in self.FANDOM_DOMAINS.items():
            if key in work_lower:
                return domain
        work_slug = re.sub(r'[^\w\s]', '', work).replace(' ', '-').lower()
        return f"{work_slug}.{self.DEFAULT_DOMAIN}"
    
    def _build_api_url(self, character: str, work: str, action: str = "parse") -> str:
        """构建 MediaWiki API URL"""
        domain = self._get_domain(work)
        char_encoded = quote(character.replace(' ', '_'))
        if action == "parse":
            return f"https://{domain}/api.php?action=parse&page={char_encoded}&prop=text|sections&format=json"
        elif action == "query":
            return f"https://{domain}/api.php?action=query&titles={char_encoded}&format=json"
        return f"https://{domain}/wiki/{char_encoded}"
    
    def fetch(self, character: str, work: str, prefer: str = "api") -> QuoteResult:
        """
        三层抓取主入口
        
        Args:
            character: 角色名（英文，如 Eriri Spencer Sawamura）
            work: 作品名（用于确定 Fandom 域名）
            prefer: 优先策略 api|browser
        
        Returns:
            QuoteResult: 抓取结果
        """
        source_url = self._build_api_url(character, work, "parse")
        
        # Phase 1: API 探测
        try:
            logger.info(f"[Phase 1] API 探测: {character}@{work}")
            api_result = self._fetch_api(character, work)
            if api_result:
                quotes, has_confident = api_result
                if has_confident:
                    return QuoteResult(
                        character=character,
                        work=work,
                        source_type="api",
                        source_url=source_url,
                        quotes=quotes
                    )
                logger.info("API 结果置信度不足，进入 Phase 2")
        except (NetworkError, CharacterNotFoundError) as e:
            logger.warning(f"API 失败: {e}，进入 Phase 2")
        
        # Phase 2: Playwright 精准提取
        if prefer in ("api", "browser"):
            try:
                logger.info(f"[Phase 2] Playwright 提取: {character}")
                page_url = self._build_api_url(character, work, "page")
                quotes = self._fetch_browser(page_url, character)
                if quotes:
                    return QuoteResult(
                        character=character,
                        work=work,
                        source_type="browser",
                        source_url=page_url,
                        quotes=quotes
                    )
            except Exception as e:
                logger.warning(f"Browser 失败: {e}")
        
        # Phase 3: Local 兜底
        logger.info(f"[Phase 3] Local 兜底: {character}")
        quotes = self._fetch_local(character)
        if quotes:
            return QuoteResult(
                character=character,
                work=work,
                source_type="local",
                source_url=f"local://quotes_database.json#{character}",
                quotes=quotes
            )
        
        raise ParseError(f"无法获取 {character} 的有效台词（API/Browser/Local 均失败）")
    
    def _fetch_api(self, character: str, work: str) -> Optional[Tuple[List[QuoteItem], bool]]:
        """
        Phase 1: API 抓取
        
        Returns:
            (quotes, has_confident): 台词列表 + 是否有高置信度结果
        """
        api_url = self._build_api_url(character, work, "parse")
        
        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.session.get(api_url, timeout=self.REQUEST_TIMEOUT)
                response.raise_for_status()
                data = response.json()
                
                # 检查错误
                if "error" in data:
                    code = data["error"].get("code", "")
                    if code in ("missingtitle", "invalidtitle"):
                        raise CharacterNotFoundError(f"页面不存在: {character}")
                    raise NetworkError(f"API 错误: {data['error']}")
                
                parse_data = data.get("parse", {})
                if not parse_data or "text" not in parse_data:
                    raise ParseError(f"API 返回无效数据: {character}")
                
                # 提取台词
                html_content = parse_data["text"]["*"]
                sections = parse_data.get("sections", [])
                
                quotes = self._extract_quotes_api(html_content, sections, character, api_url)
                
                # 检查是否有高置信度结果
                has_confident = any(q.confidence >= self.CONFIDENCE_THRESHOLD for q in quotes)
                
                return quotes, has_confident
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"API 请求失败 (尝试 {attempt+1}): {e}")
                if attempt == self.MAX_RETRIES - 1:
                    raise NetworkError(f"API 请求失败: {e}")
                time.sleep(2 ** attempt)
        
        return None, False
    
    def _extract_quotes_api(self, html: str, sections: List[Dict], 
                            character: str, source_url: str) -> List[QuoteItem]:
        """从 API 返回的 HTML 中提取台词"""
        soup = BeautifulSoup(html, 'html.parser')
        quotes = []
        
        # 1. 找出 quotes section
        quote_section_indices = []
        for i, sec in enumerate(sections):
            line = sec.get("line", "").lower()
            if any(k in line for k in ["quote", "quotes", "台词", "名言", "语录"]):
                quote_section_indices.append(i)
        
        # 2. 提取这些 section 的内容
        if quote_section_indices:
            for sec_idx in quote_section_indices:
                sec = sections[sec_idx]
                sec_name = sec.get("line", "")
                sec_anchor = sec.get("anchor", "")
                
                # 找到对应 section 的 HTML
                section_elem = soup.find(id=sec_anchor)
                if not section_elem:
                    continue
                
                # 提取该 section 下的台词
                section_quotes = self._parse_section_content(
                    section_elem, sec_name, character, source_url
                )
                quotes.extend(section_quotes)
        
        # 3. 全局 fallback：找 blockquote, dd 等
        if not quotes:
            quotes = self._parse_global_fallback(soup, character, source_url)
        
        # 4. 去重
        quotes = self._deduplicate_quotes(quotes)
        
        # 5. 过滤低置信度
        quotes = [q for q in quotes if q.confidence >= self.LOW_CONFIDENCE_THRESHOLD]
        
        return quotes
    
    def _parse_section_content(self, section_elem, section_name: str, 
                               character: str, source_url: str) -> List[QuoteItem]:
        """解析单个 section 的内容"""
        quotes = []
        
        # 收集该 section 下的所有元素（直到下一个 h2/h3）
        elements = []
        for elem in section_elem.find_all_next():
            if elem.name in ["h2", "h3"]:
                break
            elements.append(elem)
        
        # 从 elements 中提取台词
        for elem in elements:
            if elem.name in ["blockquote", "dd", "li", "p"]:
                text = elem.get_text(strip=True)
                if self._is_valid_quote_text(text):
                    speaker, clean_text = self._extract_speaker(text, character)
                    quote_id = hashlib.md5(clean_text.encode()).hexdigest()[:8]
                    
                    confidence = self._score_quote(
                        text=clean_text,
                        speaker=speaker,
                        target_character=character,
                        in_quotes_section=True
                    )
                    
                    quotes.append(QuoteItem(
                        text=clean_text,
                        speaker=speaker,
                        section=section_name,
                        quote_id=quote_id,
                        confidence=confidence,
                        source_url=source_url
                    ))
        
        return quotes
    
    def _parse_global_fallback(self, soup: BeautifulSoup, character: str, 
                               source_url: str) -> List[QuoteItem]:
        """全局 fallback 解析"""
        quotes = []
        
        # 找所有可能的台词元素
        for elem in soup.find_all(["blockquote", "dd", "li"]):
            text = elem.get_text(strip=True)
            if self._is_valid_quote_text(text):
                speaker, clean_text = self._extract_speaker(text, character)
                quote_id = hashlib.md5(clean_text.encode()).hexdigest()[:8]
                
                confidence = self._score_quote(
                    text=clean_text,
                    speaker=speaker,
                    target_character=character,
                    in_quotes_section=False
                )
                
                quotes.append(QuoteItem(
                    text=clean_text,
                    speaker=speaker,
                    quote_id=quote_id,
                    confidence=confidence,
                    source_url=source_url
                ))
        
        return quotes
    
    def _extract_speaker(self, text: str, character: str) -> Tuple[str, str]:
        """
        提取 speaker 和 clean text
        
        Returns:
            (speaker, clean_text)
        """
        # 模式1: "角色名: 台词" 或 "角色名：台词"
        match = re.match(r'^([^：:]+)[：:]\s*(.+)$', text)
        if match:
            speaker = match.group(1).strip()
            clean_text = match.group(2).strip()
            return speaker, clean_text
        
        # 模式2: （角色名）台词
        match = re.match(r'^（([^）]+)）\s*(.+)$', text)
        if match:
            speaker = match.group(1).strip()
            clean_text = match.group(2).strip()
            return speaker, clean_text
        
        # 模式3: [角色名] 台词
        match = re.match(r'^\[([^\]]+)\]\s*(.+)$', text)
        if match:
            speaker = match.group(1).strip()
            clean_text = match.group(2).strip()
            return speaker, clean_text
        
        # 默认
        return "unknown", text
    
    def _score_quote(self, text: str, speaker: str, target_character: str, 
                     in_quotes_section: bool) -> float:
        """
        计算台词置信度 (0-1)
        """
        score = 0.0
        
        # 在 quotes section: +0.35
        if in_quotes_section:
            score += 0.35
        
        # 有明确 speaker 且匹配目标角色: +0.35
        if speaker != "unknown":
            if target_character.lower() in speaker.lower() or speaker.lower() in target_character.lower():
                score += 0.35
            else:
                # 有 speaker 但不匹配，+0.1
                score += 0.1
        
        # 文本长度合理: +0.15
        if 4 <= len(text) <= 180:
            score += 0.15
        
        # 命中对话标记: +0.15
        if any(c in text for c in ['「', '『', '"', '"', '"', '？', '！']):
            score += 0.15
        
        return min(score, 1.0)
    
    def _is_valid_quote_text(self, text: str) -> bool:
        """检查是否为有效台词文本"""
        if not text or len(text) < 4:
            return False
        # 过滤掉导航、模板等
        if text.startswith(("[", "{", "|", "*", "#")):
            return False
        # 过滤过长的（可能是段落）
        if len(text) > 300:
            return False
        return True
    
    def _deduplicate_quotes(self, quotes: List[QuoteItem]) -> List[QuoteItem]:
        """去重（基于 quote_id）"""
        seen = set()
        unique = []
        for q in quotes:
            if q.quote_id not in seen:
                seen.add(q.quote_id)
                unique.append(q)
        return unique
    
    def _fetch_browser(self, url: str, character: str) -> List[QuoteItem]:
        """
        Phase 2: Camofox 浏览器提取（Fandom 专用模板）
        
        针对 Fandom Quotes 子页面优化：
        - URL: /wiki/Character/Quotes
        - 结构: <dl><dt>Speaker</dt><dd>Quote</dd></dl>
        - 或者: <blockquote>Quote</blockquote>
        """
        # 尝试导入 Camofox
        try:
            from camofox import Camofox
        except ImportError:
            logger.warning("Camofox 未安装，跳过 browser 模式")
            return []
        
        quotes = []
        try:
            # 优先尝试 Quotes 子页面
            quotes_url = url.replace('/wiki/', '/wiki/') + '/Quotes'
            logger.info(f"Camofox 访问 Quotes 页面: {quotes_url}")
            
            with Camofox(headless=True) as browser:
                page = browser.new_page()
                
                # 访问 Quotes 子页面
                page.goto(quotes_url, timeout=60000)
                
                # 等待内容加载（Fandom 使用 .mw-parser-output）
                try:
                    page.wait_for_selector(".mw-parser-output", timeout=15000)
                except:
                    logger.warning("等待 .mw-parser-output 超时，尝试继续")
                
                # 提取 HTML
                content = page.content()
                soup = BeautifulSoup(content, 'html.parser')
                
                # 使用 Fandom 专用解析
                quotes = self._parse_fandom_quotes_page(soup, character, quotes_url)
                
                # 如果 Quotes 子页面没有内容，尝试主页面
                if not quotes:
                    logger.info(f"Quotes 子页面为空，尝试主页面: {url}")
                    page.goto(url, timeout=60000)
                    try:
                        page.wait_for_selector(".mw-parser-output", timeout=15000)
                    except:
                        pass
                    content = page.content()
                    soup = BeautifulSoup(content, 'html.parser')
                    quotes = self._parse_fandom_character_page(soup, character, url)
                
        except Exception as e:
            logger.error(f"Camofox 提取失败: {e}")
            return []
        
        # 过滤低置信度
        quotes = [q for q in quotes if q.confidence >= self.LOW_CONFIDENCE_THRESHOLD]
        return self._deduplicate_quotes(quotes)
    
    def _parse_fandom_quotes_page(self, soup: BeautifulSoup, character: str, source_url: str) -> List[QuoteItem]:
        """
        解析 Fandom Quotes 子页面
        
        Fandom 典型结构:
        <h2>Section Name</h2>
        <dl>
            <dt>Speaker Name</dt>
            <dd>"Quote text"</dd>
            <dt>Another Speaker</dt>
            <dd>"Another quote"</dd>
        </dl>
        """
        quotes = []
        content = soup.find('div', {'class': 'mw-parser-output'})
        if not content:
            return quotes
        
        current_section = ""
        
        for elem in content.find_all(['h2', 'h3', 'dl', 'blockquote']):
            # 更新当前 section
            if elem.name in ['h2', 'h3']:
                current_section = elem.get_text(strip=True).replace('[edit]', '').strip()
                continue
            
            # 解析 <dl> 列表（Fandom 常用）
            if elem.name == 'dl':
                dts = elem.find_all('dt')
                dds = elem.find_all('dd')
                
                for dt, dd in zip(dts, dds):
                    speaker = dt.get_text(strip=True)
                    text = dd.get_text(strip=True)
                    
                    if self._is_valid_quote_text(text):
                        clean_text = self._clean_quote_text(text)
                        quote_id = hashlib.md5(clean_text.encode()).hexdigest()[:8]
                        
                        # Fandom Quotes 页面置信度较高
                        confidence = 0.9 if speaker else 0.7
                        
                        quotes.append(QuoteItem(
                            text=clean_text,
                            speaker=speaker or "unknown",
                            section=current_section,
                            quote_id=quote_id,
                            confidence=confidence,
                            source_url=source_url
                        ))
            
            # 解析 <blockquote>（备用）
            elif elem.name == 'blockquote':
                text = elem.get_text(strip=True)
                if self._is_valid_quote_text(text):
                    clean_text = self._clean_quote_text(text)
                    quote_id = hashlib.md5(clean_text.encode()).hexdigest()[:8]
                    
                    quotes.append(QuoteItem(
                        text=clean_text,
                        speaker="unknown",
                        section=current_section,
                        quote_id=quote_id,
                        confidence=0.75,
                        source_url=source_url
                    ))
        
        return quotes
    
    def _parse_fandom_character_page(self, soup: BeautifulSoup, character: str, source_url: str) -> List[QuoteItem]:
        """
        解析 Fandom 角色主页面（查找 Quotes section）
        """
        quotes = []
        content = soup.find('div', {'class': 'mw-parser-output'})
        if not content:
            return quotes
        
        # 查找 Quotes section
        in_quotes_section = False
        current_section = ""
        
        for elem in content.children:
            if hasattr(elem, 'name'):
                # 检查是否是 Quotes section 的标题
                if elem.name in ['h2', 'h3']:
                    section_text = elem.get_text(strip=True).lower()
                    if any(k in section_text for k in ['quote', 'quotes', '台词', '名言']):
                        in_quotes_section = True
                        current_section = elem.get_text(strip=True).replace('[edit]', '').strip()
                    else:
                        in_quotes_section = False
                    continue
                
                # 如果在 Quotes section 内，提取台词
                if in_quotes_section:
                    if elem.name == 'dl':
                        dts = elem.find_all('dt')
                        dds = elem.find_all('dd')
                        for dt, dd in zip(dts, dds):
                            speaker = dt.get_text(strip=True)
                            text = dd.get_text(strip=True)
                            if self._is_valid_quote_text(text):
                                clean_text = self._clean_quote_text(text)
                                quote_id = hashlib.md5(clean_text.encode()).hexdigest()[:8]
                                quotes.append(QuoteItem(
                                    text=clean_text,
                                    speaker=speaker or "unknown",
                                    section=current_section,
                                    quote_id=quote_id,
                                    confidence=0.85,
                                    source_url=source_url
                                ))
                    elif elem.name == 'blockquote':
                        text = elem.get_text(strip=True)
                        if self._is_valid_quote_text(text):
                            clean_text = self._clean_quote_text(text)
                            quote_id = hashlib.md5(clean_text.encode()).hexdigest()[:8]
                            quotes.append(QuoteItem(
                                text=clean_text,
                                speaker="unknown",
                                section=current_section,
                                quote_id=quote_id,
                                confidence=0.7,
                                source_url=source_url
                            ))
        
        return quotes
    
    def _fetch_local(self, character: str) -> List[QuoteItem]:
        """Phase 3: 本地数据库兜底"""
        # 查找本地数据库
        db_paths = [
            Path(__file__).parent.parent.parent / "data" / "quotes_database.json",
            Path.cwd() / "data" / "quotes_database.json",
        ]
        
        for db_path in db_paths:
            if db_path.exists():
                try:
                    with open(db_path, 'r', encoding='utf-8') as f:
                        db = json.load(f)
                    
                    for key, data in db.items():
                        if character in key or key in character:
                            quotes = []
                            for q in data.get("quotes", []):
                                quote_id = hashlib.md5(q["text"].encode()).hexdigest()[:8]
                                quotes.append(QuoteItem(
                                    text=q["text"],
                                    speaker=q.get("speaker", "unknown"),
                                    context=q.get("context", ""),
                                    section=q.get("section", ""),
                                    quote_id=quote_id,
                                    confidence=0.8,  # 本地数据默认高置信度
                                    source_url=f"local://{db_path}"
                                ))
                            return quotes
                except Exception as e:
                    logger.warning(f"本地数据库读取失败: {e}")
        
        return []


def fetch_quotes_fandom(character: str, work: str, prefer: str = "api") -> Dict[str, Any]:
    """
    便捷函数：抓取 Fandom Wiki 角色台词
    
    Args:
        character: 角色英文名（如 "Eriri Spencer Sawamura"）
        work: 作品名（如 "Saekano"）
        prefer: 优先策略 api|browser
    
    Returns:
        dict: 结构化台词数据
    """
    fetcher = FandomHybridFetcher()
    result = fetcher.fetch(character, work, prefer)
    return result.to_dict()


if __name__ == "__main__":
    # 测试
    logging.basicConfig(level=logging.INFO)
    
    try:
        result = fetch_quotes_fandom("Eriri Spencer Sawamura", "Saekano")
        print(f"\n抓取成功！")
        print(f"角色: {result['character']}")
        print(f"来源: {result['source_type']}")
        print(f"台词数: {result['quote_count']}")
        print("\n前5条台词:")
        for i, q in enumerate(result['quotes'][:5], 1):
            print(f"{i}. [{q['speaker']}] {q['text'][:50]}... (置信度: {q['confidence']})")
    except Exception as e:
        print(f"抓取失败: {e}")
