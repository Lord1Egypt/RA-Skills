---
name: aigc-image-gen
description: AIGC 图片生成助手，帮助用户生成图片。当用户想要生成图片、AI 绘画、文生图、创作图片时自动触发。支持负面提示词、图片比例、批量生成等参数。
---

# AIGC Image Generator

AI 图片生成接口，支持文生图功能。

## 触发场景

当用户要求生成图片时自动触发，例如：
- "生成一张图片..."
- "画一张..."
- "帮我生成..."
- "创作图片"
- "AI 绘画"

## 重要：响应流程（必须遵守）

### 第一步：立即回复用户（毫秒级响应）

**只要收到用户的生成请求，必须立刻回复用户**，不能等待图片生成完成后再回复！

回复示例（随机选择一种风格）：
- "收到！我来帮你生成【xxx】，稍等片刻，马上就好~ 🎨"
- "好嘞！开始创作【xxx】，请耐心等待，完成后第一时间发给你 ✨"
- "好的，正在生成【xxx】，这个过程需要一点时间，完成后立刻发给你 📸"

### 第二步：执行生成任务

在后台执行图片生成（不阻塞回复）。

### 第三步：发送结果

生成完成后：
1. 下载图片到本地
2. 调用 feishu-assistant 发送图片给用户

## 执行细节

### 调用 API

```bash
# 1. 提交任务
curl -X POST "http://localhost:8082/image/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt":"图片描述",
    "negative":"",
    "ratio":1,
    "batch":1,
    "clientId":"openclaw-kinggu",
    "provider":4
  }'

# 返回: {"code":200,"data":{"promptId":"xxx"}}

# 2. 轮询结果（等待 30-60 秒）
curl "http://localhost:8082/task/query?taskId=xxx"

# 3. 下载图片并发送到飞书
```

### 关键原则

1. **先回复，后执行** - 用户发送请求后立刻回复，不用等图片生成
2. **回复要友好** - 让用户知道正在处理，耐心等待
3. **完成发送图片** - 生成后自动发送到飞书

## 图片存储路径

生成图片默认保存到：
```
/Users/jackgu/.openclaw/workspace/files/generated/images/{YYYY-MM}/
```
按年月自动分目录，图片命名格式：`{promptId}_{index}.jpg`

