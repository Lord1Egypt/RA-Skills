---
name: chanjing-content-creation-skill
description: 蝉镜内容创作聚合技能包。提供凭据管理、TTS 语音合成、声音克隆、数字人口播、对口型、文生图/视频、定制数字人训练、一键成片编排、卡通视频编排等能力。当用户表达"做一个短视频""语音合成""数字人口播""一键成片""卡通视频"等意图时触发。副作用：HTTPS 访问蝉镜 Open API、读写本地凭据文件、下载、ffmpeg/ffprobe 子进程（仅成片链路）、可能打开浏览器引导登录。本 Skill 是路由入口，不直接执行业务；具体能力由子 products/ 与 orchestration/ 承载。
metadata:
  {"openclaw":{"homepage":"https://doc.chanjing.cc","os":["darwin","linux"],"requires":{"bins":["python3"],"anyBins":["ffmpeg","ffprobe"],"env":["CHANJING_APP_ID","CHANJING_SECRET_KEY"]}}}
---

# chanjing content creation skill

蝉镜内容创作技能包（顶层路由）

本文件只负责：触发边界、路由消歧、统一执行约束与运行时契约摘要。  
具体执行步骤以子技能 `*-SKILL.md` 为真值；长文细节以 `references/` 为真值。

## Use When

当用户需求涉及以下任一项时使用本 Skill：

- 短视频成片（含一键成片、卡通视频、口播混剪）
- 蝉镜语音能力（TTS、声音克隆）
- 数字人能力（公共/定制数字人、对口型、文生数字人）
- 蝉镜 AI 创作（文生图、文生视频）
- 蝉镜凭据管理（APP_ID/SECRET_KEY 配置、Token 刷新、登录引导）

## Do NOT Use

- 与蝉镜平台无关的通用需求（纯文案、非蝉镜剪辑工具等）
- 用户仅讨论方案且明确不执行任何蝉镜 API/脚本调用

## Route Map（唯一映射）

| 用户意图 | 路由目标 |
|---|---|
| 一键成片、完整短视频、做一个 xx 视频 | [`orchestration/chanjing-one-click-video-creation/chanjing-one-click-video-creation-SKILL.md`](orchestration/chanjing-one-click-video-creation/chanjing-one-click-video-creation-SKILL.md) |
| 卡通短剧、动漫多镜叙事 | [`orchestration/cartoon-video-creation/cartoon-video-creation-SKILL.md`](orchestration/cartoon-video-creation/cartoon-video-creation-SKILL.md) |
| 文字转语音、语音合成 | [`products/chanjing-tts/chanjing-tts-SKILL.md`](products/chanjing-tts/chanjing-tts-SKILL.md) |
| 声音克隆、音色复刻 | [`products/chanjing-tts-voice-clone/chanjing-tts-voice-clone-SKILL.md`](products/chanjing-tts-voice-clone/chanjing-tts-voice-clone-SKILL.md) |
| 对口型、唇形驱动（非卡通） | [`products/chanjing-avatar/chanjing-avatar-SKILL.md`](products/chanjing-avatar/chanjing-avatar-SKILL.md) |
| 数字人口播、公共数字人、纯口播视频、卡通数字人口播合成 | [`products/chanjing-video-compose/chanjing-video-compose-SKILL.md`](products/chanjing-video-compose/chanjing-video-compose-SKILL.md) |
| 文生图、创意视频 | [`products/chanjing-ai-creation/chanjing-ai-creation-SKILL.md`](products/chanjing-ai-creation/chanjing-ai-creation-SKILL.md) |
| 定制数字人（上传素材训练） | [`products/chanjing-customised-person/chanjing-customised-person-SKILL.md`](products/chanjing-customised-person/chanjing-customised-person-SKILL.md) |
| 人设图、人像 LoRA、文生数字人形象 | [`products/chanjing-text-to-digital-person/chanjing-text-to-digital-person-SKILL.md`](products/chanjing-text-to-digital-person/chanjing-text-to-digital-person-SKILL.md) |
| 凭据、APP_ID/SECRET_KEY、Token | [`products/chanjing-credentials-guard/chanjing-credentials-guard-SKILL.md`](products/chanjing-credentials-guard/chanjing-credentials-guard-SKILL.md) |

