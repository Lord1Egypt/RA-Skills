#!/usr/bin/env python3
"""
Research Claw Bridge - 统一的研究工具
支持多数据源 + Survey报告生成
"""

import sys
import os

REARCH_CLAW_PATH = '/root/.openclaw/workspace/research-claw/research-claw-main'
sys.path.insert(0, REARCH_CLAW_PATH)

import json
import tempfile
from pathlib import Path
from urllib.request import urlretrieve


class ResearchTools:
    """统一的研究工具接口"""
    
    def __init__(self):
        self.tools = {}
    
    def _get_tool(self, name):
        if name not in self.tools:
            if name == 'arxiv':
                from agent.tools.arxiv_search import ArxivSearchTool
                self.tools[name] = ArxivSearchTool()
            elif name == 'pubmed':
                from agent.tools.pubmed_search import PubMedSearchTool
                self.tools[name] = PubMedSearchTool()
            elif name == 'openalex':
                from agent.tools.openalex_search import OpenAlexSearchTool
                self.tools[name] = OpenAlexSearchTool()
            elif name == 'semantic':
                from agent.tools.semantic_scholar import SemanticScholarTool
                self.tools[name] = SemanticScholarTool()
        return self.tools[name]
    
    def search(self, query, sources=None, max_results=10):
        """
        多数据源搜索
        sources: list of ['arxiv', 'pubmed', 'openalex', 'semantic']
        """
        if sources is None:
            sources = ['arxiv', 'pubmed']
        
        all_papers = []
        
        for source in sources:
            try:
                tool = self._get_tool(source)
                results = tool.execute(query=query, max_results=max_results)
                parsed = self._parse_results(results, source)
                all_papers.extend(parsed)
                print(f"  [{source}] 找到 {len(parsed)} 篇")
            except Exception as e:
                print(f"  [{source}] 搜索失败: {e}")
        
        # 去重
        return self._deduplicate(all_papers)
    
    def _parse_results(self, raw, source):
        """解析不同数据源的结果"""
        papers = []
        lines = [line.rstrip() for line in str(raw).split('\n') if line.strip()]
        
        current_paper = {}
        for i, line in enumerate(lines):
            if '[{}]'.format(len(papers)+1) in line and 'arXiv ID' not in line:
                # 这是标题行
                current_paper['title'] = line.lstrip('[] 0123456789.').strip()
            elif 'arXiv ID' in line and source == 'arxiv':
                arxiv_id = line.split(':')[-1].strip()
                current_paper['id'] = arxiv_id
                current_paper['source'] = 'arxiv'
                current_paper['url'] = f'https://arxiv.org/abs/{arxiv_id}'
                if 'title' in current_paper:
                    papers.append(current_paper.copy())
                    current_paper = {}
            elif 'PMID' in line and source == 'pubmed':
                # PubMed格式
                pmid = line.split(':')[-1].strip()
                current_paper['id'] = pmid
                current_paper['source'] = 'pubmed'
                if 'title' in current_paper:
                    papers.append(current_paper.copy())
                    current_paper = {}
        
        return papers
    
    def _find_title(self, lines, arxiv_line):
        """查找标题 - 保留兼容旧代码"""
        idx = lines.index(arxiv_line)
        # 向上找非空行
        for i in range(idx-1, max(0, idx-10), -1):
            title = lines[i].strip().lstrip('[] 0123456789.').strip()
            if title and len(title) > 5:
                return title
        return ''
    
    def _deduplicate(self, papers):
        """去重"""
        seen = set()
        unique = []
        for p in papers:
            pid = p.get('id', p.get('title', ''))
            if pid and pid not in seen:
                seen.add(pid)
                unique.append(p)
        return unique
    
    def generate_survey_report(self, papers, topic, output_path=None):
        """
        生成Survey报告
        调用LLM总结论文
        """
        from openai import OpenAI
        
        # 使用baiduqianfan
        client = OpenAI(
            api_key='bce-v3/ALTAKSP-MhjY1gIGq8XyzO87nI28J/60019ccc75714796af69ebaac1ed805a73aa3863',
            base_url='https://qianfan.baidubce.com/v2/coding'
        )
        
        # 准备论文列表
        paper_list = ""
        for i, p in enumerate(papers[:10], 1):
            paper_list += f"{i}. {p.get('title', 'N/A')}\n"
        
        # 构建prompt
        prompt = f"""请为以下研究主题生成Survey报告：

主题：{topic}

相关论文：
{paper_list}

请按以下格式生成报告：
1. 研究背景
2. 主要研究方向
3. 关键技术
4. 应用场景
5. 未来趋势

请用中文回复，总结每篇论文的核心贡献。
"""
        
        try:
            response = client.chat.completions.create(
                model='minimax-m2.5',
                messages=[{'role': 'user', 'content': prompt}],
                max_tokens=64000
            )
            report = response.choices[0].message.content
            
            # 保存报告
            if output_path:
                Path(output_path).write_text(report)
                print(f"✅ 报告已保存: {output_path}")
            
            return report
        except Exception as e:
            print(f"LLM调用失败: {e}")
            return None
    
    def full_research_flow(self, topic, sources=None, max_results=10):
        """
        完整的深度研究流程
        """
        print(f"\n{'='*50}")
        print(f"🔍 深度研究: {topic}")
        print('='*50)
        
        # 1. 搜索
        print("\n[1] 多数据源搜索...")
        papers = self.search(topic, sources=sources or ['arxiv', 'pubmed'], max_results=max_results)
        print(f"   共找到 {len(papers)} 篇")
        
        # 2. 生成报告
        print("\n[2] 生成Survey报告...")
        report = self.generate_survey_report(papers, topic)
        
        return {
            'papers': papers,
            'report': report
        }


def main():
    """测试"""
    tools = ResearchTools()
    
    # 测试多数据源搜索
    print("=== 测试多数据源搜索 ===")
    papers = tools.search('LLM healthcare', sources=['arxiv'], max_results=3)
    print(f"\n结果: {len(papers)} 篇")
    for p in papers[:3]:
        print(f"  - {p.get('title', 'N/A')[:50]}")


if __name__ == '__main__':
    main()
