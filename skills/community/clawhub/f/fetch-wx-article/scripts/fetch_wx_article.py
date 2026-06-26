#!/usr/bin/env python3
"""
获取微信公众号文章内容
Usage: python3 fetch_wx_article.py <wechat_article_url>
"""

import sys
import html2text


def fetch_wx_article(url: str) -> str:
    """
    获取微信公众号文章内容
    
    Args:
        url: 微信公众号文章链接
        
    Returns:
        Markdown 格式的文章内容
    """
    from scrapling.fetchers import Fetcher, FetcherSession
    
    # 获取网页内容
    page = Fetcher.get(url)
    
    # 转换为 Markdown
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    
    md = h.handle(page.html_content)
    return md


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_wx_article.py <wechat_article_url>")
        print("Example: python3 fetch_wx_article.py https://mp.weixin.qq.com/s/xxx")
        sys.exit(1)
    
    url = sys.argv[1]
    
    try:
        content = fetch_wx_article(url)
        print(content)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
