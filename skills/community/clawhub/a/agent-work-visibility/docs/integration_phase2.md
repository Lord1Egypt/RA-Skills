# Agent Work Visibility - Phase 2 接入设计

**版本：** v0.2.0  
**日期：** 2026-03-18  
**阶段：** 真实接入与验证

---

## 一、接入目标

### 核心目标

将 Agent Work Visibility MVP 接入真实可运行的 Research Agent，用真实任务连续跑至少 10 个长任务，验证产品效果。

### 接入对象

| 优先级 | Agent 类型 | 说明 |
|--------|-----------|------|
| P0 | Research Agent | 调研、搜索、比较、整理、写摘要 |
| P1 | Browser Agent | 连续读取网页、跨站点收集信息 |

**本阶段优先完成：Research Agent 接入**

---

## 二、事件源梳理

### Research Agent 真实事件列表

以下为 Research Agent 执行过程中可捕获的原始事件：

| 事件 | 触发时机 | 当前映射 |
|------|---------|---------|
| `task_start` | 任务开始执行 | `task_started` |
| `task_replan` | 任务重新规划 | `planning_started` |
| `phase_start` | 阶段开始 | `phase_started` |
| `search_query_built` | 搜索查询构建完成 | `search_query_defined` |
| `page_fetch_start` | 开始抓取网页 | `page_fetch_started` |
| `page_fetch_timeout` | 网页抓取超时 | `page_fetch_timeout` |
| `page_fetch_success` | 网页抓取成功 | `page_fetch_completed` |
| `retry_started` | 开始重试 | `retry_attempt` |
| `retry_success` | 重试成功 | `retry_success` |
| `retry_failed` | 重试失败 | `retry_failed` |
| `extraction_done` | 数据提取完成 | `extraction_completed` |
| `shortlist_done` | 候选名单确定 | `extraction_completed` |
| `compare_started` | 开始比较分析 | `comparison_started` |
| `conflict_detected` | 发现信息冲突 | `cross_validation_started` |
| `draft_started` | 开始生成输出 | `output_generating` |
| `user_input_required` | 需要用户输入 | `user_input_requested` |
| `task_complete` | 任务完成 | `task_completed` |
| `task_failed` | 任务失败 | `task_failed` |

### 事件分类

| 类别 | 事件 | 用途 |
|------|------|------|
| **阶段事件** | phase_start, phase_complete | 更新 current_phase, progress |
| **进度事件** | page_fetch_start, extraction_done | 更新 phase_progress, action_log |
| **阻塞事件** | timeout, auth_required, conflict | 触发 blocker_detector |
| **介入事件** | user_input_required | 触发 ask_human_builder |
| **完成事件** | task_complete, task_failed | 更新 overall_status |

---

## 三、事件映射层设计

### Adapter 架构

```
┌─────────────────────────────────────────────────────────┐
│                    Research Agent                        │
│  (原始事件：task_start, page_fetch_timeout, etc.)        │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Event Adapter                          │
│  - 事件标准化 (normalize)                                │
│  - 事件翻译 (translate)                                  │
│  - 阻塞检测 (detect_blocker)                             │
│  - 介入触发 (trigger_ask_human)                          │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Visibility Skill (现有 MVP)                  │
│  - TaskVisibilityManager                                 │
│  - 状态维护 + 视图渲染                                    │
└─────────────────────────────────────────────────────────┘
```

### 映射规则

| 原始事件 | 标准化事件 | 人类可读动作 | 阻塞检测 |
|---------|-----------|-------------|---------|
| `page_fetch_start` | `fetch_started` | "正在读取第 X 个网页" | - |
| `page_fetch_timeout` | `fetch_timeout` | "网页加载超时，正在重试" | `low` (首次) |
| `retry_started (n>3)` | `retry_exhausted` | "多次重试失败" | `medium` |
| `conflict_detected` | `info_conflict` | "发现信息不一致，正在交叉验证" | 判断是否需介入 |
| `auth_required` | `auth_needed` | "需要登录才能访问" | `medium` |
| `scope_expansion` | `scope_grow` | "发现扩展内容" | 判断是否需确认 |

---

## 四、Snapshot 触发时机

### 必须更新 snapshot 的时刻

| 时机 | 触发条件 | 更新内容 |
|------|---------|---------|
| 任务开始 | `task_start` | 初始化状态，创建默认视图 |
| 阶段切换 | `phase_start` | 更新 current_phase, progress |
| 进度更新 | `phase_progress >= 25%` | 更新 progress_percent |
| 阻塞发生 | `blocker_detected` | 更新 blocker_status, why_not_done |
| 阻塞解除 | `blocker_cleared` | 清除阻塞状态 |
| Ask Human | `user_input_required` | 设置 needs_user_input, user_question |
| 用户响应 | `user_input_provided` | 清除介入状态 |
| 任务完成 | `task_complete` | 更新 overall_status, completed_at |

### Snapshot 历史记录

每个任务保留关键 snapshot：

```
artifacts/phase2/{task_id}/
├── snapshot_init.json       # 初始状态
├── snapshot_phase_1.json    # 阶段 1 完成
├── snapshot_phase_2.json    # 阶段 2 完成
├── snapshot_blocked.json    # 阻塞状态（如有）
├── snapshot_ask_human.json  # Ask Human（如有）
└── snapshot_final.json      # 最终状态
```

---

## 五、Blocker / Ask Human 校准策略

### Blocker 校准目标

| 问题 | 当前规则 | 验证目标 |
|------|---------|---------|
| 超时多久算阻塞？ | 立即 | 5 秒后显示 waiting，30 秒后显示 blocked |
| 重试中显示什么？ | blocked | waiting（可自动恢复） |
| 页面加载慢 vs 失败？ | 统一超时 | 区分 slow (>5s) 和 failed (>30s) |
| 长推理停顿？ | 可能误报 | 检测 CPU/推理活动，避免误报 |
| 信息冲突？ | 可能阻塞 | 判断是否需要用户决策 |

