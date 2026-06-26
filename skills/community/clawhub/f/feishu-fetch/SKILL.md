---
name: feishu-fetch
description: "飞书文件下载：从收到的群消息中下载 file/image/audio 附件，使用 im/v1/messages/{id}/resources/{key} 端点。需要 curl、python3；运行时从 ~/.openclaw/openclaw.json 读取 (appId, appSecret)。仅调用 open.feishu.cn，不向任何第三方转发。授予 token 最小权限。"
metadata: {"openclaw":{"emoji":"📥","requires":{"anyBins":["curl","python3","bash"]}}}
---

# feishu-fetch

下载飞书群聊中收到的 file / image / audio 消息附件到本地。

## 何时使用

- 群里收到 file 消息，需要下载到本地处理
- 用户要求读取、转发、转换收到的附件
- `message.read` 工具对 file 消息只返回占位符，需要 fallback

**不**处理发送消息（那是另一个 skill 的事）。如果需要"下载-上传-转发"链路，本 skill 只负责下载第一步。

## 调用方式

**首选：通过脚本**

```bash
bash ~/.openclaw/skills/feishu-fetch/scripts/feishu-fetch.sh <message_id> [options]
```

或者在调用前 `export AGENT_NAME=<name>` 选择非 main 账户。

### 入参

| 参数 | 必填 | 说明 |
|---|---|---|
| `message_id` | ✅ | 飞书消息 ID（`om_xxx`）。**必须是 file/image/audio 消息本身**，不是 thread 里的文本 reply |
| `--type TYPE` | ❌ | 资源类型：`file` / `image` / `audio`（**默认 auto-detect**，从消息体读 msg_type） |
| `--output PATH` | ❌ | 输出文件路径（默认：`/tmp/<file_name>`，image 消息默认 `image_<key12>.jpg`） |
| `--agent NAME` | ❌ | 飞书账户名（默认：`$AGENT_NAME` 变量，回退 `main`） |
| `--print-key` | ❌ | 只打印 file_key/image_key 后退出（调试用，正常流程**不要**用） |
| `-h`, `--help` | ❌ | 显示帮助 |

**auto-detect**：不传 `--type` 时，脚本从消息 body 拿 `msg_type`，自动选 `file_key`（file/audio）或 `image_key`（image），并在下载 URL 用对应的 `?type=`。传了 `--type` 跟 `msg_type` 不一致会打 warning 但仍用用户传的值。

### 输出

| 通道 | 内容 |
|---|---|
| `stdout` | 成功：下载的本地文件**绝对路径** |
| `stderr` | 错误信息 |
| `exit 0` | 成功 |
| `exit 1` | API 错误 |
| `exit 2` | 参数错误 |
| `exit 3` | 消息不存在 / 已删除 |
| `exit 4` | 权限不足 |

### 示例

```bash
# 默认：下载 file 消息到 /tmp/<原文件名>
bash scripts/feishu-fetch.sh om_xxxxx

# 下载图片到指定路径
bash scripts/feishu-fetch.sh om_xxxxx --type image --output /tmp/photo.png

# auto-detect：不传 --type，脚本从消息 msg_type 推断
# 适用于收到一个消息但不知道是 file 还是 image 的场景
bash scripts/feishu-fetch.sh om_xxxxx --output /tmp/dl.bin

# 用非 main 账户（多 bot 场景）
AGENT_NAME=mala bash scripts/feishu-fetch.sh om_xxxxx

# 拿 key 而不下载（调试）
bash scripts/feishu-fetch.sh om_xxxxx --print-key
```

agent 拿 stdout 的路径继续后续处理（用 `image` 工具读图、`feishu-send` 转发等）。

## thread / reply 注意事项

用户用文本消息 reply 一条 file 消息时：

- **file 消息本体**在 thread root（`parent_id` / `root_id` 指向）
- reply 的**文本消息**里**没有** `file_key`

如果传进来的 message_id 拿不到 file_key：

1. **不要**反复试 reply 链
2. **重新定位** file 消息本身：`message.read` 取 reply 消息的 `root_id` → 用 root_id 调本 skill
3. 实在拿不到 → 提示用户"消息链断了，请直接给我 file 消息的 message_id"

## applink 链接

`https://applink.feishu.cn/client/message/link/open?token=*** ` 里的 token **没有**公开 API 反查到 message_id。

**解法**：
- 让用户**直接**给 message_id（最快）
- 或者用户**重新发送**文件到当前对话（不通过 reply 引用旧消息）
- 不要尝试 token 反查

## 凭据安全

**不**要：

- 把 `appId` / `appSecret` 硬编码在调用里 → **不**行，凭据必须从 `openclaw.json` 读
- 把 `file_key` / `token` 打印到日志 / 返回值 → 脚本已做，正常流程不会泄露
- 用裸 `curl -d` 把 secret 放命令行 → 脚本内部已用 stdin/临时文件，secret 不会出现在 `ps`

如果需要调试 file_key，用 `--print-key`（仅自己看，**不要**入日志）。

## 错误码速查

| 错误码 | 含义 | 修法 |
|---|---|---|
| `99992402 type is required` | 缺 `?type=` 参数 | 重跑时加 `--type file` |
| `99991663 token invalid` | appSecret 错 | 检查 `openclaw.json` |
| `230002 token not exist` | token 吊销 | 重跑（脚本自动重拿） |
| `230027 Lack of permissions` | scope 不够 | 后台勾 `im:resource`（tenant 级） |
| `230020 message not found` | message_id 错 / 跨 app / 已删 | 重新确认 message_id |

## 范围边界

**做**：file / image / audio 三类资源下载

**不做**：

- 发消息（用其他 skill）
- 读云文档 / Drive / Bitable / Wiki
- applink token 反查 message_id
- 后台进程、长连接、polling
- 转发到任何非 `open.feishu.cn` 的域

## 与其他 skill 组合

本 skill 完成后**可能**接入的下游：

- `feishu-send` —— 上传 + 转发到其他群
- `image` 工具 —— 读图（`--type image` 下载后）
- `pdf` 工具 —— 读 PDF

具体组合由调用方按需拼装，**本 skill 不假设任何特定下游**。

## 安全

- `appSecret` 仅运行时从磁盘读，**不**入日志、**不**入返回值
- 临时文件由脚本 `trap` 清理（退出后自动删）
- tenant_access_token 2 小时自动过期，无需手动 rotation
- 主机被入侵时**立即**在飞书开放平台重置 `appSecret`
- **最小权限**：飞书 app 后台只勾必要 scope（`im:resource` 等），不要 `*:read` 通配

## OpenClaw 内部凭据

读 `~/.openclaw/openclaw.json`：

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "<agent_name>": {
          "appId": "cli_xxx",
          "appSecret": "..."
        }
      }
    }
  }
}
```

agent 名字优先级：`--agent <name>` > `$AGENT_NAME` 环境变量 > `main` 兜底。
