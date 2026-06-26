# /tdd - 测试驱动开发指令

## 功能
调度 QA + Backend/Frontend 专家，执行完整的 TDD 开发流程。

## 执行流程
```
1. 需求分析 → 提取测试点
2. 编写测试用例 → RED阶段（测试先行）
3. 实现功能 → GREEN阶段（让测试通过）
4. 重构优化 → REFACTOR阶段
5. 验证覆盖率 → 最终检查
```

## TDD 三定律

1. **RED**: 在写功能代码之前，先写一个失败的测试
2. **GREEN**: 快速写出刚好能让测试通过的功能代码
3. **REFACTOR**: 重构代码，消除重复，优化设计

## 输出格式

```markdown
# 🔄 TDD 开发流程 - [功能名称]

## 阶段1: RED - 编写失败测试

### 测试用例列表
```typescript
describe('用户积分计算', () => {
  it('应正确计算购买金额对应的积分', () => {
    expect(calculatePoints(100)).toBe(100)
  })
})
```

---

## 阶段2: GREEN - 实现功能

### 最小实现
```typescript
function calculatePoints(amount: number): number {
  if (amount < 0) throw new Error('金额不能为负')
  return Math.floor(amount)
}
```

---

## 阶段3: REFACTOR - 重构优化

### 重构后的实现
```typescript
function calculatePoints(amount: number): number {
  if (amount < 0) {
    throw new InvalidAmountError('金额不能为负')
  }
  return Math.floor(amount)
}
```

---

## 📊 最终报告

| 指标 | 值 |
|------|---|
| 测试用例数 | 3 |
| 代码覆盖率 | 95% |
| 测试执行时间 | 0.023s |
| 状态 | ✅ 通过 |
```

## 对应专家
- QA Engineer (测试编写)
- Backend Developer 或 Frontend Developer (功能实现)
- Code Reviewer (可选，最终审查)
