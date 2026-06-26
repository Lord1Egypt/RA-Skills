# Bilibili 字幕下载分析 Skill

基于 [biliSub](https://github.com/lvusyy/biliSub) 项目

## 功能

1. **字幕下载** - 下载 B 站视频官方字幕或 ASR 字幕
2. **内容分析** - 词频、情感、统计
3. **详细总结** - 生成结构化总结报告

## 安装

```bash
# 安装 Python 依赖
pip install -r requirements.txt
pip install bilibili-api-python==17.1.2
```

## B 站 Cookie 配置（重要！）

下载字幕需要 B 站登录凭证，请按以下步骤获取：

### 获取 Cookie

1. 登录 [bilibili.com](https://bilibili.com)
2. 按 `F12` 打开开发者工具 → 切换到 **Network** 标签
3. 左侧找到 **Cookies** → 选择 `bilibili.com`
4. 找到并复制发给openclaw

### 配置 Cookie

## 使用

直接发视频链接说使用技能bilibili-subtitle-analysis
```bash
# 下载字幕
node index.js download "https://www.bilibili.com/video/BV1xx411c79H"

# 分析字幕
node index.js analyze "./subtitle.json"

# 生成详细总结
node index.js summary "./subtitle.json"

# 一键下载+总结
node index.js full "https://www.bilibili.com/video/BV1xx411c79H"
```

## 常见问题

### Q: 字幕下载失败，提示 "Credential 未提供"？
**A:** 需要配置 B 站 Cookie，见上方「B 站 Cookie 配置」

### Q: 官方字幕为空或下载失败？
**A:** 大部分视频都有官方字幕，如提示无字幕，可能需要：
- 确认 Cookie 有效
- 或视频本身没有字幕

### Q: ffmpeg 是什么？需要安装吗？
**A:** ffmpeg 是 **可选** 的，用于 ASR 语音识别生成字幕。
- 普通下载字幕 **不需要** ffmpeg
- 如需语音识别功能，请安装 [ffmpeg](https://ffmpeg.org/download.html)

## 目录结构

```
skills/
├── bilibili-subtitle-analysis/  ← 技能主目录
│   ├── index.js
│   └── README.md
└── biliSub/                    ← 已内置
    └── enhanced_bilisub.py
```

## 许可证声明

本技能基于 MIT 许可证开源的 [biliSub](https://github.com/lvusyy/biliSub) 项目构建。
biliSub License: Copyright (c) 2024 lvsyy
