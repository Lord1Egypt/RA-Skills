---
title: "使用 Content Publisher Pro 自动发布文章"
date: 2026-05-23
tags: ["教程", "自动化", "内容发布"]
cover_image: "./assets/cover.jpg"
excerpt: "本文介绍如何使用 Content Publisher Pro 将文章一键发布到 GitHub Pages 和 Dev.to。"
---

## 简介

Content Publisher Pro 是一个多平台发布工具，帮助你快速将 Markdown 文章发布到 GitHub Pages 博客和 Dev.to 开发者社区。

## 功能特点

- 支持 GitHub Pages (Jekyll 博客) 和 Dev.to 双平台
- 自动 SEO 优化：生成 meta description、提取关键词
- 内容差异化：完整版、精简版、摘要版
- 发布前去重检查

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

复制配置文件并填入 API 密钥：

```bash
cp config.yaml.example config.yaml
```

### 发布文章

```bash
python publish.py --article ./my-article.md --dry-run
```

## 总结

使用 Content Publisher Pro 可以大幅提升内容分发效率，让技术博主专注于写作本身。
