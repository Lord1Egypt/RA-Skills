# 候选但未通过三重验证的方法论

> cangjie-skill 阶段 1.5 产出。这些单元通过了部分验证但未全部通过，保留供后续捞回。
> v3.3 D1 教程蒸馏新增候选记录（2026-07-24）。

## 候选池（16 个原始候选 → 11 个通过 → 5 个未通过）

### 未通过的 5 个候选

| # | 候选名 | V1 跨域 | V2 预测力 | V3 独特性 | 淘汰原因 |
|---|--------|---------|---------|---------|---------|

## v3.3 D1 教程蒸馏记录（2026-07-24）

### 蒸馏来源
- 教程：D1 数据分析与可视化课程（CRISP-DM 7 步 + Demo + 挑战任务）
- 文件：`<source-docs>/D1. 数据分析与可视化-内容框架.md` + `D1. 数据分析与可视化-课程内容文档.md` + `.pptx`
- 蒸馏方法：人工 + 三重验证（V1/V2/V3）

### 通过的 5 个候选（M17-M21）

| # | 候选名 | V1 跨域 | V2 预测力 | V3 独特性 | 挂载 |
|---|--------|---------|---------|---------|------|
| M17 | CRISP-DM 7 步 SOP | ≥6 处 | ✅ 能回答"每步该做什么" | ✅ 含决策点+交付物 | ✅ 挂载 |
| M18 | 清洗决策审查 | ≥3 处 | ✅ 能回答"清洗是否合理" | ✅ 4 列结构独特 | ✅ 挂载 |
| M19 | 图表三秒体检 | ≥4 处 | ✅ 能回答"图表是否准确" | ✅ 3 维度清单独特 | ✅ 挂载 |
| M20 | 相关≠因果验证 | ≥8 处 | ✅ 能回答"是否误说因果" | ✅ 6 项验证独特 | ✅ 挂载 |
| M21 | AI 背答案识别 | ≥4 处 | ✅ 能回答"AI 是否背答案" | ✅ 数据手术独特 | ✅ 挂载 |

### 未通过的 4 个候选（D1 教程）

| # | 候选名 | V1 跨域 | V2 预测力 | V3 独特性 | 淘汰原因 |
|---|--------|---------|---------|---------|---------|
| D1-C1 | 维度与指标概念 | ≥3 处 | ✅ | ❌ 统计学常识 | V3 独特性不足 |
| D1-C2 | Architect/Executor 分工 | ≥2 处 | ✅ | ❌ 已在 M2/M3 覆盖 | 重复方法论 |
| D1-C3 | 数据来源常识（Kaggle/政府） | ≥2 处 | ❌ | ❌ | 不构成方法论 |
| D1-C4 | Prompt 结构化（C1 五要素） | ≥3 处 | ✅ | ❌ 已在 M1 覆盖 | 重复方法论 |

### 挂载结果

- ✅ M17-M21 全部挂载（达到单次挂载上限 5 个）
- ❌ D1-C1~C4 未通过，留候选池供后续捞回
- 更新文件清单：
  - 新建 `references/methods/M17-crispdm-7step-sop.md`
  - 新建 `references/methods/M18-cleaning-decision-review.md`
  - 新建 `references/methods/M19-chart-3sec-checkup.md`
  - 新建 `references/methods/M20-correlation-causation-verification.md`
  - 新建 `references/methods/M21-ai-recitation-detection.md`
  - 更新 `assets/INDEX.md`（16 → 21 方法论）
  - 更新 `references/routing/scenario-router.md`（新增场景 8 + M17-M21 信号词）
  - 更新 `references/routing/method-composition.md`（新增场景 8 组合 + M17-M21 引用关系）
  - 更新 `assets/test-prompts.json`（新增 T26-T31 共 6 条测试用例）
| C1 | 把 AI 当实习生（聪明但需要交代清楚） | ✅ 心法 1 | ⚠️ 较常识 | ❌ 不够独特 | V3 失败——是常识性类比，非独特方法论 |
| C2 | 中文乱码提醒（指定 SimHei 字体） | ❌ 仅场景 7 一处 | ❌ 太局部 | ❌ 常识 | V1+V2+V3 全失败——只是个工具小坑，非方法论 |
| C3 | 7 个案例本身（老王/小林/小陈等） | ✅ 各场景 | ❌ 非方法论 | ❌ 只是故事 | V2 失败——案例是方法论的载体，不是方法论本身 |
| C4 | 多任务并行（关电脑去喝咖啡） | ❌ 仅场景 5 一处 | ❌ 非方法论 | ❌ 常识 | V1+V2+V3 全失败——是工具能力说明 |
| C5 | 把工作流沉淀为 Skill（自然语言沉淀） | ✅ 场景 5 | ⚠️ 元方法论 | ⚠️ 较通用 | V2+V3 边缘——是元方法论（如何做 Skill），不是数据分析方法论 |

## 捞回条件

如未来需要扩展 data-prompt-coach 的范围，以下候选可重新评估：

