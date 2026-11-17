# PM 阶段方法论 (Stage 1)

> 融合: SP brainstorming + writing-plans + ECC planner + OpenSpec constraint sets + Ponytail YAGNI

---

## 1. 需求探索协议 (from SP brainstorming)

逐个提问，不一次性倾倒。根据回答决定下一个问题。

提出 2-3 个方案，带权衡（优点/缺点/工作量），附推荐方案。

### Spec 自审
- [ ] 无 placeholder（TBD/TODO/待定）
- [ ] 功能列表 vs 页面列表 vs API 端点一致
- [ ] MVP 边界明确

---

## 2. Pattern Grounding (from ECC planner)

**写 PRD 前先搜索代码库已有惯例：**

| 惯例类型 | 搜索什么 |
|----------|---------|
| 命名 | 文件名格式、变量名风格 |
| 错误处理 | try/catch 模式、错误类型 |
| 数据访问 | repository pattern? 直接 ORM? |
| 测试 | 测试结构、断言风格 |

PRD 新增 **Patterns to Mirror** 段 — 新代码必须镜像这些惯例。

---

## 3. 约束集思维 (from OpenSpec spec-research)

约束告诉后续阶段"不要考虑这个方向"。

PRD 新增 **Constraints** 段:
- **Hard Constraints**: 平台限制、合规要求、性能指标
- **Soft Constraints**: 代码风格、依赖控制、时间

---

## 4. YAGNI 裁剪 (from Ponytail)

对每个 Feature 问:
1. MVP 中真的需要吗？
2. 有没有更简单的替代？
3. 现有代码/native 能覆盖吗？

输出 **MVP Feature 裁剪表** (Feature / 保留-移除-简化 / 原因)

---

## 5. 任务分解 (from SP writing-plans)

任务粒度 2-5 分钟。每个任务有明确文件路径。
无 placeholder（"实现业务逻辑" 不合格）。
接口定义已确定（不留给实现阶段决定）。
