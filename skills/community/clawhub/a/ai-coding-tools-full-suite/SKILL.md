---
name: ai-coding-tools-full-suite
description: 一站式AI编程工具分析技能包，支持Cursor、Claude Code、Devin、Windsurf等35+工具的深度分析、对比选型、Agent设计参考和提示词工程。封装了11个技能，覆盖 35+AI编程工具。当用户想要分析、学习、对比AI编程工具，或需要设计AI Agent系统、编写高效提示词时使用。触发指令：/ai-tools、/aitools、@ai-coding-tools-full-suite。
---

# AI编程工具全能套件

## 智能调度指令

使用以下任一方式激活本技能：

| 指令格式 | 示例 |
|---------|------|
| `/ai-tools` | `/ai-tools 对比Cursor和Claude Code` |
| `/aitools` | `/aitools 分析Devin的Agent循环` |
| `@ai-coding-tools-full-suite` | `@ai-coding-tools-full-suite 我想选择一个AI编程助手` |
| 直接描述 | "帮我分析Cursor的提示词设计" |

## 智能路由引擎

### 指令解析规则

当您使用上述指令时，系统会自动解析您的需求并路由到最合适的技能：

```
用户输入 → 意图识别 → 关键词提取 → 技能匹配 → 内容输出
```

### 路由映射表

| 需求类型 | 触发关键词 | 路由目标 | 输出内容 |
|---------|-----------|---------|---------|
| **工具对比** | 对比、哪个好、比较、选择、区别 | 对比分析 | 7+工具横向对比+选型决策树 |
| **Cursor深入** | Cursor、Agent模式、Chat模式 | Cursor分析 | 工具定义+双轨模式详解 |
| **Claude分析** | Claude Code、Anthropic、上下文 | Claude分析 | Agent循环+200K窗口奥秘 |
| **Devin分析** | Devin、自主执行、端到端 | Devin分析 | 浏览器自动化+部署能力 |
| **Windsurf分析** | Windsurf、Cascade、Wave 11 | Windsurf分析 | Cascade工作流+智能索引 |
| **Agent设计** | Agent设计、架构、工具定义 | 设计实践 | 最佳实践+组件设计 |
| **规范开发** | Spec、EARS、需求规范 | 规范开发 | 三阶段工作流+模板 |
| **工具参考** | 工具定义、Schema、API | 工具参考 | 30+工具完整定义 |
| **提示词工程** | 提示词、Prompt技巧、编写 | 提示词工程 | 四大模板+链式思维 |
| **综合学习** | 学习、入门、教程、概览 | 引导助手 | 个性化学习路径 |

## 快捷指令菜单

### /ai-tools help - 显示完整帮助

```
可用命令：
/ai-tools compare <工具A> [vs/and] <工具B>  - 对比两个工具
/ai-tools analyze <工具名>                    - 深度分析指定工具
/ai-tools design <系统类型>                   - 获取设计参考
/ai-tools prompt <场景>                       - 获取提示词模板
/ai-tools guide                               - 启动引导助手
/ai-tools all                                 - 完整内容索引
```

### /ai-tools compare - 工具对比

**用法**：
```
/ai-tools compare cursor vs claude
/ai-tools compare devin and windsurf
/ai-tools compare all
```

**输出**：
- 功能维度对比表
- 适用场景分析
- 成本效益评估
- 选择建议矩阵

### /ai-tools analyze - 深度分析

**用法**：
```
/ai-tools analyze cursor
/ai-tools analyze claude-code
/ai-tools analyze devin
/ai-tools analyze windsurf
/ai-tools analyze all
```

**输出**：
- 提示词架构图解
- 核心组件详解
- 工具定义完整版
- 设计亮点提炼
- 应用建议

### /ai-tools design - 设计参考

**用法**：
```
/ai-tools design agent        - Agent系统设计
/ai-tools design tools        - 工具定义设计
/ai-tools design workflow     - 工作流设计
/ai-tools design best-practices - 最佳实践汇总
```

**输出**：
- 架构设计蓝图
- 组件规范文档
- 实现示例代码
- 避坑指南

### /ai-tools prompt - 提示词工程

**用法**：
```
/ai-tools prompt templates    - 获取模板库
/ai-tools prompt optimize     - 优化现有提示词
/ai-tools prompt techniques   - 技巧大全
/ai-tools prompt compare      - 各工具风格对比
```

**输出**：
- 四大提示词模板
- 链式思维技巧
- 角色扮演方法
- 优化前后对比

### /ai-tools guide - 启动引导

**用法**：
```
/ai-tools guide
/ai-tools start
/ai-tools onboarding
```

**触发**：启动交互式引导流程，帮助您明确需求并规划学习路径。

## 自然语言交互模式

除了指令格式，您也可以直接用自然语言描述需求：

### 示例1：选型咨询
```
您：我想给团队选一个AI编程工具，我们主要做Web开发，预算有限

系统路由：对比分析技能
输出：
- 工具能力对比表
- Web开发专项评估
- 成本效益分析
- 组合使用建议
```

### 示例2：深度研究
```
您：帮我分析Cursor和Windsurf在代码重构方面的差异

系统路由：对比分析 + Cursor分析 + Windsurf分析
输出：
- 双工具深度对比
- 代码重构能力专项分析
- 最佳实践建议
```

