# Data Audit — 数据操作审计追踪器

## Overview

Data Audit 为数据目录提供 **SHA256 快照 → 快照对比 → 差异报告 → 操作追溯** 的完整审计链路。适用于合规审查、数据完整性验证、变更追溯、数据目录巡检等场景。

**Key Features:**
- 📸 **目录快照** — 递归扫描目录，计算每个文件的 SHA256 哈希和元数据
- 🔄 **快照对比** — 对比两个时间点的快照，识别新增/删除/修改的文件
- 📝 **操作日志** — 记录和查询数据操作历史
- 🔍 **健康检查** — 检测空文件、空目录、不可读文件等异常
- 🎯 **智能过滤** — 按扩展名、忽略模式、深度限制精确控制扫描范围
- 📊 **多格式导出** — JSON / CSV 报告导出，方便集成和分析

## Quick Start

```bash
# 生成目录快照
python3 scripts/auditor.py --snapshot ./data/ --output snapshot.json

# 对比两个快照，输出变更报告
python3 scripts/auditor.py --compare snapshot_old.json snapshot_new.json
python3 scripts/auditor.py --compare snapshot_old.json snapshot_new.json --output report.json

# 目录健康检查
python3 scripts/auditor.py --validate ./data/

# 操作记录与查询
python3 scripts/auditor.py --log "初始化数据库" --target ./data/db/
python3 scripts/auditor.py --history
```

## Advanced Usage

### 过滤扫描范围
```bash
# 只扫描 CSV 和 JSON 文件
python3 scripts/auditor.py --snapshot ./data/ --filter .csv,.json

# 忽略缓存目录和临时文件
python3 scripts/auditor.py --snapshot ./data/ --ignore __pycache__,*.tmp

# 从文件加载忽略模式
python3 scripts/auditor.py --snapshot ./data/ --ignore-file .auditignore

# 限制递归深度为 2 层
python3 scripts/auditor.py --snapshot ./data/ --depth 2
```

### 大目录进度显示
```bash
python3 scripts/auditor.py --snapshot ./large_data/ --progress
```

### CSV 导出
```bash
# 快照导出 CSV
python3 scripts/auditor.py --snapshot ./data/ --export-csv snapshot.csv

# 对比结果导出 CSV
python3 scripts/auditor.py --compare old.json new.json --export-csv changes.csv

# 健康检查导出 CSV
python3 scripts/auditor.py --validate ./data/ --export-csv issues.csv
```

### 配置文件模式
```bash
# 生成配置文件模板
python3 scripts/auditor.py --init-config .auditconfig.json

# 使用配置文件运行
python3 scripts/auditor.py --snapshot ./data/ --config .auditconfig.json
```

`.auditconfig.json` 示例：
```json
{
  "filter_extensions": [".csv", ".json", ".xlsx"],
  "ignore_patterns": ["__pycache__", "*.tmp", ".git"],
  "max_depth": 5,
  "show_progress": true,
  "skip_hidden": true,
  "skip_symlinks": true
}
```

### `.auditignore` 语法
```
# 忽略缓存目录
__pycache__/
node_modules/

# 忽略特定扩展名
*.tmp
*.log~

# 忽略隐藏文件
.*
```

## Use Cases

### 合规审查准备
```bash
# 1. 审查前生成基线快照
python3 scripts/auditor.py --snapshot ./production_data/ --output baseline.json

# 2. 审查时生成当前快照
python3 scripts/auditor.py --snapshot ./production_data/ --output current.json

# 3. 对比生成审计差异报告
python3 scripts/auditor.py --compare baseline.json current.json --output audit_diff.json

# 4. 导出变更清单供存档
python3 scripts/auditor.py --compare baseline.json current.json --export-csv audit_changes.csv
```

### 数据变更追溯
```bash
# 记录重要操作
python3 scripts/auditor.py --log "月度数据更新" --target ./data/monthly/
python3 scripts/auditor.py --log "数据迁移完成" --target ./data/archive/

# 查看操作历史
python3 scripts/auditor.py --history
```

### 数据目录周期性巡检
```bash
# 检查目录健康状态
python3 scripts/auditor.py --validate ./archive/

# 重点检查业务数据目录
python3 scripts/auditor.py --validate ./data/ --export-csv health_issues.csv
```

## Security

### Declared Capabilities

| Function | Purpose | Input | Output | Network | Filesystem |
|----------|---------|-------|--------|---------|------------|
| `--snapshot` | 目录快照 | Path | stdout/JSON/CSV | No | Read only |
| `--compare` | 快照对比 | JSON files | stdout/JSON/CSV | No | Read only |
| `--log` | 操作记录 | Action text | Log file | No | Write ~/.data-audit-logs |
| `--history` | 历史查询 | None | stdout | No | Read ~/.data-audit-logs |
| `--validate` | 健康检查 | Path | stdout/JSON/CSV | No | Read only |

### Explicitly Denied
- ❌ No network access (HTTP, socket, API calls)
- ❌ No arbitrary code execution via exec()/eval()
- ❌ No dynamic imports from external sources
- ❌ No system commands via subprocess/shell
- ❌ No telemetry, analytics, or usage reporting
- ❌ No modification of user files (logs only write to ~/.data-audit-logs)

### Data Privacy
- All processing is local — no data leaves the machine
- File content is hashed but never stored or transmitted
- No user data is collected
- Log history is stored locally in ~/.data-audit-logs/

## Requirements

- Python 3.7+
- No external dependencies (pure Python standard library)

## License

MIT © ChengQian (成乾)
