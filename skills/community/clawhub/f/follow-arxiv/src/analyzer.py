"""论文深度分析模块"""

from typing import Dict, Any, List, Optional
import json


class PaperAnalyzer:
    """论文分析器"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def prepare_analysis_context(
        self,
        paper_data: Dict[str, Any],
        analysis_type: str = "deep"
    ) -> Dict[str, Any]:
        """
        准备分析上下文，返回给 Agent

        Args:
            paper_data: 论文数据（包含元数据和内容）
            analysis_type: 分析类型 ("deep" 或 "quick")

        Returns:
            分析上下文字典
        """
        metadata = {
            'title': paper_data.get('title', ''),
            'authors': paper_data.get('authors', []),
            'arxiv_id': paper_data.get('arxiv_id', ''),
            'published': paper_data.get('published', ''),
            'categories': paper_data.get('categories', []),
            'summary': paper_data.get('summary', '')
        }

        content = paper_data.get('content', {})
        full_text = content.get('full_text', '')
        equations = content.get('equations', [])

        # 构建分析上下文
        context = {
            'metadata': metadata,
            'full_text': full_text,
            'equations': equations,
            'analysis_type': analysis_type,
            'content_length': len(full_text),
            'equation_count': len(equations)
        }

        # 加载提示词模板并填充数据
        from utils import load_prompt
        prompt_template = load_prompt('deep_analysis')

        # 填充提示词模板
        filled_prompt = self._fill_prompt_template(prompt_template, context)

        # 返回完整信息给 Agent
        return {
            'context': context,
            'prompt': filled_prompt,
            'instruction': '请使用上述提示词和数据生成论文深度分析报告'
        }

    def prepare_summary_context(
        self,
        papers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        准备日报摘要上下文

        Args:
            papers: 论文列表

        Returns:
            摘要上下文字典
        """
        papers_metadata = []

        for paper in papers:
            metadata = {
                'title': paper.get('title', ''),
                'authors': paper.get('authors', []),
                'arxiv_id': paper.get('arxiv_id', ''),
                'published': paper.get('published', ''),
                'categories': paper.get('categories', []),
                'summary': paper.get('summary', ''),
                'pdf_url': paper.get('pdf_url', '')
            }
            papers_metadata.append(metadata)

        context = {
            'papers': papers_metadata,
            'total_papers': len(papers_metadata),
            'time_window': self.config.get('time_window_hours', 24)
        }

        # 加载提示词模板并填充数据
        from utils import load_prompt
        prompt_template = load_prompt('daily_summary')

        # 填充提示词模板
        filled_prompt = self._fill_prompt_template(prompt_template, context)

        # 返回完整信息给 Agent
        return {
            'context': context,
            'prompt': filled_prompt,
            'instruction': '请使用上述提示词和数据生成论文日报'
        }

    def _fill_prompt_template(self, template: str, context: Dict[str, Any]) -> str:
        """
        填充提示词模板

        Args:
            template: 提示词模板
            context: 上下文数据

        Returns:
            填充后的提示词
        """
        filled = template

        # 简单的模板变量替换
        for key, value in context.items():
            placeholder = '{{' + key + '}}'
            if isinstance(value, (list, dict)):
                # 格式化为 JSON 字符串
                filled = filled.replace(placeholder, json.dumps(value, ensure_ascii=False, indent=2))
            elif isinstance(value, (int, float, str)):
                filled = filled.replace(placeholder, str(value))

        return filled


def prepare_analysis(
    paper_data: Dict[str, Any],
    analysis_type: str = "deep",
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    准备分析的便捷函数

    Args:
        paper_data: 论文数据
        analysis_type: 分析类型
        config: 配置字典

    Returns:
        包含 context、prompt、instruction 的字典
    """
    if config is None:
        from utils import load_config
        config = load_config()

    analyzer = PaperAnalyzer(config)
    return analyzer.prepare_analysis_context(paper_data, analysis_type)


def prepare_summary(
    papers: List[Dict[str, Any]],
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    准备日报摘要的便捷函数

    Args:
        papers: 论文列表
        config: 配置字典

    Returns:
        包含 context、prompt、instruction 的字典
    """
    if config is None:
        from utils import load_config
        config = load_config()

    analyzer = PaperAnalyzer(config)
    return analyzer.prepare_summary_context(papers)
