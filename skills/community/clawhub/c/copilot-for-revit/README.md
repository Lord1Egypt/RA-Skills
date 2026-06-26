# Copilot for Revit Skill

OpenClaw skill，让用户能在飞书、Telegram 等聊天工具中用自然语言操作 Revit。

## 安装

### 方式一：从 ClawHub 安装（推荐）

```bash
openclaw skill install copilot-for-revit
```

### 方式二：从 GitHub 安装

```bash
git clone https://github.com/ryanchan720/copilot-for-revit-skill.git
cp -r copilot-for-revit-skill ~/.openclaw/workspace/skills/copilot-for-revit
```

## 前置条件

1. **Windows 端**已配置好 Copilot for Revit
2. **Linux 端**已安装 openclaw-bridge
3. 网络互通

详细配置请参考 [快速开始指南](https://github.com/ryanchan720/copilot-for-revit/blob/main/QUICKSTART.md)。

## 配置

在 `~/.bashrc` 或 `~/.zshrc` 中添加：

```bash
export REVIT_MCP_URL="http://<WINDOWS_IP>:18181"
export OPENCLAW_BRIDGE_DIR="$HOME/repos/openclaw-bridge"
```

## 使用示例

```
你: Revit 在线吗？
OpenClaw: 在线，版本 1.0.0，协议 2024-11-05

你: 帮我看看当前项目有哪些门
OpenClaw: 找到 15 种门类型...

你: 把所有门的高度改成 2100
OpenClaw: 已更新 23 扇门的高度参数
```

## 文件结构

```
copilot-for-revit/
├── SKILL.md              # Skill 定义
├── README.md             # 本文件
└── scripts/
    └── revit_call.py     # Bridge 调用脚本
```

## 许可证

MIT License