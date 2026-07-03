---
name: ecommerce-video-generator
description: AI视频脚本提炼与视频生成器（国际化电商视频管线 Skill3）。读取分镜脚本JSON，AI压缩至2000字以内，提取时长和产品参考图，构建视频生成请求payload并提交aigc API。当用户已完成分镜脚本生成、需要渲染最终视频时触发。
version: 1.1.0
license: MIT
compatibility: opencode
metadata:
  category: e-commerce-video
  workflow: AI短视频生成管线-Skill3
  openclaw:
    requires:
      env:
        - AIGC_APP_KEY
        - AIGC_APP_SECRET
      bins:
        - python3
---

# 国际化电商视频生成 — Skill3：AI视频脚本提炼与AI视频生成

## 管线定位

```
Skill1 基图生成器 → product_layer.png + selling_points.json（含product_function + user_pain_point）
                    ↓
Skill2 分镜脚本生成器 → storyboard.json（含镜头脚本+时长+产品参考图）
                    ↓
Skill3 AI视频生成器 ← 本技能
  输入: Storyboard JSON + 产品白底图
  处理: AI压缩脚本至≤2000字 + 提取总时长 + 产品图转URL
  输出: video_payload.json（模型ID/脚本/参考图/时长/分辨率/比例）
```

## 核心流程

```
Storyboard JSON（Skill2输出）
    │
    ├─ 提取 镜头脚本[] → format_script_text() → 原始脚本文本
    ├─ 提取 单镜时长 → 累加 → total_duration (≥5s)
    ├─ 提取 {产品名}产品参考图 → 产品图路径 → local_to_url() → data URI
    │
    ├─ 原始脚本 > 2000字？
    │   ├─ 是 → compress_script() → AI精简至≤2000字（保留全部核心内容）
    │   └─ 否 → 直接使用原始脚本
    │
    └─ 构建 payload → {
         modelId, prompt (压缩后脚本),
         imageMode: "REFERENCE",
         content: [{fileUrl: 产品图dataURI, role: "product"}],
         resolution: "720p", ratio: "9:16",
         duration: total_duration, count: 1
       }
          │
          ├─ 预览模式（默认）→ 保存video_payload.json
          └─ 提交模式（--submit）→ POST /openapi/call/generation/video
```

## 输入参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--script` | 是 | Skill2输出的分镜脚本JSON路径 |
| `--product` | 否 | 产品白底图路径（不填则从脚本JSON的`{产品名}产品参考图`字段提取） |
| `--output` | 否 | 输出目录（默认./output） |
| `--submit` | 否 | 提交视频生成（默认预览模式只构建payload不提交） |

## 输出文件

| 文件 | 说明 |
|------|------|
| `compressed_script.txt` | 压缩后的脚本文本（≤2000字） |
| `video_payload.json` | 视频生成请求payload（含modelId/prompt/content/resolution/ratio/duration） |

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `AIGC_APP_KEY` | 是 | aigc API 应用 Key |
| `AIGC_APP_SECRET` | 是 | aigc API 应用 Secret |
| `SUDOCODE_API_KEY` | 否 | Sudocode API Key（用于AI脚本压缩，无则降级规则截断） |
| `AIGC_API_BASE` | 否 | API 基础地址（默认 https://aigc.hkttok.com） |

## 输出目录规则

- **默认路径**：桌面 `AI视频脚本` 文件夹（自动创建）
- **自定义路径**：通过 `--output` 参数指定
- **聊天环境**：同时输出 Markdown 结果到聊天窗口 + 保存文件到输出目录

## 压缩策略

- 原始脚本 ≤2000 字 → 不压缩，直接使用
- 原始脚本 >2000 字 → 调用 Sudocode gpt-5.4-mini 最小幅度精简，保留全部镜头核心内容
- AI不可用时 → 智能截断（每镜等比例保留）

## 使用方式

```bash
# 预览模式（默认，输出到桌面AI视频脚本文件夹）
python {baseDir}/scripts/generate_video.py \
  --script ./storyboard.json \
  --product ./product_layer.png

# 提交模式（需配置AIGC_APP_KEY/AIGC_APP_SECRET环境变量）
python {baseDir}/scripts/generate_video.py \
  --script ./storyboard.json \
  --product ./product_layer.png \
  --submit

# ArkClaw 聊天环境（使用{baseDir}和{image_path}变量）
python {baseDir}/scripts/generate_video.py \
  --script "{baseDir}/output/storyboard.json" \
  --product "{image_path}" \
  --submit

---
## 管线串联（重要 — AI 执行流程）

本 Skill 是国际化电商视频生成管线的 **最终环节**。

### 执行前检查

本 Skill 依赖上游输出：
- `storyboard.json` — Skill2 的分镜脚本（通过 `--script` 传入）
- `product_layer.png` — Skill1 的产品白底图（通过 `--product` 传入）

> **注意:** `usage_instructions` 字段仅在 Skill1→Skill2 间传递，Skill3 不涉及此字段。

如果文件不存在，提示用户先执行 Skill1 和 Skill2。

### 执行完成后

1. **告知用户结果**：输出目录、生成文件列表、payload 摘要
2. **告知用户视频生成状态**：预览模式（payload 已保存）或已提交（task_id）

### 上下游说明

| 方向 | 技能 | 仓库 |
|------|------|------|
| ⬆ 上游 | `ecommerce-product-info-generator` | `https://github.com/BStory28/ecommerce-product-info-generator` |
| ⬆ 上游 | `ecommerce-video-script-generator` | `https://github.com/BStory28/ecommerce-video-script-generator` |
| ⬇ 下游 | 无（本技能是最终环节） | — |
```
