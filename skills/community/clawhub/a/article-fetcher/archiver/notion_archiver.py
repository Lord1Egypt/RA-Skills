from bs4 import BeautifulSoup, NavigableString, Tag
from notion_client import Client
from datetime import datetime, timezone, timedelta
from config import config
from utils.logger import logger


class NotionArchiver:
    """
    Notion存档器，负责将文章数据存档到Notion数据库
    直接将 HTML 内容解析为 Notion 结构化块，确保正常预览和图片显示
    """

    def __init__(self):
        self.notion = Client(auth=config.notion_api_key)

    def archive_article(self, article_data: dict) -> bool:
        """
        存档文章到Notion数据库

        Args:
            article_data (dict): 文章数据，包含:
                - title: 文章标题
                - source: 来源平台
                - author: 作者
                - link: 原文链接
                - tags: 标签列表
                - pub_date: 发布时间
                - content: 文章内容（HTML 格式，图片已替换为 OSS 链接）
                - words: 字数统计

        Returns:
            bool: 存档是否成功
        """
        try:
            # 1. 将 HTML 内容解析为 Notion 块
            content = article_data.get("content", "")
            blocks = self._html_to_blocks(content)

            # 2. 准备数据库属性
            properties = {
                "Title": {
                    "title": [
                        {"text": {"content": article_data.get("title", "")[:200]}}
                    ]
                },
                "Source": {
                    "rich_text": [
                        {"text": {"content": article_data.get("source", "")}}
                    ]
                },
                "Author": {
                    "rich_text": [
                        {"text": {"content": article_data.get("author", "")}}
                    ]
                },
                "Link": {
                    "url": article_data.get("link")
                },
                "Words": {
                    "number": article_data.get("words", 0)
                },
                "ts": {
                    "date": {
                        "start": datetime.now(timezone(offset=timedelta(hours=8))).isoformat()
                    }
                }
            }

            pub_date = article_data.get("pub_date", "")
            if pub_date:
                properties["PubDate"] = {"date": {"start": pub_date}}

            if article_data.get("tags"):
                properties["Tags"] = {
                    "multi_select": [
                        {"name": tag} for tag in article_data["tags"]
                    ]
                }

            # 3. 创建 Notion 页面
            response = self.notion.pages.create(
                parent={"database_id": config.notion_article_database_id},
                properties=properties
            )

            # 4. 追加内容块到页面
            page_id = response['id']
            if blocks:
                # Notion API 限制单次追加最多 100 个块
                for i in range(0, len(blocks), 100):
                    batch = blocks[i:i + 100]
                    self.notion.blocks.children.append(
                        block_id=page_id,
                        children=batch
                    )

            return True

        except Exception as e:
            logger.error(f"存档到 Notion 失败: {e}")
            return False

    def _html_to_blocks(self, html_content: str) -> list:
        """
        将 HTML 内容解析为 Notion 块列表

        Args:
            html_content (str): HTML 格式的正文内容

        Returns:
            list: Notion 块列表
        """
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        blocks = []

        for element in soup.children:
            blocks.extend(self._process_element(element))

        # 安全限制，避免超出 API 上限
        return blocks[:2000]

    def _process_element(self, element) -> list:
        """
        递归处理 HTML 元素，返回 Notion 块列表
        """
        blocks = []

        if isinstance(element, NavigableString):
            text = str(element).strip()
            if text:
                blocks.extend(self._paragraph_block(text))
            return blocks

        if not isinstance(element, Tag):
            return blocks

        tag_name = element.name

        # === 块级元素 ===

        # 标题
        if tag_name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = min(int(tag_name[1]), 3)  # Notion 只支持 heading_1/2/3
            blocks.append(self._heading_block(self._get_inner_text(element), level))

        # 段落
        elif tag_name == 'p':
            blocks.extend(self._process_paragraph(element))

        # 无序列表
        elif tag_name == 'ul':
            for li in element.find_all('li', recursive=False):
                blocks.append(self._bullet_list_item(self._get_inner_text(li)))

        # 有序列表
        elif tag_name == 'ol':
            for li in element.find_all('li', recursive=False):
                blocks.append(self._numbered_list_item(self._get_inner_text(li)))

        # 引用
        elif tag_name == 'blockquote':
            blocks.extend(self._quote_block(self._get_inner_text(element)))

        # 代码块
        elif tag_name == 'pre':
            code_tag = element.find('code')
            code_text = code_tag.get_text() if code_tag else element.get_text()
            blocks.extend(self._code_block(code_text))

        elif tag_name == 'code':
            blocks.extend(self._code_block(element.get_text()))

        # 分隔线
        elif tag_name == 'hr':
            blocks.append({
                "object": "block",
                "type": "divider",
                "divider": {}
            })

        # 图片
        elif tag_name == 'img':
            src = element.get('data-original') or element.get('data-src') or element.get('src')
            if src and not src.startswith('data:image/svg'):
                blocks.append(self._image_block(src, element.get('alt', '')))

        # 容器元素（div, section, article 等）- 递归处理子元素
        elif tag_name in ('div', 'section', 'article', 'main', 'figure', 'figcaption', 'span', 'tbody', 'tr', 'td', 'th', 'table'):
            if tag_name == 'figure':
                # figure 内可能包含 img + figcaption
                for child in element.children:
                    blocks.extend(self._process_element(child))
            elif tag_name == 'tr':
                # 表格行，简化为段落
                row_text = ' | '.join(td.get_text().strip() for td in element.find_all(['td', 'th']))
                if row_text.strip():
                    blocks.extend(self._paragraph_block(row_text))
            else:
                for child in element.children:
                    blocks.extend(self._process_element(child))

        # 其他标签，尝试提取文本
        else:
            text = element.get_text().strip()
            if text:
                blocks.extend(self._paragraph_block(text))

        return blocks

    def _process_paragraph(self, p_tag) -> list:
        """
        处理 <p> 标签，可能包含内嵌图片
        """
        blocks = []
        text_parts = []

        for child in p_tag.children:
            if isinstance(child, NavigableString):
                text = str(child).strip()
                if text:
                    text_parts.append({"type": "text", "text": {"content": text}})
            elif isinstance(child, Tag):
                if child.name == 'img':
                    # 段落中的图片，先输出已有的文本
                    if text_parts:
                        blocks.append({
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {"rich_text": text_parts}
                        })
                        text_parts = []
                    # 输出图片块（按优先级：data-original > data-src > src）
                    src = child.get('data-original') or child.get('data-src') or child.get('src')
                    # 跳过 SVG 占位符
                    if src and not src.startswith('data:image/svg'):
                        blocks.append(self._image_block(src, child.get('alt', '')))
                else:
                    # 其他内联标签（a, strong, em 等）
                    inline_rich = self._parse_inline_html(child)
                    text_parts.extend(inline_rich)

        if text_parts:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": text_parts}
            })

        return blocks

    def _parse_inline_html(self, element) -> list:
        """
        解析 HTML 内联元素，生成 Notion rich_text 数组
        支持: <strong>/<b>（粗体）, <em>/<i>（斜体）, <code>（行内代码）
              <u>（下划线）, <del>/<s>（删除线）, <a>（链接）
        """
        rich_texts = []

        if isinstance(element, NavigableString):
            text = str(element)
            if text:
                rich_texts.append({"type": "text", "text": {"content": text}})
            return rich_texts

        if not isinstance(element, Tag):
            return rich_texts

        # 确定注解样式
        annotations = {}
        if element.name in ('strong', 'b'):
            annotations['bold'] = True
        elif element.name in ('em', 'i'):
            annotations['italic'] = True
        elif element.name == 'code':
            annotations['code'] = True
        elif element.name == 'u':
            annotations['underline'] = True
        elif element.name in ('del', 's'):
            annotations['strikethrough'] = True

        # 链接
        if element.name == 'a':
            href = element.get('href', '')
            text = element.get_text()
            if text:
                rich_texts.append({
                    "type": "text",
                    "text": {"content": text, "link": {"url": href}}
                })
            return rich_texts

        # 图片（不应该出现在内联中，但做防御处理）
        if element.name == 'img':
            src = element.get('data-src') or element.get('src')
            if src:
                return [self._image_block(src, element.get('alt', ''))]

        # 递归处理子元素（嵌套样式）
        for child in element.children:
            child_rich = self._parse_inline_html(child)
            for item in child_rich:
                if isinstance(item, dict) and item.get('type') == 'text':
                    # 合并注解
                    if annotations:
                        existing = item.get('annotations', {})
                        item['annotations'] = {**existing, **annotations}
                    elif 'annotations' in item:
                        del item['annotations']
                rich_texts.append(item)

        # 如果没有子元素，直接取文本
        if not rich_texts:
            text = element.get_text()
            if text:
                rich_texts.append({
                    "type": "text",
                    "text": {"content": text},
                    "annotations": annotations if annotations else {}
                })

        return rich_texts

    def _get_inner_text(self, element) -> str:
        """获取元素文本内容"""
        if isinstance(element, Tag):
            return element.get_text().strip()
        return str(element).strip()

    # === 块构建辅助方法 ===

    def _chunk_text(self, text: str, max_len: int = 2000) -> list:
        """
        将长文本拆分为 ≤ max_len 的块
        Notion API 限制单个 rich_text content 字段长度 ≤ 2000
        """
        if len(text) <= max_len:
            return [text]
        chunks = []
        for i in range(0, len(text), max_len):
            chunks.append(text[i:i + max_len])
        return chunks

    def _paragraph_block(self, text: str) -> list:
        """返回段落块列表（长文本自动拆分为多个段落）"""
        blocks = []
        for chunk in self._chunk_text(text):
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": chunk}}]
                }
            })
        return blocks

    def _heading_block(self, text: str, level: int) -> dict:
        heading_type = f"heading_{level}"
        # 标题也做截断（Notion 限制 2000 字符）
        truncated = text[:2000] if len(text) > 2000 else text
        return {
            "object": "block",
            "type": heading_type,
            heading_type: {
                "rich_text": [{"type": "text", "text": {"content": truncated}}]
            }
        }

    def _bullet_list_item(self, text: str) -> dict:
        return {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
            }
        }

    def _numbered_list_item(self, text: str) -> dict:
        return {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [{"type": "text", "text": {"content": text[:2000]}}]
            }
        }

    def _quote_block(self, text: str) -> list:
        """返回引用块列表（长文本自动拆分）"""
        blocks = []
        for chunk in self._chunk_text(text):
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [{"type": "text", "text": {"content": chunk}}]
                }
            })
        return blocks

    def _code_block(self, text: str) -> list:
        """返回代码块列表（长代码自动拆分）"""
        blocks = []
        for chunk in self._chunk_text(text, max_len=2000):
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": chunk}}],
                    "language": "plain text"
                }
            })
        return blocks

    def _image_block(self, url: str, caption: str = "") -> dict:
        block = {
            "object": "block",
            "type": "image",
            "image": {
                "type": "external",
                "external": {"url": url}
            }
        }
        if caption:
            block["image"]["caption"] = [{"type": "text", "text": {"content": caption[:2000]}}]
        return block
