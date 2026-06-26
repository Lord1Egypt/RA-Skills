#!/usr/bin/env python3
"""
fetch-with-auto-detect.py - 智能URL处理，自动检测PDF并分流

功能:
- 自动检测PDF链接
- arXiv链接自动转为PDF下载
- 普通网页使用Web Fetcher
- 输出统一格式的卡片

用法:
  python fetch-with-auto-detect.py <card_id> <url> [options]

示例:
  python fetch-with-auto-detect.py card-001 "https://arxiv.org/abs/2301.12345" --domain ml
  python fetch-with-auto-detect.py card-002 "https://.../paper.pdf" --domain healthcare
"""

import sys
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional, Dict, Any


def is_pdf_url(url: str) -> bool:
    """检测URL是否为PDF链接"""
    url_lower = url.lower()
    
    # 直接PDF链接
    if url_lower.endswith('.pdf'):
        return True
    
    # arXiv PDF链接
    if 'arxiv.org/pdf/' in url_lower:
        return True
    
    # PMC PDF链接
    if 'ncbi.nlm.nih.gov/pmc/articles/' in url_lower and '/pdf' in url_lower:
        return True
    
    return False


def convert_arxiv_to_pdf(url: str) -> str:
    """将arXiv摘要页转为PDF链接"""
    # abs/2301.12345 -> pdf/2301.12345
    if '/abs/' in url:
        return url.replace('/abs/', '/pdf/')
    return url


def download_pdf(url: str, output_path: Path, timeout: int = 60) -> bool:
    """
    下载PDF文件
    
    Returns:
        下载成功返回True
    """
    try:
        import requests
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        response.raise_for_status()
        
        # 验证是PDF
        content_type = response.headers.get('content-type', '')
        if 'pdf' not in content_type.lower():
            # 检查文件头
            first_bytes = response.raw.read(4)
            response.raw.seek(0)
            if first_bytes != b'%PDF':
                print(f"警告: 下载的内容不是PDF ({content_type})")
        
        # 保存文件
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
        
    except Exception as e:
        print(f"PDF下载失败: {e}")
        return False


def clean_pdf_text(text: str) -> str:
    """清理 PDF 提取文本：修复空格/换行/连字符"""
    import re
    
    # 1. 修复单词粘连（大写字母间加空格）
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', text)
    
    # 2. 修复连字符换行
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    
    # 3. 合并过短行
    lines = text.split('\n')
    cleaned = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            cleaned.append('')
            continue
        if len(line) < 30 and i < len(lines)-1 and not line.endswith(('.', '!', '?', ':', ';')):
            if cleaned and not cleaned[-1].endswith(('.', '!', '?', ':', ';')):
                cleaned[-1] = cleaned[-1] + ' ' + line
            else:
                cleaned.append(line)
        else:
            cleaned.append(line)
    
    # 4. 修复常见粘连词
    text = '\n'.join(cleaned)
    text = re.sub(r'ATTENTIONRESIDUALS', 'ATTENTION RESIDUALS', text)
    text = re.sub(r'TECHNICALREPORT', 'TECHNICAL REPORT', text)
    text = re.sub(r'KimiTeam', 'Kimi Team', text)
    
    return text


def extract_from_pdf(pdf_path: Path, verbose: bool = False) -> Dict[str, Any]:
    """
    从PDF提取文本（带清洗）
    
    Returns:
        提取结果字典
    """
    result = {
        "success": False,
        "title": None,
        "content_text": None,
        "word_count": 0,
        "error": None
    }
    
    try:
        # 尝试使用pdfplumber
        import pdfplumber
        
        with pdfplumber.open(pdf_path) as pdf:
            # 提取标题（第一页顶部文本）
            if pdf.pages:
                first_page = pdf.pages[0]
                text = first_page.extract_text() or ""
                # 清洗文本
                text = clean_pdf_text(text)
                lines = [l.strip() for l in text.split('\n') if l.strip()]
                if lines:
                    result["title"] = lines[0][:200]
            
            # 提取全文
            full_text = []
            for i, page in enumerate(pdf.pages):
                if i > 20:  # 限制页数
                    break
                text = page.extract_text()
                if text:
                    full_text.append(text)
            
            raw_text = "\n".join(full_text)
            # 清洗全文
            result["content_text"] = clean_pdf_text(raw_text)
            result["word_count"] = len(result["content_text"].split())
            result["success"] = True
            
    except ImportError:
        result["error"] = "pdfplumber未安装，请运行: pip install pdfplumber"
    except Exception as e:
        result["error"] = str(e)
    
    return result


