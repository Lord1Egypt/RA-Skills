---
name: activity-duration-estimation
tags: ['duration-estimation', 'pert', 'monte-carlo', 'project-management', 'semantic-analysis', 'wbs', 'work-breakdown', 'project-docs', 'html-report', 'settings', 'knowledge-base', 'economic-analysis', 'evm', 'earned-value']
version: 1.11.7
author: wUwproject
license: MIT
description: 活动历时估算 + WBS工作分解 + 项目文档生成 + 经济效益分析 + 挣值管理（Activity Duration Estimation & WBS & Project Docs & Economic Analysis & EVM）—— 支持三点估算/蒙特卡洛四种方法 + WBS项目规划与分解 + 项目文档双模式生成（手动空模版/逐节自动）+ ROI/NPV/IRR/BCR 经济效益分析 + PV/EV/AC/SPI/CPI 挣值管理。三库隔离架构：shared.db + economic.db + evm.db。输出自包含HTML评估报告、经济效益分析报告和挣值分析报告。
sensitive_access: false
critical_write: false
permission_weight: LOW
data_dir: ../.standardization/activity-duration-estimation/
external_data_dir: true
trigger: 活动历时估算/三点估算/PERT/蒙特卡洛模拟/工期估算/任务历时/概率估算/β分布/正态分布/历时分析/WBS/WBS分解/项目规划/工作分解/项目分解/分解任务/立项申请书/结项报告/相关方登记册/风险登记册/项目文档/项目模板/经济效益分析/投资回报/ROI/NPV/IRR/BCR/投资回收期/可行性分析/项目经济效益/折现分析/多折现率对比/挣值管理/EVM/PV/EV/AC/SPI/CPI/成本绩效/进度偏差/挣得值/EAC/挣值分析
trigger_negative: 只是询问概念不执行估算/纯数学公式讨论不含实际任务
faq_quality: improve_qa
meta_field_sync: true
create_permissions_md: true
---
# activity-duration-estimation — 全周期项目管理

> **WBS项目规划 → 活动历时估算 → 项目文档生成**，三环节完整闭环。
> 全流程由 `scripts/runner.py` 的 `run_full()` 自动编排，
> LLM 只需调用一个函数即可完成项目从分解到文档的全部工作。
> 详细内容拆分到 `references/*.md` 按需加载。

---

## 触发场景

**正向触发**：估算工期/三点估算/PERT/蒙特卡洛/β分布/OMP/紧前关系/FS-SS-FF-SF/CPM甘特图/重叠分析/P50-P90/生成评估报告：估算工期/三点估算/PERT/蒙特卡洛/β分布/OMP/紧前关系/FS-SS-FF-SF/CPM甘特图/重叠分析/P50-P90/生成评估报告

**不触发**：仅概念询问 / 纯数学讨论 / 明确使用其他技能
---

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

