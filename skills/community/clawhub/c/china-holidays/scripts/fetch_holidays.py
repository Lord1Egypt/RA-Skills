#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取中国国家法定节假日安排通知

从中国政府网 (www.gov.cn) 搜索并获取国务院办公厅发布的节假日安排通知。
支持本地缓存优先读取，避免重复网络请求。
"""

import argparse
import io
import json
import os
import re
import sys
import urllib.request
import urllib.error
import urllib.parse

# 修复 Windows 控制台编码问题：强制使用 UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 获取脚本所在目录，用于定位缓存目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'assets')


def get_cache_path(year: int) -> str:
    """获取指定年份的缓存文件路径"""
    return os.path.join(CACHE_DIR, f'{year}.md')


def load_from_cache(year: int) -> dict | None:
    """
    从本地缓存加载节假日数据

    Args:
        year: 查询年份

    Returns:
        解析后的数据字典，如果不存在则返回 None
    """
    cache_path = get_cache_path(year)
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return parse_md_content(content)
        except IOError as e:
            print(f"读取缓存文件失败：{e}", file=sys.stderr)
    return None


def parse_md_content(content: str) -> dict:
    """
    解析 Markdown 文件内容

    Args:
        content: Markdown 文件内容

    Returns:
        包含 title, url, content 的字典
    """
    result = {
        'title': '',
        'url': '',
        'content': content
    }

    # 解析 YAML 前置信息
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            body = parts[2].strip()

            # 解析 frontmatter
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    if key == 'title':
                        result['title'] = value
                    elif key == 'url':
                        result['url'] = value

            result['content'] = body

    return result


def save_to_cache(year: int, title: str, url: str, content: str) -> bool:
    """
    保存节假日数据到本地缓存

    Args:
        year: 年份
        title: 标题
        url: 来源 URL
        content: 内容

    Returns:
        是否保存成功
    """
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        cache_path = get_cache_path(year)

        md_content = f"""---
title: {title}
url: {url}
---

