# Article Collect Skill

将用户提供的 URL 转化成文章记录的 OpenClaw Skill。支持添加、查询、删除文章条目。

## 功能特性

- 通过 Puppeteer 自动抓取 URL 页面标题作为摘要
- 知识记录存储为 JSON 文件
- 支持添加、列出、删除操作

## 使用

```bash
# 添加知识
pnpm start add_knowledge "https://mp.weixin.qq.com/s/xxx"

# 查看知识列表
pnpm start list_knowledge

# 删除第 N 条知识
pnpm start delete_knowledge 3
```

## 数据存储

知识记录保存在 `~//openclaw-skill-data/article-knowledge.json`。

## 依赖

- puppeteer - 浏览器自动化，用于抓取页面内容
- @bondli-skills/shared - 共享浏览器连接模块
