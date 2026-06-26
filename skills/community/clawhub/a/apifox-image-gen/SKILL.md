---
name: apifox-image-gen
description: 使用Apifox图像生成API (jyapi.AI-WX.CN) 生成图片。支持gpt-image-1.5和grok-4-1-image模型。
metadata:
  author: blackbee
  version: 1.0.0
  openclaw:
    emoji: 🖼️
allowed-tools: [exec, message]
---

# Apifox Image Generation

使用jyapi.AI-WX.CN图像生成API生成图片。

## 快速开始

```bash
python3 /root/.openclaw/workspace/skills/apifox-image-gen/image_gen.py -p "你的图片描述" -m gpt-image-1.5 -s 1024x1024
```

## 参数说明

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| --prompt | -p | (必填) | 图片描述 |
| --model | -m | gpt-image-1.5 | 模型: gpt-image-1.5, grok-4-1-image |
| --size | -s | 1024x1024 | 尺寸: 1024x1024, 1536x1024, 1024x1536, 1:1, 2:3, 3:2, 9:16, 16:9 |
| --n | -n | 1 | 生成数量 |
| --output | -o | (自动) | 输出文件路径 |

## 示例

```bash
# 生成小蜜蜂图片
python3 /root/.openclaw/workspace/skills/apifox-image-gen/image_gen.py -p "一只可爱的小蜜蜂" -m gpt-image-1.5 -s 1024x1024

# 生成横版图片
python3 /root/.openclaw/workspace/skills/apifox-image-gen/image_gen.py -p "风景画" -m gpt-image-1.5 -s 1536x1024

# 生成竖版图片
python3 /root/.openclaw/workspace/skills/apifox-image-gen/image_gen.py -p "手机壁纸" -m gpt-image-1.5 -s 9:16

# 使用grok模型
python3 /root/.openclaw/workspace/skills/apifox-image-gen/image_gen.py -p "科技感海报" -m grok-4-1-image -s 16:9
```

## 使用方式

1. 直接用exec运行脚本
2. 图片会保存到 /tmp/ 目录
3. 可以用message工具发给用户
