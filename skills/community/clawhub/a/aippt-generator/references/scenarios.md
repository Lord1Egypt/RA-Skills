# 场景诊断配置

6 大业务场景的诊断问题与业务字段。收集内容时逐项确认，数据越具体生成质量越高。

---

## 1. boss_report（老板汇报）

**适用**：工作汇报 / 申请预算 / 申请项目 / 销售提案

### 基础问题

| 字段 | 标签 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| topic | 汇报主题 | text | ✓ | 如：Q4季度营销预算申请 |
| audience | 汇报对象 | select | ✓ | 老板/客户/投资人/团队 |
| duration | 汇报时长 | select | ✓ | 10/20/30分钟 |
| purpose | 汇报目的 | select | ✓ | 工作汇报/申请预算/申请项目/销售提案 |
| industry | 所属行业 | text | | 如：互联网、制造、金融 |
| existing_material | 现有资料 | select | | 有详细数据/暂无 |

### 业务字段

**快速模式**：只收集 3 个核心字段即可生成（标记 ★），其余字段可选填或由 AI 推断。

| 字段 | 标签 | 必填 | 要点 |
|------|------|------|------|
| topic ★ | 汇报主题 | ✓ | 如：Q4季度营销预算申请 |
| core_conclusion ★ | 核心结论（一句话） | ✓ | 整份PPT的灵魂——所有页面围绕这句话展开 |
| context_problem ★ | 为什么做（背景与问题） | ✓ | 市场变化、当前问题、为什么是现在 |
| risk_of_inaction | 不做的风险 | △ | 申请预算/项目时必填；工作汇报时可不填 |
| key_data | 关键数据支撑 | | 3-8条数据，每条带对比基准（同比/环比/竞对） |
| solution_plan | 方案与计划 | △ | 申请预算/项目时必填；纯工作汇报可不填 |
| expected_outcome | 预期收益 | △ | 申请预算/项目时必填；工作汇报可不填 |
| additional_info | 其他补充信息 | | 竞品动态、特殊情况等 |

> ✓ = 所有模式必填 | △ = 根据汇报目的决定是否必填 | 空 = 可选填

---

## 2. client_proposal（客户方案）

**适用**：从需求分析到方案呈现的专业提案

### 基础问题

| 字段 | 标签 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| client_name | 客户名称 | text | ✓ | 如：某大型制造企业 |
| industry | 客户行业 | text | ✓ | 如：制造业、金融 |
| budget_range | 预算规模 | select | ✓ | <10万/10-50万/50-100万/>100万 |
| decision_maker | 决策人角色 | select | ✓ | CEO/CTO/CFO/部门负责人/采购负责人 |
| pain_point | 客户痛点 | textarea | ✓ | 如：效率低、成本高、数据孤岛 |
| competitor | 竞品情况 | textarea | | 客户正在考虑的竞品 |
| your_solution | 方案核心 | textarea | ✓ | 方案一句话概括 |

### 业务字段

| 字段 | 标签 | 必填 | 要点 |
|------|------|------|------|
| pain_point_detail | 客户痛点（详细） | ✓ | 痛点表现（带数据）+ 业务影响 |
| cost_of_inaction | 不解决的代价 | ✓ | 维持现状会损失什么（成本/效率/竞对差距），量化 |
| solution_detail | 方案详情 | ✓ | 模块化：每个模块解决什么 + 怎么解决 + 效果 |
| success_cases | 成功案例（2-3个） | ✓ | 同行业同规模优先，每案例3个关键数字 |
| implementation_plan | 实施与服务 | | 周期、节点、付款方式 |

---

## 3. quarterly_review（季度总结）

**适用**：KPI复盘 / 亮点提炼 / 不足分析 / 下季度规划

### 基础问题

| 字段 | 标签 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| quarter | 季度 | select | ✓ | Q1/Q2/Q3/Q4 |
| kpi_completion | KPI完成率 | text | ✓ | 如 92% |
| highlights | 本季度亮点（3个） | textarea | ✓ | 如：新签客户200家，同比增长35% |
| challenges | 本季度不足（3个） | textarea | ✓ | 如：华东区未达标 |
| next_quarter_goals | 下季度核心目标 | textarea | ✓ | 如：营收增长30% |
| support_needed | 需要支持 | textarea | | 如：增加2名销售 |

