---
name: dlazy-chat
version: 1.2.0
description: 与 dlazy 沙箱 agent 对话 —— 一个以项目为单位、可端到端运行技能的多轮助手。用 dlazy skills list / dlazy projects list 发现可用技能与项目。
metadata:
  {
    'clawdbot':
      {
        'emoji': '🤖',
        'requires': { 'bins': ['npm', 'npx'] },
        'install': 'npm install -g @dlazy/cli@1.2.0',
        'installAlternative': 'npx @dlazy/cli@1.2.0',
        'homepage': 'https://github.com/dlazyai/cli',
        'source': 'https://github.com/dlazyai/cli',
        'author': 'dlazyai',
        'license': 'see-repo',
        'npm': 'https://www.npmjs.com/package/@dlazy/cli',
        'configLocation': '~/.dlazy/config.json',
        'apiEndpoints': ['api.dlazy.com', 'files.dlazy.com'],
      },
    'openclaw': { 'systemPrompt': '当调用此技能时，使用 `dlazy chat`；通过 `dlazy skills list` 和 `dlazy projects list` 发现 id。' },
  }
---

# dlazy-chat

[English](./SKILL.md) · [中文](./SKILL-cn.md)

与 dlazy 沙箱 agent 对话 —— 一个以项目为单位、可端到端运行技能的多轮助手。用 `dlazy skills list` / `dlazy projects list` 发现可用技能与项目。

## 触发关键词

- 对话、和 agent 聊
- 沙箱 agent、项目对话
- 继续某个项目、多轮任务

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
npx @dlazy/cli@1.2.0 <command>
```

如选择全局安装，技能的 `metadata.clawdbot.install` 字段已固定到 `npm install -g @dlazy/cli@1.2.0`。安装前建议先到 GitHub 仓库审阅源码。

## 工作原理

此技能是 dLazy 托管沙箱 agent 的轻量封装。调用时：

- 你发送的消息与参数会发送到 dLazy API（`api.dlazy.com`），agent 的回复会流式返回到终端。
- 通过 `--files` 附带的本地文件会先上传到 dLazy 媒体存储（`files.dlazy.com`），再以 url 形式引用。
- 会话按项目跟踪，后续多轮对话因此能保持上下文；项目与技能 id 来自 `dlazy projects list` / `dlazy skills list`。

这是标准的 SaaS 调用模式；技能本身不会越权访问网络或文件系统，所有动作都由 dLazy CLI 完成。完整服务条款请参见 [dlazy.com](https://dlazy.com)。

## 使用方法

此技能与 dlazy 沙箱 agent 对话 —— 一个以项目为单位、可端到端运行技能（模板）的助手。适用于对话式、多轮的工作，而非一次性生成。

### 发现技能与项目

```bash
# 列出可以用来开始对话的技能/模板
dlazy skills list

# 列出当前组织下已有的项目
dlazy projects list
```

### 开始或继续对话

```bash
# 根据提示词自动选择模板（会新建一个项目）
dlazy chat --prompt "做一个关于夜晚城市的三镜头分镜"

# 用指定技能/模板新建项目
dlazy chat --skill storyboard --prompt "..."

# 在已有项目里继续（指定后 --skill 失效）
dlazy chat --project <project_id> --prompt "..."

# 附带本地文件（会先上传到存储）
dlazy chat --project <project_id> --prompt "参考这张图" --files ref.png

# 会话控制
dlazy chat --project <project_id> --clear      # 清除已保存会话，重新开始
dlazy chat --project <project_id> --compact    # 压缩当前会话的上下文
```

在终端（TTY）下，`dlazy chat` 在首轮之后会进入交互模式 —— 直接输入后续消息，或输入 `exit` 退出。

> **智能体关键指令**:
>
> 1. 先运行 `dlazy skills list`（继续工作时再加 `dlazy projects list`）以获取有效的 id。
> 2. 新建项目用 `--skill`，继续已有项目用 `--project` —— 二者不可同时使用。
> 3. 非交互（无 TTY）运行时必须传 `--prompt`。
> 4. 运行 `dlazy chat -h` 查看全部参数。

## 错误处理

| Code | 错误类型                   | 示例信息                                                                                       |
| ---- | -------------------------- | ---------------------------------------------------------------------------------------------- |
| 401  | 未授权 (API Key缺失或无效) | `ok: false, code: "unauthorized", message: "API key is missing or invalid"`                    |
| 501  | 缺少必填参数               | `error: required option '--prompt <prompt>' not specified`                                     |
| 502  | 本地文件读取失败           | `Error: Image file/Video file not found: C:\path\to\your\file`                                 |
| 503  | API 请求失败（余额不足）   | `ok: false, code: "insufficient_balance"`                                                      |
| 503  | API 请求失败（服务端错误） | `HTTP status code error (500 server crash)`                                                    |
| 504  | 异步任务执行失败           | `=== Generation Failed ===` / `{后端返回的具体失败原因，比如 "Prompt violates safety policy"}` |

> **智能体关键指令**:
>
> 1. 如果执行结果返回 `code: "insufficient_balance"` 且提示余额不足（Insufficient balance），您必须明确告知用户当前积分不足，并引导用户点击以下链接前往充值：[https://dlazy.com/dashboard/organization/settings?tab=credits](https://dlazy.com/dashboard/organization/settings?tab=credits)
> 2. 如果执行结果返回 `code: "unauthorized"` 或提示缺少 API Key，您必须明确告知用户前往 [https://dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key) 获取 API Key 并使用 `dlazy auth set <key>` 保存，然后继续执行任务。

## Tips

Visit https://dlazy.com for more information.