{content}"""

        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"已缓存到：{cache_path}", file=sys.stderr)
        return True
    except IOError as e:
        print(f"保存缓存失败：{e}", file=sys.stderr)
        return False


def search_holiday_notice_v2(year: int) -> dict:
    """
    搜索指定年份的节假日通知（使用简化 GET 接口）

    Args:
        year: 查询年份

    Returns:
        搜索结果的 JSON 数据，结构包含 searchVO.catMap.gongwen.listVO
    """
    base_url = 'https://sousuo.www.gov.cn/search-gov/data'
    params = (
        f't=zhengcelibrary'
        f'&q={urllib.parse.quote(f"{year}年节假日")}'
        f'&timetype=timeqb'
        f'&mintime='
        f'&maxtime='
        f'&sort=score'
        f'&sortType=1'
        f'&searchfield=title'
        f'&pcodeJiguan='
        f'&childtype='
        f'&subchildtype='
        f'&tsbq='
        f'&pubtimeyear='
        f'&puborg='
        f'&pcodeYear='
        f'&pcodeNum='
        f'&filetype='
        f'&p=1'
        f'&n=1'
        f'&inpro='
        f'&bmfl='
        f'&dup='
        f'&orpro='
        f'&type=gwyzcwjk'
    )
    url = f'{base_url}?{params}'

    req = urllib.request.Request(url)

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.URLError as e:
        print(f"网络请求失败：{e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败：{e}", file=sys.stderr)
        sys.exit(1)


def extract_first_url_v2(search_result: dict) -> tuple:
    """
    从新版本搜索结果中提取第一个通知的 URL 和标题

    Args:
        search_result: 搜索结果 JSON（新接口返回的结构）

    Returns:
        (URL, 标题) 元组

    Raises:
        ValueError: 如果无法找到有效的 URL 或搜索结果为空
    """
    # 检查接口返回的 code 是否为 200（成功）
    code = search_result.get('code')
    if code != 200:
        msg = search_result.get('msg', '')
        raise ValueError(f"搜索接口返回错误：{msg}（code={code}）")

    # 检查 searchVO 是否存在
    search_vo = search_result.get('searchVO')
    if search_vo is None:
        raise ValueError("搜索结果为空，该年份的节假日通知可能尚未发布")

    try:
        # 新接口结构：searchVO.catMap.gongwen.listVO 或 searchVO.catMap.gongbao.listVO
        # 优先从 gongbao 中读取，如果没有再从 gongwen 中获取
        cat_map = search_vo.get('catMap', {})
        list_items = []
        if cat_map:
            # 优先尝试 gongbao
            gongbao = cat_map.get('gongbao', {})
            if gongbao:
                list_items = gongbao.get('listVO', [])
            # 如果 gongbao 中没有，再尝试 gongwen
            if not list_items:
                gongwen = cat_map.get('gongwen', {})
                if gongwen:
                    list_items = gongwen.get('listVO', [])

        if not list_items:
            raise ValueError("搜索结果为空，该年份的节假日通知可能尚未发布")

        first_item = list_items[0]
        url = first_item.get('url', '')
        title = first_item.get('title', '')

        if not url:
            raise ValueError("未找到 URL")

        # 清理标题中的 HTML 标签
        title = re.sub(r'<[^>]+>', '', title)

        return url, title
    except (KeyError, IndexError) as e:
        raise ValueError(f"解析搜索结果失败：{e}")


# =============================================================================
# 方法 search_holiday_notice 和方法 extract_first_url 已废弃！
# 改为使用 search_holiday_notice_v2 和 extract_first_url_v2
# 原因：老方法使用复杂的 POST 请求接口，包含大量 header 和请求体参数，存在未来不可控性
# 新方法使用简化的 GET 请求接口，更加稳定可靠
# =============================================================================
def search_holiday_notice(year: int) -> dict:
    """
    搜索指定年份的节假日通知

    注意：此方法已废弃，请使用 search_holiday_notice_v2 替代。

    Args:
        year: 查询年份

    Returns:
        搜索结果的 JSON 数据
    """
    url = 'https://sousuoht.www.gov.cn/athena/forward/2B22E8E39E850E17F95A016A74FCB6B673336FA8B6FEC0E2955907EF9AEE06BE'

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://sousuo.www.gov.cn',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'athenaAppKey': 'A279FYM6cwbCEXLcL0uA21VgBc%2Fb0O9TBD3%2F2gAS7u21qKOuAdm2A1e5uJHOM09hETH43%2F4nDWG96nzwR5YEiXI6Bff5q%2B22Vv95OjkaFLNPHU%2FaIWDFLlVaYlD7KauvCDzkhns%2FhMw%2BJCKFSJxhmlpIsOqmgbMszFM3qMgpr1g%3D',
        'athenaAppName': '%E5%9B%BD%E7%BD%91%E6%90%9C%E7%B4%A2',
    }

    data = {
        "code": "17da70961a7",
        "historySearchWords": [],
        "dataTypeId": "15",
        "orderBy": "time",
        "searchBy": "title",
        "appendixType": "",
        "granularity": "ALL",
        "trackTotalHits": True,
        "beginDateTime": "",
        "endDateTime": "",
        "isSearchForced": 0,
        "filters": [],
        "pageNo": 1,
        "pageSize": 10,
        "customFilter": {
            "operator": "and",
            "properties": []
        },
        "searchWord": f"{year}年节假日"
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.URLError as e:
        print(f"网络请求失败：{e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败：{e}", file=sys.stderr)
        sys.exit(1)


def extract_first_url(search_result: dict) -> tuple:
    """
    从搜索结果中提取第一个通知的 URL 和标题

    注意：此方法已废弃，请使用 extract_first_url_v2 替代。

    Args:
        search_result: 搜索结果 JSON

    Returns:
        (URL, 标题) 元组

    Raises:
        ValueError: 如果无法找到有效的 URL
    """
    try:
        list_items = search_result['result']['data']['middle']['list']
        if not list_items:
            raise ValueError("搜索结果为空")

        first_item = list_items[0]
        url = first_item.get('url', '')
        title = first_item.get('title', '')

        if not url:
            raise ValueError("未找到 URL")

        # 清理标题中的 HTML 标签
        title = re.sub(r'<[^>]+>', '', title)

        return url, title
    except (KeyError, IndexError) as e:
        raise ValueError(f"解析搜索结果失败：{e}")


def fetch_notice_content(url: str) -> str:
    """
    获取通知页面的内容并清理，只保留中文

    Args:
        url: 通知页面 URL

    Returns:
        清理后的纯中文内容
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            html_content = response.read().decode('utf-8')
            return extract_chinese_text(html_content)
    except urllib.error.URLError as e:
        print(f"获取通知内容失败：{e}", file=sys.stderr)
        sys.exit(1)


