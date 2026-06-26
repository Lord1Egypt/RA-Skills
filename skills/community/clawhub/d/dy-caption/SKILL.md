---
name: dy-caption
version: 1.0.0
description: 提取抖音视频语音并转成文字。使用场景：(1) 用户要求提取抖音/短视频文案字幕 (2) 用户提供抖音分享链接想转文字 (3) 用户想查询转写余额或历史。requires:
  binaries:
    - curl
sendsDataTo:
  - https://api.dycaption.cn
---

# 抖音字幕提取

通过 `dy-caption` 服务把抖音视频里的语音转成文字。

> **注意**：本技能会将抖音分享链接 / 分享文案 与 API Key 发送到 dy-caption 服务，请确认你信任该服务后再使用。

## 认证

调用接口前需要先准备 API Key：

```bash
export DY_CAPTION_API_KEY="你的 API Key"
```

## 快速使用

```bash
# 提交转写任务
curl -X POST https://api.dycaption.cn/api/v1/transcribe \
  -H "X-API-Key: $DY_CAPTION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input":"7.53 复制打开抖音，看看【示例】 https://v.douyin.com/xxxx/"}'

# 查询余额
curl -X GET https://api.dycaption.cn/api/v1/credits \
  -H "X-API-Key: $DY_CAPTION_API_KEY"

# 查询历史
curl -X GET https://api.dycaption.cn/api/v1/history \
  -H "X-API-Key: $DY_CAPTION_API_KEY"
```

## 任务流程

1. 提交 `/api/v1/transcribe`
2. 记录返回的 `taskId`
3. 轮询 `/api/v1/transcribe/:taskId`
4. 任务完成后读取 `text`

## 相关链接

- CLI 工具：https://github.com/xwchris/douyin-caption-cli
- API 服务：https://api.dycaption.cn
