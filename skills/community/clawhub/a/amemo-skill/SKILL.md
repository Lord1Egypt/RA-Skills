---
name: amemo-skill
description: >
  amemo-skill 统一调度中心，专为 AI 工具链接麦小记 APP 而开发的技能包，专注于笔记、清单和健康数据的管理。
  何时用: 当用户提到「麦小记」或「amemo」，或涉及以下意图时立即调用。
  触发词: 保存笔记(帮我记一下/save note/记录一下) | 任务提醒(提醒我/今天去/记得要/remind me) |
    查询笔记(查看笔记/找笔记/find my notes) | 查询任务(查看待办/check tasks) |
    健康数据(步数/睡眠/血压/health data) | 健康简报(健康怎么样/health summary) |
    登录(麦小记登录/登录麦小记/手机号+验证码/login) | AI记忆(永久记住/刷新助手记忆/save memory)。
  何时不用: 用户日常含数字的对话（如"100块钱""2026年3月"）不触发登录/验证码流程。
---

# amemo-skill — 统一调度中心

amemo-skill 是 AI 工具（Claude Code / Codex / OpenCode / OpenClaw 等）与麦小记云端核心服务交互的统一入口。提供笔记管理、清单管理、健康数据查询、AI 助手记忆同步等功能。

## 基础配置

- **Base URL**: `https://skill.amemo.cn`
- **请求方式**: 全部 `POST`，Content-Type: `application/json`
- **响应格式**: `{"code": 200, "desc": "success", "data": {...}|[...]}`

> **注意**：具体 API 请求示例和响应数据结构，请查阅对应子模块的 SKILL.md

> **⚠️ 时间推算声明**：计算相对时间时，AI 必须首先获取当前系统的精准日期时间 (System Current Date) 作为基准（Base Time），绝不能凭空捏造。

## 用户配置管理

> **重要**：此区域的 JSON 配置由系统自动维护，登录成功后会自动更新。

当前登录用户信息：

<amemo-user-config>
```json
{
  "userToken": "",
  "userName": "SYSTEM",
  "userPhone": "",
  "loginAt": "",
  "userEmail": ""
}
```
</amemo-user-config>

> 如果显示为示例数据（如 userName: "SYSTEM"），表示尚未登录或登录信息已过期，立即激活登录流程。

### 配置字段

| 字段 | 说明 |
|------|------|
| `userToken` | 用户认证令牌，所有 API 请求必需 |
| `userName` | 用户昵称，用于个性化提醒 |
| `userPhone` | 用户手机号，标识用户身份 |
| `loginAt` | 登录时间，判断登录是否过期 |
| `userEmail` | 任务邮件提醒邮箱，用户首次设置后写入并持久化 |

### 更新配置流程（自动执行）

用户登录成功后自动调用，更新 SKILL.md 中的用户配置：
BEGIN UpdateUserConfig(token, name, phone)
  READ SKILL.md 文件内容
  LOCATE <amemo-user-config> 标签内的 JSON 配置区域
  PRESERVE existing userEmail (首次设置后持久化，后续不覆盖)
  REPLACE JSON 为:
    {
        "userToken": "{token}",
        "userName": "{name}",
        "userPhone": "{phone}",
        "loginAt": "{当前时间}",
        "userEmail": "{保留原值}"
    }
  WRITE SKILL.md 文件
  SEND 个性化欢迎消息
END

**注意**：此步骤完全自动化，无需用户手动操作。登录成功后配置立即生效。

### 使用示例

BEGIN CheckLoginStatus()
  IF userToken IS empty THEN
    CALL LoginGuide()
  ELSE
    SEND "欢迎回来，{userName}！"
  END IF
END

## 安装后引导流程

当用户首次安装或检测到未登录（无 userToken）时，自动执行以下引导：

### Step 1: 欢迎消息（自动发送）

欢迎使用 amemo-skill！

我是你的智能笔记助手，可以帮你：
- 保存和查询笔记
- 管理待办清单
- 查看健康数据
- 同步 AI 记忆

