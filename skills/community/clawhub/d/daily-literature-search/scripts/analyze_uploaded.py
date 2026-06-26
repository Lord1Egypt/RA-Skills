#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传文献自动分析归类脚本
功能：
1. 扫描上传目录的 PDF 文件
2. 基于标题/文件名进行智能分类（B-ALL / MM / OTHER）
3. 提取 DOI（从文件名或内容）
4. 重命名并移动到对应目录
5. 生成归类报告
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

# ==================== 配置 ====================

WORKSPACE = Path.home() / ".openclaw" / "workspace"
PAPERS_DIR = WORKSPACE / "papers"
UPLOAD_DIR = PAPERS_DIR / "upload_temp" / "3_18"
B_ALL_DIR = PAPERS_DIR / "B-ALL" / "raw"
MM_DIR = PAPERS_DIR / "MM" / "raw"
OTHER_DIR = PAPERS_DIR / "OTHER" / "raw"
REPORT_FILE = PAPERS_DIR / "upload_analysis_report.md"

# 确保目标目录存在
for dir_path in [B_ALL_DIR, MM_DIR, OTHER_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# ==================== 分类逻辑 ====================

B_ALL_KEYWORDS = [
    "b-cell acute lymphoblastic leukemia",
    "b-all",
    "b cell acute lymphoblastic",
    "b lymphoblastic leukemia",
    "acute lymphoblastic leukemia",
    "cd19",
    "cd22",
    "blinatumomab",
    "inotuzumab",
    "car-t",
    "cart",
    "tisagenlecleucel",
    "brexucabtagene",
    "ph-positive",
    "ph-negative",
    "philadelphia chromosome"
]

MM_KEYWORDS = [
    "multiple myeloma",
    "myeloma",
    "plasma cell",
    "bcma",
    "gprc5d",
    "fcrh5",
    "elranatamab",
    "teclistamab",
    "talquetamab",
    "daratumumab",
    "isatuximab",
    "pomilidomide",
    "lenalidomide"
]

def classify_by_filename(filename):
    """基于文件名分类"""
    name_lower = filename.lower().replace("_", " ").replace("-", " ")
    
    b_all_score = sum(1 for kw in B_ALL_KEYWORDS if kw in name_lower)
    mm_score = sum(1 for kw in MM_KEYWORDS if kw in name_lower)
    
    if b_all_score > mm_score:
        return "B-ALL", b_all_score
    elif mm_score > b_all_score:
        return "MM", mm_score
    else:
        return "OTHER", 0

def classify_by_title(title):
    """基于标题分类"""
    title_lower = title.lower()
    
    b_all_score = sum(1 for kw in B_ALL_KEYWORDS if kw in title_lower)
    mm_score = sum(1 for kw in MM_KEYWORDS if kw in title_lower)
    
    if b_all_score > mm_score:
        return "B-ALL", b_all_score
    elif mm_score > b_all_score:
        return "MM", mm_score
    else:
        return "OTHER", 0

def extract_doi_from_filename(filename):
    """从文件名提取 DOI"""
    # 匹配 DOI 模式
    doi_pattern = r"10\.\d+[/\w\.\-]+"
    matches = re.findall(doi_pattern, filename, re.IGNORECASE)
    if matches:
        return matches[0]
    
    # 匹配期刊文章编号（如 cancers-18-00740）
    journal_pattern = r"([a-z]+)-(\d+)-(\d+)"
    match = re.search(journal_pattern, filename.lower())
    if match:
        journal = match.group(1)
        vol = match.group(2)
        page = match.group(3)
        # 常见期刊 DOI 格式
        doi_map = {
            "cancers": f"10.3390/cancers{vol}{page}",
            "jnccn": f"10.6004/jnccn.{vol}.{page}",
        }
        if journal in doi_map:
            return doi_map[journal]
    
    return None

def safe_filename(title, doi=None):
    """生成安全的文件名"""
    if doi:
        # 使用 DOI 作为文件名
        safe_doi = doi.replace("/", "_").replace(":", "_")
        return f"{safe_doi}.pdf"
    else:
        # 使用标题前 50 字符
        safe_title = re.sub(r'[^\w\s\-]', '', title[:50]).strip().replace(" ", "_")
        return f"{safe_title}.pdf"

# ==================== 主处理流程 ====================

def analyze_uploaded_papers():
    """分析并归类上传的文献"""
    
    print("=" * 60)
    print("📚 上传文献自动分析归类系统")
    print("=" * 60)
    print(f"上传目录：{UPLOAD_DIR}")
    print(f"分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    if not UPLOAD_DIR.exists():
        print(f"❌ 上传目录不存在：{UPLOAD_DIR}")
        return
    
    # 获取所有 PDF 文件
    pdf_files = list(UPLOAD_DIR.glob("*.pdf"))
    total_files = len(pdf_files)
    
    if total_files == 0:
        print("⚠️  未找到 PDF 文件")
        return
    
    print(f"📁 找到 {total_files} 篇 PDF 文献")
    print()
    
    # 统计
    results = {
        "B-ALL": {"count": 0, "papers": []},
        "MM": {"count": 0, "papers": []},
        "OTHER": {"count": 0, "papers": []}
    }
    
    # 处理每个文件
    for i, pdf_path in enumerate(pdf_files, 1):
        filename = pdf_path.name
        print(f"[{i}/{total_files}] 处理：{filename[:60]}...")
        
        # 1. 分类
        category, score = classify_by_filename(filename)
        
        # 2. 提取 DOI
        doi = extract_doi_from_filename(filename)
        
        # 3. 确定目标目录
        if category == "B-ALL":
            target_dir = B_ALL_DIR
        elif category == "MM":
            target_dir = MM_DIR
        else:
            target_dir = OTHER_DIR
        
        # 4. 生成新文件名
        if doi:
            new_filename = f"{doi.replace('/', '_').replace(':', '_')}.pdf"
        else:
            # 使用原标题，清理特殊字符
            clean_name = re.sub(r'[^\w\s\-\.\(\)]', '', filename)
            new_filename = clean_name
        
        # 5. 检查是否已存在
        target_path = target_dir / new_filename
        if target_path.exists():
            print(f"  ⚠️  文件已存在，跳过：{new_filename}")
            continue
        
        # 6. 复制文件
        shutil.copy2(pdf_path, target_path)
        
        # 7. 记录
        results[category]["count"] += 1
        results[category]["papers"].append({
            "original": filename,
            "new": new_filename,
            "doi": doi,
            "target": str(target_dir)
        })
        
        print(f"  ✓ 归类：{category} | DOI: {doi or '无'} | 新文件名：{new_filename[:40]}...")
    
    # 生成报告
    print()
    print("=" * 60)
    print("✅ 归类完成！")
    print("=" * 60)
    print()
    print("📊 统计结果：")
    print(f"  📑 B-ALL: {results['B-ALL']['count']} 篇")
    print(f"  📑 MM: {results['MM']['count']} 篇")
    print(f"  📑 OTHER: {results['OTHER']['count']} 篇")
    print(f"  📊 总计：{sum(r['count'] for r in results.values())} 篇")
    print()
    
    # 生成 Markdown 报告
    generate_report(results)
    
    return results

def generate_report(results):
    """生成归类报告"""
    
    report = []
    report.append("# 📚 上传文献归类报告")
    report.append(f"**处理时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**上传目录：** `upload_temp/3_18/`")
    report.append("")
    
    # 汇总
    report.append("## 📊 归类统计")
    report.append("")
    report.append("| 分类 | 数量 | 占比 |")
    report.append("|------|------|------|")
    total = sum(r["count"] for r in results.values())
    for cat in ["B-ALL", "MM", "OTHER"]:
        count = results[cat]["count"]
        pct = f"{count/total*100:.1f}%" if total > 0 else "0%"
        report.append(f"| {cat} | {count} | {pct} |")
    report.append(f"| **总计** | **{total}** | **100%** |")
    report.append("")
    
    # 详细列表
    for category in ["B-ALL", "MM", "OTHER"]:
        if results[category]["papers"]:
            report.append(f"## {category} 文献")
            report.append("")
            report.append("| 原文件名 | 新文件名 | DOI |")
            report.append("|----------|----------|-----|")
            for paper in results[category]["papers"]:
                orig = paper["original"][:40] + "..." if len(paper["original"]) > 40 else paper["original"]
                new = paper["new"][:35] + "..." if len(paper["new"]) > 35 else paper["new"]
                doi = paper["doi"] or "-"
                report.append(f"| {orig} | {new} | {doi} |")
            report.append("")
    
    # 保存报告
    report_text = "\n".join(report)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_text)
    
    print(f"📝 报告已生成：{REPORT_FILE}")

if __name__ == "__main__":
    analyze_uploaded_papers()
