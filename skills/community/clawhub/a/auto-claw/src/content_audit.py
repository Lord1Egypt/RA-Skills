"""
Content Quality Auditor — WordPress 内容质量审计
分析文章可读性、结构、深度，生成改进建议
E-A-T 评估（Expertise, Experience, Authority, Trust）
"""
import re
import json
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
from collections import Counter

@dataclass
class ContentIssue:
    severity: str  # ERROR / WARNING / SUGGESTION
    category: str  # readability / structure / depth / etype
    message: str
    location: str = ""  # e.g. "paragraph 2"
    suggestion: str = ""

@dataclass
class ContentAuditResult:
    url: str
    title: str = ""
    word_count: int = 0
    reading_time_minutes: float = 0.0
    
    # 可读性
    flesch_kincaid_grade: float = 0.0  # 年级水平
    flesch_reading_ease: float = 0.0    # 易读性分数
    avg_sentence_length: float = 0.0
    avg_word_length: float = 0.0
    complex_word_ratio: float = 0.0
    
    # 结构
    has_h1: bool = False
    has_h2: bool = False
    h2_count: int = 0
    h3_count: int = 0
    paragraph_count: int = 0
    image_count: int = 0
    internal_link_count: int = 0
    external_link_count: int = 0
    
    # E-A-T
    has_author: bool = False
    author_name: str = ""
    has_published_date: bool = False
    published_date: str = ""
    has_modified_date: bool = False
    has_schema: bool = False
    external_citations: int = 0
    
    # 深度评分
    depth_score: int = 0  # 0-100
    quality_score: int = 0  # 0-100
    readability_score: int = 0  # 0-100
    
    issues: List[ContentIssue] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

