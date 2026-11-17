"""
Obsidian Markdown 存档器
将文章数据转换为 Obsidian 兼容的 .md 文件，存入本地知识库
"""
import os
import re
import yaml
from datetime import datetime, timezone, timedelta
from utils.logger import logger

# 文件名非法字符
_FILENAME_ILLEGAL = re.compile(r'[\\/:*?"<>|]')


class ObsidianArchiver:
    """Obsidian 本地 Markdown 存档器"""

    def __init__(self, vault_path: str = None):
        if vault_path is None:
            from config import config
            vault_path = config.obsidian_vault_path
        self.vault_path = vault_path
        self.article_dir = os.path.join(vault_path, '收件箱')

    def archive_article(self, article_data: dict) -> bool:
        """
        存档文章到 Obsidian Vault

        Args:
            article_data (dict): 文章数据，包含:
                - title: 文章标题
                - source: 来源平台 (wechat/xhs/douban/zhihu)
                - author: 作者
                - link: 原文链接
                - tags: 标签列表
                - pub_date: 发布时间
                - content: 文章内容（HTML，图片已替换为 OSS 链接）
                - words: 字数统计

        Returns:
            bool: 存档是否成功
        """
        try:
            os.makedirs(self.article_dir, exist_ok=True)

            title = article_data.get('title', '未知标题')
            platform = article_data.get('source', 'unknown')

            # 构建文件名
            filename = self._build_filename(title, platform)
            filepath = os.path.join(self.article_dir, filename)

            # 构建内容
            md_content = self._build_markdown(article_data)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)

            logger.info(f"Obsidian 存档成功：{filepath}")
            return True

        except Exception as e:
            logger.error(f"Obsidian 存档失败：{e}")
            return False

    def _build_filename(self, title: str, platform: str) -> str:
        """构建文件名：{YYYY-MM-DD}_{sanitized_title}.md"""
        date_str = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d')
        safe_title = _FILENAME_ILLEGAL.sub('-', title)
        safe_title = re.sub(r'\s+', ' ', safe_title).strip()
        if len(safe_title) > 60:
            safe_title = safe_title[:57] + '...'
        return f"{date_str}_{safe_title}.md"

    def _build_markdown(self, data: dict) -> str:
        """构建完整的 Markdown 文件内容（Frontmatter + 正文）"""
        frontmatter = self._build_frontmatter(data)
        body = self._html_to_markdown(data.get('content', ''))

        # 如果正文为空，用标题作为一级标题
        if not body.strip():
            body = f"# {data.get('title', '')}"

        return f"---\n{frontmatter}---\n\n{body}\n"

    def _build_frontmatter(self, data: dict) -> str:
        """构建 YAML Frontmatter"""
        tags = data.get('tags', []) or []
        pub_date = data.get('pub_date', '') or ''
        fetched = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')

        fm = {
            'title': data.get('title', ''),
            'source': data.get('source', ''),
            'author': data.get('author', ''),
            'link': data.get('link', ''),
            'tags': tags,
            'pub_date': pub_date,
            'words': data.get('words', 0),
            'fetched': fetched,
        }

        # 使用 safe_dump 避免特殊字符问题
        yaml_str = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)

        # yaml.dump 会在列表项前加 "- "，Obsidian 期望的 tags 格式也是 "- tag"
        # 但 title 包含特殊字符（如 []）时 yaml 会加引号，这是正确行为
        return yaml_str

    def _html_to_markdown(self, html_content: str) -> str:
        """将 HTML 正文转换为 Markdown（懒加载 markdownify）"""
        if not html_content:
            return ''

        try:
            from markdownify import markdownify as md

            # markdownify 将 HTML 转为 Markdown
            text = md(
                html_content,
                heading_style='ATX',      # # 标题格式
                bullets='-',              # - 无序列表
                strip=['script', 'style', 'noscript'],
            )
            # 清理多余空行
            text = re.sub(r'\n{3,}', '\n\n', text)
            return text.strip()
        except Exception as e:
            logger.warning(f"Markdown 转换失败，保留原始 HTML：{e}")
            return html_content