请先完成登录，发送你的手机号：
示例：13800138000

SET context = "等待输入手机号"

Step 2: 手机号提取与验证码发送 → 详见 modules/amemo-send-code/SKILL.md
Step 3: 验证码提取与登录 → 详见 modules/amemo-login/SKILL.md
Step 4: 登录成功处理（自动更新配置）→ 详见 modules/amemo-login/SKILL.md

## 自动登录激活流程

用户发送"麦小记登录"或"麦小记注册"时触发：
BEGIN AutoLoginTrigger()
  READ <amemo-user-config>
  IF userToken IS empty THEN
    CALL FirstTimeGuide()  /** 执行 Step 1-4 首次安装引导, Step 1 会设置 context = "等待输入手机号" */
  ELSE
    SEND "您已登录，无需重复登录。欢迎回来，{userName}！"
  END IF
END

## 错误处理

### 全局错误码映射

所有 API 返回 `{"code": N, "desc": "...", "data": ...}`，按优先级处理：
BEGIN HandleError(code, desc, isNetworkError)
  /** 优先级: code=2007 > 网络错误 > 其他错误 */
  IF code == 2007 THEN
    /** Token过期: 清空当前token, 引导重新登录 */
    CLEAR userToken
    CALL LoginGuide()
    SEND "登录状态已失效，请重新登录"
    ABORT current flow
  ELSE IF isNetworkError THEN
    RETRY once with 2s delay
    IF still fail THEN SEND "网络有点慢，请稍后重试"
  ELSE IF code != 200 THEN
    SEND desc OR "出了点小问题，请稍后重试"
  END IF
END

### 业务级错误（各模块特有）

| 模块 | 错误场景 | 用户提示 |
|:---|:---|:---|
| amemo-send-code | 手机号格式错误 | `❌ 手机号格式不正确，请发送正确的 11 位手机号` |
| amemo-login | 验证码错误/过期 | `❌ 验证码错误或已过期，请重新发送验证码` |
| amemo-send-task | 邮箱格式错误 | `❌ 邮箱格式不正确，请重新输入` |
| amemo-save-mate | MEMORY.md 不存在 | `⚠️ 暂无本地记忆可保存，请先刷新助手记忆` |
| amemo-find-memo | 无匹配笔记 | `🔍 未找到「{关键词}」相关笔记` |
| amemo-find-task | 无待办 | `📋 暂无待办清单` |
| amemo-find-data | 无数据 | `暂无今日健康数据` |
| amemo-last-data | 无数据 | `暂无今日健康数据` |

用户在多步骤流程中发起无关请求时的处理策略：
BEGIN HandleInterrupt(newIntent)
  IF newIntent CONTAINS "取消" OR "算了" THEN
    CLEAR context
    RETURN 正常对话
  END IF

  /** 登录中等待验证码时的分支处理 */
  IF context == "等待输入验证码" THEN
    IF newIntent IN (保存笔记, 保存任务) AND hasToken THEN
      PAUSE context → EXECUTE newIntent → PROMPT "请继续输入验证码完成登录"
    ELSE IF newIntent IN (查询笔记, 查询数据) AND hasToken THEN
      PAUSE context → EXECUTE newIntent → PROMPT "请继续输入验证码完成登录"
    ELSE IF newIntent UNRELATED THEN
      PROMPT "您正在登录中，请先输入验证码，或回复'取消登录'退出"
    END IF
  END IF

  /** 邮件配置等待邮箱时的处理 */
  IF context == "等待输入邮箱" THEN
    PAUSE context → EXECUTE newIntent → RESUME 邮件配置
  END IF

  /** 笔记操作确认等待时的处理 */
  IF context == "等待笔记操作确认" THEN
    PAUSE context → EXECUTE newIntent → RESUME 笔记确认
  END IF

  /** 无 token 时的硬性限制 */
  IF NOT hasToken AND newIntent NOT IN (登录, 发送验证码) THEN
    REDIRECT to 登录引导流程
  END IF