def fetch_with_auto_detect(
    card_id: str,
    url: str,
    domain: str = "general",
    timeout: int = 60,
    verbose: bool = False
) -> Optional[Dict[str, Any]]:
    """
    智能抓取，自动检测PDF并分流处理
    
    Returns:
        卡片数据字典
    """
    
    # 检测URL类型
    is_pdf = is_pdf_url(url)
    is_arxiv = 'arxiv.org' in url.lower()
    
    if verbose:
        print(f"[Auto Detect] URL: {url}")
        print(f"[Auto Detect] PDF: {is_pdf}, arXiv: {is_arxiv}")
    
    # arXiv处理
    if is_arxiv and not is_pdf:
        url = convert_arxiv_to_pdf(url)
        is_pdf = True
        if verbose:
            print(f"[Auto Detect] 转换为PDF: {url}")
    
    # PDF处理流程
    if is_pdf:
        return _process_pdf(card_id, url, domain, timeout, verbose)
    else:
        # 网页处理流程
        return _process_web(card_id, url, domain, timeout, verbose)


def _process_pdf(
    card_id: str,
    url: str,
    domain: str,
    timeout: int,
    verbose: bool
) -> Optional[Dict[str, Any]]:
    """处理PDF流程"""
    
    # 创建临时目录
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    pdf_path = temp_dir / f"{card_id}.pdf"
    
    if verbose:
        print(f"[PDF] 下载: {url}")
    
    # 下载PDF
    if not download_pdf(url, pdf_path, timeout):
        return None
    
    if verbose:
        print(f"[PDF] 已下载: {pdf_path} ({pdf_path.stat().st_size} bytes)")
    
    # 提取内容
    extracted = extract_from_pdf(pdf_path, verbose)
    
    if not extracted["success"]:
        print(f"❌ PDF提取失败: {extracted['error']}")
        return None
    
    # 生成卡片
    card = _create_card(
        card_id=card_id,
        url=url,
        source_type="pdf",
        title=extracted.get("title"),
        content_text=extracted.get("content_text"),
        word_count=extracted.get("word_count", 0),
        domain=domain
    )
    
    # 清理临时文件
    pdf_path.unlink(missing_ok=True)
    
    return card


def _process_web(
    card_id: str,
    url: str,
    domain: str,
    timeout: int,
    verbose: bool
) -> Optional[Dict[str, Any]]:
    """处理网页流程"""
    
    # PubMed特殊处理：使用API获取元数据
    if "pubmed.ncbi.nlm.nih.gov" in url.lower():
        pmid_match = re.search(r'/(\d+)', url)
        if pmid_match:
            pmid = pmid_match.group(1)
            if verbose:
                print(f"[PubMed] 使用API获取元数据: PMID {pmid}")
            
            pubmed_meta = fetch_pubmed_api(pmid)
            
            if pubmed_meta.get("title"):
                # 生成PubMed卡片
                card = _create_pubmed_card(
                    card_id=card_id,
                    url=url,
                    pmid=pmid,
                    meta=pubmed_meta,
                    domain=domain
                )
                
                # 保存卡片
                output_dir = Path("sources")
                output_dir.mkdir(exist_ok=True)
                card_file = output_dir / f"{card_id}.json"
                with open(card_file, 'w', encoding='utf-8') as f:
                    json.dump(card, f, indent=2, ensure_ascii=False)
                
                print(f"✅ PubMed卡片生成: {card_file}")
                return card
    
    # 调用fetch-card-from-web
    script_path = Path(__file__).parent / "fetch-card-from-web.py"
    
    cmd = [
        "python3", str(script_path),
        card_id, url,
        "--domain", domain,
        "--timeout", str(timeout)
    ]
    
    if verbose:
        cmd.append("-v")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
        
        if result.returncode != 0:
            print(f"❌ 抓取失败: {result.stderr}")
            return None
        
        # 读取生成的卡片
        card_file = Path("sources") / f"{card_id}.json"
        if card_file.exists():
            with open(card_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print("❌ 卡片文件未生成")
            return None
            
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return None


def parse_arxiv_metadata(text: str, url: str) -> Dict[str, Any]:
    """从 arXiv 论文文本中提取元数据"""
    import re
    meta = {"authors": None, "published_date": None, "arxiv_id": None}
    
    # 提取 arXiv ID
    arxiv_match = re.search(r'arXiv:(\d+\.\d+)', text, re.IGNORECASE)
    if arxiv_match:
        meta["arxiv_id"] = arxiv_match.group(1)
    else:
        url_match = re.search(r'arXiv/(\d+\.\d+)', url, re.IGNORECASE)
        if url_match:
            meta["arxiv_id"] = url_match.group(1)
    
    # 提取日期
    date_patterns = [r'Submitted on (\d{1,2} [A-Za-z]+ \d{4})', r'(\d{4}-\d{2}-\d{2})']
    for pattern in date_patterns:
        date_match = re.search(pattern, text)
        if date_match:
            meta["published_date"] = date_match.group(1)
            break
    
    # 提取作者
    author_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*(?:Team|Group|Lab))', text[:500])
    if author_match:
        meta["authors"] = author_match.group(1).strip()
    
    return meta


