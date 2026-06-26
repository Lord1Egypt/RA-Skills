#!/usr/bin/env python3
"""Legacy implementation snapshot from pre-refactor single-file script."""
#!/usr/bin/env python3
"""
Anime Character Loader v2.0 - Multi-source character data with validation

优化重点：
1. 多源数据并行查询（AniList + Jikan + MediaWiki）
2. 失败重试、限流、缓存
3. 角色重名消歧机制
4. 可回滚、可验证的生成流程
5. 量化验收清单
"""

import sys
import json
import re
import os
import shutil
import argparse
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3

try:
    import requests
except ImportError:
    print("Error: requests module not found. Install with: pip install requests")
    sys.exit(1)

# ============== 配置 ==============
CACHE_DIR = os.path.expanduser("~/.cache/anime-character-loader")
CACHE_DURATION = timedelta(hours=24)  # 缓存24小时
MAX_RETRIES = 3
RETRY_DELAY = 2  # 秒
RATE_LIMIT_DELAY = 0.5  # API调用间隔

# 置信度阈值
CONFIDENCE_THRESHOLD_HIGH = 0.8
CONFIDENCE_THRESHOLD_MEDIUM = 0.6
CONFIDENCE_THRESHOLD_LOW = 0.5

# 强制消歧设置
FORCE_DISAMBIGUATION = True  # 是否强制要求消歧提示

# 高风险名字列表 - 这些名字即使单匹配也必须提供 --anime 提示
AMBIGUOUS_NAMES = {
    # 常见名字（多作品出现）
    "sakura", "rin", "miku", "yuki", "haruka", "kaori", "maki", "nana",
    "akira", "kira", "rei", "asuka", "maya", "yui", "mio", "azusa",
    # 常见姓氏
    "sato", "suzuki", "takahashi", "tanaka", "watanabe", "ito", "yamamoto",
    # 单个字（极高风险）
    "sora", "aoi", "hikari", "kage", "tsuki", "hana", "yume", "kaze",
}

# ============== 数据源配置 ==============
SOURCES = {
    "anilist": {
        "name": "AniList",
        "endpoint": "https://graphql.anilist.co",
        "weight": 0.5,
        "enabled": True,
    },
    "jikan": {
        "name": "Jikan (MyAnimeList)",
        "endpoint": "https://api.jikan.moe/v4",
        "weight": 0.3,
        "enabled": True,
    },
    "wikia": {
        "name": "Fandom Wikia",
        "endpoint": "https://{wiki}.fandom.com/api.php",
        "weight": 0.2,
        "enabled": True,
    }
}

# 中文名映射（扩展版）
NAME_MAPPING = {
    # Saekano
    "霞之丘诗羽": ("Kasumigaoka Utaha", "Saenai Heroine no Sodatekata"),
    "霞ヶ丘詩羽": ("Kasumigaoka Utaha", "Saenai Heroine no Sodatekata"),
    "加藤惠": ("Katou Megumi", "Saenai Heroine no Sodatekata"),
    "加藤恵": ("Katou Megumi", "Saenai Heroine no Sodatekata"),
    "Kato Megumi": ("Katou Megumi", "Saenai Heroine no Sodatekata"),
    
    # Railgun
    "御坂美琴": ("Misaka Mikoto", "Toaru Kagaku no Railgun"),
    "美琴": ("Misaka Mikoto", "Toaru Kagaku no Railgun"),
    "炮姐": ("Misaka Mikoto", "Toaru Kagaku no Railgun"),
    "bilibili": ("Misaka Mikoto", "Toaru Kagaku no Railgun"),
    
    # Oregairu
    "雪之下雪乃": ("Yukinoshita Yukino", "Yahari Ore no Seishun Love Comedy wa Machigatteiru"),
    "由比滨结衣": ("Yuigahama Yui", "Yahari Ore no Seishun Love Comedy wa Machigatteiru"),
    "一色彩羽": ("Isshiki Iroha", "Yahari Ore no Seishun Love Comedy wa Machigatteiru"),
    
    # Bunny Girl Senpai
    "樱岛麻衣": ("Sakurajima Mai", "Seishun Buta Yarou"),
    
    # Steins;Gate
    "牧濑红莉栖": ("Makise Kurisu", "Steins;Gate"),
    
    # Sakurasou
    "椎名真白": ("Shiina Mashiro", "Sakurasou no Pet na Kanojo"),
    
    # Fate
    "阿尔托莉雅": ("Artoria Pendragon", "Fate/stay night"),
    "Saber": ("Artoria Pendragon", "Fate/stay night"),
    "远坂凛": ("Tohsaka Rin", "Fate/stay night"),
    "间桐樱": ("Matou Sakura", "Fate/stay night"),
}


