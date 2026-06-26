# 配置保护指南 - Article Workflow

## 🎯 问题背景

**痛点：** 每次重构或升级 Skill 时，`config.json` 配置文件会被覆盖，导致配置丢失。

**原因：**
1. `config.json` 在 `.gitignore` 中（正确，保护敏感信息）
2. 修改 Skill 时用 `write` 工具会覆盖现有文件
3. 没有配置备份和恢复机制

---

## ✅ 解决方案

### 配置保护脚本

| 脚本 | 用途 | 使用时机 |
|------|------|---------|
| `scripts/backup-config.sh` | 备份配置 | 修改 Skill 前 |
| `scripts/restore-config.sh` | 恢复配置 | 修改 Skill 后 |
| `scripts/config_manager.py` | 配置管理工具 | 检查/备份/恢复/向导 |
| `scripts/pre-git-operation.sh` | Git 操作前备份 | Git pull/checkout 前 |

---

## 📋 使用流程

### 场景 1：修改/重构 Skill

```bash
cd ~/.openclaw/workspace/skills/article-workflow

# Step 1: 备份配置（修改前必做）
python3 scripts/config_manager.py backup

# Step 2: 修改 Skill 文件
# ... 编辑文件 ...

# Step 3: 恢复配置
python3 scripts/config_manager.py restore

# Step 4: 验证配置
python3 scripts/config_manager.py check
```

### 场景 2：升级 Skill（Git pull）

```bash
cd ~/.openclaw/workspace/skills/article-workflow

# Step 1: Git 操作前自动备份
./scripts/pre-git-operation.sh

# Step 2: 执行 Git 操作
git pull

# Step 3: 恢复配置
./scripts/restore-config.sh

# Step 4: 合并配置（如有新配置项）
python3 scripts/config_manager.py merge
```

### 场景 3：首次使用

```bash
cd ~/.openclaw/workspace/skills/article-workflow

# 运行配置向导
python3 scripts/config_manager.py guide

# 按提示输入：
# 1. Bitable App Token
# 2. Table ID（可选）
```

---

## 🔧 配置管理工具

### 命令列表

```bash
# 检查配置状态
python3 scripts/config_manager.py check

# 备份配置
python3 scripts/config_manager.py backup

# 恢复配置
python3 scripts/config_manager.py restore

# 配置向导（首次使用）
python3 scripts/config_manager.py guide

# 合并配置（升级时保留用户配置）
python3 scripts/config_manager.py merge
```

### 配置合并规则

**升级时自动合并配置：**

| 配置项 | 处理方式 |
|--------|---------|
| `bitable.app_token` | ✅ 保留用户现有配置 |
| `bitable.table_id` | ✅ 保留用户现有配置 |
| `workflow.*` | 🔄 使用新配置（如有更新） |
| `paths.*` | 🔄 使用新配置 |
| 新增配置项 | ➕ 添加到配置 |

---

## 🛡️ 最佳实践

### 1. 修改前备份

**习惯：** 任何修改前先备份配置

```bash
# 添加到 alias（~/.zshrc）
alias aw-backup='cd ~/.openclaw/workspace/skills/article-workflow && python3 scripts/config_manager.py backup'
alias aw-restore='cd ~/.openclaw/workspace/skills/article-workflow && python3 scripts/config_manager.py restore'
```

### 2. 使用配置模板

**创建 `config.local.json` 保存个人配置：**

```json
{
  "bitable": {
    "app_token": "FOKgbCL2FarkSusBCRkcz4JZnad",
    "table_id": "tblyYMAnktSwNQ2i"
  }
}
```

升级时：
```bash
# 备份
cp config.json config.backup.json

# 复制新配置
cp config.example.json config.json

# 恢复个人配置
python3 -c "
import json
with open('config.local.json') as f: local = json.load(f)
with open('config.json') as f: config = json.load(f)
config['bitable'] = local['bitable']
with open('config.json', 'w') as f: json.dump(config, f, indent=2)
"
```

### 3. 环境变量（推荐用于 CI/CD）

