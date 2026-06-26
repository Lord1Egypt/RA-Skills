---
name: wechat-article-fetcher
description: |
  微信公众号文章抓取工具。当用户发送微信文章链接、需要保存公众号文章、
  想要离线阅读微信文章、提取微信文章内容、下载微信文章图片时自动触发。
  支持 mp.weixin.qq.com 域名的所有文章链接。
---

# wechat-article-fetcher

微信公众号文章抓取工具 - 一键保存文章为本地HTML

## 触发条件

当用户发送微信公众号文章链接时自动触发：
- `https://mp.weixin.qq.com/s/xxxxx`
- `https://mp.weixin.qq.com/s?__biz=xxxxx`

## 使用示例

**用户输入：**
```
https://mp.weixin.qq.com/s/C7xUcSWVXLYfexbFIeI8Jw
```

**助手执行：**
```bash
./fetch.sh https://mp.weixin.qq.com/s/C7xUcSWVXLYfexbFIeI8Jw
```

**助手回复：**
```
✅ 文章抓取完成！

标题：LibTV 上线，首个同时面向人与 Agent 的专业视频创作平台
文件名：2026-03-21_LibTV_Agent.html
图片：10张已下载
视频封面：2张已下载

访问地址：http://localhost:8080/2026-03-21_LibTV_Agent.html
```

## 功能说明

### 自动命名
文件名格式：`{日期}_{英文关键词}.html`
- 从标题提取英文单词（如 LibTV, Agent, OpenClaw）
- 无英文时提取数字
- 兜底使用URL短码

### 图片处理
- 自动下载文章内所有图片
- 保存到 `images/` 目录
- 替换HTML中的远程URL为本地路径

### 视频处理
- 下载视频封面图到 `video_covers/` 目录
- 点击封面跳转到原文查看视频
- （微信视频有防盗链，无法直接嵌入或下载）

## 文件结构

```
workspace/
├── skills/wechat-article-fetcher/
│   ├── fetch.sh              # 主脚本
│   ├── fetch.py              # Python核心
│   ├── SKILL.md              # 本文件
│   └── README.md             # 说明文档
├── images/                   # 文章图片（自动创建）
├── video_covers/            # 视频封面（自动创建）
└── 2026-03-21_xxx.html      # 生成的文章HTML
```

## 手动启动服务器

如果8080端口被占用：

```bash
# 指定端口
./skills/wechat-article-fetcher/fetch.sh URL 8888

# 或手动启动
cd /root/.openclaw/workspace && python3 -m http.server 8080
```

## 注意事项

1. 首次使用会自动创建 `images/` 和 `video_covers/` 目录
2. 重复抓取同一文章会复用已下载的图片
3. 视频封面图命名格式：`{文件名}_cover_{序号}.jpg`

## 故障排查

**问题：图片显示不出来**
- 检查 `images/` 目录是否存在
- 确认HTTP服务器已启动

**问题：视频封面无法显示**
- 微信图片有防盗链，已下载到本地 `video_covers/`
- 检查文件是否存在

**问题：文件名是日期+数字**
- 文章标题中没有英文单词
- 属于正常情况

## 更新日志

### v1.0.0
- 初始版本
- 支持文章抓取、图片下载、视频封面提取
- 自动命名（日期+英文关键词）
