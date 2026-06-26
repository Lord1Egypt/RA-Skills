"""
Wikiquote Fetcher 模块

从 MediaWiki API 抓取角色台词数据
支持缓存（24小时）、本地数据库兜底和分级错误处理
"""

import json
import hashlib
import os
import re
import time
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import List, Optional, Dict, Any
from urllib.parse import quote, unquote
import logging

import requests
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class Quote:
    """台词数据类"""
    text: str
    context: str = ""  # 场景/上下文
    emotion: str = ""  # 情绪标签
    source_url: str = ""
    section: str = ""
    quote_id: str = ""
    
    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class QuoteCollection:
    """角色台词集合"""
    character: str
    work: str = ""  # 作品名
    quotes: List[Quote] = field(default_factory=list)
    source_url: str = ""
    source_type: str = "api"  # api | local | cache
    fetched_at: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "character": self.character,
            "work": self.work,
            "quotes": [q.to_dict() for q in self.quotes],
            "source_url": self.source_url,
            "source_type": self.source_type,
            "fetched_at": self.fetched_at
        }
    
    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class WikiquoteError(Exception):
    """Wikiquote 抓取错误基类"""
    pass


class CharacterNotFoundError(WikiquoteError):
    """角色未找到错误: page不存在/无parse"""
    pass


class NetworkError(WikiquoteError):
    """网络错误: API请求失败"""
    pass


class ParseError(WikiquoteError):
    """解析错误: 有页面但无可用台词"""
    pass


class CacheManager:
    """缓存管理器 - 24小时缓存"""
    
    CACHE_DURATION = 24 * 60 * 60  # 24小时（秒）
    
    def __init__(self, cache_dir: Optional[str] = None):
        if cache_dir is None:
            cache_dir = os.path.join(os.path.dirname(__file__), "..", "cache")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(self, character: str, work: str) -> str:
        """生成缓存键"""
        key = f"{character}_{work}".lower().replace(" ", "_")
        return hashlib.md5(key.encode()).hexdigest()
    
    def _get_cache_path(self, character: str, work: str) -> Path:
        """获取缓存文件路径"""
        cache_key = self._get_cache_key(character, work)
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, character: str, work: str) -> Optional[QuoteCollection]:
        """获取缓存数据"""
        cache_path = self._get_cache_path(character, work)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查缓存是否过期
            fetched_at = data.get('fetched_at', 0)
            if time.time() - fetched_at > self.CACHE_DURATION:
                logger.info(f"缓存已过期: {character}@{work}")
                cache_path.unlink()
                return None
            
            # 重建 QuoteCollection
            quotes = [Quote(**q) for q in data.get('quotes', [])]
            return QuoteCollection(
                character=data['character'],
                work=data.get('work', ''),
                quotes=quotes,
                source_url=data.get('source_url', ''),
                source_type="cache",
                fetched_at=fetched_at
            )
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"缓存解析失败: {e}")
            cache_path.unlink(missing_ok=True)
            return None
    
    def set(self, collection: QuoteCollection) -> None:
        """设置缓存数据"""
        cache_path = self._get_cache_path(collection.character, collection.work)
        
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(collection.to_dict(), f, ensure_ascii=False, indent=2)
            logger.info(f"缓存已保存: {cache_path}")
        except IOError as e:
            logger.warning(f"缓存保存失败: {e}")


