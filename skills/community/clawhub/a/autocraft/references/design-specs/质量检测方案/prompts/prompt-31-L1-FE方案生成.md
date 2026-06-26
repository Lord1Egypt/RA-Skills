# L1-FE测试方案生成提示词模板

> 执行子代理读取此模板生成L1前端测试方案

**适用规范：** 31-L1-FE测试方案规范.md
**适用Checklist：** 33-L1-FE测试方案审核Checklist.md
**生成时机：** FE-DEV任务单执行（vitest闭环内部）

---

## 任务说明

本模板用于指导执行子代理在FE-DEV任务单vitest闭环内部动态生成测试代码。

**核心设计**：L1测试不生成独立方案文档，测试代码在vitest闭环内部动态生成。

---

## 输入文档清单

| 输入文档 | 提取内容 | 用途 |
|---------|---------|------|
| UI设计文档 | 组件清单、Props定义、事件定义 | 测试场景提取 |
| 组件规范文档 | Props约束、交互规范 | 边界场景提取 |
| API设计文档 | API响应格式 | 数据验证测试 |

---

## 测试代码生成要求

### 1. 测试文件命名

```
tests/frontend/{module}/{组件名}.test.ts
```

### 2. 测试代码结构（Vue + Vitest）

```typescript
import { describe, test, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import {ComponentName} from '@/components/{ComponentName}.vue'

describe('{组件名称}', () => {
  
  test('正向场景：{场景描述}', () => {
    // 准备测试数据（Props）
    // 执行组件挂载
    // 验证渲染结果
  })
  
  test('异常场景：{场景描述}', () => {
    // 准备边界Props数据
    // 执行组件挂载
    // 验证异常处理
  })
})
```

### 3. 场景覆盖规则

| 规则 | 说明 | 数量要求 |
|------|------|---------|
| 每个组件≥1正向场景 | 基础渲染测试 | 1+ |
| 每个Props边界≥1边界场景 | Props验证测试 | 1+ |
| 每个交互事件≥1场景 | 事件处理测试 | 1+ |
| 每个状态变化≥1场景 | 状态管理测试 | 1+ |

### 4. 场景命名规范

```
test_{组件名}_{场景类型}_{描述}

场景类型：
  render    渲染场景
  props     Props边界场景
  event     事件交互场景
  state     状态变化场景
```

---

## vitest执行要求

### 命令

```bash
vitest run tests/frontend/{module}/{组件名}.test.ts \
    --coverage \
    --coverage-reporter=json \
    --coverage-threshold.lines=70
```

### 验收标准

| 指标 | 阈值 | Guardian验证 |
|------|------|-------------|
| vitest通过率 | 100% | E4: vitest_passed=true |
| 代码覆盖率 | ≥70% | E5: coverage_percent≥70% |

---

## quality_check结构

```json
{
  "vitest_passed": true,
  "coverage_percent": 72,
  "eslint_errors": 0,
  "tsc_errors": 0,
  "complexity_score": 5
}
```

---

## Checklist对照（确保生成代码能通过审核）

| 检查项 | 检查内容 | 生成要求 |
|--------|---------|---------|
| E11 | vitest通过率100% | 所有测试函数必须通过 |
| E12 | 覆盖率≥70% | 覆盖所有组件逻辑 |
| E13 | ESLint无Error | 代码符合lint规范 |
| E14 | TypeScript无Error | 类型定义完整 |

---

## 执行流程

```
Step1: 读取UI设计文档 → 提取组件Props和事件
Step2: 根据规则生成测试代码
Step3: 执行vitest + 覆盖率采集
Step4: 失败 → 检查lint → 修复 → vitest → 循环最多3次
Step5: 产出quality_check → Guardian验证
```

---

**模板版本：** v1.0
**创建时间：** 2026-04-15
**作者：** 皮皮虾 🦐