def extract_chinese_text(html: str) -> str:
    """
    从 HTML 中提取中文文本

    Args:
        html: HTML 内容

    Returns:
        提取的中文文本
    """
    # 移除 script 和 style 标签及其内容
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # 移除 HTML 注释
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)

    # 尝试提取正文内容 - 查找包含"国务院办公厅关于"的段落
    # 通常正文内容会包含这些关键信息
    main_content = None

    # 方法 1: 查找 id="UCAP-CONTENT" 或 class="pages_content" 的容器（老版本页面）
    ucap_match = re.search(
        r'<div[^>]*(?:id|class)\s*=\s*["\'](?:UCAP-CONTENT|pages_content)["\'][^>]*>(.*?)</div>\s*</div>',
        html,
        flags=re.DOTALL | re.IGNORECASE
    )
    if ucap_match:
        main_content = ucap_match.group(1)

    # 方法 2: 查找 TRS 相关的内容容器
    if not main_content:
        trs_match = re.search(
            r'<div[^>]*class=["\'][^"\']*TRS[^"\']*["\'][^>]*>(.*?)</div>\s*(?:</div>)?\s*(?:</div>)?',
            html,
            flags=re.DOTALL | re.IGNORECASE
        )
        if trs_match:
            main_content = trs_match.group(1)

    # 方法 3: 查找包含通知正文的内容（匹配完整的公告格式）
    if not main_content:
        # 尝试匹配从"国务院办公厅关于"开始到"二○○×年"或"20××年"结束的内容
        content_match = re.search(
            r'(国务院办公厅关于\d{4}年.*?(?:二○[○〇一二三四五六七八九] 年|20\d{2}年)\d{1,2}月\d{1,2}日)',
            html,
            flags=re.DOTALL
        )
        if content_match:
            main_content = content_match.group(1)

    # 方法 4: 如果还没找到，尝试查找 ucms_content 容器
    if not main_content:
        ucms_match = re.search(
            r'<div[^>]*(?:id|class)\s*=\s*["\'][^"\']*content[^"\']*["\'][^>]*>(.*?)</div>',
            html,
            flags=re.DOTALL | re.IGNORECASE
        )
        if ucms_match:
            main_content = ucms_match.group(1)

    # 方法 5: 老版本页面 - 查找 id="zoom" 或 class="zoom" 的容器
    if not main_content:
        zoom_match = re.search(
            r'<div[^>]*(?:id|class)\s*=\s*["\']zoom["\'][^>]*>(.*?)</div>',
            html,
            flags=re.DOTALL | re.IGNORECASE
        )
        if zoom_match:
            main_content = zoom_match.group(1)

    # 方法 6: 查找包含"国办发明电"的内容块
    if not main_content:
        notice_match = re.search(
            r'(国办发明电〔\d{4}〕\d+号.*?(?:二○[○〇一二三四五六七八九] 年|20\d{2}年)\d{1,2}月\d{1,2}日)',
            html,
            flags=re.DOTALL
        )
        if notice_match:
            main_content = notice_match.group(1)

    if main_content:
        html = main_content

    # 移除所有 HTML 标签，但保留内容
    text = re.sub(r'<br\s*/?>', '\n', html)
    text = re.sub(r'</p>', '\n\n', text)
    text = re.sub(r'<[^>]+>', '', text)

    # 处理常见的 HTML 实体
    html_entities = {
        '&nbsp;': ' ',
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&apos;': "'",
        '&#8220;': '"',
        '&#8221;': '"',
        '&#8212;': '——',
        '&#8211;': '-',
        '&mdash;': '——',
        '&ndash;': '-',
        '&ldquo;': '"',
        '&rdquo;': '"',
        '&bull;': '•',
        '&#12288;': ' ',
        '&ensp;': ' ',
        '&emsp;': ' ',
    }

    for entity, char in html_entities.items():
        text = text.replace(entity, char)

    # 处理数字实体
    text = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), text)

    # 提取中文字符、数字、标点符号和必要的空白
    # 包含特殊字符：○ (U+25CB)、〇 (U+3007)、〔〕等
    chinese_pattern = r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef0-9\s\(\)（）—\-、,，。：:；;！!？?""〇○〔〕]+'
    matches = re.findall(chinese_pattern, text)

    result = ''.join(matches)

    # 清理可能导致编码问题的特殊 Unicode 字符
    cleaned_result = []
    for char in result:
        if ('\u4e00' <= char <= '\u9fff' or
            '\u3000' <= char <= '\u303f' or
            '\uff00' <= char <= '\uffef' or
            char.isdigit() or
            char in ' \n\r\t、,，。：:；;！!？?""''（）()【】[]《》<>—-·…〇○〔〕'):
            cleaned_result.append(char)

    result = ''.join(cleaned_result)

    # 移除文章中的无关内容（直接匹配文字）
    result = result.replace('扫一扫在手机打开当前页', '')
    result = result.replace('解读', '')
    result = result.replace('登录', '')
    result = result.replace('注册', '')

    # 清理多余的空行和空格
    result = re.sub(r'\n\s*\n+', '\n\n', result)
    result = re.sub(r' +', ' ', result)
    result = result.strip()

    return result


