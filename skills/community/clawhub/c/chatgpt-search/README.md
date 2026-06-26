# ChatGPT Search Skill - 全局配置指南

## 📦 安装

Skill 已创建在：
```
~/.openclaw/workspace/skills/chatgpt-search/
```

## 🔧 配置为全局 Skill

### 方法 1：自动加载（推荐）

OpenClaw 会自动加载 `~/.openclaw/workspace/skills/` 目录下的所有 Skill。

只需确保 Skill 目录结构正确：
```
~/.openclaw/workspace/skills/chatgpt-search/
├── SKILL.md
└── scripts/
    ├── chatgpt-search.js
    └── chatgpt-handler.js
```

### 方法 2：在 AGENTS.md 中引用

编辑 `~/.openclaw/workspace/AGENTS.md`，添加：

```markdown
## 可用 Skills

- **chatgpt-search**: 使用 ChatGPT 搜索问题
  - 用法：`使用 ChatGPT 搜索：[问题]`
  - 位置：`skills/chatgpt-search/`
```

### 方法 3：配置 Skill 加载

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "skills": {
    "entries": {
      "chatgpt-search": {
        "enabled": true,
        "config": {
          "timeout": 30000,
          "outputFormat": "text"
        }
      }
    }
  }
}
```

## 🚀 使用方法

### 在 OpenClaw 会话中

直接对 AI 说：

```
使用 ChatGPT 搜索：OpenClaw 最新版本是多少？
```

或

```
帮我用 ChatGPT 查询一下如何配置 VPS 防火墙
```

### 使用脚本

```bash
# 基础使用（搜索后自动关闭标签页）
node ~/.openclaw/workspace/skills/chatgpt-search/scripts/chatgpt-search.js "你的问题"

# 带上下文
node ~/.openclaw/workspace/skills/chatgpt-search/scripts/chatgpt-search.js "解释这个概念" --context "量子计算"

# JSON 输出
node ~/.openclaw/workspace/skills/chatgpt-search/scripts/chatgpt-search.js "问题" --output json

# 保持标签页打开（用于调试或查看完整对话）
node ~/.openclaw/workspace/skills/chatgpt-search/scripts/chatgpt-search.js "问题" --keep-open
```

## 📋 全局触发词

配置后，以下触发词会自动使用此 Skill：

- "使用 ChatGPT 搜索"
- "用 ChatGPT 查询"
- "问 ChatGPT"
- "ChatGPT 搜索"
- "chatgpt search"

## ⚙️ 自定义配置

### 修改超时时间

编辑 `scripts/chatgpt-handler.js`：

```javascript
const CONFIG = {
    timeout: 60000,  // 增加到 60 秒
    waitAfterSubmit: 15000  // 等待回答时间
};
```

### 修改截图保存路径

```javascript
const CONFIG = {
    screenshotDir: '/your/custom/path'
};
```

## 🔍 验证安装

1. **检查 Skill 文件**：
```bash
ls -la ~/.openclaw/workspace/skills/chatgpt-search/
```

2. **测试脚本**：
```bash
node ~/.openclaw/workspace/skills/chatgpt-search/scripts/chatgpt-search.js "测试"
```

3. **在 OpenClaw 中测试**：
```
使用 ChatGPT 搜索：1+1 等于几？
```

## 🛠️ 故障排查

### Skill 未加载

**检查：**
```bash
# 查看 Skill 目录
ls ~/.openclaw/workspace/skills/

# 查看 SKILL.md 格式
cat ~/.openclaw/workspace/skills/chatgpt-search/SKILL.md
```

### 浏览器不可用

**解决：**
```bash
# 重启浏览器
pkill chrome
/snap/bin/chromium --remote-debugging-port=18800 --user-data-dir=/tmp/openclaw-chrome &
```

### ChatGPT 要求登录

**说明：** 简单问题通常无需登录，复杂问题可能需要手动登录。

## 📝 更新日志

### v1.0.0 (2026-03-17)
- 初始版本
- 支持基础问答
- 浏览器自动化集成
- 全局 Skill 配置

---

## 📚 相关文档

- [OpenClaw Skills 文档](https://docs.openclaw.ai/skills)
- [Skill 创建指南](https://docs.openclaw.ai/skills/creating)
- [浏览器工具使用](https://docs.openclaw.ai/tools/browser)