| # | 能力 | 说明 |
|---|------|------|
| 0 | **WBS工作分解** (子技能) | 基于3个参考模板+LLM自适应填充，支持4种分解方法，100%规则验证，自动衔接估算 |
| 1 | **项目文档生成** (子技能) | 双模式：手动模式输出特化空模版（token≈0）/ 自动模式逐节生成，4个预置模板（立项/结项/相关方/风险） |
| 2 | **四种估算方法** | 直接估算法 / β分布（PERT）估算法 / 正态分布估算法 / 蒙特卡洛模拟法 |
| 3 | **语义分析推荐** | 根据任务类型（建筑/制造/软件/科研/农业等）自动推荐最适估算方法组合 |
| 4 | **外部知识搜索** | 两阶段搜索流程：大模型自判→搜索补充→汇总推荐 |
| 5 | **知识库查询/写入** (新增) | 按需信息通道，与联网搜索平行。标准字段硬编码，LLM做格式翻译入库。支持历史项目查询、OMP基准检索、外部数据库/文件（SQLite/CSV/MD/DOCX/JSON）按标准导入 |
| 6 | **CPM关键路径分析** | 基于紧前关系的关键路径计算，含ES/EF/LS/LF/总时差，自动识别关键任务 |
| 7 | **多分布蒙特卡洛** | 支持PERT-Beta、三角分布、泊松近似三种分布并行模拟，提供多维度概率评估 |
| 8 | **任务重叠分析** | 自动检测任务时间重叠，输出最大重叠数和最长重叠时段 |
| 9 | **甘特图可视化** | 基于CPM结果的甘特图（SVG），关键路径高亮标注 |
| 10 | **紧前关系规划** | 手动指定/自动规划两种模式，支持FS/SS/FF/SF四种依赖关系 |
| 11 | **HTML评估报告** | 自包含HTML，含甘特图/概率分布/重叠分析图表，有图有表有数据有分析 |
| 12 | **项目文档生成** | 双模式：手动空模版/混合逐节生成；4个P0模板（立项/结项/相关方/风险） |
| 13 | **全局配置系统** | 5项可调整配置（联网搜索/知识库采集/知识库调用/文档指定/文档撰写），每项可选 auto/manual。`scripts/settings_server.py` 提供 HTML 可视化配置面板。配置通过 `state.settings` 注入流程，LLM 可读取 `_get_setting()` 决定行为。 |
| 14 | **经济效益分析** (分支子技能) | 独立于全流程，单独触发。ROI/NPV/IRR/BCR/PBP 计算引擎 + HTML 报告 + 独立 economic.db 知识库。可插入立项申请书模板。 |
| 15 | **挣值管理** (分支子技能) | 独立于全流程，单独触发。PV/EV/AC/SPI/CPI/EAC 计算引擎 + HTML 报告 + 独立 evm.db 知识库。可插入结项报告书模板。 |

---

### 渐进式文件索引

| 文件名 | 分类 | 包含内容 | 审计关联 |
|--------|------|----------|----------|
| `references/antipatterns.md` | 规范指南 | skill 编写中的常见反模式。包含：错误做法示例、正确做法示例、避坑指引。 | R-18 |
| `references/changelog.md` | 版本管理 | 版本更新日志。包含：版本号、更新类型、修复项、升级说明。 | R-24 |
| `references/economic-analysis-methodology.md` | 参考文档 | > **子技能定位**：独立于活动历时估算的核心全流程，单独触发、单独运行。 | 无 |
| `references/evm-methodology.md` | 参考文档 | > **子技能定位**：独立于活动历时估算的核心全流程，单独触发、单独运行。 | 无 |
| `references/faq.md` | 常见问题 | 常见疑问与解答。包含：问题分类、原因分析、解决方案。 | R-19, R-25 C-19 |
| `references/knowledge-interface.md` | 参考文档 | > 知识库是与「联网搜索」平行的信息获取/存储通道。 | 无 |
| `references/methods.md` | 参考文档 | > 本文件详细说明四种活动历时估算方法的公式、计算步骤和适用场景。 | 无 |
| `references/permissions.md` | 权限与测试 | 权限扫描说明与测试结论。包含：风险等级、高权限操作说明、测试概览、计时统计。 | R-15, R-16 |
| `references/project-docs-methodology.md` | 参考文档 | > 本文件说明:project-docs 子技能的双模式设计、模板结构、操作流程和使用规范。 | 无 |
| `references/report-template.md` | 参考文档 | > 本文件定义 REPORT_DATA 数据结构的完整接口，以及分析结果→格式化→填充→生成的标准化流程。 | 无 |
| `references/risk-dimensions.md` | 参考文档 | > 内置7大类风险维度，根据项目特征自动匹配适用维度。 | 无 |
| `references/search-integration.md` | 参考文档 | > 本文件说明外部知识搜索的两个阶段流程。 | 无 |
| `references/semantic-analysis.md` | 参考文档 | > 本文件说明语义分析引擎如何工作：任务参数提取、任务类型分类、推荐方法映射。 | 无 |
| `references/thinking-tools.md` | 参考文档 | > 本文件收录项目管理/文档撰写中常用的思维工具和方法论框架。 | 无 |
| `references/wbs-methodology.md` | 参考文档 | > 本文件定义 WBS（Work Breakdown Structure）在活动历时估算技能中的完整实现：分解方法、参考模板、递归算法、验证规则以及与估算流程的 | 无 |
## 工作流程