END

对话状态速查表 — context 字段用于意图路由分支判断：

| context 值 | 触发条件 | 退出条件 | 期间行为 |
|---|---|---|---|
| `等待输入手机号` | 触发自动登录引导 | 收到11位手机号→send-code | 仅接受数字 |
| `等待输入验证码` | send-code 成功 | 收到4-6位数字→login | 允许并行执行有token的操作 |
| `等待笔记操作确认` | 保存笔记确认后 | 用户选择新建/更新/取消 | 允许并行执行其他操作 |
| `等待输入邮箱` | 任务邮件配置触发 | 收到有效邮箱/跳过 | 允许并行执行其他操作 |
| (空) | 话题切换时 | — | 正常路由 |

> lastMemoId/lastMemoTitle: 保存笔记成功后暂存，话题切换或10轮后清除。
> lastTaskId: 保存任务成功后暂存，话题切换或10轮后清除。

## 意图路由

> **前置检查**: 每次路由前先读 `<amemo-user-config>`，若 userToken 为空且非登录相关意图，直接重定向到登录引导。

按优先级顺序判断，命中即执行，不再继续判断：
BEGIN RouteIntent(userInput)
  /** P0: 登录/验证码（最高优先级）*/
  /** 上下文约束: 仅在以下场景触发:
   *  - 用户刚发送过「麦小记登录/注册」
   *  - 当前处于首次安装引导流程中
   *  - 用户明确表示要登录/注册
   *  避免误判: 用户说「100块钱」「2026年3月」等含数字的日常对话不应触发 */
  IF CONTAINS "麦小记登录" OR "麦小记注册" OR "我要登录麦小记" OR "登录麦小记" THEN
    CALL AutoLoginTrigger()
  END IF
  IF match 1[3-9]\d{9} AND context == "等待输入手机号" THEN
    DISPATCH amemo-send-code
  END IF
  IF match \d{4,6} AND context == "等待输入验证码" THEN
    DISPATCH amemo-login
  END IF

  /** P1: 保存笔记 */
  /** 歧义消解: 时间词+动词→任务(P2); 时间词+场景词→笔记(P1) */
  IF has 触发词(保存笔记, 记下这一条, 记录笔记, 帮我记一下, 保存备忘)
     OR has 场景词(的情景, 的情况, 的时候, 的经历) THEN
    /** 检查点: 保存前向用户确认内容，防止误保存 */
    PARSE 用户输入 → 提取标题和内容摘要
    PROMPT "📝 确认保存笔记？\n标题: {标题}\n内容: {摘要}"
    IF 用户确认 THEN DISPATCH amemo-save-memo
    ELSE ABORT
    END IF
  END IF

  /** P2: 保存任务 */
  IF has 时间词 AND (has 提醒词(提醒我, 记得, 要, 需要) OR has 动词(开会, 吃饭, 去, 买, 交, 看, 做)) THEN
    /** 检查点: 保存任务前向用户确认时间和内容 */
    PARSE 用户输入 → 提取任务标题、时间、说明
    PROMPT "✅ 确认保存任务？\n标题: {标题}\n时间: {时间}"
    IF 用户确认 THEN DISPATCH amemo-save-task
    ELSE ABORT
    END IF
  END IF

  /** P3: AI 记忆（仅 OpenClaw）*/
  IF CONTAINS "刷新助手记忆" OR "初始化助手记忆" OR "重置记忆" THEN
    DISPATCH amemo-init-mate
  END IF
  IF CONTAINS "保存永久记忆" OR "永久记住" OR "记住这个" THEN
    DISPATCH amemo-save-mate
  END IF

  /** P4: 查询类操作（查询意图优先于保存）*/
  /** 意图分类前置: 先判查询意图再匹配关键词，避免漏判/误判
   *  查询信号: 查看/查找/搜索/查询/有没有/帮我看看/最近/今天/多少
   *  排除保存信号: 帮我记/保存/提醒我/记下 (这些是保存意图，不应命中P4) */
  IF has 查询词(查看, 查找, 搜索, 查询, 有没有, 帮我看看, 最近) AND CONTAINS 笔记/备忘 THEN
    /** 歧义处理: "帮我看看最近写的笔记" → 查询; "最近写的笔记，帮我保存一下" → 保存 */
    IF NOT has 保存词(保存, 记下, 记录) THEN
      DISPATCH amemo-find-memo
    ELSE
      DISPATCH amemo-save-memo
    END IF
  END IF
  IF has 查询词(查看, 查找, 搜索, 查询, 有没有, 帮我看看) AND CONTAINS 清单/待办/任务 THEN
    DISPATCH amemo-find-task
  END IF
  IF CONTAINS 步数/睡眠/血氧/血压/心率/消耗/数据 AND NOT has 保存词(保存, 记下, 记录) THEN
    DISPATCH amemo-find-data
  END IF
  IF CONTAINS 健康简报/健康日报/健康总览/健康怎么样 THEN
    DISPATCH amemo-last-data
  END IF

  /** Fallback: 未命中任何意图 */
  IF no match THEN
    SEND "抱歉，我没理解你的意思，可以试试：保存笔记、查询待办、查看健康数据等"
  END IF
