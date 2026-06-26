---
name: ai-coding-standards
description: AI编码规范与自我修正系统 - 基于Claude Code最佳实践的质量红线、渐进式上下文加载、Plan持久化、Hook拦截机制
---

# AI Coding Standards Skill

基于 Claude Code 最佳实践的 AI 编码规范系统，帮助 AI  agent 保持代码质量和上下文整洁。

## 核心理念

**上下文的熵增才是瓶颈** - 不治这个，迭代越快崩越快

## 四大规则

### 1. 📏 质量红线 (Quality Red Lines)

硬性阈值：
- 单个文件 ≤ 800 行
- 单个函数 ≤ 30 行
- 嵌套 ≤ 3 层
- 分支 ≤ 3 个

**为什么：** AI 对"要短"理解飘忽，但对"≤30行"执行稳定

### 2. 📦 渐进式上下文 (Progressive Context Loading)

- **查 bug：** 只加载目标模块
- **架构决策：** 才加载全局上下文
- **命中率 > 覆盖率** — 精准加载比塞满上下文更重要

1M 上下文缓解熵增但不根除，渐进加载是必修课。

### 3. 💾 Plan 文件持久化

- 复杂任务落到文件（memory/tasks/）
- 加 checklist 跟踪进度
- 新会话读文件断点恢复
- **文件系统是唯一可靠状态源**

### 4. 🚧 Hook 自动拦截

- 规范写成脚本，违规操作瞬间打回
- 比 prompt 强调一百遍更有效

## 使用方法

### 在项目根目录创建 hooks

```bash
# 创建质量检查 hook
mkdir -p .git/hooks
cp pre-commit.sample .git/hooks/pre-commit
```

### 创建 CLAUDE.md

在项目根目录创建 CLAUDE.md，强制加载规范：

```markdown
# 项目编码规范

## 质量红线
- 函数 ≤ 30 行
- 文件 ≤ 800 行

## 加载策略
- Bug 修复只加载相关文件
- 重构才加载全貌
```

### 使用示例

```python
from ai_coding_standards import QualityChecker

checker = QualityChecker()
result = checker.check_file("src/main.py")
if not result.passed:
    print(f"违规: {result.issues}")
```

## 触发信号

- code_quality
- function_length
- file_size
- context_overflow
- plan_persistence

## 包含工具

- `QualityChecker` - 代码质量检查
- `ContextManager` - 上下文管理
- `PlanTracker` - Plan 持久化跟踪
- `HookRunner` - Hook 拦截执行
