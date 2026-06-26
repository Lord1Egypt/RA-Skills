# 🚀 飞书机器人创建器

快速创建飞书机器人并连接到 OpenClaw，绑定到独立 Agent。

## 当前适配环境

- 系统：Windows
- OpenClaw：2026.4.26
- 当前工作区：`C:\Users\26462\.openclaw\workspace`
- 主人偏好称呼：主人
- 当前主代理身份：皇帝

这个版本已经整理成更适合主人当前机器的 Windows + OpenClaw 用法，不再沿用旧的 macOS/Linux 风格说明。

## 适合做什么

- 创建新的飞书机器人
- 让机器人绑定到独立 Agent
- 为不同业务角色拆分多个飞书入口

## 快速开始

### 1. 创建飞书应用
访问 <https://open.feishu.cn/page/openclaw?form=multiAgent> 创建应用，获取 App ID 和 App Secret。

### 2. 检查事件与权限
在飞书开放平台中确认：
- 已开启事件订阅
- 已配置消息接收相关事件
- 应用处于可用状态

### 3. 创建 Agent 工作区
推荐路径：

```powershell
$agentId = "<agent-id>"
$base = "C:\Users\26462\.openclaw\agents\$agentId"
New-Item -ItemType Directory -Force -Path "$base\agent" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\.learnings" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\memory" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\skills" | Out-Null
```

### 4. 配置 OpenClaw
按当前本机 OpenClaw 文档与配置格式，补充：
- Agent 信息
- Feishu 账号信息
- Agent / 渠道路由绑定

### 5. 重启 Gateway
```powershell
openclaw gateway restart
```

### 6. 验证
在飞书里给机器人发送 `你好`，确认是否有回复。

详见 [SKILL.md](./SKILL.md)
