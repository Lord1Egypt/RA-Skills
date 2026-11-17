---

name: free-media-gen
description: "免费文生图/文生视频：直连 Agnes、商汤 SenseNova、硅基流动 Kolors 等第三方免费模型，绕过混元 ImageGen、出图无水印。触发：打开免费生媒体 / 免费生图 / 免费生视频。 Free text-to-image & text-to-video: directly calls free third-party models (Agnes, SenseNova, SiliconFlow Kolors); bypasses Hunyuan ImageGen, no watermark."
version: 1.1.0
author: iGenomed
license: MIT
category: productivity
tags:
  - workbuddy
  - free-media-gen
  - image-generation
  - text-to-video
  - free-api
homepage: https://www.workbuddy.cn
metadata:
  openclaw:
    requires:
      bins:
        - python3
      config:
        - "~/.workbuddy/models.json"
        - "<skill_dir>/config.json"
      env: []
    envVars:
      - name: WORKBUDDY_CONFIG_DIR
        required: false
        description: "WorkBuddy 配置根目录（含 models.json）；未设置则回退 ~/.workbuddy"
      - name: CODEBUDDY_CONFIG_DIR
        required: false
        description: "WorkBuddy 配置根兜底目录；未设置则回退 ~/.workbuddy"
    primaryEnv: ""
    os:
      - windows
      - macos
      - linux
    homepage: https://www.workbuddy.cn
---

# 免费生图 / 生视频（free-media-gen）

## 功能概述

一个统一入口，聚合用户已在 WorkBuddy「自定义模型」（`models.json`）中配置好的各平台密钥下，
所有**免费**的图像 / 视频生成模型。本技能**刻意不调用**内置的混元 ImageGen 工具，
因此产出不带 "Workbuddy" 水印，用哪个后端完全由用户决定。

设计要点：

- **可移植**：不写死任何绝对路径，运行时自动解析，任何用户安装即用。
- **密钥复用**：媒体模型通过 `api_key_ref` 复用 `models.json` 中已有的平台密钥，不重复保存明文。
- **首装引导**：若用户没有任何可用平台密钥，会引导其去申请，而不是空跑报错。

## 何时使用

- 一级命令：**"打开免费生媒体"**
- 二级命令：`用 Agnes 生图 <提示词>`、`用商汤生图 <提示词>`、`用 Kolors 生图 <提示词>`、
  `用 Agnes 生视频 <提示词>`
- 用户提到"免费生图/生视频"、"不要 Workbuddy 水印"、"换一个生图后端"

> 若用户一句话里已指定后端与提示词（如"用 Agnes 生图 一只猫"），**跳过菜单直接执行**。

## 启动必做：路径自动解析

本技能会分发给不同用户，各人的 WorkBuddy **配置根**与**工作区根**位置不同。
**严禁写死绝对路径**（不要把作者本机的配置/工作区目录写进命令），一律用 `resolve_paths.py` 解析。

```bash
python {{SKILL_DIR}}/references/resolve_paths.py [--workspace <目录>] [--skill <目录>]
```

输出 JSON，含 `models_json`（配置根下的模型注册表）、`workspace_root`、`outputs_dir`、
`generated_images_dir`、`skill_dir`、`config_json`。解析优先级：

- **配置根**：`$WORKBUDDY_CONFIG_DIR` → `$CODEBUDDY_CONFIG_DIR` → `~/.workbuddy`
- **工作区根**：`--workspace` 参数 → 当前工作目录
- **技能目录**：`--skill` 参数 → 由脚本自身位置推导

后续步骤一律用占位符替换：
`{{MODELS_JSON}}` / `{{WORKSPACE_ROOT}}` / `{{SKILL_DIR}}` / `{{OUTPUTS}}`。

> 可移植说明：未配置上述环境变量的用户会自动回退到 `~/.workbuddy` 与自己打开的工作区目录，
> 无需为任何用户单独改配置。

## 工作流：一级命令「打开免费生媒体」

### 第 0 步 — 首装自检（决定走哪个分支）

先做路径解析，再检查 `{{MODELS_JSON}}` 中是否存在**任意**条目，其 `url` 主机属于可服务媒体的平台
（`api.agnes-ai.cn`、`token.sensenova.cn`、`api.siliconflow.cn`）。

**分支 B — 一个都没有**：不要报错、不要空跑。直接输出申请引导并结束本轮：

> 未检测到可服务免费生图/生视频的平台密钥。请到以下站点申请免费 API，
> 并在 WorkBuddy「自定义模型」中配置后，再次执行 **打开免费生媒体**：
> 
> | 提供商              | 免费媒体能力                    | 申请地址                               |
> | ---------------- | ------------------------- | ---------------------------------- |
> | Agnes            | 图 + 视频                    | https://agnes-ai.cn                |
> | 商汤 SenseNova     | 图（U1.5 Lite / U1 Fast）    | https://www.sensenova.cn           |
> | 硅基流动 SiliconFlow | 图（Kolors 免费）              | https://cloud.siliconflow.cn       |

**分支 A — 至少一个**：继续第 1 步。

### 第 1 步 — 输出模型清单（含简要特性）

读取 `{{SKILL_DIR}}/config.json`，输出表格：**模型 / 平台 / 模态 / 免费 / 需 VPN / 特点 /
二级命令示例**。

- 主表只列 **`free == true` 且 `status != "dead"`** 的模型（本技能定位是**免费**生媒体）。
- 对 `free == false` 或 `status == "paid"` 的条目，
  在表格下方另设"当前不可用 / 已转付费"一节说明原因，**不要**混入可用清单。

