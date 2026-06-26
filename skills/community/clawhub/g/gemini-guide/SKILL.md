---
name: "Gemini Guide"
version: "1.0.0"
description: "Google Gemini API 开发助手，精通 Gemini Pro/Flash、多模态、函数调用、上下文缓存"
tags: ["ai", "api", "gemini", "google"]
author: "ClawSkills Team"
category: "ai"
---
# Gemini API - Google AI 模型接入指南

## 简介
Gemini 是 Google 的多模态大模型，通过 AI Studio 或 Vertex AI 提供 API。
核心优势：超长上下文（最高 200 万 token）和原生多模态（文本/图片/视频/音频）。

## 模型矩阵
| 模型 | 上下文窗口 | 特点 | 适用场景 |
|------|-----------|------|---------|
| gemini-2.5-pro | 100 万 | 最强推理，思维链 | 复杂分析、代码生成 |
| gemini-2.0-flash | 100 万 | 速度快，性价比高 | 日常对话、批量处理 |
| gemini-2.0-flash-lite | 100 万 | 最快最便宜 | 简单任务、高并发 |
| gemini-1.5-pro | 200 万 | 超长上下文 | 长文档分析、代码库理解 |

## SDK 安装与基础调用
```bash
pip install google-genai   # 官方 SDK
```
```python
from google import genai
client = genai.Client(api_key="YOUR_API_KEY")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="用 Python 实现一个快速排序算法"
)
print(response.text)
```

## 多模态能力
```python
from google.genai import types
import pathlib
# 图片理解
image = types.Part.from_bytes(data=pathlib.Path("photo.jpg").read_bytes(), mime_type="image/jpeg")
response = client.models.generate_content(model="gemini-2.0-flash", contents=["描述图片内容", image])
# 视频理解（直接上传文件）
video_file = client.files.upload(file="video.mp4")
response = client.models.generate_content(model="gemini-2.0-flash", contents=["总结视频内容", video_file])
# 音频理解
audio_file = client.files.upload(file="audio.mp3")
response = client.models.generate_content(model="gemini-2.0-flash", contents=["转录并翻译", audio_file])
```

## 函数调用与 JSON 模式
```python
# 函数调用
get_weather = types.FunctionDeclaration(
    name="get_weather", description="获取城市天气",
    parameters=types.Schema(type="OBJECT",
        properties={"city": types.Schema(type="STRING", description="城市名")},
        required=["city"]))
tool = types.Tool(function_declarations=[get_weather])
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="北京天气？",
    config=types.GenerateContentConfig(tools=[tool]))
# JSON 模式
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="列出 3 种编程语言",
    config=types.GenerateContentConfig(response_mime_type="application/json"))
```

## 上下文缓存（Context Caching）
反复查询同一大文档时可大幅降低成本：
```python
cache = client.caches.create(model="gemini-2.0-flash", contents=[large_document],
    config=types.CreateCachedContentConfig(display_name="my-cache", ttl="3600s"))
response = client.models.generate_content(model="gemini-2.0-flash", contents="第三章讲了什么？",
    config=types.GenerateContentConfig(cached_content=cache.name))
```

## 定价对比（每百万 token）
| 模型 | 输入价格 | 输出价格 |
|------|---------|---------|
| Gemini 2.0 Flash | $0.10 | $0.40 |
| Gemini 2.5 Pro | $1.25 | $10.00 |
| Claude Sonnet 4 | $3.00 | $15.00 |
| GPT-4o | $2.50 | $10.00 |

## 与 OpenAI/Claude API 的差异
| 特性 | Gemini API | OpenAI API | Claude API |
|------|-----------|------------|------------|
| 最大上下文 | 200 万 token | 12.8 万 | 20 万 |
| 原生多模态 | 文本/图片/视频/音频 | 文本/图片/音频 | 文本/图片 |
| 免费额度 | 有（AI Studio） | 无 | 无 |
| 上下文缓存 | 原生支持 | 无 | Prompt Caching |
| SDK 风格 | 自有 + OpenAI 兼容 | 自有 | 自有 |

## 最佳实践
- 默认用 `gemini-2.0-flash`，性价比最高
- 长文档用上下文缓存，节省 75%+ 成本
- 视频/音频理解是 Gemini 独特优势
- API Key: https://aistudio.google.com/apikey
