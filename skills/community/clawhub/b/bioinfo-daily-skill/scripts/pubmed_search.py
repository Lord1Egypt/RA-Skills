#!/usr/bin/env python3
"""
Bioinfo Daily - PubMed 文献日报生成器
使用 PubMed E-utilities API 搜索前一天的生物信息学和肿瘤学文献
筛选 CNS 及 Nature Index 期刊，生成中文亮点介绍
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict
import xml.etree.ElementTree as ET
import time

# PubMed API 配置（从环境变量或 .env 文件读取，避免硬编码）
import os

# 尝试加载 .env 文件（方式3）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
ENV_FILE = os.path.join(SKILL_DIR, '.env')

if os.path.exists(ENV_FILE):
    with open(ENV_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                if key not in os.environ:  # 环境变量优先
                    os.environ[key] = value

NCBI_EMAIL = os.environ.get("NCBI_EMAIL", "your@email.com")
NCBI_API_KEY = os.environ.get("NCBI_API_KEY", "")
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

if not NCBI_API_KEY:
    print("⚠️  警告: 未设置 NCBI_API_KEY 环境变量")
    print("   请在 ~/.openclaw/openclaw.json 中配置或设置环境变量")
    print("   export NCBI_EMAIL=your@email.com")
    print("   export NCBI_API_KEY=your_api_key")

# 高影响力期刊列表 (CNS + 子刊 + Nature Index)
HIGH_IMPACT_JOURNALS = {
    # CNS 主刊
    "Nature", "Science", "Cell",
    # Nature 子刊
    "Nature Medicine", "Nature Genetics", "Nature Biotechnology", "Nature Methods",
    "Nature Immunology", "Nature Cancer", "Nature Cell Biology", "Nature Reviews Cancer",
    "Nature Reviews Clinical Oncology", "Nature Reviews Drug Discovery", "Nature Biomedical Engineering",
    "Nature Computational Science", "Nature Machine Intelligence", "Nature Communications",
    "Nature Structural & Molecular Biology", "Nature Chemical Biology", "Nature Microbiology",
    # Science 子刊
    "Science Translational Medicine", "Science Immunology", "Science Signaling",
    "Science Advances", "Science Robotics",
    # Cell 子刊
    "Cell Research", "Cell Metabolism", "Cell Host & Microbe", "Cell Stem Cell",
    "Cell Systems", "Molecular Cell", "Cancer Cell", "Immunity", "Neuron",
    "Cell Genomics", "Cell Reports", "iScience", "Heliyon",
    # 其他高影响力期刊
    "The Lancet", "The Lancet Oncology", "The Lancet Digital Health",
    "JAMA", "JAMA Oncology", "PNAS", "Proceedings of the National Academy of Sciences",
    "Genome Research", "Genome Biology", "Nucleic Acids Research",
    "Bioinformatics", "Briefings in Bioinformatics",
    "Cancer Research", "Clinical Cancer Research", "Journal of Clinical Oncology",
    "Blood", "Leukemia", "Journal of Experimental Medicine",
    "Gut", "Hepatology", "Gastroenterology",
}

# 搜索主题配置（限定 cancer 相关）
SEARCH_TOPICS = [
    ("(bioinformatics[Title/Abstract] OR computational biology[Title/Abstract]) AND (cancer[Title/Abstract] OR tumor[Title/Abstract] OR neoplasm[Title/Abstract])", "🧬 生物信息学"),
    ("cancer immunotherapy[Title/Abstract] OR tumor immunity[Title/Abstract] OR immuno-oncology[Title/Abstract] OR checkpoint inhibitor[Title/Abstract]", "🦠 肿瘤免疫"),
    ("(single cell sequencing[Title/Abstract] OR single-cell RNA-seq[Title/Abstract] OR scRNA-seq[Title/Abstract]) AND (cancer[Title/Abstract] OR tumor[Title/Abstract])", "🔬 单细胞测序"),
    ("(spatial transcriptomics[Title/Abstract] OR spatial genomics[Title/Abstract]) AND (cancer[Title/Abstract] OR tumor[Title/Abstract])", "🧪 空间转录组"),
    ("(cancer[Title/Abstract] OR tumor[Title/Abstract]) AND (clinical trial[Publication Type] OR therapeutic[Title/Abstract] OR treatment[Title/Abstract])", "💊 临床进展"),
]

def get_yesterday_date() -> str:
    """获取昨天的日期 (YYYY/MM/DD)"""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y/%m/%d")

def search_pubmed(query: str, date: str, max_results: int = 100) -> List[str]:
    """搜索 PubMed 文献"""
    # 添加日期限制（前一天）
    date_query = f"({query}) AND ({date}[PDAT])"
    
    # 第一步：搜索获取 PMIDs
    search_url = f"{BASE_URL}/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": date_query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "date",
        "email": NCBI_EMAIL,
        "api_key": NCBI_API_KEY,
    }
    
    try:
        response = requests.get(search_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        pmids = data.get("esearchresult", {}).get("idlist", [])
        return pmids
    except Exception as e:
        print(f"搜索失败: {e}")
        return []

def fetch_article_details(pmids: List[str]) -> List[Dict]:
    """获取文献详细信息"""
    if not pmids:
        return []
    
    # 第二步：获取文献详情
    fetch_url = f"{BASE_URL}/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
        "email": NCBI_EMAIL,
        "api_key": NCBI_API_KEY,
    }
    
    try:
        response = requests.get(fetch_url, params=params, timeout=30)
        response.raise_for_status()
        
        # 解析 XML
        root = ET.fromstring(response.content)
        articles = []
        
        for article in root.findall(".//PubmedArticle"):
            try:
                # 提取标题
                title_elem = article.find(".//ArticleTitle")
                title = title_elem.text if title_elem is not None else "N/A"
                
                # 提取期刊名
                journal_elem = article.find(".//Journal/Title")
                journal = journal_elem.text if journal_elem is not None else "N/A"
                
                # 提取摘要
                abstract_elems = article.findall(".//Abstract/AbstractText")
                abstract = " ".join([elem.text for elem in abstract_elems if elem.text]) or "N/A"
                
                # 提取作者
                author_elems = article.findall(".//Author/LastName")
                authors = [elem.text for elem in author_elems if elem.text]
                first_author = authors[0] if authors else "N/A"
                
                # 提取日期
                date_elem = article.find(".//PubDate/Year")
                year = date_elem.text if date_elem is not None else "N/A"
                
                # 提取 PMID
                pmid_elem = article.find(".//PMID")
                pmid = pmid_elem.text if pmid_elem is not None else "N/A"
                
                # 提取 DOI
                doi_elem = article.find(".//ArticleId[@IdType='doi']")
                doi = doi_elem.text if doi_elem is not None else "N/A"
                
                articles.append({
                    "pmid": pmid,
                    "title": title,
                    "journal": journal,
                    "abstract": abstract[:500] + "..." if len(abstract) > 500 else abstract,
                    "first_author": first_author,
                    "year": year,
                    "doi": doi,
                })
            except Exception as e:
                continue
        
        return articles
    except Exception as e:
        print(f"获取文献详情失败: {e}")
        return []

def filter_high_impact(articles: List[Dict]) -> List[Dict]:
    """筛选高影响力期刊文献"""
    filtered = []
    for article in articles:
        journal = article.get("journal", "")
        # 检查是否在高影响力期刊列表中
        for high_impact_journal in HIGH_IMPACT_JOURNALS:
            if high_impact_journal.lower() in journal.lower():
                article["journal_tier"] = "High Impact"
                filtered.append(article)
                break
    return filtered

def generate_highlight(article: Dict) -> str:
    """生成中文亮点介绍（30字左右）"""
    title = article.get("title", "")
    journal = article.get("journal", "")
    
    # 根据标题关键词生成亮点
    highlights = []
    
    if any(kw in title.lower() for kw in ["single-cell", "scRNA", "single cell"]):
        highlights.append("单细胞技术揭示细胞异质性新机制")
    elif any(kw in title.lower() for kw in ["spatial", "spatial transcriptomics"]):
        highlights.append("空间组学解析肿瘤微环境空间结构")
    elif any(kw in title.lower() for kw in ["immunotherapy", "checkpoint", "CAR-T", "PD-1", "PD-L1"]):
        highlights.append("免疫治疗新靶点或耐药机制研究")
    elif any(kw in title.lower() for kw in ["bioinformatics", "algorithm", "machine learning", "deep learning", "AI"]):
        highlights.append("生物信息学算法或AI模型创新")
    elif any(kw in title.lower() for kw in ["genomic", "mutation", "variant"]):
        highlights.append("基因组学发现新生物标志物")
    elif any(kw in title.lower() for kw in ["clinical trial", "patient", "therapeutic"]):
        highlights.append("临床试验或治疗策略重要进展")
    elif any(kw in title.lower() for kw in ["tumor microenvironment", "TME"]):
        highlights.append("肿瘤微环境调控机制新发现")
    else:
        highlights.append("肿瘤生物学重要机制研究")
    
    # 根据期刊级别调整
    if "Nature" in journal or "Science" in journal or "Cell" in journal:
        highlights[0] = "【顶刊】" + highlights[0]
    
    return highlights[0][:35] if highlights else "重要研究进展"

def calculate_innovation_score(article: Dict) -> int:
    """计算文章创新性得分"""
    score = 0
    title = article.get("title", "").lower()
    abstract = article.get("abstract", "").lower()
    journal = article.get("journal", "").lower()
    
    # 期刊级别得分
    if any(tier in journal for tier in ["nature", "science", "cell"]):
        score += 30
    elif "pnas" in journal or "proceedings of the national academy" in journal:
        score += 25
    elif any(j in journal for j in ["lancet", "jama", "bmj"]):
        score += 25
    
    # 创新性关键词
    innovation_keywords = [
        ("novel", 5), ("new", 3), ("first", 5), ("breakthrough", 8),
        ("innovative", 5), ("pioneering", 6), ("landmark", 7),
        ("single-cell", 4), ("spatial", 4), ("multi-omics", 5),
        ("artificial intelligence", 5), ("machine learning", 4), ("deep learning", 4),
        ("crispr", 5), ("car-t", 5), ("checkpoint inhibitor", 4),
        ("biomarker", 3), ("therapeutic target", 4), ("drug resistance", 3),
    ]
    
    for keyword, points in innovation_keywords:
        if keyword in title or keyword in abstract:
            score += points
    
    return score

def select_diverse_articles(articles: List[Dict], max_count: int = 10) -> List[Dict]:
    """智能优选：选择创新性强且方向有区分的文章"""
    if len(articles) <= max_count:
        return articles
    
    # 计算创新性得分
    for article in articles:
        article["innovation_score"] = calculate_innovation_score(article)
    
    # 按类别分组
    categories = {}
    for article in articles:
        cat = article.get("category", "其他")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(article)
    
    # 每个类别选择得分最高的，确保方向区分
    selected = []
    for cat, cat_articles in categories.items():
        cat_articles.sort(key=lambda x: x["innovation_score"], reverse=True)
        # 每个类别最多选2篇，确保多样性
        selected.extend(cat_articles[:2])
    
    # 如果还不够，从剩余文章中按得分补充
    if len(selected) < max_count:
        remaining = [a for a in articles if a not in selected]
        remaining.sort(key=lambda x: x["innovation_score"], reverse=True)
        selected.extend(remaining[:max_count - len(selected)])
    
    # 最终排序：顶刊优先，然后按得分
    selected.sort(key=lambda x: (
        0 if any(tier in x.get("journal", "").lower() for tier in ["nature", "science", "cell"]) else 1,
        -x.get("innovation_score", 0)
    ))
    
    return selected[:max_count]

def generate_summary(articles: List[Dict]) -> str:
    """生成精选文章 summary"""
    if not articles:
        return "昨日暂无重要文献更新。"
    
    # 统计各方向
    categories = {}
    top_journals = []
    
    for article in articles:
        cat = article.get("category", "其他")
        categories[cat] = categories.get(cat, 0) + 1
        journal = article.get("journal", "")
        if any(tier in journal for tier in ["Nature", "Science", "Cell", "Lancet", "JAMA"]):
            top_journals.append(journal.split(":")[0])
    
    summary_parts = []
    summary_parts.append(f"本日共筛选出 {len(articles)} 篇高影响力文献")
    
    if top_journals:
        unique_journals = list(set(top_journals))[:3]
        summary_parts.append(f"，涵盖 {', '.join(unique_journals)} 等顶刊")
    
    if categories:
        cat_str = ", ".join([f"{cat.split()[1] if ' ' in cat else cat}({count}篇)" for cat, count in sorted(categories.items(), key=lambda x: -x[1])[:3]])
        summary_parts.append(f"；主要涉及 {cat_str}")
    
    # 找出最具创新性的文章
    if articles:
        most_innovative = max(articles, key=lambda x: x.get("innovation_score", 0))
        if most_innovative.get("innovation_score", 0) > 20:
            title = most_innovative.get("title", "")[:50] + "..." if len(most_innovative.get("title", "")) > 50 else most_innovative.get("title", "")
            summary_parts.append(f"。亮点研究：{title}")
    
    return "".join(summary_parts)

def generate_daily_report(articles: List[Dict], date: str) -> str:
    """生成日报"""
    if not articles:
        return f"📰 生物信息学日报 ({date})\n\n昨日暂无新文献。"
    
    # 智能优选
    selected_articles = select_diverse_articles(articles, max_count=10)
    
    report = []
    report.append("=" * 60)
    report.append("📰 生物信息学日报")
    report.append(f"📅 {date}")
    report.append("=" * 60)
    report.append("")
    
    # 添加 summary
    summary = generate_summary(selected_articles)
    report.append(f"📝 {summary}")
    report.append("")
    
    report.append(f"🔍 精选 {len(selected_articles)} 篇高影响力文献（从 {len(articles)} 篇中优选）")
    report.append("")
    
    for i, article in enumerate(selected_articles, 1):
        highlight = generate_highlight(article)
        innovation_tag = "🔥" if article.get("innovation_score", 0) > 25 else ""
        report.append(f"{i}. {article.get('title', 'N/A')} {innovation_tag}")
        report.append(f"   📚 {article.get('journal', 'N/A')}")
        report.append(f"   👤 {article.get('first_author', 'N/A')} et al. | {article.get('year', 'N/A')}")
        report.append(f"   💡 {highlight}")
        report.append(f"   🔗 https://pubmed.ncbi.nlm.nih.gov/{article.get('pmid', '')}/")
        report.append("")
    
    report.append("=" * 60)
    report.append("📊 数据来源: PubMed | 筛选标准: CNS及Nature Index期刊")
    report.append("💡 标记🔥为创新性评分>25的高亮点文章")
    report.append("=" * 60)
    
    return "\n".join(report)

def save_markdown_report(report_text: str, date: str) -> str:
    """保存为 Markdown 格式，便于分享"""
    # 转换为 Markdown 格式
    md_content = report_text
    
    # 添加 Markdown 标题格式
    md_content = md_content.replace("📰 生物信息学日报", "# 📰 生物信息学日报")
    md_content = md_content.replace("📝 ", "## 📝 ")
    md_content = md_content.replace("🔍 精选", "## 🔍 精选")
    
    # 保存文件
    md_file = f"/tmp/bioinfo_daily_{date.replace('/', '')}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return md_file

def main():
    """主函数"""
    print("🔬 正在生成生物信息学日报...\n")
    
    yesterday = get_yesterday_date()
    print(f"📅 搜索日期: {yesterday}")
    print("🔍 正在搜索高影响力期刊文献...\n")
    
    all_articles = []
    
    for query, category in SEARCH_TOPICS:
        print(f"搜索: {category}...")
        pmids = search_pubmed(query, yesterday, max_results=50)
        if pmids:
            articles = fetch_article_details(pmids)
            high_impact_articles = filter_high_impact(articles)
            for article in high_impact_articles:
                article["category"] = category
            all_articles.extend(high_impact_articles)
            print(f"  ✓ 找到 {len(high_impact_articles)} 篇高影响力文献")
        time.sleep(0.5)  # 避免请求过快
    
    # 去重
    unique_articles = {article["pmid"]: article for article in all_articles}
    all_articles = list(unique_articles.values())
    
    print(f"\n📊 总计: {len(all_articles)} 篇高影响力文献")
    
    # 生成日报
    report = generate_daily_report(all_articles, yesterday)
    print("\n" + report)
    
    # 保存到文本文件
    output_file = f"/tmp/bioinfo_daily_{yesterday.replace('/', '')}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n📄 日报已保存: {output_file}")
    
    # 保存为 Markdown 格式，便于分享
    md_file = save_markdown_report(report, yesterday)
    print(f"📥 Markdown 格式: {md_file}")
    print(f"\n💡 提示: 使用以下命令下载 Markdown 文件:")
    print(f"   curl -o bioinfo_daily.md file://{md_file}")
    print(f"   # 或在服务器上直接复制: cp {md_file} ./")
    
    # 在报告末尾添加下载链接信息
    report += f"\n\n{'=' * 60}\n"
    report += f"📥 文件下载:\n"
    report += f"   文本格式: {output_file}\n"
    report += f"   Markdown: {md_file}\n"
    report += f"{'=' * 60}\n"
    
    return report

if __name__ == "__main__":
    main()
