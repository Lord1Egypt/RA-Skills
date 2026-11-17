# Test 阶段方法论 (Stage 4)

> 融合: SP TDD + BDD + systematic-debugging + ECC e2e-testing + Ponytail YAGNI

---

## 1. TDD Iron Law (from SP, 可选 --tdd 模式)

RED → GREEN → REFACTOR → 重复。没有失败测试就不能写生产代码。

常见借口: "太简单不需测试" → 非平凡逻辑留 ONE runnable check。
"先实现后补测试" → 删掉代码，先写测试。
"测试拖慢速度" → 短期慢，长期快 10x。

---

## 2. BDD 场景 (from SP behavior-driven-development)

Given/When/Then 格式:
- Happy path: 至少 1 个
- 每个输入验证: 至少 1 个失败场景
- 权限: 无权限 / 有权限各 1 个
- 边界: 空值 / 超长 / 特殊字符

---

## 3. 系统调试法 (from SP systematic-debugging)

4 阶段:
1. **根因调查** — 读完整错误、复现、git log 最近改动、追踪数据流
2. **模式分析** — 找能工作的类似代码，对比差异
3. **假设验证** — 一次改一个变量，有预测
4. **最小修复** — 先写失败测试 → 最小修复 → 回归测试

**3+ 次修复失败 = 质疑架构**

---

## 4. E2E 测试 (from ECC e2e-testing, 可选)

Playwright Page Object Model。Flaky 测试用 `test.fixme()` quarantine。
识别 flaky: `--repeat-each=10`。

---

## 5. YAGNI 应用于测试 (from Ponytail)

Trivial one-liners 不需测试。非平凡逻辑留 ONE runnable check。
最简单框架: 语言 assert > Jest/pytest > 不需 framework。
