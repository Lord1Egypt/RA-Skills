# AI 友好技术文档模板

将产品需求文档转化为以下结构化格式，便于 AI 阅读和理解。

## 模板结构

以下为完整模板，每个 `##` 章节为一个独立模块。使用时复制整个模板，按需填写。

---

### META（元信息）

| 字段 | 值 |
|------|---|
| requirement_id | {唯一标识} |
| type | frontend / backend / ops |
| sub_type | {子类型} |
| priority | P0 / P1 / P2 |
| status | draft / review / approved / dev / testing / released |
| author | {作者} |
| reviewer | {评审人} |
| created | {创建日期} |
| updated | {更新日期} |
| version | {版本号} |

### SUMMARY

{一段话描述需求的核心内容，50-100字}

### PROBLEM

- current_state: {现状描述}
- pain_points:
  - {痛点1}
  - {痛点2}
- metrics_before:
  - {指标1}: {当前值}
  - {指标2}: {当前值}

### GOAL

- target_metrics:
  - {指标1}: {目标值}
  - {指标2}: {目标值}
- success_criteria:
  - {标准1}
  - {标准2}

### SCOPE

- in_scope:
  - {范围内1}
  - {范围内2}
- out_of_scope:
  - {范围外1}
  - {范围外2}
- dependencies:
  - {依赖1}: {说明}
  - {依赖2}: {说明}

### USER_SCENARIOS

**scenario_{n}**:
- name: {场景名}
- actor: {用户角色}
- precondition: {前置条件}
- steps:
  1. {步骤1}
  2. {步骤2}
- expected_result: {预期结果}
- exception_flows:
  - {异常1}: {处理方式}
  - {异常2}: {处理方式}

## PROCESS_MODEL（分层建模，按需填写）

### L1_MAIN_FLOW（业务主干，面向管理层，5-8个节点）
- steps:
  1. {步骤1}
  2. {步骤2}
  3. {步骤3}
- 说明：纯线性主干，无判断分支，任何人 10 秒内能看懂

### L2_SYSTEM_FLOW（系统泳道图，面向技术团队）
- swimlanes: [{角色/系统1}, {角色/系统2}, ...]
- flow:
  | {泳道1} | {泳道2} | {泳道3} |
  |---------|---------|---------|
  | {动作}  |         |         |
  |         | {动作}  |         |
  |         |         | {动作}  |
- async_marks:
  - {步骤X}: 【异步回调】
  - {步骤Y}: 【定时任务】

### L3_STATE_MACHINE（FSM 状态图，面向开发/测试）
| 当前状态 | 事件 | 下一状态 | 副作用 |
|---------|------|---------|--------|
| {状态A} | {事件} | {状态B} | {操作} |

### L4_DECISION_TABLES（规则/决策表，面向运营/风控）
#### rule_{n}: {规则名} (V{版本号})
| {条件1} | {条件2} | {条件3} | 结果 |
|---------|---------|---------|------|
| {值}    | {值}    | {值}    | {结果} |

### L5_INTERACTION_FLOW（交互流程，面向设计/前端）
- pages: [{页面1} → {页面2} → {页面3}]
- 各页面状态见 UI_SPEC 章节

### EXCEPTION_FLOWS（异常场景表）
| 异常场景 | 触发条件 | 处理逻辑 | 用户提示 |
|---------|---------|---------|---------|
| {场景} | {条件} | {逻辑} | {提示} |

### GUARD_CLAUSES（前置校验/卫语句）
| 校验项 | 校验逻辑 | 失败处理 |
|--------|---------|---------|
| {校验} | {逻辑}  | {处理}  |

### UI_SPEC（前端需求必填）

**page_{n}**:
- name: {页面名}
- url: {路由}
- components:
  - {组件1}: {描述}
  - {组件2}: {描述}
- states:
  - empty: {空态描述}
  - loading: {加载态}
  - normal: {正常态}
  - error: {错误态}
- interactions:
  - {交互1}: {描述}
- assets: {交互稿/视觉稿路径}

### API_SPEC（后端需求必填）

**api_{n}**:
- method: GET / POST / PUT / DELETE
- path: {接口路径}
- description: {接口说明}
- request: `{请求JSON示例}`
- response: `{响应JSON示例}`
- error_codes:

| code | message | 说明 |
|------|---------|------|
| {码} | {消息} | {说明} |

- performance:
  - expected_qps: {预估QPS}
  - response_time_p99: {P99响应时间}
  - cache_strategy: {缓存策略}

### DATA_MODEL（后端需求必填）

**table_{n}**: {表名} — {说明}

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| {字段} | {类型} | {是/否} | {默认} | {说明} |

- indexes:
  - {索引名}: {字段} ({类型})

### OPS_CONFIG（运营需求必填）

**config_items**:

| 配置项 | 类型 | 默认值 | 说明 | 生效方式 |
|--------|------|--------|------|---------|
| {配置} | {类型} | {默认} | {说明} | 实时/重启 |

**activity_rules**:
- time_range: {开始} ~ {结束}
- target_users: {用户范围}
- discount_rules:
  - {规则1}
  - {规则2}
- budget_limit: {预算上限}
- per_user_limit: {单用户上限}

### TRACKING

**events**:

| 事件名 | 触发时机 | 参数 | 用途 |
|--------|---------|------|------|
| {事件} | {时机} | {参数列表} | {分析用途} |

**dashboards**:
- {看板1}: {包含的指标}
- {看板2}: {包含的指标}

### SECURITY

- data_classification: {数据分级}
- encryption: {加密方案}
- access_control: {权限控制}
- audit_log: {审计要求}
- compliance: {合规要求}

### RELEASE_PLAN

- phases:
  1. {阶段1}: {内容} ({时间})
  2. {阶段2}: {内容} ({时间})
- grayscale:
  - stage_1: {比例} ({条件})
  - stage_2: {比例} ({条件})
  - full: {全量条件}
- rollback_plan: {回滚方案}
- monitoring:
  - {监控项1}: {告警阈值}
  - {监控项2}: {告警阈值}

### RISKS

| 风险 | 等级 | 概率 | 影响 | 应对方案 |
|------|------|------|------|---------|
| {风险} | 高/中/低 | {概率} | {影响} | {方案} |

### ACCEPTANCE_CRITERIA

- [ ] {验收条件1}
- [ ] {验收条件2}
- [ ] {验收条件3}

### CHANGELOG

| 版本 | 日期 | 作者 | 变更内容 |
|------|------|------|---------|
| {版本} | {日期} | {作者} | {变更} |

## 转化规则

将产品需求文档转化为技术文档时遵循以下原则：

1. **结构化优先**：将自然语言描述转为 key-value 或表格
2. **消除歧义**：模糊表述转为精确定义
3. **补充缺失**：标注原文档未覆盖的必填项为 `[TODO]`
4. **保留原意**：不改变需求本身的含义
5. **图片引用**：保留原图引用路径，标注图片内容摘要
6. **HTML 解析**：提取 HTML 中的交互逻辑和页面结构，转为 UI_SPEC
