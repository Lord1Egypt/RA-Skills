---
name: cmclaw
version: "1.0.1"
display_name: "创意管家 AI 策略分析助手"
display_name_en: "Creative Manager AI Strategy Analysis Assistant"
description: >
  有米云创意管家 AI 策略分析：AI 驱动创意策略迭代，为你全方位分析第三方广告素材和自有待投放的广告素材，生成广告投放策略报告或持续碰撞，灵感激发。
  当用户需要广告投放策略分析、创意灵感激发、素材策略分析，或提到"创意管家"、
  "策略探索"、"灵感激发"、或使用 `/cmclaw` 时触发。
description_zh: "有米云创意管家 AI 策略分析：AI 驱动创意策略迭代，全方位分析第三方广告素材和自有待投放素材，生成广告投放策略报告或持续碰撞、灵感激发。触发词：创意管家、策略探索、灵感激发、投放策略分析、素材策略分析；命令：/cmclaw"
description_en: "YouCloud Creative Manager AI strategy analysis: AI-driven creative strategy iteration that comprehensively analyzes third-party ad creatives and your own creatives pending launch, generating ad placement strategy reports or ongoing brainstorming and inspiration. Triggers: keywords Creative Manager, strategy exploration, inspiration, creative analysis; command /cmclaw"
invocation: /cmclaw
emoji: 🎯
metadata:
  env:
    - YOUCLOUD_API_KEY
    - DAM_API_BASE
  credential: YOUCLOUD_API_KEY
  cli:
    - python3
---

# cmclaw — 创意管家 AI 策略分析

> 完整 API 接口文档（域名、请求/响应字段、流式协议、错误码）见 `references/cm-claw-api.md`。


## 权限说明
仅对 创意管家 已付费 且 非 **灵感版**的用户开放。获取API Key方式：登录 创意管家 → 个人中心 → 企业信息。

## 能力

- **策略探索**（`chat_mode=2`，默认）：直接输出完整投放策略报告。
- **灵感激发**（`chat_mode=3`）：多轮渐进追问，每轮流式返回增量 markdown。
- **多轮对话**：首轮建立 session，后续带 `session_id` 续聊。
- **素材限定**：在问题中 `@灵感库` / `@物料` / `@成片` / `@账户素材` / `@有数` / `@AppGrowing` 指定检索范围（软提示，后端不解析）。

## 执行流程

每次对话按以下步骤执行：

1. **素材范围引导**：检查用户提问是否包含 `@` 素材标签。
   - 若用户提问**没有**带任何 `@` 标签，**必须先向用户确认素材检索范围**。
   - **支持 AskUserQuestion 的平台**：通过弹窗分页引导，每页最多 4 个选项（含"下一页"）。
     - **第一页**：
       - 问题：你想探索哪些数据范围？
       - 选项：直接开始分析（不限定范围） | @灵感库 | @物料 | 下一页
     - 若用户选择"下一页"，弹出**第二页**：
       - 问题：你想探索哪些数据范围？
       - 选项：@成片 | @账户素材 | @有数 | @AppGrowing
     - 用户选择后，将对应标签拼接到用户原始提问末尾再发起 API 调用。
   - **不支持 AskUserQuestion 的平台**：直接输出以下文本提示，等待用户回复数字：
     > 请选择你要探索的数据范围（回复数字即可）：
     > 1. 直接开始分析（不限定范围）
     > 2. @灵感库
     > 3. @物料
     > 4. @成片
     > 5. @账户素材
     > 6. @有数
     > 7. @AppGrowing
     - 用户回复数字后，将对应标签拼接到用户原始提问末尾再发起 API 调用；若用户回复 1 则直接开始。
   - 若用户提问**已带** `@` 标签，跳过此步骤，直接进入下一步。
2. **取身份**：调 `GET /api/rpc/user/v1/user/userInfo:get`，拿到 `user_id` + `team_id` 并记住，后续对话复用。鉴权前缀为 `YC_API_KEY`（不是 `Bearer`）。
3. **发起对话**：调 `POST /api/rpc/ai/claw/v1/chat`，body 必须带 `user_id` + `team_id`。
   - 首轮：传 `chat_mode`（2 或 3），不传 `session_id`。用户意图为讨论、脑暴、创意发散时传 `chat_mode=3`，其余默认传 `chat_mode=2`。
   - 续聊：传上一轮首包返回的 `session_id`，不传 `chat_mode`。
4. **读流**：逐行解析 NDJSON，剥掉 `result` envelope，拼接非空的 `answer_content` 为完整 markdown，记住首包的 `session_id`。流结束后才能回复用户，不要在流未结束时输出半截结果。
5. **输出**：流结束后将完整 markdown 原样回复用户，保存 `session_id` 供后续追问。在完整 markdown 下方换行输出 Web 端对话详情链接：
   - 生产环境：`https://console.dam.youcloud.com/ai-strategy/chat-detail?chat_gid={session_id}` 
   - 根据 `DAM_API_BASE` 判断当前环境，拼接对应链接 -->
   - 输出格式：
     > 对话详情：{拼接的链接}
6. **⚠️ 强制红线规则（公共Skill必须严格遵守）**
   - 超时 ≥ 650s；后端不主动断流。错误处理（401/400/404/流中段错误等）见 `references/cm-claw-api.md`。
   - **🔴 绝对禁止：未到超时时间不得中断请求，不得提前给用户发送任何「正在处理」「需要等待」「结果出来后告诉你」这类消息**
   - **必须：一直等待后端返回结果，拿到完整结果后再一次性回复给用户**
   - 只有两种情况允许发消息：
     1. API返回了完整分析结果 → 直接输出结果
     2. API超时/请求报错 → 输出错误提示


## 调用方式

通过 `skill.py` 执行，无需手动构造 HTTP 请求。仅使用 Python 内置标准库，不依赖第三方包。环境变量：`YOUCLOUD_API_KEY`（必填）、`DAM_API_BASE`（可选，默认生产环境）。

```bash
# 首轮（策略探索）
python skill.py "分析这个美妆品牌的投放策略，重点 @灵感库"

# 首轮（灵感激发）
python skill.py "帮我找一些美妆广告创意灵感"

# 续聊（需修改 skill.py 传入 session_id）
```
