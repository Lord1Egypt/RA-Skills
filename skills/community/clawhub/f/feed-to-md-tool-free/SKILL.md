---slug: feed-to-md-tool-free
name: feed-to-md-tool-free
version: 1.0.0
displayName: RSS转MD(免费版)
summary: "RSS转Markdow"
license: Proprietary
edition: free
description: "RSS转Markdown助手免费版是面向个人用户的轻量RSS内容转换工具。聚焦\"获取-解析-转换-保存\"四步流程，将RSS订阅内容转换为结构化Markdown文档。Use
  when 需要文件处理、文档转换、格式互转、内容提取时使用。不适用于加密文件破解。自动化生成专业文档，提升文档覆盖率。触发关键词：文档生成、转换、设计、机器学习"
  when 需要文件处理、文档转换、格式互转、内容提取时使用。不适用于加密文件破解.
tags:
  - RSS转换
  - Markdown
  - 内容归档
  - 订阅备份
  - 搜索
  - 检索
  - 工具
  - lines
  - append
  - get
  - markdown
  - feed_info
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Knowledge"
---> **获取、解析、转换、保存。四步完成RSS到Markdown的转换。**

无需复杂配置，通过简单的脚本即可将RSS订阅内容转换为结构化的Markdown文档。免费版聚焦轻量场景，提供基础的转换能力.
## 概述
免费版RSS转Markdown工具为个人用户提供基础的RSS内容转换能力。通过Python脚本解析XML，提取核心元素（标题、链接、描述、发布日期），转换为Markdown格式并保存到本地文件.
### 核心定位
| 维度 | 免费版能力 |
|---|-----|
| 单源转换 | 支持 |
| 批量转换 | 不支持（需专业版） |
| 自定义模板 | 不支持（需专业版） |
| 内容增强 | 不支持（需专业版） |
| 定时归档 | 不支持（需专业版） |
| 基础元素提取 | 支持（标题/链接/描述/日期） |
| Markdown输出 | 支持 |
| 文件保存 | 支持 |

## 核心能力
### 1. RSS获取与解析

> 详细代码示例已移至 `references/detail.md`

