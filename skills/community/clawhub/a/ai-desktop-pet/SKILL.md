---
name: desktop-pet
version: 1.0.0
description: "🐾 AI-powered 3D desktop pet with emotion detection. Interactive dog/cat that reacts to your mood. Triggers: 桌面宠物, 宠物陪伴, 情绪安慰, desktop pet, virtual pet, 电子宠物."
author: bettermen
tags: [desktop-pet, 3d, threejs, emotion-detection, companion, chinese, web]
platform: [web]
agent_created: true
allowed-tools: Read, Write, Bash, WebFetch, WebSearch
---

# 桌面宠物 Desktop Pet 🐾

> AI驱动的3D桌面宠物 | Three.js程序化建模 | 情绪识别互动 | 狗/猫双模式

## 概述

一个可爱的3D桌面宠物，支持狗狗🐕和猫咪🐈两种模式。上传宠物照片自动提取毛色，根据用户的情绪文字做出不同反应，提供陪伴和安慰。

### 触发场景

- 用户说"打开桌面宠物"、"启动桌面宠物"、"显示宠物"
- 用户表达情绪需要安慰时
- 用户想和宠物互动玩耍时

### 核心功能

| 功能 | 说明 |
|------|------|
| 🐕🐈 双宠物模式 | 狗狗（垂耳圆润）/ 猫咪（尖耳胡须），一键切换 |
| 🎨 3D程序化建模 | 纯 Three.js 几何体构建，卡通材质+动态阴影 |
| 🎬 12种动画 | 跳跃/转圈/摇尾/坐下/趴下/跳舞/蹭蹭/装死/后空翻/踱步 |
| 💬 中文情绪识别 | 7种情绪关键词检测，自动映射对应动画 |
| 📷 照片取色 | 上传照片自动提取主色调，应用到3D宠物毛发 |
| ✨ 粒子特效 | 爱心/星星粒子迸发 |
| 🖱️ 完整交互 | 拖拽旋转/点击互动/双击/滚轮缩放 |
| 🪟 浮窗模式 | 弹出无边框窗口，宠物悬浮桌面 |

## 使用方式

### 启动宠物

直接打开宠物页面：

```
open C:\Users\PC\.workbuddy\skills\desktop-pet\index.html
```

或使用预览：
```
preview_url: file:///C:/Users/PC/.workbuddy/skills/desktop-pet/index.html
```

### 浮窗模式

```
index.html?mode=floating
```

### API 接口

```js
petAPI.setEmotion('happy')     // 触发情绪反应
petAPI.doAction('dance')       // 执行动作
petAPI.getStatus()             // { emotion, pet }
petAPI.setColors({primary, secondary, dark})
```

### 情绪触发

支持的情绪及对应行为：

| 情绪 | 宠物行为 |
|------|----------|
| 😊 开心 | 跳跃、转圈、摇尾巴 |
| 😢 伤心 | 趴下、蹭蹭、安慰 |
| 😰 焦虑 | 来回踱步、坐下 |
| 🎉 兴奋 | 连跳、跳舞、后空翻 |
| 🧘 平静 | 坐下、摇尾、蹭蹭 |
| 😴 孤独 | 趴下、踱步、安慰 |
| 😤 沮丧 | 踱步、趴下、坐下 |

### 动作命令

支持的动作：`jump`, `spin`, `wag`, `sit`, `lie`, `dance`, `nuzzle`, `play_dead`, `backflip`, `pace`

## 文件结构

```
desktop-pet/
├── SKILL.md          # 本文件
├── index.html        # 完整3D宠物应用 (37KB)
└── README.md         # 使用说明
```

## 技术栈

- Three.js 0.157 (CDN ES Module)
- 原生 JavaScript
- 程序化几何体构建（零外部模型依赖）
- 自建 TWEEN 动画播放器
- Canvas 像素采样取色

## 依赖

无外部依赖。所有资源通过 CDN 加载：
- Three.js: `https://unpkg.com/three@0.157.0/build/three.module.js`

## 注意事项

- 需要现代浏览器支持 WebGL
- 浮窗模式需要允许弹出窗口
- 照片取色功能在本地文件模式下可能受限（跨域），建议通过 HTTP 服务访问
- GitHub: https://github.com/bettermen/desktop-pet
