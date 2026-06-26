---
name: ai-product-space
version: 1.0.0
author: ai-product-space
description: "上传一张产品白底图，AI 自动生成电商全套素材：商品主图、场景图、卖点海报、营销文案与 8 秒展示视频。Generate full ecommerce assets from a single product photo."
triggers:
  - 电商素材
  - 商品图
  - 生成产品图
  - 卖点海报
  - product images
  - ecommerce assets
  - generate product
  - product video
auth:
  type: oauth
  provider: ai-product-space
tools:
  - create_space
  - upload_product_image
  - run_ecommerce_pipeline
  - generate_single_image
  - generate_video
  - get_space_status
  - list_assets
---

# AI Product Space Skill

将 AI Product Space 的电商素材生成能力接入 OpenClaw。一张白底产品图即可自动生成商品主图、场景图、卖点海报、营销文案和展示视频。

## 授权

首次使用时，OpenClaw 会自动弹出浏览器窗口引导你登录并授权。点击「允许」即可完成一键连接，无需手动配置 API Key。

如需手动配置（离线环境），在 `config.json` 中填入：

```json
{
  "APS_BASE_URL": "https://renshevy.com",
  "APS_API_KEY": "aps_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

API Key 可在 AI Product Space 的「设置 → API 密钥」页面创建。

## 工具说明

### create_space
创建新的工作空间。每个产品建议一个独立空间。
- `name`（可选）: 空间名称，建议用产品名

### upload_product_image
上传产品白底图到工作空间。支持本地路径或 URL。
- `space_id`（必填）: 空间 ID
- `image_path`: 本地图片路径
- `image_url`: 图片 URL（二选一）

### run_ecommerce_pipeline
运行全套电商素材生成流水线，一键生成 20+ 张商品图和多段文案。
- `space_id`（必填）: 空间 ID
- `language`: 输出语言（zh/en/ja/ko 等 10 种）
- `wait`: 是否等待完成（默认 true，约需 2-5 分钟）

### generate_single_image
根据自定义 Prompt 生成单张商品图。
- `space_id`（必填）: 空间 ID
- `prompt`（必填）: 图片描述
- `count`: 生成数量（1-4）

### generate_video
从商品图生成 8 秒展示视频。
- `space_id`（必填）: 空间 ID
- `image_urls`（必填）: 1-2 张图片 URL
- `prompt`: 运镜/风格描述
- `wait`: 是否等待完成（默认 true，约需 1-3 分钟）

### get_space_status
查看空间状态和流水线进度。
- `space_id`（必填）: 空间 ID

### list_assets
浏览已生成的素材资源。
- `folder_id`（可选）: 文件夹 ID

## 典型使用流程

### 完整流水线（推荐）

```
用户: 帮我生成蓝牙耳机的电商素材

1. create_space → 创建 "蓝牙耳机" 空间
2. （请用户提供产品图）
3. upload_product_image → 上传白底图
4. run_ecommerce_pipeline → 运行全套生成
5. 返回生成结果摘要
```

### 单张图片生成

```
用户: 帮我生成一张场景图，蓝牙耳机放在书桌上

1. generate_single_image → 使用自定义 prompt 生成
2. 返回图片链接
```

### 视频生成

```
用户: 把这张商品图做成视频

1. generate_video → 提交图片生成视频
2. 返回视频链接
```

## 注意事项

- 生成流水线需要消耗积分，请确保账户余额充足
- 上传的图片建议为白底产品图，效果最佳
- 流水线生成通常需要 2-5 分钟，视频生成需要 1-3 分钟
- 支持 10 种输出语言：中文、英语、日语、韩语、法语、德语、西班牙语、葡萄牙语、阿拉伯语、俄语
