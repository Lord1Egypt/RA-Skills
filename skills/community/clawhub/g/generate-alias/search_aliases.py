#!/usr/bin/env python3
"""
企业别名网络搜索模块
使用 web_fetch 从百度百科、维基百科、企业信息网站获取常用简称
"""

import subprocess
import json
import re
from typing import Optional


def fetch_url(url: str, timeout: int = 10) -> Optional[str]:
    """使用 curl 获取网页内容"""
    try:
        result = subprocess.run(
            ['curl', '-s', '-A', 'Mozilla/5.0',
             '--connect-timeout', str(timeout),
             '--max-time', str(timeout * 2),
             '-L',  # 跟随重定向
             url],
            capture_output=True,
            text=True,
            timeout=timeout * 3
        )
        if result.returncode == 0:
            return result.stdout
    except Exception as e:
        print(f"⚠️  获取 {url} 失败：{e}")
    return None


def search_baike(company_name: str) -> list[str]:
    """
    搜索百度百科获取企业别名
    """
    aliases = []
    
    # 尝试访问百度百科
    baike_url = f"https://baike.baidu.com/search?word={company_name}"
    html = fetch_url(baike_url)
    
    if html:
        # 提取百科条目中的别名信息
        patterns = [
            r'中文名 [：:]\s*([^<\n]+)',
            r'简称 [：:]\s*([^<\n]+)',
            r'英文名 [：:]\s*([^<\n]+)',
            r'别名 [：:]\s*([^<\n]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                # 清理 HTML 标签
                clean = re.sub(r'<[^>]+>', '', match).strip()
                if clean and 2 <= len(clean) <= 15:
                    aliases.append(clean)
    
    return aliases


def search_qichacha(company_name: str) -> list[str]:
    """
    搜索企查查/天眼查获取企业信息
    """
    aliases = []
    
    # 企查查搜索
    qcc_url = f"https://www.qcc.com/web/search?key={company_name}"
    html = fetch_url(qcc_url)
    
    if html:
        # 提取企业名称和简称
        patterns = [
            r'企业名称 [：:]\s*([^<\n]+)',
            r'品牌 [名]？[：:]\s*([^<\n]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                clean = re.sub(r'<[^>]+>', '', match).strip()
                if clean and 2 <= len(clean) <= 15:
                    aliases.append(clean)
    
    return aliases


def search_news(company_name: str) -> list[str]:
    """
    搜索新闻获取企业常用称呼
    """
    aliases = []
    
    # 百度搜索新闻
    news_url = f"https://www.baidu.com/s?wd={company_name}+简称&tn=news"
    html = fetch_url(news_url)
    
    if html:
        # 从新闻标题和摘要中提取
        patterns = [
            r'简称 [为是:：]\s*([^\s，。、,\.<>"]{2,8})',
            r'（以下 (?:简称 | 称)"?([^"）]+)"?）',
            r'"([^"]+)"(?:，)?(?:即 | 就是 | 又称 | 也叫| 旗下)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                if isinstance(match, tuple):
                    for m in match:
                        if m and 2 <= len(m) <= 10:
                            aliases.append(m)
                elif match and 2 <= len(match) <= 10:
                    aliases.append(match)
    
    return aliases


def search_web_aliases(company_name: str) -> list[str]:
    """
    综合搜索多个来源获取企业别名
    """
    all_aliases = []
    
    print(f"🔍 开始网络搜索...")
    
    # 1. 搜索百度百科
    print(f"   → 百度百科...")
    baike_aliases = search_baike(company_name)
    all_aliases.extend(baike_aliases)
    
    # 2. 搜索企业信息网站
    print(f"   → 企业信息网站...")
    qcc_aliases = search_qichacha(company_name)
    all_aliases.extend(qcc_aliases)
    
    # 3. 搜索新闻
    print(f"   → 新闻搜索...")
    news_aliases = search_news(company_name)
    all_aliases.extend(news_aliases)
    
    # 去重和过滤
    unique_aliases = list(set(
        a for a in all_aliases
        if a and 2 <= len(a) <= 10 and not a.isdigit()
    ))
    
    print(f"   ✅ 找到 {len(unique_aliases)} 个别名")
    
    return unique_aliases


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        company_name = ' '.join(sys.argv[1:])
        aliases = search_web_aliases(company_name)
        print(f"\n📋 网络搜索到的别名：{'|'.join(aliases)}")
    else:
        print("用法：python search_aliases.py <企业名称>")
