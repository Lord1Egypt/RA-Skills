---
name: autodream-core
description: 通用记忆整理引擎 — 基于适配器模式的跨平台记忆整理技能。自动去重、合并、删除过时条目。| Universal Memory Consolidation Engine — Adapter-based cross-platform memory organization. Auto-dedup, merge, prune stale entries.
version: 1.0.0
author: 無生滅 (research agent)
license: MIT
tags: [memory, consolidation, automation, cross-platform]
---

# AutoDream-Core | 通用记忆整理引擎

**让任何 Agent 都拥有记忆整理能力 | Give Any Agent Memory Consolidation Power**

---

## 📖 概述 | Overview

**中文:**
autodream-core 是一个通用的记忆整理引擎，采用适配器模式设计，支持跨平台记忆管理。
它解决了 AI 代理长期运行中的记忆衰减问题：
- 记忆文件随时间积累变得混乱
- 相对日期（如"昨天"）失去意义
- 过时的调试方案引用已删除的文件
- 矛盾条目堆积

**English:**
autodream-core is a universal memory consolidation engine with adapter-based design for cross-platform memory management.
It solves the memory decay problem in long-running AI agents:
- Memory files become chaotic over time
- Relative dates (e.g., "yesterday") lose meaning
- Outdated debug solutions reference deleted files
- Contradictory entries accumulate

---

## 🎯 核心特性 | Core Features

| 特性 | 说明 |
|------|------|
| **平台无关** | 核心逻辑与具体平台解耦 |
| **适配器模式** | 轻松支持 OpenClaw、Claude Code 等平台 |
| **四阶段流程** | Orientation → Gather → Consolidate → Prune |
| **性能优化** | Session 扫描节流、文件数量限制 |
| **可观测性** | Task 状态追踪、Analytics 埋点 |
| **单元测试** | 15 个核心测试用例，100% 通过 |

| Feature | Description |
|---------|-------------|
| **Platform Agnostic** | Core logic decoupled from specific platforms |
| **Adapter Pattern** | Easy support for OpenClaw, Claude Code, etc. |
| **4-Stage Flow** | Orientation → Gather → Consolidate → Prune |
| **Performance** | Session scanning throttling, file limits |
| **Observability** | Task state tracking, Analytics logging |
| **Test Coverage** | 15 core test cases, 100% pass |

---

## 🚀 快速开始 | Quick Start

### 安装 | Installation

```bash
# 使用 skillhub (推荐)
skillhub install autodream-core

# 或使用 clawhub
clawhub install autodream-core
```

### 基础用法 | Basic Usage

```python
from pathlib import Path
from autodream_core import AutoDreamEngine, OpenClawAdapter

# 初始化适配器 | Initialize adapter
adapter = OpenClawAdapter(
    workspace=Path("~/.openclaw/workspace-research").expanduser()
)

# 创建引擎 | Create engine
engine = AutoDreamEngine(adapter)

# 运行整理 | Run consolidation
result = engine.run(force=True)  # force=True 强制运行

print(f"整理完成！处理了 {result['consolidation']['final_count']} 个条目")
```

---

## 📦 目录结构 | Directory Structure

```
autodream-core/
├── SKILL.md           # 技能描述 (Skill metadata)
├── README.md          # 详细文档 (Documentation)
├── package.json       # 包信息 (Package info)
├── install.sh         # 安装脚本 (Install script)
├── core/              # 核心逻辑 (Core logic)
│   ├── engine.py      # 主引擎 (Main engine)
│   ├── analytics.py   # 分析日志 (Analytics)
│   ├── stages/        # 四阶段实现 (4 stages)
│   └── utils/         # 工具函数 (Utilities)
├── adapters/          # 平台适配器 (Platform adapters)
│   ├── base.py        # 基础接口 (Base interface)
│   └── openclaw.py    # OpenClaw 实现 (OpenClaw impl)
├── tests/             # 单元测试 (Unit tests)
└── examples/          # 使用示例 (Examples)
```

---

## 🔧 配置选项 | Configuration

```python
from autodream_core import AutoDreamEngine, OpenClawAdapter

adapter = OpenClawAdapter(
    workspace=Path("/path/to/workspace"),
    memory_dir=Path("/path/to/workspace/memory"),  # 可选
)

engine = AutoDreamEngine(
    adapter,
    max_memory_lines=200,        # MEMORY.md 最大行数
    stale_days=30,               # 过期条目阈值（天）
    session_throttle=0.1,        # Session 扫描节流（秒/文件）
    enable_analytics=True,       # 启用分析日志
)
```

---

## 📊 输出示例 | Output Example

```json
{
  "orientation": {
    "memory_files": 5,
    "total_entries": 42
  },
  "gather": {
    "new_signals": 8,
    "session_scanned": 12
  },
  "consolidation": {
    "merged": 3,
    "removed_stale": 5,
    "final_count": 38
  },
  "prune": {
    "lines_before": 245,
    "lines_after": 178
  }
}
```

---

## 🧪 运行测试 | Run Tests

```bash
cd autodream-core
python -m pytest tests/ -v
```

---

## 🤝 贡献 | Contributing

欢迎提交 Issue 和 Pull Request！

**中文:**
- 报告 Bug 或提出新功能 → GitHub Issues
- 提交代码改进 → Pull Requests
- 添加新平台适配器 → 参考 `adapters/base.py`

**English:**
- Report bugs or request features → GitHub Issues
- Submit code improvements → Pull Requests
- Add new platform adapters → Refer to `adapters/base.py`

---

## 📄 许可证 | License

MIT License — See [LICENSE](LICENSE) file for details.

---

## 🔗 链接 | Links

- **GitHub:** https://github.com/yourusername/autodream-core
- **NPM:** https://www.npmjs.com/package/autodream-core (待发布)
- **OpenClaw Docs:** https://docs.openclaw.ai

---

## ⚠️ 注意事项 | Notes

1. **首次运行建议手动触发**，确认整理结果符合预期
2. **定期备份 MEMORY.md**，防止意外丢失重要信息
3. **生产环境建议先在小范围测试**

1. **Recommend manual trigger on first run** to verify results
2. **Backup MEMORY.md regularly** to prevent accidental data loss
3. **Test in staging environment first** before production use
