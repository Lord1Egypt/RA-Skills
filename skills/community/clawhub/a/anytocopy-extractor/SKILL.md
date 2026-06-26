---
name: anytocopy-extractor
description: |
  使用 anytocopy.com 在线提取抖音、小红书等平台的视频文案。
  当用户发送抖音、小红书等链接，想要提取文案时使用此技能。
  支持50+平台：无水印视频下载、视频转音频、图片去水印等。
---

# AnyToCopy 文案提取器

使用 [AnyToCopy](https://www.anytocopy.com/) 在线提取抖音、小红书等平台的视频文案。

## 工作流

### Step 1：打开网站
使用 browser 工具导航到 AnyToCopy 首页：
```
https://www.anytocopy.com/
```

### Step 2：输入链接
找到输入框（textbox），输入用户提供的链接。

### Step 3：点击提取
找到并点击 "Start Extract" 按钮。

### Step 4：等待结果
等待页面加载出结果（文案内容）。可能需要等待几秒钟。

### Step 5：提取文案
从页面中提取文案内容，返回给用户。

## 注意事项

- 这是一个基于浏览器的自动化方案，适合临时使用
- 如果 AnyToCopy 网站有变化，需要更新 selectors
- 提取是免费的，无需登录
- 支持 50+ 平台：抖音、小红书、快手、B站、微博等

## 输出格式

向用户返回提取到的文案内容，包括：
- 标题
- 正文/脚本
- 如果有视频/图片链接也可以一并提供