```bash
# ~/.zshrc 或 ~/.bashrc
export BITABLE_APP_TOKEN=FOKgbCL2FarkSusBCRkcz4JZnad
export BITABLE_TABLE_ID=tblyYMAnktSwNQ2i
```

程序会自动读取环境变量。

---

## 📁 文件结构

```
article-workflow/
├── config.example.json          # 配置模板（提交到 Git）
├── config.json                  # 实际配置（.gitignore，不提交）
├── .config.backup.json          # 自动备份（.gitignore）
├── .env.example                 # 环境变量模板
├── .env                         # 环境变量（.gitignore）
└── scripts/
    ├── config_manager.py        # 配置管理工具
    ├── backup-config.sh         # 备份脚本
    ├── restore-config.sh        # 恢复脚本
    └── pre-git-operation.sh     # Git 操作前备份
```

---

## 🔍 故障排查

### 问题 1：配置丢失

**症状：** 修改 Skill 后配置不见了

**解决：**
```bash
# 检查是否有备份
ls -la .config.backup.json

# 恢复备份
python3 scripts/config_manager.py restore
```

### 问题 2：Git pull 后配置被覆盖

**预防：**
```bash
# Git pull 前
./scripts/pre-git-operation.sh

# Git pull 后
./scripts/restore-config.sh
```

### 问题 3：找不到配置文件

**检查：**
```bash
# 查看文件列表
ls -la config.json .config.backup.json

# 检查配置状态
python3 scripts/config_manager.py check
```

---

## 🎯 自动化建议

### 1. Git Hook（高级）

在 `.git/hooks/pre-pull` 添加：
```bash
#!/bin/bash
./scripts/pre-git-operation.sh
```

### 2. Makefile

```makefile
.PHONY: backup restore check

backup:
	python3 scripts/config_manager.py backup

restore:
	python3 scripts/config_manager.py restore

check:
	python3 scripts/config_manager.py check

upgrade: backup
	git pull
	restore
	python3 scripts/config_manager.py merge
```

### 3. 自动检测脚本

在 `install.sh` 中添加：
```bash
# 检查是否有现有配置
if [ -f "config.json" ]; then
    echo "✅ 检测到现有配置，备份中..."
    cp config.json .config.backup.json
fi
```

---

## 📝 配置示例

### 完整配置

```json
{
  "bitable": {
    "app_token": "FOKgbCL2FarkSusBCRkcz4JZnad",
    "table_id": "tblyYMAnktSwNQ2i"
  },
  "bitable_fields": {
    "url": "URL 链接",
    "title": "标题",
    "summary": "简短摘要",
    "read_date": "阅读日期",
    "source": "来源",
    "tags": "关键词标签",
    "importance": "重要程度",
    "doc_url": "详细报告链接",
    "status": "已完成",
    "creation_method": "手动触发"
  },
  "workflow": {
    "check_interval_hours": 6,
    "batch_limit": 10,
    "enable_quality_score": true,
    "enable_url_dedup": true,
    "timeout_minutes": 30
  },
  "paths": {
    "data": "./data",
    "logs": "./logs"
  },
  "quality_score": {
    "weights": {
      "content_value": 40,
      "technical_depth": 30,
      "relevance": 20,
      "readability": 10
    },
    "levels": {
      "S": {"min": 85, "max": 100},
      "A": {"min": 70, "max": 84},
      "B": {"min": 55, "max": 69},
      "C": {"min": 40, "max": 54},
      "D": {"min": 0, "max": 39}
    }
  }
}
```

---

## ✅ 检查清单

在修改/升级 Skill 前：

- [ ] 运行 `python3 scripts/config_manager.py check` 检查配置
- [ ] 运行 `python3 scripts/config_manager.py backup` 备份配置
- [ ] 确认备份文件存在（`.config.backup.json`）
- [ ] 执行修改/升级操作
- [ ] 运行 `python3 scripts/config_manager.py restore` 恢复配置
- [ ] 运行 `python3 scripts/config_manager.py check` 验证配置
- [ ] 测试功能是否正常

---

*最后更新：2026-03-15*
*作者：Nox（DongNan 的 AI 助理）*
