# 通道配置指南

**适用于所有 OpenClaw 用户** - 无论使用什么通讯工具

---

## 📱 支持的通道类型

### 国内主流
| 通道 | 配置值 | 说明 |
|------|--------|------|
| 飞书 | `feishu` | 企业协作首选 ✅ |
| 微信 | `wechat` | 个人/工作混合 |
| 企业微信 | `wecom` | 企业办公 |
| 钉钉 | `dingtalk` | 企业办公 |

### 国际主流
| 通道 | 配置值 | 说明 |
|------|--------|------|
| Telegram | `telegram` | 国际团队首选 ✅ |
| Discord | `discord` | 开发者社区 |
| Slack | `slack` | 国际企业 |
| WhatsApp | `whatsapp` | 个人/小团队 |
| iMessage | `imessage` | Apple 生态 |

### Web 端
| 通道 | 配置值 | 说明 |
|------|--------|------|
| WebChat | `webchat` | OpenClaw 内置会话 |
| Matrix | `matrix` | 开源即时通讯 |

---

## ⚙️ 配置示例

### 示例 1：国内团队（飞书 + 微信）
```json
{
  "notification": {
    "channels": ["feishu", "wechat", "webchat"]
  }
}
```

### 示例 2：国际团队（Telegram + Slack）
```json
{
  "notification": {
    "channels": ["telegram", "slack", "webchat"]
  }
}
```

### 示例 3：混合团队（全通道）
```json
{
  "notification": {
    "channels": ["feishu", "wechat", "telegram", "discord", "slack", "imessage", "webchat"]
  }
}
```

### 示例 4：最小配置（仅 WebChat）
```json
{
  "notification": {
    "channels": ["webchat"]
  }
}
```

---

## 🔧 如何配置

### 步骤 1：确认你的 OpenClaw 通道
```bash
# 查看已配置的通道
openclaw channels list
```

### 步骤 2：编辑 config.json
```bash
# 编辑技能配置
cd ~/.openclaw/workspace/skills/doc-collaboration-watcher
vim examples/config.json
```

### 步骤 3：修改 channels 数组
```json
{
  "notification": {
    "channels": ["你的通道 1", "你的通道 2"]
  }
}
```

### 步骤 4：保存并重启
```bash
# 重启监控
python3 bin/doc-watcher.py restart
```

---

## ❓ 常见问题

### Q: 我的通道不在列表中怎么办？
A: OpenClaw 持续集成新通道。检查可用通道：
```bash
openclaw channels list
```

### Q: 可以只用部分通道吗？
A: 可以！只配置你需要的通道：
```json
{
  "notification": {
    "channels": ["feishu"]  // 只用飞书
  }
}
```

### Q: 多通道会重复通知吗？
A: 不会！每个通道只发送一次，避免重复。

### Q: 通道配置错误会怎样？
A: 监控会跳过不可用通道，继续发送其他通道。

---

## 🌍 全球用户适用

**无论你在哪里，使用什么工具，都能用！**

- 🇨🇳 中国大陆：飞书、微信、钉钉、企业微信
- 🇺🇸 北美：Slack、Discord、Telegram、iMessage
- 🇪🇺 欧洲：Telegram、WhatsApp、Slack、Matrix
- 🇯🇵 日本：LINE、Slack、Discord
- 🇰🇷 韩国：KakaoTalk、Slack
- 🌏 全球：WebChat（内置）

---

*本技能基于 OpenClaw 通道系统，自动适配所有支持的通讯工具*