工作流程由 `scripts/runner.py` 自动编排，LLM 无需关心内部阶段顺序。

```python
# 推荐：一键全流程（WBS → 估算 → 报告 → 文档，全环节必做）
from scripts.runner import run_full, PipelineState
result = run_full("帮我规划并估算一个电商后台管理系统")

if result["status"] == "ok":
    state = result["state"]
    print(state.wbs_text_tree)      # ① WBS文本树
    print(state.estimate_summary)   # ② 估算摘要
    print(state.html_report_path)   # ③ HTML报告路径
    print(state.doc_content)        # ④ 项目文档
elif result["status"] == "blocked":
    # 需要LLM提供WBS数据（即使已有OMP参数，WBS也是必做的）
    wbs_data = {"name": "电商后台", "children": [...]}  # LLM提供
    state = PipelineState("帮我规划并估算一个电商后台管理系统")
    state.run_wbs(custom_data=wbs_data)
    result = state.run_full()  # 继续执行估算→报告→文档
else:
    print(result["message"])        # 错误信息
```

**全流程阶段（代码硬编码，不可跳过，与 runner.py 中 6 个阶段一一对应）：**

1. WBS分解 → `run_wbs()`（全流程模式下必做，LLM提供结构化数据）
2. WBS进入估算门控 → `_wbs_passes_estimation_gate()` 硬校验
3. 紧前关系规划 → `_prompt_llm_for_dependencies()` / 自动FS串联
4. 估算计算 → `run_estimate()`（全Python自动：CPM + MC + 重叠分析）
5. HTML评估报告 → `_generate_html_report()`（全Python自动）
6. 项目文档 → `generate_docs()`（按模板生成立项/结项/风险/相关方文档）

**单独调用模式**（不经过`run_full()`全流程，按需使用）：

| 需求 | 调用方式 |
|------|---------|
| 仅有估算需求 | `run_pipeline(mode="estimate")` 或 `state.run_estimate()` |
| 仅需文档 | `run_pipeline(mode="docs")` 或 `state.generate_docs()` |
| 仅WBS分解 | `run_pipeline(mode="wbs")` 或 `state.run_wbs()` |

### LLM交互点

当流程需要LLM推理时，`runner.py` 会抛出 `LLMInteractionRequired` 异常：

| 交互点 | 触发条件 | LLM需提供 |
|--------|---------|-----------|
| `_prompt_llm_for_wbs()` | 模糊需求 | WBS结构化数据 `{name, children: [...]}` |
| `_prompt_llm_for_omp()` | 阶段缺OMP | OMP值 `{o, m, p}` |
| `_prompt_llm_for_dependencies()` | >5个阶段 | 紧前关系或确认自动规划 |

LLM看到异常后按提示提供数据，然后继续执行即可。

---

## 快速开始

```text
场景1：直接估算 — "乐观3天、最可能6天、悲观15天" → β分布7天, σ=2天 → 68%概率5~9天
场景2：多阶段CPM — "前端(5/10/20)→后端(8/15/25)→测试(10/20/35), FS" → 总工期47天 →出HTML报告
场景3：搜索辅助 — "装配式建筑施工" → 搜索同类→给出典型OMP→确认→估算
场景4：WBS→估算 — "帮我规划并估算电商后台" → 分解→确认→HTML报告
场景5：项目文档 — "生成立项申请书, 手动模式" → 空模板→"自动填充背景"→逐节生成→拼合
场景6：经济效益分析 — "初始100万, 年收益12万, 年支出5万, 5年, 终值200万, 折现率10%" → NPV=50.72, IRR=20.35%
场景7：挣值管理 — "项目到D阶段, 做挣值分析" → EV=320.27, SPI=1.01, CPI=1.07, EAC=379.73
```

