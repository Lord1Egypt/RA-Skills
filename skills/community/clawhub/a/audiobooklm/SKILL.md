---
name: audiobooklm
description: AudioBookLM 有声创作平台 skill。用于播客生成、单播有声书、多播有声书、多人演播、章节合成、角色音色绑定、混音上架等任务；通过 audiobooklm_mcp 调用远端工具。
homepage: https://aigc.ximalaya.com
source: https://aigc.ximalaya.com/audiobooklm/mcp
author: AudiobookLM
---

# audiobooklm

AudioBookLM 的唯一 skill 入口。这个文件只负责 MCP 接入、自检、通用原则和任务路由；具体创作流程放在同目录子文件中，按需读取。

不要一次性读取所有子文件。根据用户意图，只加载当前任务需要的 workflow。

---

## 强制 Skill 边界（必须遵守）

1. 有声书生产任务只允许使用当前目录下的 `*.md` skill 文件：
   - workflow：`podcast.md`，`multicast.md`
2. 禁止使用模型记忆、临时拼接、外部未声明文档来“自行组装”生产流程。
3. 未命中上述同级 skill 文件时，必须停止执行并要求用户明确选择可用 workflow，不得继续调用写操作 MCP。
4. 发生规则冲突时只允许按以下优先级执行：`workflow > reference > 停止执行并询问用户`。
5. 在进入生产前必须先向用户声明：

```text
我将严格按 audiobooklm/<workflow>.md 执行，不使用未定义流程。
```

---

## 安装后提示 / 首次使用提示

首次使用或用户询问安装结果时，先向用户说明：

```text
AudioBookLM skill 已安装成功。

我可以帮你完成以下有声创作任务：
- 播客创作：单人播客、多人播客、主持人/嘉宾对话、口语化节目。
- 多播有声书：识别旁白和角色对白，为多角色绑定音色并生成章节音频。

使用前请先到 https://aigc.ximalaya.com/user/center 登录，并在用户中心创建 API Token。
拿到 Token 后，将它配置为 AUDIOBOOKLM_TOKEN 或 MCP Authorization Bearer Token。
```

如果用户已经配置并确认 MCP 可用，不要重复展示完整安装提示，直接进入任务处理。

---

## 目录

```text
audiobooklm/
  SKILL.md
  podcast.md
  multicast.md
```

---

## 强制自检

在询问书名、章节、文本来源等业务问题前，必须先确认 MCP 可用。

可用以下任一方式：

1. 检查当前会话是否存在 `mcp__audiobooklm_mcp__*` 工具。
2. 调用轻量只读工具，例如 `list_tts_voices(exclude_role_voice=True)` 或 `read_abs(scope={"domain":"books"})`。

处理规则：

| 状态 | 处理 |
|---|---|
| 工具存在且调用正常 | 继续识别用户意图 |
| 找不到 `audiobooklm_mcp` 工具 | 提示用户配置 MCP 和 token，停止业务追问 |
| 返回 401/403/invalid_token/unauthorized | 提示 token 无效或过期，停止业务操作 |
| 连接失败或超时 | 提示服务不可达或网络异常，停止写操作 |

MCP 地址：

```text
https://aigc.ximalaya.com/audiobooklm/mcp
```

Bearer 直连配置示例：

```jsonc
{
  "mcpServers": {
    "audiobooklm_mcp": {
      "type": "http",
      "url": "https://aigc.ximalaya.com/audiobooklm/mcp",
      "headers": {
        "Authorization": "Bearer <AUDIOBOOKLM_TOKEN>"
      }
    }
  }
}
```

---

## 通用原则

1. 所有书籍、章节、角色、音色、任务、音频 URL 结论必须来自本轮真实工具返回，禁止编造。
2. 写操作必须使用真实 `book_id`、`chapter_id`、`character_id`、`speaker_id`，禁止使用占位符。
3. 调用成功不等于业务成功。若工具返回 `success=false`、`code!=20000/200000`、`status=failed` 或错误文本，必须按失败处理。
4. 不向用户输出原始大段 JSON；整理为自然语言，但保留关键 ID、标题、URL、错误信息。
5. 涉及版权、隐私、未授权文本或敏感个人信息时，先提醒用户确认授权。
6. 写 ABS 前优先做对象定位和必要确认；高风险批量写入可先 `dry_run=true`。
7. 不为完成流程自动改写用户原文。改写、口语化、删改内容必须得到用户明确要求。

---

## 任务路由（强制门禁）

执行任何生产写操作前，必须先通过以下门禁：

1. 识别用户意图。
2. 仅从同级 workflow 中选择一个入口文件。
3. 明确告知用户“本次将使用哪个 workflow 文件”。
4. 只按该 workflow 执行。

若无法匹配到下表中的 workflow，必须停止并让用户在可用 workflow 中选择，不得继续执行写操作。

| 用户意图 | 必须读取文件 |
|---|---|
| 播客生成、播客制作、单人播客、主持人/嘉宾对话、口语化节目 | `podcast.md` |
| 多播有声书、多人演播、多角色、旁白加对白、广播剧式小说 | `multicast.md` |

规则冲突时：优先遵循 workflow；workflow 未说明时，必须停下来询问用户，不得自行补流程。

---

## 常用组合

播客制作：

```text
读取 podcast.md
```

```

多播有声书：

```text
读取 multicast.md
```

## 输出规范

面向用户只输出关键信息：

- 书籍、章节、角色、音色、任务的真实 ID。
- 音频、编辑页、专辑页等真实 URL。
- 成功/失败的业务状态。
- 需要用户确认或补充的下一步。

不要输出：

- token、cookie、Authorization header。
- 大段原始 JSON。
- 本地调试路径。
- 未经工具返回确认的推断 URL。
