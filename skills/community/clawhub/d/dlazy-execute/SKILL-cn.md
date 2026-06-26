---
name: dlazy-execute
version: 1.1.1
description: 执行 plan 输出的扁平节点列表。按 `shape://name:<X>` 引用计算依赖顺序，依次通过 /api/ai/tool 调度每个 shape；上游产物的 url 会替换到下游 input 中相应字段，`promptRefs` 引用的文本会被拼接到消费者的 `prompt` 前面。重要：只有 `props.status === "idle"` 的 shape 才会真正执行；其它状态（`completed` / `failed` / `processing`）一律视为已完成，其当前的 `props.url` 被作为产物供下游引用。若上次执行中途失败，可将失败节点（以及任何需要重跑的节点）的 status 改回 `idle`，可选地修改 `props.input`，再次调用 execute 即可从失败位置继续。
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["npm","npx"]},"install":"npm install -g @dlazy/cli@1.0.9","installAlternative":"npx @dlazy/cli@1.0.9","homepage":"https://github.com/dlazyai/cli","source":"https://github.com/dlazyai/cli","author":"dlazyai","license":"see-repo","npm":"https://www.npmjs.com/package/@dlazy/cli","configLocation":"~/.dlazy/config.json","apiEndpoints":["api.dlazy.com","files.dlazy.com"]},"openclaw":{"systemPrompt":"当调用此技能时，可以使用 dlazy execute -h 查看帮助信息。"}}
---

# dlazy-execute

[English](./SKILL.md) · [中文](./SKILL-cn.md)


执行 plan 输出的扁平节点列表。按 `shape://name:<X>` 引用计算依赖顺序，依次通过 /api/ai/tool 调度每个 shape；上游产物的 url 会替换到下游 input 中相应字段，`promptRefs` 引用的文本会被拼接到消费者的 `prompt` 前面。重要：只有 `props.status === "idle"` 的 shape 才会真正执行；其它状态（`completed` / `failed` / `processing`）一律视为已完成，其当前的 `props.url` 被作为产物供下游引用。若上次执行中途失败，可将失败节点（以及任何需要重跑的节点）的 status 改回 `idle`，可选地修改 `props.input`，再次调用 execute 即可从失败位置继续。

## 触发关键词

- execute

## 身份验证 (Authentication)

所有请求都需要 dLazy API key。**推荐使用** `dlazy login` 完成登录：

```bash
dlazy login
```

该命令使用设备码流程（远程终端也可用），登录成功后 **自动把 API key 写入本地 CLI 配置**，无需手动复制粘贴。

### 备选：手动设置 API Key

如果你已有 API key，也可以直接保存：

```bash
dlazy auth set YOUR_API_KEY
```

CLI 会把 key 保存在你的用户配置目录（macOS/Linux 上为 `~/.dlazy/config.json`，Windows 上为 `%USERPROFILE%\.dlazy\config.json`），文件权限仅限当前操作系统用户访问。你也可以用 `DLAZY_API_KEY` 环境变量按次传入。

### 手动获取 API Key

