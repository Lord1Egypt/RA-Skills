# 破坏性重写备份规范与回滚机制（v3.4.2 审计整改）

> SKILL.md § 破坏性重写先备份规范的详细补充。执行 L0.4 RIA++ 挂载、缓存清理、clear-and-rewrite 时，AI 必须读取本文件并遵守全部铁律。
> v3.4.2 外迁自 SKILL.md，回应 ClawHub SkillSpector [SQP-2a/b/c] persistence_privilege concern。

## 1. 备份策略表（L0.4 挂载时）

⚠️ **L0.4 挂载时，对"已存在文件的修改"必须先备份再写入**：

| 操作类型 | 文件 | 备份策略（v3.4.2 强制） |
|---------|------|----------------------|
| **新建文件** | `references/methods/M{N+1}-*.md` | 无需备份（新文件） |
| **追加修改** | `assets/INDEX.md` | 写入前先复制到 `assets/.backup/INDEX.backup_<timestamp>.md` |
| **追加修改** | `references/routing/method-composition.md` | 同上，复制到 `references/routing/.backup/` 目录 |
| **追加修改** | `assets/test-prompts.json` | 同上，复制到 `assets/.backup/` 目录 |
| **追加修改** | `references/audit/candidates.md` | 同上，复制到 `references/audit/.backup/` 目录 |
| **可能修改** | `SKILL.md` | 同上，复制到 `.backup/` 目录 |
| **可能修改** | `README.md` / `CHANGELOG.md` | 同上，复制到 `.backup/` 目录 |

## 2. 破坏性重写铁律

1. 🚫 禁止直接覆盖已存在文件而不先备份
2. 🚫 禁止备份目录 `.backup/` 中保留超过 30 天的备份（自动清理）
3. 🚫 禁止备份目录 `.backup/` 被提交到 GitHub（必须在 `.gitignore` 中排除）
4. ✅ 必须在挂载报告中输出"已备份文件清单 + 备份目录位置"
5. ✅ 必须提供回滚命令：`python scripts/rollback_mount.py --to <timestamp>`

## 3. 回滚脚本使用方法

### 3.1 列出可回滚的时间点

```bash
python scripts/rollback_mount.py --list
```

输出示例：
```
=== 可用的回滚时间点 ===
  20260731_120000  (7 个备份文件)
  20260730_180000  (5 个备份文件)
```

### 3.2 预演回滚（不实际执行）

```bash
python scripts/rollback_mount.py --dry-run --to 20260731_120000
```

### 3.3 正式回滚

```bash
python scripts/rollback_mount.py --to 20260731_120000
```

### 3.4 自动确认模式（用于脚本化）

```bash
python scripts/rollback_mount.py --yes --to 20260731_120000
```

## 4. 回滚函数参考实现

如需在自定义脚本中调用回滚，可参考以下函数（实际执行请用 `scripts/rollback_mount.py`）：

```python
import shutil
from pathlib import Path
from datetime import datetime

def rollback_mount(timestamp: str, skill_dir: str = "."):
    """回滚到指定时间戳的挂载前状态（v3.4.2 强制）"""
    backup_dir = Path(skill_dir) / "assets" / ".backup"
    target_files = ["INDEX.md", "test-prompts.json"]
    routing_files = ["method-composition.md"]

    print(f"🔄 正在回滚到 {timestamp}...")

    # 恢复 assets 文件
    for fname in target_files:
        backup = backup_dir / f"{fname}.backup_{timestamp}"
        target = Path(skill_dir / "assets" / fname)
        if backup.exists():
            shutil.copy2(backup, target)
            print(f"  ✅ 已恢复 {fname}")

    # 恢复 routing 文件
    for fname in routing_files:
        backup = backup_dir / f"{fname}.backup_{timestamp}"
        target = Path(skill_dir / "references" / "routing" / fname)
        if backup.exists():
            shutil.copy2(backup, target)
            print(f"  ✅ 已恢复 {fname}")

    # 删除新增的 M{N+1} 方法论文件（需用户确认）
    new_methods = list_methods_created_after(timestamp)
    for m in new_methods:
        confirm = input(f"删除 {m}? (y/n): ")
        if confirm.lower() == 'y':
            Path(m).unlink()
            print(f"  ✅ 已删除 {m}")

    print(f"✅ 回滚完成")

def list_backup_timestamps(skill_dir: str = "."):
    """列出所有可用的回滚时间点"""
    backup_dir = Path(skill_dir) / "assets" / ".backup"
    if not backup_dir.exists():
        return []
    timestamps = set()
    for f in backup_dir.iterdir():
        if ".backup_" in f.name:
            ts = f.name.split(".backup_")[1]
            timestamps.add(ts)
    return sorted(timestamps, reverse=True)
```

## 5. 来源声明

- **v3.4.2**：从 SKILL.md 外迁到本文件，回应 SKILL.md 行数超 300 行硬门禁
- **同步**：M14 缓存保留与清理规范 + clear-and-rewrite 安全控制 仍在 `references/methods/M14-incremental-sync.md` 内（属于方法论本体）
- **回滚脚本**：实际实现在 `scripts/rollback_mount.py`，本文件仅作规范说明
