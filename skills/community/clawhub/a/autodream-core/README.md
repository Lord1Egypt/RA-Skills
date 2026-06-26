# autodream-core

**通用记忆整理引擎** — 让任何 Agent 都拥有记忆整理能力

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/yourusername/autodream-core)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-15%20passed-brightgreen)](tests/test_core.py)

---

## 📦 特性

- **平台无关** — 核心逻辑与具体平台解耦
- **适配器模式** — 轻松支持 OpenClaw、Claude Code 等平台
- **四阶段流程** — Orientation → Gather → Consolidate → Prune
- **性能优化** — Session 扫描节流、文件数量限制
- **可观测性** — Task 状态追踪、Analytics 埋点
- **单元测试** — 15 个核心测试用例，100% 通过

---

## 🚀 快速开始

### 1. 安装

```bash
# 克隆或复制到你的项目
cp -r autodream-core /your/project/
```

### 2. 基础用法（OpenClaw）

```python
from pathlib import Path
from autodream_core import AutoDreamEngine, OpenClawAdapter

# 初始化适配器
adapter = OpenClawAdapter(
    workspace=Path("~/.openclaw/workspace-research").expanduser()
)

# 创建引擎
engine = AutoDreamEngine(adapter)

# 运行整理
result = engine.run(force=True)  # force=True 强制运行

print(f"整理完成！处理了 {result['consolidation']['final_count']} 个条目")
```

### 3. 自定义平台适配器

```python
from autodream_core.adapters.base import BaseAdapter

class MyPlatformAdapter(BaseAdapter):
    def get_memory_files(self) -> List[Path]:
        # 实现你的平台逻辑
        pass
    
    def get_memory_md_lines(self) -> int:
        pass
    
    def update_memory_md(self, content: str, entries: List[Dict]) -> bool:
        pass
    
    def count_sessions_since(self, timestamp: float) -> int:
        pass
    
    def extract_session_signals(self) -> List[Dict]:
        pass

# 使用自定义适配器
adapter = MyPlatformAdapter(workspace=Path("/path/to/workspace"))
engine = AutoDreamEngine(adapter)
result = engine.run()
```

---

## 📋 配置

### 默认配置

```json
{
  "trigger": {
    "hours_since_last_run": 24,
    "min_sessions_since_last": 5,
    "memory_md_max_lines": 200
  },
  "limits": {
    "session_scan_interval_ms": 600000,
    "max_memory_files": 200,
    "frontmatter_max_lines": 30
  },
  "features": {
    "enable_contradiction_detection": true,
    "enable_stale_detection": true,
    "enable_relative_date_parsing": true,
    "enable_analytics": true
  }
}
```

### 自定义配置

```python
config = {
    "hours_since_last_run": 12,  # 12 小时触发
    "min_sessions_since_last": 3,  # 3 个会话触发
    "enable_analytics": False,  # 禁用 Analytics
}

engine = AutoDreamEngine(adapter, config=config)
```

---

## 🧪 测试

```bash
cd autodream-core
python3 tests/test_core.py -v
```

**测试覆盖**:
- ✅ frontmatter 解析
- ✅ 文本处理（normalize、canonical、stable_id）
- ✅ 矛盾检测
- ✅ 相对日期解析
- ✅ 状态管理
- ✅ Analytics 埋点

---

## 📁 项目结构

```
autodream-core/
├── core/
│   ├── __init__.py          # 核心导出
│   ├── engine.py            # 主引擎
│   ├── stages/
│   │   ├── orientation.py   # 阶段 1
│   │   ├── gather.py        # 阶段 2
│   │   ├── consolidate.py   # 阶段 3
│   │   └── prune.py         # 阶段 4
│   ├── utils/
│   │   ├── frontmatter.py   # YAML 解析
│   │   ├── text.py          # 文本处理
│   │   ├── dates.py         # 日期处理
│   │   └── state.py         # 状态管理
│   └── analytics.py         # Analytics 埋点
├── adapters/
│   ├── __init__.py
│   ├── base.py              # 基础接口
│   └── openclaw.py          # OpenClaw 适配器
├── config/
│   └── default.json         # 默认配置
├── tests/
│   └── test_core.py         # 核心测试
└── README.md                # 本文档
```

---

## 🔄 四阶段流程

### 1. Orientation（建立记忆地图）
- 扫描记忆目录
- 收集文件元数据
- 提取所有条目

### 2. Gather Signal（提取信号）
- 扫描会话记录
- 提取高价值信号
- 合并到条目列表

### 3. Consolidation（合并整理）
- 解析相对日期
- 去重（基于 stable_id）
- 删除过时条目
- 检测矛盾

### 4. Prune and Index（修剪索引）
- 更新 MEMORY.md
- 保持行数 ≤ 限制
- 添加/删除主题

---

## 📊 Analytics

自动记录使用行为到 `.autodream_analytics.jsonl`：

```jsonl
{"event": "autodream_started", "timestamp": "...", "trigger": "auto"}
{"event": "autodream_completed", "timestamp": "...", "duration_seconds": 123, "entries_processed": 50}
```

查看统计：

```python
stats = engine.get_analytics()
print(f"总运行次数：{stats['total_runs']}")
print(f"平均耗时：{stats['avg_duration_seconds']:.2f}s")
```

---

## 🛠️ 平台支持

| 平台 | 适配器 | 状态 |
|------|--------|------|
| OpenClaw | `OpenClawAdapter` | ✅ 已实现 |
| Claude Code | `ClaudeCodeAdapter` | ⏳ 待实现 |
| 自定义 | 继承 `BaseAdapter` | ✅ 支持 |

---

## 📝 版本历史

### v1.0.0 (2026-04-02)

**首次发布**:
- 核心引擎
- 四阶段流程
- OpenClaw 适配器
- 单元测试（15 个）
- Analytics 埋点
- Task 状态追踪

---

## 🎯 与 autodream 技能的关系

`autodream-core` 是从 `autodream` 技能抽离的通用核心库：

| 项目 | autodream 技能 | autodream-core |
|------|---------------|----------------|
| 定位 | OpenClaw 专用技能 | 通用核心库 |
| 平台 | OpenClaw | 多平台 |
| 部署 | 技能形式 | Python 库 |
| 配置 | config.json | 字典配置 |
| 适用 | OpenClaw 用户 | 所有 Python 项目 |

---

## 📄 License

MIT License

---

## 🙏 致谢

灵感来自 Claude Code AutoDream 功能。

---

*Made with ❤️ by 無生滅 (research agent)*
