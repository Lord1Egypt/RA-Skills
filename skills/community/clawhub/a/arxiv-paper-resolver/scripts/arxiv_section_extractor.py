#!/usr/bin/env python3
"""
arXiv 论文章节提取器

可复用脚本：接收 arXiv ID，自动提取论文信息、下载 PDF、解析 HTML 全文章节结构

用法:
  python arxiv_section_extractor.py <arxiv_id>
  python arxiv_section_extractor.py <arxiv_id> -o ~/papers

输出目录:
  {output_dir}/{paper-title-slug}/
    ├── {arxiv_id}.pdf                  ← 原始 PDF
    ├── {arxiv_id}_raw_sections/        ← 原始章节文件（供翻译用）
    │   ├── 00_abstract.txt
    │   ├── 01_introduction.txt
    │   └── ...
    ├── {arxiv_id}_metadata.json        ← 论文元数据
    └── {arxiv_id}_section_structure.txt ← 章节层级结构

依赖: requests, beautifulsoup4
"""

import requests
import re
import os
import sys
import json
import argparse
from bs4 import BeautifulSoup


def sanitize_title(title):
    """将论文标题转为安全的目录名"""
    name = title.lower()
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    name = re.sub(r'\s+', '-', name.strip())
    name = re.sub(r'-+', '-', name)
    return name[:80].rstrip('-')


def fetch_page(url, timeout=30):
    """安全地获取页面内容"""
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def extract_arxiv_id(raw_input):
    """从 URL 或裸 ID 中提取 arxiv_id"""
    raw_input = raw_input.strip()
    m = re.search(r'arxiv\.org/abs/(\d+\.\d+)', raw_input)
    if m:
        return m.group(1)
    m = re.search(r'arxiv\.org/html/(\d+\.\d+)', raw_input)
    if m:
        return m.group(1)
    m = re.match(r'(\d+\.\d+)', raw_input)
    if m:
        return m.group(1)
    return None


def get_paper_info_from_abs(arxiv_id):
    """从 abs 页面获取论文标题和 Access Paper 链接"""
    abs_url = f"https://arxiv.org/abs/{arxiv_id}"
    html = fetch_page(abs_url)
    soup = BeautifulSoup(html, 'html.parser')

    # 提取标题
    title_el = soup.find('h1', class_='title')
    paper_title = ""
    if title_el:
        paper_title = title_el.get_text().strip()
        paper_title = re.sub(r'^Title:\s*', '', paper_title, flags=re.IGNORECASE)

    # 提取 Access Paper 的三个链接
    links = {'pdf': '', 'html': '', 'tex': ''}

    pdf_link = soup.find('a', {'class': 'download-pdf'})
    if pdf_link and pdf_link.get('href'):
        href = pdf_link['href']
        links['pdf'] = f"https://arxiv.org{href}" if href.startswith('/') else href

    html_link = soup.find('a', {'id': 'latexml-download-link'})
    if html_link and html_link.get('href'):
        links['html'] = html_link['href']

    tex_link = soup.find('a', {'class': 'download-eprint'})
    if tex_link and tex_link.get('href'):
        href = tex_link['href']
        links['tex'] = f"https://arxiv.org{href}" if href.startswith('/') else href

    return paper_title, links


def fetch_html_content(arxiv_id):
    """获取 HTML 实验版全文，自动尝试 v1 和无后缀"""
    urls_to_try = [
        f"https://arxiv.org/html/{arxiv_id}v1",
        f"https://arxiv.org/html/{arxiv_id}"
    ]
    for url in urls_to_try:
        try:
            html = fetch_page(url)
            print(f"  HTML 获取成功: {url} ({len(html)} 字符)")
            return html, url
        except Exception as e:
            print(f"  尝试 {url} 失败: {e}")
    return None, None


