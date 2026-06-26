---
name: ernie-image-art-name
description: "名字转艺术字签名 Skill，使用百度星河社区 ERNIE-Image API 将姓名或文字生成为艺术字/签名图片。This skill should be used when users want to generate artistic text/name images, calligraphy art, cartoon signature, cute line-art signature, watercolor pencil signature, stylized name designs, or text-to-art-typography tasks. 触发词：艺术字、名字艺术字、书法字、艺术字体、文字设计、名字图片、姓名生成图片、把名字变成艺术字、文字转图片、ERNIE-Image 生图、文生图名字、可爱签名、卡通签名、单线签名、彩铅签名、ins风签名。"
version: 1.1.0
author: whisky-12
tags:
  - image-generation
  - ernie-image
  - art-typography
  - cartoon-signature
  - chinese
  - baidu-aistudio
---

# 名字转艺术字 Skill

## 功能概述

使用百度星河社区 ERNIE-Image（文心图像大模型）API，将用户提供的姓名或文字生成为高质量的艺术字/签名图片。支持 **12 种风格**，涵盖经典艺术字、可爱单线卡通签名、软萌彩铅风卡通签名三大类。

## 前置条件

需要百度星河社区 Access Token：前往 https://aistudio.baidu.com/account/accessToken 获取。

## 执行流程

### Step 1：确认 Access Token

优先检查是否已配置，按以下顺序：
1. 用户本次提供的 Token（命令行 `--token`）
2. 环境变量 `AISTUDIO_ACCESS_TOKEN`
3. 配置文件 `config.json`（位于 skill 安装目录下）

**若 Token 未配置**，引导用户通过以下命令保存（只需一次）：
```bash
python3 scripts/generate_art_name.py --set-token YOUR_TOKEN
```
Token 获取地址：https://aistudio.baidu.com/account/accessToken

### Step 2：确认输入参数

向用户确认：
- **名字/文字**：要生成的内容（必填）
- **风格**：从预设风格中选择（默认中国风）
  - 【经典风格】中国风、烫金、霓虹、卡通、石刻、玫瑰、极简、火焰、冰晶、自定义
  - 【卡通签名】单线卡通（7 种模板随机）、彩铅卡通（4 种模板随机）
- **输出目录**（可选，默认 `./art_names`）

若用户描述不够具体，主动询问风格偏好；若用户提到"可爱签名""ins 风""花体字""单线"等关键词，优先推荐卡通签名风格。

### Step 3：执行生成

调用核心脚本（路径相对于 skill 安装目录）：

```bash
python3 scripts/generate_art_name.py \
  --name "用户名字" \
  --style 风格名称 \
  --output 输出目录
```

**常用参数：**

| 参数 | 说明 |
|---|---|
| `--name` / `-n` | 要生成的名字或文字（必填） |
| `--style` / `-s` | 风格：中国风/烫金/霓虹/卡通/石刻/玫瑰/极简/火焰/冰晶/单线卡通/彩铅卡通/自定义 |
| `--prompt` / `-p` | 自定义描述，配合 `--style 自定义` 使用 |
| `--output` / `-o` | 图片保存目录 |
| `--token` / `-t` | 临时指定 Access Token |
| `--model` / `-m` | 模型选择（默认 ERNIE-Image-Turbo） |
| `--set-token` | 将 Token 保存到配置文件（只需一次） |
| `--list-styles` | 查看所有可用风格 |
| `--show-config` | 查看当前配置 |

**卡通签名风格提示：**
- `单线卡通` 和 `彩铅卡通` 每次调用会从多个模板中随机选取，多次生成可获得不同效果
- 这两类风格适合英文名/拼音，中文名效果可能偏弱

### Step 4：展示结果

脚本成功执行后，生成的图片会保存到本地。使用 `open_result_view` 展示图片，并询问是否需要调整风格重新生成。

## 错误处理

| 错误 | 解决方案 |
|---|---|
| Token 无效 / 401 | 引导用户重新获取 Token 并用 `--set-token` 保存 |
| 网络超时 | 重试，或将 timeout 延长至 180 秒 |
| 内容审核拦截 | 调整 Prompt 表达方式，避免敏感词 |
| 模型不可用 | 切换为 `ERNIE-Image` 或 `Stable-Diffusion-XL` |

## 参考文档

详见 `references/api_docs.md`：包含完整 API 参数说明、Prompt 写作技巧和代码示例。

## 配置管理

配置文件 `config.json` 位于 skill 安装目录下，格式如下：

```json
{
  "access_token": "在这里填写你的 Access Token",
  "model": "ERNIE-Image-Turbo",
  "output_dir": "./art_names"
}
```

可直接编辑此文件，或用 `--set-token` 命令更新 Token。
