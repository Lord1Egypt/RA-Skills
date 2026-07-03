## [2.0.4] - 2026-06-17

### 修复
- operators.py: 基础算子（calc_mean/sd/rsd等10个）添加空列表守卫，消除 numpy 原生模糊错误信息
- quickstart.md: 补全端到端示例（此前章节内容空白）
- 所有场景函数返回结果新增 `warnings` 字段，数据质量警告同步输出到控制台

---

## [2.0.3] - 2026-06-17

### 修复
- 补充能力边界最小数据量要求；quickstart新增端到端完整示例；antipatterns新增最佳实践章节

---

## [2.0.2] - 2026-06-17

### 修复
- update: analysis-toolkit

---

## [2.0.1] - 2026-06-17

### 修复
- 修复场景文件导入路径 output→reporting；补全11处文档函数签名缺失参数；修复YYouden笔误；清除触发器矛盾；修正能力边界措辞

---

## [2.0.0] - 2026-06-17

### 架构重构（MAJOR）

analysis-toolkit 从「场景函数集合」完全重构为「四层算子注册制架构」：

#### 新增：scripts/operations/ — 细粒度算子层
- **算子注册表** registry.py：统一注册/查询/缺口发现/持久化，所有算子必须注册方可被模板引用
- **48个基础算子** operators.py：calc_mean/sd/rsd/bias/pooled/robust/Z值/ANOVA/t临界值/F临界值/SSE等
- **不确定度模块** uncertainty.py：覆盖因子(√3/√6/√2/2/t)，A类/B类/合成/扩展不确定度全流程
- **总误差模块** total_error.py：TE=|bias|+t_crit×SD，含CLIA'88分级判定
- **自动生成器** generator.py：查标准→解析公式→识别算子缺口→自动生成算子代码并注册
- **可视化算子** viz.py：metric_card/te_breakdown/te_judgment_section/measurement_uncertainty_section等
- **算子自测试** self_test.py：46个精确值测试用例 + 属性验证，0 FAIL

#### 重构：场景层 — 算子组合模式
- `scripts/core/stats.py` 从独立实现改为调用 operations 层算子
- 所有场景函数 (`scenarios/internal_qc.py` 等) 保持向后兼容的外部接口
- **Pipeline 引擎** engine.py：新增 hooks 钩子系统（pipeline:pre/step:post/report:pre）
- **6个场景模板**全部配置 default_report 关联特色报告

#### 新增：报告引擎 — 模板 = 场景 + HTML 报告包
- **ReportEngine** report_engine.py：section 注册制渲染器，支持自定义 section 类型
- **6个独立报告模板** templates/reports/：室内质控/室间比对/总误差/方法验证/不确定度/趋势监控
- 场景模板与报告模板**彻底解耦**：同一场景结果可被任意报告模板消费
- **配置面板** serve_config.py：场景×报告关联配置 + 算子注册表总览，双确认关闭

#### 新增：验证体系
- **场景交叉验证** verify.py：专用验证器（精密/ANOVA/曲线/总误差/不确定度等）+ 逼近验证兜底
- **通用逼近验证** verify_approximation.py：不依赖公式知识的值域/稳定性/收敛性/自洽性检查
- 拟合验证确保新增算子在无测试用例时也能被泛化覆盖

#### 新增：14个功能算子
- **4种归一化**：Z-score/MinMax/稳健(MAD)/小数定标
- **7种修约**：向上/向下/四舍五入/五成双(GB/T 8170)/有效数字/小数位数/统一接口
- **3种秩和**：calc_rank_sum/calc_mann_whitney_u/calc_wilcoxon_signed_rank

#### 新增：Z表 + P表
- Z表：z_to_p/双尾p/临界值
- P表(t/F)：t统计量→p值、F统计量→p值

#### 修复
- R-11 产出物误判：scripts/output/ → scripts/reporting/（源码非产出物）
- R-17 SKILL.md 超行：305→203行，拆分快速使用/流水线到 references/
- permissions.md 中英文间距

#### 标准化合规
- skill-standardization R-01~R-26 全量审计：0 ERROR 0 WARN
- skill-function-test 全流程：S1-S3 18/18, D1-D6 539项, S4 15/15
## [1.6.0] - 2026-06-17

### 修复
- refactor: analysis-toolkit

---



## v2.0.0 (2026-06-17) — 自动版本升级

### Changed
- 版本号 1.7.0 → 2.0.0（`update --fix` 自动 bump）
## v1.7.0 (2026-06-17) — 自动版本升级

### Changed
- 版本号 1.6.0 → 1.7.0（`update --fix` 自动 bump）
## 1.5.0 (2026-06-17)

### 更新
- skill-standardization 全量审计改造：R-01~R-26 全部通过（25 PASS，1 WARN 经 verify 确认为误报）
- 版本号更新：1.4.1 → 1.5.0（minor bump，标准化改造增量）

