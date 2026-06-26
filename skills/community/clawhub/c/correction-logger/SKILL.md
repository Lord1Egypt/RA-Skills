---
name: correction-logger
version: 2.0.0
layer: processing
function_type: correction_extraction
health: healthy
adapter: correction_logger_adapter
dependencies: []
---
# correction-logger - 纠正记录插件

## 概述

`correction-logger` 是 Self-Improving + Proactive Agent (SIPA) 系统的第一个单功能拆分插件，负责记录用户纠正、代理错误、以及系统自我改进的关键事件。集成 NeverOnce 理念：修正优先级系统、有效性反馈、FTS5全文搜索。插件保持与现有 `~/self‑improving/corrections.md` 文件格式完全兼容，同时提供结构化 API 与适配器接口，便于星型架构其他组件调用。

## 功能特性
### NeverOnce 增强功能
- ✅ **修正优先级系统**：修正固定优先级10/10，永不衰减，始终优先召回
- ✅ **有效性反馈系统**：`.helped()` 反馈记录，动态有效性分数计算
- ✅ **FTS5全文搜索**：SQLite FTS5 全文搜索，BM25 相关性排序
- ✅ **行动前检查**：`check_corrections_for_action()` 预检相关修正
- ✅ **增强统计报告**：优先级分布、有效性分析、学习进度跟踪
- ✅ **向后兼容**：保持现有 `corrections.md` 文件格式完全兼容
            
### 兼容性说明
- **文件格式**：继续使用现有 Markdown 格式，新增 SQLite 数据库存储增强元数据
- **API 兼容**：原有 API 完全兼容，新增增强方法可选使用
- **数据迁移**：自动迁移现有修正到增强存储格式


### 核心功能
- ✅ **纠正记录**：将用户纠正、代理错误、改进建议以标准格式写入文件
- ✅ **记录查询**：获取最近 N 条纠正记录（支持过滤、排序）
- ✅ **统计报告**：生成纠正数量、时间分布、错误类型统计
- ✅ **健康检查**：验证文件可写性、格式有效性、服务可用性

### 兼容性保证
- 🔄 **文件格式不变**：继续使用现有 Markdown 列表格式，确保现有工具（如 `self‑improving` 技能）无需修改
- 🔄 **原子写入**：使用文件锁避免多进程/多线程写入冲突
- 🔄 **自动归档**：当 `corrections.md` 超过 1000 行时自动创建归档文件（`corrections_YYYY‑MM‑DD.md`）

### 适配器接口
- 🧩 **MemoryAdapter 兼容**：实现 `MemoryAdapter` 基类，提供 `log_correction`、`get_recent_corrections`、`get_stats`、`health_check` 方法
- 🧩 **星型架构注册**：自动注册到星型架构注册表，依赖关系为 `self‑improving`

## 安装与配置

### 安装方法
```bash
# 从 ClawHub 安装（发布后）
clawhub install correction-logger

# 或本地开发模式
cp -r correction-logger /root/.openclaw/workspace/skills/
```

### 配置文件
`config/default.yaml`：
```yaml
# 纠正记录配置
corrections_file: "~/self-improving/corrections.md"
max_lines_per_file: 1000
archive_directory: "~/self-improving/archive/"
enable_health_check: true
health_check_interval_seconds: 300

# 适配器配置
adapter:
  name: "correction_logger"
  version: "0.1.0"
  dependencies:
    - "self-improving"
```

## 使用方法

### Python API
```python
from correction_logger import CorrectionLogger

logger = CorrectionLogger()

# 记录纠正
correction_id = logger.log_correction(
    user_input="你刚才说的版本号错了",
    agent_response="当前版本是 v0.1.0",
    corrected_response="应该是 v0.5.0",
    context={"skill": "evolution-watcher", "timestamp": "2026-03-18T15:30:00Z"}
)

# 获取最近纠正
recent = logger.get_recent_corrections(limit=10)

# 获取统计
stats = logger.get_stats()
print(f"总纠正数: {stats['total_corrections']}")

# 健康检查
health = logger.health_check()
```

### 适配器调用
```python
from integration.adapter.correction_logger_adapter import CorrectionLoggerAdapter

adapter = CorrectionLoggerAdapter()
health = adapter.health_check()
print(health['healthy'])  # True/False
```

