---
name: "dtwo-workflow-guide"
description: "通过 TaskFlow 编排预处理（审核、分类、元数据填充），再用 ClawHub CLI 完成数字资源入库的可复现操作指南与实操记录。"
metadata:
  clawdbot:
    emoji: "🔧"
    requires:
      - taskflow
  author: "terrycarter1985"
  created: "2026-10-07"
  updated: "2026-10-07"
  version: "1.0.0"
  license: "MIT"
  tags:
    - "digital-resource"
    - "workflow"
    - "taskflow"
    - "clawhub"
    - "ingest"
    - "guide"
  category: "guide"
  source: ""
  dependencies:
    - "taskflow"
  related:
    - "digital-resource-management-guide"
    - "digital-resource-ingest-demo"
---

# TaskFlow × ClawHub 数字资源入库操作指南

本资源是一次**真实入库**的产物：先用 TaskFlow 风格的业务流程对内容做预处理
（审核、分类、元数据填充、质量门禁），再用 `clawhub publish` 发布到 ClawHub
资源中心，最后用 `clawhub inspect` / `clawhub search` 验证。

## 1. 两个工具

- **TaskFlow（业务流程处理）**：为多步、可能跨会话/跨子代理的工作流提供
  持久化状态、孩子任务链接、等待/恢复与 revision 安全的状态变更。负责
  "处理"阶段。
- **ClawHub CLI（数字资源入库与管理）**：`publish` 将本地资源目录发布到
  资源中心，`inspect`/`search` 验证元数据与可发现性。负责"入库"阶段。

## 2. 串联流程（可复现）

1. 准备资源目录，编写 `SKILL.md` 并填充必填元数据
   （name/description/author/created/version/tags）。
2. 用 TaskFlow 风格状态机驱动预处理：create → runTask(审核/分类/元数据)
   → 质量门禁（checklist）→ finish。
3. 执行 `clawhub publish <dir> --slug ... --name ... --version ... --changelog ...`。
4. 执行 `clawhub inspect <slug>` 与 `clawhub search "<关键词>"` 验证。

## 3. 关键注意事项

- 元数据 description 控制在 10–200 字；tags 3–8 个。
- 无敏感信息、无版权争议、无可疑代码。
- 每次状态变更携带最新 `revision`，避免并发覆盖。
- 发布前用 `--dry-run` 预览，正式发布用真实参数。

## 4. 本次实操记录

- flowId: `flow-demo-20261007-001`
- 预处理：审核 → 分类(guide) → 元数据填充 → 质量门禁通过
- 发布：`clawhub publish` 到 ClawHub Registry
- 验证：inspect + search 命中

---

**入库记录**
- 发布时间: 2026-10-07
- 发布者: terrycarter1985
- 资源中心: ClawHub Registry
- 状态: 已发布
