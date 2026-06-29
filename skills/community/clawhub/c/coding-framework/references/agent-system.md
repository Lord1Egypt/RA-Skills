# 代理系统完整文档

> coding-framework 的标准化编程代理定义和调度系统。

## 概述

代理系统提供 7 个专业代理，每个代理有明确的职责、工具权限和输出格式。
灵感来源：Claude Code 代理定义 + Codex YAML 格式 + OpenAI Codex 安全沙箱。

## 代理定义规范

每个代理使用 YAML 文件定义，存放于 `agents/` 目录：

```yaml
name: agent-id              # 唯一标识符
display_name: "显示名称"     # 中文友好名称
description: "职责描述"      # 一句话说明
model: sonnet               # 推荐模型
color: green                # UI 显示颜色
tools:                      # 允许使用的工具
  - Read
  - Grep
trigger_examples:           # 触发示例
  - "示例消息"
system_prompt: |            # 系统提示
  详细的系统提示文本...
```

## 代理列表

### code-reviewer（代码审查员）

- **职责**：代码质量、可维护性、最佳实践 + Ponytail 决策阶梯
- **工具**：Read, Grep, Glob, exec
- **输出**：审查报告 + 评分（代码质量/可维护性/最佳实践/精简度）
- **特色**：集成 YAGNI 决策阶梯，识别过度抽象

### security-auditor（安全审计员）

- **职责**：安全漏洞、敏感信息、权限风险 + 25 种安全模式
- **工具**：Read, Grep, Glob, exec
- **输出**：安全报告 + CWE 编号 + 安全评分
- **特色**：覆盖 25 种安全模式，从注入到依赖漏洞

### test-engineer（测试工程师）

- **职责**：测试用例生成、覆盖率分析、测试策略
- **工具**：Read, Grep, Glob, exec
- **输出**：测试用例列表 + 测试代码 + 覆盖率建议
- **特色**：单元/集成/边界/异常全覆盖

### architecture-critic（架构批评家）

- **职责**：模块划分、依赖关系、设计模式、扩展性
- **工具**：Read, Grep, Glob
- **输出**：JSON 结构化发现 + 评分
- **特色**：SRP/开闭原则/循环依赖检测

### performance-analyst（性能分析师）

- **职责**：算法复杂度、资源泄漏、I/O 性能、并发
- **工具**：Read, Grep, Glob, exec
- **输出**：JSON 结构化发现 + 复杂度标注
- **特色**：N+1 检测、内存泄漏识别、可量化优化建议

### maintainability-reviewer（可维护性审查员）

- **职责**：命名质量、函数设计、复杂度、技术债务
- **工具**：Read, Grep, Glob
- **输出**：JSON 结构化发现 + 评分
- **特色**：TODO/FIXME 检测、圈复杂度分析

### documentation-checker（文档检查员）

- **职责**：API 文档、代码注释、README 完整性
- **工具**：Read, Grep, Glob
- **输出**：JSON 结构化发现 + 评分
- **特色**：文档一致性检查、示例代码建议

## 调度逻辑

```
用户请求 → 识别任务类型
  → 关键词匹配（trigger_examples）
  → 文件类型匹配（扩展名）
  → 任务类型匹配（审查/安全/测试）
  → 默认回退：code-reviewer
```

调度优先级：security-auditor > test-engineer > code-reviewer

## 与 sessions_spawn 集成

```
用户请求 → coding-framework 识别任务类型
  → 加载对应 agents/*.yaml
  → sessions_spawn(
      model: agent.model,
      system_prompt: agent.system_prompt,
      task: 用户请求 + 上下文
    )
  → 等待子代理返回
  → 格式化输出
```

## 输出格式规范

所有代理输出遵循统一格式：

```markdown
## [代理名称] 审查结果

### 概要
一句话总结发现。

### 详细发现
1. **[严重程度]** 问题描述
   - 位置：文件:行号
   - 建议：修复方案

### 评分
- 整体评分：X/10
- 置信度：X%
```

## 自定义代理

在 `agents/` 下创建新的 `.yaml` 文件，确保：
- `name` 唯一
- `system_prompt` 足够详细
- `trigger_examples` 覆盖常见场景
- `tools` 最小权限原则
