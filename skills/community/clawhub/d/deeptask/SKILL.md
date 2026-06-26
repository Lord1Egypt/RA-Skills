---
name: deeptask
description: AI 自动拆解需求与任务管理工具。实现 AI 自动拆解需求 → 人工审核 → AI 执行任务 → UT 验证 → **Git Commit** 的完整闭环。使用 SQLite 数据库管理项目、会话、子任务、MUF（最小功能单元）、单元测试。**核心特性：每完成一个 MUF 并通过 UT 后自动执行 git commit，commit 信息包含 SE_ID, ST_ID, MUF_ID, UT_ID**。
---

# DeepTask Skill

AI 自动拆解需求 → 人工审核 → AI 执行 → UT 验证 → Git Commit 的闭环流程管理工具。

## 核心目标

- **任务分解粒度可控**：项目 → 会话 → 子任务 → MUF（最小功能单元）
- **明确状态机**：每个环节有清晰的状态流转
- **人工审核精准介入**：仅在关键节点（会话级）触发审核
- **失败自动熔断**：7 次失败或 5 小时超时自动暂停
- **环境预检机制**：执行前先检查工具链/环境是否可用
- **Hello World 验证**：新语言先写测试代码验证语法
- **⭐ Git Commit 追踪**：每完成一个 MUF 并通过 UT 后自动执行 git commit

---

## ⭐ Git Commit 机制（核心特性）

### Commit 触发条件

```
MUF 完成 → UT 验证通过 → 执行 git commit
```

### Commit 信息格式

```bash
git commit -m "SE_ID:SE-1, ST_ID:ST-1, MUF_ID:MUF-1, UT_ID:UT-1"
```

### 完整流程

```python
# ai_worker.py 中的 execute_muf 函数

def execute_muf(muf_id, project_dir, tool_name, se_id, st_id, code_content):
    # 1. 更新 MUF 状态为 in_progress
    db.update_status("mufs", muf_id, "in_progress")
    
    # 2. 实现 MUF 代码（写入文件，包含追踪注释）
    # 代码文件头部：# SE_ID:SE-1, ST_ID:ST-1, MUF_ID:MUF-1, UT_ID:UT-1
    
    # 3. 运行 UT 验证
    ut_passed = run_unit_test(ut_id, project_dir, tool_name)
    
    if not ut_passed:
        # UT 失败，标记为 failed，不执行 commit
        db.update_status("mufs", muf_id, "failed")
        return False
    
    # 4. ⭐ UT 通过，执行 git commit
    git_commit(project_dir, se_id, st_id, muf_id, ut_id)
    # commit 信息："SE_ID:SE-1, ST_ID:ST-1, MUF_ID:MUF-1, UT_ID:UT-1"
    
    # 5. 验证 git 历史
    verify_git_history(project_dir, se_id, st_id, muf_id, ut_id)
    
    # 6. 更新 MUF 状态为 completed
    db.update_status("mufs", muf_id, "completed")
    
    return True
```

### 验证 Commit

```bash
# 查看项目 git 历史
git log --oneline

# 查找特定 MUF 的 commit
git log --grep "SE_ID:SE-1" --grep "MUF_ID:MUF-1"

# 示例输出：
# a1b2c3d SE_ID:SE-1, ST_ID:ST-1, MUF_ID:MUF-1, UT_ID:UT-1
```

---

## 快速开始

### 1. 初始化数据库

```bash
python ~/.openclaw/skills/deeptask/scripts/cli.py init
```

### 2. 创建项目

```bash
python ~/.openclaw/skills/deeptask/scripts/cli.py create_project \
  --name "用户管理系统" \
  --desc "支持注册/登录/权限管理" \
  --summary "核心功能：RBAC 权限模型"
```

### 3. 执行完整周期（含 Git Commit）

```bash
python ~/.openclaw/skills/deeptask/scripts/ai_worker.py \
  --project DT-1 \
  --tool python3 \
  --workspace ~/.openclaw/workspace \
  --cycle
```

输出示例：
```
=== 执行 MUF: MUF-1 ===
  SE: SE-1, ST: ST-1, UT: UT-1
  📝 实现 MUF 代码...
  ✅ 代码已写入：project_DT-1/muf_1.py
  🧪 运行 UT 验证...
  ✅ UT 验证通过
  📦 执行 git commit...
  ✅ Git commit 成功：SE_ID:SE-1, ST_ID:ST-1, MUF_ID:MUF-1, UT_ID:UT-1
  ✅ Git commit 已验证
  ✅ MUF 完成
```

### 4. 查看 Git 历史

```bash
cd ~/.openclaw/workspace/project_DT-1
git log --oneline
```

### 5. 人工审核

```bash
# 批准会话
python ~/.openclaw/skills/deeptask/scripts/cli.py review \
  --session SE-1 \
  --status approved \
  --reviewer "张三" \
  --comments "Git commit 验证通过，代码质量良好"
```

---

## 执行流程（增强版）

### 0. 环境预检

```python
# 检查工具链
env_ok, env_msg = check_environment("python3")
if not env_ok:
    trigger_fuse("环境不可用")
```

### 1. Hello World 验证

```python
# 验证语法
hw_ok, hw_msg = hello_world_test("python3")
if not hw_ok:
    trigger_fuse("语法验证失败")
```

