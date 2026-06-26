#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily Literature Search - Main Script

Automated literature search and retrieval system for academic research.
Supports scheduled searches, automatic deduplication, OA download, and categorized storage.

Usage:
    python3 daily_literature_search.py [--config PATH] [--dry-run] [--verbose]

Examples:
    python3 daily_literature_search.py
    python3 daily_literature_search.py --config /path/to/config.yaml
    python3 daily_literature_search.py --dry-run --verbose
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.parse
import hashlib
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Add scripts directory to path for imports
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from utils import (
    load_config,
    setup_logging,
    ensure_directories,
    get_today_str,
    get_timestamp_str,
    get_cutoff_date,
    normalize_doi,
    extract_doi_from_text,
    safe_filename,
    generate_report_filename,
    generate_log_filename,
)
from classifier import create_default_classifier, PaperClassifier

# ==================== Global Variables ====================

# Will be initialized from config
CONFIG = None
LOGGER = None
TODAY = None
LOG_FILE = None
REPORT_FILE = None
CLASSIFIER = None

# ==================== Configuration ====================

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Daily Literature Search - Automated literature retrieval system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Run with default config
  %(prog)s --config config.yaml     # Run with custom config
  %(prog)s --dry-run                # Test run without downloads
  %(prog)s --verbose                # Enable debug logging
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        default=None,
        help='Path to configuration YAML file (default: config/config.yaml)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without downloading papers (test mode)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose/debug logging'
    )
    
    parser.add_argument(
        '--no-download',
        action='store_true',
        help='Skip paper downloads (search and report only)'
    )
    
    return parser.parse_args()

def initialize_config(args):
    """Initialize configuration from file and command line args."""
    global CONFIG, LOGGER, TODAY, LOG_FILE, REPORT_FILE, CLASSIFIER
    
    # Load configuration
    try:
        CONFIG = load_config(args.config)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\nPlease create a config file:")
        print("  cp config.example.yaml config.yaml")
        print("  # Edit config.yaml with your settings")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        sys.exit(1)
    
    # Override config with command line args
    if args.verbose:
        if 'logging' not in CONFIG:
            CONFIG['logging'] = {}
        CONFIG['logging']['level'] = 'DEBUG'
    
    # Set global variables
    TODAY = get_today_str()
    
    # Setup logging
    log_dir = CONFIG.get('log_dir', Path.cwd() / 'logs')
    log_dir.mkdir(parents=True, exist_ok=True)
    LOG_FILE = log_dir / generate_log_filename('daily_search', TODAY)
    REPORT_FILE = log_dir / generate_report_filename('daily_report', TODAY)
    
    LOGGER = setup_logging(CONFIG, LOG_FILE)
    
    # Ensure directories exist
    ensure_directories(CONFIG)
    
    # Initialize classifier
    if 'classification' in CONFIG:
        CLASSIFIER = PaperClassifier(CONFIG['classification'])
    else:
        CLASSIFIER = create_default_classifier()
    
    return CONFIG

# ==================== Logging ====================

def log(message, level="INFO"):
    """
    Log a message with timestamp and level.
    
    Args:
        message: Message to log
        level: Log level (INFO, DEBUG, WARNING, ERROR, SUCCESS)
    """
    if LOGGER:
        if level == "SUCCESS":
            LOGGER.info(f"✅ {message}")
        elif level == "ERROR":
            LOGGER.error(f"❌ {message}")
        elif level == "WARNING":
            LOGGER.warning(f"⚠️  {message}")
        elif level == "DEBUG":
            LOGGER.debug(message)
        else:
            LOGGER.info(message)
    else:
        # Fallback if logger not initialized
        timestamp = get_timestamp_str()
        print(f"[{timestamp}] [{level}] {message}")

# ==================== Literature Search ====================

def search_lit_review(keyword, limit=10, source="pm"):
    """
    Search literature using literature-review skill.
    
    Args:
        keyword: Search query
        limit: Maximum results to return
        source: Data source (pm=PubMed, oa=OpenAlex, s2=Semantic Scholar)
    
    Returns:
        List of paper dictionaries
    """
    log(f"检索关键词：{keyword} (来源：{source})")
    
    # Get workspace from config
    papers_dir = CONFIG.get('papers_dir', Path.home() / ".openclaw" / "workspace" / "papers")
    skill_script = papers_dir.parent / "skills" / "literature-review" / "scripts" / "lit_search.py"
    
    if not skill_script.exists():
        log(f"  → literature-review skill not found: {skill_script}", "ERROR")
        return []
    
    cmd = [
        "python3", str(skill_script),
        "search", keyword,
        "--limit", str(limit),
        "--source", source
    ]
    
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            timeout=120
        )
        
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                papers = data.get("data", [])
                log(f"  → 找到 {len(papers)} 篇文献", "SUCCESS")
                return papers
            except json.JSONDecodeError:
                log(f"  → 解析检索结果失败", "ERROR")
                return []
        else:
            log(f"  → 检索失败：{result.stderr}", "ERROR")
            return []
            
    except subprocess.TimeoutExpired:
        log(f"  → 检索超时 (120s)", "ERROR")
        return []
    except Exception as e:
        log(f"  → 异常：{e}", "ERROR")
        return []