class ContentAuditor:
    """
    WordPress 内容质量审计器
    
    评估维度：
    1. 可读性 (Readability) — Flesch-Kincaid 指数
    2. 内容结构 (Structure) — H标签、段落、图片
    3. 内容深度 (Depth) — 字数、引用、外部链接
    4. E-A-T 信号 — 作者、日期、Schema
    5. 转化因素 — CTA、内部链接
    """
    
    def __init__(self, site_name: str = "", site_url: str = ""):
        self.site_name = site_name
        self.site_url = site_url
    
    def syllable_count(self, word: str) -> int:
        """估算音节数"""
        word = word.lower().strip()
        if len(word) <= 3:
            return 1
        
        # 哑元音
        vowels = "aeiouy"
        count = 0
        prev_is_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_is_vowel:
                count += 1
            prev_is_vowel = is_vowel
        
        # 结尾哑元
        if word.endswith("e"):
            count = max(1, count - 1)
        if word.endswith("le") and len(word) > 2 and word[-3] not in vowels:
            count += 1
        
        return max(1, count)
    
    def flesch_kincaid(self, text: str) -> Tuple[float, float]:
        """
        计算 Flesch-Kincaid 指数
        返回 (年级水平, 易读性分数)
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        sentence_count = max(1, len(sentences))
        
        words = re.findall(r'[a-zA-Z0-9_\-\']+', text.lower())
        word_count = max(1, len(words))
        
        syllable_count_total = sum(self.syllable_count(w) for w in words)
        
        # Flesch Reading Ease = 206.835 - 1.015(total words/total sentences) - 84.6(total syllables/total words)
        reading_ease = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (syllable_count_total / word_count)
        reading_ease = max(0, min(100, reading_ease))
        
        # Flesch-Kincaid Grade = 0.39(total words/total sentences) + 11.8(total syllables/total words) - 15.59
        grade = 0.39 * (word_count / sentence_count) + 11.8 * (syllable_count_total / word_count) - 15.59
        grade = max(0, grade)
        
        return grade, reading_ease
    
    def extract_plain_text(self, html: str) -> str:
        """从 HTML 中提取纯文本"""
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<nav[^>]*>.*?</nav>', '', text, flags=re.DOTALL)
        text = re.sub(r'<footer[^>]*>.*?</footer>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def analyze_structure(self, html: str) -> Dict[str, Any]:
        """分析页面结构"""
        h1s = re.findall(r'<h1[^>]*>([^<]+)</h1>', html, re.IGNORECASE)
        h2s = re.findall(r'<h2[^>]*>([^<]+)</h2>', html, re.IGNORECASE)
        h3s = re.findall(r'<h3[^>]*>([^<]+)</h3>', html, re.IGNORECASE)
        paragraphs = re.findall(r'<p[^>]*>([^<]+)</p>', html, re.IGNORECASE)
        images = re.findall(r'<img[^>]+>', html, re.IGNORECASE)
        internal_links = re.findall(r'<a[^>]+href=["\'][^"\']*', html, re.IGNORECASE)
        external_links = []
        
        # 过滤内部链接
        for link in internal_links[:]:
            href_match = re.search(r'href=["\']([^"\']+)["\']', link)
            if href_match:
                href = href_match.group(1)
                if href.startswith("http") and self.site_url not in href:
                    external_links.append(href)
                elif href.startswith("/"):
                    pass  # 内部
                elif href.startswith("#"):
                    pass  # 锚点
        
        return {
            "h1s": [h.strip() for h in h1s],
            "h2s": [h.strip() for h in h2s],
            "h3s": [h.strip() for h in h3s],
            "paragraphs": [p.strip() for p in paragraphs if len(p.strip()) > 20],
            "image_count": len(images),
            "internal_link_count": len(internal_links) - len(external_links),
            "external_link_count": len(external_links),
        }
    
    def audit_page(self, url: str, html: str, title: str = "") -> ContentAuditResult:
        """审计单个页面的内容质量"""
        result = ContentAuditResult(url=url, title=title)
        
        # 提取纯文本
        plain_text = self.extract_plain_text(html)
        result.word_count = len(plain_text.split())
        result.reading_time_minutes = result.word_count / 200  # 假设阅读速度200字/分钟
        
        # 可读性
        grade, ease = self.flesch_kincaid(plain_text)
        result.flesch_kincaid_grade = round(grade, 1)
        result.flesch_reading_ease = round(ease, 1)
        
        words = plain_text.split()
        if words:
            result.avg_word_length = round(sum(len(w) for w in words) / len(words), 2)
            complex_words = [w for w in words if self.syllable_count(w) >= 3]
            result.complex_word_ratio = round(len(complex_words) / len(words), 3)
        
        sentences = re.split(r'[.!?]+', plain_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        if sentences:
            result.avg_sentence_length = round(sum(len(s.split()) for s in sentences) / len(sentences), 1)
        
        # 结构分析
        structure = self.analyze_structure(html)
        result.h1_count = len(structure["h1s"])
        result.has_h1 = result.h1_count > 0
        result.h2_count = len(structure["h2s"])
        result.has_h2 = result.h2_count > 0
        result.h3_count = len(structure["h3s"])
        result.paragraph_count = len(structure["paragraphs"])
        result.image_count = structure["image_count"]
        result.internal_link_count = max(0, structure["internal_link_count"])
        result.external_link_count = structure["external_link_count"]
        
        # E-A-T 信号
        # 作者
        author_match = re.search(r'<span[^>]+class=["\'][^"\']*author[^"\']*["\'][^>]*>([^<]+)</span>', html, re.IGNORECASE)
        if not author_match:
            author_match = re.search(r'rel=["\']author["\'][^>]*href=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if author_match:
            result.has_author = True
            result.author_name = author_match.group(1).strip()
        
        # 日期
        date_match = re.search(r'<time[^>]+datetime=["\']([^"\']+)["\']', html, re.IGNORECASE)
        if date_match:
            result.has_published_date = True
            result.published_date = date_match.group(1)[:10]
        
        # Schema
        result.has_schema = bool(re.search(r'application/ld\+json', html, re.IGNORECASE))
        
        # 引用/外部来源
        result.external_citations = result.external_link_count
        
        # ===== 问题检测 =====
        issues = []
        
        # 可读性
        if result.flesch_kincaid_grade > 10:
            issues.append(ContentIssue(
                "ERROR", "readability",
                f"内容难度过高（年级水平 {result.flesch_kincaid_grade}，建议 ≤ 10）",
                suggestion=f"简化句子，平均句子长度控制在 {result.avg_sentence_length:.0f} 字以内"
            ))
        elif result.flesch_kincaid_grade > 8:
            issues.append(ContentIssue(
                "WARNING", "readability",
                f"内容偏难（年级水平 {result.flesch_kincaid_grade}）",
                suggestion="考虑简化一些复杂句子"
            ))
        
        if result.flesch_reading_ease < 30:
            issues.append(ContentIssue(
                "WARNING", "readability",
                f"易读性分数偏低（{result.flesch_reading_ease:.0f}/100）",
                suggestion="使用更多短句和日常词汇"
            ))
        
        # 字数
        if result.word_count < 300:
            issues.append(ContentIssue(
                "ERROR", "depth",
                f"内容过少（{result.word_count} 字，建议 ≥ 300）",
                suggestion="扩充内容深度，至少达到 300 字"
            ))
        elif result.word_count < 600:
            issues.append(ContentIssue(
                "WARNING", "depth",
                f"内容偏短（{result.word_count} 字，建议 ≥ 600）",
                suggestion="建议扩展到 600 字以上以提升 SEO"
            ))
        
        # 结构
        if not result.has_h1:
            issues.append(ContentIssue(
                "ERROR", "structure",
                "缺少 H1 标签",
                suggestion="确保页面有且仅有一个 H1"
            ))
        
        if result.h2_count == 0 and result.word_count > 300:
            issues.append(ContentIssue(
                "WARNING", "structure",
                "缺少 H2 副标题",
                suggestion="使用 H2 分隔内容段落，提升可扫描性"
            ))
        
        if result.image_count > 0:
            # 检查图片 alt
            imgs_without_alt = len(re.findall(r'<img(?![^>]*alt=)[^>]*>', html, re.IGNORECASE))
            if imgs_without_alt > 0:
                issues.append(ContentIssue(
                    "WARNING", "structure",
                    f"{imgs_without_alt} 个图片缺少 alt 属性",
                    suggestion="为所有图片添加描述性 alt 文本"
                ))
        
        # E-A-T
        if not result.has_author:
            issues.append(ContentIssue(
                "ERROR", "e-a-t",
                "缺少作者信息",
                suggestion="添加作者名称或作者链接"
            ))
        
        if not result.has_published_date:
            issues.append(ContentIssue(
                "WARNING", "e-a-t",
                "缺少发布日期",
                suggestion="添加 <time> 标签标注发布日期"
            ))
        
        if not result.has_schema:
            issues.append(ContentIssue(
                "SUGGESTION", "e-a-t",
                "缺少结构化数据（Article Schema）",
                suggestion="添加 Article Schema 以增强搜索展示"
            ))
        
        if result.external_citations == 0 and result.word_count > 500:
            issues.append(ContentIssue(
                "SUGGESTION", "depth",
                "内容缺少外部引用/来源",
                suggestion="添加数据来源和研究引用，增强可信度"
            ))
        
        result.issues = issues
        
        # ===== 评分 =====
        # 可读性评分
        if result.flesch_reading_ease >= 60:
            result.readability_score = 100
        elif result.flesch_reading_ease >= 40:
            result.readability_score = 80
        else:
            result.readability_score = 50
        
        # 深度评分
        depth_score = min(100, int(result.word_count / 3))  # 每300字=100分
        structure_bonus = 0
        if result.h2_count >= 3:
            structure_bonus += 15
        if result.image_count >= 2:
            structure_bonus += 10
        if result.external_citations >= 2:
            structure_bonus += 10
        result.depth_score = min(100, depth_score + structure_bonus)
        
        # 总质量评分
        quality = (
            result.readability_score * 0.3 +
            result.depth_score * 0.4 +
            (100 if result.has_author else 0) * 0.1 +
            (100 if result.has_schema else 0) * 0.1 +
            (100 if result.has_published_date else 0) * 0.1
        )
        result.quality_score = int(quality)
        
        # ===== 建议 =====
        recs = []
        if result.quality_score < 60:
            recs.append("🔴 内容质量偏低，需要大幅改进")
        elif result.quality_score < 80:
            recs.append("🟡 内容质量中等，有改进空间")
        else:
            recs.append("🟢 内容质量良好")
        
        if result.word_count < 600:
            recs.append(f"📝 建议扩充到 600 字以上（当前 {result.word_count} 字）")
        
        if result.flesch_kincaid_grade > 8:
            recs.append(f"📖 简化语言（当前年级水平 {result.flesch_kincaid_grade}，建议 ≤ 8）")
        
        if not result.has_schema:
            recs.append("📋 添加 Article Schema 结构化数据")
        
        result.recommendations = recs
        
        return result

def audit_all_posts(urls_data: List[Dict], html_content: Dict[str, str]) -> List[ContentAuditResult]:
    """审计所有文章"""
    auditor = ContentAuditor()
    results = []
    
    for page_info in urls_data:
        url = page_info["url"]
        title = page_info.get("title", "")
        html = html_content.get(url, "")
        
        result = auditor.audit_page(url, html, title)
        results.append(result)
    
    return results