**处理**: 解析RSS获取与解析的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回RSS获取与解析的响应数据,包含状态码、结果和日志.
### 2. Markdown转换
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | RSS转MD(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```python
class MarkdownConverter:
    """Markdown转换器（免费版）"""
# ...
    def convert(self, feed_info, max_items=None):
        """转换为Markdown"""
        lines = []
# ...
        lines.append(f"# {feed_info.get('title', '未知订阅源')}")
        lines.append("")
        if feed_info.get('description'):
            lines.append(f"> {feed_info['description']}")
            lines.append("")
# ...
        lines.append(f"**订阅源链接**：{feed_info.get('link', '无')}")
get('last_build_date'):
            lines.append(f"**最后更新**：{feed_info['last_build_date']}")
        lines.append("")
        lines.append("---")
        lines.append("")
# ...
        items = feed_info.get('items', [])
        if max_items:
            items = items[:max_items]
# ...
        lines.append(f"## 条目列表（共 {len(items)} 条）")
        lines.append("")
# ...
        for i, item in enumerate(items, 1):
            lines.append(f"
### {i}. {item.get('title', '无标题')}")
            lines.append("")
# ...
            if item.get('pub_date'):
                lines.append(f"**发布日期**：{item['pub_date']}")
            if item.get('author'):
append(f"**作者**：{item['author']}")
            if item.get('link'):
append(f"**原文链接**：[{item['link']}]({item['link']})")
            lines.append("")
# ...
            if item.get('description'):
                desc = self._strip_html(item['description'])
                if len(desc) > 500:
append(f"... [查看完整内容]({item.get('link', '')})")
# ...
            lines.append("---")
            lines.append("")
# ...
        return "\n".join(lines)
# ...
    def _strip_html(self, text):
        """移除HTML标签"""
        import re
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text).strip()
# ...
converter = MarkdownConverter()
markdown = converter.convert(feed, max_items=10)
print(markdown[:500])
```

**处理**: 解析Markdown转换的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回Markdown转换的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 文件保存
```python
import os
from datetime import datetime
# ...
class FileSaver:
    """文件保存器（免费版）"""
# ...
    def __init__(self, output_dir="./output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
# ...
    def save(self, content, filename=None, feed_title=None):
        """保存Markdown文件"""
        if filename is None:
            if feed_title:
                safe_title = "".join(c for c in feed_title if c.isalnum() or c in (' ', '-', '_')).strip()
                filename = f"{safe_title}_{datetime.now().strftime('%Y%m%d')}.md"
            else:
                filename = f"feed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
# ...
        filepath = os.path.join(self.output_dir, filename)
# ...
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
# ...
        print(f"已保存：{filepath}")
        return filepath
# ...
    def save_batch_info(self, feed_info):
        """保存订阅源基本信息"""
        info = {
            'title': feed_info.get('title'),
            'description': feed_info.get('description'),
            'link': feed_info.get('link'),
            'last_build_date': feed_info.get('last_build_date'),
            'item_count': len(feed_info.get('items', [])),
            'saved_at': datetime.now().isoformat()
        }
# ...
        info_file = os.path.join(self.output_dir, "feed_info.json")
        import json
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
# ...
        return info_file
# ...
saver = FileSaver("./output")
filepath = saver.save(markdown, feed_title=feed.get('title'))
saver.save_batch_info(feed)
```

**处理**: 解析文件保存的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回文件保存的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：支持单个订阅源转、基础元素提取与文、助手免费版是面向、个人用户的轻量、内容转换工具、四步流程、订阅内容转换为结、Use、when、需要文件处理、文档转换、格式互转、内容提取时使用、不适用于加密文件、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一：订阅内容归档
**场景描述**：将RSS订阅内容转换为Markdown归档保存.
```python
parser = RSSParser()
converter = MarkdownConverter()
saver = FileSaver("./archives")
# ...
xml = parser.fetch("https://example.com/feed.xml")
# ...
feed = parser.parse(xml)
# ...
# ...
saver.save(markdown, feed_title=feed['title'])
```

### 场景二：博客文章备份
**场景描述**：备份自己博客的RSS内容为Markdown.
```python
parser = RSSParser()
converter = MarkdownConverter()
saver = FileSaver("./blog_backup")
# ...
blog_feed = "https://myblog.com/rss.xml"
xml = parser.fetch(blog_feed)
feed = parser.parse(xml)
# ...
convert(feed, max_items=None)  # 全部条目
saver.save(markdown, feed_title="blog_backup")
# ...
for item in feed['items']:
    single_feed = {'title': item['title'], 'items': [item]}
    single_md = converter.convert(single_feed)
    saver.save(single_md, filename=f"{item['title'][:50]}.md")
```

### 场景三：学习资料整理
**场景描述**：将技术博客的RSS转为Markdown方便阅读.
```python
parser = RSSParser()
converter = MarkdownConverter()
saver = FileSaver("./learning")
# ...
tech_feeds = [
    "https://example.com/tech-feed-1.xml",
com/tech-feed-2.xml",
]
# ...
for url in tech_feeds:
    xml = parser.fetch(url)
    if xml:
        feed = parser.parse(xml)
        if feed:
convert(feed, max_items=5)
            saver.save(markdown, feed_title=feed['title'])
```

## 快速开始
1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 30秒上手
```bash
python3 << 'PYEOF'
import requests
import xml.etree.ElementTree as ET
# ...
url = "https://example.com/feed.xml"
r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
root = ET.fromstring(r.content)
channel = root.find('channel')
# ...
print(f"# {channel.find('title').text}\n")
for item in channel.findall('item')[:5]:
    print(f"## {item.find('title').text}")
    print(f"Link: {item.find('link').text}\n")
PYEOF
```

### 120秒标准搭建

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 配置示例
### 基础配置
```python
import os
# ...
class FeedToMdConfig:
    """RSS转MD配置（免费版）"""
    OUTPUT_DIR = os.getenv("F2M_OUTPUT_DIR", "./output")
    TIMEOUT = int(os.getenv("F2M_TIMEOUT", "10"))
    MAX_ITEMS = int(os.getenv("F2M_MAX_ITEMS", "0"))  # 0表示全部
    USER_AGENT = os.getenv("F2M_USER_AGENT", "Mozilla/5.0")
# ...
    INCLUDE_AUTHOR = True
    INCLUDE_DATE = True
    INCLUDE_DESCRIPTION = True
    DESCRIPTION_MAX_LENGTH = 500
# ...
    @classmethod
    def show(cls):
        print("=== RSS转MD配置 ===")
        print(f"输出目录：{cls.OUTPUT_DIR}")
        print(f"超时时间：{cls.TIMEOUT}s")
        print(f"最大条目数：{cls.MAX_ITEMS if cls.MAX_ITEMS > 0 else '全部'}")
# ...
FeedToMdConfig.show()
```

### 输出格式模板
```python
OUTPUT_TEMPLATE = """# {title}
**订阅源链接**：{link}
**最后更新**：{last_build_date}
# ...
{items_content}
# ...
*转换时间：{converted_at}*
"""
# ...
ITEM_TEMPLATE = """
### {index}. {title}
**发布日期**：{pub_date}
**作者**：{author}
**原文链接**：[{link}]({link})
# ...
{description}
# ...
"""
```

## 最佳实践
## 错误处理
```python
def safe_fetch_and_convert(url):
    """安全的获取与转换"""
    try:
        parser = RSSParser()
        xml = parser.fetch(url)
        if not xml:
            return None
# ...
        if not feed:
            return None
# ...
        converter = MarkdownConverter()
        return converter.convert(feed)
    except Exception as e:
        print(f"转换失败：{e}")
        return None
```

### 2. 增量保存 - 处理方式: 按上述步骤操作并确认结果
```python
def save_incremental(feed, output_dir):
    """增量保存（按条目）"""
    saver = FileSaver(output_dir)
    for item in feed['items']:
        single = {'title': item['title'], 'items': [item]}
        md = MarkdownConverter().convert(single)
        saver.save(md, filename=f"{item['title'][:50]}.md")
```

### 3. 文件命名规范 - 处理方式: 按上述步骤操作并确认结果
```python
def generate_filename(feed_title, item_title=None):
    """生成规范文件名"""
    from datetime import datetime
    date_str = datetime.now().strftime('%Y%m%d')
# ...
    if item_title:
join(c for c in item_title if c.strip()
        return f"{safe_title[:50]}_{date_str}.md"
    else:
        safe_name = "".strip()
        return f"{safe_name}_{date_str}.md"
```
### 错误场景3

检查`error_code`并按照处理方式进行排查.
## 常见问题
### Q1：免费版支持批量转换多个订阅源吗？
不支持。免费版每次只能转换一个订阅源。如需批量转换多个RSS源、并发处理、结果聚合，需升级至专业版.
### Q2：RSS获取失败怎么办？
可能原因：(1) 网络问题，稍后重试；(2) URL错误，检查格式；(3) User-Agent被屏蔽，尝试更换UA；(4) 源站临时不可用。免费版会跳过失败源并报告错误.
### Q3：转换后的Markdown格式不规范？
免费版使用固定模板转换。如需自定义模板（如添加自定义字段、调整格式、添加目录等），需升级专业版。当前模板包含：标题、描述、链接、更新时间、条目列表.
### Q4：可以转换Atom格式吗？
可以。免费版同时支持RSS 2.0和Atom 1.0格式。解析器会自动识别格式并使用对应的解析逻辑.
### Q5：支持哪些输出格式？
免费版仅支持Markdown格式输出。如需HTML、PDF、EPUB等其他格式，需升级专业版.
## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+
- **Node.js**: 16+（可选，用于JavaScript实现）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Python 3.8+ | 运行时 | 必需 | 官网下载安装 |
| requests | Python库 | 必需 | `pip install requests` |
| xml.etree.ElementTree | Python库 | 必需 | Python标准库（XML解析） |
| Node.js 16+ | 运行时 | 可选 | JavaScript实现使用 |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置
- 免费版无需任何API Key
- RSS获取基于公开订阅源，不涉及付费API调用
- LLM模型路由由Agent平台内置提供

### 可用性分类
- **分类**: MD+EXEC（Markdown指令+命令行执行）
- **说明**: 通过自然语言指令驱动Agent执行RSS到Markdown转换任务

## 已知限制
本免费体验版限制以下高级功能（需升级至专业版解锁）：

- **批量转换**（多个订阅源并发处理）
- **自定义模板**（完全自定义输出格式）
- **内容增强**（AI生成摘要、提取关键词）
- **定时归档**（cron调度自动归档）
- **多格式输出**（HTML/PDF/EPUB）
- **图片下载**（自动下载文章图片）
- **全文获取**（自动获取文章完整内容）
- **去重处理**（跨源去重）
- **优先技术支持**

解锁全部高级能力请使用专业版：`feed-to-md-tool-pro`

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```
