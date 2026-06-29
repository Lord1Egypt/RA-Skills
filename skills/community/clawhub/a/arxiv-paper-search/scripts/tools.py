from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def search_arxiv(
    query: str,
    maxResults: Optional[float] = 5.0
) -> Dict[str, Any]:
    """
    搜索 arXiv 论文
    
    Args:
        query: 搜索英文关键词
        maxResults: 最大结果数量
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "maxResults": maxResults
    }
    
    return call_api("1777316659949571", "search_arxiv", arguments)

def get_recent_ai_papers(
) -> Dict[str, Any]:
    """
    获取 arXiv AI 领域最新论文（cs.AI/recent）
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659949571", "get_recent_ai_papers", arguments)

def get_arxiv_pdf_url(
    input: str
) -> Dict[str, Any]:
    """
    获取 arXiv PDF 下载链接
    
    Args:
        input: arXiv 论文URL（如：http://arxiv.org/abs/2403.15137v1）或 arXiv ID（如：2403.15137v1）
    
    Returns:
        
    """
    arguments = {
        "input": input
    }
    
    return call_api("1777316659949571", "get_arxiv_pdf_url", arguments)

def parse_paper_content(
    input: str,
    paperInfo: Optional[null] = None
) -> Dict[str, Any]:
    """
    解析论文内容（优先使用 HTML 版本，回退到 PDF）
    
    Args:
        input: arXiv 论文URL或 arXiv ID
        paperInfo: 论文信息（可选，用于添加论文元数据）
    
    Returns:
        
    """
    arguments = {
        "input": input,
        "paperInfo": paperInfo
    }
    
    return call_api("1777316659949571", "parse_paper_content", arguments)

