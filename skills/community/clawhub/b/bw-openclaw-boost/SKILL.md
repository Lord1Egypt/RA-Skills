# bw-openclaw-boost - OpenClaw 效率提升工具包

## 概述

基于 Claude Code 架构分析开发的 OpenClaw 效率工具包，包含成本追踪、记忆管理、压缩系统、权限控制等功能。

## 版本

**v1.2.2** — 2026-04-03

## 文件结构

```
bw-openclaw-boost/
├── SKILL.md              # 本文件
├── version.json          # 版本信息
├── install.sh            # 安装脚本
├── launch.sh             # 统一启动器
├── config/               # 本地配置（不访问全局）
│   └── feature-flags.json
└── tools/
    ├── cost_tracker.py         # 成本追踪
    ├── memory_relevance.py     # 相关性记忆检索
    ├── compaction_manager.py   # 多层压缩
    ├── permission_manager.py   # 权限管理（本地规则）
    ├── tool_tracker.py         # 工具执行追踪
    ├── coordinator.py          # 任务协调（仅本地记录）
    ├── dream_consolidation.py  # 自动记忆整理
    ├── slash_commands.py       # 斜杠命令
    ├── token_budget.py         # Token 预算监控
    ├── feature_flags.py        # 功能开关
    └── check_permission.sh     # 权限检查
```

## 安装

```bash
bash install.sh
```

安装后位于 `~/.openclaw/bw-openclaw-boost/`

## 安全特性

- ✅ **配置文件在技能本地目录**，不访问全局 ~/.openclaw
- ✅ **不删除任何日志文件**，只整理不清理
- ✅ coordinator 仅做本地任务记录，**不发送消息**
- ✅ 所有 openclaw CLI 调用均为只读操作
- ✅ 无网络下载，无外部凭据要求

## 配置说明

- 配置存储在：`~/.openclaw/bw-openclaw-boost/config/`
- 记忆数据存储在：`~/.openclaw/bw-openclaw-boost/memory/`
- **不修改全局 ~/.openclaw/** 目录

## 使用方式

### 统一启动器
```bash
bash launch.sh cost        # 成本追踪
bash launch.sh memory      # 记忆检索
bash launch.sh budget      # Token 预算
bash launch.sh all-status  # 所有状态概览
```

### 单独工具
```bash
python3 tools/cost_tracker.py
python3 tools/memory_relevance.py scan
python3 tools/compaction_manager.py status
python3 tools/feature_flags.py list
```

## 依赖要求

- **Python 3**
- **Bash**
- **openclaw CLI**（部分工具需要，仅读取状态）

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 1.2.2 | 2026-04-03 | 配置文件移至技能本地；dream_consolidation 不删除日志 |
| 1.2.1 | 2026-04-03 | 修复launch.sh路径；coordinator仅本地记录 |
| 1.2.0 | 2026-04-03 | 打包完整工具脚本 |
| 1.0.7 | 2026-04-03 | 移除 stream_exec.py |

## License

MIT-0 - Free to use, modify, and redistribute. No attribution required.
