#!/usr/bin/env python3
"""
fetch.py - 获取arxiv指定领域的文章信息

用法: python fetch.py <领域> <保存路径> [日期]
示例: python fetch.py cs.CV ./output 2026-03-19
"""

import sys
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def get_target_date(date_str=None):
    """获取目标日期，如果未指定则返回当天"""
    if date_str:
        # 尝试解析输入的日期格式
        formats = ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).strftime('%a, %d %b %Y')
            except ValueError:
                continue
        raise ValueError(f"无法解析日期: {date_str}，请使用 YYYY-MM-DD 格式")
    else:
        # 返回当天日期，格式如 "Thu, 19 Mar 2026"
        return datetime.now().strftime('%a, %d %b %Y')


def fetch_list_page(category):
    """获取arxiv列表页面"""
    url = f"https://arxiv.org/list/{category}/recent?skip=0&show=2000"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"获取列表页面失败: {e}")
        sys.exit(1)


def parse_date_section(html, target_date):
    """解析指定日期的文章列表"""
    soup = BeautifulSoup(html, 'html.parser')
    
    # 找到所有dl元素
    dls = soup.find_all('dl')
    
    target_dl = None
    for dl in dls:
        # 查找日期标题
        prev_h3 = dl.find('h3')
        if prev_h3:
            date_text = prev_h3.get_text(strip=True)
            # 匹配目标日期，支持多种格式
            if target_date in date_text or match_date_fuzzy(target_date, date_text):
                print(target_date)
                print(date_text)
                target_dl = dl
                break
    
    if not target_dl:
        print(f"未找到日期 {target_date} 的文章")
        return []
    return extract_papers(target_dl)


def match_date_fuzzy(target, found):
    """模糊匹配日期"""
    # 将 "Thu, 19 Mar 2026" 转换为其他可能格式进行匹配
    try:
        dt = datetime.strptime(target, '%a, %d %b %Y')
        # 检查多种格式
        formats = ['%d %b %Y', '%A, %d %B %Y', '%a %d %b %Y']
        for fmt in formats:
            if dt.strftime(fmt) in found:
                return True
    except:
        pass
    return False


def extract_papers(dl_element):
    """从dl元素中提取文章信息"""
    papers = []
    
    # 每个dt对应一个论文条目
    dts = dl_element.find_all('dt')
    dds = dl_element.find_all('dd')
    
    for i, (dt, dd) in enumerate(zip(dts, dds)):
        try:
            # 获取abs链接
            abs_link = dt.find('a', href=re.compile(r'/abs/'))
            if not abs_link:
                continue
            
            arxiv_id = abs_link.get_text(strip=True)
            abs_url = f"https://arxiv.org/abs/{arxiv_id}"
            
            # 获取标题
            title_div = dd.find('div', class_='list-title')
            title = title_div.get_text(strip=True).replace('Title:', '').strip() if title_div else 'N/A'
            
            # 获取comments
            comments_div = dd.find('div', class_='list-comments')
            comment = comments_div.get_text(strip=True).replace('Comments:', '').strip() if comments_div else ''
            
            # 过滤条件：检查comment是否只有 pages/tables/figures
            if not is_valid_comment(comment):
                continue
            
            papers.append({
                'title': title,
                'abs_url': abs_url,
                'comment': comment,
                'arxiv_id': arxiv_id
            })
            
        except Exception as e:
            print(f"解析第{i+1}篇文章时出错: {e}")
            continue
    
    return papers


def is_valid_comment(comment_text):
    """
    检查comment是否有效（不是纯页数/表格/图表统计）
    
    Args:
        comment_text: 评论文本内容
    
    Returns:
        bool: True表示有效，False表示应过滤掉
    """
    if not comment_text:
        return False
    
    comment_text = comment_text.strip()
    
    # 去除常见的连接词和标点后再检查
    cleaned = re.sub(r'[,\.;]', '', comment_text.lower())
    cleaned = re.sub(r'\s+and\s+', ' ', cleaned)
    cleaned = cleaned.strip()
    
    # 检查是否只包含 pages, tables, figures
    words = cleaned.split()
    valid_words = {'pages', 'page', 'tables', 'table', 'figures', 'figure'}
    
    # 如果所有非数字单词都是 pages/tables/figures 相关的，则过滤掉
    non_digit_words = [w for w in words if not w.isdigit()]
    if non_digit_words and all(w in valid_words for w in non_digit_words):
        return False
    
    return True


def fetch_abstract(abs_url):
    """从abs页面获取摘要"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
    }
    
    try:
        response = requests.get(abs_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找abstract
        abstract_block = soup.find('blockquote', class_='abstract')
        if abstract_block:
            # 移除"Abstract:"标签
            abstract_text = abstract_block.get_text(strip=True)
            abstract_text = re.sub(r'^Abstract:\s*', '', abstract_text, flags=re.IGNORECASE)
            return abstract_text
        
        # 备用方案
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            return meta_desc.get('content', 'N/A')
        
        return 'N/A'
        
    except Exception as e:
        print(f"获取摘要失败 {abs_url}: {e}")
        return 'N/A'


def save_to_file(papers, save_path, filename_date, category):
    """保存结果到文件"""
    # 构建文件名: 日期-领域.txt
    filename = f"{filename_date}-{category}.txt"
    filepath = Path(save_path) / filename
    
    # 确保目录存在
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for i, paper in enumerate(papers, 1):
            line = (f"Paper{i:03d}: "
                   f"Title: {paper['title']} "
                   f"Url: {paper['abs_url']} "
                   f"Abstract: {paper['abstract']} "
                   f"Comment: {paper['comment']}\n")
            f.write(line)
    
    print(f"已保存 {len(papers)} 篇文章到: {filepath}")
    return filepath


def main():
    if len(sys.argv) < 3:
        print("用法: python fetch.py <领域> <保存路径> [日期]")
        print("示例: python fetch.py cs.CV ./output 2026-03-19")
        sys.exit(1)
    
    category = sys.argv[1]
    save_path = sys.argv[2]
    date_str = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 获取目标日期（用于匹配页面）
    target_date = get_target_date(date_str)
    print(f"目标日期: {target_date}")
    
    # 获取文件名用的日期格式
    if date_str:
        filename_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
    else:
        filename_date = datetime.now().strftime('%Y-%m-%d')
    
    # 1. 获取列表页面
    print(f"正在获取 {category} 领域的文章列表...")
    html = fetch_list_page(category)
    
    # 2. 解析指定日期的文章
    papers = parse_date_section(html, target_date)
    print(f"找到 {len(papers)} 篇符合条件的文章（过滤后）")
    
    if not papers:
        print("没有符合条件的文章，退出")
        sys.exit(0)
    
    # 3. 获取每篇文章的摘要
    print("正在获取文章摘要...")
    for i, paper in enumerate(papers):
        print(f"  处理 {i+1}/{len(papers)}: {paper['arxiv_id']}")
        paper['abstract'] = fetch_abstract(paper['abs_url'])
        # 每隔3秒请求一次
        if i < len(papers) - 1:  # 最后一个不需要等待
            time.sleep(3)
    
    # 4. 保存结果
    save_to_file(papers, save_path, filename_date, category)
    print("完成！")


if __name__ == '__main__':
    main()
