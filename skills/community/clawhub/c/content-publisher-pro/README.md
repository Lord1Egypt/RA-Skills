# Content Publisher Pro

一键将 Markdown 文章发布到 GitHub Pages 博客和 Dev.to 开发者社区，支持内容差异化、SEO 优化、发布前去重检查。

## 功能特点

- **GitHub Pages 发布** - 将文章发布到 Jekyll 博客
- **Dev.to 发布** - 将文章发布到开发者社区，自动检查重复
- **内容差异化** - 自动生成完整版、精简版、摘要版
- **SEO 自动优化** - 生成 meta 标签、关键词、Open Graph 标签
- **预览模式** - 发布前预览效果，不实际发布

## 快速开始

### 1. 安装

```bash
pip install -r requirements.txt
```

### 2. 配置

复制示例配置文件并修改：

```bash
cp config.yaml.example config.yaml
```

编辑 `config.yaml`，填入你的 API 密钥：

```yaml
github:
  token: "ghp_xxxxxxxxxxxx"
  repo: "your-username/your-username.github.io"

devto:
  api_key: "xxxxxxxxxx"
```

### 3. 使用

```bash
# 发布单篇文章到所有平台
python publish.py --article ./my-article.md

# 预览模式（不实际发布）
python publish.py --article ./my-article.md --dry-run

# 仅发布到博客
python publish.py --article ./my-article.md --platforms blog

# 仅发布到 Dev.to
python publish.py --article ./my-article.md --platforms devto
```

## 文章格式

```markdown
---
title: "文章标题"
date: 2026-05-23
tags: ["技术", "AI", "教程"]
cover_image: "./assets/cover.jpg"
---

文章内容...
```

## 详细文档

见 `SKILL.md` 文件。

## 许可

MIT License
