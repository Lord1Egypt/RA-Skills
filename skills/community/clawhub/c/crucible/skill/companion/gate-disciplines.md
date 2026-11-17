# Gate 阶段方法论

> 融合: ECC code-reviewer 误报过滤 + SP verification + receiving-code-review + branch-finishing

---

## 1. 误报过滤门 (from ECC code-reviewer)

报告每个 finding 前问 4 个问题:
1. 真的会导致运行时错误/安全漏洞/数据丢失吗？
2. 调用者是否已处理？
3. 这是代码库已有惯例吗？
4. 修复 diff 有多大？

任一为否 → 降低严重度或跳过。

### 12 种显式误报（直接跳过）

| # | 模式 | 原因 |
|---|------|------|
| 1 | "缺少错误处理" | 调用者已处理 |
| 2 | "magic number" | 公认常量 (200/404/8080) |
| 3 | "函数太长" | 单一职责清晰 |
| 4 | "缺少类型注解" | 类型可推导 |
| 5 | "重复代码" | 相似但不相同，提取更复杂 |
| 6 | "缺少测试" | getter/setter/config |
| 7 | "未使用变量" | 回调签名要求 |
| 8 | "嵌套太深" | 错误处理链 |
| 9 | "应用 const" | 确实需要重新赋值 |
| 10 | "应拆文件" | < 400 行，职责单一 |
| 11 | "缺少注释" | 代码自解释 |
| 12 | "性能问题" | 无证据的过早优化 |

---

## 2. 审查反馈处理 (from SP receiving-code-review)

禁止 "You're absolutely right!" — 先验证代码库，技术评估，YAGNI 检查评审建议。

| 严重度 | 处理 |
|--------|------|
| CRITICAL | 立即修复 |
| HIGH | 继续前修复 |
| MEDIUM | 记录，酌情 |
| LOW | 记录，不强求 |

---

## 3. Pre-Gate 自动化验证

所有 Gate 前必须先通过 (详见 `references/verification.md`):
Build → Type Check → Lint → Test (≥80%) → Security Scan → Diff Review

只有 READY 才进 Gate。

---

## 4. 分支收尾 (from SP finishing-a-development-branch)

所有 Gate PASS 后:
- 检测环境 (normal/worktree/detached HEAD)
- 3 选项: merge locally / push+PR / keep
- Discard 需明确确认
