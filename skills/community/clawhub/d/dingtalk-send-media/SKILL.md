---
name: dingtalk-send-media
description: 发送钉钉媒体文件给用户或群聊。仅在用户明确要求把本地文件、截图、录音、视频、附件发送到钉钉，或当前上下文已明确是钉钉会话时使用。通过 `scripts/send_media.py` 执行，支持 image/voice/video/file 等。
metadata:
  {
    "openclaw":
      {
        "emoji": "📤",
        "requires": { "anyBins": ["python", "python3"] },
      },
  }
---

# DingTalk Send Media

使用同目录脚本 `scripts/send_media.py` 发送钉钉媒体消息。OpenClaw 不会自动执行目录中的 `.py` 文件；命中本 skill 后，应显式调用脚本。

## 触发场景

在这些场景使用本 skill：

- 用户要求把本地文件、图片、截图、录音、视频、压缩包发到钉钉
- 用户要求发送给某个钉钉用户 ID，或发送到某个钉钉群 ID
- 当前上下文已明确是钉钉账号或钉钉会话，且目标是“发送附件”

不要在这些场景使用本 skill：

- 用户想编辑钉钉文档正文或知识库内容
- 用户只说“发给他”但没有文件路径、目标 ID，且上下文无法补全
- 与钉钉无关的发送场景，例如邮件附件、飞书文件、Slack 上传

## 运行前提

脚本依赖 `python` 或 `python3`。

可用配置来源：

1. 环境变量 `DINGTALK_CLIENTID` + `DINGTALK_CLIENTSECRET`，优先级最高
2. `openclaw.json` 中的 `channels.dingtalk.accounts`
3. `openclaw.json` 中的 `channels.dingtalk-connector.accounts`
4. `openclaw.json` 中的 `channels.dingtalk-connector` 顶层凭证

相关环境变量：

- `DINGTALK_CLIENTID`
- `DINGTALK_CLIENTSECRET`
- `DINGTALK_ROBOTCODE`
- `DINGTALK_CORPID`
- `DINGTALK_AGENTID`
- `OPENCLAW_AGENT_ID`
- `OPENCLAW_ACCOUNT_ID`
- `OPENCLAW_CONFIG`

## 执行入口

脚本文件：`scripts/send_media.py`

执行时使用绝对路径，形式如下：

```bash
python /absolute/path/to/scripts/send_media.py <file-path> <target-id> [account-id] [media-type] [--group|--user] [--debug]
```

在 Linux 或 macOS 上，如果只有 `python3`，使用：

```bash
python3 /absolute/path/to/scripts/send_media.py <file-path> <target-id> [account-id] [media-type] [--group|--user] [--debug]
```

## 发送前检查

执行前尽量确认这些信息：

- 文件路径存在，且是本机可访问的绝对路径
- 目标 ID 是钉钉用户 ID，或以 `cid` 开头的群 ID
- 如果存在多个钉钉账号，确认应该使用哪个账号
- 如果用户没有指定媒体类型，可以让脚本自动检测
- 默认会将 `cid...` 自动识别为群聊；如需覆盖，可使用 `--group` 或 `--user`

## 命令映射

### 1. 自动检测账号并发送

适用：

- 当前只有一个账号
- 或者已能从 `OPENCLAW_AGENT_ID` / `OPENCLAW_ACCOUNT_ID` / bindings 推导账号

执行：

```bash
python /absolute/path/to/scripts/send_media.py <file-path> <target-id>
```

说明：

- 若 `target-id` 以 `cid` 开头，脚本会自动按群聊发送
- 其他目标默认按单聊发送

### 2. 指定账号发送

适用：

- 存在多个钉钉账号
- 用户明确要求用某个账号发送

执行：

```bash
python /absolute/path/to/scripts/send_media.py <file-path> <target-id> <account-id>
```

### 3. 指定媒体类型发送

适用：

- 自动检测类型不可靠
- 用户明确要求按图片、语音、视频或普通文件发送

执行：

```bash
python /absolute/path/to/scripts/send_media.py <file-path> <target-id> <account-id-or-type> [media-type]
```

媒体类型仅允许：

- `image`
- `voice`
- `video`
- `file`

### 4. 显式指定群聊或单聊

适用：

- 目标 ID 规则不稳定，不能只靠 `cid` 判断
- 你想覆盖自动检测结果

执行：

```bash
python /absolute/path/to/scripts/send_media.py <file-path> <target-id> [account-id] [media-type] --group
python /absolute/path/to/scripts/send_media.py <file-path> <target-id> [account-id] [media-type] --user
```

### 5. 调试模式

适用：

- 账号检测或配置选择异常

执行：

```bash
python /absolute/path/to/scripts/send_media.py <file-path> <target-id> --debug
```

## 工作流程

1. 确认目标是钉钉发送媒体，而不是文档编辑。
2. 提取文件路径和目标 ID。
3. 如有多个账号或上下文不明确，优先确认账号。
4. 执行脚本。
5. 若脚本返回 `ok: true`，向用户报告已发送的文件名、目标和账号。
6. 若脚本返回 `ok: false`，根据错误内容给出下一步说明。

## 常见错误

- `未找到 OpenClaw 配置文件 openclaw.json`：当前无配置文件，需提供环境变量凭证或配置文件
- `未找到钉钉账号配置`：账号自动检测失败，需显式指定账号或补齐配置
- `获取 access token 失败`：检查 `clientId` / `clientSecret`
- `上传媒体文件失败`：检查文件路径、大小、媒体类型和上传权限
- `发送消息失败`：检查目标用户 ID / 群 ID、机器人权限和 `robotCode`

## 限制

- 本 skill 用于发送媒体，不用于编辑钉钉文档内容
- 需要本机已有可发送的文件路径
- 群聊发送要求目标是合法 `cid...`
- 多账号场景下，若无法唯一推导账号，可能需要显式传入 `account-id`

## 参考

- 人工说明文档：`README.md`
- 实际执行脚本：`scripts/send_media.py`