### 命令行工具
```bash
# 记录纠正（测试用）
python3 scripts/correction_logger.py log --input "你错了" --response "旧答案" --corrected "新答案"

# 查看最近纠正
python3 scripts/correction_logger.py recent --limit 5

# 运行健康检查
python3 scripts/correction_logger.py health
```

## 集成示例

### 与 evolution‑watcher 集成
当 evolution‑watcher 检测到插件升级失败时，自动记录纠正：
```python
def record_upgrade_failure(plugin_name, error_message):
    from correction_logger import CorrectionLogger
    logger = CorrectionLogger()
    logger.log_correction(
        user_input=f"升级 {plugin_name} 失败",
        agent_response="尝试自动升级插件",
        corrected_response="需要手动检查依赖冲突",
        context={"plugin": plugin_name, "error": error_message}
    )
```

### 与 self‑improving 技能集成
self‑improving 技能通过适配器调用纠正记录，无需直接操作文件：
```python
# 原代码（直接写入文件）
with open("~/self-improving/corrections.md", "a") as f:
    f.write(f"- **{timestamp}** 用户纠正: ...")

# 新代码（通过适配器）
adapter = CorrectionLoggerAdapter()
adapter.log_correction(...)
```

## 文件格式

### 纠正记录格式
每行格式：
```
- **YYYY‑MM‑DD HH:MM:SS** 用户纠正: {用户输入} | 代理回应: {代理回应} | 纠正后: {纠正后内容} [上下文: {JSON}]
```

示例：
```
- **2026‑03‑18 15:30:00** 用户纠正: 你刚才说的版本号错了 | 代理回应: 当前版本是 v0.1.0 | 纠正后: 应该是 v0.5.0 [上下文: {"skill": "evolution-watcher"}]
```

### 归档文件命名
当主文件超过 1000 行时，自动创建：
```
corrections_2026‑03‑18.md  # 包含前1000行
corrections.md             # 重置为空，继续写入新记录
```

## 适配器接口规范

### 必需方法
| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `log_correction` | `user_input`, `agent_response`, `corrected_response`, `context` | `str` (纠正ID) | 记录新纠正 |
| `get_recent_corrections` | `limit=50` | `List[dict]` | 获取最近纠正 |
| `get_stats` | 无 | `dict` | 统计信息 |
| `health_check` | 无 | `dict` | 健康检查结果 |

### 健康检查响应格式
```json
{
  "healthy": true,
  "status": "healthy",
  "message": "纠正记录服务正常",
  "stats": {
    "total_corrections": 42,
    "last_correction_time": "2026‑03‑18T15:30:00Z",
    "file_size_bytes": 12345,
    "file_writable": true
  },
  "plugin": "correction-logger",
  "version": "1.0.0",
  "timestamp": "2026‑03‑18T15:31:00Z"
}
```

## 故障排除

### 常见问题
1. **文件权限错误**：确保 `~/self‑improving/` 目录对当前用户可写
2. **格式损坏**：如果 `corrections.md` 格式损坏，插件会自动创建备份并新建文件
3. **适配器注册失败**：检查星型架构注册表中 `correction‑logger` 条目是否存在

### 日志位置
- 插件日志：`/tmp/correction‑logger.log`
- 适配器日志：通过 `adapter_cli.py health` 查看

## 错误码

| 错误码 | 描述 | 解决方案 |
|--------|------|----------|
| E001 | 未知错误 | 检查日志，联系开发者 |
| E002 | 配置错误 | 验证配置文件格式 |
| E003 | 依赖缺失 | 安装所需依赖包 |

## 版本历史

### v0.1.0 (2026‑03‑18)
- 初始版本
- 提供基本纠正记录、查询、统计功能
- 实现 MemoryAdapter 接口
- 保持与现有文件格式兼容

## 贡献与支持

- **问题反馈**：通过 ClawHub 提交 Issue
- **开发指南**：参见 `DEVELOPMENT.md`（待补充）
- **依赖关系**：仅依赖 Python 标准库，无外部包要求

---
*此插件为 SIPA 单功能拆分试点，旨在验证周边插件拆分模式，为后续 rule‑ranker、layer‑manager 等插件奠定基础。*