# ==================== Deduplication ====================

def load_existing_dois():
    """
    Load DOIs from existing paper library.
    
    Returns:
        Set of existing DOIs (normalized, lowercase)
    """
    log("加载本地论文库 DOI 索引...")
    
    existing_dois = set()
    papers_dir = CONFIG.get('papers_dir')
    
    if not papers_dir:
        log("  ⚠️  未配置 papers_dir，跳过本地库去重", "WARNING")
        return existing_dois
    
    # Scan category directories
    categories = CONFIG.get('categories', {})
    for cat_name, cat_config in categories.items():
        cat_dir = cat_config.get('directory')
        if not cat_dir or not Path(cat_dir).exists():
            continue
        
        for pdf_file in Path(cat_dir).glob("*.pdf"):
            filename = pdf_file.name.lower()
            
            # Extract DOI from filename
            doi = extract_doi_from_text(filename)
            if doi:
                existing_dois.add(normalize_doi(doi))
    
    # Scan historical search logs
    log_dir = CONFIG.get('log_dir')
    if log_dir and Path(log_dir).exists():
        for log_file in log_dir.glob("daily_search_*.log"):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    dois = extract_dois_from_text(content)
                    existing_dois.update(dois)
            except Exception as e:
                log(f"  读取日志文件失败 {log_file}: {e}", "DEBUG")
    
    log(f"  本地库中共有 {len(existing_dois)} 篇文献（基于 DOI 索引）")
    return existing_dois

def extract_dois_from_text(text):
    """Extract all DOIs from text."""
    import re
    doi_pattern = r"10\.\d+[/\w\.\-]+"
    matches = re.findall(doi_pattern, text, re.IGNORECASE)
    return [normalize_doi(m) for m in matches if m]

def deduplicate_papers(papers_list, existing_dois=None):
    """
    Deduplicate papers by DOI.
    
    Args:
        papers_list: List of paper dictionaries
        existing_dois: Set of existing DOIs to check against
    
    Returns:
        Tuple of (unique_papers, stats_dict)
    """
    log("开始去重...")
    
    doi_set = set()
    unique_papers = []
    duplicates_session = 0
    duplicates_library = 0
    
    # Load existing DOIs if not provided
    if existing_dois is None:
        existing_dois = load_existing_dois()
    
    for paper in papers_list:
        doi = paper.get("doi", "")
        
        if doi:
            doi_clean = normalize_doi(doi)
            
            # Check if in library
            if doi_clean in existing_dois:
                duplicates_library += 1
                log(f"  库中已有，跳过：{doi_clean}", "DEBUG")
                continue
            
            # Check if duplicate in batch
            if doi_clean not in doi_set:
                doi_set.add(doi_clean)
                unique_papers.append(paper)
            else:
                duplicates_session += 1
                log(f"  批次内重复 DOI: {doi_clean}", "DEBUG")
        else:
            # No DOI: use title hash
            title = paper.get("title", "")
            title_hash = hashlib.md5(title.encode()).hexdigest()
            
            if title_hash not in doi_set:
                doi_set.add(title_hash)
                unique_papers.append(paper)
            else:
                duplicates_session += 1
    
    total_duplicates = duplicates_session + duplicates_library
    
    log(f"去重完成：原始 {len(papers_list)} 篇，去重后 {len(unique_papers)} 篇")
    log(f"  - 批次内重复：{duplicates_session} 篇")
    log(f"  - 库中已有：{duplicates_library} 篇")
    
    stats = {
        'session_duplicates': duplicates_session,
        'library_duplicates': duplicates_library,
        'total_duplicates': total_duplicates,
        'raw_count': len(papers_list),
        'unique_count': len(unique_papers),
        'library_size': len(existing_dois)
    }
    
    return unique_papers, stats

# ==================== Date Filtering ====================