## 常用操作速查

| 我想... | 一句话答案 |
|---------|-----------|
| 快速估算一个项目工期 | 调用 `from scripts.runner import run_full; result = run_full("项目描述")` — AI 自动拆解+估算+出报告 |
| 只用 WBS 不做估算 | `state.run_wbs()` — 只做工作分解，不进估算流程 |
| 指定每个任务的 OMP | 在 WBS 数据结构中填写 `{"o": 3, "m": 5, "p": 8}` 字段 |
| 用我自己的文档模板 | `load_template() → customize_sections() → save_template()` — 增删改排章节后另存 |
| 更新全局配置 | `python scripts/settings_manager.py set <key> <value>` — 纯 CLI，无需 LLM 参与 |
| HTML 报告打不开 | 报告是自包含 HTML，直接用浏览器打开 state.html_report_path |
| 调整蒙特卡洛模拟次数 | `run_full(mc_iterations=5000)` — 默认 2000，数值越高越精确但越慢 |
| 从历史项目参考数据 | 告诉 LLM「查一下同类项目的基准数据」— 会自动搜索 SQLite 知识库 |

---

## WBS子技能 — Phase -1：项目规划与工作分解
>  | `scripts/wbs_engine.py`
> 全流程模式下必做，由 `run_full()` 自动触发。

---
## 项目文档生成子技能 — :project-docs

>  | `scripts/project_docs_engine.py`
三种模式：`manual`（空模板，token≈0）/ `mixed`（按章节设 auto/outline/manual，推荐）/ `全自动`（所有节 auto）。
支持模板定制：增/删/改/重排章节、每节独立模式、另存为新模板。

```python
from project_docs_engine import set_section_mode
tpl = load_template("立项申请书")
tpl = set_section_mode(tpl, "项目背景", "auto")    # 自动生成
tpl = set_section_mode(tpl, "预算", "manual")       # 留空手动填
state.generate_docs(mode="mixed", filled_sections={"project_background": "..."})
save_template(tpl, "我的模板", overwrite=True)       # 另存自定义模板
```

**内置模板**：`立项申请书`(11节) / `结项报告书`(10节) / `相关方登记册`(4节) / `风险登记册`(5节)
---

## 子模块详解

各子模块详细说明见 `references/`：
- **Phase 0**: 语义分析与方法推荐 → `references/semantic-analysis.md`
- **Phase 1**: 外部知识搜索 → `references/search-integration.md`
- **Phase 2-3**: 紧前关系规划 + 估算计算（CPM/MC/重叠分析）→ `references/methods.md`
- **Phase 4**: HTML评估报告 → `references/report-template.md`
- **WBS方法论**: → `references/wbs-methodology.md`
- **项目文档**: → `references/project-docs-methodology.md`

| 估算方法 | 公式 | 适用场景 |
|---------|------|---------|
| 三点直接 | (O+M+P)/3 | 快速估算 |
| β分布(PERT) | (O+4M+P)/6, σ=(P-O)/6 | 标准项目管理 |
| 蒙特卡洛 | 2000+次模拟, 多分布并行 | 高不确定性项目 |

---

## 限制与边界

| 维度 | 说明 |
|------|------|
| 任务数量 | 建议 ≤50 个阶段/任务，超过时蒙特卡洛模拟耗时显著增加 |
| OMP值 | 必须满足 O ≤ M ≤ P（乐观≤最可能≤悲观），不满足时会提示修正 |
| 紧前关系 | 不能形成循环依赖（A→B→C→A），系统会检测并报错 |
| 工期单位 | 统一使用同一单位（天/小时/周），混用需先归一化 |
| 网络依赖 | 首次使用需联网搜索（非典型任务），后续使用完全离线 |
| 报告生成 | 输出自包含HTML文件，需要浏览器打开查看，不支持PDF直接导出 |

---

## 版本

当前版本 **v1.11.0** — 
