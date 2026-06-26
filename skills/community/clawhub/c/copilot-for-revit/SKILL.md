---
name: copilot-for-revit
description: |
  让 OpenClaw 能够操作 Revit。当用户提及 Revit 相关操作（图纸、标注、视图、元素等）时自动调用。
  
  支持的操作包括：
  - 检查 Revit 状态
  - 列出可用工具
  - 执行 Revit 命令（生成图纸、创建标注、查询元素等）

env:
  required:
    - name: REVIT_MCP_URL
      description: Revit MCP 服务地址（格式：http://<WINDOWS_IP>:18181）
      default: "http://localhost:18181"
    - name: OPENCLAW_BRIDGE_DIR
      description: openclaw-bridge 仓库路径
      default: "~/repos/openclaw-bridge"

config:
  - path: REVIT_MCP_URL
    description: Revit MCP 服务地址
    required: true
  - path: OPENCLAW_BRIDGE_DIR
    description: openclaw-bridge 仓库路径
    required: false

security:
  permissions: 
    - network-access  # 需要访问远程 Revit MCP 服务
  warnings:
    - "此 skill 可以执行修改 Revit 项目的命令（如删除元素、修改参数等），请在信任的环境中使用"
    - "默认无命令执行确认，建议在测试项目中验证后再用于生产环境"
---

# Copilot for Revit Skill

自动检测 Revit 相关意图，通过 `openclaw-bridge` 调用远程 Revit MCP 服务。

## ⚠️ 安全警告

**此 skill 可以执行修改 Revit 项目的命令**（如删除元素、修改参数、生成图纸等）。

- 请确保在**信任的网络环境**中使用
- 建议先在**测试项目**中验证
- 如需命令执行确认，可在 OpenClaw 配置中启用命令确认机制

## 前置条件

1. **Windows 端**已配置好 Copilot for Revit（参考 [快速开始指南](https://github.com/ryanchan720/copilot-for-revit/blob/main/QUICKSTART.md)）
2. **Linux 端**已安装 openclaw-bridge（`git clone https://github.com/ryanchan720/openclaw-bridge`）
3. 网络互通：Linux 能访问 Windows 的 18181 端口

## 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `REVIT_MCP_URL` | Revit MCP 服务地址 | `http://localhost:18181` |
| `OPENCLAW_BRIDGE_DIR` | openclaw-bridge 仓库路径 | `~/repos/openclaw-bridge` |

在 `~/.bashrc` 或 `~/.zshrc` 中配置：

```bash
export REVIT_MCP_URL="http://192.168.1.100:18181"
export OPENCLAW_BRIDGE_DIR="$HOME/repos/openclaw-bridge"
```

### 验证

```bash
# 测试连通性
curl $REVIT_MCP_URL/sse

# 或使用 bridge CLI
cd $OPENCLAW_BRIDGE_DIR
uv run python -m openclaw_bridge.cli health
```

## 使用方式

### 自动检测（推荐）

直接在聊天中提及 Revit 相关操作：

```
用户: Revit 在线吗？
OpenClaw: [自动调用 health 检查]

用户: 帮我看看 Revit 里有哪些可用命令
OpenClaw: [自动调用 tools list]

用户: 帮我在当前视图里创建梁标记
OpenClaw: [自动匹配 TagBeamCommand 并调用]
```

### 显式调用

明确指定要使用的工具：

```
用户: 用 GetEnvInfoCommand 查看一下环境信息
OpenClaw: [调用指定工具]
```

## 触发关键词

当用户消息包含以下关键词时自动激活：

- Revit
- 图纸 / 标注 / 视图 / 元素
- 墙 / 门 / 窗 / 梁 / 柱
- 标高 / 房间
- 以及从 `tools list` 动态获取的所有工具名称

## 错误处理

| 错误 | 提示 |
|------|------|
| Revit 不在线 | 提示用户启动 Revit 或检查网络 |
| Revit is not ready | 提示用户打开项目文件 |
| 工具不存在 | 列出可用工具供用户选择 |
| 参数缺失 | 向用户询问缺失的参数 |

## 注意事项

1. **Revit 必须打开项目**：大多数命令需要在打开 `.rvt` 文件后才能执行
2. **同步执行**：当前为同步调用，长耗时命令可能需要等待
3. **网络依赖**：需要 Linux 主机能访问 Windows 的 18181 端口

## 相关链接

- [Copilot for Revit](https://github.com/ryanchan720/copilot-for-revit) - 主框架
- [openclaw-bridge](https://github.com/ryanchan720/openclaw-bridge) - 桥接器
- [通用命令插件](https://github.com/ryanchan720/general-copilot-addins-for-revit) - 开箱即用的命令