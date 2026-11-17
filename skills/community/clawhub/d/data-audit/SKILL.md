---
name: data-audit
description: |
  数据操作审计追踪器 (Data Audit)。
  对数据目录生成 SHA256 快照、比对文件变化（新增/删除/修改）、
  记录操作日志、检查数据目录健康状态。
  适用于数据合规场景中的操作追溯和审计准备。

  Use when: 需要追踪数据文件变化、生成审计快照、
  合规审查准备、文件完整性验证、数据目录健康检查。

  🎉 v1.1.0 核心功能：
  - 📸 数据目录 SHA256 快照
  - 🔄 快照对比（新增/删除/修改检测）
  - 📝 操作日志记录与查询
  - 🔍 数据目录健康检查
  - 📊 JSON 报告导出

  触发关键词：数据审计、文件追踪、快照比对、SHA256、
  完整性校验、合规审计、数据治理、变更追踪

  适用范围：任意数据文件目录
  运行模式：纯本地，无网络请求 ❎
  外部依赖：Python标准库（无需额外安装）
---

# 📋 Data Audit

## Overview

Data Audit 为数据目录提供 **SHA256 快照 → 快照对比 → 差异报告** 的完整审计链路。适用于合规审查、数据完整性验证、变更追溯等场景。

### 核心流程
```
[数据目录] → 生成快照(snapshot.json) → 后续快照 → 对比 → 审计报告
                                      ↗ 操作日志 → 历史查询
                                      ↘ 健康检查 → 问题报告
```

---

## Usage

### 1. 生成快照
对数据目录递归扫描，计算每个文件的 SHA256 哈希和元数据。
```bash
python3 scripts/auditor.py --snapshot ./data/ --output snapshot.json
```

输出：
```
📸 数据快照
   目录: /Users/me/project/data
   文件数: 1,245
   总大小: 156.3 MB
   时间: 2026-07-19T10:30:00
```

### 2. 快照对比
对比两个时间点的快照，识别新增、删除、修改的文件。
```bash
python3 scripts/auditor.py --compare snapshot_before.json snapshot_after.json
python3 scripts/auditor.py --compare old.json new.json --output audit_report.json
```

输出：
```
📊 审计对比结果
   =============================================
   新增: 5   删除: 2   修改: 12   总计: 19
   时间窗口: 2026-07-18 → 2026-07-19
   
   变更明细:
   🟢 added     data/sales_2026.csv (12.2 KB)
   🔴 deleted   temp/backup.csv (45.0 KB)
   🟡 modified  config/settings.json (2.0 KB → 2.1 KB)
```

### 3. 操作日志
记录和查询数据操作历史。
```bash
# 记录操作
python3 scripts/auditor.py --log "导入销售数据" --target ./data/sales/

# 查看历史
python3 scripts/auditor.py --history
```

### 4. 健康检查
检查数据目录的完整性：空文件、空目录、不可读文件等。
```bash
python3 scripts/auditor.py --validate ./data/
```

输出：
```
🔍 数据健康检查 — ✅ healthy
   目录: /Users/me/project/data
   文件数: 1,245
   总大小: 156.3 MB
   目录数: 38
   空目录: 2
```

---

## JSON Output Format

**Snapshot:**
```json
{
  "snapshot_time": "2026-07-19T10:30:00",
  "directory": "/data/",
  "total_files": 1245,
  "total_size": 156300000,
  "files": [
    {"path": "data.csv", "size": 12450, "hash": "sha256...", "modified": "2026-07-19T10:00:00"}
  ]
}
```

**Compare Report:**
```json
{
  "compare_time": "2026-07-19T10:35:00",
  "total_changes": 19,
  "by_type": {"added": 5, "deleted": 2, "modified": 12},
  "changes": [
    {"type": "added", "file": "data/sales_2026.csv", "size": 12450}
  ]
}
```

---

## Use Cases

### 合规审查准备
```bash
# 1. 审查前生成基线快照
python3 scripts/auditor.py --snapshot ./production_data/ --output baseline.json

# 2. 审查时生成当前快照
python3 scripts/auditor.py --snapshot ./production_data/ --output current.json

# 3. 对比生成审计差异报告
python3 scripts/auditor.py --compare baseline.json current.json --output audit_diff.json
```

### 数据变更追溯
```bash
# 查看操作历史
python3 scripts/auditor.py --history

# 结合业务记录，定位变更时间点
python3 scripts/auditor.py --log "月度数据更新完成" --target ./data/monthly/
```

### 数据目录周期性巡检
```bash
python3 scripts/auditor.py --validate ./archive/
# → 发现空目录和0字节文件，提示清理
```

---

## Security

### Declared Capabilities

| Function | Purpose | Input | Output | Network | Filesystem |
|----------|---------|-------|--------|---------|------------|
| `--snapshot` | 目录快照 | Path | stdout/JSON | No | Read only |
| `--compare` | 快照对比 | JSON files | stdout/JSON | No | Read only |
| `--log` | 操作记录 | Action text | Log file | No | Write ~/.data-audit-logs |
| `--history` | 历史查询 | None | stdout | No | Read ~/.data-audit-logs |
| `--validate` | 健康检查 | Path | stdout/JSON | No | Read only |

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
