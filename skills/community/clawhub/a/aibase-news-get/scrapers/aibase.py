"""
AI Base 新闻网站爬虫
https://www.aibase.com/zh/news
"""

from datetime import datetime
from typing import List, Dict
import re
from bs4 import BeautifulSoup
from scrapers.base import BaseScraper


class AIBaseScraper(BaseScraper):
    """AI Base 新闻爬虫"""

    @property
    def name(self) -> str:
        return "AIBase"

    @property
    def site_id(self) -> str:
        return "aibase"

    @property
    def list_url(self) -> str:
        return "https://www.aibase.com/zh/news"

    def _parse_relative_time(self, time_str: str) -> str:
        """解析相对时间如 '6 小时前'"""
        now = datetime.now()
        match = re.search(r'(\d+)\s*小时前', time_str)
        if match:
            hours = int(match.group(1))
            from datetime import timedelta
            dt = now - timedelta(hours=hours)
            return dt.strftime("%Y-%m-%d %H:%M:%S")

        match = re.search(r'(\d+)\s*天前', time_str)
        if match:
            days = int(match.group(1))
            from datetime import timedelta
            dt = now - timedelta(days=days)
            return dt.strftime("%Y-%m-%d %H:%M:%S")

        return ""

    def parse_list(self, html: str) -> List[Dict]:
        """解析新闻列表页"""
        soup = BeautifulSoup(html, "html.parser")
        news_list = []

        # 根据实际网页结构调整选择器
        # AI Base网站通常使用卡片式布局
        articles = soup.select("div.news-item, article.news-card, li.news-item, a[href*='/news/']")

        # 尝试更通用的选择器
        if not articles:
            articles = soup.select("a[href*='news']")

        for article in articles:
            try:
                # 尝试提取链接
                link_elem = article if article.name == "a" else article.find("a", href=True)
                if not link_elem:
                    continue

                url = link_elem.get("href", "")
                # 保存原始URL用于去重
                original_url = url
                if not url.startswith("http"):
                    # 确保使用中文版URL获取内容
                    if "/zh" not in url:
                        url = "/zh" + url
                    url = "https://www.aibase.com" + url
                    # 原始URL用于去重
                    original_url = "https://www.aibase.com" + original_url
                else:
                    # 如果是完整URL，确保也获取中文版本
                    if "/zh" not in url:
                        url = url.replace("www.aibase.com/news", "www.aibase.com/zh/news")
                    original_url = url

                # 提取标题和相对时间
                full_text = ""
                if article.name == "a":
                    full_text = article.get_text(strip=True)
                else:
                    title_elem = article.find("h3") or article.find("h2") or article.find("title")
                    if title_elem:
                        full_text = title_elem.get_text(strip=True)

                if not full_text:
                    continue

                # 从文本中提取相对时间（如 "6  小时前.AIbase..."）
                time_str = ""
                title = full_text
                match = re.match(r'(\d+\s*小时前|\d+\s*天前)\.(.+)', full_text)
                if match:
                    time_str = match.group(1).strip()  # "6 小时前"
                    title = match.group(2).strip()     # 实际标题

                # 如果没有匹配到格式，尝试直接提取时间
                if not time_str:
                    match = re.search(r'(\d+)\s*小时前', full_text)
                    if match:
                        time_str = f"{match.group(1)} 小时前"
                        # 从标题中移除时间部分
                        title = re.sub(r'\d+\s*小时前\.?', '', full_text).strip()

                # 解析相对时间为具体时间
                publish_time = self._parse_relative_time(time_str)

                news_list.append({
                    "title": title,
                    "url": url,
                    "original_url": original_url,  # 用于去重的原始URL
                    "publish_time": publish_time,
                    "source": self.name,
                })
            except Exception as e:
                print(f"[{self.site_id}] 解析列表项失败: {e}")
                continue

        return news_list

    def parse_detail(self, html: str, url: str) -> Dict:
        """解析新闻详情页"""
        soup = BeautifulSoup(html, "html.parser")
        result = {
            "content": "",
            "publish_time": "",
        }

        # 提取正文内容 - 根据实际页面结构调整
        # 通常在 article 或 div.content 中
        article = soup.find("article") or soup.find(class_="article-content") or soup.find(class_="content")

        if article:
            # 移除脚本和样式
            for tag in article.find_all(["script", "style"]):
                tag.decompose()

            # 获取文本
            texts = article.get_text(separator="\n", strip=True)
            # 清理多余空白
            lines = [line.strip() for line in texts.split("\n") if line.strip()]
            result["content"] = "\n\n".join(lines)

        # 提取发布时间 - 支持多种格式
        time_elem = soup.find("time") or soup.find(class_="publish-time") or soup.find(class_="date")
        if time_elem:
            time_str = time_elem.get_text(strip=True)
            # 尝试解析时间 - 支持多种格式
            time_formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d",
                "%Y/%m/%d",
                "%b %d, %Y",        # Mar 16, 2026
                "%B %d, %Y",        # March 16, 2026
                "%d %b %Y",         # 16 Mar 2026
                "%d %B %Y",         # 16 March 2026
            ]
            parsed = False
            for fmt in time_formats:
                try:
                    result["publish_time"] = datetime.strptime(time_str, fmt).strftime("%Y-%m-%d %H:%M:%S")
                    parsed = True
                    break
                except ValueError:
                    continue
            if not parsed:
                # 如果都失败，保留原始文本
                result["publish_time"] = time_str

        # 如果没有提取到正文，尝试从整个页面获取
        if not result["content"]:
            body = soup.find("body")
            if body:
                for tag in body.find_all(["script", "style", "nav", "header", "footer"]):
                    tag.decompose()
                result["content"] = body.get_text(separator="\n", strip=True)[:5000]

        return result