class WikiquoteFetcher:
    """
    MediaWiki API 台词抓取器
    """
    
    DEFAULT_DOMAIN = "zh.moegirl.org.cn"
    API_PATH = "/api.php"
    REQUEST_TIMEOUT = 10  # 请求超时（秒）
    MAX_RETRIES = 2  # 最大重试次数
    
    def __init__(self, cache_dir: Optional[str] = None):
        self.cache = CacheManager(cache_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AnimeCharacterLoader/1.0 (https://github.com/OpenClaw/anime-character-loader)',
        })
    
    def _get_api_url(self) -> str:
        return f"https://{self.DEFAULT_DOMAIN}{self.API_PATH}"

    def _fetch_api(self, character: str) -> Dict[str, Any]:
        """通过 MediaWiki API 获取页面解析后的 HTML 内容"""
        params = {
            "action": "parse",
            "page": character,
            "prop": "text",
            "format": "json",
            "redirects": 1
        }
        
        url = self._get_api_url()
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                logger.info(f"请求 API: {url} page={character} (尝试 {attempt + 1})")
                response = self.session.get(url, params=params, timeout=self.REQUEST_TIMEOUT)
                response.raise_for_status()
                data = response.json()
                
                if "error" in data:
                    code = data["error"].get("code", "unknown")
                    if code == "missingtitle":
                        raise CharacterNotFoundError(f"页面不存在: {character}")
                    raise ParseError(f"API 返回错误: {data['error'].get('info', code)}")
                
                if "parse" not in data or "text" not in data["parse"]:
                    raise CharacterNotFoundError(f"无法解析页面内容: {character}")
                
                return data["parse"]
                
            except requests.exceptions.RequestException as e:
                if attempt < self.MAX_RETRIES:
                    time.sleep(1)
                    continue
                raise NetworkError(f"API 请求失败: {e}")
        
        raise NetworkError("API 请求超出重试次数")

    def _extract_quotes(self, parse_data: Dict[str, Any], character: str) -> List[Quote]:
        """解析 parse.text['*'] 内容"""
        html_content = parse_data["text"]["*"]
        soup = BeautifulSoup(html_content, 'html.parser')
        
        quotes = []
        source_url = f"https://{self.DEFAULT_DOMAIN}/{quote(parse_data['title'])}"
        
        # 调试：看看 BeautifulSoup 到底看到了什么
        headers = soup.find_all(['h2', 'h3'])
        for header in headers:
            header_text = header.get_text().lower()
            # 兼容更多关键词
            if any(k in header_text for k in ['quote', '台词', '名言', '经典语录', '话语']):
                section_quotes = self._parse_section(header, source_url, character)
                quotes.extend(section_quotes)
        
        # Fallback: 如果没有找到明确的 Quotes section，则全局搜索 blockquote 或特定模式
        if not quotes:
            quotes.extend(self._parse_fallback(soup, source_url, character))
            
        # 最后的去重 (通过 quote_id)
        seen_ids = set()
        unique_quotes = []
        for q in quotes:
            if q.quote_id not in seen_ids:
                unique_quotes.append(q)
                seen_ids.add(q.quote_id)
                
        return unique_quotes

    def _parse_section(self, header, source_url: str, character: str) -> List[Quote]:
        section_name = header.get_text(strip=True).replace("[编辑]", "").strip()
        quotes = []
        
        # 遍历兄弟节点直到遇到下一个标题
        for curr in header.next_siblings:
            if hasattr(curr, 'name') and curr.name in ['h1', 'h2', 'h3']:
                break
                
            # 处理节点及其内部
            targets = []
            if hasattr(curr, 'name'):
                if curr.name in ['blockquote', 'p', 'li', 'dd']:
                    targets.append(curr)
                if hasattr(curr, 'find_all'):
                    targets.extend(curr.find_all(['blockquote', 'p', 'li', 'dd']))
            
            for item in targets:
                text = item.get_text(strip=True)
                if self._is_likely_quote(text, character):
                    clean_text = self._clean_quote_text(text)
                    if clean_text:
                        quote_id = hashlib.md5(clean_text.encode()).hexdigest()[:8]
                        # 避免在同一 Section 内重复
                        if not any(q.quote_id == quote_id for q in quotes):
                            quotes.append(Quote(
                                text=clean_text,
                                context=section_name,
                                emotion=self._analyze_emotion(clean_text, section_name),
                                source_url=source_url,
                                section=section_name,
                                quote_id=quote_id
                            ))
        return quotes

    def _parse_fallback(self, soup: BeautifulSoup, source_url: str, character: str) -> List[Quote]:
        quotes = []
        # 仅在 mw-parser-output 内部搜索
        container = soup.find(class_="mw-parser-output") or soup
        
        for block in container.find_all(['blockquote', 'dd']):
            text = block.get_text(strip=True)
            if self._is_likely_quote(text, character):
                clean_text = self._clean_quote_text(text)
                if clean_text:
                    quote_id = hashlib.md5(clean_text.encode()).hexdigest()[:8]
                    quotes.append(Quote(
                        text=clean_text,
                        source_url=source_url,
                        section="General",
                        quote_id=quote_id,
                        emotion=self._analyze_emotion(clean_text, "")
                    ))
        return quotes

    def _clean_quote_text(self, text: str) -> str:
        text = re.sub(r'^["""「『]', '', text)
        text = re.sub(r'["""」』]$', '', text)
        text = re.sub(r'\[\d+\]', '', text)  # 移除引用 [1]
        text = ' '.join(text.split())
        return text.strip()

    def _is_likely_quote(self, text: str, character: str) -> bool:
        if not text: return False
        text = text.strip()
        if len(text) < 2: return False
        if any(c in text for c in ['「', '『', '“', '”', '\"']): return True
        return len(text) >= 4

    def _analyze_emotion(self, text: str, context: str) -> str:
        combined = f"{text} {context}".lower()
        patterns = {
            "傲娇": [r'バカ|笨蛋|baka', r'哼', r'才不是'],
            "温柔": [r'谢谢|ありがとう', r'喜欢|好き', r'没事|大丈夫'],
            "生气": [r'可恶|くそ', r'不行|だめ'],
        }
        for emotion, ps in patterns.items():
            if any(re.search(p, combined) for p in ps): return emotion
        return "平静"

    def _load_from_local_db(self, character: str) -> Optional[QuoteCollection]:
        db_paths = [
            Path(__file__).parent.parent.parent.parent / "data" / "quotes_database.json",
            Path.cwd() / "data" / "quotes_database.json",
        ]
        # 调试输出：让测试时明确查找路径
        for path in db_paths:
            logger.debug(f"正在查找本地数据库: {path}")
            if path.exists():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        db = json.load(f)
                    if character in db:
                        data = db[character]
                        quotes = [Quote(**{**q, "source_url": f"local://{path}"}) for q in data.get('quotes', [])]
                        return QuoteCollection(
                            character=character,
                            work=data.get('work', ''),
                            quotes=quotes,
                            source_url=f"local://{path}",
                            source_type="local"
                        )
                except Exception as e:
                    logger.warning(f"本地数据库加载异常: {e}")
        return None

    def fetch(self, character: str, work: str = "", use_cache: bool = True) -> QuoteCollection:
        if use_cache:
            cached = self.cache.get(character, work)
            if cached: return cached
            
        try:
            parse_data = self._fetch_api(character)
            quotes = self._extract_quotes(parse_data, character)
            
            if not quotes:
                raise ParseError(f"页面存在但未提取到有效台词: {character}")
                
            collection = QuoteCollection(
                character=parse_data["title"],
                work=work,
                quotes=quotes,
                source_url=f"https://{self.DEFAULT_DOMAIN}/{quote(parse_data['title'])}",
                source_type="api"
            )
            self.cache.set(collection)
            return collection
            
        except (NetworkError, CharacterNotFoundError, ParseError) as e:
            logger.warning(f"API 获取/解析失败，尝试本地兜底: {e}")
            local = self._load_from_local_db(character)
            if local: return local
            raise e


def fetch_quotes(character: str, work: str = "", use_cache: bool = True) -> Dict[str, Any]:
    fetcher = WikiquoteFetcher()
    return fetcher.fetch(character, work, use_cache).to_dict()


if __name__ == "__main__":
    try:
        res = fetch_quotes("加藤惠")
        print(json.dumps(res, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
