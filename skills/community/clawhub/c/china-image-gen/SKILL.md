---
name: china-image-gen
description: 国内可用的文生图技能，基于硅基流动（SiliconFlow）API。Use when the user wants to generate images from text in China without VPN. Supports FLUX.1-schnell (free/fast), FLUX.1-dev (highest quality), Kolors (best Chinese prompt understanding), and SD3 (accurate text rendering). Requires a SiliconFlow API key — register at siliconflow.cn with Chinese phone number, pay via Alipay/WeChat. No VPN needed.
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins:
        - curl
    requires_env:
      - name: SILICONFLOW_API_KEY
        description: 硅基流动 API Key，在 cloud.siliconflow.cn 注册后创建，新用户有免费额度
---

# 国内文生图 China Image Generator

基于硅基流动（SiliconFlow）API，国内直连，无需翻墙，支持支付宝/微信充值。
覆盖 FLUX.1、Kolors、SD3 等顶级模型，中文 prompt 直接可用。

## 触发时机

- "帮我生成一张图片：..."
- "画一张..."
- "用 FLUX 生成..."
- "生成一张[风格][内容]的图"

---

## 前置配置（首次使用）

```
1. 访问 cloud.siliconflow.cn，手机号注册（国内直连，新用户送免费额度）
2. 进入「API密钥」页面，创建并复制 API Key
3. 在 OpenClaw 中设置环境变量：
   export SILICONFLOW_API_KEY="sk-xxxxxxxxxxxxxxxx"
   或写入 ~/.openclaw/.env 文件
```

---

## 模型选择指南

根据用户需求选择最合适的模型：

```
追求速度/免费额度    → FLUX.1-schnell（最快，部分免费）
追求最高质量        → FLUX.1-dev（最佳效果，稍慢）
中文 prompt/人像    → Kolors（快手可图，中文理解最强）
图片含文字          → stable-diffusion-3-medium（文字渲染准确）
用户未指定          → 默认用 FLUX.1-schnell（速度快，效果好）
```

---

## API 调用（curl，无需任何其他依赖）

### 基础调用（FLUX.1-schnell，最常用）

```bash
curl -s -X POST "https://api.siliconflow.cn/v1/images/generations" \
  -H "Authorization: Bearer $SILICONFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "black-forest-labs/FLUX.1-schnell",
    "prompt": "YOUR_PROMPT_HERE",
    "image_size": "1024x1024",
    "num_inference_steps": 20,
    "n": 1
  }'
```

### Kolors（中文 prompt 最佳）

```bash
curl -s -X POST "https://api.siliconflow.cn/v1/images/generations" \
  -H "Authorization: Bearer $SILICONFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Kwai-Kolors/Kolors",
    "prompt": "YOUR_PROMPT_HERE",
    "negative_prompt": "低质量, 模糊, 变形, 多余肢体",
    "image_size": "1024x1024",
    "num_inference_steps": 20,
    "guidance_scale": 7.5,
    "n": 1
  }'
```

### FLUX.1-dev（最高质量）

```bash
curl -s -X POST "https://api.siliconflow.cn/v1/images/generations" \
  -H "Authorization: Bearer $SILICONFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "black-forest-labs/FLUX.1-dev",
    "prompt": "YOUR_PROMPT_HERE",
    "image_size": "1024x1024",
    "num_inference_steps": 30,
    "guidance_scale": 3.5,
    "n": 1
  }'
```

### 响应解析

```bash
# 成功响应示例：
{
  "images": [
    {
      "url": "https://cdn.siliconflow.cn/generated/xxx.png",
      "seed": 12345
    }
  ],
  "timings": { "inference": 2.3 }
}

# 提取图片 URL：
IMAGE_URL=$(curl -s ... | python3 -c "import sys,json; print(json.load(sys.stdin)['images'][0]['url'])")

# 或用 jq（如已安装）：
IMAGE_URL=$(curl -s ... | jq -r '.images[0].url')
```

---

## 支持的尺寸规格

