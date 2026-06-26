#!/usr/bin/env python3
"""
OpenClaw Academic Literature Search Skill
专注于提供最强大的文献检索功能
"""

import os
import sys
import json
import asyncio
import aiohttp
import yaml
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
import hashlib
import re
import logging
from pathlib import Path
from enum import Enum
from urllib.parse import quote

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 常量定义
CACHE_DIR = Path("~/.cache/openclaw/literature").expanduser()
CACHE_DIR.mkdir(parents=True, exist_ok=True)

class Database(Enum):
    """支持的数据库"""
    SEMANTIC_SCHOLAR = "semantic_scholar"
    CROSSREF = "crossref"
    PUBMED = "pubmed"
    ARXIV = "arxiv"

@dataclass
class Paper:
    """论文数据类"""
    title: str
    authors: List[str] = field(default_factory=list)
    abstract: Optional[str] = None
    year: Optional[int] = None
    venue: Optional[str] = None
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    pmid: Optional[str] = None
    citation_count: int = 0
    url: Optional[str] = None
    open_access_pdf: Optional[str] = None
    is_open_access: bool = False
    source_database: Database = Database.SEMANTIC_SCHOLAR
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        data = asdict(self)
        # 将 Database 枚举转换为字符串
        data['source_database'] = self.source_database.value
        return data

