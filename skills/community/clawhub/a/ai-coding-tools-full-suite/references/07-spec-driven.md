# Spec规范驱动开发方法论参考

## 核心概念

### 1. 什么是Spec

```yaml
Spec定义:
  全称: Specification (规范)
  定位: 结构化的需求和设计文档
  目的: 为AI Agent提供清晰的开发蓝图

核心理念:
  1. 先想后做
     - 充分理解需求
     - 完善设计方案
     - 再开始编码

  2. 文档即指导
     - 规范文档驱动开发
     - 每个阶段有明确产物
     - 可追溯和验证

  3. 迭代式推进
     - 需求迭代
     - 设计迭代
     - 任务迭代
```

### 2. Spec与其他方法论对比

| 维度 | 传统瀑布 | Agile敏捷 | Spec驱动 |
|------|---------|----------|---------|
| 需求 | 一次性详设 | User Story | 结构化Spec |
| 设计 | 详细文档 | 架构原则 | 规范文档 |
| 开发 | 按计划执行 | 迭代交付 | 任务驱动 |
| 验证 | 最终测试 | 持续集成 | 逐步验证 |
| 变更 | 困难 | 相对灵活 | 规范更新 |

## 三阶段工作流

### 阶段概览

```mermaid
graph LR
    A[需求收集] --> B[设计创建]
    B --> C[任务分解]
    C --> D[执行实施]
    D --> A
```

```yaml
三个阶段:
  1. Requirements (需求)
     - 用户故事
     - 验收标准
     - EARS格式

  2. Design (设计)
     - 架构设计
     - 组件接口
     - 数据模型

  3. Tasks (任务)
     - 实现步骤
     - 任务清单
     - 编码任务
```

## 阶段一：需求收集

### 1. 用户故事格式

```yaml
用户故事结构:
  格式: As a [role], I want [feature], so that [benefit]

示例:
  As a 用户,
  I want 能够保存草稿,
  so that 不会因意外丢失内容

组成要素:
  - Role (角色): 谁需要这个功能
  - Feature (功能): 需要什么功能
  - Benefit (收益): 解决什么问题
```

### 2. EARS需求格式

```yaml
EARS简介:
  全称: Easy Approach to Requirements Syntax
  特点: 简洁、清晰、易于验证

基本模式:
  1. 通用事件响应
     WHEN [event] THEN [system] SHALL [response]

  2. 条件事件响应
     WHEN [event] AND [condition] THEN [system] SHALL [response]

  3. 状态驱动
     WHEN [state] THEN [system] SHALL [response]

  4. 可选特性
     IF [feature_enabled] THEN [system] SHALL [response]

  5. 初始状态
     AT STARTUP [system] SHALL [response]
```

### 3. 需求文档结构

```yaml
文档结构:
  1. Introduction (介绍)
     - 功能概述
     - 背景说明
     - 目标定义

  2. Requirements (需求)
     - Requirement 1
       * User Story
       * Acceptance Criteria
         - EARS格式标准
         - 可验证标准

  3. Constraints (约束)
     - 技术约束
     - 时间约束
     - 资源约束

  4. Assumptions (假设)
     - 已知条件
     - 依赖关系
```

## 阶段二：设计创建

### 1. 设计文档结构

```yaml
文档结构:
  1. Overview (概述)
     - 功能概述
     - 设计目标
     - 关键决策

  2. Architecture (架构)
     - 系统架构
     - 组件关系
     - 数据流图

  3. Components and Interfaces (组件和接口)
     - 组件清单
     - 接口定义
     - 交互协议

  4. Data Models (数据模型)
     - 数据结构
     - 数据库设计
     - 序列化格式

  5. Error Handling (错误处理)
     - 错误类型
     - 处理策略
     - 降级方案

  6. Testing Strategy (测试策略)
     - 测试用例
     - 验证方法
     - 覆盖率目标
```

### 2. Mermaid图表使用

```yaml
图表类型:
  1. 流程图
     graph TD/LR/BT
       用于: 流程设计

  2. 序列图
     sequenceDiagram
       用于: 接口交互

  3. 状态图
     stateDiagram
       用于: 状态管理

  4. 类图
     classDiagram
       用于: 数据结构

图表规范:
  1. 简洁清晰
  2. 不含样式定义
  3. 避免颜色定制
  4. 基础节点和关系
```

## 阶段三：任务分解

### 1. 任务分解原则

```yaml
分解原则:
  1. 原子性
     - 每个任务可独立执行
     - 单一职责
     - 可验证结果

  2. 递增性
     - 从基础开始
     - 逐步构建
     - 早期验证

  3. 可追溯性
     - 引用需求编号
     - 引用设计文档
     - 明确完成标准

  4. 可执行性
     - 具体的代码操作
     - 明确的文件位置
     - 可直接执行
```

### 2. 任务格式

```yaml
任务格式:
  - [ ] 1. 任务标题
     - 子任务描述
     - 实现细节
     - _Requirements: X.X_
     - _Design: X.X_

分级结构:
  顶级: 史诗 (Epic)
    二级: 功能 (Feature)
      三级: 任务 (Task)
        四级: 子任务 (Subtask)
```

## 用户交互机制

### 1. 确认节点

```yaml
确认节点:
  1. Requirements完成
     - 询问: "Do the requirements look good?"
     - 等待: "yes", "approved"等

  2. Design完成
     - 询问: "Does the design look good?"
     - 等待: 明确批准

  3. Tasks完成
     - 询问: "Do the tasks look good?"
     - 等待: 明确批准

  4. 任务执行完成
     - 用户主动触发下一任务
     - 或从tasks.md点击"Start task"
```

### 2. 回退机制

```yaml
回退触发:
  - 用户要求回退到需求阶段
  - 用户要求回退到设计阶段
  - 发现遗漏或错误

回退处理:
  1. 确认回退点
  2. 重新审视该阶段
  3. 补充或修改
  4. 重新确认
  5. 继续后续阶段
```

## 优势与适用场景

### 1. 核心优势

```yaml
优势:
  1. 需求清晰
     - EARS格式确保完整性
     - 显式验收标准
     - 可追溯验证

  2. 设计完善
     - 在编码前充分思考
     - 减少返工
     - 架构更合理

  3. 执行有序
     - 任务清单指导
     - 逐步执行验证
     - 风险可控

  4. 用户参与
     - 阶段确认机制
     - 及时反馈
     - 确保满意
```

### 2. 适用场景

```yaml
最适合:
  ✓ 复杂功能开发
  ✓ 需要详细设计的大型项目
  ✓ 团队协作开发
  ✓ 需要文档追溯的项目

不太适合:
  ✗ 简单快速的修改
  ✗ 探索性/实验性工作
  ✗ 时间极度紧张的情况
  ✗ 小型一次性任务
```

## 实践清单

### 设计检查清单

```yaml
需求阶段:
  ☐ 用户故事完整
  ☐ EARS格式正确
  ☐ 验收标准明确
  ☐ 约束条件清晰
  ☐ 用户已批准

设计阶段:
  ☐ 架构设计合理
  ☐ 组件划分清晰
  ☐ 接口定义完整
  ☐ 数据模型准确
  ☐ 用户已批准

任务阶段:
  ☐ 任务分解合理
  ☐ 每个任务可执行
  ☐ 需求引用完整
  ☐ 验收标准明确
  ☐ 用户已批准
```
