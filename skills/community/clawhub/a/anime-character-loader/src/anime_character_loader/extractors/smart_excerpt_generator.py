"""
Smart Excerpt Generator - 智能角色描述摘录生成器

⚠️ 重要提示：此模块提取的是"角色描述摘录"，不是"原始台词/quote"。
   输出内容来自 Wiki 的角色简介、性格特点、经历描述等章节，
   用于辅助理解角色背景，不能替代真实的角色台词。

用途：
- 当 Wiki 没有专门的 Quotes/台词区块时的兜底方案
- 为 SOUL 生成提供角色背景素材
- 补充 wikiquote.py 的不足

数据来源：角色介绍、性格描述、经历等章节的文本摘录
"""

import json
import re
import hashlib
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from pathlib import Path

import requests
from bs4 import BeautifulSoup


@dataclass
class ExcerptItem:
    """摘录项 - 来自Wiki角色描述，不是原始台词"""
    text: str
    source: str  # 来源Wiki和章节
    context: str  # 上下文/章节名
    excerpt_type: str  # 类型：excerpt(摘录)/note(备注)
    confidence: float
    excerpt_id: str
    is_original_quote: bool = False  # 明确标记：这不是原始台词


class SmartExcerptGenerator:
    """
    智能角色描述摘录生成器
    
    ⚠️ 本类提取的是Wiki上的角色描述，不是原始台词。
    
    策略：
    1. 抓取角色页面（Biography/Personality/经历）
    2. 提取关键描述段落
    3. 输出带明确标注的角色背景素材
    
    用途：作为wikiquote的兜底/补充，当Wiki没有Quotes区块时使用
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_from_fandom(self, character: str, work: str) -> List[ExcerptItem]:
        """
        从 Fandom Wiki 提取
        
        提取：Biography, Personality, Background 等章节
        """
        domain = self._get_fandom_domain(work)
        api_url = f"https://{domain}/api.php?action=parse&page={character.replace(' ', '_')}&prop=text|sections&format=json"
        
        try:
            resp = self.session.get(api_url, timeout=30)
            data = resp.json()
            
            if 'error' in data:
                return []
            
            html = data['parse']['text']['*']
            sections = data['parse'].get('sections', [])
            soup = BeautifulSoup(html, 'html.parser')
            
            excerpts = []
            
            # 提取关键章节
            target_sections = ['Biography', 'Personality', 'Background', 'Character', 'Overview']
            
            for section in sections:
                section_name = section.get('line', '')
                if any(target.lower() in section_name.lower() for target in target_sections):
                    section_excerpts = self._extract_from_section(
                        soup, section, section_name, character
                    )
                    excerpts.extend(section_excerpts)
            
            return excerpts
            
        except Exception as e:
            print(f"Fandom 提取失败: {e}")
            return []
    
    def fetch_from_moegirl(self, character: str) -> List[ExcerptItem]:
        """
        从萌娘百科提取

        提取：性格特点、角色经历、简介
        """
        # 处理重定向（斯潘塞/斯宾塞）
        variants = [character, character.replace('斯潘塞', '斯宾塞')]

        for variant in variants:
            # 第一步：获取 HTML 内容
            api_url = f"https://zh.moegirl.org.cn/api.php?action=parse&page={variant}&prop=text&format=json"

            try:
                resp = self.session.get(api_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
                data = resp.json()

                if 'error' in data or 'parse' not in data:
                    print(f"API 错误或无效数据: {variant}")
                    continue

                # 检查是否是重定向页面
                html = data['parse']['text']['*']
                if 'redirectMsg' in html:
                    soup = BeautifulSoup(html, 'html.parser')
                    redirect_link = soup.find('a', class_='redirectText')
                    if redirect_link:
                        target = redirect_link.get_text(strip=True)
                        print(f"重定向到: {target}")
                        continue

                # 从 HTML 中解析章节
                soup = BeautifulSoup(html, 'html.parser')
                excerpts = []
                target_sections = ['性格特点', '角色经历', '简介', '角色形象', '人物设定']

                # 遍历所有 h2/h3 章节
                for h in soup.find_all(['h2', 'h3']):
                    section_name = h.get_text(strip=True).replace('[编辑]', '').strip()
                    if any(target in section_name for target in target_sections):
                        section_excerpts = self._extract_from_section_elem(
                            soup, h, section_name, character
                        )
                        excerpts.extend(section_excerpts)

                return excerpts

            except Exception as e:
                print(f"萌娘百科提取失败: {e}")
                import traceback
                traceback.print_exc()
                continue

        return []
    
    def _extract_from_section_elem(self, soup: BeautifulSoup, section_elem,
                                   section_name: str, character: str) -> List[ExcerptItem]:
        """从章节元素提取内容"""
        excerpts = []

        if not section_elem:
            return excerpts

        # 收集段落文本
        paragraphs = []
        current = section_elem
        while current:
            current = current.find_next(['p', 'h2', 'h3'])
            if not current:
                break
            if current.name in ['h2', 'h3']:
                # 检查是否是新章节
                current_text = current.get_text(strip=True)
                if section_name not in current_text:
                    break
            if current.name == 'p':
                text = current.get_text(strip=True)
                if len(text) > 20 and len(text) < 500:
                    paragraphs.append(text)

        # 将描述转换为摘录
        for para in paragraphs[:3]:  # 限制数量
            clean_text = self._clean_text(para)
            if not clean_text:
                continue

            excerpt_id = hashlib.md5(clean_text.encode()).hexdigest()[:8]
            source_type = "萌娘百科" if any(c in character for c in ['泽', '斯', '英', '麻', '衣', '惠', '诗']) else "Fandom"

            excerpts.append(ExcerptItem(
                text=clean_text,
                source=f"{source_type}/{section_name}",
                context=section_name,
                excerpt_type="excerpt",
                confidence=0.7,
                excerpt_id=excerpt_id,
                is_original_quote=False
            ))

        return excerpts

    def _extract_from_section(self, soup: BeautifulSoup, section: Dict,
                              section_name: str, character: str) -> List[ExcerptItem]:
        """从单个章节提取内容"""
        excerpts = []

        # 找到章节锚点
        anchor = section.get('anchor', '')

        # 方法1: 通过 id 查找
        section_elem = soup.find(id=anchor)

        # 方法2: 通过章节名在 h2/h3 中查找
        if not section_elem:
            for h in soup.find_all(['h2', 'h3', 'span']):
                h_text = h.get_text(strip=True)
                if section_name in h_text or anchor in h.get('id', ''):
                    section_elem = h
                    break

        if not section_elem:
            return excerpts

        # 收集段落文本
        paragraphs = []
        current = section_elem
        while current:
            current = current.find_next(['p', 'h2', 'h3'])
            if not current:
                break
            if current.name in ['h2', 'h3']:
                current_text = current.get_text(strip=True)
                if section_name not in current_text and anchor not in current.get('id', ''):
                    break
            if current.name == 'p':
                text = current.get_text(strip=True)
                if len(text) > 20 and len(text) < 500:
                    paragraphs.append(text)

        # 将描述转换为摘录
        for para in paragraphs[:3]:  # 限制数量
            clean_text = self._clean_text(para)
            if not clean_text:
                continue

            # 明确标记：这是摘录，不是原始台词
            excerpt_id = hashlib.md5(clean_text.encode()).hexdigest()[:8]
            source_type = "萌娘百科" if any(c in character for c in ['泽', '斯', '英', '麻', '衣', '惠', '诗']) else "Fandom"
            
            excerpts.append(ExcerptItem(
                text=clean_text,
                source=f"{source_type}/{section_name}",
                context=section_name,
                excerpt_type="excerpt",
                confidence=0.7,
                excerpt_id=excerpt_id,
                is_original_quote=False  # ⚠️ 明确标记
            ))

        return excerpts

    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 移除引用标记 [1][2]
        text = re.sub(r'\[\d+\]', '', text)
        # 移除编辑链接
        text = re.sub(r'\[编辑[^\]]*\]', '', text)
        # 规范化空白
        text = ' '.join(text.split())
        return text.strip()

    def _get_fandom_domain(self, work: str) -> str:
        """获取 Fandom 域名"""
        work_lower = work.lower()
        if 'saekano' in work_lower or '路人' in work_lower:
            return 'saekano.fandom.com'
        if 'aobuta' in work_lower or '猪头' in work_lower or '兔女郎' in work_lower:
            return 'aobuta.fandom.com'
        return f"{work_lower.replace(' ', '-').replace(':', '')}.fandom.com"

    def fetch_all_sources(self, character: str, work: str) -> Dict[str, Any]:
        """
        从所有可用源获取
        
        Returns:
            {
                'character': str,
                'work': str,
                'excerpts': List[ExcerptItem],
                'sources': List[str],
                'note': str  # ⚠️ 明确提示
            }
        """
        all_excerpts = []
        sources = []

        # 1. Fandom
        fandom_excerpts = self.fetch_from_fandom(character, work)
        if fandom_excerpts:
            all_excerpts.extend(fandom_excerpts)
            sources.append('fandom')

        # 2. 萌娘百科
        moegirl_excerpts = self.fetch_from_moegirl(character)
        if moegirl_excerpts:
            all_excerpts.extend(moegirl_excerpts)
            sources.append('moegirl')

        # 去重
        seen = set()
        unique_excerpts = []
        for e in all_excerpts:
            if e.excerpt_id not in seen:
                seen.add(e.excerpt_id)
                unique_excerpts.append(e)

        return {
            'character': character,
            'work': work,
            'excerpts': [
                {
                    'text': e.text,
                    'source': e.source,
                    'context': e.context,
                    'type': e.excerpt_type,
                    'confidence': e.confidence,
                    'excerpt_id': e.excerpt_id,
                    'is_original_quote': e.is_original_quote,
                    'note': '⚠️ 来自Wiki角色描述，不是原始台词'  # 明确提示
                }
                for e in unique_excerpts
            ],
            'sources': sources,
            'total': len(unique_excerpts),
            'note': '⚠️ 本数据为Wiki角色描述摘录，用于辅助理解角色背景，不是原始台词。如需真实台词，请使用wikiquote模块或本地数据库。'
        }


def generate_smart_excerpts(character: str, work: str) -> Dict[str, Any]:
    """
    便捷函数：智能生成角色描述摘录
    
    ⚠️ 注意：输出的是Wiki角色描述，不是原始台词！
    
    示例：
        >>> result = generate_smart_excerpts('泽村·斯潘塞·英梨梨', '路人女主')
        >>> print(result['excerpts'][0]['text'])
        >>> print(result['note'])  # 查看使用提示
    """
    generator = SmartExcerptGenerator()
    return generator.fetch_all_sources(character, work)


if __name__ == "__main__":
    # 测试
    result = generate_smart_excerpts('泽村·斯潘塞·英梨梨', '路人女主')
    print(f"\n{'='*60}")
    print(f"⚠️ {result['note']}")
    print(f"{'='*60}")
    print(f"\n角色: {result['character']}")
    print(f"来源: {', '.join(result['sources']) if result['sources'] else '无'}")
    print(f"摘录数: {result['total']}")
    
    if result['excerpts']:
        print("\n角色描述摘录示例:\n")
        for i, e in enumerate(result['excerpts'][:5], 1):
            print(f"【{i}】[{e['type']}] {e['context']}")
            print(f"    {e['text'][:80]}...")
            print(f"    来源: {e['source']} | 置信度: {e['confidence']}")
            print(f"    ⚠️ {e['note']}")
            print()
