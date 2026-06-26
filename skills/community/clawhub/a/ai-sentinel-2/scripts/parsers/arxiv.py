"""
arXiv 论文解析器
获取AI/ML领域最新学术论文
"""
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urlencode


def fetch_arxiv_papers(config):
    """
    获取arXiv最新论文
    
    Args:
        config: 信息源配置，包含:
            - categories: 论文类别列表 (默认: cs.AI, cs.LG, cs.CL)
            - max_results: 返回数量 (默认: 20)
            - search_query: 自定义搜索词
    
    Returns:
        list: 论文列表，每项包含 title, authors, abstract, url, published
    """
    categories = config.get("categories", ["cs.AI", "cs.LG", "cs.CL"])
    max_results = config.get("max_results", 20)
    search_query = config.get("search_query", "")
    
    # 构建搜索查询
    # 基础查询：AI相关类别
    base_query = "+OR+".join([f"cat:{cat}" for cat in categories])
    
    # 添加自定义搜索词
    if search_query:
        full_query = f"({base_query})+AND+({search_query})"
    else:
        full_query = base_query
    
    # arXiv API URL
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": full_query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "start": 0,
        "max_results": min(max_results, 100)
    }
    
    url = f"{base_url}?{urlencode(params)}"
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        return _parse_arxiv_response(response.text)
        
    except requests.exceptions.RequestException as e:
        print(f"arXiv API请求失败: {e}")
        return []


def _parse_arxiv_response(xml_content):
    """
    解析arXiv API返回的XML内容
    
    Args:
        xml_content: XML格式的API响应
    
    Returns:
        list: 解析后的论文列表
    """
    items = []
    
    try:
        root = ET.fromstring(xml_content)
        namespaces = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom"
        }
        
        for entry in root.findall("atom:entry", namespaces):
            # 提取基本信息
            title = entry.find("atom:title", namespaces)
            title = title.text.strip().replace("\n", " ") if title is not None else "无标题"
            
            summary = entry.find("atom:summary", namespaces)
            abstract = summary.text.strip().replace("\n", " ") if summary is not None else ""
            
            # 截取摘要前300字符
            abstract_short = abstract[:300] + "..." if len(abstract) > 300 else abstract
            
            authors = []
            for author in entry.findall("atom:author", namespaces):
                name = author.find("atom:name", namespaces)
                if name is not None:
                    authors.append(name.text)
            
            # 获取链接
            links = {}
            for link in entry.findall("atom:link", namespaces):
                href = link.get("href", "")
                link_type = link.get("type", "")
                if "pdf" in link_type:
                    links["pdf"] = href
                elif link.get("rel") == "alternate":
                    links["html"] = href
            
            # 获取发布日期
            published = entry.find("atom:published", namespaces)
            published = published.text if published is not None else ""
            
            # 获取类别
            categories = []
            for cat in entry.findall("atom:category", namespaces):
                term = cat.get("term", "")
                if term:
                    categories.append(term)
            
            items.append({
                "title": title,
                "authors": authors,
                "author_str": ", ".join(authors[:3]) + (" et al." if len(authors) > 3 else ""),
                "abstract": abstract_short,
                "abstract_full": abstract,
                "url": links.get("html", links.get("pdf", "")),
                "pdf_url": links.get("pdf", ""),
                "published": published,
                "categories": categories,
                "primary_category": categories[0] if categories else "Unknown",
                "source": "arxiv",
                "source_type": "paper"
            })
            
    except ET.ParseError as e:
        print(f"XML解析失败: {e}")
    
    return items


def search_arxiv(query, categories=None, max_results=10):
    """
    搜索arXiv论文
    
    Args:
        query: 搜索关键词
        categories: 论文类别列表
        max_results: 返回数量
    
    Returns:
        list: 论文列表
    """
    if categories:
        cat_query = "+OR+".join([f"cat:{cat}" for cat in categories])
        full_query = f"({query})+AND+({cat_query})"
    else:
        full_query = f"all:{query}"
    
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": full_query,
        "sortBy": "relevance",
        "sortOrder": "descending",
        "start": 0,
        "max_results": min(max_results, 100)
    }
    
    url = f"{base_url}?{urlencode(params)}"
    
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        return _parse_arxiv_response(response.text)
    except requests.exceptions.RequestException:
        return []


if __name__ == "__main__":
    # 测试代码
    config = {
        "categories": ["cs.AI", "cs.LG"],
        "max_results": 5
    }
    results = fetch_arxiv_papers(config)
    print(f"获取到 {len(results)} 篇论文:")
    for item in results:
        print(f"  - {item['title'][:50]}...")