### 示例3：设计参考
```
您：我要设计一个类似Devin的自主Agent，需要哪些核心组件？

系统路由：Devin分析 + Agent设计最佳实践
输出：
- 核心组件清单
- 架构设计参考
- 工具系统设计
- 错误处理策略
```

### 示例4：提示词优化
```
您：我写的Cursor提示词效果不好，怎么改进？

系统路由：Cursor分析 + 提示词工程
输出：
- 问题诊断
- 优化建议
- 参考模板
```

## 技能索引

### 子技能1：ai-coding-assistant-comparison

**能力**：
- 7+主流AI编程助手横向对比
- 35+维度结构化评估
- 选型决策树生成
- 工具组合策略

**包含工具**：Cursor、Claude Code、Windsurf、Devin、Kiro、Qoder、Manus、VSCode Agent、Replit、Lovable等

**适用场景**：
- 团队工具选型
- 产品对标分析
- 投资/采购评估

### 子技能2：cursor-prompt-analysis

**能力**：
- Agent模式深度解析
- Chat模式详解
- 双轨并行架构
- 工具调用规范

**特色内容**：
- 内存管理系统
- 错误处理策略
- Web开发专项
- 版本演进历史

### 子技能3：claude-code-prompt-analysis

**能力**：
- Agent循环机制
- 200K上下文窗口
- 任务管理系统
- 安全权限控制

**特色内容**：
- 架构理解层级
- 状态管理机制
- 多层验证体系
- 企业级设计

### 子技能4：devin-agent-loop-analysis

**能力**：
- 端到端自主执行
- 浏览器自动化
- Shell执行系统
- 部署能力

**特色内容**：
- Playwright集成
- 端口暴露机制
- Git操作规范
- 思维工具使用

### 子技能5：windsurf-prompt-analysis

**能力**：
- Cascade工作流
- Wave 11工具定义
- 代码库索引
- 上下文持久化

**特色内容**：
- 探索/实现/重构工作流
- 项目级上下文管理
- 智能任务分解
- 错误诊断能力

### 子技能6：ai-agent-design-best-practices

**能力**：
- 架构组件设计
- 工具定义规范
- Agent循环设计
- 安全性能优化

**特色内容**：
- 三大Agent模式
- 错误分类处理
- 权限控制体系
- 性能优化策略

### 子技能7：spec-driven-development

**能力**：
- 需求→设计→任务工作流
- EARS需求格式
- 三阶段确认机制
- 文档模板库

**特色内容**：
- 迭代式工作流
- 用户参与设计
- 可追溯验证
- 回退机制

### 子技能8：tool-definitions-reference

**能力**：
- 30+工具完整定义
- JSON Schema模板
- XML调用规范
- 并行执行规则

**特色内容**：
- Schema模板库
- 调用规范对比
- 能力矩阵
- 设计最佳实践

### 子技能9：prompt-engineering-for-coding

**能力**：
- 四大提示词模板
- 链式思维技巧
- 角色扮演方法
- 各工具风格对比

**特色内容**：
- 约束强化策略
- 迭代优化技巧
- 模板库
- 效果评估方法

## 快速查询索引

### 按需求类型

| 需求 | 推荐命令 |
|-----|---------|
| 刚入门，想了解全局 | `/ai-tools compare all` |
| 纠结选哪个工具 | `/ai-tools guide` |
| 想深入学习某个工具 | `/ai-tools analyze <工具名>` |
| 要基于某工具做设计 | `/ai-tools design agent` |
| 想优化自己的提示词 | `/ai-tools prompt optimize` |
| 需要工具定义参考 | `/ai-tools design tools` |

### 按角色

| 角色 | 推荐路径 |
|-----|---------|
| 开发新人 | 对比分析 → 单工具分析 → 提示词工程 |
| 团队Tech Lead | 对比分析 → 设计参考 → 规范开发 |
| 产品经理 | 对比分析 → 概览速查 |
| AI研究者 | 全技能深度学习 |
| 创业者/决策者 | 对比分析 → 成本评估 |

## 高级用法

### 1. 组合查询
```
/ai-tools compare cursor vs claude && analyze cursor && prompt templates
```
系统将依次输出：对比报告 + Cursor深度分析 + 提示词模板

### 2. 场景定制
```
/ai-tools compare all for "大型前端团队，React技术栈，预算中等"
```
系统将基于场景给出定制化评估

### 3. 竞品分析
```
/ai-tools analyze devin for "我要做一个类似Devin的产品"
```
系统将输出设计参考和实现建议

### 4. 学习路径
```
/ai-tools guide for "我想成为AI编程工具专家，学习时间每天1小时"
```
系统将规划个性化学习路径

## 技术规格

| 指标 | 数值 |
|-----|------|
| 覆盖工具 | 35+ |
| 分析维度 | 100+ |
| 子技能数量 | 11 |
| 文档规模 | 50,000+字 |
| 持续更新 | 是 |

## 总结

> **一句话总结**：输入您的需求，一句话说明您想做什么，我来帮您找到最合适的分析和指导！

**支持的交互方式**：
- 指令式：`/ai-tools <command>`
- 提及式：`@ai-coding-tools-full-suite <需求>`
- 描述式：直接描述您的需求

**适用场景**：
- AI编程工具选型
- 提示词设计优化
- Agent系统设计
- 竞品分析研究
- 学习路径规划
