---
name: douyin-downloader-js
description: 使用 Node.js 从抖音网页解析视频信息并下载，支持视频和图文类型
---

# 抖音视频下载器 (Node.js 版本)

## 描述

使用 Node.js 从抖音网页的 `window._ROUTER_DATA` 中解析视频信息，支持：
- 视频类型：下载视频并去除水印
- 图文类型：下载图片（最多3张）

## 何时使用

在需要下载抖音链接的内容时使用此技能：
- 下载抖音链接的视频 (v.douyin.com/xxx)
- 下载抖音链接的图文
- 解析视频信息（标题、作者、统计数据等）

## 前置要求

- Node.js 环境

## 使用方法

### 解析并下载

```bash
node ~/.openclaw/skills/douyin-downloader-js/script/douyin-parse.cjs "抖音链接" [输出目录]
```

- 第一个参数：抖音链接（必填）
- 第二个参数：输出目录（可选，默认 ./output）

## 自动识别

脚本会自动识别内容类型：
- **视频类型**：返回 `videoUrl`，下载视频
- **图文类型**：返回 `images` 数组，下载图片

## 图文处理规则

- 图文数量 ≤ 3张：全部发送
- 图文数量 > 3张：只发送前3张，告知用户剩余数量
- 示例：共7张图片 → 发送前3张 → 提示"还有4张图片未发送"

## 返回格式

### 视频类型
```json
{
  "parseId": "视频ID",
  "title": "视频标题",
  "author": { "nickname": "作者昵称", "avatar": "头像URL" },
  "statistics": { "digg": 点赞数, "comment": 评论数, "share": 分享数 },
  "images": [],
  "cover": "封面URL",
  "videoUrl": "视频URL（去除水印）"
}
```

### 图文类型
```json
{
  "parseId": "图文ID",
  "title": "图文标题",
  "author": { "nickname": "作者昵称", "avatar": "头像URL" },
  "statistics": { "digg": 点赞数, "comment": 评论数, "share": 分享数 },
  "images": ["图片URL1", "图片URL2", ...],
  "cover": "封面URL",
  "videoUrl": ""
}
```

## 技术细节

- 使用移动端 User-Agent 模拟手机访问
- 从 `window._ROUTER_DATA` 中提取数据
- 自动去除视频水印（playwm → play）
- 短链接自动重定向到完整URL

## 注意事项

- 视频/图片 URL 是临时的，可能会过期
- 某些内容可能需要登录才能访问
- 下载完成后删除本地临时文件
- 下载的文件默认保存到你的工作空间
