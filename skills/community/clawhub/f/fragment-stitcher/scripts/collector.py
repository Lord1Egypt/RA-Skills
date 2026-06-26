"""
智能收集器 - 碎片信息的智能提取和结构化

这个脚本处理来自各种来源的碎片信息（文本、截图、文件），
提取核心内容并结构化存储。
"""

import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib


class FragmentCollector:
    """碎片信息收集器"""

    def __init__(self, knowledge_base_path: str = None):
        """
        初始化收集器

        Args:
            knowledge_base_path: 知识库存储路径
        """
        if knowledge_base_path:
            self.knowledge_base = Path(knowledge_base_path)
            self.knowledge_base.mkdir(parents=True, exist_ok=True)
        else:
            self.knowledge_base = None

        self.fragments = []
        self._load_existing_fragments()

    def collect_from_text(self, text: str, source: str = "手动输入",
                        tags: List[str] = None) -> Dict:
        """
        从文本收集碎片

        Args:
            text: 文本内容
            source: 来源标识（如：微信、网页、会议）
            tags: 主题标签列表

        Returns:
            结构化的碎片信息
        """
        # 提取核心信息
        core_insights = self._extract_core_insights(text)

        # 生成碎片 ID
        fragment_id = self._generate_fragment_id(text)

        # 构建碎片对象
        fragment = {
            'id': fragment_id,
            'content': text,
            'source': source,
            'tags': tags or [],
            'core_insights': core_insights,
            'created_at': datetime.now().isoformat(),
            'related_fragments': [],  # 后续填充
            'stitch_notes': []  # 后续填充
        }

        self.fragments.append(fragment)
        return fragment

    def collect_from_file(self, file_path: str) -> Dict:
        """
        从文件收集碎片

        Args:
            file_path: 文件路径

        Returns:
            结构化的碎片信息
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        # 读取文件内容
        content = self._read_file(path)

        # 确定来源类型
        source = self._identify_source_type(path)

        # 提取碎片
        fragment = self.collect_from_text(
            text=content,
            source=f"文件:{path.name}",
            tags=[path.stem]  # 使用文件名作为标签
        )

        fragment['file_path'] = str(file_path)
        return fragment

    def collect_from_url(self, url: str, content: str = None) -> Dict:
        """
        从 URL 收集碎片

        Args:
            url: 网页 URL
            content: 网页内容（可选，如果不提供则假设已抓取）

        Returns:
            结构化的碎片信息
        """
        if content is None:
            raise ValueError("需要提供网页内容，请先使用网页抓取工具")

        # 提取网页标题
        title = self._extract_web_title(content)

        fragment = self.collect_from_text(
            text=content,
            source=f"网页:{url}",
            tags=[self._extract_domain(url)]
        )

        fragment['url'] = url
        fragment['title'] = title
        return fragment

    def _extract_core_insights(self, text: str) -> Dict:
        """
        提取核心观点和关键信息

        Args:
            text: 文本内容

        Returns:
            核心信息字典
        """
        insights = {
            'main_points': [],  # 主要观点
            'key_concepts': [],  # 关键概念
            'sentences': [],  # 重要句子
            'summary': ''  # 摘要
        }

        # 分段
        sentences = re.split(r'[。！？；]', text)

        # 提取重要句子（较长且包含关键词）
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # 过滤太短的句子
                insights['sentences'].append(sentence)

        # 提取关键概念（识别专有名词和术语）
        insights['key_concepts'] = self._extract_key_concepts(text)

        # 生成摘要（取前几句）
        insights['summary'] = ' '.join(sentences[:3]) if sentences else text[:200]

        # 提取主要观点（含"认为""建议""表示"等词的句子）
        for sentence in sentences:
            if any(keyword in sentence for keyword in ['认为', '建议', '表示', '发现', '指出', '说明']):
                insights['main_points'].append(sentence.strip())

        return insights

    def _extract_key_concepts(self, text: str) -> List[str]:
        """
        提取关键概念

        简单实现：识别可能的技术术语和专有名词
        """
        # 常见的技术前缀和后缀
        tech_patterns = [
            r'\b[A-Z][a-z]+(?:模型|系统|算法|架构|框架|技术)\b',
            r'\b(?:深度学习|人工智能|机器学习|云计算|微服务)\b',
            r'\b[A-Z]{2,}\b',  # 全大写的缩写
        ]

        concepts = set()
        for pattern in tech_patterns:
            matches = re.findall(pattern, text)
            concepts.update(matches)

        # 提取中英文混合的术语
        mixed_pattern = r'[\u4e00-\u9fa5]+(?:算法|模型|系统|技术)'
        matches = re.findall(mixed_pattern, text)
        concepts.update(matches)

        return list(concepts)[:10]  # 限制返回数量

    def _extract_web_title(self, content: str) -> str:
        """从 HTML 内容中提取标题"""
        # 简单实现：提取 title 标签
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if title_match:
            return title_match.group(1).strip()
        return "未命名网页"

    def _extract_domain(self, url: str) -> str:
        """从 URL 提取域名"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return "未知来源"

    def _identify_source_type(self, path: Path) -> str:
        """识别文件来源类型"""
        ext_map = {
            '.md': 'Markdown',
            '.txt': '文本文件',
            '.pdf': 'PDF',
            '.docx': 'Word 文档',
            '.html': 'HTML',
            '.json': 'JSON'
        }
        return ext_map.get(path.suffix.lower(), f"文件:{path.suffix}")

    def _read_file(self, path: Path) -> str:
        """读取文件内容"""
        try:
            if path.suffix == '.pdf':
                # TODO: 实现 PDF 解析
                return f"[PDF 文件: {path.name}]"
            elif path.suffix in ['.docx', '.doc']:
                # TODO: 实现 Word 文档解析
                return f"[Word 文档: {path.name}]"
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            return f"读取文件失败: {str(e)}"

    def _generate_fragment_id(self, content: str) -> str:
        """生成碎片 ID"""
        # 使用内容哈希 + 时间戳
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime('%H%M%S')
        return f"frag_{content_hash}_{timestamp}"

    def _load_existing_fragments(self):
        """加载已有碎片"""
        if self.knowledge_base:
            fragments_file = self.knowledge_base / 'fragments.json'
            if fragments_file.exists():
                with open(fragments_file, 'r', encoding='utf-8') as f:
                    self.fragments = json.load(f)

    def save_fragments(self):
        """保存碎片到知识库"""
        if self.knowledge_base:
            fragments_file = self.knowledge_base / 'fragments.json'
            with open(fragments_file, 'w', encoding='utf-8') as f:
                json.dump(self.fragments, f, indent=2, ensure_ascii=False)

    def search_fragments(self, query: str, limit: int = 10) -> List[Dict]:
        """
        搜索碎片

        Args:
            query: 搜索关键词
            limit: 返回结果数量

        Returns:
            匹配的碎片列表
        """
        results = []
        query_lower = query.lower()

        for fragment in self.fragments:
            score = 0

            # 搜索内容
            if query_lower in fragment['content'].lower():
                score += 10

            # 搜索核心概念
            for concept in fragment['core_insights']['key_concepts']:
                if query_lower in concept.lower():
                    score += 5

            # 搜索标签
            for tag in fragment['tags']:
                if query_lower in tag.lower():
                    score += 3

            # 搜索主要观点
            for point in fragment['core_insights']['main_points']:
                if query_lower in point.lower():
                    score += 7

            if score > 0:
                results.append({
                    'fragment': fragment,
                    'score': score
                })

        # 按分数排序
        results.sort(key=lambda x: x['score'], reverse=True)

        return [r['fragment'] for r in results[:limit]]

    def get_fragment_by_id(self, fragment_id: str) -> Optional[Dict]:
        """根据 ID 获取碎片"""
        for fragment in self.fragments:
            if fragment['id'] == fragment_id:
                return fragment
        return None