def extract_sections_from_html(html_content, html_url):
    """从 HTML 实验版中提取所有章节及内容"""
    soup = BeautifulSoup(html_content, 'html.parser')

    result = {
        'title': '',
        'authors': '',
        'abstract': '',
        'arxiv_info': '',
        'sections': []
    }

    # 获取标题
    title_el = soup.find('h1', class_='ltx_title_document')
    if not title_el:
        title_el = soup.find('h1')
    if title_el:
        result['title'] = title_el.get_text().strip()

    # 获取作者
    authors_el = soup.find('div', class_='ltx_authors')
    if authors_el:
        authors_text = authors_el.get_text().strip()
        authors_text = re.sub(r'[\u2070-\u2079\u00b2\u00b3\u00b9]+', '', authors_text)
        authors_text = re.sub(r'\s+', ' ', authors_text).strip()
        result['authors'] = authors_text

    # 获取摘要
    abstract_el = soup.find('div', id='abstract1')
    if not abstract_el:
        abstract_el = soup.find('blockquote', class_='abstract')
    if abstract_el:
        abstract_text = abstract_el.get_text().strip()
        abstract_text = re.sub(r'^Abstract[:\\s]*', '', abstract_text, flags=re.IGNORECASE)
        result['abstract'] = abstract_text

    # 从页脚获取 arXiv 信息
    body_text = soup.get_text()
    arxiv_id_match = re.search(
        r'arXiv:\s*[\d\.]+v?\d*\s*\[[^\]]+\]\s*\d+\s+\w+\s+\d{4}',
        body_text
    )
    if arxiv_id_match:
        result['arxiv_info'] = arxiv_id_match.group(0).strip()

    # 提取各 h2 章节
    h2_tags = soup.find_all('h2')

    for h2 in h2_tags:
        h2_text = h2.get_text(strip=True)

        # 跳过 References 和附录
        skip_keywords = ['References', 'references', 'Instructions for reporting',
                         'Acknowledgments', 'acknowledgements', 'Appendix', 'appendix',
                         'Supplementary', 'supplementary']
        if any(kw in h2_text for kw in skip_keywords):
            break

        # 提取 h2 后的所有内容
        content_parts = []
        sub_sections = []

        for sibling in h2.find_next_siblings():
            if sibling.name == 'h2':
                break
            if sibling.name == 'h3':
                sub_title = sibling.get_text(strip=True)
                sub_content = []
                for sub_sib in sibling.find_next_siblings():
                    if sub_sib.name in ['h2', 'h3']:
                        break
                    txt = sub_sib.get_text(strip=True)
                    if txt:
                        sub_content.append(txt)
                sub_sections.append({
                    'title': sub_title,
                    'content': '\n\n'.join(sub_content)
                })
                continue

            txt = sibling.get_text(strip=True)
            if txt:
                content_parts.append(txt)

        full_content = '\n\n'.join(content_parts)
        if len(full_content) < 50:
            continue

        # 确定章节编号
        section_num = ""
        section_name = h2_text
        num_match = re.match(r'(\d+)\.?\s*(.*)', h2_text)
        if num_match:
            section_num = num_match.group(1)
            section_name = num_match.group(2).strip() or section_name

        result['sections'].append({
            'heading': h2_text,
            'content': full_content,
            'number': section_num,
            'subsections': sub_sections
        })

    return result


def save_section_files(paper_dir, arxiv_id, parsed):
    """将提取的章节保存为独立文件"""
    sections_dir = os.path.join(paper_dir, f"{arxiv_id}_raw_sections")
    os.makedirs(sections_dir, exist_ok=True)

    saved_files = []

    # 保存摘要
    if parsed['abstract']:
        meta_file = os.path.join(sections_dir, "00_abstract.txt")
        with open(meta_file, 'w', encoding='utf-8') as f:
            f.write(parsed['abstract'])
        saved_files.append(meta_file)

    # 保存每个章节
    for sec in parsed['sections']:
        idx = parsed['sections'].index(sec)
        heading = sec['heading']
        safe_name = re.sub(r'[^\w\s-]', '', heading).strip()
        safe_name = re.sub(r'\s+', '_', safe_name)[:50]
        filename = f"{idx+1:02d}_{safe_name}.txt"

        filepath = os.path.join(sections_dir, filename)

        content = f"# {heading}\n\n{sec['content']}"

        for sub in sec.get('subsections', []):
            content += f"\n\n### {sub['title']}\n\n{sub['content']}"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        saved_files.append(filepath)
        print(f"  章节已保存: {filename} ({len(content)} 字符)")

    # 保存章节结构总览
    struct_lines = [f"论文标题: {parsed['title']}"]
    struct_lines.append(f"章节数: {len(parsed['sections'])}")
    struct_lines.append("")
    for i, sec in enumerate(parsed['sections'], 1):
        struct_lines.append(f"  {i}. {sec['heading']}")
        for sub in sec.get('subsections', []):
            struct_lines.append(f"     - {sub['title']}")

    struct_path = os.path.join(paper_dir, f"{arxiv_id}_section_structure.txt")
    with open(struct_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(struct_lines))

    saved_files.append(struct_path)
    return saved_files