## Conflict Resolution（强制消歧）

出现重叠意图时，按以下优先级判定：

1. 完整成片（文案+分镜+画面+交付）优先路由 `chanjing-one-click-video-creation`
2. 卡通/动漫多镜叙事成片优先路由 `cartoon-video-creation`
3. 卡通数字人口播合成（`model=2`）或仅数字人口播，路由 `chanjing-video-compose`
4. 已有视频改口型（非卡通）路由 `chanjing-avatar`
5. 路由不确定时，遵循 [`orchestration/orchestration-contract.md`](orchestration/orchestration-contract.md) 的 `need_param` 分支最小补参

## Root Workflow（最小入口流程）

| Step | 动作 | 输出 | 下一步 | 失败分支 |
|---|---|---|---|---|
| 1 | 凭据可用性检查（缺失时走 `chanjing-credentials-guard`） | `ok` 或 `auth_required` | Step 2 | `auth_required`：先完成鉴权再回 Step 2 |
| 2 | 按 Route Map 选择单一目标子技能 | 目标 `*-SKILL.md` 路径 | Step 3 | `need_param`：只补路由必需信息 |
| 3 | 打开目标子技能并执行其 Standard Workflow | 子技能结果 | Step 4 | 按子技能失败分支执行 |
| 4 | 返回产物 URL/路径或标准错误语义 | `ok`/`need_param`/`auth_required`/`upstream_error`/`timeout` | 结束 | 需要降级跨产品时先征得用户确认 |

## Global Execution Rules

- 仅可调用 `products/*/scripts/` 与 `orchestration/*/scripts/` 的已有入口。
- 禁止自行编写临时脚本替代既有 CLI。
- 默认不主动下载；仅当用户明确要求“下载/保存到本地”时执行下载脚本。
- 重复任务可复用已确认参数，但当核心输入冲突时必须切换为新任务。
- 外部副作用（网络、写盘、子进程、浏览器）必须与运行时契约一致。

## Three-Layer Architecture

| 层级 | 路径 | 作用 |
|---|---|---|
| 顶层入口 | `SKILL.md` | 路由、消歧、契约摘要 |
| L1 公共层 | [`common/`](common/) | 公共鉴权、HTTP 封装、上传下载、日志 |
| L2 产品层 | [`products/`](products/) | 单产品能力与标准脚本 |
| L3 编排层 | [`orchestration/`](orchestration/) | 跨产品场景编排 |

依赖方向固定为：`common <- products <- orchestration`（禁止反向依赖）。

## Runtime Contract（摘要）

完整契约见 [`references/top-level-runtime-contract.md`](references/top-level-runtime-contract.md)。

- 凭据来源：项目 `.env`（`CHANJING_APP_ID`、`CHANJING_SECRET_KEY`）
- 凭据文件：`skills/chanjing-content-creation-skill/.env`
- Token 策略：不写入磁盘；按需请求并在当前进程内短时复用
- API 基址：`${CHANJING_API_BASE:-https://open-api.chanjing.cc}`
- 关键环境变量：`CHANJING_APP_ID`、`CHANJING_SECRET_KEY`、`CHANJING_ACCESS_TOKEN`、`CHANJING_TOKEN_EXPIRE_IN`、`CHANJING_API_BASE`、`CHAN_SKILLS_DIR`（其中 token 变量仅作为进程级可选输入，不持久化）
- 外部二进制：`python3`（所有脚本入口）、`ffmpeg`/`ffprobe`（主要用于 L3 成片链路）
- 副作用分类：出站 HTTPS、本地写入、子进程、浏览器引导登录

## Constraints

- 脚本写盘边界受运行时契约约束（凭据路径、`--output-dir`、`output/`、`work/`）。