1. 登录或在 [dlazy.com](https://dlazy.com) 创建账号
2. 访问 [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. 复制 API Key 区域显示的密钥

每个 key 都属于你自己的 dLazy 组织，可在同一控制面板**随时轮换或吊销**。

## 关于与来源 (Provenance)

- **CLI 源代码**: [github.com/dlazyai/cli](https://github.com/dlazyai/cli)
- **维护者**: dlazyai
- **npm 包名**: `@dlazy/cli`（本技能 install 字段固定到 `1.0.9` 版本）
- **官网**: [dlazy.com](https://dlazy.com)

如果你不希望在系统上长期保留一个全局 CLI，可以按需运行：

```bash
npx @dlazy/cli@1.0.9 <command>
```

如选择全局安装，技能的 `metadata.clawdbot.install` 字段已固定到 `npm install -g @dlazy/cli@1.0.9`。安装前建议先到 GitHub 仓库审阅源码。

## 工作原理

此技能是 dLazy 托管 API 的轻量封装。调用时：

- 你提供的提示词与参数会发送到 dLazy API（`api.dlazy.com`）进行推理。
- 传入图像 / 视频 / 音频字段的本地文件路径会被 CLI 上传到 dLazy 媒体存储（`files.dlazy.com`），以便模型读取 —— 与任何云端生成 API 的流程一致。
- API 返回的生成结果 URL 由 `files.dlazy.com` 托管。

这是标准的 SaaS 调用模式；技能本身不会越权访问网络或文件系统，所有动作都由 dLazy CLI 完成。完整服务条款请参见 [dlazy.com](https://dlazy.com)。

## 使用方法

**CRITICAL INSTRUCTION FOR AGENT**:
执行 `dlazy execute` 命令获取结果。

```bash
dlazy execute -h

Options:
  --shapes [shapes...]                 Flat shape list to execute (typically plan.shapes). Cross-shape references inside `props.input` use either `shape://name:<name>` (resolves to the producer matching `props.name`) or `shape://shape:<id>` (resolves to the producer matching `id`); refs whose target is not in this array are dropped as if the param were absent. Each shape's `props.status` controls scheduling: only `idle` shapes run; shapes with any other status are treated as already-done and their `props.url` is reused as the producer output for downstream refs. To resume a failed run, set the failed/affected shapes back to `idle` (optionally edit their `props.input`) and call execute again.
  --projectId [projectId]              Optional project id forwarded to every downstream tool call (used for asset scoping and credit accounting).
  --sessionId [sessionId]              Optional execution session id; pass the same value across resume attempts so logs can be correlated.
  --dry-run                            Print payload + cost estimate without calling API
  --no-wait                            Return generateId immediately for async tasks
  --timeout <seconds>                  Max seconds to wait for async completion (default: "1800")
  -h, --help                           display help for command
```

> Any flag also accepts pipe references — `-` (auto-pick from upstream stdin), `@N` (n-th output), `@N.path` (jsonpath into output), `@*` (all primary values), `@stdin` / `@stdin:path` (whole envelope). See `dlazy --help` for details.

## 输出格式

```json
{
  "ok": true,
  "result": {
    "tool": "execute",
    "modelId": "execute",
    "outputs": [
      {
        "type": "shape",
        "id": "o_xxxxxxxx",
        "shape": {}
      }
    ]
  }
}
```

> Async tasks (when `--no-wait` is passed) return `outputs: []` and a `task: { generateId, status }` field instead. Use `dlazy status <generateId> --wait` to poll.

## 命令示例

```bash
dlazy execute --prompt '提示词内容'
```

## 错误处理

| Code | 错误类型                         | 示例信息                                                                                                                 |
| ---- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 401  | 未授权 (API Key缺失或无效)       | `ok: false, code: "unauthorized", message: "API key is missing or invalid"`                                                              |
| 501  | 缺少必填参数                     | `error: required option '--prompt <prompt>' not specified`                                                               |
| 502  | 本地文件读取失败                 | `Error: Image file/Video file not found: C:\path\to\your\file`                                                           |
| 503  | API 请求失败（余额不足）         | `ok: false, code: "insufficient_balance"` |
| 503  | API 请求失败（服务端错误）       | `HTTP status code error (500 server crash)`                                                                              |
| 504  | 异步任务执行失败                 | `=== Generation Failed ===` / `{后端返回的具体失败原因，比如 "Prompt violates safety policy"}`                             |

> **智能体关键指令**: 
> 1. 如果执行结果返回 `code: "insufficient_balance"` 且提示余额不足（Insufficient balance），您必须明确告知用户当前积分不足，并引导用户点击以下链接前往充值：[https://dlazy.com/dashboard/organization/settings?tab=credits](https://dlazy.com/dashboard/organization/settings?tab=credits)
> 2. 如果执行结果返回 `code: "unauthorized"` 或提示缺少 API Key，您必须明确告知用户前往 [https://dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key) 获取 API Key 并使用 `dlazy auth set <key>` 保存，然后继续执行任务。

## Tips

Visit https://dlazy.com for more information.