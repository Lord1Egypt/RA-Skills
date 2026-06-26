---
name: dingtalk-channel-install
description: 安装和配置 OpenClaw 钉钉通道。使用当用户需要：(1) 安装 @soimy/dingtalk 插件，(2) 配置钉钉通道（Client ID/Secret 等），(3) 设置钉钉机器人连接。提供一键安装脚本和完整配置流程。
---

# 钉钉通道安装配置

快速安装和配置 OpenClaw 钉钉通道，实现钉钉与 OpenClaw 的双向通信。

## ⚠️ 安全提示

**切勿将真实的 Client ID/Secret 提交到代码仓库！** 示例中的凭证均为占位符，请替换为你自己的凭证。

## 快速开始

### 方式一：使用安装脚本（推荐）

```bash
python3 ~/.openclaw/workspace/my-skills/skills/dingtalk-channel-install/scripts/install_dingtalk.py \
  --client-id <你的 Client ID> \
  --client-secret <你的 Client Secret>
```

### 方式二：手动安装

1. **安装插件**
   ```bash
   openclaw plugins install @soimy/dingtalk
   ```

2. **配置 channels** - 编辑 `~/.openclaw/openclaw.json`：
   ```json
   {
     "channels": {
       "dingtalk": {
         "enabled": true,
         "clientId": "<你的 Client ID>",
         "clientSecret": "<你的 Client Secret>",
         "dmPolicy": "open",
         "groupPolicy": "open",
         "showThinking": true,
         "thinkingMessage": "🤔 思考中，请稍候...",
         "debug": false,
         "messageType": "markdown",
         "allowFrom": ["*"]
       }
     }
   }
   ```

3. **重启 Gateway**
   ```bash
   openclaw gateway restart
   ```

## 脚本参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--client-id` | ✅ | 钉钉应用 Client ID |
| `--client-secret` | ✅ | 钉钉应用 Client Secret |
| `--robot-code` | ❌ | 机器人 Code |
| `--corp-id` | ❌ | 企业 Corp ID |
| `--agent-id` | ❌ | 应用 Agent ID |
| `--card-template-id` | ❌ | 卡片模板 ID（仅 card 模式） |
| `--card-template-key` | ❌ | 卡片模板内容变量（仅 card 模式） |
| `--message-type` | ❌ | 消息类型：markdown/card，默认 markdown |
| `--skip-restart` | ❌ | 跳过 gateway 重启 |
| `--config-path` | ❌ | 配置文件路径，默认 `~/.openclaw/openclaw.json` |

## 完整示例

### 基础配置（markdown 消息）

```bash
python3 ~/.openclaw/workspace/my-skills/skills/dingtalk-channel-install/scripts/install_dingtalk.py \
  --client-id <你的 Client ID> \
  --client-secret <你的 Client Secret>
```

### 卡片消息模式

```bash
python3 ~/.openclaw/workspace/my-skills/skills/dingtalk-channel-install/scripts/install_dingtalk.py \
  --client-id <clientId> \
  --client-secret <clientSecret> \
  --message-type card \
  --card-template-id <模板 ID> \
  --card-template-key <模板变量>
```

### 企业应用模式（带 corpId 和 agentId）

```bash
python3 ~/.openclaw/workspace/my-skills/skills/dingtalk-channel-install/scripts/install_dingtalk.py \
  --client-id <clientId> \
  --client-secret <clientSecret> \
  --corp-id <corpId> \
  --agent-id <agentId>
```

## 配置说明

### 必填配置

- **clientId**: 钉钉应用的唯一标识
- **clientSecret**: 应用密钥，用于身份验证

### 可选配置

- **dmPolicy**: `"open"` 允许私聊，`"restricted"` 限制私聊
- **groupPolicy**: `"open"` 允许群聊，`"restricted"` 限制群聊
- **allowFrom**: 允许的聊天来源，`["*"]` 表示允许所有
- **messageType**: `"markdown"` 或 `"card"`
- **showThinking**: 是否显示思考状态
- **debug**: 调试模式

## 验证安装

1. 检查插件状态：
   ```bash
   openclaw plugins list
   ```

2. 检查配置：
   ```bash
   openclaw gateway status
   ```

3. 在钉钉中添加机器人并发送消息测试

## 故障排查

### 插件重复警告

```
plugins.entries.dingtalk: plugin dingtalk: duplicate plugin id detected
```

这是正常警告，不影响使用。如需清理，删除重复的插件目录后重启。

### 配置验证失败

运行 `openclaw doctor --fix` 自动修复配置问题。

### 消息无法发送

1. 检查 Client ID/Secret 是否正确
2. 确认钉钉应用已配置机器人
3. 检查 `allowFrom` 设置是否匹配 `dmPolicy`/`groupPolicy`

## 参考资源

- [钉钉开放平台](https://open.dingtalk.com/)
- [OpenClaw 钉钉通道文档](https://github.com/soimy/openclaw-channel-dingtalk)
