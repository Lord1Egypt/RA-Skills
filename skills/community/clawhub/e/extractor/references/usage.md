# Extractor 使用文档

## 概述

Extractor 是一个 HTML 结构化字段提取工具，支持三种提取方式：

1. **CSS Selector** — 最直观，适合熟悉前端的选择器语法
2. **XPath** — 功能强大，支持复杂的节点导航和条件过滤
3. **正则表达式** — 适合模式匹配（邮箱、电话、价格等）

三种方式可以混合使用，结果合并输出为 JSON。

## 安装

```bash
pip install beautifulsoup4 lxml

# 仅 URL 模式需要 Playwright
pip install playwright
playwright install chromium
```

## 使用场景

### 场景 1：电商产品价格提取

```python
from scripts.extractor import PageExtractor, load_html

html = load_html("https://shop.example.com/product/123")
ext = PageExtractor(html)

result = ext.extract_all(
    css={
        "name": "h1.product-name",
        "price": {"selector": "span.price", "text": True},
        "images": {"selector": "img.product-img", "attr": "src", "all": True},
    },
    regex={
        "sku": {"pattern": r"SKU[:\s]+([A-Z0-9-]+)", "all": False},
    }
)
# {'name': '产品名', 'price': '¥299', 'images': [...], 'sku': 'ABC-123'}
```

### 场景 2：联系信息提取

```python
ext = PageExtractor(html)

result = ext.extract_by_regex({
    "emails": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "phones": {"pattern": r"1[3-9]\d{9}", "all": True},
    "addresses": {"pattern": r"(?:省|市|区|路|号|街|道).{5,50}", "all": True},
})
```

### 场景 3：表格数据提取

```python
# 用 XPath 提取表格
result = ext.extract_by_xpath({
    "headers": "//table//th/text()",
    "rows": "//table//tr/td/text()",
})
```

### 场景 4：批量页面处理

```python
from pathlib import Path

files = list(Path("html_pages/").glob("*.html"))
all_results = []

for f in files:
    html = f.read_text(encoding="utf-8")
    ext = PageExtractor(html)
    result = ext.extract_by_css({
        "title": "h1",
        "date": "time.published",
    })
    result["_source"] = f.name
    all_results.append(result)

# 保存为 JSON
import json
json.dump(all_results, open("results.json", "w"), ensure_ascii=False, indent=2)
```

## 高级用法

### 提取属性而非文本

```python
# 提取链接
result = ext.extract_by_css({
    "canonical": {"selector": "link[rel='canonical']", "attr": "href"},
    "og_image": {"selector": "meta[property='og:image']", "attr": "content"},
})
```

### 正则分组提取

```python
# 使用捕获分组，只返回分组内容
result = ext.extract_by_regex({
    "price_num": {"pattern": r"¥(\d+\.\d{2})", "all": False},
    # 返回 "299.00" 而不是 "¥299.00"
})
```

### 处理动态页面

对于 JavaScript 渲染的页面，使用 URL 模式（内置 Playwright）：

```python
html = load_html("https://spa-example.com")  # 自动等待 DOM 加载
ext = PageExtractor(html)
```

## 错误处理

- 选择器无匹配 → 对应字段返回 `null`
- XPath 语法错误 → 打印警告到 stderr，字段返回 `null`
- 正则语法错误 → 打印警告到 stderr，字段返回 `null`
- 文件不存在 → 抛出 `FileNotFoundError`
- URL 超时 → 抛出 Playwright 超时异常

## 性能建议

1. **大页面裁剪**：如果只需要页面某个区域，先用 CSS/XPath 定位到容器，再提取
2. **避免过度使用 all=True**：只取需要的数量
3. **复用提取器**：同一页面多次提取时，复用 PageExtractor 实例
4. **文件优先于 URL**：本地文件比网络请求快得多
