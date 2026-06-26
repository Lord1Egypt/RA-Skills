# SKILL.md 同步方案

## 问题描述

项目中有两个 SKILL.md 文件：
1. **根目录 `SKILL.md`** (6.6K → 35K) - 用于 ClawHub 提交和 `hermes skills install` 从根目录安装
2. **`src/skills/SKILL.md`** (35K) - 权威版本，包含详细文档

**问题**：
- 两个文件内容不同步
- 相对路径 `references/` 在根目录无效（实际在 `src/skills/references/`）

## 解决方案

### 1. 同步脚本 (`scripts/sync_skill.sh`)

```bash
# 从 src/skills/ 同步到根目录 (调整路径)
./scripts/sync_skill.sh src2root

# 从根目录同步到 src/skills/ (调整路径)
./scripts/sync_skill.sh root2src

# 显示差异
./scripts/sync_skill.sh diff

# 检查一致性 (用于 CI)
./scripts/sync_skill.sh check
```

**路径调整逻辑**：
- `src2root`: `references/` → `src/skills/references/`
- `root2src`: `src/skills/references/` → `references/`

### 2. Git Pre-commit Hook (`.git/hooks/pre-commit`)

自动同步：
- 当 `src/skills/SKILL.md` 被修改时，自动同步到根目录
- 当根目录 `SKILL.md` 被修改时，自动同步到 `src/skills/`

### 3. GitHub Actions CI (`.github/workflows/check-skill-md.yml`)

检查一致性：
- 每次 push/PR 时检查两个文件是否一致
- 考虑路径调整后的内容一致性

## 工作流程

1. **开发时**：修改 `src/skills/SKILL.md`（权威版本）
2. **提交时**：Git hook 自动同步到根目录（调整路径）
3. **CI 检查**：确保文件一致
4. **发布时**：
   - ClawHub 使用根目录 `SKILL.md`（路径已调整）
   - Hermes Skill Hub 使用 `src/skills/SKILL.md`（原始路径）

## 路径说明

| 位置 | references 路径 | 说明 |
|------|----------------|------|
| `src/skills/SKILL.md` | `references/` | 原始路径，本地开发使用 |
| 根目录 `SKILL.md` | `src/skills/references/` | 调整后路径，GitHub/ClawHub 使用 |
| 本地安装 `~/.hermes/skills/...` | `references/` | Hermes 安装时复制整个目录 |

## 验证

```bash
# 检查一致性
./scripts/sync_skill.sh check

# 验证路径有效性
ls -la src/skills/references/skill-hub-publishing.md

# 测试同步
./scripts/sync_skill.sh src2root
```

## 注意事项

1. **不要手动编辑根目录 `SKILL.md`**
   - 应该修改 `src/skills/SKILL.md`
   - 提交时会自动同步

2. **路径调整是自动的**
   - 同步脚本会自动处理 `references/` 路径
   - 无需手动调整

3. **CI 会检查一致性**
   - 如果文件不一致，CI 会失败
   - 运行 `./scripts/sync_skill.sh src2root` 修复
