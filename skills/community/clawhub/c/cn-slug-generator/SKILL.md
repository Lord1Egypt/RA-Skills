slug: cn-slug-generator
name: URL Slug生成器
version: "1.0.1"
description: "将中文标题转换为SEO友好的URL Slug，支持拼音和英文翻译转换。"
license: MIT-0
tags:
  - tools
  - seo
  - chinese

<scripts>
  cn_slug_generator.py:
    description: URL Slug生成器主脚本
    run: python3 cn_slug_generator.py
</scripts>

# URL Slug生成器


将中文标题转换为SEO友好的URL Slug，用于博客文章、文档链接、文件命名等场景。

## 功能

- 中文→英文Slug（可选音译）
- 中文→拼音Slug
- 保留数字和常用符号
- 支持批量转换

## 使用方法

```bash
python3 cn_slug_generator.py "如何用Python写一个爬虫"
python3 cn_slug_generator.py "2026年AI发展趋势分析" --pinyin
python3 cn_slug_generator.py "ChatGPT使用技巧" --output slug.txt
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `text` | 要转换的中文文本（位置参数） | 必填 |
| `--pinyin` | 转换为拼音而非英文 | False |
| `--separator` | 分隔符 | - |
| `--output` | 输出文件路径 | 输出到终端 |
| `--batch` | 批量模式，每行一个标题 | False |

## 示例

```bash
# 基本转换
python3 cn_slug_generator.py "开源AI工具推荐"
# 输出: kai-yuan-ai-gong-ju-tui-jian

# 拼音模式
python3 cn_slug_generator.py "深度学习入门" --pinyin
# 输出: shendu-xuexi-rumen

# 批量转换
cat titles.txt | python3 cn_slug_generator.py --batch
```

## 依赖

- Python 3.x
- pypinyin (pip install pypinyin) - 仅拼音模式需要

## 注意事项

- 默认使用英文翻译转换（无需API）
- 拼音模式需安装pypinyin
- 特殊字符自动过滤
- 多语言标题保留英文部分

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