def extract_methodology_info(text: str) -> Dict[str, Any]:
    """提取方法类论文的关键信息"""
    import re
    metrics = {}
    text_lower = text.lower()
    
    is_method_paper = any(kw in text_lower[:500] for kw in 
                          ['propose', 'introduce', 'novel', 'method', 'approach'])
    
    if is_method_paper:
        # 提取方法名称
        method_patterns = [
            r'[Ww]e propose[d]?\s+([^,.\n]{5,50}?)(?:\s+\(|,|\.\s|to|for)',
            r'introduce[d]?\s+([^,.\n]{5,50}?)(?:\s+\(|,|\.\s|to|for)',
        ]
        for pattern in method_patterns:
            match = re.search(pattern, text[:2000])
            if match:
                method_name = match.group(1).strip()
                method_name = re.sub(r'^(a |an |the )', '', method_name, flags=re.IGNORECASE)
                if len(method_name) > 3:
                    metrics['method_name'] = method_name
                    break
        
        # 提取关键创新点
        innovation_match = re.search(r'which\s+([^,.]{10,100}?)(?:\.|:|,|\s+and)', text[:3000], re.IGNORECASE)
        if innovation_match:
            metrics['key_innovation'] = innovation_match.group(1).strip()
        
        # 提取对比基线
        baseline_match = re.search(r'compared to\s+([^,.]{5,50}?)(?:\.|,|;)', text[:4000], re.IGNORECASE)
        if baseline_match:
            metrics['baseline'] = baseline_match.group(1).strip()
        
        # 提取适用场景
        app_match = re.search(r'(?:applies? to|for)\s+([^,.]{10,80}?)(?:\.|,|and)', text[:3000], re.IGNORECASE)
        if app_match:
            metrics['application'] = app_match.group(1).strip()
        
        metrics['_paper_type'] = 'methodology'
    
    return metrics


def extract_key_quote(text: str) -> Dict[str, str]:
    """提取关键原文引用"""
    result = {"quote": "", "location": ""}
    if not text:
        return result
    
    # 查找摘要中的关键句
    abstract_match = re.search(r'ABSTRACT\s*\n(.*?)(?:\n\n|\n[A-Z])', text, re.DOTALL | re.IGNORECASE)
    if abstract_match:
        abstract = abstract_match.group(1).strip()
        # 取第一句作为关键引用
        first_sentence = re.split(r'[.!?]\s+', abstract)[0]
        if len(first_sentence) > 20:
            result["quote"] = first_sentence + "."
            result["location"] = "Abstract"
    
    # 如果没找到，查找引言第一句
    if not result["quote"]:
        intro_match = re.search(r'1\s+Introduction\s*\n(.*?)(?:\n\n|\n2\s)', text, re.DOTALL | re.IGNORECASE)
        if intro_match:
            intro = intro_match.group(1).strip()
            first_sentence = re.split(r'[.!?]\s+', intro)[0]
            if len(first_sentence) > 20:
                result["quote"] = first_sentence + "."
                result["location"] = "Introduction, Section 1"
    
    return result


