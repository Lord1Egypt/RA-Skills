# Crucible — 实战经验总结

> 来自 sparks-lab 项目（花艺展示小程序）的完整 Pipeline 实战经验。

---

## 项目背景

- **需求**: 花艺展示微信小程序（瀑布流浏览 + 分类 + 全屏详情 + 后台管理）
- **技术栈**: Python FastAPI + uni-app Vue 3 + Vue 3 Element Plus
- **团队规模**: 1 人（Claude Code 编排 + 多个 Agent 执行）
- **Pipeline**: 完整 8 阶段，含 1 次 Gate REJECT 循环

---

## 关键教训

### 1. Gate 3 是价值最高的门禁

**现象**: 并行开发（backend + miniprogram + admin）后，Gate 3 首轮发现 4 项 CRITICAL：

| # | 问题 | 影响 |
|---|------|------|
| C1 | POST /images 后端期望 multipart，Admin 发送 JSON | 图片创建完全不可用 |
| C2 | 图片 URL 缺少前导 `/`，小程序无法拼接 | 所有图片 404 |
| C3 | 字段名 `count` vs `image_count` | 分类计数始终为 0 |
| C4 | 文件删除基于 CWD 路径 | 删除静默失败 |

**教训**: 并行开发必然导致前后端契约不一致。Gate 3 的 API 契约验证是 Pipeline 的核心价值。

**建议**: Gate 3 prompt 必须包含完整的 API 契约表，要求审查员逐字段比对。

---

### 2. API 契约必须前置注入

**现象**: 三个开发 Agent 各自理解 PRD 中的 API 定义，产生了不同的实现。

**根因**: PRD 中的 API 定义是文字描述，不同 Agent 的理解有偏差（如 JSON vs multipart）。

**解决**: 编排者在 Stage 3 启动前，从 PRD 提取 **结构化 API 契约表**，注入每个 Agent 的 prompt：

```markdown
| 方法 | 路径 | Request 格式 | Response 字段 |
|------|------|-------------|--------------|
| POST | /images | JSON: {name, image_url, thumb_url?, category_id} | {id, name, ...} |
```

---

### 3. Re-review 发现新引入问题

**现象**: Gate 3 Round 2 验证 4 项修复时，发现 1 项新 HIGH 问题：
- upload 端点丢弃了 `thumb_url`（`url, _ = save_upload(file)`）
- 缩略图链路断裂：生成→返回→保存→展示，在"返回"环节断了

**教训**: Fix Agent 修复问题时可能引入新问题。Re-review 不仅要验证修复，还要检查修复是否引入新问题。

**建议**: Re-review prompt 必须包含"检查修复是否引入新问题"的维度。

---

### 4. 遗留项传递的价值

**现象**: Gate 2 的 leftover "FlowerImage 增加 thumb_url 字段" 成功传递到 Stage 3，后端数据模型正确包含该字段。

**教训**: Gate leftover 自动传递是 Pipeline 的关键机制。它确保上游审查的发现不会在下游被遗忘。

**建议**: 编排者必须显式提取 Gate 报告的 leftover 列表，注入下一阶段的 prompt 中。

---

### 5. UX 降级方案需在 Gate 2 确认

**现象**: UX 设计使用了 `backdrop-filter`（毛玻璃效果），但小程序 WebView 不支持。

**发现时机**: Gate 2 Dev 评审。

**降级方案**: `backdrop-filter` → `rgba(0,0,0,0.35)` 纯色蒙层。

**教训**: Gate 2 的技术可行性评审能提前发现平台限制，避免开发阶段返工。

---

### 6. 并行开发的文件隔离

**现象**: 3 个开发 Agent 分别操作 `backend/`、`miniprogram/`、`admin/`，零文件冲突。

**教训**: 并行开发的前提是严格的文件隔离。编排者在 prompt 中明确每个 Agent 的目录范围。

**建议**: 并行 Agent 的 prompt 必须包含"只操作以下目录"的约束。

---

### 7. 测试用内存数据库

**现象**: SQLite 内存数据库在 Windows 上需要 `StaticPool`，默认的 `file::memory:` URL 不工作。

**解决**: 
```python
engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
```

**教训**: 测试环境的平台差异需要在 conftest.py 中处理。

---

## Pipeline 执行统计

| 阶段 | 耗时 | Agent 模型 | 产出 |
|------|------|-----------|------|
| Stage 1: PM | ~3 min | sonnet | PRD.md (116 行) |
| Gate 1: UX 评审 | ~2 min | sonnet | PASS + 5 leftovers |
| Stage 2: UX 设计 | ~5 min | sonnet | UX-Design.md (392 行) |
| Gate 2: Dev 评审 | ~3 min | sonnet | PASS + 2 调整项 |
| Stage 3: 开发 (×3 并行) | ~15 min | sonnet ×3 | 47 文件 |
| Gate 3: Code Review R1 | ~5 min | sonnet | REJECT (4 CRITICAL) |
| Stage 3.5: Fix | ~8 min | sonnet | 修复 4 项 + 4 HIGH |
| Gate 3: Re-review R2 | ~3 min | sonnet | PASS + 1 新 HIGH |
| Stage 3.6: Fix thumb_url | ~2 min | sonnet | 缩略图链路修复 |
| Stage 4: 测试 | ~5 min | sonnet | 18/18 PASS |
| Gate 4: 产品验收 | ~3 min | sonnet | PASS |
| **总计** | **~55 min** | | **55+ 文件, 8 文档** |

---

## 适用场景

### 适合使用完整 Pipeline

- 从 0 到 1 的新产品（需要 PM + UX + Dev + Test）
- 多端并行开发（backend + frontend + admin）
- 需要质量保障的交付（Gate 审查拦截问题）

### 适合使用最小 Pipeline

- 已有设计稿，只需 Dev + Review
- 单模块开发，不需要跨角色协作
- 快速原型验证

### 不适合使用

- 单文件修改或小 bug 修复（用 `orch-fix-defect`）
- 已有完整 spec 的 MVP 构建（用 `orch-build-mvp`）
- 纯重构任务（用 `orch-refine-code`）
