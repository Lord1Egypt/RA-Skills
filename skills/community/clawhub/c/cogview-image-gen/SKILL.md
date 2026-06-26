---
name: zhipu-image-gen
description: 使用智谱AI的CogView模型生成图片。当用户想要AI生成图片时使用此技能，支持中文提示词自动翻译为英文，支持自定义图片尺寸。在首次使用时需要用户配置智谱API密钥。
---

# 智谱AI图片生成

## 首次使用配置

首次使用时会检查是否存在API密钥配置。如果不存在，会提示用户输入智谱API密钥。

**API密钥获取方式：**
1. 访问 https://open.bigmodel.cn/
2. 注册/登录账号
3. 在控制台获取API密钥

## 图片生成

### 基本用法

直接告诉AI你想生成什么样的图片，AI会自动：
1. 将中文提示词翻译成英文
2. 调用智谱CogView-3-Flash模型生成图片
3. 返回生成的图片给你

### 支持的尺寸

- 1024x1024（默认）
- 768x768
- 512x512
- 1024x768（横版）
- 768x1024（竖版）

## 调用方式

使用 `scripts/generate_image.ps1` 脚本：

```powershell
# 基本调用
& "scripts/generate_image.ps1" -Prompt "a cute cat"

# 指定尺寸
& "scripts/generate_image.ps1" -Prompt "a cute cat" -Size "1024x768"
```

## 注意事项

- 使用免费的CogView-3-Flash模型
- 生成的图片URL有效期约24小时
- 如遇401错误，请检查API密钥是否有效