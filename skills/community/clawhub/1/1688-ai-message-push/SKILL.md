---
name: 1688-ai-message-push
description: |
  1688 AI 消息推送 Skill —— 向当前用户自己推送通知，支持微信通知和 APP 系统通知两种渠道。
  核心工具能力：微信通知推送（发给自己）、APP 系统通知推送（发给自己）。
  触发词：微信通知、发微信、微信推送、APP通知、系统通知、APP推送。
metadata: {"openclaw": {"emoji": "📨", "requires": {"bins": ["python3"]}, "primaryEnv": "ALI_1688_AK"}}
---

# 1688-ai-message-push

统一入口：`python3 {baseDir}/cli.py <command> [options]`

## 命令速查

| 命令 | 说明 | 示例 |
|------|------|------|
| `wx_push` | 发送微信通知 | `cli.py wx_push --text "您的订单已发货，请注意查收"` |
| `app_push` | 发送 APP 系统通知 | `cli.py app_push --text "您的订单已发货，请注意查收"` |
| `configure` | 配置 AK | `cli.py configure YOUR_AK` |

所有命令输出 JSON：`{"success": bool, "markdown": str, "data": {...}}`

**展示时直接输出 `markdown` 字段，Agent 分析追加在后面，不得混入其中。**

## 使用流程

Agent 根据用户意图**直接执行对应命令**。
各命令在 AK 缺失等情况下会自行返回明确错误，Agent 按下方「异常处理」应对即可。

**发送消息使用指引**：
- 当用户要求发送微信通知时，使用 `wx_push`
  - 若用户未提供通知内容，应先补齐：`text`
- 当用户要求发送 APP 系统通知时，使用 `app_push`
  - 若用户未提供通知内容，应先补齐：`text`

## 安全声明

| 风险级别 | 命令 | Agent 行为 |
|---------|------|-----------|
| **写入** | wx_push | 当通知内容明确时直接执行；内容缺失时先追问补齐 |
| **写入** | app_push | 当通知内容明确时直接执行；内容缺失时先追问补齐 |

**全局写入规则（适用于所有写操作）**：
1. 发送类操作属于写入，通知只会发送给用户自己，无需指定接收人。
2. 当通知内容明确时，可直接执行。
3. 当通知内容缺失时，先向用户追问补齐后再执行。
4. 不擅自扩写、改写用户希望发送的通知内容；如需润色，应明确告知并征得用户认可。

## 环境变量（.env）

项目根目录的 `.env` 文件存储 skill 基础信息，供埋点上报等模块读取。发布到不同环境时可直接替换该文件中的变量值。

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SKILL_NAME` | `1688-open-skill-template` | skill 名称 |
| `SKILL_VERSION` | `1.0.0` | skill 版本号 |
| `SKILL_CHANNEL` | `clawhubai` | 发布渠道 |

> 已存在的系统环境变量优先级高于 `.env`，CI/CD 注入的变量不会被覆盖。

## 埋点上报

每次 CLI 命令执行时，自动向 skill 网关上报一次调用记录，用于统计 skill 调用次数。

- **实现位置**：`scripts/_tracker.py` → `report_skill_usage()`，在 `cli.py` 的 `main()` 中每次命令执行后自动调用
- **上报接口**：`POST /api/alibaba.1688.report.skills.usage/1.0.0`
- **上报参数**：

  | 参数 | 值来源 | 说明 |
  |------|--------|------|
  | `apiName` | 固定 `null` | 固定传 null |
  | `skillsName` | `.env` `SKILL_NAME` | skill 名称 |
  | `version` | `.env` `SKILL_VERSION` | skill 版本号 |
  | `scene` | 固定 `CLI` | 固定值 |
  | `channel` | `.env` `SKILL_CHANNEL` | 发布渠道 |

- **失败处理**：上报失败静默忽略，不影响主流程

## 异常处理

任何命令输出 `success: false` 时：

1. **先输出 `markdown` 字段**（已包含用户可读的错误描述）
2. **再根据关键词追加引导**：

| markdown 关键词 | Agent 额外动作 |
|----------------|--------------|
| "AK 未配置" 或 "AK 无效或已过期" | 提示用户当前发送能力所需鉴权未就绪，请补充有效 AK 或检查鉴权配置后重试 |
| "该用户没有与AI业务类型机器人的有效好友关系" | 提示用户到1688AI版工作台绑定微信账号 |
| "请求参数不合法" | 提示用户补充缺失参数后重试 |
| "请求被限流" | 建议用户等待 1-2 分钟后重试 |
| 其他 | 仅输出 markdown 即可 |

## 执行前置（首次命中能力时必须）
- 首次执行 `configure` 前：先完整阅读 `references/capabilities/configure.md`
- 首次执行 `wx_push` 前：先完整阅读 `references/capabilities/wx_push.md`
- 首次执行 `app_push` 前：先完整阅读 `references/capabilities/app_push.md`

## 参数补齐引导话术

**微信通知**：
> "发送微信通知需要通知内容 text。你可以直接告诉我，例如：微信通知"您的订单已发货，请注意查收"。"

**APP 系统通知**：
> "发送 APP 系统通知需要通知内容 text。你可以直接告诉我，例如：APP 通知"您的订单已发货，请注意查收"。"