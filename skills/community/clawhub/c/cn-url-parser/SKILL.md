---
slug: cn-url-parser
name: URL解析器
version: "1.2.1"
author: 千策
---

# URL解析器

URL解析工具。Web开发者调试好帮手。

## 功能

- **URL分解**：协议、域名、端口、路径、参数、锚点
- **参数提取**：逐个列出query参数的key-value
- **URL编码/解码**：处理%XX编码的中文和特殊字符
- **URL构建**：从各部分组装完整URL
- **批量解析**：一次解析多个URL

## 安装要求

- Python 3.6+
- 无外部依赖

## 使用方法

```bash
# 解析URL
python3 scripts/url_parser.py "https://example.com/search?q=hello&page=1#top"

# URL编码
python3 scripts/url_parser.py "encode 你好世界"

# URL解码
python3 scripts/url_parser.py "decode %E4%BD%A0%E5%A5%BD"
```

## 示例

输入：`https://example.com/search?q=hello&page=1`
输出：
```
协议: https
域名: example.com
路径: /search
参数: q=hello, page=1
```

## 分类

开发工具

## 关键词

URL, 解析, 参数提取, parser, query, encode, decode

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