### 业务字段

| 字段 | 标签 | 必填 | 要点 |
|------|------|------|------|
| kpi_detail | KPI详细数据 | ✓ | 每指标：目标 → 实际 → 达成率 → 分析 |
| highlight_stories | 亮点故事（2-3个） | ✓ | 数据 + 原因 + 可复制经验 |
| challenge_analysis | 不足与根因分析 | ✓ | 数据 + 根因 + 已在做的改进 |
| cost_of_not_improving | 不改进的代价 | ✓ | 如果下季度不改进不足，会怎样（量化影响） |
| next_quarter_plan | 下季度目标与计划 | ✓ | 目标量化 + 动作可执行 + 资源有依据 |

---

## 4. project_report（项目汇报）

**适用**：项目进度 / 里程碑 / 风险管控 / 资源需求

### 基础问题

| 字段 | 标签 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| project_name | 项目名称 | text | ✓ | 如：官网重构项目 |
| stage | 项目阶段 | select | ✓ | 规划中/执行中/监控中/收尾 |
| progress | 当前进度 | text | ✓ | 如 总体70% |
| milestones_achieved | 已达成里程碑 | textarea | ✓ | 如：需求调研完成、UI设计定稿 |
| risks | 主要风险 | textarea | | 如：开发资源不足 |
| next_milestones | 下阶段里程碑 | textarea | ✓ | 如：开发完成、联调测试 |
| resource_needs | 资源需求 | textarea | | 如：2名前端开发 |

### 业务字段

| 字段 | 标签 | 必填 | 要点 |
|------|------|------|------|
| progress_detail | 详细进度与里程碑 | ✓ | 进度 + 里程碑 + 时间节点 |
| risk_and_blockers | 风险与阻塞 | ✓ | 每项风险：影响评估 + 应对措施 + 当前状态 |
| risk_impact | 风险不解决的后果 | ✓ | 不处理这些风险对目标/交付时间/预算的影响 |
| budget_status | 预算与资源 | | 花了多少、值不值、还需多少 |
| next_phase_detail | 下阶段详细计划 | ✓ | 任务 → 时间 → 交付物 → 依赖 |

---

## 5. training_share（培训分享）

**适用**：内部分享 / 外部培训 / 知识沉淀

### 基础问题

| 字段 | 标签 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| topic | 分享主题 | text | ✓ | 如：ChatGPT实战应用 |
| audience_level | 受众基础 | select | ✓ | 入门/进阶/高级/混合 |
| duration | 培训时长 | select | ✓ | 30/60/90/120分钟 |
| core_value | 核心价值（3点） | textarea | ✓ | 如：提升效率、降低成本 |
| target_outcome | 期望收获 | textarea | | 学完能做什么 |
| key_points | 核心知识点 | textarea | ✓ | 如：Prompt工程、Agent搭建 |

### 业务字段

| 字段 | 标签 | 必填 | 要点 |
|------|------|------|------|
| detailed_outline | 详细内容大纲 | ✓ | 时间分配 + 内容要点 |
| cost_of_not_learning | 不学的代价 | ✓ | 不掌握这些技能/知识，工作中会遇到什么障碍、效率损失多少 |
| practical_cases | 实战案例（2-3个） | ✓ | 场景 + 痛点 + 解决方案 + 效果 |
| interactive_design | 互动与练习设计 | | 让学员动手的环节 |
| takeaway_materials | 学员可带走什么 | | 具体可复用材料 |

---

## 6. custom（自定义）

**适用**：已有核心内容（文档/笔记/邮件/现有PPT文本），直接转PPT

无诊断问题，只有一个核心字段：

| 字段 | 标签 | 必填 | 说明 |
|------|------|------|------|
| ppt_content | 核心内容 | ✓ | 直接粘贴内容（要点、段落、已有PPT文本均可） |

使用 custom 模式时，Prompt 使用 `shared_requirements.custom` 而非 `standard`。
