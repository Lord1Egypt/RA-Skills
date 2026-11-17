# Git Worktree 使用指南

> 借鉴 Superpowers 的隔离开发设计，在模式 5（工作流编排）中实现主分支不受影响的隔离开发。

## 什么是 Git Worktree

Git worktree 允许你从同一个仓库创建多个工作目录，每个工作目录独立检出一个分支。这意味着你可以：

- 在主分支保持不变的情况下，在新分支上开发功能
- 同时处理多个功能，快速切换
- 避免 `git stash` 的混乱

## 目录结构

```
workspace/
├── .worktrees/              # 所有隔离工作区
│   ├── feature-x/           # feature-x 的独立工作区
│   │   ├── .worktree-metadata.json
│   │   ├── src/
│   │   └── ...
│   └── feature-y/
├── src/                     # 主工作区（master 分支）
└── ...
```

## 工作流

### 1. 开始新功能

```bash
# 创建隔离工作区（自动创建同名分支）
python scripts/worktree-manager.py create --name "feature-login"

# 输出：
# {
#   "status": "success",
#   "path": ".worktrees/feature-login",
#   "branch": "feature-login"
# }
```

### 2. 在隔离环境中开发

```bash
# 切换到 worktree 目录
cd .worktrees/feature-login

# 正常开发，所有修改都在 feature-login 分支
# 主工作区（master）不受影响
```

### 3. 查看状态

```bash
# 列出所有 worktree
python scripts/worktree-manager.py list

# 查看特定 worktree 的 git 状态
python scripts/worktree-manager.py status --name "feature-login"
```

### 4. 完成功能

```bash
# 回到主工作区
cd ../..

# 合并功能分支
git merge feature-login

# 清理已合并的 worktree
python scripts/worktree-manager.py cleanup --merged
```

### 5. 放弃功能

```bash
# 删除 worktree 和分支
git worktree remove .worktrees/feature-login
git branch -D feature-login
```

## 使用场景

### 场景 1：复杂功能开发

当你需要开发一个涉及多文件修改的功能时：

1. 创建 worktree：`worktree-manager.py create --name "feature-x"`
2. 在 worktree 中开发，主分支保持干净
3. 完成后合并或丢弃

### 场景 2：并行开发

当你需要同时处理多个任务时：

```bash
# 创建多个 worktree
worktree-manager.py create --name "feature-a"
worktree-manager.py create --name "feature-b"

# 在不同 worktree 中并行开发
# 快速切换：worktree-manager.py switch --name "feature-a"
```

### 场景 3：实验性修改

当你想尝试一种实现方式，但不确定是否可行时：

1. 创建 worktree
2. 在 worktree 中实验
3. 如果不行，直接丢弃（不影响主分支）

## 注意事项

1. **磁盘空间**：每个 worktree 都是完整的工作目录，会占用额外磁盘空间
2. **依赖安装**：每个 worktree 需要独立安装依赖（如 `npm install`）
3. **定期清理**：使用 `cleanup --merged` 清理已合并的 worktree
4. **分支命名**：worktree 名称就是分支名称，建议使用 `feature-xxx` 格式

## 与 coding-framework 集成

在模式 5（工作流编排）中，worktree 创建是自动的：

```
用户: "实现用户登录功能"
  ↓
daily-agent 分类: 编码任务
  ↓
coding-framework 模式 5:
  1. 任务分类 → backend
  2. 规划阶段 → 生成实现计划
  3. 用户确认
  4. 🌳 创建 worktree → worktree-manager.py create --name "feature-login"
  5. 在 worktree 中执行
  6. 审查 → 多代理审查
  7. 优化
  8. 交付确认 → 合并/保留/丢弃
```

## 故障排除

### 问题：worktree 创建失败

```
错误: 'feature-x' already exists
```

**解决**：worktree 已存在，使用 `switch` 切换或先 `cleanup`

### 问题：合并冲突

```bash
# 在 worktree 中解决冲突
cd .worktrees/feature-x
git merge master  # 或 rebase
# 解决冲突后
git add .
git commit
```

### 问题：磁盘空间不足

```bash
# 清理所有已合并的 worktree
worktree-manager.py cleanup --merged

# 或手动删除特定 worktree
git worktree remove .worktrees/old-feature
```