def main():
    parser = argparse.ArgumentParser(description='arXiv 论文章节提取器')
    parser.add_argument('input', help='arXiv ID 或 URL（如 2604.25836 或 https://arxiv.org/abs/2604.25836）')
    parser.add_argument('-o', '--output-dir',
                        default=os.environ.get('ARXIV_PAPERS_DIR', os.path.join(os.path.expanduser('~'), 'papers')),
                        help='论文输出根目录（默认: ~/papers/，可设置 ARXIV_PAPERS_DIR 环境变量）')
    args = parser.parse_args()

    raw_input = args.input
    arxiv_id = extract_arxiv_id(raw_input)
    if not arxiv_id:
        print(f"错误: 无法从 '{raw_input}' 中提取 arXiv ID")
        sys.exit(1)

    print("=" * 60)
    print(f"arXiv 论文提取器")
    print(f"论文 ID: {arxiv_id}")
    print("=" * 60)

    # 步骤 1: 获取 abs 页面信息
    print("\n[1/5] 获取论文信息...")
    paper_title, access_links = get_paper_info_from_abs(arxiv_id)
    if not paper_title:
        print("错误: 无法获取论文标题")
        sys.exit(1)
    print(f"  标题: {paper_title}")
    print(f"  PDF:  {access_links['pdf']}")
    print(f"  HTML: {access_links['html']}")
    print(f"  TeX:  {access_links['tex']}")

    # 步骤 2: 创建目录
    print("\n[2/5] 创建目录...")
    slug = sanitize_title(paper_title)
    paper_dir = os.path.join(args.output_dir, slug)
    os.makedirs(paper_dir, exist_ok=True)
    print(f"  目录: {paper_dir}")

    # 步骤 3: 下载 PDF
    print("\n[3/5] 下载 PDF...")
    pdf_path = os.path.join(paper_dir, f"{arxiv_id}.pdf")
    try:
        pdf_resp = requests.get(access_links['pdf'], stream=True, timeout=60)
        pdf_resp.raise_for_status()
        with open(pdf_path, 'wb') as f:
            for chunk in pdf_resp.iter_content(8192):
                f.write(chunk)
        pdf_size = os.path.getsize(pdf_path)
        print(f"  PDF 已下载: {pdf_path} ({pdf_size/1024:.0f} KB)")
    except Exception as e:
        print(f"  PDF 下载失败: {e}")

    # 步骤 4: 获取 HTML 实验版
    print("\n[4/5] 获取 HTML 实验版全文...")
    html_content, html_url = fetch_html_content(arxiv_id)
    if not html_content:
        print("错误: 无法获取 HTML 内容")
        sys.exit(1)

    # 步骤 5: 解析章节并保存
    print("\n[5/5] 解析章节结构...")
    parsed = extract_sections_from_html(html_content, html_url)
    print(f"  共解析出 {len(parsed['sections'])} 个章节")

    saved_files = save_section_files(paper_dir, arxiv_id, parsed)

    # 保存元数据 JSON
    metadata = {
        'arxiv_id': arxiv_id,
        'title': paper_title,
        'title_slug': slug,
        'authors': parsed['authors'],
        'abstract': parsed['abstract'],
        'arxiv_info': parsed['arxiv_info'],
        'links': access_links,
        'section_count': len(parsed['sections']),
        'sections': [
            {'number': s.get('number', ''), 'heading': s['heading'],
             'subsections': [sub['title'] for sub in s.get('subsections', [])]}
            for s in parsed['sections']
        ],
        'paper_dir': paper_dir,
        'pdf_path': pdf_path,
        'sections_dir': os.path.join(paper_dir, f"{arxiv_id}_raw_sections"),
        'structure_file': os.path.join(paper_dir, f"{arxiv_id}_section_structure.txt")
    }

    meta_path = os.path.join(paper_dir, f"{arxiv_id}_metadata.json")
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"  元数据: {meta_path}")

    # 输出摘要
    print("\n" + "=" * 60)
    print("提取完成！")
    print("=" * 60)
    print(f"论文: {paper_title}")
    print(f"目录: {paper_dir}")
    print(f"PDF:  {pdf_path}")
    print(f"章节数: {len(parsed['sections'])}")
    print()
    print("章节结构:")
    for i, sec in enumerate(parsed['sections'], 1):
        print(f"  {i}. {sec['heading']}")
        for sub in sec.get('subsections', []):
            print(f"      - {sub['title']}")
    print()
    print(f"章节文件目录: {os.path.join(paper_dir, arxiv_id + '_raw_sections')}/")
    print("下一步: 读取各章节文件 -> 翻译为中文 -> 组装中文文档")


if __name__ == "__main__":
    main()