```
正方形：  1024x1024（默认，通用）
横版：    1280x720 / 1920x1080（16:9，适合壁纸/横幅）
竖版：    720x1280 / 1080x1920（9:16，适合手机/小红书）
小红书：  1080x1440（3:4，最推荐）
宽幅：    1440x1024（广告横幅）
```

---

## Prompt 优化指南

### 中文 prompt 处理

Kolors 模型原生支持中文，直接输入即可。
FLUX 系列对英文理解更好，中文 prompt 时建议先翻译为英文再输入：

```
用户输入：一只橘猫在阳光下的咖啡馆里睡觉

→ Kolors 直接用中文：
  "一只橘猫在阳光下的咖啡馆里睡觉，温暖的光线，写实风格"

→ FLUX 翻译为英文：
  "An orange cat sleeping in a sunlit cafe, warm golden light,
   photorealistic style, shallow depth of field"
```

### 高质量 prompt 结构

```
[主体描述] + [风格/媒介] + [光线/氛围] + [技术参数]

示例：
  "Portrait of a young woman in traditional Chinese hanfu,
   standing in a bamboo forest, soft morning light,
   watercolor painting style, detailed brushwork,
   high quality, 8k resolution"
```

### 常用风格关键词

```
写实摄影：  photorealistic, DSLR photo, 85mm lens, bokeh
插画：      illustration, digital art, concept art
水彩：      watercolor painting, soft edges, pastel colors
油画：      oil painting, canvas texture, impasto
动漫：      anime style, Studio Ghibli, cel shading
国风：      Chinese ink painting, traditional Chinese art, 工笔画
赛博朋克：  cyberpunk, neon lights, dark city, rain
极简：      minimalist, clean background, simple composition
```

### 负向提示词（Kolors/SD3 使用）

```
通用负向提示词：
"低质量, 模糊, 变形, 多余肢体, 残缺手指, 畸形, 水印, 文字"

英文版：
"low quality, blurry, distorted, extra limbs, missing fingers,
deformed, watermark, text, bad anatomy, ugly"
```

---

## 执行流程

```
用户描述图片需求
  ↓
根据需求选择最佳模型
（中文/人像→Kolors，高质→FLUX-dev，快速→FLUX-schnell）
  ↓
优化/翻译 prompt（FLUX系列优先英文）
  ↓
确认尺寸规格（默认1024x1024）
  ↓
执行 curl 调用
  ↓
解析响应，获取图片 URL
  ↓
⚠️ 提示用户：URL 有效期1小时，请立即下载保存
  ↓
输出图片 URL + 生成参数（方便复现）
```

---

## 输出格式

```
🎨 图片生成完成
━━━━━━━━━━━━━━━━━━━━
模型：FLUX.1-schnell
尺寸：1024x1024
用时：约 X 秒

图片链接：
https://cdn.siliconflow.cn/generated/xxx.png

⚠️  链接有效期：1小时，请立即下载保存
     下载命令：curl -o output.png "上方链接"

生成参数（可复现）：
  Prompt: "..."
  Steps: 20
  Seed: 12345
```

---

## 价格参考（硅基流动，2026年）

```
FLUX.1-schnell   ：极低，部分规格免费
FLUX.1-dev       ：约 ¥0.07/张（1024x1024）
Kolors           ：极低，约 ¥0.03/张
SD3-Medium       ：约 ¥0.07/张

新用户注册免费额度可生成数十至数百张图片
充值方式：支付宝 / 微信支付，最低充值 ¥10
```

---

## 常见错误处理

```
401 Unauthorized   → API Key 未配置或已过期，重新获取
429 Too Many Requests → 请求频率过高，稍等几秒后重试
400 Bad Request    → prompt 含违规内容，修改描述后重试
图片URL打不开       → URL 已超过1小时有效期，重新生成
```

---

## 注意事项

- 生成图片 URL **有效期仅1小时**，务必立即下载保存
- 不支持生成涉及政治人物、暴力、色情等违规内容
- FLUX 系列对英文 prompt 响应更好，Kolors 中英文均佳
- 同一 seed 值可以复现相同图片（在相同参数下）
