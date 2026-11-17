# Dev 阶段方法论 (Stage 3)

> 融合: SP subagent-driven-dev + Ponytail Ladder + OpenSpec spec-impl + ECC build-fix + Codegraph

---

## 1. Ponytail Ladder 嵌入 Agent Prompt

每个 Dev Agent prompt 必须包含 Ladder 7 级决策梯。
禁止未请求的抽象、为"以后"的脚手架。
标记有意简化: `# ponytail: {ceiling}, {upgrade path}`

---

## 2. 双阶段审查 (from SP subagent-driven-dev)

替代原单阶段自审:

**Stage A: Spec 合规** — PRD 功能是否实现? API 契约一致? 数据模型匹配?
**Stage B: 代码质量** — Ladder 遵守? 无多余抽象? 错误处理完整? 安全就位?

两阶段都 PASS → 提交 Gate。任一 FAIL → fix → 重审（最多 3 轮）。

---

## 3. Minimal Verifiable Phase (from OpenSpec spec-impl)

不要一次完成所有任务。选 3-5 个为一批 → 实现 → 验证 → 下一批。
每批后运行 Build + Type Check + Test 确认增量可验证。

---

## 4. 并行开发增强 (from SP dispatching-parallel-agents)

每个并行 Agent prompt 必须含:
1. 完整 API 契约表
2. Gate 2 调整项
3. 目录范围（文件隔离）
4. Ladder 指令

原则: Focused prompts, specific scope, clear constraints.

---

## 5. Codegraph 集成

每次修改前 `codegraph_explore` 查影响范围 + 发现已有 helper (Ladder 第 2 级)。

---

## 6. Build 失败恢复 (from ECC build-fix)

Build 失败 → 最小 diff 修复循环:
- 解析错误按依赖排序，一次修一个
- 修完立即重建
- Stop-and-ask: 同错误 3 次 / 需架构变更
- 禁止: 重构、改名、加功能
