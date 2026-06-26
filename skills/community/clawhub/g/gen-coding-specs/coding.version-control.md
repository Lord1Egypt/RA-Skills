# 版本控制规范

## 概述
本文档定义Git工作流和版本管理标准，确保代码版本管理的规范性和可追溯性。

## Git工作流

### 分支策略
```
main (生产环境)
  └── develop (开发环境)
      └── feature/xxx (功能分支)
      └── bugfix/xxx (Bug修复分支)
      └── hotfix/xxx (热修复分支)
```

### 分支说明
- **main**: 生产环境代码，只接受来自release或hotfix的合并
- **develop**: 开发环境代码，功能开发的主分支
- **feature/xxx**: 功能开发分支，从develop创建，完成后合并回develop
- **bugfix/xxx**: Bug修复分支，从develop创建，完成后合并回develop
- **hotfix/xxx**: 紧急修复分支，从main创建，完成后合并回main和develop

## 提交信息规范

### 提交信息格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型（type）
- **feat**: 新功能
- **fix**: Bug修复
- **docs**: 文档更新
- **style**: 代码格式（不影响代码运行）
- **refactor**: 重构（既不是新功能也不是Bug修复）
- **perf**: 性能优化
- **test**: 测试相关
- **chore**: 构建过程或辅助工具的变动

### 示例
```bash
# 新功能
feat(user): 添加用户注册功能

# Bug修复
fix(order): 修复订单金额计算错误

# 文档更新
docs(api): 更新API文档

# 重构
refactor(auth): 重构认证逻辑

# 性能优化
perf(query): 优化用户查询性能
```

### 提交信息要求
- 使用中文或英文
- 第一行不超过50个字符
- 使用祈使语气（如：添加、修复、更新）
- 详细说明在body中

## 提交最佳实践

### 1. 原子性提交
- 每次提交只做一件事
- 提交应该可以独立工作
- 避免大而全的提交

### 2. 频繁提交
- 完成一个小功能就提交
- 修复一个Bug就提交
- 保持提交历史清晰

### 3. 提交前检查
```bash
# 检查变更
git status

# 查看差异
git diff

# 运行测试
npm test

# 运行代码检查
npm run lint
```

## 合并策略

### Merge Commit
```bash
# 保留分支历史
git checkout develop
git merge --no-ff feature/user-registration
```

### Rebase
```bash
# 保持线性历史
git checkout feature/user-registration
git rebase develop
git checkout develop
git merge feature/user-registration
```

### Squash Merge
```bash
# 压缩提交历史
git checkout develop
git merge --squash feature/user-registration
git commit -m "feat(user): 添加用户注册功能"
```

## 标签管理

### 版本标签
```bash
# 创建标签
git tag -a v1.0.0 -m "版本1.0.0"

# 推送标签
git push origin v1.0.0

# 查看标签
git tag -l
```

### 语义化版本
- **主版本号（MAJOR）**: 不兼容的API修改
- **次版本号（MINOR）**: 向下兼容的功能性新增
- **修订号（PATCH）**: 向下兼容的问题修正

示例：`v1.2.3`

## .gitignore

### 常见忽略文件
```gitignore
# 依赖
node_modules/
vendor/

# 构建产物
dist/
build/
*.class

# 环境配置
.env
.env.local

# IDE配置
.idea/
.vscode/
*.swp

# 日志
*.log
logs/

# 操作系统
.DS_Store
Thumbs.db
```

## Git Hooks

### Pre-commit Hook
```bash
#!/bin/sh
# .git/hooks/pre-commit

# 运行测试
npm test
if [ $? -ne 0 ]; then
  echo "测试失败，提交被阻止"
  exit 1
fi

# 运行代码检查
npm run lint
if [ $? -ne 0 ]; then
  echo "代码检查失败，提交被阻止"
  exit 1
fi
```

### Commit-msg Hook
```bash
#!/bin/sh
# .git/hooks/commit-msg

# 检查提交信息格式
commit_msg=$(cat "$1")
if ! echo "$commit_msg" | grep -qE "^(feat|fix|docs|style|refactor|perf|test|chore)(\(.+\))?: .{1,50}"; then
  echo "提交信息格式不正确"
  exit 1
fi
```

## 冲突解决

### 合并冲突
```bash
# 查看冲突文件
git status

# 手动解决冲突
# 编辑冲突文件，保留需要的代码

# 标记为已解决
git add <file>

# 完成合并
git commit
```

### 避免冲突
- 频繁拉取最新代码
- 小粒度提交
- 及时合并功能分支

## 版本回退

### 查看历史
```bash
# 查看提交历史
git log --oneline

# 查看文件变更
git log --follow <file>
```

### 回退操作
```bash
# 回退到指定提交（保留工作区）
git reset --soft <commit>

# 回退到指定提交（保留暂存区）
git reset --mixed <commit>

# 回退到指定提交（不保留）
git reset --hard <commit>
```

---

> **上下文提示**：在使用版本控制时，建议同时加载：
> - `coding.coding-style.md` - 编码风格规范
> - `coding.code-review.md` - 代码审查规范
> - `coding.documentation.md` - 文档规范