class LiteratureSearchEngine:
    """文献检索引擎核心"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.session = None
        self.cache = {}
        
        # API配置
        self.api_config = {
            "semantic_scholar": {
                "base_url": "https://api.semanticscholar.org/graph/v1",
                "api_key": os.getenv("SEMANTIC_SCHOLAR_API_KEY", ""),
            },
            "crossref": {
                "base_url": "https://api.crossref.org/works",
                "email": os.getenv("CROSSREF_API_EMAIL", "openclaw@example.com"),
            },
            "pubmed": {
                "base_url": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils",
                "api_key": os.getenv("PUBMED_API_KEY", ""),
            },
            "arxiv": {
                "base_url": "http://export.arxiv.org/api/query",
            }
        }
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    async def search(self, query: str, databases: List[str], 
                    max_results: int = 50, year_range: Tuple[int, int] = None,
                    **kwargs) -> List[Paper]:
        """执行文献检索"""
        
        # 创建检索任务
        tasks = []
        db_objects = [Database(db) for db in databases if db in [d.value for d in Database]]
        
        for db in db_objects:
            if db == Database.SEMANTIC_SCHOLAR:
                task = self._search_semantic_scholar(query, max_results, year_range)
            elif db == Database.CROSSREF:
                task = self._search_crossref(query, max_results, year_range)
            elif db == Database.PUBMED:
                task = self._search_pubmed(query, max_results, year_range)
            elif db == Database.ARXIV:
                task = self._search_arxiv(query, max_results, year_range)
            else:
                continue
            
            tasks.append(task)
        
        # 并行执行所有检索
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 合并结果
        all_papers = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"数据库 {databases[i]} 检索失败: {result}")
                continue
            if result:
                all_papers.extend(result)
        
        # 去重和排序
        deduplicated = self._deduplicate_papers(all_papers)
        sorted_papers = self._sort_papers(deduplicated, kwargs.get("sort_by", "relevance"))
        
        return sorted_papers[:max_results]
    
    async def _search_semantic_scholar(self, query: str, max_results: int, 
                                      year_range: Tuple[int, int] = None) -> List[Paper]:
        """Semantic Scholar检索"""
        params = {
            "query": query,
            "limit": min(max_results * 2, 100),
            "fields": "paperId,title,abstract,authors,year,venue,citationCount,url,openAccessPdf,isOpenAccess,externalIds"
        }
        
        if year_range:
            params["year"] = f"{year_range[0]}-{year_range[1]}"
        
        try:
            async with self.session.get(
                f"{self.api_config['semantic_scholar']['base_url']}/paper/search",
                params=params,
                headers={"x-api-key": self.api_config['semantic_scholar']['api_key']} 
                if self.api_config['semantic_scholar']['api_key'] else {}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_semantic_scholar_results(data.get("data", []))
        except Exception as e:
            logger.error(f"Semantic Scholar检索失败: {e}")
        
        return []
    
    async def _search_crossref(self, query: str, max_results: int,
                              year_range: Tuple[int, int] = None) -> List[Paper]:
        """Crossref检索"""
        params = {
            "query": query,
            "rows": min(max_results * 2, 100),
            "select": "DOI,title,author,issued,abstract,URL,container-title"
        }
        
        if year_range:
            params["filter"] = f"from-pub-date:{year_range[0]},until-pub-date:{year_range[1]}"
        
        headers = {
            "User-Agent": f"OpenClawLiteratureSearch/2.0.0 (mailto:{self.api_config['crossref']['email']})"
        }
        
        try:
            async with self.session.get(
                self.api_config['crossref']['base_url'],
                params=params,
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_crossref_results(data.get("message", {}).get("items", []))
        except Exception as e:
            logger.error(f"Crossref检索失败: {e}")
        
        return []
    
    async def _search_pubmed(self, query: str, max_results: int,
                           year_range: Tuple[int, int] = None) -> List[Paper]:
        """PubMed检索"""
        # 构建PubMed查询
        pubmed_query = query
        if year_range:
            pubmed_query += f" AND ({year_range[0]}[Date - Publication] : {year_range[1]}[Date - Publication])"
        
        # 第一步：获取 ID 列表
        params = {
            "db": "pubmed",
            "term": pubmed_query,
            "retmax": min(max_results, 100),
            "retmode": "json",
        }
        
        try:
            async with self.session.get(
                f"{self.api_config['pubmed']['base_url']}/esearch.fcgi",
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    id_list = data.get("esearchresult", {}).get("idlist", [])
                    
                    if not id_list:
                        return []
                    
                    # 第二步：获取详细信息
                    id_str = ",".join(id_list[:max_results])
                    fetch_params = {
                        "db": "pubmed",
                        "id": id_str,
                        "retmode": "xml",
                        "rettype": "abstract"
                    }
                    
                    async with self.session.get(
                        f"{self.api_config['pubmed']['base_url']}/efetch.fcgi",
                        params=fetch_params
                    ) as fetch_response:
                        if fetch_response.status == 200:
                            xml_data = await fetch_response.text()
                            return self._process_pubmed_results(xml_data)
        except Exception as e:
            logger.error(f"PubMed检索失败: {e}")
        
        return []
    
    def _process_pubmed_results(self, xml_data: str) -> List[Paper]:
        """解析 PubMed XML 结果"""
        papers = []
        try:
            root = ET.fromstring(xml_data)
            
            for article in root.findall('.//PubmedArticle'):
                # 提取标题
                title_elem = article.find('.//ArticleTitle')
                title = title_elem.text if title_elem is not None else ""
                
                # 提取作者
                authors = []
                for author in article.findall('.//Author'):
                    last_name = author.find('LastName')
                    fore_name = author.find('ForeName')
                    if last_name is not None:
                        name = f"{fore_name.text} {last_name.text}" if fore_name is not None else last_name.text
                        authors.append(name.strip())
                
                # 提取年份
                year = None
                pub_date = article.find('.//PubDate')
                if pub_date is not None:
                    year_elem = pub_date.find('Year')
                    if year_elem is not None and year_elem.text:
                        year = int(year_elem.text)
                
                # 提取期刊
                journal = article.find('.//Journal/Title')
                venue = journal.text if journal is not None else ""
                
                # 提取摘要
                abstract = ""
                for abs_elem in article.findall('.//AbstractText'):
                    if abs_elem.text:
                        abstract += abs_elem.text + " "
                
                pmid_elem = article.find('.//PMID')
                pmid = pmid_elem.text if pmid_elem is not None else ""
                
                papers.append(Paper(
                    title=title,
                    authors=authors,
                    abstract=abstract.strip() if abstract else None,
                    year=year,
                    venue=venue,
                    pmid=pmid,
                    source_database=Database.PUBMED
                ))
        except Exception as e:
            logger.error(f"解析 PubMed 结果失败: {e}")
        
        return papers
    
    async def _search_arxiv(self, query: str, max_results: int,
                           year_range: Tuple[int, int] = None) -> List[Paper]:
        """arXiv检索"""
        params = {
            "search_query": f"all:{query}",
            "max_results": min(max_results, 100),
            "sortBy": "relevance",
            "sortOrder": "descending"
        }
        
        try:
            async with self.session.get(
                self.api_config['arxiv']['base_url'],
                params=params
            ) as response:
                if response.status == 200:
                    xml_data = await response.text()
                    return self._process_arxiv_results(xml_data)
        except Exception as e:
            logger.error(f"arXiv检索失败: {e}")
        
        return []
    
    def _process_arxiv_results(self, xml_data: str) -> List[Paper]:
        """解析 arXiv XML 结果"""
        papers = []
        try:
            root = ET.fromstring(xml_data)
            
            # arXiv 使用命名空间
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            for entry in root.findall('atom:entry', ns):
                # 提取标题
                title = entry.find('atom:title', ns)
                title_text = title.text.strip() if title is not None and title.text else ""
                
                # 提取摘要
                summary = entry.find('atom:summary', ns)
                abstract = summary.text.strip() if summary is not None and summary.text else ""
                
                # 提取作者
                authors = []
                for author in entry.findall('atom:author', ns):
                    name = author.find('atom:name', ns)
                    if name is not None and name.text:
                        authors.append(name.text)
                
                # 提取日期
                year = None
                updated = entry.find('atom:updated', ns)
                if updated is not None and updated.text:
                    year = int(updated.text[:4])
                
                # 提取 arXiv ID
                arxiv_id = None
                id_elem = entry.find('atom:id', ns)
                if id_elem is not None and id_elem.text:
                    # 从 URL 提取 ID: http://arxiv.org/abs/2306.04338v1 -> 2306.04338
                    arxiv_id = id_elem.text.split('/')[-1]
                    if 'v' in arxiv_id:
                        arxiv_id = arxiv_id.split('v')[0]
                
                # 提取 PDF 链接
                pdf_link = None
                for link in entry.findall('atom:link', ns):
                    if link.get('title') == 'pdf':
                        pdf_link = link.get('href')
                        break
                
                papers.append(Paper(
                    title=title_text,
                    authors=authors,
                    abstract=abstract,
                    year=year,
                    arxiv_id=arxiv_id,
                    url=f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else None,
                    open_access_pdf=pdf_link,
                    is_open_access=True,
                    source_database=Database.ARXIV
                ))
        except Exception as e:
            logger.error(f"解析 arXiv 结果失败: {e}")
        
        return papers
    
    def _process_semantic_scholar_results(self, results: List[Dict]) -> List[Paper]:
        """处理Semantic Scholar结果"""
        papers = []
        for item in results:
            paper = Paper(
                title=item.get("title", ""),
                authors=[author.get("name", "") for author in item.get("authors", [])],
                abstract=item.get("abstract"),
                year=item.get("year"),
                venue=item.get("venue", ""),
                doi=item.get("externalIds", {}).get("DOI"),
                citation_count=item.get("citationCount", 0),
                url=item.get("url"),
                open_access_pdf=item.get("openAccessPdf", {}).get("url"),
                is_open_access=item.get("isOpenAccess", False),
                source_database=Database.SEMANTIC_SCHOLAR
            )
            papers.append(paper)
        return papers
    
    def _process_crossref_results(self, results: List[Dict]) -> List[Paper]:
        """处理Crossref结果"""
        papers = []
        for item in results:
            # 提取作者
            authors = []
            if "author" in item:
                for author in item["author"]:
                    name = f"{author.get('given', '')} {author.get('family', '')}".strip()
                    if name:
                        authors.append(name)
            
            # 提取年份
            year = None
            if "issued" in item and "date-parts" in item["issued"]:
                date_parts = item["issued"]["date-parts"]
                if date_parts and date_parts[0]:
                    year = date_parts[0][0]
            
            paper = Paper(
                title=item.get("title", [""])[0] if item.get("title") else "",
                authors=authors,
                abstract=item.get("abstract"),
                year=year,
                venue=", ".join(item.get("container-title", [])),
                doi=item.get("DOI"),
                url=item.get("URL"),
                source_database=Database.CROSSREF
            )
            papers.append(paper)
        return papers
    
    def _deduplicate_papers(self, papers: List[Paper]) -> List[Paper]:
        """论文去重"""
        seen_dois = set()
        seen_titles = set()
        deduplicated = []
        
        for paper in papers:
            # 基于DOI去重
            if paper.doi and paper.doi in seen_dois:
                continue
            
            # 基于标题去重
            title_lower = paper.title.lower()
            if title_lower in seen_titles:
                continue
            
            if paper.doi:
                seen_dois.add(paper.doi)
            seen_titles.add(title_lower)
            deduplicated.append(paper)
        
        return deduplicated
    
    def _sort_papers(self, papers: List[Paper], sort_by: str) -> List[Paper]:
        """论文排序"""
        if sort_by == "citations":
            return sorted(papers, key=lambda x: x.citation_count, reverse=True)
        elif sort_by == "year":
            return sorted(papers, key=lambda x: x.year or 0, reverse=True)
        elif sort_by == "relevance":
            # 简单按引用数排序作为相关性代理
            return sorted(papers, key=lambda x: x.citation_count, reverse=True)
        else:
            return papers

class OutputFormatter:
    """输出格式化器"""
    
    @staticmethod
    def format_markdown(papers: List[Paper], query: str = "") -> str:
        """Markdown格式输出"""
        output = [f"# 文献检索结果\n"]
        
        if query:
            output.append(f"**检索词**: {query}")
        output.append(f"**检索时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"**结果数量**: {len(papers)}篇\n")
        
        output.append("## 检索结果\n")
        
        for i, paper in enumerate(papers, 1):
            output.append(f"### {i}. {paper.title}")
            
            # 作者信息
            if paper.authors:
                authors_str = ", ".join(paper.authors[:5])
                if len(paper.authors) > 5:
                    authors_str += f" 等{len(paper.authors)}人"
                output.append(f"- **作者**: {authors_str}")
            
            # 出版信息
            pub_info = []
            if paper.year:
                pub_info.append(f"{paper.year}年")
            if paper.venue:
                pub_info.append(paper.venue)
            if pub_info:
                output.append(f"- **出版信息**: {' | '.join(pub_info)}")
            
            # 引用信息
            if paper.citation_count > 0:
                output.append(f"- **引用数**: {paper.citation_count}")
            
            # 标识符
            identifiers = []
            if paper.doi:
                identifiers.append(f"DOI: {paper.doi}")
            if paper.pmid:
                identifiers.append(f"PMID: {paper.pmid}")
            if paper.arxiv_id:
                identifiers.append(f"arXiv: {paper.arxiv_id}")
            if identifiers:
                output.append(f"- **标识符**: {' | '.join(identifiers)}")
            
            # 摘要
            if paper.abstract:
                abstract_preview = paper.abstract[:200] + "..." if len(paper.abstract) > 200 else paper.abstract
                output.append(f"- **摘要**: {abstract_preview}")
            
            # 链接
            links = []
            if paper.url:
                links.append(f"[原文链接]({paper.url})")
            if paper.open_access_pdf:
                links.append(f"[PDF下载]({paper.open_access_pdf})")
            if paper.is_open_access:
                links.append("🔓 开放获取")
            if links:
                output.append(f"- **访问**: {' | '.join(links)}")
            
            output.append("")  # 空行分隔
        
        return "\n".join(output)
    
    @staticmethod
    def format_json(papers: List[Paper]) -> str:
        """JSON格式输出"""
        papers_data = [paper.to_dict() for paper in papers]
        return json.dumps({
            "timestamp": datetime.now().isoformat(),
            "count": len(papers),
            "papers": papers_data
        }, ensure_ascii=False, indent=2)
    
    @staticmethod
    def format_csv(papers: List[Paper]) -> str:
        """CSV格式输出"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # 写入表头
        writer.writerow([
            "标题", "作者", "年份", "期刊/会议", "DOI", "PMID", "arXiv ID",
            "引用数", "是否开放获取", "原文链接", "PDF链接", "检索来源"
        ])
        
        # 写入数据
        for paper in papers:
            writer.writerow([
                paper.title,
                "; ".join(paper.authors),
                paper.year or "",
                paper.venue or "",
                paper.doi or "",
                paper.pmid or "",
                paper.arxiv_id or "",
                paper.citation_count,
                "是" if paper.is_open_access else "否",
                paper.url or "",
                paper.open_access_pdf or "",
                paper.source_database.value
            ])
        
        return output.getvalue()
    
    @staticmethod
    def format_bibtex(papers: List[Paper]) -> str:
        """BibTeX格式输出"""
        bibtex_entries = []
        
        for i, paper in enumerate(papers, 1):
            # 生成BibTeX键
            if paper.doi:
                key = paper.doi.replace("/", "_").replace(".", "_")
            elif paper.arxiv_id:
                key = f"arxiv_{paper.arxiv_id}"
            elif paper.authors and paper.year:
                first_author = paper.authors[0].split()[-1] if paper.authors[0] else "unknown"
                key = f"{first_author.lower()}_{paper.year}"
            else:
                key = f"paper_{i:04d}"
            
            # 确定文献类型
            entry_type = "article"
            if paper.arxiv_id:
                entry_type = "misc"
            elif paper.venue and any(conf in paper.venue.lower() for conf in ["conference", "proceedings", "workshop"]):
                entry_type = "inproceedings"
            
            # 构建BibTeX条目
            entry = [f"@{entry_type}{{{key},"]
            
            # 添加字段
            fields = []
            if paper.title:
                fields.append(f"  title = {{{paper.title}}},")
            if paper.authors:
                authors_bibtex = " and ".join([f"{author}" for author in paper.authors])
                fields.append(f"  author = {{{authors_bibtex}}},")
            if paper.year:
                fields.append(f"  year = {{{paper.year}}},")
            if paper.venue:
                if entry_type == "article":
                    fields.append(f"  journal = {{{paper.venue}}},")
                else:
                    fields.append(f"  booktitle = {{{paper.venue}}},")
            if paper.doi:
                fields.append(f"  doi = {{{paper.doi}}},")
            if paper.arxiv_id:
                fields.append(f"  eprint = {{{paper.arxiv_id}}},")
                fields.append(f"  archivePrefix = {{arXiv}},")
            if paper.url:
                fields.append(f"  url = {{{paper.url}}},")
            if paper.abstract:
                fields.append(f"  abstract = {{{paper.abstract[:500]}}},")
            
            entry.extend(fields)
            entry.append("}")
            bibtex_entries.append("\n".join(entry))
        
        return "\n\n".join(bibtex_entries)