def collect_fragments(items: List[Dict], knowledge_base: str = None) -> List[Dict]:
    """
    批量收集碎片

    Args:
        items: 碎片项列表，每项包含 type 和对应数据
        knowledge_base: 知识库存储路径

    Returns:
        收集到的碎片列表
    """
    collector = FragmentCollector(knowledge_base)

    collected = []
    for item in items:
        if item['type'] == 'text':
            fragment = collector.collect_from_text(
                text=item['content'],
                source=item.get('source', '手动输入'),
                tags=item.get('tags')
            )
        elif item['type'] == 'file':
            fragment = collector.collect_from_file(item['path'])
        elif item['type'] == 'url':
            fragment = collector.collect_from_url(
                url=item['url'],
                content=item['content']
            )
        else:
            continue

        collected.append(fragment)

    # 保存到知识库
    if knowledge_base:
        collector.save_fragments()

    return collected


if __name__ == '__main__':
    import sys

    # 示例：从文本收集
    collector = FragmentCollector('test_knowledge_base')

    sample_text = """
    人工智能的发展正在加速，尤其是在大语言模型领域。我认为未来几年，
    多模态模型将成为主流，能够同时处理文本、图像和音频。
    深度学习算法的优化将进一步提升模型性能。
    """

    fragment = collector.collect_from_text(
        text=sample_text,
        source="示例文本",
        tags=["人工智能", "大模型"]
    )

    print("收集到的碎片:")
    print(json.dumps(fragment, indent=2, ensure_ascii=False))

    # 保存碎片
    collector.save_fragments()
    print(f"\n碎片已保存到知识库: {collector.knowledge_base}")
