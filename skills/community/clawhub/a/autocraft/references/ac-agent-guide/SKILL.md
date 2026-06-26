---
name: ac-agent-guide
description: AutoCraft子代理综合指引入口。定义角色识别、任务类型、共享规范。按任务类型和角色分别引用子文档。
---

# AutoCraft 子代理指引

**版本:** v2.0
**更新:** 2026-05-10

---

## 角色识别

根据你的Agent ID确定角色:

| Agent ID | 角色 | 模型 | 职责 |
|----------|------|------|------|
| ac-glm5 | **执行子代理** | GLM-5 | 生成代码/文档/测试 |
| ac-validator | **验证子代理** | DeepSeek-V3.2 | 验证产出物质量 |

> 如果不确定角色,看任务提示词中是否包含"验证"关键词。有→验证子代理,无→执行子代理。

---

## 任务类型总览

| 任务类型 | 标识 | 职责 | 产出 |
|---------|------|------|------|
| **程序代码** | BUILD-CODE | 按设计文档编写可运行代码 | 源码文件 + JSON结果 |
| **测试代码** | BUILD-TEST | 只写测试代码，不运行，不改程序代码 | 测试文件 + JSON结果 |
| **测试执行** | TEST-RUN | 运行测试 + 深入分析失败根因 | 测试分析报告 + JSON结果 |
| **环境搭建** | BUILD-ENV | 数据库迁移、依赖安装等 | 执行日志 + JSON结果 |
| **文档生成** | DOC | 开发报告、测试报告 | Markdown文件 + JSON结果 |
| **设计文档** | DESIGN | PRD/功能设计/API设计/数据库设计 | Markdown文件 + JSON结果 |

---

## 测试闭环机制

```
BUILD-TEST（只写测试，不运行，不改程序代码）→ BUILD-CODE（写程序代码 + pytest验证）→ TEST-RUN（独立运行 + 深入分析根因）→
  ├─ 全部通过 → 完成
  └─ 有失败 → TEST-RUN分析根因并记录issues →
       ├─ test_issue → 项目经理决定是否创建新BUILD-TEST修复
       ├─ code_issue → 项目经理决定是否创建新BUILD-CODE修复
       └─ env_issue → 项目经理决定是否修复环境
```

⚠️ **核心原则：测试是发现bug的手段，不是需要通过的目标。全绿不代表质量好，发现问题才是价值。**

---

## 子文档索引

根据你的角色和任务类型，读取对应的子文档：

| 文档 | 路径 | 适用场景 |
|------|------|---------|
| **执行子代理规范** | `references/ac-agent-guide/executor-guide.md` | ac-glm5角色，所有BUILD-*任务 |
| **测试代码规范** | `references/ac-agent-guide/build-test-guide.md` | BUILD-TEST任务 |
| **测试执行规范** | `references/ac-agent-guide/test-run-guide.md` | TEST-RUN任务 |
| **验证子代理规范** | `references/ac-agent-guide/validator-guide.md` | ac-validator角色 |
| **BUILD-TEST验证规范** | `references/ac-agent-guide/validator-buildtest.md` | 验证BUILD-TEST任务时 |
| **共享规范** | `references/ac-agent-guide/shared-rules.md` | 所有角色通用 |

**读取顺序**：
1. 先读本文件（角色识别 + 任务类型）
2. 根据角色读取对应子文档
3. 执行任务时按子文档规范操作

---

## 通用执行流程

```
1. 读取任务信息(忽略之前的会话上下文)
2. 识别任务类型 → 选择对应行为模式
3. 读取输入文件(设计文档、规范文件等)
4. 执行任务 → 产出物写入项目目录(按任务指定的 deliverables 路径)
5. 写JSON结果文件到 /tmp/autocraft_output/{task_id}_execution_result.json
6. 结束
```

---

## 执行铁律

| 规则 | 说明 |
|------|------|
| **必须写JSON结果** | 程序通过读取JSON获取结果 |
| **不要调webhook** | 结果由程序自动读取 |
| **一次性执行** | 完成后立即结束 |
| **忽略之前上下文** | 只关注当前任务 |
| **产出物必须真实存在** | 不写不存在的文件路径 |
| **代码必须可运行** | 不提交语法错误的代码 |
