---
name: agent-manager
description: Multi-Agent conversation management platform with Gemini-style UI. Manage all your OpenClaw agents in one place with image upload, chat history, and message isolation.
version: 1.0.0
author: MSK
license: MIT
tags: agent,management,chat,ui,gemini,multi-agent,conversation
homepage: https://clawhub.com
category: productivity
---

# Agent Manager - 多 Agent 对话管理平台

统一管理多个 OpenClaw Agent 的对话平台，支持文字 + 图片输入，对话历史自动保存。

## 🎯 功能亮点

- **多 Agent 管理** - 统一管理所有 Agent
- **Gemini 风格界面** - 现代化左右分栏设计
- **图片输入** - 支持拖拽上传、按钮选择
- **对话历史** - 自动保存，切换 Agent 不丢失
- **消息隔离** - 每个 Agent 独立对话历史
- **本地存储** - 数据保存在浏览器

## 🔒 安全说明

**本技能访问的资源:**
- `~/.openclaw/agents` - Agent 配置目录
- `~/.openclaw/workspace-*` - Agent 工作区目录
- `~/.openclaw/devices/paired.json` - 读取 Operator Token

**安全承诺:**
- ✅ 无硬编码凭证（Token 由用户自行配置）
- ✅ 无外部 API 调用（所有数据本地处理）
- ✅ 无数据外传（对话历史存储在浏览器 localStorage）
- ✅ 代码完全开源可审查

**使用前请审查代码，确保信任作者。**

## 🚀 快速开始

### 1. 安装依赖

```bash
cd agent-manager
npm install
```

### 2. 配置 Token

```bash
# 复制示例配置
cp config.example.json config.json

# 获取你的 Operator Token
cat ~/.openclaw/devices/paired.json | jq '.[].tokens.operator.token'

# 编辑 config.json，填入 Token
nano config.json
```

### 3. 启动服务

```bash
node server-gemini.js
```

### 4. 访问界面

打开浏览器访问：
```
http://localhost:3000
```

## 📋 使用说明

### 与 Agent 对话

1. 左侧选择 Agent（如 Judy/MNK/Fly 等）
2. 右侧输入框输入消息
3. 按 Enter 或点击发送
4. 等待 Agent 回复

### 上传图片

1. 点击 📎 按钮选择图片
2. 或直接拖拽图片到输入框
3. 可添加文字说明
4. 点击发送

### 查看历史

1. 切换到其他 Agent
2. 再次切换回来
3. 完整对话记录自动加载

## 📁 文件结构

```
agent-manager/
├── server-gemini.js      # 主服务器
├── index.html            # 前端界面
├── package.json          # 依赖配置
├── config.json           # 配置文件（需自行填写 Token）
├── config.example.json   # 配置示例
├── cli.js                # 命令行工具
├── README.md             # 详细文档
└── SKILL.md              # 本文件
```

## ⚙️ 配置说明

### config.json

```json
{
  "openclawGateway": "http://127.0.0.1:18789",
  "openclawToken": "你的 Operator Token"
}
```

| 字段 | 说明 | 默认值 |
|------|------|--------|
| openclawGateway | OpenClaw Gateway 地址 | http://127.0.0.1:18789 |
| openclawToken | Operator Token（必填） | 需自行获取 |

### 获取 Operator Token

```bash
# 方法 1: 使用 jq
cat ~/.openclaw/devices/paired.json | jq '.[].tokens.operator.token'

# 方法 2: 手动查看
cat ~/.openclaw/devices/paired.json
```

## 🎨 界面特点

- **Gemini 风格** - 参考 Google Gemini 设计
- **左右分栏** - 左侧 Agent 列表，右侧对话区
- **响应式设计** - 自适应窗口大小
- **现代配色** - 紫色渐变主题
- **流畅动画** - 消息淡入效果

## 📊 支持的 Agent

| Agent | 职责 | 模型 |
|-------|------|------|
| Judy | 营销外展 | qwen3.5-plus |
| MNK | 技术架构 | glm-5 |
| Fly | 日程管理 | qwen3.5-plus |
| Dav | 数据分析 | qwen3.5-plus |
| Zhou | 用户运营 | qwen3.5-plus |
| PNews | 新闻播报 | qwen3.5-plus |

## ⚠️ 注意事项

1. **Gateway 必须运行** - 确保 `openclaw gateway status` 显示 running
2. **浏览器隔离** - 不同浏览器历史不互通
3. **隐私模式** - 隐私模式下关闭浏览器会丢失历史
4. **图片大小** - 建议 5MB 以内
5. **Token 安全** - 不要分享你的 config.json 文件

## 🆘 故障排查

**界面打不开？**
```bash
# 检查服务是否运行
ps aux | grep "node server"

# 查看端口占用
lsof -i :3000

# 重启服务
node server-gemini.js
```

**Agent 未加载？**
```bash
# 检查 OpenClaw Gateway
openclaw gateway status

# 刷新浏览器 Ctrl+Shift+R

# 检查 Token 是否正确
cat config.json
```

**无法与 Agent 对话？**
```bash
# 检查 Gateway 日志
tail -f ~/.openclaw/logs/gateway.log

# 检查 Agent 是否已配对
openclaw devices list
```

## 💰 付费说明

**价格:** $10 USD（一次性购买）

**支付:** PayPal (396554498@qq.com)

**包含:**
- ✅ 完整源代码
- ✅ 永久使用授权
- ✅ 基础技术支持
- ✅ 未来小版本更新

**购买流程:**
1. 通过 ClawHub 购买
2. 自动获得下载链接
3. 按照本指南安装使用

## 📄 许可

**使用权限:**
- ✅ 个人使用
- ✅ 商业使用
- ❌ 转售技能本身
- ❌ 公开分发源码

**免责声明:**
本技能按"原样"提供，不提供任何明示或暗示的保证。使用本技能的风险由用户自行承担。

---

**详细文档请查看 README.md 和 CLAWHUB.md**

**享受与 Agent 的高效对话！** 🚀