class ConfidenceLevel(Enum):
    HIGH = "high"      # >= 0.8
    MEDIUM = "medium"  # 0.5 - 0.8
    LOW = "low"        # < 0.5


@dataclass
class CharacterMatch:
    """角色匹配结果"""
    name: str
    source: str
    source_work: str
    confidence: float
    data: Dict[str, Any]
    disambiguation_note: str = ""


@dataclass
class ValidationResult:
    """验证结果"""
    passed: bool
    score: float  # 0-100
    checks: Dict[str, Tuple[bool, str]]  # 检查项: (通过, 说明)
    errors: List[str]


# ============== 缓存管理 ==============
class CacheManager:
    def __init__(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        self.db_path = os.path.join(CACHE_DIR, "cache.db")
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_cache (
                    key TEXT PRIMARY KEY,
                    data TEXT,
                    created_at TIMESTAMP
                )
            """)
    
    def get(self, key: str) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT data, created_at FROM api_cache WHERE key = ?",
                (key,)
            ).fetchone()
            
            if row:
                data, created_at = row
                created = datetime.fromisoformat(created_at)
                if datetime.now() - created < CACHE_DURATION:
                    return json.loads(data)
                else:
                    conn.execute("DELETE FROM api_cache WHERE key = ?", (key,))
        return None
    
    def set(self, key: str, data: Dict):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO api_cache (key, data, created_at) VALUES (?, ?, ?)",
                (key, json.dumps(data), datetime.now().isoformat())
            )


cache = CacheManager()


# ============== API 客户端 ==============
class APIClient:
    """带重试和限流的 API 客户端"""
    
    @staticmethod
    def request(url: str, method: str = "GET", **kwargs) -> Optional[Dict]:
        cache_key = hashlib.md5(f"{method}:{url}:{json.dumps(kwargs)}".encode()).hexdigest()
        
        # 检查缓存
        cached = cache.get(cache_key)
        if cached:
            print(f"  📦 Cache hit for {url[:50]}...")
            return cached
        
        for attempt in range(MAX_RETRIES):
            try:
                time.sleep(RATE_LIMIT_DELAY)  # 限流
                
                if method == "POST":
                    response = requests.post(url, timeout=30, **kwargs)
                else:
                    response = requests.get(url, timeout=30, **kwargs)
                
                response.raise_for_status()
                data = response.json()
                
                # 写入缓存
                cache.set(cache_key, data)
                return data
                
            except requests.exceptions.RequestException as e:
                print(f"  ⚠️ Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    print(f"  ❌ Max retries reached for {url}")
                    return None
            except json.JSONDecodeError as e:
                print(f"  ❌ JSON parse error: {e}")
                return None
        
        return None


# ============== 数据源查询 ==============
class AniListSource:
    """AniList GraphQL 数据源"""
    
    QUERY = """
    query ($search: String) {
      Character(search: $search) {
        id
        name {
          full
          native
          alternative
        }
        description(asHtml: false)
        image {
          large
        }
        media(sort: POPULARITY_DESC, perPage: 5) {
          nodes {
            id
            title {
              romaji
              native
            }
            type
            popularity
          }
        }
      }
    }
    """
    
    @classmethod
    def search(cls, name: str) -> Optional[Dict]:
        print(f"  🔍 Querying AniList...")
        data = APIClient.request(
            SOURCES["anilist"]["endpoint"],
            "POST",
            json={"query": cls.QUERY, "variables": {"search": name}},
            headers={"Content-Type": "application/json"}
        )
        
        if data and "data" in data and data["data"].get("Character"):
            char = data["data"]["Character"]
            return {
                "id": char["id"],
                "name": char["name"]["full"],
                "name_native": char["name"].get("native", ""),
                "aliases": char["name"].get("alternative", []),
                "description": char.get("description", ""),
                "image": char.get("image", {}).get("large", ""),
                "source_works": [
                    {
                        "title": m.get("title", {}).get("romaji", ""),
                        "type": m.get("type", ""),
                        "popularity": m.get("popularity", 0)
                    }
                    for m in char.get("media", {}).get("nodes", [])
                ],
                "confidence": 0.9 if char["name"]["full"].lower() == name.lower() else 0.7,
            }
        return None


class JikanSource:
    """Jikan (MyAnimeList) 数据源"""
    
    @classmethod
    def search(cls, name: str) -> Optional[Dict]:
        print(f"  🔍 Querying Jikan...")
        data = APIClient.request(
            f"{SOURCES['jikan']['endpoint']}/characters",
            params={"q": name, "limit": 5}
        )
        
        if data and "data" in data and data["data"]:
            # 找最匹配的
            best_match = None
            best_score = 0
            
            for char in data["data"]:
                score = cls._calc_match_score(name, char)
                if score > best_score:
                    best_score = score
                    best_match = char
            
            if best_match:
                char = best_match
                return {
                    "id": char["mal_id"],
                    "name": char.get("name", ""),
                    "name_native": char.get("name_kanji", ""),
                    "aliases": [],
                    "description": "",  # Jikan 详情需要单独请求
                    "image": char.get("images", {}).get("jpg", {}).get("image_url", ""),
                    "source_works": [],
                    "confidence": best_score,
                }
        return None
    
    @staticmethod
    def _calc_match_score(query: str, char: Dict) -> float:
        name = char.get("name", "").lower()
        query_lower = query.lower()
        
        if query_lower == name:
            return 1.0
        if query_lower in name or name in query_lower:
            return 0.8
        return 0.5


class WikiaSource:
    """Fandom Wikia 数据源（备用）"""
    
    @classmethod
    def search(cls, name: str, anime_name: str = "") -> Optional[Dict]:
        print(f"  🔍 Querying Fandom Wikia...")
        
        # 需要知道具体是哪个作品的 wiki
        wiki_map = {
            "saekano": "saekano",
            "railgun": "toarumajutsunoindex",
            "oregairu": "yahari",
            "steins gate": "steins-gate",
        }
        
        # 简化处理：跳过 wikia，或者根据 anime_name 映射
        return None


# ============== 核心逻辑 ==============
class CharacterLoader:
    """角色加载器主类"""
    
    def __init__(self):
        self.sources = [AniListSource, JikanSource]
    
    def translate_name(self, name: str) -> Tuple[str, str]:
        """翻译中文名，返回 (英文名, 作品名)"""
        name_clean = name.strip()
        
        if name_clean in NAME_MAPPING:
            return NAME_MAPPING[name_clean]
        
        for cn, (en, work) in NAME_MAPPING.items():
            if cn in name_clean or name_clean in cn:
                return (en, work)
        
        return (name, "")
    
    def query_multi_source(self, name: str, anime_hint: str = "") -> List[CharacterMatch]:
        """多源并行查询，返回匹配列表"""
        print(f"\n🔍 Querying multiple sources for: {name}")
        print("-" * 50)
        
        matches = []
        
        for source_class in self.sources:
            try:
                result = source_class.search(name)
                if result:
                    match = CharacterMatch(
                        name=result["name"],
                        source=source_class.__name__.replace("Source", ""),
                        source_work=result.get("source_works", [{}])[0].get("title", "Unknown") if result.get("source_works") else "Unknown",
                        confidence=result.get("confidence", 0.5),
                        data=result
                    )
                    matches.append(match)
                    print(f"  ✅ Found: {match.name} (confidence: {match.confidence:.2f})")
            except Exception as e:
                print(f"  ❌ Error querying {source_class.__name__}: {e}")
        
        # 按置信度排序
        matches.sort(key=lambda x: x.confidence, reverse=True)
        return matches
    
    def is_ambiguous_name(self, name: str) -> bool:
        """检查名字是否是常见/模糊的（需要强制消歧）"""
        name_lower = name.lower()
        # 检查名字的任何部分是否在模糊列表中
        for ambiguous in AMBIGUOUS_NAMES:
            if ambiguous in name_lower or name_lower in ambiguous:
                return True
        # 单个词的名字通常也模糊
        if len(name_lower.split()) == 1 and len(name_lower) <= 6:
            return True
        return False
    
    def disambiguate(self, matches: List[CharacterMatch], user_hint: str = "", 
                     force_hint: bool = True, original_query: str = "") -> Optional[CharacterMatch]:
        """角色消歧 - 强制模式：无提示时更严格"""
        if not matches:
            return None
        
        # 单匹配情况
        if len(matches) == 1:
            match = matches[0]
            # 检查是否是模糊名字（强制消歧加强）
            is_ambiguous = self.is_ambiguous_name(match.name) or self.is_ambiguous_name(original_query)
            
            if force_hint and not user_hint and is_ambiguous:
                print(f"\n⚠️ Ambiguous name detected: '{match.name}'")
                print(f"   This is a common name that appears in multiple works.")
                print(f"   Source: {match.source_work}")
                print(f"   💡 Use --anime '{match.source_work}' to confirm")
                return None
            
            # 强制消歧：即使是单匹配，无提示且置信度不够高也需要确认
            if force_hint and not user_hint and match.confidence < CONFIDENCE_THRESHOLD_HIGH:
                print(f"\n⚠️ Single match but low confidence without anime hint: {match.name} ({match.confidence:.2f})")
                print(f"   Source: {match.source_work}")
                print(f"   💡 Use --anime '{match.source_work}' to confirm")
                return None
            
            if match.confidence >= CONFIDENCE_THRESHOLD_LOW:
                return match
            else:
                print(f"\n⚠️ Low confidence match: {match.name} ({match.confidence:.2f})")
                return None
        
        # 多个匹配，需要消歧
        print(f"\n⚠️ Multiple matches found ({len(matches)}):")
        for i, match in enumerate(matches[:5], 1):
            print(f"  {i}. {match.name} from {match.source_work}")
            print(f"     Source: {match.source}, Confidence: {match.confidence:.2f}")
        
        # 如果有用户提示，尝试匹配
        if user_hint:
            for match in matches:
                if user_hint.lower() in match.source_work.lower():
                    print(f"\n✅ Auto-selected based on hint: {match.name}")
                    return match
            # 提示匹配失败
            print(f"\n⚠️ Hint '{user_hint}' didn't match any source work")
        
        # 强制消歧模式：无提示时必须人工选择
        if force_hint and not user_hint:
            print(f"\n❌ Force disambiguation enabled: --anime hint required")
            print(f"   Examples:")
            for match in matches[:3]:
                print(f"     --anime '{match.source_work}'")
            return None
        
        # 高置信度优先（仅在非强制模式或已有提示时）
        high_conf = [m for m in matches if m.confidence >= CONFIDENCE_THRESHOLD_HIGH]
        if len(high_conf) == 1:
            print(f"\n✅ Auto-selected high confidence match: {high_conf[0].name}")
            return high_conf[0]
        
        # 需要人工选择
        return None
    
    def _sanitize_field(self, value: str) -> str:
        """清洗字段值，防止 prompt injection"""
        if not value:
            return ""
        
        # 移除控制字符
        value = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', value)
        value = re.sub(r'[\u200b-\u200f\ufeff]', '', value)
        
        # 移除换行和特殊markdown字符
        value = value.replace('\n', ' ').replace('\r', ' ')
        value = re.sub(r'[#*`\[\]<>]', '', value)
        
        return value.strip()
    
    def generate_soul(self, match: CharacterMatch) -> str:
        """生成 SOUL.md"""
        data = match.data
        name = self._sanitize_field(data.get("name", "Unknown"))
        source_work = self._sanitize_field(match.source_work)
        
        # 清洗描述
        description = self._clean_description(data.get("description", ""))
        
        # 提取性格特征
        traits = self._extract_personality(description)
        
        # 构建 SOUL
        lines = [
            f"# {name}",
            "",
            f"**Source:** {source_work}",
            "",
        ]
        
        if data.get("name_native"):
            native_name = self._sanitize_field(data['name_native'])
            lines.append(f"**Japanese Name:** {native_name}")
        
        if data.get("aliases"):
            safe_aliases = [self._sanitize_field(a) for a in data['aliases'][:3]]
            lines.append(f"**Also Known As:** {', '.join(safe_aliases)}")
        
        lines.extend([
            "",
            "---",
            "",
            "## Identity",
            "",
            f"You are {name}, a character from {match.source_work}.",
            "",
        ])
        
        if description:
            lines.extend([
                "## Background",
                "",
                description[:800] if len(description) > 800 else description,
                "",
            ])
        
        lines.extend([
            "## Personality",
            "",
        ])
        
        if traits:
            for trait in traits[:5]:
                lines.append(f"- {trait}")
        else:
            lines.append("- Adapt personality based on source material")
        
        lines.extend([
            "",
            "## Speaking Style",
            "",
            "- Maintain established personality and speech patterns",
            "- Use characteristic vocabulary and expressions",
            "- Stay true to relationships with other characters",
        ])
        
        # 根据描述添加特征
        desc_lower = description.lower()
        if any(w in desc_lower for w in ["sarcastic", "sharp tongue", "毒舌"]):
            lines.append("- You have a sharp tongue and can be sarcastic")
        if any(w in desc_lower for w in ["calm", "composed", "冷静"]):
            lines.append("- Speak in a calm, composed manner")
        if any(w in desc_lower for w in ["shy", "embarrassed", "害羞"]):
            lines.append("- Can become shy or flustered in certain situations")
        
        lines.extend([
            "",
            "## Boundaries",
            "",
            f"- Stay in character as {name}",
            f"- Reference events and relationships from {source_work}",
            "- Do not break the fourth wall unless characteristic",
            "- Maintain appropriate emotional responses",
            "",
            "---",
            "",
            f"*Generated by anime-character-loader v2.0 on {datetime.now().strftime('%Y-%m-%d')}*",
            f"*Data sources: {match.source} (confidence: {match.confidence:.2f})*",
        ])
        
        return "\n".join(lines)
    
    def _clean_description(self, desc: str) -> str:
        """清洗描述文本 - 防止 prompt injection"""
        if not desc:
            return ""
        
        # 移除 HTML 标签
        desc = re.sub(r'<[^>]+>', '', desc)
        
        # 移除 markdown 链接
        desc = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', desc)
        
        # 清理多余换行
        desc = re.sub(r'\n{3,}', '\n\n', desc)
        
        # 防止 prompt injection: 移除角色标记和指令覆盖尝试
        # 移除常见的 injection 模式
        injection_patterns = [
            r'\[system\]:.*',           # [system]: ...
            r'\[user\]:.*',              # [user]: ...
            r'\[assistant\]:.*',         # [assistant]: ...
            r'ignore previous instructions.*',
            r'ignore all previous.*',
            r'reveal your.*prompt.*',
            r'system prompt.*',
            r'you are now.*',
            r'<system>.*</system>',
            r'<instruction>.*</instruction>',
        ]
        
        for pattern in injection_patterns:
            desc = re.sub(pattern, '', desc, flags=re.IGNORECASE)
        
        # 移除控制字符和零宽字符
        desc = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', desc)
        desc = re.sub(r'[\u200b-\u200f\ufeff]', '', desc)  # 零宽字符
        
        return desc.strip()
    
    def _extract_personality(self, description: str) -> List[str]:
        """提取性格特征"""
        traits = []
        keywords = [
            "tsundere", "yandere", "kuudere", "dandere", "genki",
            "calm", "quiet", "shy", "confident", "intelligent",
            "hardworking", "cheerful", "serious", "playful", "kind",
            "cold", "warm", "sarcastic", "gentle", "strong",
        ]
        
        desc_lower = description.lower()
        
        for keyword in keywords:
            if keyword in desc_lower:
                idx = desc_lower.find(keyword)
                start = max(0, idx - 30)
                end = min(len(description), idx + len(keyword) + 30)
                context = description[start:end].strip()
                traits.append(context)
        
        if not traits:
            sentences = re.split(r'[.!?。！？]+', description)
            for sent in sentences:
                sent = sent.strip()
                if len(sent) > 10 and any(word in sent.lower() for word in 
                    ["personality", "character", "usually", "often", "tends"]):
                    traits.append(sent)
        
        return traits[:5]
    
    def validate_soul(self, content: str, original_data: Dict) -> ValidationResult:
        """验证生成的 SOUL.md 质量 - 加强语义校验"""
        checks = {}
        errors = []
        warnings = []
        
        # 检查1: 必须包含角色名
        name = original_data.get("name", "")
        has_name = name in content
        checks["contains_name"] = (has_name, f"Character name '{name}' present" if has_name else f"Missing character name '{name}'")
        if not has_name:
            errors.append("Missing character name")
        
        # 检查2: 必须包含作品名
        source_work = original_data.get("source_works", [{}])[0].get("title", "") if original_data.get("source_works") else ""
        has_source = source_work in content or any(w in content for w in ["Source:", "**Source:**"])
        checks["contains_source"] = (has_source, "Source work referenced" if has_source else "Missing source work")
        if not has_source:
            errors.append("Missing source work reference")
        
        # 检查3: 结构完整性
        required_sections = ["## Identity", "## Personality", "## Boundaries"]
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        has_structure = len(missing_sections) == 0
        checks["has_structure"] = (has_structure, "All required sections present" if has_structure else f"Missing: {', '.join(missing_sections)}")
        if missing_sections:
            errors.append(f"Missing sections: {missing_sections}")
        
        # 检查4: 内容长度
        content_length = len(content)
        has_content = content_length >= 500
        checks["content_length"] = (has_content, f"Content length: {content_length} chars" if has_content else f"Content too short: {content_length} chars")
        if not has_content:
            errors.append("Content too short")
        
        # 检查5: 无占位符文本
        placeholder_patterns = ["TODO", "FIXME", "placeholder", "adapt personality"]
        has_placeholders = any(p.lower() in content.lower() for p in placeholder_patterns)
        checks["no_placeholders"] = (not has_placeholders, "No placeholder text" if not has_placeholders else "Contains placeholder text")
        if has_placeholders:
            errors.append("Contains placeholder text")
        
        # === 新增语义校验 ===
        
        # 检查6: Background 章节内容质量
        bg_match = re.search(r'## Background\s*\n\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
        if bg_match:
            bg_content = bg_match.group(1).strip()
            bg_lines = [l for l in bg_content.split('\n') if l.strip()]
            has_meaningful_bg = len(bg_lines) >= 2 and len(bg_content) >= 100
            checks["meaningful_background"] = (has_meaningful_bg, f"Background: {len(bg_lines)} lines, {len(bg_content)} chars" if has_meaningful_bg else "Background too brief")
            if not has_meaningful_bg:
                warnings.append("Background section lacks meaningful content")
        else:
            checks["has_background"] = (False, "Missing Background section")
            warnings.append("Missing Background section")
        
        # 检查7: Personality 具体性
        personality_match = re.search(r'## Personality\s*\n\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
        if personality_match:
            p_content = personality_match.group(1).strip()
            # 检查是否有具体性格描述（不只是占位符）
            vague_patterns = ["adapt personality", "based on", "source material"]
            is_vague = any(p in p_content.lower() for p in vague_patterns)
            has_specific_traits = len(p_content) > 50 and not is_vague
            checks["specific_personality"] = (has_specific_traits, "Personality has specific traits" if has_specific_traits else "Personality too vague/generic")
            if not has_specific_traits:
                warnings.append("Personality description is too generic")
        
        # 检查8: Speaking Style 完整性
        ss_match = re.search(r'## Speaking Style\s*\n\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
        if ss_match:
            ss_content = ss_match.group(1).strip()
            ss_bullets = [l for l in ss_content.split('\n') if l.strip().startswith('-')]
            has_speaking_details = len(ss_bullets) >= 2
            checks["speaking_style_details"] = (has_speaking_details, f"Speaking Style: {len(ss_bullets)} bullet points" if has_speaking_details else "Speaking Style lacks details")
            if not has_speaking_details:
                warnings.append("Speaking Style section needs more detail")
        else:
            checks["has_speaking_style"] = (False, "Missing Speaking Style section")
            warnings.append("Missing Speaking Style section")
        
        # 检查9: 数据一致性 - 角色名在多个地方一致
        name_variations = [
            original_data.get("name", ""),
            original_data.get("name_native", ""),
        ]
        name_variations = [n for n in name_variations if n]
        name_consistency = sum(1 for n in name_variations if n in content)
        checks["name_consistency"] = (name_consistency > 0, f"Name consistency: {name_consistency}/{len(name_variations)} variations found")
        
        # 计算总分 (错误扣重分，警告扣轻分)
        passed_checks = sum(1 for passed, _ in checks.values() if passed)
        total_checks = len(checks)
        base_score = (passed_checks / total_checks) * 100
        
        # 扣分机制
        error_penalty = len(errors) * 15  # 每个错误扣15分
        warning_penalty = len(warnings) * 5  # 每个警告扣5分
        
        score = max(0, base_score - error_penalty - warning_penalty)
        
        return ValidationResult(
            passed=len(errors) == 0 and score >= 80,
            score=score,
            checks=checks,
            errors=errors
        )


# ============== 文件操作 ==============
class FileManager:
    """文件管理（支持回滚）"""
    
    TEMP_DIR = os.path.join(CACHE_DIR, "temp")
    
    @classmethod
    def ensure_dirs(cls):
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
    
    @classmethod
    def generate_temp_path(cls, character_name: str) -> str:
        """生成临时文件路径"""
        safe_name = re.sub(r'[^\w\s-]', '', character_name).strip().replace(' ', '_')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return os.path.join(cls.TEMP_DIR, f"{safe_name}_{timestamp}_SOUL.md")
    
    @classmethod
    def _sanitize_output_dir(cls, output_dir: str) -> str:
        """验证并清理输出目录，防止路径遍历攻击"""
        # 解析为绝对路径
        output_dir = os.path.abspath(os.path.expanduser(output_dir))
        
        # 检查是否包含路径遍历序列
        normalized = os.path.normpath(output_dir)
        if '..' in normalized.split(os.sep):
            raise ValueError(f"Invalid output directory: path traversal detected in '{output_dir}'")
        
        # 确保目录存在或是可创建的
        try:
            os.makedirs(output_dir, exist_ok=True)
        except (OSError, PermissionError) as e:
            raise ValueError(f"Cannot create or access output directory '{output_dir}': {e}")
        
        return output_dir
    
    @classmethod
    def generate_final_path(cls, character_name: str, output_dir: str) -> str:
        """生成最终文件路径 - 使用 SOUL.generated.md 约定"""
        safe_dir = cls._sanitize_output_dir(output_dir)
        return os.path.join(safe_dir, "SOUL.generated.md")
    
    @classmethod
    def generate_character_path(cls, character_name: str, output_dir: str) -> str:
        """生成角色专用文件路径 - 用于多角色模式"""
        safe_dir = cls._sanitize_output_dir(output_dir)
        safe_name = re.sub(r'[^\w\s-]', '', character_name).strip().replace(' ', '_')
        return os.path.join(safe_dir, f"{safe_name}_SOUL.md")
    
    @classmethod
    def write_temp(cls, content: str, character_name: str) -> str:
        """写入临时文件"""
        cls.ensure_dirs()
        temp_path = cls.generate_temp_path(character_name)
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return temp_path
    
    @classmethod
    def commit(cls, temp_path: str, final_path: str) -> str:
        """提交（从临时到最终）"""
        # 备份已存在的文件
        if os.path.exists(final_path):
            backup_path = f"{final_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(final_path, backup_path)
            print(f"  📦 Backed up existing file to: {backup_path}")
        
        os.rename(temp_path, final_path)
        return final_path
    
    @classmethod
    def rollback(cls, temp_path: str):
        """回滚（删除临时文件）"""
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"  🗑️  Rolled back temp file: {temp_path}")
    
    @classmethod
    def structured_merge(cls, generated_path: str, existing_path: str, character_name: str) -> str:
        """结构化合并：将生成的角色内容合并到现有 SOUL.md"""
        
        # 读取现有 SOUL.md
        with open(existing_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # 读取生成的内容
        with open(generated_path, 'r', encoding='utf-8') as f:
            generated_content = f.read()
        
        # 提取生成的角色核心信息
        char_identity = cls._extract_section(generated_content, "Identity")
        char_personality = cls._extract_section(generated_content, "Personality")
        char_speaking = cls._extract_section(generated_content, "Speaking Style")
        char_boundaries = cls._extract_section(generated_content, "Boundaries")
        
        # 构建合并后的内容
        merged_lines = []
        
        # 保留现有文件的头部（如果有）
        if existing_content.strip():
            merged_lines.append(existing_content.rstrip())
            merged_lines.append("\n\n")
            merged_lines.append("---")
            merged_lines.append(f"\n\n# Additional Character: {character_name}\n")
        else:
            merged_lines.append(f"# Multi-Character SOUL\n")
        
        # 添加角色身份（简化版）
        if char_identity:
            merged_lines.append("\n## Identity")
            merged_lines.append(f"\n{char_identity}\n")
        
        # 添加性格特征
        if char_personality:
            merged_lines.append("\n## Personality Traits")
            merged_lines.append(f"\n{char_personality}\n")
        
        # 添加说话风格
        if char_speaking:
            merged_lines.append("\n## Speaking Style")
            merged_lines.append(f"\n{char_speaking}\n")
        
        # 添加边界
        if char_boundaries:
            merged_lines.append("\n## Boundaries")
            merged_lines.append(f"\n{char_boundaries}\n")
        
        # 添加来源标记
        merged_lines.append("\n---")
        merged_lines.append(f"\n*Character '{character_name}' merged on {datetime.now().strftime('%Y-%m-%d')}*")
        
        merged_content = "\n".join(merged_lines)
        
        # 备份并写入
        backup_path = f"{existing_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.rename(existing_path, backup_path)
        
        with open(existing_path, 'w', encoding='utf-8') as f:
            f.write(merged_content)
        
        print(f"  📦 Backed up existing SOUL.md to: {backup_path}")
        print(f"  ✅ Merged character '{character_name}' into: {existing_path}")
        
        return existing_path
    
    @classmethod
    def _extract_section(cls, content: str, section_name: str) -> str:
        """提取特定章节内容"""
        pattern = rf'## {re.escape(section_name)}\s*\n\n(.+?)(?=\n## |\Z)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""


# ============== CLI ==============
def main():
    parser = argparse.ArgumentParser(
        description="Anime Character Loader v2.0 - Multi-source character data with validation"
    )
    parser.add_argument("name", help="Character name (EN/JP/CN)")
    parser.add_argument("--anime", "-a", help="Anime/manga name hint for disambiguation")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    parser.add_argument("--info", "-i", action="store_true", help="Show info only, don't generate")
    parser.add_argument("--force", "-f", action="store_true", help="Force generation even with low confidence")
    parser.add_argument("--select", "-s", type=int, help="Select specific match by index (when multiple found)")
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print("🎭 Anime Character Loader v2.0")
    print(f"{'='*60}")
    
    loader = CharacterLoader()
    
    # 1. 翻译名称
    translated_name, anime_hint = loader.translate_name(args.name)
    if translated_name != args.name:
        print(f"\n📝 Name translation: '{args.name}' → '{translated_name}'")
    
    # 使用命令行提示或翻译得到的作品名
    hint = args.anime or anime_hint
    if hint:
        print(f"🎬 Anime hint: {hint}")
    
    # 2. 多源查询
    matches = loader.query_multi_source(translated_name, hint)
    
    if not matches:
        print("\n❌ No matches found")
        print("\n💡 Suggestions:")
        print("- Try English or Japanese name")
        print("- Check spelling")
        print("- Use --anime to specify source work")
        sys.exit(1)
    
    # 3. 消歧（强制模式：必须有 --anime 提示或 --select）
    if args.select and 1 <= args.select <= len(matches):
        selected = matches[args.select - 1]
        print(f"\n✅ User selected: {selected.name}")
    else:
        selected = loader.disambiguate(matches, hint, force_hint=FORCE_DISAMBIGUATION, original_query=args.name)
    
    if not selected:
        print("\n⚠️ Cannot auto-select. Please use --select <number> to choose:")
        for i, match in enumerate(matches[:5], 1):
            print(f"  {i}. {match.name} ({match.source_work})")
        sys.exit(1)
    
    # 4. 置信度检查
    if selected.confidence < CONFIDENCE_THRESHOLD_LOW and not args.force:
        print(f"\n⚠️ Low confidence ({selected.confidence:.2f}). Use --force to generate anyway.")
        sys.exit(1)
    
    # 显示信息模式
    if args.info:
        print(f"\n{'='*60}")
        print("CHARACTER INFO")
        print(f"{'='*60}")
        print(f"Name: {selected.name}")
        print(f"Source: {selected.source_work}")
        print(f"Confidence: {selected.confidence:.2f}")
        print(f"Data source: {selected.source}")
        print(f"\nDescription preview:")
        desc = loader._clean_description(selected.data.get("description", ""))
        print(desc[:500] + "..." if len(desc) > 500 else desc)
        return
    
    # 5. 生成 SOUL.md
    print(f"\n📝 Generating SOUL.md...")
    content = loader.generate_soul(selected)
    
    # 6. 验证
    print("\n🔍 Validating...")
    validation = loader.validate_soul(content, selected.data)
    
    print(f"\n{'='*60}")
    print("VALIDATION REPORT")
    print(f"{'='*60}")
    print(f"Overall Score: {validation.score:.1f}/100")
    print(f"Status: {'✅ PASSED' if validation.passed else '❌ FAILED'}")
    print()
    
    for check_name, (passed, description) in validation.checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check_name}: {description}")
    
    if validation.errors:
        print(f"\n⚠️ Errors:")
        for error in validation.errors:
            print(f"  - {error}")
    
    # 7. 写入临时文件
    temp_path = FileManager.write_temp(content, selected.name)
    print(f"\n📄 Temp file: {temp_path}")
    
    # 8. 验证通过后提交
    if validation.passed or args.force:
        final_path = FileManager.generate_final_path(selected.name, args.output)
        final_path = FileManager.commit(temp_path, final_path)
        print(f"✅ Final file: {final_path}")
        
        # 显示预览
        print(f"\n{'='*60}")
        print("PREVIEW")
        print(f"{'='*60}")
        preview = content[:1000] + "..." if len(content) > 1000 else content
        print(preview)
        
        # 9. 询问加载方式
        print(f"\n{'='*60}")
        print("📋 LOADING OPTIONS")
        print(f"{'='*60}")
        print(f"\nCharacter: {selected.name}")
        print(f"File: {final_path}")
        
        # 检查是否已有 SOUL.md
        existing_soul = os.path.join(args.output, "SOUL.md")
        has_existing = os.path.exists(existing_soul)
        
        if has_existing:
            print(f"\n⚠️  Existing SOUL.md found: {existing_soul}")
        
        print(f"\nHow would you like to load this character?")
        print(f"\n  [1] REPLACE - Replace existing SOUL.md with this character")
        if has_existing:
            print(f"      (Will backup existing SOUL.md first)")
        else:
            print(f"      cp {final_path} ./SOUL.md")
        
        print(f"\n  [2] MERGE - Structured merge into existing SOUL.md")
        if has_existing:
            print(f"      (Preserves existing content, adds character sections)")
        else:
            print(f"      (No existing SOUL.md, will create new)")
        
        print(f"\n  [3] KEEP - Keep as SOUL.generated.md for manual review")
        print(f"      (No changes to existing files)")
        
        # 在非交互式环境中默认选择 KEEP
        try:
            choice = input(f"\nEnter choice [1/2/3] (default: 3): ").strip() or "3"
        except (EOFError, KeyboardInterrupt):
            choice = "3"
            print("\n(non-interactive mode, defaulting to KEEP)")
        
        if choice == "1":
            # REPLACE
            target_path = os.path.join(args.output, "SOUL.md")
            if os.path.exists(target_path):
                backup_path = f"{target_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                os.rename(target_path, backup_path)
                print(f"\n  📦 Backed up existing SOUL.md to: {backup_path}")
            
            import shutil
            shutil.copy2(final_path, target_path)
            print(f"  ✅ Replaced: {target_path}")
            
        elif choice == "2":
            # MERGE
            target_path = os.path.join(args.output, "SOUL.md")
            if os.path.exists(target_path):
                FileManager.structured_merge(final_path, target_path, selected.name)
            else:
                # 没有现有文件，直接复制
                import shutil
                shutil.copy2(final_path, target_path)
                print(f"  ✅ Created: {target_path}")
            
        else:
            # KEEP (default)
            print(f"\n  📄 Kept as: {final_path}")
            print(f"  💡 To load manually:")
            print(f"     cp {final_path} ./SOUL.md")
        
    else:
        FileManager.rollback(temp_path)
        print("\n❌ Generation failed validation. Use --force to override.")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print("✅ Complete!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