- **C1**：如要做"AI 协作理念"模块，可捞回作为开篇认知
- **C2**：如要做"故障排除手册"，可捞回作为常见问题
- **C3**：案例已融入各 M1-M11 的 A1 段，不需要单独捞回
- **C4**：如要做"工具能力说明"，可捞回
- **C5**：如要做"Skill 化进阶"，可捞回作为元方法论

## 审计轨迹

- **蒸馏日期**：2026-07-22
- **原始候选数**：16
- **通过数**：11（通过率 69%）
- **淘汰数**：5
- **通过率高于整本书的 25-50%**：因教程密度高，方法论单元较集中

## v3.4.0 TRAE 社区爬虫教程蒸馏记录（2026-07-31）

### 蒸馏来源
- 教程：TRAE 社区《编程实践：如何使用 AI 写爬虫获取数据》
- 文件：`<source-docs>/TRAE  编程实践：如何使用 AI 写爬虫获取数据.md`
- 蒸馏方法：人工 + 三重验证（V1/V2/V3）
- 蒸馏动机：用户主动推荐该教程，认为"非常适合融入当前技能，增加案例、增加用户引导提示词、增加网站分析脚本"

### 通过的 5 个候选（M22-M26）

| # | 候选名 | V1 跨域 | V2 预测力 | V3 独特性 | 挂载 |
|---|--------|---------|---------|---------|------|
| M22 | SPA 动态 API 识别 | ≥8 处（80% 现代网站） | ✅ 能回答"为何 requests.get 抓不到" | ✅ 6 步识别流程独特（含 Ctrl+U 判别） | ✅ 挂载 |
| M23 | 动态 API Key 模拟 | ≥3 处（Algolia/Solr 等） | ✅ 能回答"Key 为何失效" | ✅ Session 模拟链独特（Cookie+CSRF+Key） | ✅ 挂载 |
| M24 | 增量唯一 ID 设计 | ≥5 处（增量抓取/去重/缓存） | ✅ 能回答"如何区分已抓未抓" | ✅ 5 种 ID 策略+决策树独特 | ✅ 挂载 |
| M25 | HTML 元素定位法 | ≥4 处（AI 兜底场景） | ✅ 能回答"AI 识别失败怎么办" | ✅ DevTools 5 步定位流程独特 | ✅ 挂载 |
| M26 | 飞书多维表格双存储 | ≥6 处（本地+云端双写） | ✅ 能回答"如何同时存 CSV 和飞书" | ✅ 6 种字段类型映射规则独特 | ✅ 挂载 |

### 未通过的 3 个候选（TRAE 爬虫教程）

| # | 候选名 | V1 跨域 | V2 预测力 | V3 独特性 | 淘汰原因 |
|---|--------|---------|---------|---------|---------|
| TRAE-C1 | User-Agent 请求头设置 | ≥2 处 | ⚠️ | ❌ 已在 M2 防幻觉覆盖 | 重复方法论 |
| TRAE-C2 | requests.Session 自动 Cookie | ≥3 处 | ✅ | ❌ 融入 M23 实现 | 已被 M23 内部化 |
| TRAE-C3 | 异常重试机制 | ≥2 处 | ⚠️ | ❌ 通用工程常识 | V3 独特性不足 |

### 挂载结果

- ✅ M22-M26 全部挂载（达到单次挂载上限 5 个）
- ❌ TRAE-C1~C3 未通过，留候选池供后续捞回
- 更新文件清单：
  - 新建 `references/methods/M22-spa-dynamic-api-identification.md`
  - 新建 `references/methods/M23-dynamic-api-key-simulation.md`
  - 新建 `references/methods/M24-incremental-unique-id-design.md`
  - 新建 `references/methods/M25-html-element-location.md`
  - 新建 `references/methods/M26-feishu-base-dual-storage.md`
  - 新建 `references/asset-templates/website-analysis-script-template.md`
  - 新建 `references/asset-templates/feishu-base-storage-template.md`
  - 新建 `references/asset-templates/crawler-debug-experience.md`
  - 新建 `references/asset-templates/scenario-1-prompt-template.md`
  - 新建 `references/examples/airtable-community-demo.md`
  - 新建 `references/examples/monday-demo.md`
  - 更新 `assets/INDEX.md`（21 → 26 方法论）
  - 更新 `references/routing/scenario-router.md`（新增 M22-M26 信号词 + 场景 1 子场景决策树）
  - 更新 `references/routing/method-composition.md`（新增 7 种场景 1 v3.4.0 子组合）
  - 更新 `assets/test-prompts.json`（新增 T32-T41 共 10 条测试用例，41 条总计）
  - 更新 `SKILL.md`（升级 v3.4.0 + 新增规则 14 模型选择建议）

### 捞回条件

- **TRAE-C1**：如要做"请求头完整性清单"，可捞回作为 M23 的子模块
- **TRAE-C2**：已被 M23 内部化，无需单独捞回
- **TRAE-C3**：如要做"爬虫稳定性"专题，可捞回作为独立方法论

### 审计轨迹

- **蒸馏日期**：2026-07-31
- **原始候选数**：8
- **通过数**：5（通过率 62.5%）
- **淘汰数**：3
- **通过率符合 25-50% 行业基准**：教程偏实操，部分候选已被现有方法论覆盖