### 第 2 步 — 弹窗选择（AskUserQuestion）

弹出两个选项：

1. **继续使用** → 关闭选择，回到对话框，等用户输入二级命令。
2. **审计（更新）模型状态** → 执行第 3 步。

### 第 3 步 — 审计（仅在用户选择时执行）

```bash
python {{SKILL_DIR}}/scripts/media_auditor.py [--no-live] --workspace {{WORKSPACE_ROOT}}
```

- 拉取各平台 `/v1/models` 目录，筛出媒体类候选（跳过 `excluded_models` 中的已知付费项）。
- 对新增图像候选做活体生成测试（`--no-live` 可跳过以省额度）。
- 更新 `{{SKILL_DIR}}/config.json` 的 `status` 字段。
- 输出 `{{WORKSPACE_ROOT}}/免费生图生视频模型审计_YYYY-MM-DD.md`（滚动更新，只保留一份）。
- 完成后**回到对话框**，等候二级命令。

## 工作流：二级命令（执行生成）

按后端选择脚本，`--out` 默认落到 `{{OUTPUTS}}` 或 `generated_images`：

| 二级命令关键词   | 脚本                                                                                       |
| --------- | ---------------------------------------------------------------------------------------- |
| Agnes 生图  | `scripts/agnes_image.py --model agnes-image-2.1-flash --prompt "..." [--size 1024x1024]` |
| Agnes 生视频 | `scripts/agnes_video.py --model agnes-video-v2.0 --prompt "..." [--timeout 300]`         |
| 商汤生图      | `scripts/sensenova_image.py --model sensenova-u1.5-lite --prompt "..." [--size]`         |
| Kolors 生图 | `scripts/kolors_image.py --model Kwai-Kolors/Kolors --prompt "..." [--size]`             |

所有脚本输出 JSON（成功 `{"ok":true,"saved":[...]}`，失败 `ok:false` 并带 `error`）。
成功后用 `present_files` 展示生成的文件。

### Agnes 视频是异步的（重要）

提交后会先输出 `stage: submitted` 与 `task_id`，随后轮询到完成并自动两步取片：

1. `GET /v1/videos/<task_id>` → 取 `video_id`（**≠ task_id**）
2. `GET /agnesapi?video_id=<video_id>&model_name=<model>` → `metadata.url` 即 MP4 直链
   （**必须带 `model_name`**，否则该字段不返回）

若中途被打断，可用 `scripts/agnes_video.py --task-id <任务id> --model <模型id>` 单独取片。

> 注意：`agnes-video-2.5-flash` 走的是**新版接口**——`POST /v1/videos`，且必填
> `mode`（text / keyframe / reference）、`size` 固定 `"720P"`；与旧版 `v2.0` 不兼容，
> 脚本已自动分支，无需手工区分。

## 错误处理

| 情况                        | 处理                                                |
| ------------------------- | ------------------------------------------------- |
| HTTP 401 / 403            | 密钥无效或该平台未开通此模型 → 提示检查 key 与模型权限                   |
| HTTP 402                  | 该模型已转付费 → 在 `config.json` 标 `status:"paid"` 并告知用户 |
| HTTP 429                  | 限流 → 退避重试，切勿删除条目                                  |
| 5xx / 超时                  | 瞬态错误，脚本已内置指数退避重试                                  |
| 未知模型 id                   | 提示可用模型清单，或建议执行审计                                  |

## 安全与运维

- **密钥**：`models.json` 中的 key 为明文存储，建议定期在平台控制台轮换。
- **不污染聊天注册表**：媒体模型只写本技能的 `config.json`，**绝不写入 `models.json`**
  （媒体模型不是对话补全模型，混写会导致客户端报错）。
- **不调用混元 ImageGen**：本技能全部走自带脚本直连第三方端点。
- **按需审计**：每次一级命令时询问是否审计；**不做**定期自动化。
- **跨设备同步**：本技能目录纳入 `workbuddy-cross-sync` 同步。

## 文件结构

```
{{SKILL_DIR}}/
├── SKILL.md
├── config.json              媒体模型注册表（含 excluded_models 排除名单）
├── scripts/
│   ├── _common.py           路径解析 + 密钥解析 + HTTP/下载工具
│   ├── agnes_image.py       Agnes 文生图
│   ├── agnes_video.py       Agnes 文生视频（新旧两套接口，含两步取片）
│   ├── sensenova_image.py   商汤文生图（可去水印）
│   ├── kolors_image.py      硅基流动 Kolors 文生图
│   └── media_auditor.py     媒体模型审计（输出带日期报告）
├── references/
│   ├── resolve_paths.py     跨用户路径自解析
│   ├── platforms.md         各平台端点 / 限流 / 实测注意事项
│   └── model_catalog.md     已知模型清单 + 申请引导
└── templates/
    └── audit_report.md      审计报告模板
```

## Changelog

### v1.0.0（首发，2026-08-28）

- 聚合 Agnes / 商汤 SenseNova / 硅基流动 Kolors 三个平台的免费生图与（Agnes）生视频能力。
- 刻意不调用混元 ImageGen，出图不带 Workbuddy 水印。
- 密钥复用 `models.json` 中已有平台密钥，不重复保存明文。
- 跨用户可移植：运行时自动解析配置根 / 工作区根，无硬编码绝对路径。
- 首装自检：无可用密钥时输出 3 家免费平台申请引导。
- 按需审计：一级命令可触发模型清单审计，输出带日期 Markdown 报告。
