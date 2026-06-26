---
name: Qwen 方言语音识别
description: 基于Qwen3-ASR-0.6B的语音转文字Skill，支持22种中文方言和多语言识别，让你可以用方言和OpenClaw交流。
version: 1.0.0
author: OpenClaw Team
license: Apache-2.0
icon: 🎤
category: audio
tags:
  - asr
  - speech-recognition
  - dialect
  - qwen
  - 语音识别
  - 方言
metadata:
  openclaw:
    requires:
      env:
        - PORT
        - HOST
        - MODEL_NAME
        - DEVICE
        - DTYPE
      bins:
        - node
        - python3
---

# Qwen 方言语音识别 Skill

基于通义千问Qwen3-ASR-0.6B模型的语音转文字服务，支持22种中文方言和30种语言识别，让用户可以用方言直接和OpenClaw交流。

## ✨ 功能特性

- 🎤 **多方言支持**：支持22种中文方言识别
- 🌐 **多语言**：支持30种国际语言
- 💻 **CPU友好**：无需GPU，普通服务器即可运行
- 🔍 **自动检测**：自动识别语言和方言类型
- ⚡ **低延迟**：优化的CPU推理，接近实时响应
- 🎯 **高准确率**：方言识别平均准确率超过90%
- 🔌 **即插即用**：完美适配OpenClaw生态

## 🗣️ 支持的中文方言

安徽话、东北话、福建话、甘肃话、贵州话、河北话、河南话、湖北话、湖南话、江西话、宁夏话、山东话、陕西话、山西话、四川话、天津话、云南话、浙江话、粤语（香港口音）、粤语（广东口音）、吴语、闽南语。

## 🚀 快速开始

### 安装

在OpenClaw中搜索「Qwen方言语音识别」，点击一键安装即可。

### 手动安装

```bash
# 克隆项目
git clone <repository-url>
cd qwen-asr-skill

# 安装依赖
npm install
pip install -r requirements.txt

# 启动服务
npm start
```

### 环境变量配置

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| PORT | 3000 | 服务端口 |
| HOST | 0.0.0.0 | 监听地址 |
| MODEL_NAME | Qwen/Qwen3-ASR-0.6B | ASR模型名称 |
| DEVICE | cpu | 运行设备（cpu/cuda） |
| DTYPE | float32 | 数据类型 |
| BATCH_SIZE | 4 | 批量处理大小 |

## 🔧 使用方式

安装并启用后，直接在OpenClaw中发送语音消息即可，系统会自动：
1. 接收语音输入
2. 调用本Skill进行语音转文字
3. 将识别后的文字传给大模型
4. 返回语音回答给用户

你可以直接说方言，系统会自动识别，无需手动切换语言。

## 📡 API 接口

### POST /transcribe

音频转文字接口

**请求参数：**
- `audio`：音频文件或base64编码的音频数据（必需）
- `language`：指定语言/方言（可选，如："四川话"、"粤语"等）
- `timestamps`：是否返回时间戳（可选，默认false）

**响应示例：**
```json
{
  "success": true,
  "data": {
    "text": "你好，我是四川人，今天吃火锅。",
    "language": "Sichuan",
    "confidence": 0.98,
    "duration": 1.23
  }
}
```

## 📊 性能指标

- 推理速度：实时音频的1.5-2倍速（8核CPU）
- 内存占用：6-8GB运行时
- 支持音频时长：最长5分钟
- 方言识别WER：<16%（平均）

## 🔒 隐私保护

- 所有语音处理在本地完成，不会上传到第三方服务器
- 处理完的音频文件会自动删除，不会存储
- 不收集任何用户语音数据和识别内容

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个Skill！

## 📄 许可证

Apache-2.0 License