def _create_card(
    card_id: str,
    url: str,
    source_type: str,
    title: Optional[str],
    content_text: Optional[str],
    word_count: int,
    domain: str
) -> Dict[str, Any]:
    """创建标准卡片（集成修复后的逻辑）"""
    
    from datetime import datetime
    
    # 提取arXiv元数据
    arxiv_meta = {}
    if "arxiv.org" in url.lower() and content_text:
        arxiv_meta = parse_arxiv_metadata(content_text[:2000], url)
    
    # 提取方法类指标
    method_info = extract_methodology_info(content_text) if content_text else {}
    
    # 提取关键引用
    key_quote = extract_key_quote(content_text)
    
    # 判断是否有真正的定量指标（数值+单位/统计）
    has_quantitative_metrics = False
    if method_info:
        for key, value in method_info.items():
            if key.startswith('_'):
                continue
            # 检查是否包含数字和单位
            if re.search(r'\d+(\.\d+)?\s*(%|dB|ms|F1|AUC|accuracy|precision|recall)', str(value), re.IGNORECASE):
                has_quantitative_metrics = True
                break
    
    # 判断数据级别（修正后逻辑）
    has_methodology = '_paper_type' in method_info and method_info['_paper_type'] == 'methodology'
    
    if word_count > 2000 and has_quantitative_metrics:
        data_level = "high"
    elif word_count > 500 and (has_quantitative_metrics or has_methodology):
        data_level = "medium"
    else:
        data_level = "low"
    
    # 生成验证建议
    verification_suggestions = []
    if not arxiv_meta.get("published_date"):
        arxiv_id = arxiv_meta.get("arxiv_id") or url.split('/')[-1].replace('.pdf', '')
        verification_suggestions.append(f"发布日期: 访问 https://arxiv.org/abs/{arxiv_id} 查看提交历史")
    if not has_quantitative_metrics and has_methodology:
        verification_suggestions.append("性能指标: 本文未报告性能指标，如需评估效果，建议查看后续引用此工作的论文")
    
    card = {
        "card_id": card_id,
        "created_at": datetime.now().isoformat(),
        "version": "v6.0",
        "source": {
            "type": source_type,
            "url": url,
            "title": title or "Untitled",
            "author": arxiv_meta.get("authors"),
            "published_date": arxiv_meta.get("published_date"),
            "arxiv_id": arxiv_meta.get("arxiv_id"),
            "accessed_at": datetime.now().isoformat()
        },
        "content": {
            "word_count": word_count,
            "data_level": data_level,
            "preview": (content_text or "")[:800] + "..." if content_text and len(content_text) > 800 else (content_text or ""),
            "full_text": content_text[:20000] if content_text else None
        },
        "extracted_metrics": method_info,
        "key_quote": key_quote,
        "quality": {
            "has_full_text": word_count > 500,
            "has_quantitative_metrics": has_quantitative_metrics,
            "paper_type": method_info.get('_paper_type', 'unknown'),
            "credibility": "high" if source_type in ["pdf", "arxiv"] else "medium"
        },
        "verification_status": {
            "data_extracted": True,
            "needs_manual_check": word_count < 500,
            "missing_fields": [],
            "suggestions": verification_suggestions
        },
        "meta": {
            "domain": domain,
            "fetcher_version": "auto-detect-v1.2"
        }
    }
    
    # 检测缺失字段
    if not card["source"]["author"]:
        card["verification_status"]["missing_fields"].append("author")
    if not card["source"]["published_date"]:
        card["verification_status"]["missing_fields"].append("published_date")
    
    # 保存卡片
    output_dir = Path("sources")
    output_dir.mkdir(exist_ok=True)
    
    card_file = output_dir / f"{card_id}.json"
    with open(card_file, 'w', encoding='utf-8') as f:
        json.dump(card, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 卡片生成: {card_file}")
    print(f"   类型: {source_type.upper()}")
    print(f"   字数: {word_count}")
    
    return card


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="智能URL处理，自动检测PDF并分流",
        epilog="""
示例:
  python fetch-with-auto-detect.py card-001 "https://arxiv.org/abs/2301.12345"
  python fetch-with-auto-detect.py card-002 "https://.../paper.pdf" -v
        """
    )
    
    parser.add_argument("card_id", help="卡片ID")
    parser.add_argument("url", help="目标URL")
    parser.add_argument("--domain", "-d", default="general", help="研究领域")
    parser.add_argument("--timeout", "-t", type=int, default=60, help="超时时间")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细日志")
    
    args = parser.parse_args()
    
    card = fetch_with_auto_detect(
        card_id=args.card_id,
        url=args.url,
        domain=args.domain,
        timeout=args.timeout,
        verbose=args.verbose
    )
    
    if card:
        print("\n--- JSON OUTPUT ---")
        print(json.dumps(card, ensure_ascii=False, indent=2))
        sys.exit(0)
    else:
        sys.exit(1)


