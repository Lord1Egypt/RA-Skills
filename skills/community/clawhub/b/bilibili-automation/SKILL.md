---
name: bilibili-automation
version: 1.0.0
description: "B站自动化 - 观看视频、提取字幕、总结内容"
metadata:
  openclaw:
    emoji: "📺"
    requires:
      bins: ["curl"]
      env: ["BROWSERWING_URL"]
    user-invocable: true
---

# 📺 B站自动化 Skill

自动观看 B站视频、提取字幕、总结视频内容。

## 🎯 功能

- 🔍 搜索 B站视频
- 📺 自动播放视频
- 📝 提取视频字幕
- 🤖 AI 总结视频内容
- 📊 获取视频信息（播放量、弹幕、评论）

## 🚀 使用方法

### 场景 1: 搜索并观看视频

**用户说**: "帮我找 B站上关于 Python 教程的视频"

**AI 执行**:
1. 调用 BrowserWing 搜索 "Python 教程"
2. 返回视频列表
3. 用户选择后自动播放

### 场景 2: 提取视频字幕

**用户说**: "提取这个 B站视频的字幕 https://bilibili.com/video/BVxxxxx"

**AI 执行**:
1. 调用 BrowserWing 打开视频
2. 提取字幕/弹幕
3. 返回文本内容

### 场景 3: 总结视频内容

**用户说**: "总结一下这个视频讲了什么"

**AI 执行**:
1. 提取视频字幕
2. 使用 AI 模型总结
3. 返回要点摘要

## 🔧 API 调用

### 搜索视频

```bash
curl -X POST http://localhost:8080/api/v1/tasks/execute \
  -H "Content-Type: application/json" \
  -d '{
    "scriptId": "bilibili-search",
    "params": {
      "keyword": "{{keyword}}",
      "sort": "click"  // click, pubdate, dm
    }
  }'
```

### 提取字幕

```bash
curl -X POST http://localhost:8080/api/v1/tasks/execute \
  -H "Content-Type: application/json" \
  -d '{
    "scriptId": "bilibili-subtitle",
    "params": {
      "videoUrl": "{{videoUrl}}"
    }
  }'
```

### 获取视频信息

```bash
curl -X POST http://localhost:8080/api/v1/tasks/execute \
  -H "Content-Type: application/json" \
  -d '{
    "scriptId": "bilibili-info",
    "params": {
      "videoUrl": "{{videoUrl}}"
    }
  }'
```

## 📋 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 是 | 搜索关键词 |
| videoUrl | string | 是 | B站视频链接 |
| sort | string | 否 | 排序方式：click(播放量), pubdate(发布时间), dm(弹幕) |

## 🔐 安全配置

### 环境变量

```bash
# BrowserWing 服务地址
export BROWSERWING_URL=http://localhost:8080

# B站 Cookie（可选，用于登录功能）
export BILIBILI_SESSDATA=your_sessdata
export BILIBILI_BILI_JCT=your_bili_jct
```

### Cookie 获取方法

1. 登录 B站 (bilibili.com)
2. 按 F12 打开开发者工具
3. 切换到 Application/应用 → Cookies
4. 找到 `SESSDATA` 和 `bili_jct`
5. 复制值并保存到环境变量

## ⚠️ 注意事项

1. **遵守 B站规则** - 不要频繁请求，避免被封
2. **版权问题** - 仅用于个人学习，不要商用
3. **隐私保护** - Cookie 不要泄露给他人
4. **Rate Limit** - 建议间隔 5-10 秒再请求

## 📝 示例对话

### 示例 1: 搜索视频
```
用户: 帮我找 B站上关于 OpenClaw 的视频
AI: 🔍 正在搜索 "OpenClaw"...
    📺 找到 10 个相关视频：
    1. OpenClaw 6大必要配置推荐 - 10万播放
    2. OpenClaw 安装教程 - 5万播放
    3. ...
    
用户: 播放第一个
AI: 📺 正在播放: OpenClaw 6大必要配置推荐
    📝 提取字幕中...
    ✅ 已获取字幕，需要我总结一下吗？
```

### 示例 2: 提取字幕并总结
```
用户: 提取这个视频的字幕 https://bilibili.com/video/BV1G7PFz1E7x
AI: 📝 正在提取字幕...
    ✅ 字幕提取完成！
    📊 视频时长: 15:30
    📝 字幕字数: 3,500 字
    
    🤖 需要我总结一下视频内容吗？
    
用户: 总结一下
AI: 📋 视频总结：
    1. OpenClaw 安全性设置...
    2. 记忆优化配置...
    3. ...
```

## 🔧 故障排除

### 问题 1: 无法提取字幕
**解决**: 部分视频无字幕，尝试提取弹幕

### 问题 2: 视频无法播放
**解决**: 检查 BrowserWing 是否正常运行，Chrome 是否安装

### 问题 3: 需要登录
**解决**: 配置 B站 Cookie 到环境变量

## 📚 相关链接

- B站: https://www.bilibili.com
- BrowserWing: http://localhost:8080
- API 文档: http://localhost:8080/docs

---

**创建时间**: 2026-03-06  
**版本**: 1.0.0  
**状态**: ✅ 已配置，等待录制脚本