def filter_by_date(papers, days=None):
    """
    Filter papers by publication date.
    
    Args:
        papers: List of paper dictionaries
        days: Number of days to look back (from config if not specified)
    
    Returns:
        Filtered list of papers
    """
    if days is None:
        days = CONFIG.get('date_range_days', 7)
    
    log(f"筛选最近 {days} 天的文献...")
    
    cutoff_date = get_cutoff_date(days)
    filtered = []
    
    for paper in papers:
        year = paper.get("year", 0)
        
        # Simple filter: keep papers from current year and previous year
        current_year = datetime.now().year
        if year >= current_year - 1:
            filtered.append(paper)
        else:
            log(f"  排除旧文献 ({year}): {paper.get('title', '')[:50]}", "DEBUG")
    
    log(f"日期筛选完成：{len(filtered)} 篇符合条件")
    return filtered

# ==================== Classification ====================

def classify_paper(paper):
    """
    Classify paper into category.
    
    Args:
        paper: Paper dictionary with title and abstract
    
    Returns:
        Category name (e.g., "B-ALL", "MM", "OTHER")
    """
    title = paper.get("title", "") or ""
    abstract = paper.get("abstract", "") or ""
    
    category, score = CLASSIFIER.classify(title, abstract)
    
    if score > 0:
        log(f"  分类：{category} (置信度：{score})", "DEBUG")
    else:
        log(f"  分类：{category} (无匹配关键词)", "DEBUG")
    
    return category

# ==================== Download ====================

