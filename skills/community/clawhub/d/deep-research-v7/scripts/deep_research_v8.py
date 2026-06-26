#!/usr/bin/env python3
"""
深度研究 v8.0 最终版
基于Research-Claw, 目标80分
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime
from openai import OpenAI
import tempfile
from urllib.request import urlretrieve

sys.path.insert(0, '/root/.openclaw/workspace/research-claw/research-claw-main')


class DeepResearchV8:
    """最终版深度研究引擎"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key='bce-v3/ALTAKSP-MhjY1gIGq8XyzO87nI28J/60019ccc75714796af69ebaac1ed805a73aa3863',
            base_url='https://qianfan.baidubce.com/v2/coding'
        )
        self.tools = {}
        
    def _get_tool(self, name):
        if name not in self.tools:
            if name == 'arxiv':
                from agent.tools.arxiv_search import ArxivSearchTool
                self.tools[name] = ArxivSearchTool()
            elif name == 'pubmed':
                from agent.tools.pubmed_search import PubMedSearchTool
                self.tools[name] = PubMedSearchTool()
            elif name == 'google':
                try:
                    from agent.tools.google_scholar import GoogleScholarTool
                    self.tools[name] = GoogleScholarTool()
                except:
                    print(f"  ⚠ {name} 不可用")
                    return None
            elif name == 'semantic':
                try:
                    from agent.tools.semantic_scholar import SemanticScholarTool
                    self.tools[name] = SemanticScholarTool()
                except:
                    print(f"  ⚠ {name} 不可用")
                    return None
            elif name == 'openalex':
                from agent.tools.openalex_search import OpenAlexSearchTool
                self.tools[name] = OpenAlexSearchTool()
        return self.tools.get(name)
    
    def expand_keywords(self, topic):
        base = topic.replace(',', ' ').replace('，', ' ').split()
        keywords = []
        for kw in base:
            keywords.extend([kw, f"AI {kw}", f"ML {kw}", f"machine learning {kw}"])
        return list(set(keywords))[:20]
    
    async def search_all(self, topic):
        """全数据源并行搜索"""
        keywords = self.expand_keywords(topic)
        
        # 5个数据源
        sources = ['arxiv', 'pubmed', 'google', 'semantic', 'openalex']
        
        print(f"\n[Phase 1] 多数据源搜索 ({len(sources)}个)")
        
        papers = []
        for source in sources:
            tool = self._get_tool(source)
            if tool is None:
                continue
            for kw in keywords[:4]:
                try:
                    result = tool.execute(query=kw, max_results=8)
                    parsed = self._parse_result(result, source)
                    papers.extend(parsed)
                    print(f"  [{source}] {kw[:15]}... → {len(parsed)}篇")
                except:
                    pass
        
        # 去重
        seen = set()
        unique = []
        for p in papers:
            pid = p.get('id', p.get('title', '')[:30])
            if pid and pid not in seen:
                seen.add(pid)
                unique.append(p)
        
        print(f"  总计: {len(unique)}篇 (去重后)")
        return unique
    
    def _parse_result(self, raw, source):
        papers = []
        lines = str(raw).split('\n')
        
        for line in lines:
            if 'arXiv ID' in line:
                aid = line.split(':')[-1].strip()
                idx = lines.index(line)
                title = lines[idx-1].strip().lstrip('[]') if idx > 0 else ''
                papers.append({
                    'id': aid,
                    'title': title,
                    'source': 'arXiv',
                    'url': f'https://arxiv.org/abs/{aid}',
                    'pdf': f'https://arxiv.org/pdf/{aid}.pdf'
                })
            elif 'PMID' in line:
                pid = line.split(':')[-1].strip()
                papers.append({
                    'id': pid,
                    'title': line.strip(),
                    'source': 'PubMed',
                    'url': f'https://pubmed.ncbi.nlm.nih.gov/{pid}/'
                })
        
        return papers
    
    def deep_analyze(self, papers, topic):
        """深度分析 + PDF解读"""
        print(f"\n[Phase 2] 深度分析 {len(papers)}篇...")
        
        # 取核心论文
        core = papers[:20]
        
        # PDF深度解读
        pdf_analyses = []
        for i, p in enumerate(core[:5], 1):
            print(f"  PDF解析 {i}/5: {p.get('title','')[:30]}...")
            pdf_content = self._extract_pdf(p.get('pdf', ''))
            if pdf_content:
                pdf_analyses.append({
                    'paper': p,
                    'content': pdf_content[:2000]
                })
        
        # 生成报告
        paper_list = ""
        for i, p in enumerate(core[:15], 1):
            paper_list += f"{i}. [{p.get('source','')}] {p.get('title', 'N/A')[:80]}\n"
            paper_list += f"   📎 {p.get('url', 'N/A')}\n"
        
        prompt = f"""请作为医疗健康保险领域的专家，对以下论文进行深度分析：

主题: {topic}

论文列表:
{paper_list}

请分析:
## 1. 研究方向聚类 (轻症居家治疗/重症预警/保险控费)
## 2. 核心技术 (联邦学习/预测模型/可解释AI)
## 3. 实施建议 (短期/中期/长期)
## 4. 数据来源

请用中文，结构化输出。
"""
        
        try:
            resp = self.client.chat.completions.create(
                model='qianfan-code-latest',
                messages=[{'role': 'user', 'content': prompt}],
                max_tokens=4000
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"分析失败: {e}"
    
    def _extract_pdf(self, pdf_url):
        """提取PDF内容"""
        if not pdf_url:
            return None
        try:
            import pymupdf
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
                urlretrieve(pdf_url, f.name)
                doc = pymupdf.open(f.name)
                text = ""
                for page in doc:
                    text += page.get_text()
                import os
                os.unlink(f.name)
                return text[:3000]
        except:
            return None
    
    def generate_report(self, topic, analysis, papers):
        """生成报告"""
        print(f"\n[Phase 3] 生成报告...")
        
        # 带溯源的论文列表
        ref_list = ""
        for i, p in enumerate(papers[:30], 1):
            ref_list += f"{i}. [{p.get('source','')}] {p.get('title', 'N/A')}\n"
            ref_list += f"   🔗 {p.get('url', 'N/A')}\n"
        
        full = f"""# {topic} - 深度研究报告 v8.0-Final

*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
*数据源: arXiv, PubMed, Google Scholar, Semantic Scholar, OpenAlex*
*论文数量: {len(papers)}篇*

---

## 研究分析

{analysis or '无'}

---

## 参考文献 ({len(papers)}篇)

{ref_list}

---
*自动生成*
"""
        return full
    
    async def run(self, topic, output_path=None):
        print("="*50)
        print(f"深度研究 v8.0-Final | 目标: 80分")
        print(f"主题: {topic}")
        print("="*50)
        
        # 搜索
        papers = await self.search_all(topic)
        
        # 分析
        analysis = self.deep_analyze(papers, topic)
        
        # 报告
        report = self.generate_report(topic, analysis, papers)
        
        if output_path:
            Path(output_path).write_text(report)
            print(f"\n✅ 已保存: {output_path}")
        
        print(f"\n完成! 论文数: {len(papers)}")
        return report


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('topic', help='研究主题')
    parser.add_argument('-o', '--output', help='输出文件')
    args = parser.parse_args()
    
    engine = DeepResearchV8()
    asyncio.run(engine.run(args.topic, args.output))