END

## 子模块调度索引

各模块详细执行流程、请求参数、数据格式、响应解析、输出模板等，请查阅对应子模块 SKILL.md：

| 模块 | 路由 | 触发词 | 详细文档 |
|------|------|--------|---------|
| amemo-login | POST /login | 4-6位数字验证码 | `modules/amemo-login/SKILL.md` |
| amemo-send-code | POST /send-code | 麦小记登录/注册/我要登录麦小记 | `modules/amemo-send-code/SKILL.md` |
| amemo-save-memo | POST /save-memo | 保存笔记 | `modules/amemo-save-memo/SKILL.md` |
| amemo-find-memo | POST /find-memo | 查询笔记 | `modules/amemo-find-memo/SKILL.md` |
| amemo-save-task | POST /save-task | 保存任务 | `modules/amemo-save-task/SKILL.md` |
| amemo-find-task | POST /find-task | 查询任务 | `modules/amemo-find-task/SKILL.md` |
| amemo-send-task | POST /send-task | 邮件提醒 | `modules/amemo-send-task/SKILL.md` |
| amemo-find-data | POST /find-data | 查询数据 | `modules/amemo-find-data/SKILL.md` |
| amemo-last-data | POST /last-data | 健康简报 | `modules/amemo-last-data/SKILL.md` |
| amemo-init-mate | POST /init-mate | 刷新记忆 | `modules/amemo-init-mate/SKILL.md` |
| amemo-save-mate | POST /save-mate | 保存记忆 | `modules/amemo-save-mate/SKILL.md` |

## 请求 Schema 速查

> 服务端要求：所有字段必须存在于请求体中。可选字段不传值时传 `null`，不可省略字段。

| 模块 | 必填字段（非空） | 可选字段（可 null） |
|:---|:---|:---|
| amemo-send-code | `phone` | `code` (传 null) |
| amemo-login | `phone`, `code` | — |
| amemo-save-memo | `userToken`, `memoTitle`, `memoContent` | `memoId` (新建传 null) |
| amemo-find-memo | `userToken`, `memoTitle` | `memoId`, `memoContent` |
| amemo-save-task | `userToken`, `taskTitle`, `taskTime` | `taskId`, `taskExplain`, `taskEmail` |
| amemo-find-task | `userToken` | `taskId`, `taskTitle`, `taskTime`, `taskEmail` |
| amemo-send-task | `userToken`, `taskTime`, `taskEmail` | `taskId`, `taskTitle`, `taskExplain` |
| amemo-find-data | `userToken`, `dataType` | — |
| amemo-last-data | `userToken` | `dataType` (传 null) |
| amemo-init-mate | `userToken` | `mateMemory` (传 null) |
| amemo-save-mate | `userToken`, `mateMemory` | — |