### Ask Human 校准目标

| 场景 | 触发条件 | 验证目标 |
|------|---------|---------|
| 选方向 | 发现≥3 个可深入方向 | 只在高价值节点触发 |
| 补范围 | 搜索结果<3 条 | 避免过早触发 |
| 确认扩大 | 范围扩大>50% | 需要用户确认 |
| 登录/授权 | 遇到 login wall | 明确提示 |
| 信息冲突 | 关键信息矛盾 | 判断是否需人工裁决 |

---

## 六、本阶段不做什么

### 明确排除的功能

| 功能 | 原因 |
|------|------|
| 多 Agent 任务树 | V3 范围 |
| Manager 总览面板 | V3 范围 |
| 复杂前端 Dashboard | MVP 文本视图已足够 |
| 完整通知系统 | 只做内部 hook |
| Confidence Score 正式版 | V2 范围 |
| SDK / Protocol 化 | V4 范围 |
| Developer Trace Mode | V4 范围 |

### 本阶段只做

- ✅ 接入真实 Research Agent
- ✅ 跑 10 个真实任务
- ✅ 保存 artifacts
- ✅ 输出验证报告
- ✅ 校准 blocker/ask-human 规则
- ✅ 优化默认视图文案

---

## 七、10 个真实任务设计

### A 组：正常完成任务（3 个）

| 任务 ID | 任务描述 | 预期时长 |
|--------|---------|---------|
| `task-001` | 调研 1 个 AI Agent 基础设施项目 | 3-5 分钟 |
| `task-002` | 比较 3 个类似项目的功能和定位 | 5-8 分钟 |
| `task-003` | 搜索并整理最近 3 个月的行业新闻 | 4-6 分钟 |

### B 组：中途等待/重试（3 个）

| 任务 ID | 任务描述 | 预期阻塞 |
|--------|---------|---------|
| `task-004` | 抓取响应慢的网页 | API 超时 |
| `task-005` | 访问限流的数据源 | Rate Limited |
| `task-006` | 部分内容加载失败 | 部分失败后恢复 |

### C 组：需要用户介入（2 个）

| 任务 ID | 任务描述 | 介入类型 |
|--------|---------|---------|
| `task-007` | 发现多个深入方向 | 方向选择 |
| `task-008` | 任务范围显著扩大 | 范围确认 |

### D 组：失败/卡住任务（2 个）

| 任务 ID | 任务描述 | 预期失败 |
|--------|---------|---------|
| `task-009` | 访问需要登录的资源 | 权限不足 |
| `task-010` | 关键数据源不可用 | 资源不可用 |

---

## 八、验证指标

### 产品效果指标

| 指标 | 测量方式 | 目标 |
|------|---------|------|
| 3 秒理解率 | 用户能否 3 秒看懂 | ≥90% |
| 阻塞准确率 | blocker 误报/漏报 | 误报<10% |
| Ask Human 价值 | 用户是否认为有帮助 | ≥80% 正面 |
| 文案清晰度 | 是否太空/太技术 | 无太空文案 |
| 信息过载 | 默认视图是否简洁 | ≤7 个字段 |

### 技术指标

| 指标 | 测量方式 | 目标 |
|------|---------|------|
| Snapshot 可用性 | 任意时刻可调用 | 100% |
| 事件映射覆盖率 | 原始事件→标准化 | ≥90% |
| 历史记录完整性 | 关键 snapshot 保存 | 100% |

---

## 九、交付物

### 必须产出

| 文件 | 内容 |
|------|------|
| `docs/integration_phase2.md` | 本文件，接入设计 |
| `docs/validation_report_phase2.md` | 验证报告 |
| `artifacts/phase2/` | 10 个任务 artifacts |
| `src/adapters/research_agent_adapter.js` | 事件映射层 |
| `src/hooks/simple_hooks.js` | 简单通知钩子 |
| `src/history/snapshot_history.js` | Snapshot 历史 |

### 可选产出

| 文件 | 内容 |
|------|------|
| `src/adapters/browser_agent_adapter.js` | Browser Agent 适配 |
| `examples/real_task_examples.md` | 真实任务示例 |

---

## 十、执行计划

| 步骤 | 内容 | 预计时间 |
|------|------|---------|
| 1 | 梳理真实 agent 事件源 | 1 小时 |
| 2 | 做 adapter / mapping | 2 小时 |
| 3 | 接入 snapshot 更新链路 | 2 小时 |
| 4 | 跑 10 个真实任务 | 4 小时 |
| 5 | 保存 artifacts | 1 小时 |
| 6 | 写 validation report | 2 小时 |
| 7 | 给出 V2 最小升级建议 | 1 小时 |

**总计：约 13 小时**

---

## 十一、风险与应对

| 风险 | 影响 | 应对 |
|------|------|------|
| 真实 agent 事件不足 | 无法完整映射 | 补充模拟事件 |
| 任务执行时间过长 | 验证周期拉长 | 优先短任务 |
| 误报率高 | 用户不信任 | 快速迭代校准 |
| Ask Human 太频繁 | 用户烦躁 | 收敛触发条件 |

---

## 十二、版本历史

| 版本 | 日期 | 内容 |
|------|------|------|
| v0.2.0 | 2026-03-18 | Phase 2 接入设计 |

---

## 十三、参考

- MVP 设计文档：`docs/agent_work_visibility_mvp.md`
- 技能文档：`SKILL.md`
- 交付总结：`DELIVERY.md`