def check_open_access(doi):
    """
    Check if paper is open access using Unpaywall API.
    
    Args:
        doi: Paper DOI
    
    Returns:
        Tuple of (is_oa, oa_url)
    """
    if not doi:
        return False, None
    
    try:
        url = f"https://api.unpaywall.org/v2/{doi}"
        params = {"email": CONFIG.get('user_email', 'anonymous@example.org')}
        full_url = f"{url}?{urllib.parse.urlencode(params)}"
        
        with urllib.request.urlopen(full_url, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if data.get("is_oa", False):
                oa_url = data.get("oa_url", "")
                log(f"  ✓ 开放获取：{oa_url}", "SUCCESS")
                return True, oa_url
            else:
                log(f"  ✗ 付费墙文献", "DEBUG")
                return False, None
                
    except Exception as e:
        log(f"  OA 检查失败：{e}", "DEBUG")
        return False, None

def download_paper(url, save_path, title="unknown"):
    """
    Download paper PDF from URL.
    
    Args:
        url: Download URL
        save_path: Path to save PDF
        title: Paper title (for logging)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        headers = {
            "User-Agent": CONFIG.get('download', {}).get(
                'user_agent',
                "Mozilla/5.0 (compatible; LiteratureBot/1.0)"
            )
        }
        req = urllib.request.Request(url, headers=headers)
        
        timeout = CONFIG.get('download', {}).get('timeout', 60)
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            with open(save_path, "wb") as f:
                f.write(response.read())
        
        log(f"  ✓ 下载成功：{save_path.name}", "SUCCESS")
        return True
        
    except Exception as e:
        log(f"  ✗ 下载失败 {title[:50]}: {e}", "ERROR")
        if save_path.exists():
            save_path.unlink()
        return False

def download_from_pubmed(pmid, save_path):
    """
    Download paper from PubMed Central.
    
    Args:
        pmid: PubMed ID
        save_path: Path to save PDF
    
    Returns:
        True if successful, False otherwise
    """
    try:
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
        params = {
            "dbfrom": "pubmed",
            "db": "pmc",
            "id": pmid,
            "retmode": "json"
        }
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            linksets = data.get("linksets", [])
            
            if linksets and len(linksets) > 0:
                linksetdb = linksets[0].get("linksetdb", [])
                if linksetdb and len(linksetdb) > 0:
                    links = linksetdb[0].get("links", [])
                    
                    if links:
                        pmcid = f"PMC{links[0]}"
                        pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/"
                        return download_paper(pdf_url, save_path, pmcid)
                        
    except Exception as e:
        log(f"  PubMed Central 下载失败：{e}", "DEBUG")
    
    return False

# ==================== Report Generation ====================

def generate_daily_report(results, dedup_stats=None):
    """
    Generate daily search report in Markdown format.
    
    Args:
        results: Dictionary with search results by category
        dedup_stats: Dictionary with deduplication statistics
    """
    log(f"生成报告...")
    
    report = []
    report.append("# 📚 每日文献检索报告")
    report.append(f"**检索日期：** {TODAY}")
    report.append(f"**生成时间：** {get_timestamp_str()}")
    report.append("")
    
    # Summary table
    report.append("## 📊 检索汇总")
    report.append("")
    report.append("| 分类 | 检索到 | 成功下载 | 付费墙 |")
    report.append("|------|--------|---------|--------|")
    
    for cat_name in ["B-ALL", "MM", "OTHER"]:
        if cat_name in results:
            cat = results[cat_name]
            report.append(f"| {cat_name} | {cat['total']} | {cat['downloaded']} | {cat['paywall']} |")
    
    total = results.get('total', 0)
    downloaded = results.get('downloaded', 0)
    paywall = results.get('paywall', 0)
    report.append(f"| **总计** | **{total}** | **{downloaded}** | **{paywall}** |")
    report.append("")
    
    # Deduplication stats
    if dedup_stats:
        report.append("## 🔀 去重统计")
        report.append("")
        report.append(f"- **原始检索结果：** {dedup_stats.get('raw_count', 0)} 篇")
        report.append(f"- **去重后文献：** {dedup_stats.get('unique_count', 0)} 篇")
        report.append(f"- **批次内重复：** {dedup_stats.get('session_duplicates', 0)} 篇")
        report.append(f"- **库中已有：** {dedup_stats.get('library_duplicates', 0)} 篇")
        report.append(f"- **本地库文献总数：** {dedup_stats.get('library_size', 0)} 篇")
        report.append("")
    
    # Detailed lists by category
    for cat_name in ["B-ALL", "MM", "OTHER"]:
        if cat_name not in results:
            continue
            
        cat = results[cat_name]
        if cat['downloaded_papers'] or cat['paywall_papers']:
            report.append(f"## {cat_name} 文献")
            report.append("")
            
            if cat['downloaded_papers']:
                report.append("### ✅ 已下载")
                report.append("")
                for i, paper in enumerate(cat['downloaded_papers'], 1):
                    title = paper.get('title', 'Unknown')
                    journal = paper.get('venue', 'Unknown')
                    year = paper.get('year', 'Unknown')
                    doi = paper.get('doi', '')
                    
                    report.append(f"{i}. **{title}**")
                    report.append(f"   - 期刊：{journal} | 年份：{year}")
                    if doi:
                        report.append(f"   - DOI: [{doi}](https://doi.org/{doi})")
                    report.append("")
            
            if cat['paywall_papers']:
                report.append("### 🔒 付费墙（需手动下载）")
                report.append("")
                for i, paper in enumerate(cat['paywall_papers'], 1):
                    title = paper.get('title', 'Unknown')
                    journal = paper.get('venue', 'Unknown')
                    year = paper.get('year', 'Unknown')
                    doi = paper.get('doi', '')
                    
                    report.append(f"{i}. **{title}**")
                    report.append(f"   - 期刊：{journal} | 年份：{year}")
                    if doi:
                        report.append(f"   - DOI: [{doi}](https://doi.org/{doi})")
                    report.append("")
    
    # Search keywords
    report.append("## 🔍 检索关键词")
    report.append("")
    search_keywords = CONFIG.get('search_keywords', [])
    for kw in search_keywords:
        report.append(f"- {kw}")
    report.append("")
    
    # File locations
    report.append("## 📥 文件位置")
    report.append("")
    papers_dir = CONFIG.get('papers_dir', Path.cwd() / 'papers')
    categories = CONFIG.get('categories', {})
    
    for cat_name in ["B-ALL", "MM", "OTHER"]:
        if cat_name in categories:
            cat_dir = categories[cat_name].get('directory', '')
            report.append(f"- {cat_name} 文献：`{cat_dir}`")
    
    if LOG_FILE:
        report.append(f"- 检索日志：`{LOG_FILE}`")
    report.append("")
    
    # Save report
    report_text = "\n".join(report)
    
    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(report_text)
        log(f"报告已生成：{REPORT_FILE}", "SUCCESS")
    except Exception as e:
        log(f"报告保存失败：{e}", "ERROR")
    
    return report_text

# ==================== Main Execution ====================

def main():
    """Main execution flow."""
    # Parse arguments
    args = parse_args()
    
    # Initialize configuration
    CONFIG = initialize_config(args)
    
    log("=" * 60)
    log("📚 Daily Literature Search System Starting")
    log("=" * 60)
    log(f"配置来源：{args.config or 'default'}")
    log(f"运行模式：{'Dry Run' if args.dry_run else 'Normal'}")
    log(f"检索关键词：{len(CONFIG.get('search_keywords', []))} 个")
    log("")
    
    # Get configuration values
    search_keywords = CONFIG.get('search_keywords', [])
    sources = CONFIG.get('sources', ['pm', 'oa', 's2'])
    max_results = CONFIG.get('max_results_per_keyword', 10)
    no_download = args.no_download or args.dry_run
    
    # Collect all papers
    all_papers = []
    
    # Step 1: Search
    log("【步骤 1/5】检索文献...")
    for keyword in search_keywords:
        for source in sources:
            papers = search_lit_review(keyword, limit=max_results, source=source)
            all_papers.extend(papers)
    
    log(f"检索完成，共获得 {len(all_papers)} 篇文献")
    log("")
    
    # Step 2: Deduplicate
    log("【步骤 2/5】去重...")
    unique_papers, dedup_stats = deduplicate_papers(all_papers)
    log("")
    
    # Step 3: Filter by date
    log("【步骤 3/5】筛选近期文献...")
    date_range = CONFIG.get('date_range_days', 7)
    recent_papers = filter_by_date(unique_papers, days=date_range)
    log("")
    
    # Step 4: Classify and download
    log("【步骤 4/5】分类和下载...")
    
    # Initialize results structure
    results = {
        'total': 0,
        'downloaded': 0,
        'paywall': 0,
    }
    
    categories = CONFIG.get('categories', {})
    for cat_name in categories.keys():
        results[cat_name] = {
            'total': 0,
            'downloaded': 0,
            'paywall': 0,
            'downloaded_papers': [],
            'paywall_papers': []
        }
    
    # Process each paper
    for i, paper in enumerate(recent_papers, 1):
        title = paper.get('title', 'Unknown')[:80]
        doi = paper.get('doi', '')
        pmid = paper.get('id', '')
        
        log(f"[{i}/{len(recent_papers)}] 处理：{title}...")
        
        # Classify
        category = classify_paper(paper)
        
        if category in results:
            results[category]['total'] += 1
        else:
            results['OTHER']['total'] += 1
            category = 'OTHER'
        
        results['total'] += 1
        
        # Get target directory
        cat_config = categories.get(category, {})
        save_dir = cat_config.get('directory', CONFIG.get('papers_dir', Path.cwd()) / 'OTHER' / 'raw')
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        if doi:
            filename = f"{normalize_doi(doi).replace('/', '_').replace(':', '_')}.pdf"
        else:
            filename = f"paper_{i}_{hashlib.md5(title.encode()).hexdigest()[:8]}.pdf"
        
        save_path = save_dir / filename
        
        # Check if already exists
        if save_path.exists():
            log(f"  文件已存在，跳过", "DEBUG")
            continue
        
        # Skip download in dry-run mode
        if no_download:
            log(f"  Dry run: 跳过下载", "DEBUG")
            if category in results:
                results[category]['paywall'] += 1
                results[category]['paywall_papers'].append(paper)
            results['paywall'] += 1
            continue
        
        # Check OA and download
        download_config = CONFIG.get('download', {})
        if download_config.get('auto_download', True):
            is_oa, oa_url = check_open_access(doi)
            
            if is_oa and oa_url:
                success = download_paper(oa_url, save_path, title)
                if success:
                    if category in results:
                        results[category]['downloaded'] += 1
                        results[category]['downloaded_papers'].append(paper)
                    results['downloaded'] += 1
                    continue
            
            # Try PubMed Central
            if download_config.get('prefer_pmc', True) and pmid and str(pmid).isdigit():
                log(f"  尝试从 PubMed Central 下载...")
                success = download_from_pubmed(pmid, save_path)
                if success:
                    if category in results:
                        results[category]['downloaded'] += 1
                        results[category]['downloaded_papers'].append(paper)
                    results['downloaded'] += 1
                    continue
        
        # Paywall
        if category in results:
            results[category]['paywall'] += 1
            results[category]['paywall_papers'].append(paper)
        results['paywall'] += 1
        log(f"  付费墙文献，无法自动下载", "WARNING")
    
    log("")
    
    # Step 5: Generate report
    log("【步骤 5/5】生成报告...")
    report = generate_daily_report(results, dedup_stats)
    
    # Completion
    log("")
    log("=" * 60)
    log("✅ Daily Literature Search Complete!")
    log("=" * 60)
    log(f"📊 总计：{results['total']} 篇 | 下载：{results['downloaded']} 篇 | 付费墙：{results['paywall']} 篇")
    log(f"📄 报告：{REPORT_FILE}")
    log("=" * 60)
    
    return report

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  用户中断执行")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 执行失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