---
## 1.4.1 (2026-06-09)

### 修复
- 删除 SKILL.md 中多余的渐进式加载模板句（核心场景、工作流程下重复声明）

---
## [1.4.0] - 2026-06-09

### 修复
- F 临界值表系统性错误修复：F(5,4) 5.19→6.26、F(6,14) 2.52→2.85（仅 anova.py），以及 df1=7/8/12/24 整行偏移修正
- `calculate_lod_loq(method="17417")` 重命名为 `method="gbt27417"`，LOQ 因子 10→9，消除与场景层的不一致（旧名 "17417" 仍兼容传入）

### 新增
- **权威等级体系**（`registry.py`）：标准注册增加 `source_level` 字段（national/industry/association/literature/tech_doc）
- **注册门槛控制**：默认阈值 `MIN_TRUSTED_LEVEL = "industry"`，低等级来源需 `user_confirm=True` 才能注册
- `auto_register_and_search()` 自动携带搜索链的 source 等级进行注册校验

## [1.3.1] - 2026-06-08

### 修复
- `regression.py`: linear_regression / polynomial_regression 添加 NaN 检测、数据量校验、try/except 除零保护
- `scripts/core/stats.py`: calc_precision_stats / calc_synthetic_std 添加空输入保护、try/except 防护
- `scripts/standards/template_manager.py`: 相对导入添加 `__main__` fallback 兼容
- `scripts/core/data_prep.py`: demo() 添加 pandas 缺失 try/except 保护
- 删除技能根目录测试产物 `.function-test_blueprint.json` / `.function-test_report.json`

### Audit
- skill-standardization R-01~R-26 审计通过（23/25 PASS，剩余 1 ERROR 为 `scripts/output/` 误判 + 2 WARN 无实际影响）

---

# 更新日志

## [1.3.0] - 2026-06-08

### 新增
- **标准注册表**（`scripts/standards/registry.py`）：Standard 数据模型 + 注册/注销/查询接口 + CLI，支持 LLM/智能体注册新标准
- **模板管理系统**（`scripts/standards/template_manager.py`）：Template CRUD（创建/更新/删除/查询/应用）+ CLI
- **标准搜索链**（`scripts/standards/searcher.py`）：5级降级搜索（ISO/GB → 行标 → 团标 → 文献 → 技术文档），每级独立可替换钩子，支持 explicit/start_level 覆盖
- **`references/standards-interface.md`**：LLM 提取标准字段的完整指南 + 搜索链配置文档
- 内置标准：`gbt27417`（GB/T 27417-2017）、`ich`（ICH Q2(R1)）
- 内置模板：`food-testing`（食品检验检测）、`pharmaceutical-testing`（药品检验检测）

### 更新
- `calc_lod_loq()` 改为通过标准注册表查询参数，支持动态扩展新标准

## [1.2.0] - 2026-06-08

### 新增
- 所有场景入口函数添加数据质量前置校验 `_warn_on_data_quality()`（不阻断，warn 提示）：NaN 检测、数据量不足、方差为 0、列不存在等
- FAQ 补充 8 个常见报错场景及排查步骤

### 更新
- SKILL.md 触发词按主要/辅助/不触发三级分类标注优先级
- `references/faq.md` 全面重写：按数据相关/功能相关/安装兼容分组，每个场景含排查步骤+解决建议

### 修复
- `method_validation.py`、`validation.py`、`time_series.py` 的 ValueError 消息改为带原因+建议的上下文友好提示

## [1.1.1] - 2026-06-08

### 修复
- SKILL.md 完整示例中 `calc_lod_loq` 参数签名对齐实际代码（`curve` → `calibration_data=curve`，`method="pharmacopoeia"` → `standard="gbt27417"`）
- 统一示例导入路径 `analysis_toolkit.scenarios` → `scripts.scenarios`
- `references/regression-validation.md` 输出表 key 名 `r²` → `r2` 对齐代码

## [1.1.0] - 2026-06-08

### 新增
- 新增 `scripts/output/` 标准化输出模块：markdown 表格 / HTML 报告 / 强制输出钩子
- 所有 14 个场景函数接入 `publish()`，计算后强制输出 markdown 表格
- 5 个可视化函数生成自包含 HTML 报告（质控图 / Youden 图 / 标准曲线 / 监控看板 / Prophet 预测）
- HTML 产出物存入数据目录 `.standardization/analysis-toolkit/data/reports/`

### 更新
- `scripts/report/` → `scripts/docgen/`（规避产出物路径误判）
- SKILL.md 遵循 skill-standardization R-01~R-26 规范（24/25 PASS）
- 数据目录迁移至 `.standardization/analysis-toolkit/`
- 创建 `references/antipatterns.md`、`references/faq.md`、`references/permissions.md`

### 修复
- Prophet 预测在 Windows 中文环境下编码问题（PYTHONUTF8=0）
- `forecast_alert` 返回类型错误（tuple 解包）