def fetch_and_cache(year: int) -> dict:
    """
    从网络获取节假日数据并缓存

    Args:
        year: 查询年份

    Returns:
        包含节假日信息的字典
    """
    print(f"正在从网络获取 {year} 年节假日数据...", file=sys.stderr)

    # 第一步：搜索节假日通知（使用新接口）
    search_result = search_holiday_notice_v2(year)

    # 第二步：提取第一个 URL 和标题
    try:
        url, title = extract_first_url_v2(search_result)
        print(f"找到通知：{url}", file=sys.stderr)
    except ValueError as e:
        print(f"错误：{e}", file=sys.stderr)
        # 如果错误信息中已经包含"没有"、"为空"或"尚未发布"，则不再重复提示
        error_msg = str(e)
        if "没有" not in error_msg and "为空" not in error_msg and "尚未发布" not in error_msg:
            print(f"可能该年份的节假日通知尚未发布", file=sys.stderr)
        sys.exit(1)

    # 第三步：获取并清理通知内容
    print("正在获取通知内容...", file=sys.stderr)
    content = fetch_notice_content(url)

    # 保存到缓存
    save_to_cache(year, title, url, content)

    return {
        'title': title,
        'url': url,
        'content': content
    }


def main():
    parser = argparse.ArgumentParser(
        description='获取中国国家法定节假日安排通知（支持本地缓存）'
    )
    parser.add_argument(
        '--year',
        type=int,
        required=True,
        help='要查询的年份，例如：2026'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='强制从网络获取，忽略本地缓存'
    )

    args = parser.parse_args()

    # 优先从缓存读取
    if not args.force:
        cached_data = load_from_cache(args.year)
        if cached_data:
            print(f"从缓存读取 {args.year} 年节假日数据", file=sys.stderr)
            # 输出内容
            print(cached_data.get('content', ''))
            return

    # 缓存不存在或强制刷新，从网络获取
    data = fetch_and_cache(args.year)

    # 输出结果
    print(data.get('content', ''))


if __name__ == '__main__':
    main()
