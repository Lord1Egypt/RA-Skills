"""
每日论文速递主程序
整合 arXiv 和 HuggingFace 的论文信息
"""
import json
import os
import logging
from typing import List, Dict
from datetime import datetime
from arxiv_fetcher import ArxivFetcher
from huggingface_fetcher import HuggingFaceFetcher

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PaperDigest:
    """论文速递主类"""
    
    def __init__(self, config_path: str = "config/sources.json"):
        """
        初始化论文速递
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.arxiv_fetcher = None
        self.hf_fetcher = None
        self._init_fetchers()
    
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            # 获取脚本所在目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            full_path = os.path.join(script_dir, config_path)
            
            with open(full_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"成功加载配置文件: {config_path}")
            return config
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}")
            # 返回默认配置
            return {
                "sources": [],
                "output_format": {
                    "include_abstract": True,
                    "include_authors": True,
                    "include_links": True,
                    "language": "zh-CN"
                }
            }
    
    def _init_fetchers(self):
        """初始化各个信息源的获取器"""
        for source in self.config.get('sources', []):
            if not source.get('enabled', False):
                continue
                
            if source['name'] == 'arxiv':
                categories = source.get('categories', ['cs.AI'])
                max_results = source.get('max_results', 10)
                self.arxiv_fetcher = ArxivFetcher(categories, max_results)
                logger.info("已初始化 arXiv 获取器")
                
            elif source['name'] == 'huggingface':
                max_results = source.get('max_results', 10)
                self.hf_fetcher = HuggingFaceFetcher(max_results)
                logger.info("已初始化 HuggingFace 获取器")
    
    def fetch_all_papers(self) -> List[Dict]:
        """
        从所有启用的信息源获取论文
        
        Returns:
            所有论文的列表
        """
        all_papers = []
        
        # 获取 arXiv 论文
        if self.arxiv_fetcher:
            try:
                arxiv_papers = self.arxiv_fetcher.fetch_daily_papers()
                all_papers.extend(arxiv_papers)
                logger.info(f"从 arXiv 获取了 {len(arxiv_papers)} 篇论文")
            except Exception as e:
                logger.error(f"获取 arXiv 论文失败: {str(e)}")
        
        # 获取 HuggingFace 论文
        if self.hf_fetcher:
            try:
                hf_papers = self.hf_fetcher.fetch_daily_papers()
                all_papers.extend(hf_papers)
                logger.info(f"从 HuggingFace 获取了 {len(hf_papers)} 篇论文")
            except Exception as e:
                logger.error(f"获取 HuggingFace 论文失败: {str(e)}")
        
        return all_papers
    
    def filter_papers(self, papers: List[Dict]) -> List[Dict]:
        """
        根据配置过滤论文
        
        Args:
            papers: 论文列表
            
        Returns:
            过滤后的论文列表
        """
        filter_config = self.config.get('filter', {})
        keywords = filter_config.get('keywords', [])
        exclude_keywords = filter_config.get('exclude_keywords', [])
        
        if not keywords and not exclude_keywords:
            return papers
        
        filtered_papers = []
        
        for paper in papers:
            title = paper.get('title', '').lower()
            abstract = paper.get('abstract', '').lower()
            text = f"{title} {abstract}"
            
            # 检查排除关键词
            if exclude_keywords:
                if any(keyword.lower() in text for keyword in exclude_keywords):
                    continue
            
            # 检查包含关键词
            if keywords:
                if any(keyword.lower() in text for keyword in keywords):
                    filtered_papers.append(paper)
            else:
                filtered_papers.append(paper)
        
        logger.info(f"过滤后剩余 {len(filtered_papers)} 篇论文")
        return filtered_papers
    
    def format_paper(self, paper: Dict, index: int) -> str:
        """
        格式化单篇论文信息
        
        Args:
            paper: 论文信息
            index: 序号
            
        Returns:
            格式化后的文本
        """
        output_format = self.config.get('output_format', {})
        
        # 构建输出
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"📄 论文 {index}")
        lines.append(f"{'='*60}")
        lines.append(f"\n📌 标题: {paper.get('title', '未知')}")
        
        # 作者信息
        if output_format.get('include_authors', True):
            authors = paper.get('authors', [])
            if authors:
                author_str = ', '.join(authors[:5])  # 最多显示5个作者
                if len(authors) > 5:
                    author_str += f" 等 {len(authors)} 人"
                lines.append(f"👥 作者: {author_str}")
        
        # 来源和发布日期
        source = paper.get('source', '未知').upper()
        published = paper.get('published', '未知')
        lines.append(f"🏷️  来源: {source} | 日期: {published}")
        
        # 摘要
        if output_format.get('include_abstract', True):
            abstract = paper.get('abstract', '')
            if abstract:
                # 限制摘要长度
                if len(abstract) > 300:
                    abstract = abstract[:300] + '...'
                lines.append(f"\n📝 摘要:\n{abstract}")
        
        # 链接
        if output_format.get('include_links', True):
            if paper.get('source') == 'arxiv':
                lines.append(f"\n🔗 arXiv: {paper.get('arxiv_url', '')}")
                lines.append(f"📥 PDF: {paper.get('pdf_url', '')}")
            elif paper.get('source') == 'huggingface':
                lines.append(f"\n🔗 链接: {paper.get('url', '')}")
                likes = paper.get('likes', '0')
                lines.append(f"👍 点赞: {likes}")
        
        return '\n'.join(lines)
    
    def format_digest(self, papers: List[Dict]) -> str:
        """
        格式化论文速递报告
        
        Args:
            papers: 论文列表
            
        Returns:
            完整的报告文本
        """
        if not papers:
            return "📭 今日暂无新论文"
        
        # 标题
        title = f"""
╔══════════════════════════════════════════════════════════╗
║           🎓 AI 论文每日速递 - {datetime.now().strftime('%Y年%m月%d日')}           ║
╚══════════════════════════════════════════════════════════╝

📊 今日共收录 {len(papers)} 篇论文

"""
        
        # 格式化每篇论文
        formatted_papers = [self.format_paper(paper, i+1) for i, paper in enumerate(papers)]
        
        # 统计信息
        arxiv_count = sum(1 for p in papers if p.get('source') == 'arxiv')
        hf_count = sum(1 for p in papers if p.get('source') == 'huggingface')
        
        footer = f"""
\n{'='*60}
📈 信息源统计:
   • arXiv: {arxiv_count} 篇
   • HuggingFace: {hf_count} 篇

⏰ 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}
"""
        
        return title + '\n'.join(formatted_papers) + footer
    
    def run(self) -> str:
        """
        执行论文速递
        
        Returns:
            格式化后的报告文本
        """
        logger.info("开始执行每日论文速递...")
        
        # 获取所有论文
        papers = self.fetch_all_papers()
        
        # 过滤论文
        filtered_papers = self.filter_papers(papers)
        
        # 格式化输出
        digest = self.format_digest(filtered_papers)
        
        logger.info("论文速递执行完成")
        return digest


def main():
    """主函数，用于 OpenClaw skill 调用"""
    digest = PaperDigest()
    result = digest.run()
    print(result)
    return result


if __name__ == "__main__":
    main()
