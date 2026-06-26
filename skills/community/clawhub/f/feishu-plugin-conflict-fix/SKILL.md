---
name: feishu-plugin-conflict-fix
description: |
  飞书插件工具冲突修复工具。解决 feishu_chat 命名冲突、TTS 语音配置、多 Bot 工具隔离等问题。

  **当以下情况时使用此 Skill**：
  (1) feishu_chat 工具命名冲突
  (2) 飞书发送信息附带 MP3 语音
  (3) 需要多 Bot 工具隔离配置
  (4) openclaw-lark vs 内置飞书技能冲突
  (5) 用户提到"飞书冲突"、"工具冲突"、"TTS 语音"
---

# 🔧 飞书插件冲突修复指南

## 版本信息

- **版本**: v1.0.0
- **作者**: 郑宇航
- **适用场景**: 飞书插件冲突排查与修复

---

## 🚨 常见问题快速索引

| 问题 | 解决方案 | 难度 |
|------|----------|------|
| feishu_chat 工具冲突 | [方案 1](#方案 1-工具命名冲突) | ⭐⭐ |
| 发送信息附带 MP3 | [方案 2](#方案 2-tts-语音配置) | ⭐ |
| 多 Bot 工具混乱 | [方案 3](#方案 3-多-bot-隔离) | ⭐⭐⭐ |

---

## 💡 核心解决方案

### 方案 1: 工具命名冲突

**症状**: `feishu_chat` 工具命名冲突 (openclaw-lark vs 内置飞书技能)

**原因分析**:
- 官方插件 `@larksuite/openclaw-lark` 提供 `feishu_chat`
- 内置飞书技能也提供 `feishu_chat`
- 工具名冲突导致调用错误

**解决步骤**:

```bash
# 1. 查看已加载的插件
openclaw plugins list

# 2. 查看工具列表
openclaw tools list | grep feishu

# 3. 禁用冲突插件
# 方案 A: 禁用内置飞书技能
openclaw config set plugins.entries.feishu.enabled false

# 方案 B: 禁用官方插件
openclaw config set plugins.entries.feishu-openclaw-plugin.enabled false

# 4. 重启 OpenClaw
openclaw gateway restart

# 5. 验证工具
openclaw tools list | grep feishu_chat
```

**使用工具**: `feishu_calendar_event`, `feishu_im_user_message`, `feishu_search_user`

**推荐配置**:
```json
{
  "plugins": {
    "entries": {
      "feishu": { "enabled": false },
      "feishu-openclaw-plugin": { "enabled": true }
    }
  }
}
```

**期望输出**:
```
✅ 已禁用内置 feishu 插件
✅ 官方插件 feishu-openclaw-plugin 已启用
✅ 工具冲突已解决
```

---

### 方案 2: TTS 语音配置

**症状**: 飞书发送信息后附带 MP3 语音文件

**原因**: TTS (Text-to-Speech) 功能默认开启

**关闭 TTS**:

```bash
# 1. 查看当前 TTS 配置
openclaw config get channels.feishu.tts

# 2. 关闭 TTS
openclaw config set channels.feishu.tts.enabled false

# 3. 重启 OpenClaw
openclaw gateway restart
```

**配置选项**:

```json
{
  "channels": {
    "feishu": {
      "tts": {
        "enabled": false,
        "provider": "azure",
        "voice": "zh-CN-XiaoxiaoNeural",
        "auto_play": false
      }
    }
  }
}
```

**使用工具**: `tts`, `feishu_im_user_message`

---

### 方案 3: 多 Bot 隔离

**症状**: 多个 Bot 工具混乱，无法区分

**解决方案**: 配置工具前缀隔离

**步骤**:

```bash
# 1. 为不同 Bot 配置不同前缀
openclaw config set agents.bot1.tool_prefix "bot1_"
openclaw config set agents.bot2.tool_prefix "bot2_"

# 2. 配置工具可见性
openclaw config set agents.bot1.tools "feishu_*,calendar_*"
openclaw config set agents.bot2.tools "database_*,web_*"

# 3. 重启 Bot
openclaw agents restart bot1
openclaw agents restart bot2
```

**配置示例**:

```json
{
  "agents": {
    "bot1": {
      "tool_prefix": "bot1_",
      "tools": ["feishu_*", "calendar_*"],
      "model": "qwen3.5-plus"
    },
    "bot2": {
      "tool_prefix": "bot2_",
      "tools": ["database_*", "web_*"],
      "model": "qwen3.5-plus"
    }
  }
}
```

**使用工具**: `subagents`, `sessions_spawn`

---

## 🛠️ 诊断工具

### 1. 插件健康检查

```bash
openclaw plugins doctor
```

**检查项目**:
- 插件加载状态
- 工具注册情况
- 配置完整性

### 2. 工具冲突检测

```bash
# 列出所有 feishu 相关工具
openclaw tools list --pattern "feishu_*"

# 查看工具来源
openclaw tools info feishu_chat
```

### 3. 配置验证

```bash
# 验证配置文件
openclaw config validate

# 查看配置差异
openclaw config diff
```

---

## 📋 插件对比

### 内置 feishu 插件

| 特性 | 说明 |
|------|------|
| **工具数量** | 50+ |
| **身份** | 机器人身份 |
| **文档权限** | 只读 |
| **消息历史** | ❌ 无法读取 |
| **流式输出** | ❌ 不支持 |

### 官方 feishu-openclaw-plugin

| 特性 | 说明 |
|------|------|
| **工具数量** | 50+ |
| **身份** | **用户身份** ✅ |
| **文档权限** | **读写** ✅ |
| **消息历史** | ✅ **完整读取** |
| **流式输出** | ✅ **打字机效果** |

**推荐**: 使用官方插件 `feishu-openclaw-plugin`

---

## 🔧 一键修复脚本

### 脚本 1: 禁用内置插件

```bash
#!/bin/bash
# fix-feishu-conflict.sh

echo "🔧 修复飞书插件冲突..."

# 1. 禁用内置插件
openclaw config set plugins.entries.feishu.enabled false

# 2. 启用官方插件
openclaw config set plugins.entries.feishu-openclaw-plugin.enabled true

# 3. 关闭 TTS
openclaw config set channels.feishu.tts.enabled false

# 4. 重启
openclaw gateway restart

echo "✅ 修复完成！"
```

### 脚本 2: 重置飞书配置

```bash
#!/bin/bash
# reset-feishu-config.sh

echo "🔄 重置飞书配置..."

# 备份
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# 删除飞书相关配置
jq 'del(.plugins.entries.feishu) | del(.channels.feishu)' \
  ~/.openclaw/openclaw.json > ~/.openclaw/openclaw.json.tmp

mv ~/.openclaw/openclaw.json.tmp ~/.openclaw/openclaw.json

# 重启
openclaw gateway restart

echo "✅ 重置完成！"
```

---

## 📝 配置模板

### 推荐配置 (仅官方插件)

```json
{
  "plugins": {
    "entries": {
      "feishu": { "enabled": false },
      "feishu-openclaw-plugin": {
        "enabled": true,
        "config": {
          "streaming": true,
          "footer": {
            "status": true,
            "elapsed": true
          },
          "tts": {
            "enabled": false
          }
        }
      }
    }
  }
}
```

### 多 Bot 配置

```json
{
  "agents": {
    "feishu-bot": {
      "tool_prefix": "feishu_",
      "tools": ["feishu_*"],
      "channels": ["feishu"]
    },
    "web-bot": {
      "tool_prefix": "web_",
      "tools": ["web_search", "web_fetch"],
      "channels": ["telegram"]
    }
  }
}
```

---

## 🆘 紧急恢复

### 完全重置飞书配置

```bash
# 1. 备份
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# 2. 删除配置
rm -rf ~/.openclaw/plugins/feishu*

# 3. 重新安装官方插件
npx -y @larksuite/openclaw-lark install

# 4. 初始化配置
openclaw config set plugins.entries.feishu-openclaw-plugin.enabled true

# 5. 重启
openclaw gateway restart
```

---

## 📚 相关资源

- [官方插件使用指南](https://my.feishu.cn/docx/MFK7dDFLFoVlOGxWCv5cTXKmnMh)
- [流式回复配置](https://www.feishu.cn/docx/Qv3fdMljgoUjYJx5cwAc3tinnfc)
- [OpenClaw 文档](https://docs.openclaw.ai)

---

## 📊 版本历史

### v1.0.0 (2026-04-09)
- ✅ 工具命名冲突解决方案
- ✅ TTS 语音配置指南
- ✅ 多 Bot 工具隔离方案
- ✅ 一键修复脚本

---

**最后更新**: 2026-04-09  
**作者**: 郑宇航
