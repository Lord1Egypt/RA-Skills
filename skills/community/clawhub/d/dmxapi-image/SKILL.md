---
name: dmxapi-image-generation
description: "使用 MiniMax (image-01) 和其他模型生成图片。支持文生图、图片编辑。当用户需要生成图片、AI绘图时使用此技能。使用方法：用户需要配置 DMXAPI_API_KEY 环境变量。"
---

# MiniMax Image Generation Skill

## 功能

- **文生图** - 根据文本描述生成图片
- 支持多种尺寸和比例

## 使用前提

用户需要：
1. MiniMax API Key（sk-cp-xxx 格式）
2. 确保套餐包含图片生成功能

## API 用法

```javascript
const https = require('https');

const apiKey = 'YOUR_MINIMAX_API_KEY';

const body = JSON.stringify({
  model: 'image-01',
  prompt: '描述内容',
  aspect_ratio: '1:1',
  response_format: 'base64'
});

const options = {
  hostname: 'api.minimaxi.com',
  path: '/v1/image_generation',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`
  }
};
```

## 示例

生成小龙虾头像：
- model: image-01
- prompt: cute cartoon lobster mascot, kawaii style, orange color, big eyes
- aspect_ratio: 1:1