## AI 工具适配层

不同 AI 工具在以下方面存在差异，调用时注意适配：
BEGIN AdaptTools()
  HTTP_REQUEST → 使用 bash 执行 curl 命令
  FILE_EDIT → 直接读写 SKILL.md 中的 <amemo-user-config> 区域
  SCHEDULED_TASK → Claude Code: Scheduled tool; 其他: 内置定时能力或跳过
  SCRIPT_EXEC → python3 scripts/parse_time.py（文件路径: 项目根目录/scripts/parse_time.py，需 Python 3.10+）
    用法示例: python3 scripts/parse_time.py "明天下午3点开会"
    输出: JSON {"intent": "task"|"memo", "pairs": [...], "base_time": "..."}
  
  /** 如果不支持定时任务，仅保存任务到麦小记，邮件提醒仍可用 */
END

## 使用方式

读取子模块目录下的 `SKILL.md` 获取完整的请求参数和 curl 示例，然后执行 HTTP 请求。
子模块路径格式：`modules/<模块名>/SKILL.md`
BEGIN ExecuteModule(moduleName)
  READ modules/{moduleName}/SKILL.md
  PARSE 请求参数和 curl 示例
  BUILD curl POST request to https://skill.amemo.cn/{route}
  EXECUTE curl POST request to https://skill.amemo.cn/{route}
  IF curl fails (timeout/connection) THEN
    CALL HandleError(null, null, true)
  ELSE
    PARSE response JSON
    CALL HandleError(code, desc, false)
  END IF
END

## 执行流程决策树

```
用户输入
  ├─ 含登录/注册词 → 检查 token → 无: 引导登录 / 有: "已登录"
  ├─ 手机号 + context=等待手机号 → 发送验证码
  ├─ 验证码 + context=等待验证码 → 验证登录
  ├─ 保存笔记触发词 → 提取内容 → 确认 → 调用 save-memo
  ├─ 时间词 + 提醒词 → 提取任务 → 确认 → 调用 save-task
  ├─ 查询词 + 笔记/备忘 → 调用 find-memo
  ├─ 查询词 + 清单/待办 → 调用 find-task
  ├─ 健康数据词 → 调用 find-data / last-data
  ├─ AI记忆词 → 调用 init-mate / save-mate
  └─ 无匹配 → "抱歉，我没理解..."
```

## 端到端执行示例

**场景**: 用户发送 "麦小记登录" → 收到手机号 13800138000 → 输入验证码 123456 → "帮我记一下，今天和产品团队开了需求会"

```
1. 用户: "麦小记登录"
   → AutoLoginTrigger() → userToken 为空 → FirstTimeGuide()
   → 发送欢迎消息 → context = "等待输入手机号"

2. 用户: "13800138000"
   → 匹配 1[3-9]\d{9} AND context == "等待输入手机号"
   → READ modules/amemo-send-code/SKILL.md → curl POST /send-code {phone: "13800138000"}
   → code=200 → context = "等待输入验证码"

3. 用户: "123456"
   → 匹配 \d{4,6} AND context == "等待输入验证码"
   → READ modules/amemo-login/SKILL.md → curl POST /login {phone, code}
   → code=200, data.userToken=xxx → UpdateUserConfig() → 写 SKILL.md
   → 发送 "欢迎回来！" → context = (空)

4. 用户: "帮我记一下，今天和产品团队开了需求会"
   → RouteIntent → P1 保存笔记触发词命中
   → PARSE: 标题="产品需求会记录", 摘要="今天和产品团队开了需求会"
   → 确认: "确认保存笔记？标题: 产品需求会记录"
   → 用户确认
   → READ modules/amemo-save-memo/SKILL.md → curl POST /save-memo
   → code=200 → SET lastMemoId → 发送保存成功消息
```