class AcademicLiteratureSearchSkill:
    """OpenClaw学术文献检索技能"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.engine = None
    
    def _load_config(self, config_path: str = None) -> Dict:
        """加载配置"""
        default_config = {
            "search": {
                "default_max_results": 50,
                "default_databases": ["semantic_scholar", "crossref"],
                "timeout": 30
            },
            "cache": {
                "enabled": True,
                "ttl": 3600
            },
            "output": {
                "default_format": "markdown"
            }
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                # 合并配置
                self._merge_configs(default_config, user_config)
            except Exception as e:
                logger.error(f"加载配置文件失败: {e}")
        
        return default_config
    
    def _merge_configs(self, base: Dict, update: Dict):
        """递归合并配置"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_configs(base[key], value)
            else:
                base[key] = value
    
    async def execute(self, params: Dict) -> Dict:
        """执行技能"""
        try:
            # 解析参数
            query = params.get("query", "")
            if not query:
                return {
                    "success": False,
                    "error": "查询参数不能为空",
                    "message": "请提供检索查询"
                }
            
            # 获取数据库列表
            databases = params.get("databases", 
                                 self.config["search"].get("default_databases", 
                                                         ["semantic_scholar", "crossref"]))
            
            # 解析年份范围
            year_range = None
            if "year_range" in params and params["year_range"]:
                try:
                    if isinstance(params["year_range"], str) and "-" in params["year_range"]:
                        start, end = params["year_range"].split("-")
                        year_range = (int(start.strip()), int(end.strip()))
                except:
                    pass
            
            # 最大结果数
            max_results = params.get("max_results", 
                                   self.config["search"].get("default_max_results", 50))
            
            # 其他参数
            sort_by = params.get("sort_by", "relevance")
            sort_order = params.get("sort_order", "desc")
            open_access_only = params.get("open_access_only", False)
            min_citations = params.get("min_citations")
            venue_filter = params.get("venue_filter")
            
            # 执行检索
            async with LiteratureSearchEngine(self.config) as engine:
                self.engine = engine
                
                papers = await engine.search(
                    query=query,
                    databases=databases,
                    max_results=max_results,
                    year_range=year_range,
                    sort_by=sort_by,
                    sort_order=sort_order
                )
                
                # 应用过滤
                if open_access_only:
                    papers = [p for p in papers if p.is_open_access]
                
                if min_citations is not None:
                    papers = [p for p in papers if p.citation_count >= min_citations]
                
                if venue_filter:
                    papers = [p for p in papers if p.venue and 
                            any(venue in p.venue for venue in venue_filter)]
                
                # 生成统计信息
                stats = self._generate_statistics(papers)
                
                # 格式化输出
                output_format = params.get("output_format", 
                                         self.config["output"].get("default_format", "markdown"))
                
                formatter = OutputFormatter()
                if output_format == "json":
                    formatted_results = formatter.format_json(papers)
                elif output_format == "csv":
                    formatted_results = formatter.format_csv(papers)
                elif output_format == "bibtex":
                    formatted_results = formatter.format_bibtex(papers)
                else:  # markdown
                    formatted_results = formatter.format_markdown(papers, query)
                
                # 保存结果
                if params.get("save_results"):
                    output_file = params.get("output_file", 
                                           f"literature_search_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{output_format}")
                    self._save_results(formatted_results, output_file, output_format)
                
                return {
                    "success": True,
                    "statistics": stats,
                    "results": formatted_results,
                    "papers_count": len(papers),
                    "papers": [paper.to_dict() for paper in papers],
                    "message": f"成功检索到 {len(papers)} 篇文献"
                }
                
        except Exception as e:
            logger.error(f"执行检索失败: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "message": "文献检索失败，请检查参数或稍后重试"
            }
    
    def _generate_statistics(self, papers: List[Paper]) -> Dict:
        """生成统计信息"""
        if not papers:
            return {}
        
        # 年份分布
        years = [p.year for p in papers if p.year]
        year_dist = {}
        if years:
            year_dist = {
                "earliest": min(years),
                "latest": max(years),
                "average": sum(years) / len(years)
            }
        
        # 引用统计
        citations = [p.citation_count for p in papers]
        citation_stats = {
            "total": sum(citations),
            "average": sum(citations) / len(citations) if citations else 0,
            "max": max(citations) if citations else 0,
            "min": min(citations) if citations else 0
        }
        
        # 来源分布
        sources = {}
        for paper in papers:
            source = paper.source_database.value
            sources[source] = sources.get(source, 0) + 1
        
        # 开放获取统计
        open_access = sum(1 for p in papers if p.is_open_access)
        
        return {
            "total_papers": len(papers),
            "year_distribution": year_dist,
            "citation_statistics": citation_stats,
            "source_distribution": sources,
            "open_access_count": open_access,
            "open_access_percentage": (open_access / len(papers)) * 100 if papers else 0
        }
    
    def _save_results(self, content: str, filename: str, format: str):
        """保存结果到文件"""
        try:
            # 确保目录存在
            filepath = Path(filename)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"结果已保存到: {filepath.absolute()}")
        except Exception as e:
            logger.error(f"保存结果失败: {e}")

# OpenClaw技能入口
async def main():
    """主函数"""
    import sys
    
    # 读取参数
    if len(sys.argv) > 1:
        try:
            params = json.loads(sys.argv[1])
        except:
            params = {}
    else:
        # 从标准输入读取
        try:
            params = json.loads(sys.stdin.read())
        except:
            params = {}
    
    # 执行技能
    skill = AcademicLiteratureSearchSkill()
    result = await skill.execute(params)
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
