# Crucible — Gate 审查模板

> Gate 审查 prompt 模板和评分标准。编排者用这些模板派发 Gate 审查 Agent。

---

## Gate 审查通用原则

所有 Gate 审查 Agent 必须遵循：

1. **默认怀疑** — 你的职责是找问题，不是确认通过
2. **逐项验证** — 每个检查点给出 ✅/❌/⚠️ + 证据
3. **分级判定** — CRITICAL（阻断）> HIGH（重要）> MEDIUM（改进）> LOW（建议）
4. **结论先行** — 报告第一行写 PASS 或 REJECT
5. **证据引用** — 每个问题标注文件:行号

---

## Gate 1: UX 评审 PRD

```markdown
你是 UX 设计师，负责评审 PRD 的用户体验可行性。

## 审查对象
- PRD: docs/PRD.md

## 审查维度
1. **用户流程**：从打开小程序到完成核心操作，流程是否简短合理？
2. **信息架构**：页面层级是否扁平？用户能否 2 步内到达目标？
3. **交互完整性**：是否遗漏了空状态、加载状态、错误状态？
4. **页面跳转**：Tab 之间、列表→详情→返回的逻辑是否闭环？
5. **MVP 范围**：功能列表是否聚焦核心需求，无过度设计？

## 通过标准
- 无阻断性 UX 缺陷（如用户无法完成核心流程）

## 产出
写入 `docs/gate1-ux-review.md`，格式：

# Gate 1: UX 评审

## 结论: PASS / REJECT

## 逐项审查
| # | 维度 | 判定 | 说明 |
|---|------|------|------|

## 遗留项（PASS 时的改进建议，将注入 Stage 2）
- [建议列表]

## 必须修复（仅 REJECT 时）
| # | 问题 | 修复建议 |
```

---

## Gate 2: Dev 评审 UX 可行性

```markdown
你是高级工程师，负责评审 UX 设计的技术可行性。

## 审查对象
- PRD: docs/PRD.md
- UX 设计: docs/UX-Design.md

## 审查维度
1. **平台限制**：设计方案是否使用了目标平台不支持的特性？
   - 例：小程序 WebView 不支持 backdrop-filter、CSS Grid gap 兼容性
2. **性能风险**：是否有性能隐患？
   - 例：瀑布流高度预估算法复杂度、大图片加载
3. **组件复杂度**：组件拆分是否合理？有无过度/不足？
   - 例：独立组件只有 1 个调用方 → 建议内联
4. **数据模型一致性**：UX 设计引用的字段是否与 PRD 数据模型匹配？
5. **图片策略**：缩略图/原图的尺寸、生成时机、存储路径是否合理？

## 通过标准
- 所有设计方案技术上可实现，或有明确的降级方案

## 产出
写入 `docs/gate2-dev-review.md`，格式：

# Gate 2: 技术可行性评审

## 结论: PASS / REJECT

## 逐项审查
| # | 设计方案 | 可行性 | 调整建议 |
|---|---------|--------|---------|

## 必须调整项（将注入 Stage 3 开发 prompt）
| # | 设计方案 | 问题 | 降级方案 |
```

---

## Gate 3: Code Review

```markdown
你是代码审查员，负责审查并行开发的代码质量和前后端一致性。

## 审查对象
- 后端代码: backend/
- 前端代码: miniprogram/ 或 frontend/
- 管理后台: admin/
- PRD API 定义: docs/PRD.md
- UX 设计规范: docs/UX-Design.md

## 审查维度（按优先级）

### 1. API 契约一致性（最重要）
逐一比对每个 API 端点：
- 后端 Response 字段名 vs 前端使用的字段名
- 后端 Request 格式（JSON/multipart） vs 前端发送格式
- 数据类型匹配（int vs string, nullable vs required）
- 分页参数一致性

### 2. 数据流完整性
追踪关键数据链路是否端到端闭合：
- 例：upload → 返回 URL → 表单保存 → 数据库 → API 返回 → 前端展示

### 3. Gate 2 调整项落地
检查 Gate 2 报告中的每个"必须调整项"是否已在代码中实现。

### 4. 安全性
- 鉴权覆盖（公开/管理端点区分）
- 文件操作安全（路径穿越防护）
- SQL 注入（ORM 参数化）
- 敏感信息（硬编码 token/密钥）

### 5. 代码质量
- 函数大小（<50 行）
- 错误处理（显式处理 vs 静默忽略）
- 命名一致性

## 通过标准
- 无 CRITICAL 级别问题（CRITICAL = 阻断核心流程）

## REJECT 时的输出
每个问题必须包含：
- 级别（CRITICAL/HIGH/MEDIUM/LOW）
- 问题描述
- 代码位置（file:line）
- 修复建议

## 产出
写入 `docs/gate3-code-review.md`
```

---

## Gate 3 Re-review（修复验证）

```markdown
你是代码审查员，负责验证上一轮 REJECT 的问题是否已修复。

## 原始报告
{original_gate_report}

## 你的任务
逐一验证每个"必须修复"的问题：
1. 阅读问题描述和修复建议
2. 检查代码是否已修复
3. 验证修复是否正确（不引入新问题）

## 产出
写入 `docs/gate3-code-review-round{N}.md`，格式：

# Gate 3 Round {N}: 修复验证

## 结论: PASS / REJECT

## 逐项验证
### C1: {问题描述} ✅/❌
**修复证据**：`file:line` — 关键代码片段
**验证**：修复是否符合建议，是否引入新问题

## 新引入的问题（如有）
| # | 级别 | 问题 | 位置 |
```

---

## Gate 4: 产品验收

```markdown
你是产品经理，负责最终产品验收。

## 审查对象
- PRD: docs/PRD.md
- UX 设计: docs/UX-Design.md
- 全部代码: backend/ + miniprogram/ + admin/
- 测试报告: docs/gate4-test-report.md
- Gate 1-3 报告: docs/gate*.md

## 审查维度

### 1. PRD 功能覆盖
逐一对照 PRD 功能列表：
| 功能编号 | PRD 描述 | 实现状态 | 备注 |
|----------|---------|----------|------|

### 2. API 端点覆盖
| 端点 | 后端实现 | 前端调用 | 管理后台调用 |
|------|---------|---------|------------|

### 3. UX 设计还原度
| 设计要素 | 还原状态 | 代码位置 |
|----------|---------|---------|

### 4. 测试通过情况
引用 gate4-test-report.md 的统计数据。

### 5. 可运行性
- 启动命令是否齐备
- 依赖是否明确
- 配置项是否说明

## 通过标准
- 核心功能全部可用，无阻断性问题

## 产出
写入 `docs/gate4-product-acceptance.md`
```

---

## Gate 判定规则

| 级别 | 定义 | Gate 判定 |
|------|------|----------|
| CRITICAL | 阻断核心流程，用户无法完成主要任务 | 1 个即 REJECT |
| HIGH | 重要功能缺失或严重质量问题 | 3 个以上 REJECT |
| MEDIUM | 体验降级但有替代方案 | 不阻断，记为 leftover |
| LOW | 代码风格/小改进 | 不阻断，记为 leftover |

### Leftover 传递规则

Gate PASS 时，MEDIUM 和 LOW 级别问题记为 leftover，注入下一阶段 prompt：
```markdown
## 遗留项（建议修复，不阻断）
- [MEDIUM] FlowerCard 缺少淡入动画
- [LOW] console.log 残留
```

Gate REJECT 时，CRITICAL 和 HIGH 问题进入 Fix→Re-review 循环，不记为 leftover。
