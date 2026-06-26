---
name: alphashop-image
category: official-1688
description: >-
  AlphaShop（遨虾）图像处理 API 工具集。支持11个接口：图片翻译、图片翻译PRO、
  图片高清放大、图片主题抠图、图片元素识别、图片元素智能消除、图像裁剪、
  虚拟试衣（创建+查询）、模特换肤（创建+查询）。
  触发场景：图片翻译、翻译图片文字、放大图片、高清放大、抠图、去背景、
  检测水印/Logo/文字、消除水印、去牛皮癣、裁剪图片、虚拟试衣、AI试衣、
  模特换肤、换模特、AlphaShop图像、遨虾图片处理。
metadata:
  version: 1.0.1
  label: 图像处理
  author: 1688官方技术团队
---

# AlphaShop 图像处理

通过 `scripts/alphashop_image.py` 调用遨虾图像处理 API。

## 前置配置（必须先完成）

⚠️ **使用本 SKILL 前，必须先配置以下环境变量，否则所有接口调用都会失败。**

| 环境变量 | 说明 | 必填 | 获取方式 |
|---------|------|------|---------|
| `ALPHASHOP_ACCESS_KEY` | AlphaShop API 的 Access Key | ✅ 必填 | 可以访问1688-AlphaShop（遨虾）来申请 https://www.alphashop.cn/seller-center/apikey-management ，直接使用1688/淘宝/支付宝/手机登录即可 |
| `ALPHASHOP_SECRET_KEY` | AlphaShop API 的 Secret Key | ✅ 必填 | 可以访问1688-AlphaShop（遨虾）来申请 https://www.alphashop.cn/seller-center/apikey-management ，直接使用1688/淘宝/支付宝/手机登录即可 |

**⚠️ AlphaShop 接口欠费处理：** 如果调用 AlphaShop 接口时返回欠费/余额不足相关的错误，**必须立即中断当前流程**，提示用户前往 https://www.alphashop.cn/seller-center/home/api-list 购买积分后再继续操作。

### 配置方式

在 OpenClaw config 中配置：
```json5
{
  skills: {
    entries: {
      "alphashop-image": {
        env: {
          ALPHASHOP_ACCESS_KEY: "YOUR_AK",
          ALPHASHOP_SECRET_KEY: "YOUR_SK"
        }
      }
    }
  }
}
```

如果用户没有提供这些密钥，**必须先询问用户获取后再继续操作**。

## 命令速查

脚本路径：`scripts/alphashop_image.py`

### 同步接口（直接返回结果）

| 命令 | 功能 | 必填参数 |
|------|------|----------|
| `translate` | 图片翻译 | `--image-url` `--source-lang` `--target-lang` |
| `translate-pro` | 图片翻译PRO（源语种可传auto） | `--image-url` `--source-lang` `--target-lang` |
| `enlarge` | 图片高清放大 | `--image-url` |
| `extract-object` | 主题抠图 | `--image-url` `--transparent true/false` |
| `detect-elements` | 元素识别 | `--image-url` |
| `remove-elements` | 元素智能消除 | `--image-url` + 至少一个消除标记 |
| `crop` | 图像裁剪 | `--image-url` |

### 异步接口（提交任务 → 查询结果）

| 命令 | 功能 | 必填参数 |
|------|------|----------|
| `virtual-try-on` | 创建虚拟试衣任务 | `--clothes 'URL,TYPE'` `--count N` |
| `query-try-on` | 查询虚拟试衣结果 | `--task-id` |
| `change-model` | 创建模特换肤任务 | `--image-url` `--model-type` `--bg-style` `--age` `--gender` `--num` |
| `query-change-model` | 查询模特换肤结果 | `--task-id` |

## 使用示例

```bash
# 图片翻译（中文→英文）
python scripts/alphashop_image.py translate \
  --image-url "https://example.com/img.jpg" \
  --source-lang zh --target-lang en

# 图片翻译PRO（自动识别源语种）
python scripts/alphashop_image.py translate-pro \
  --image-url "https://example.com/img.jpg" \
  --source-lang auto --target-lang ru

# 高清放大4倍
python scripts/alphashop_image.py enlarge \
  --image-url "https://example.com/img.jpg" --factor 4

# 抠图（透明底）
python scripts/alphashop_image.py extract-object \
  --image-url "https://example.com/img.jpg" --transparent true

# 抠图（白色背景）
python scripts/alphashop_image.py extract-object \
  --image-url "https://example.com/img.jpg" --transparent false --bg-color "255,255,255"

# 元素识别（检测主体水印+文字，返回OCR）
python scripts/alphashop_image.py detect-elements \
  --image-url "https://example.com/img.jpg" \
  --object-elements 1 3 --return-character

# 消除非主体水印和文字
python scripts/alphashop_image.py remove-elements \
  --image-url "https://example.com/img.jpg" \
  --noobj-watermark 1 --noobj-character 1

# 裁剪到800×800
python scripts/alphashop_image.py crop \
  --image-url "https://example.com/img.jpg" \
  --target-width 800 --target-height 800

# 虚拟试衣（指定模特+上装）
python scripts/alphashop_image.py virtual-try-on \
  --model-images "https://example.com/model.jpg" \
  --clothes "https://example.com/shirt.jpg,tops" --count 1

# 查询虚拟试衣结果
python scripts/alphashop_image.py query-try-on --task-id "abc123"

# 模特换肤（白人青年女性，自然背景）
python scripts/alphashop_image.py change-model \
  --image-url "https://example.com/img.jpg" \
  --model-type WHITE --bg-style NATURE --age YOUTH --gender FEMALE --num 2

# 查询模特换肤结果
python scripts/alphashop_image.py query-change-model --task-id "xyz456"
```

## 异步任务流程

虚拟试衣和模特换肤为异步接口：
1. 调用 `virtual-try-on` 或 `change-model` 提交任务，获得 `taskId`
2. 等待几秒后调用 `query-try-on` 或 `query-change-model` 查询结果
3. 如果任务未完成，等待后重试查询

## API 详细文档

完整参数说明见 `references/api-docs.md`。
