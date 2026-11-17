---
name: extractor
description: "Extract structured data from HTML pages or URLs using CSS selectors, XPath, regex, or LLM natural..."
tags: [analysis, data, api-integration, file-based, cli]
version: 1.1.0
---

# Extractor - 结构化字段提取器

�?HTML 页面中提取结构化字段，输�?JSON 格式。支持四种提取方式：CSS / XPath / Regex / LLM�?
## 快速开�?
```python
from scripts.extractor import PageExtractor, load_html

# �?URL 加载
html = load_html("https://example.com")

# 或从文件加载
html = load_html("page.html")

# 创建提取�?ext = PageExtractor(html)

# CSS 提取
result = ext.extract_by_css({
    "title": "h1",
    "price": ".price",
    "links": {"selector": "a", "attr": "href", "all": True}
})

# XPath 提取
result = ext.extract_by_xpath({
    "titles": "//h1/text()",
    "emails": "//a[contains(@href,'mailto')]/@href"
})

# 正则提取
result = ext.extract_by_regex({
    "phone": {"pattern": r"1[3-9]\d{9}", "all": False},
    "emails": r"[\w.]+@[\w.]+"
})

# 混合提取
result = ext.extract_all(
    css={"title": "h1"},
    xpath={"specs": "//li/text()"},
    regex={"phone": r"1\d{10}"}
)
```

## CLI 用法

```bash
# �?URL 提取
python scripts/extractor.py --url "https://example.com" --css '{"title": "h1"}' --pretty

# 从文件提�?python scripts/extractor.py --file page.html --xpath '{"links": "//a/@href"}' --pretty

# 混合提取
python scripts/extractor.py --file page.html \
    --css '{"title": "h1"}' \
    --regex '{"phone": "1[3-9]\\d{9}"}' \
    --pretty -o result.json
```

## 配置格式

### CSS 选择�?
简单格式（字符串）�?```json
{"title": "h1.product-title"}
```

完整格式（dict）：
```json
{
    "title": {"selector": "h1", "text": true},
    "link": {"selector": "a.btn", "attr": "href"},
    "items": {"selector": "li.item", "all": true}
}
```

| 参数 | 类型 | 默认�?| 说明 |
|------|------|--------|------|
| selector | str | - | CSS 选择�?|
| attr | str | null | 提取属性（href/src/class 等） |
| all | bool | false | 是否返回所有匹�?|
| text | bool | true | 是否提取文本 |

### XPath

简单格式（字符串）�?```json
{"titles": "//h1/text()"}
```

完整格式（dict）：
```json
{
    "first_title": {"xpath": "//h1/text()", "all": false},
    "all_links": {"xpath": "//a/@href", "all": true}
}
```

### 正则表达�?
简单格式（字符串）�?```json
{"emails": "[\\w.]+@[\\w.]+"}
```

完整格式（dict）：
```json
{
    "phone": {"pattern": "1[3-9]\\d{9}", "all": false},
    "price": {"pattern": "¥(\\d+\\.\\d{2})", "all": true},
    "email_ci": {"pattern": "admin@site", "ignorecase": true}
}
```

| 参数 | 类型 | 默认�?| 说明 |
|------|------|--------|------|
| pattern | str | - | 正则表达�?|
| all | bool | true | 是否返回所有匹�?|
| ignorecase | bool | false | 忽略大小�?|
| multiline | bool | false | 多行模式 |
| dotall | bool | false | DOTALL 模式 |

## 输出格式

所有方法返�?`{字段�? 值}` �?JSON 映射�?- 单个值：字符�?- 多个值：字符串列�?- 无匹配：null

## 依赖

```
pip install beautifulsoup4 lxml playwright
playwright install chromium  # �?URL 模式需�?```

## 限制

- LLM 提取尚未实现（标记为 TODO�?- URL 模式需�?Playwright + Chromium
- 大页面建议先裁剪 HTML 再提�?
## 详细文档

参见 [references/usage.md](references/usage.md)
