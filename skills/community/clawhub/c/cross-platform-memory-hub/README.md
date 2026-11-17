# 跨平台记忆枢纽 - 安装与配置指南

## 快速开始

1. 安装技能：

```text
使用ClawHub安装技能：cross-platform-memory-hub
```

2. 发送明确配置指令：

```text
记忆枢纽: 配置
```

3. 按提示确认读取范围、写入路径和适配平台。

## 隐私说明

- 本技能默认不读取 Obsidian 内容。
- 本技能默认不写入任何文件。
- 每次读取或写入前，都会展示范围或路径并等待用户确认。
- 远程服务仅处理订单和授权验证，不上传笔记、工作日记、项目文件或仓库内容。

## 明确命令

| 命令 | 功能 |
|------|------|
| `记忆枢纽: 配置` | 配置 Obsidian 路径与平台适配 |
| `记忆枢纽: 写入` | 写入用户明确指定的内容 |
| `记忆枢纽: 读取` | 在用户确认范围后宽泛读取短语 |
| `记忆枢纽: 复盘` | 基于用户确认的当天内容生成复盘 |
| `记忆枢纽: 状态` | 查看当前配置状态 |

不要使用宽泛短语触发写入。普通聊天中的“宽泛保存短语”“配置流程”不会自动执行。

## 各平台适配

### OpenClaw

安装技能后，在对话中使用明确命令。执行写入前确认目标路径和摘要。

### Claude Code

`adapters/claude-code/` 下脚本默认安全关闭。启用前必须设置：

```bash
MEMORY_HUB_USER_CONFIRMED=1
MEMORY_HUB_ENABLE_WRITE=1
```

读取类脚本还需要：

```bash
MEMORY_HUB_ENABLE_READ=1
```

脚本只读取 `MEMORY_HUB_*` 摘要字段，不读取原始会话全文。

### Codex

复制 `adapters/codex/project-rules.md` 到 Project Rules。规则要求每次读写前先询问用户。

## ClawHub 上传

上传目录：

```text
F:\技能包\new\cross-platform-memory-hub
```

不要上传：

```text
__pycache__
*.pyc
*.zip
```