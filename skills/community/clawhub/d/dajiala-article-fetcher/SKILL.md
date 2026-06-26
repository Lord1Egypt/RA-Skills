---
name: dajiala-article-fetcher
description: 从大咖啦API获取微信公众号文章链接列表，并保存到Excel文件
trigger: 当用户要求"获取微信文章"、"抓取公众号文章"、"获取文章列表"时触发
---

# 大咖啦文章获取 Skill

从大咖啦 API 获取微信公众号文章链接列表。

## 配置

需要配置环境变量：
- `DAJIALA_KEY`: 大咖啦 API 密钥

## 输入

- 公众号清单文件路径（默认：`/home/admin/每日茶动态/公众号清单.xlsx`）
- 输出目录（默认：`/home/admin/每日茶动态/[当天日期]`）

## 输出

Excel 文件，包含以下字段：
- 公众号名称
- 文章标题
- 文章链接
- 发布时间
