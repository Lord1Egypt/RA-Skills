#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度学术高级科研助手 V6.0
功能：搜索、按引用排序、PDF下载、工作总结+创新点、模型图显示
新增：按论文方向创建文件夹、规范命名、桌面papers目录
"""

import os
import re
import sys
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# ========== 配置 ==========
# 桌面papers目录
DESKTOP_DIR = os.path.expanduser("~/Desktop/papers")
os.makedirs(DESKTOP_DIR, exist_ok=True)

# 固定User-Agent
DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def get_headers():
    """获取请求头"""
    return {
        "User-Agent": DEFAULT_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Referer": "https://xueshu.baidu.com/"
    }

def clean_filename(title):
    """清理文件名，移除非法字符"""
    title = re.sub(r'[\\/*?:"<>|]', "", title)
    title = title.replace('\n', ' ').strip()
    return title[:80]

def get_paper_type(source):
    """判断论文类型：J=期刊，C=会议"""
    if not source:
        return "J"
    source_lower = source.lower()
    # 会议特征
    if any(kw in source_lower for kw in ["会议", "conference", "proceedings", "proc", "symposium", "workshop"]):
        return "C"
    # 期刊特征
    if any(kw in source_lower for kw in ["journal", "学报", "期刊", "trans", "transactions", "letters"]):
        return "J"
    return "J"

def download_pdf(url, title, year, source, save_dir):
    """下载PDF到指定目录"""
    if not url:
        return None
    try:
        time.sleep(random.uniform(0.5, 1.5))
        
        paper_type = get_paper_type(source)
        filename = f"{clean_filename(title)}_{year}_{paper_type}.pdf"
        path = os.path.join(save_dir, filename)
        
        # 如果已存在，跳过下载
        if os.path.exists(path) and os.path.getsize(path) > 5000:
            return filename
        
        headers = get_headers()
        resp = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
        
        if resp.status_code == 200 and len(resp.content) > 5000:
            with open(path, "wb") as f:
                f.write(resp.content)
            return filename
    except Exception as e:
        pass
    return None

def extract_abstract(paper_url):
    """进入详情页提取摘要"""
    if not paper_url:
        return None
    try:
        headers = get_headers()
        resp = requests.get(paper_url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 尝试多种摘要选择器
        abstract_tag = (
            soup.select_one(".abstract") or 
            soup.select_one(".detail-content") or
            soup.select_one("div[data-click*='abstract']") or
            soup.select_one(".kw_main") or
            soup.select_one(".article_abstract")
        )
        if abstract_tag:
            text = abstract_tag.get_text(strip=True)
            # 清理多余空白
            text = re.sub(r'\s+', ' ', text)
            return text
    except:
        pass
    return None

def extract_model_image(paper_url):
    """从详情页提取模型图"""
    if not paper_url:
        return None
    try:
        headers = get_headers()
        resp = requests.get(paper_url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 查找模型相关的图片
        img_selectors = [
            "img[src*='model']",
            "img[src*='framework']",
            "img[src*='architecture']",
            ".figure img",
            ".model-img img",
            "img[alt*='模型']",
            "img[alt*='框架']"
        ]
        
        for selector in img_selectors:
            img = soup.select_one(selector)
            if img:
                src = img.get("src", "")
                if src:
                    if src.startswith("//"):
                        src = "https:" + src
                    elif not src.startswith("http"):
                        src = "https://xueshu.baidu.com" + src
                    return src
    except:
        pass
    return None

def extract_work_and_innovation(abstract):
    """从摘要提取核心工作和创新点（简洁版）"""
    if not abstract:
        return "（需查看原文）", "（需查看原文）"
    
    # 清理摘要
    abstract = abstract.replace('\n', ' ').strip()
    
    # 按句子分割
    sentences = re.split(r'(?<=[。！？.!?])\s*', abstract)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    if len(sentences) >= 3:
        # 前1-2句通常是背景和核心工作
        work = sentences[0]
        if len(sentences) > 1 and not work.endswith(('提出', '提出了一种', '本文')):
            work = sentences[0] + " " + sentences[1]
        work = work[:150] + "..." if len(work) > 150 else work
        
        # 最后几句通常是贡献和创新
        innovation = sentences[-1]
        if len(sentences) > 2:
            # 查找包含"贡献"、"提出"、"创新"等关键词的句子
            for s in reversed(sentences):
                if any(kw in s for kw in ['贡献', '创新', '提出', '改进', '新方法', '首次']):
                    innovation = s
                    break
        innovation = innovation[:150] + "..." if len(innovation) > 150 else innovation
        
    elif len(sentences) >= 2:
        work = sentences[0]
        innovation = sentences[-1]
    else:
        work = abstract[:150] + "..." if len(abstract) > 150 else abstract
        innovation = work
    
    return work, innovation

def search_baidu_xueshu(keyword, year=None, max_results=10):
    """搜索百度学术"""
    print(f"\n{'='*70}")
    print(f"🔍 百度学术搜索：{keyword}" + (f" | 年份：{year}" if year else ""))
    print(f"{'='*70}\n")
    
    # 构建URL（按引用量排序）
    url = f"https://xueshu.baidu.com/s?wd={quote(keyword)}&sort=sc_cite"
    if year:
        url += f"&y={year}"
    
    papers = []
    
    try:
        print("📡 正在请求百度学术...")
        headers = get_headers()
        resp = requests.get(url, headers=headers, timeout=20)
        
        # 检查验证码
        if "captcha" in resp.url or "验证" in resp.text[:500]:
            print("⚠️  触发验证码拦截")
            print(f"\n🔗 请手动访问：{url}")
            return []
        
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 解析论文列表
        items = soup.select(".res-item")
        if not items:
            items = soup.select(".result")
        
        print(f"📊 找到 {len(items)} 条结果\n")
        
        for item in items:
            try:
                # 提取标题
                title_tag = item.select_one(".res-title a") or item.select_one("h3 a")
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True)
                
                # 提取链接
                link = title_tag.get("href", "")
                if link and not link.startswith("http"):
                    link = "https://xueshu.baidu.com" + link
                
                # 提取作者
                author_tag = item.select_one(".author_text") or item.select_one(".author")
                author = author_tag.get_text(strip=True) if author_tag else "未知作者"
                # 只保留前3位作者
                if len(author) > 30:
                    author = author[:30] + "..."
                
                # 提取来源
                source_tag = item.select_one(".src") or item.select_one(".source")
                source = source_tag.get_text(strip=True) if source_tag else "未知来源"
                
                # 提取年份
                year_tag = item.select_one(".year")
                year_text = year_tag.get_text(strip=True) if year_tag else "未知"
                
                # 提取引用量
                cite = 0
                cite_tag = item.select_one(".sc_cite")
                if cite_tag:
                    m = re.search(r"\d+", cite_tag.get_text())
                    if m:
                        cite = int(m.group())
                
                # 提取PDF链接
                pdf_url = None
                dl = item.select_one(".download a")
                if dl:
                    pdf_url = dl.get("href", "")
                    if pdf_url:
                        if pdf_url.startswith("//"):
                            pdf_url = "https:" + pdf_url
                        elif not pdf_url.startswith("http"):
                            pdf_url = "https://xueshu.baidu.com" + pdf_url
                
                # 提取缩略图（可能是模型图）
                img_tag = item.select_one("img.res_img") or item.select_one("img[src*='model']")
                img_url = img_tag.get("src", "") if img_tag else None
                if img_url and img_url.startswith("//"):
                    img_url = "https:" + img_url
                
                papers.append({
                    "title": title,
                    "author": author,
                    "source": source,
                    "year": year_text,
                    "cite": cite,
                    "pdf": pdf_url,
                    "img": img_url,
                    "link": link
                })
                
            except Exception as e:
                continue
        
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return []
    
    # 按引用量排序（从高到低）
    papers = sorted(papers, key=lambda x: x["cite"], reverse=True)
    
    # 限制结果数量
    papers = papers[:max_results]
    
    if not papers:
        print("❌ 未获取到论文数据")
        return []
    
    # 创建保存目录（以关键词命名）
    folder_name = clean_filename(keyword)
    save_dir = os.path.join(DESKTOP_DIR, folder_name)
    os.makedirs(save_dir, exist_ok=True)
    print(f"📂 PDF保存目录：{save_dir}\n")
    
    # 输出结果
    print(f"{'='*70}")
    print(f"📚 搜索结果（按引用量排序，共{len(papers)}篇）")
    print(f"{'='*70}\n")
    
    downloaded_count = 0
    
    for idx, p in enumerate(papers):
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📄 【{idx+1}】引用量：⭐{p['cite']}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📌 标题：{p['title']}")
        print(f"👥 作者：{p['author']}")
        print(f"📚 来源：{p['source']} | {p['year']}")
        print(f"🔗 链接：{p['link']}")
        
        # 提取摘要并分析
        print(f"\n📖 正在分析论文...")
        abstract = extract_abstract(p['link'])
        work, innovation = extract_work_and_innovation(abstract)
        
        print(f"\n🧠 【核心工作】")
        print(f"   {work}")
        print(f"\n💡 【创新点】")
        print(f"   {innovation}")
        
        # 显示模型图
        if p['img']:
            print(f"\n🖼️ 【模型图】")
            print(f"   {p['img']}")
        else:
            # 尝试从详情页提取模型图
            model_img = extract_model_image(p['link'])
            if model_img:
                print(f"\n🖼️ 【模型图】")
                print(f"   {model_img}")
        
        # 下载PDF
        print(f"\n⬇️  正在下载PDF...")
        pdf_name = download_pdf(p['pdf'], p['title'], p['year'], p['source'], save_dir)
        if pdf_name:
            print(f"✅ 已下载：{pdf_name}")
            downloaded_count += 1
        elif p['pdf']:
            print(f"⚠️  下载失败，手动下载：{p['pdf']}")
        else:
            print(f"⚠️  无PDF链接")
        
        print()
    
    # 汇总
    print(f"\n{'='*70}")
    print(f"✅ 搜索完成！")
    print(f"📊 共找到 {len(papers)} 篇论文，成功下载 {downloaded_count} 篇PDF")
    print(f"📂 PDF保存位置：{save_dir}")
    print(f"{'='*70}\n")
    
    return papers


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║           百度学术科研助手 V6.0                                   ║
╚══════════════════════════════════════════════════════════════════╝

使用方法：
  python main.py <关键词> [年份]

示例：
  python main.py 大模型
  python main.py 人工智能 2026
  python main.py transformer

功能：
  ✅ 按引用量排序（高引用在前）
  ✅ 自动提取核心工作和创新点
  ✅ 显示模型图（如有）
  ✅ 自动下载PDF到 ~/Desktop/papers/<关键词>/
  ✅ PDF命名：标题_年份_J/C.pdf
""")
        sys.exit(1)
    
    keyword = sys.argv[1]
    year = sys.argv[2] if len(sys.argv) >= 3 else None
    
    search_baidu_xueshu(keyword, year)