def _create_pubmed_card(
    card_id: str,
    url: str,
    pmid: str,
    meta: Dict[str, Any],
    domain: str
) -> Dict[str, Any]:
    """创建PubMed专用卡片"""
    from datetime import datetime
    
    abstract = meta.get("abstract", "")
    word_count = len(abstract.split()) if abstract else 0
    
    card = {
        "card_id": card_id,
        "created_at": datetime.now().isoformat(),
        "version": "v6.0",
        "source": {
            "type": "pubmed",
            "url": url,
            "title": meta.get("title") or "Untitled",
            "author": meta.get("authors"),
            "published_date": meta.get("published_date"),
            "pmid": pmid,
            "accessed_at": datetime.now().isoformat()
        },
        "content": {
            "word_count": word_count,
            "data_level": "low",  # PubMed通常只有摘要
            "preview": abstract[:800] + "..." if len(abstract) > 800 else abstract,
            "full_text": abstract,
            "html_available": True
        },
        "extracted_metrics": {
            "_extraction_notes": "PubMed摘要模式",
            "_paper_type": "unknown"
        },
        "key_quote": {
            "quote": abstract[:200] + "..." if len(abstract) > 200 else abstract,
            "location": "PubMed Abstract"
        },
        "quality": {
            "has_full_text": False,
            "has_quantitative_metrics": False,
            "paper_type": "unknown",
            "credibility": "high"  # PubMed来源可信
        },
        "verification_status": {
            "data_extracted": True,
            "needs_manual_check": True,  # 需要人工补充全文
            "missing_fields": [],
            "suggestions": [
                "全文获取: PubMed仅提供摘要，如需全文请查找PMC或期刊官网",
                "定量指标: 摘要中未包含完整定量数据"
            ]
        },
        "meta": {
            "domain": domain,
            "fetcher_version": "pubmed-api-v1.0"
        }
    }
    
    return card


def fetch_pubmed_api(pmid: str) -> Dict[str, Any]:
    """
    使用PubMed E-utilities API获取完整元数据
    """
    import requests
    
    meta = {"authors": None, "published_date": None, "pmid": pmid, "abstract": None}
    
    try:
        # ESummary API
        summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        params = {'db': 'pubmed', 'id': pmid, 'retmode': 'json'}
        
        response = requests.get(summary_url, params=params, timeout=15)
        data = response.json()
        
        if "result" in data and pmid in data["result"]:
            article = data["result"][pmid]
            
            # 提取作者
            authors = article.get("authors", [])
            if authors:
                author_names = [a.get("name", "") for a in authors[:5]]
                meta["authors"] = ", ".join(filter(None, author_names))
            
            # 提取日期
            meta["published_date"] = article.get("pubdate", "")
            meta["title"] = article.get("title", "")
        
        # EFetch API - 获取完整摘要
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {'db': 'pubmed', 'id': pmid, 'retmode': 'xml'}
        
        response = requests.get(fetch_url, params=params, timeout=15)
        xml_text = response.text
        
        # 提取摘要
        abstracts = re.findall(r'<AbstractText[^>]*>([^<]+)</AbstractText>', xml_text)
        if abstracts:
            meta["abstract"] = " ".join(abstracts)
        
    except Exception as e:
        meta["error"] = str(e)
    
    return meta


if __name__ == "__main__":
    main()