### 2. 初始化 Git

```python
init_git(project_dir)
```

### 3. AI 拆解项目

项目 → 会话 → 子任务 → MUF

### 4. 执行 MUF（含 UT 验证和 Git Commit）⭐

```
MUF 实现 → UT 验证 → ✅ 通过 → Git Commit → 状态更新
                      ❌ 失败 → 标记 failed → 不 commit
```

### 5. 更新进度

检查子任务/会话完成情况，自动更新状态

### 6. 检查熔断

失败 MUF 自动记录审查请求

---

## 命令行工具

### 可用命令

| 命令 | 说明 |
|------|------|
| `init` | 初始化数据库 |
| `create_project` | 创建新项目 |
| `list_projects` | 列出所有项目 |
| `show_project` | 显示项目详情 |
| `review` | 人工审核 |
| `status` | 显示系统状态 |
| `check_env` | 检查环境 |
| `reset_project` | 重置项目状态 |
| `git_log` | 查看 Git Commit 历史 ⭐ NEW |

### Git Log 命令示例

```bash
# 查看项目 DT-1 的 git 历史
python cli.py git_log --project DT-1

# 查看特定 MUF 的 commit
python cli.py git_log --muf MUF-1

# 验证 commit 是否包含正确的追踪信息
python cli.py git_log --project DT-1 --verify
```

---

## 数据库结构

### 核心表

1. **projects** - 项目表
2. **sessions** - 会话表
3. **subtasks** - 子任务表
4. **mufs** - 最小功能单元表
5. **unit_tests** - 单元测试表
6. **review_records** - 人工审查记录表
7. **git_commits** - Git Commit 记录 ⭐ NEW

### Git Commits 表结构

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 自增 ID |
| se_id | TEXT | 会话 ID |
| st_id | TEXT | 子任务 ID |
| muf_id | TEXT | MUF ID |
| ut_id | TEXT | UT ID |
| commit_hash | TEXT | Git commit hash |
| commit_msg | TEXT | Commit 信息 |
| committed_at | DATETIME | Commit 时间 |

---

## 检查清单（每次任务必做）

### 执行前检查

- [ ] 工具链是否安装？ (`python3 --version`)
- [ ] Hello World 是否通过？
- [ ] Git 是否初始化？

### 执行后验证

- [ ] MUF 代码已写入？
- [ ] UT 验证通过？
- [ ] **Git commit 已执行？** ⭐
- [ ] **Commit 信息包含 SE_ID/ST_ID/MUF_ID/UT_ID？** ⭐
- [ ] Git 历史可查询？ ⭐

---

## 使用场景

### 场景 1: 完整项目周期

```bash
# 1. 创建项目
python cli.py create_project --name "电商系统" --desc "在线购物平台"

# 2. 执行完整周期（含 Git Commit）
python ai_worker.py --project DT-1 --tool python3 --cycle

# 3. 查看 Git 历史
cd workspace/project_DT-1 && git log --oneline
```

### 场景 2: 验证 Git Commit

```bash
# 1. 执行 MUF
python ai_worker.py --project DT-1 --tool python3 --cycle

# 2. 验证 commit
git log --grep "MUF_ID:MUF-1"

# 3. 输出应包含：
# abc123 SE_ID:SE-1, ST_ID:ST-1, MUF_ID:MUF-1, UT_ID:UT-1
```

### 场景 3: 审计追踪

```bash
# 查找特定会话的所有 commit
git log --grep "SE_ID:SE-1" --oneline

# 统计每个 MUF 的 commit
git log --grep "MUF_ID" --oneline | wc -l
```

---

## 注意事项

1. **Git Commit 仅在 UT 通过后执行** - UT 失败不 commit
2. **Commit 信息格式固定** - 必须包含 SE_ID, ST_ID, MUF_ID, UT_ID
3. **代码文件包含追踪注释** - 文件头部应有 `# SE_ID:xxx, ST_ID:xxx...`
4. **Git 仓库自动初始化** - 首次执行时自动 `git init`
5. **Commit 失败不阻断流程** - Git 失败记录警告，继续执行

---

## 故障排查

### Git Commit 未执行

```bash
# 1. 检查 UT 是否通过
python cli.py status  # 查看 UT 状态

# 2. 检查是否有代码更改
cd project_dir && git status

# 3. 手动执行 commit
git add -A && git commit -m "SE_ID:SE-1, ST_ID:ST-1, MUF_ID:MUF-1, UT_ID:UT-1"
```

### Commit 信息格式错误

```bash
# 正确格式
git commit -m "SE_ID:SE-1, ST_ID:ST-1, MUF_ID:MUF-1, UT_ID:UT-1"

# 错误格式（缺少字段）
git commit -m "完成 MUF-1"  # ❌
```

### Git 历史验证失败

```bash
# 验证 commit 是否存在
git log --grep "SE_ID:SE-1" --grep "MUF_ID:MUF-1"

# 如果找不到，检查 ai_worker.py 日志
```

---

## 版本历史

- v1.0.0 - 初始版本
- v1.1.0 - 增加环境预检机制
- v1.1.0 - 增加 Hello World 验证
- v1.2.0 - **增加 Git Commit 追踪机制** ⭐
- v1.2.0 - 增加 git_log 命令
- v1.2.0 - 增加 commit 验证功能
