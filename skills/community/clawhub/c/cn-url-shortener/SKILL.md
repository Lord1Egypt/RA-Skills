name: 短链接生成器
version: "1.0.0"
description: "短链接生成器。将长URL转为短链接，支持自定义后缀、有效期设置、点击统计。纯Python标准库，无需API Key。"
license: MIT-0
tags:
  - tools


# 短链接生成器

短链接生成工具。分享链接更简洁。

## 功能

- **短链生成**：将长URL转为短链接
- **自定义后缀**：设置易记的短链后缀
- **有效期设置**：设置链接过期时间
- **点击统计**：查询短链访问次数
- **批量生成**：一次处理多个URL

## 安装要求

- Python 3.6+
- 无外部依赖

## 使用方法

```bash
# 生成短链接
python3 scripts/url_shortener.py "https://example.com/very/long/url"

# 自定义后缀
python3 scripts/url_shortener.py "https://example.com" --alias "mylink"

# 查询统计
python3 scripts/url_shortener.py "stats 短链接代码"
```

## 示例

输入：`https://example.com/very/long/url`
输出：`短链接: https://short.url/abc123`

## 分类

工具

## 关键词

短链接, URL缩短, short URL, 短网址, link

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
