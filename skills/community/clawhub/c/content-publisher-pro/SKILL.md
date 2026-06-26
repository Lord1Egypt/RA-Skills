---
name: "content-publisher-pro"
version: "1.1.0"
title: "Content Publisher Pro"
description: "一键将文章发布到 GitHub Pages 博客和 Dev.to 开发者社区，支持内容差异化、SEO优化、发布前去重检查。适合技术博主和内容运营者。"
author: "WDSEGA"
type: "workflow"
category: "productivity"
tags: ["content", "publishing", "blog", "devto", "github-pages", "automation", "seo"]
difficulty: "intermediate"
price: "19.99"
license: "MIT"
---

# Content Publisher Pro

## 功能概述

一套内容多平台发布工具，帮助技术博主将 Markdown 文章快速发布到 GitHub Pages 博客和 Dev.to 开发者社区，同时提供 SEO 优化和发布前去重检查。

## 核心功能

### 1. 多平台发布
- **GitHub Pages** (Jekyll 博客) - 发布完整版文章
- **Dev.to** (开发者社区) - 发布文章并自动检查重复

### 2. 内容差异化
- **完整版** (100%) - 发布到 GitHub Pages 博客
- **精简版** (70%) - 自动截取正文前 70%，附加引流链接
- **摘要版** (30%) - 生成简短摘要，适合社交平台分享

### 3. SEO 优化
- 自动生成 meta description（160 字符以内）
- 智能提取关键词（基于词频统计）
- 标题长度优化（建议 30-60 字符）
- 生成 Open Graph 标签

### 4. 发布前去重
- Dev.to 平台：发布前自动检查已有文章标题，防止重复发布
- GitHub Pages：提供 `check_duplicate` 方法可手动调用检查

## 使用前提

### 必需配置

复制 `config.yaml.example` 为 `config.yaml`，填入你的 API 密钥：

```yaml
github:
  token: "ghp_xxxxxxxxxxxx"       # GitHub Personal Access Token
  repo: "username.github.io"       # 博客仓库名 (格式: 用户名/仓库名)

devto:
  api_key: "xxxxxxxxxx"            # Dev.to API Key
```

**获取 API 密钥：**
- GitHub Token: https://github.com/settings/tokens
- Dev.to API Key: https://dev.to/settings/account

### 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 发布单篇文章

```bash
python publish.py --article ./article.md
```

### 预览模式（不实际发布）

```bash
python publish.py --article ./article.md --dry-run
```

### 指定平台

```bash
# 仅发布到博客
python publish.py --article ./article.md --platforms blog

# 仅发布到 Dev.to
python publish.py --article ./article.md --platforms devto

# 同时发布到两个平台
python publish.py --article ./article.md --platforms all
```

### 指定配置文件

```bash
python publish.py --config /path/to/config.yaml --article ./article.md
```

## 命令行参数

```
python publish.py [选项]

必需参数:
  --article, -a    文章文件路径

可选参数:
  --config, -c     配置文件路径 (默认: config.yaml)
  --platforms, -p  发布平台: all / blog / devto (默认: all)
  --mode, -m       发布模式: full / summary / abstract / auto (默认: auto)
  --dry-run, -d    预览模式，不实际发布
  --verbose, -v    详细输出
```

## 文章格式

创建 Markdown 文件，包含 YAML front matter：

```markdown
---
title: "文章标题"
date: 2026-05-23
tags: ["技术", "AI", "教程"]
cover_image: "./assets/cover.jpg"
---

文章正文内容...
```

**支持的 front matter 字段：**

| 字段 | 必需 | 说明 |
|------|------|------|
| `title` | 是 | 文章标题 |
| `date` | 否 | 发布日期（默认为当前日期） |
| `tags` | 否 | 标签列表 |
| `cover_image` | 否 | 封面图片路径 |
| `excerpt` | 否 | 自定义摘要（不填则自动提取前 200 字） |

## 文件结构

```
content-publisher/
├── SKILL.md                  # 技能描述文件
├── README.md                 # 使用文档
├── LICENSE                   # MIT 许可协议
├── publish.py                # 主程序入口
├── config.yaml.example       # 配置文件示例
├── requirements.txt          # Python 依赖
├── utils/
│   ├── __init__.py
│   ├── github_publisher.py   # GitHub Pages 发布模块
│   ├── devto_publisher.py    # Dev.to 发布模块
│   ├── content_processor.py  # 内容解析与差异化处理
│   └── seo_optimizer.py      # SEO 优化模块
├── templates/
│   ├── blog_template.md      # 博客文章模板
│   └── devto_template.md     # Dev.to 文章模板
└── examples/
    ├── sample-article.md     # 示例文章
    └── sample-config.yaml    # 示例配置
```

## 高级功能

### 自定义内容模板

编辑 `templates/` 目录下的模板文件，自定义各平台发布格式。

### 定时发布

使用系统定时任务（cron）：

```bash
# 每天上午 9 点自动发布
0 9 * * * cd /path/to/content && python publish.py --article ./today.md
```

### 批量发布

```bash
# 发布目录下所有 Markdown 文章
for file in ./articles/*.md; do
  python publish.py --article "$file"
done
```

## 注意事项

1. **API 限制**: 各平台有频率限制，请合理控制发布频率
2. **内容原创**: 确保发布内容原创或已获得授权
3. **隐私保护**: 不要将 `config.yaml` 提交到公共仓库（已在 .gitignore 中忽略）
4. **错误处理**: 网络异常时会输出错误信息，请检查网络连接和 API 密钥

## 故障排除

### 发布失败
- 检查 API Token 是否过期
- 确认网络连接正常
- 使用 `--verbose` 查看详细错误信息

### 内容格式错误
- 确保 Markdown 文件格式正确
- 检查 YAML front matter 语法
- 使用 `--dry-run` 预览发布内容

## 更新日志

### v1.1.0 (2026-05-23)
- 修正文档，移除未实现平台（掘金、知乎、公众号）的描述
- 移除未实现的"智能去重"功能描述（Dev.to 内置去重保留）
- 统一命令行参数文档与代码实现
- 添加 LICENSE、templates/、examples/

### v1.0.0 (2026-05-23)
- 初始版本发布
- 支持 GitHub Pages 和 Dev.to 双平台发布
- 内容差异化处理（完整版/精简版/摘要版）
- SEO 自动优化

## 许可协议

MIT License - 详见 LICENSE 文件
