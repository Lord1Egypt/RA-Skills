#!/usr/bin/env python3
"""
fetch-card-from-web.py - 从网页URL生成深度研究v6.0卡片

用法: python fetch-card-from-web.py <card_id> <url> [options]

示例:
  python fetch-card-from-web.py card-web-001 "https://www.mckinsey.com/..." --domain healthcare
  python fetch-card-from-web.py card-arxiv-001 "https://arxiv.org/abs/2301.12345" --domain ml -v
"""

import sys
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """清理文本，生成安全的文件名片段"""
    # 移除非法字符
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    # 替换空格和特殊字符
    text = re.sub(r'\s+', '_', text)
    # 截断
    return text[:max_length].strip('_')


def fetch_and_create_card(
    card_id: str, 
    url: str, 
    domain: str = "general",
    timeout: int = 60,
    retries: int = 3,
    verbose: bool = False
) -> Optional[Dict[str, Any]]:
    """
    抓取网页并生成深度研究v6.0格式的卡片
    
    Args:
        card_id: 卡片ID
        url: 目标URL
        domain: 领域
        timeout: 超时时间
        retries: 重试次数
        verbose: 详细日志
    
    Returns:
        卡片数据字典，失败返回None
    """
    
    # 获取web-fetcher脚本路径
    web_fetcher_script = Path(__file__).parent.parent.parent / "web-fetcher" / "scripts" / "web-fetcher.py"
    
    if not web_fetcher_script.exists():
        # 尝试相对路径
        web_fetcher_script = Path("../web-fetcher/scripts/web-fetcher.py")
    
    if not web_fetcher_script.exists():
        print(f"❌ 错误: 找不到web-fetcher脚本: {web_fetcher_script}")
        return None
    
    if verbose:
        print(f"[Fetch Card] 使用Web Fetcher: {web_fetcher_script}")
        print(f"[Fetch Card] 开始抓取: {url}")
    
    # 1. 调用web-fetcher抓取
    cmd = [
        "python3", str(web_fetcher_script),
        url,
        "--domain", domain,
        "--timeout", str(timeout),
        "--retries", str(retries)
    ]
    
    if verbose:
        cmd.append("-v")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout * retries + 30  # 总超时 = 单次超时×重试 + 缓冲
        )
        
        if result.returncode != 0:
            print(f"❌ Web Fetcher执行失败: {result.stderr}")
            return None
        
        fetched = json.loads(result.stdout)
        
    except subprocess.TimeoutExpired:
        print(f"❌ 抓取超时（总时间超过{timeout * retries + 30}秒）")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ 解析Web Fetcher输出失败: {e}")
        print(f"   输出: {result.stdout[:500]}")
        return None
    except Exception as e:
        print(f"❌ 执行Web Fetcher时出错: {e}")
        return None
    
    if not fetched.get("success"):
        print(f"❌ 抓取失败: {fetched.get('error', '未知错误')}")
        return None
    
    if verbose:
        print(f"[Fetch Card] ✅ 抓取成功，字数: {fetched.get('word_count', 0)}")
    
    # 2. 生成v6.0格式的卡片
    word_count = fetched.get("word_count", 0)
    content_text = fetched.get("content_text", "")
    extracted_metrics = fetched.get("extracted_metrics", {})
    
    # 判断数据级别（修正逻辑）
    # high: 有全文 + 有定量指标（数值/统计）
    # medium: 有全文 + 方法描述完整（但无量化指标）
    # low: 仅摘要或字数不足
    has_quantitative = any(k in extracted_metrics for k in 
                          ['sample_size', 'auc', 'accuracy', 'f1_score', 'precision', 'recall'])
    has_methodology = '_paper_type' in extracted_metrics and extracted_metrics['_paper_type'] == 'methodology'
    
    if word_count > 2000 and has_quantitative:
        data_level = "high"  # 有全文 + 定量数据
    elif word_count > 500 and (has_quantitative or has_methodology):
        data_level = "medium"  # 有全文 + 方法描述（但无量化指标）
    elif word_count > 500:
        data_level = "medium"  # 有全文但提取信息有限
    else:
        data_level = "low"  # 仅摘要或内容不足
    
    # 确定来源类型
    url_lower = url.lower()
    if "arxiv.org" in url_lower:
        source_type = "arxiv"
    elif "pubmed" in url_lower or "ncbi.nlm.nih.gov" in url_lower:
        source_type = "pubmed"
    elif ".pdf" in url_lower:
        source_type = "pdf"
    else:
        source_type = "web"
    
    # 提取核心结论（前500字作为preview）
    content_preview = content_text[:800].strip()
    if len(content_text) > 800:
        content_preview += "..."
    
    # 构建卡片
    card = {
        # 基础信息
        "card_id": card_id,
        "created_at": datetime.now().isoformat(),
        "version": "v6.0",
        
        # 来源信息
        "source": {
            "type": source_type,
            "url": url,
            "title": fetched.get("title") or "Untitled",
            "author": fetched.get("author"),
            "published_date": fetched.get("published_date"),
            "accessed_at": datetime.now().isoformat()
        },
        
        # 内容信息
        "content": {
            "word_count": word_count,
            "data_level": data_level,  # high/medium/low
            "preview": content_preview,
            "full_text": content_text[:20000] if word_count > 0 else None,  # 限制20KB
            "html_available": fetched.get("content_html") is not None
        },
        
        # 提取的指标
        "extracted_metrics": fetched.get("extracted_metrics", {}),
        
        # 研究质量评估
        "quality": {
            "has_full_text": word_count > 500,
            "has_metrics": len(fetched.get("extracted_metrics", {})) > 0,
            "has_sample_size": "sample_size" in fetched.get("extracted_metrics", {}),
            "credibility": "high" if source_type in ["arxiv", "pubmed", "pdf"] else "medium"
        },
        
        # 待验证标记（v6.0诚实度）
        "verification_status": {
            "data_extracted": True,
            "needs_manual_check": word_count < 500,
            "missing_fields": []
        },
        
        # 元数据
        "meta": {
            "domain": domain,
            "retries_used": fetched.get("retries_used", 0),
            "fetcher_version": "1.1"
        }
    }
    
    # 检测缺失字段
    if not card["source"]["author"]:
        card["verification_status"]["missing_fields"].append("author")
    if not card["source"]["published_date"]:
        card["verification_status"]["missing_fields"].append("published_date")
    if not card["extracted_metrics"]:
        card["verification_status"]["missing_fields"].append("quantitative_data")
    
    # 3. 保存卡片
    output_dir = Path("sources")
    output_dir.mkdir(exist_ok=True)
    
    card_file = output_dir / f"{card_id}.json"
    with open(card_file, 'w', encoding='utf-8') as f:
        json.dump(card, f, indent=2, ensure_ascii=False)
    
    # 4. 输出生成摘要
    print(f"\n✅ 卡片生成成功!")
    print(f"   文件: {card_file}")
    print(f"   标题: {card['source']['title'][:60]}...")
    print(f"   来源: {source_type.upper()}")
    print(f"   字数: {word_count}")
    print(f"   数据级别: {data_level.upper()}")
    print(f"   提取指标: {list(card['extracted_metrics'].keys()) or '无'}")
    
    if card["verification_status"]["missing_fields"]:
        print(f"   ⚠️  缺失字段: {', '.join(card['verification_status']['missing_fields'])}")
    
    return card


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="从网页URL生成深度研究v6.0卡片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础用法
  python fetch-card-from-web.py card-web-001 "https://www.mckinsey.com/..."
  
  # 指定领域
  python fetch-card-from-web.py card-001 "https://..." --domain healthcare -v
  
  # 增加超时（海外网站）
  python fetch-card-from-web.py card-001 "https://..." --timeout 90 --retries 5
        """
    )
    
    parser.add_argument("card_id", help="卡片ID (如: card-web-001)")
    parser.add_argument("url", help="目标URL")
    parser.add_argument("--domain", "-d", default="general",
                       help="研究领域 (default: general)")
    parser.add_argument("--timeout", "-t", type=int, default=60,
                       help="超时时间（秒）(default: 60)")
    parser.add_argument("--retries", "-r", type=int, default=3,
                       help="重试次数 (default: 3)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="详细日志")
    
    args = parser.parse_args()
    
    card = fetch_and_create_card(
        card_id=args.card_id,
        url=args.url,
        domain=args.domain,
        timeout=args.timeout,
        retries=args.retries,
        verbose=args.verbose
    )
    
    if card:
        # 同时输出JSON到stdout（便于管道使用）
        print("\n--- JSON OUTPUT ---")
        print(json.dumps(card, ensure_ascii=False, indent=2))
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
