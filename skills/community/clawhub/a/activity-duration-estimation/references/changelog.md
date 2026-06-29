## 1.11.7 (2026-06-14)

### 更新
- skill-standardization 全流程改造：blueprint → 备份 → audit → fix → verify → bump → cleanup
- R-20 术语统一：更新类型 → 更新类型
- 无功能性更新

---

## 1.11.1 (2026-06-14)

### 修复
- skill-standardization R-25 文档格式调整

---

## 1.11.0 (2026-06-04)

### 新增
- **经济效益分析子技能**（独立分支，不加入全流程）
  - `scripts/economic_analysis_engine.py` — ROI/NPV/IRR/BCR/PBP 完整计算引擎（验证通过小作坊例子）
  - `scripts/economic_knowledge.py` — economic.db 独立知识库（三库隔离架构）
  - `references/economic-analysis-methodology.md` — 方法论文档
  - `scripts/templates/economic-report.html` — 自包含 HTML 报告（Chart.js 图表）
  - 立项申请书模板新增「经济效益分析」可选章节
- **挣值管理子技能**（独立分支，不加入全流程）
  - `scripts/evm_engine.py` — PV/EV/AC/SPI/CPI/EAC 完整计算引擎（验证通过 D 阶段例子）
  - `scripts/evm_knowledge.py` — evm.db 独立知识库（三库隔离架构）
  - `references/evm-methodology.md` — 方法论文档
  - `scripts/templates/evm-report.html` — 自包含 HTML 报告（SPI/CPI 趋势图）
  - 结项报告书模板新增「挣值分析」可选章节
- **三库隔离基础设施**
  - `scripts/knowledge_schema.py` — 增加 ECONOMIC_FIELDS/EVM_FIELDS/REGISTRY_FIELDS 字段定义
  - `skill_registry` 跨库注册表：shared.db → economic.db/evm.db 标准路由
  - 独立索引查询（npv/irr/spi/cpi 走索引，不走 FTS/LIKE）
- `scripts/full_test.py` — 全功能模拟测试套件（100/100 PASS）

### 修复
- `scripts/evm_knowledge.py` — 补充缺失的 `from typing import Optional`
- `scripts/economic_analysis_engine.py` — calc_roi 系列增加零除保护

---

## 1.10.0 (2026-06-04)

### 改进
- SKILL.md 新增「常用操作速查」表格（开箱即用度 4.4→预估 4.6）
  - 8 条常见需求的一步到位答案：估算 / WBS / OMP / 模板定制 / 全局配置 / 报告查看 / MC次数 / 历史基准
  - 放在「快速开始」场景之后，不干扰渐进式披露结构
- `runner.py` `_handle_error()` 错误消息人性化改进（异常处理 4.0→预估 4.3+）
  - 根据阶段（wbs/estimate/docs/wbs执行）自动追加"💡 解决指引"
  - WBS 门控校验返回结果新增 `hint` 字段，说明如何修正

---

## 1.9.0 (2026-06-04)

### 新增
- **全局配置系统** `scripts/settings_manager.py` — 5项可调运行时配置
  - `web_search_mode`: 联网搜索（auto / manual）
  - `kb_collect_mode`: 知识库采集（auto / manual）
  - `kb_query_mode`: 知识库调用（auto / manual）
  - `doc_template`: 文档指定（null / 模板名）
  - `doc_write_mode`: 文档撰写（auto / manual / template）
- 配置持久化到 `skills/.standardization/activity-duration-estimation/data/settings.json`
- **纯文本 CLI 交互**：`python scripts/settings_manager.py` 直接管理，无需 LLM 参与
  - `show` — 查看当前配置
  - `list` — 列出所有可设项及说明
  - `set <key> <value>` — 更新单条配置
  - `reset` — 恢复默认
  - `validate` — 校验合法性
  - `import <file>` — 从 JSON 文件批量导入
  - `export [file]` — 导出为 JSON 文件
  - `server [port]` — 启动 HTML 可视化面板
  - `help` — 完整帮助
- `scripts/settings_server.py` — HTTP配置可视化服务，启动后浏览器打开即可可视化更新
- `scripts/templates/settings.html` — 自包含HTML配置面板，含约束联动（doc_template为空时禁用doc_write_mode的template选项）
- `validate()` 校验器：枚举值检查、约束联动检查（doc_template为空时doc_write_mode不能为template）
- 默认值：全部 manual，仅 doc_write_mode 默认 auto

### 改进
- `runner.py` PipelineState 初始化时自动加载配置到 `state.settings`
- `run_full()` 从配置读取 doc_template 和 doc_write_mode（显式传参时优先）
- `_resolve_doc_mode()` 配置→模式翻译逻辑（template→mixed，无模板时降级）
- SKILL.md 核心能力#13 全局配置系统 + 文件索引新增3项

---


## v1.9.1 (2026-06-04) — 自动版本升级

### Changed
- 版本号 1.9.0 → 1.9.1（`update --fix` 自动 bump）
## 1.8.5 (2026-06-04)

### 新增
- `references/knowledge-interface.md` — 知识库接口设计文档
  - 按需信息通道定义（与联网搜索平行，遵循 search-integration.md 按需模式）
  - 标准字段定义（来自 knowledge_schema.py 硬编码规范）
  - LLM格式解析指引：SQLite/CSV/MD/JSON/DOCX/XLSX/纯文本七种格式
  - 字段映射规则：标准字段固定，LLM负责从外部列名→标准字段的翻译
  - 写入/读取/外部对接三组接口函数定义

### 改进
- SKILL.md 核心能力表新增「知识库查询/写入」能力（#5），重新编号至12项
- SKILL.md 渐进式文件索引新增 knowledge-interface.md / knowledge_schema.py / project_knowledge.py 三项引用

---

## 1.8.1 (2026-06-03)

### 修复
- audit --fix 自动修正: artifact_paths, external_data_dir, writing_standards

---

## 1.8.0 (2026-06-03)

### 重构
- **依赖规划从「代码硬猜/丢异常给用户」改为「LLM自行设计+Python执行」**
  - `scripts/risk_dimensions.py` 重写：维度库只做选择+结构指引，不做硬编码内容。LLM 按实际项目数据生成分析
- `PipelineState.get_risk_context()` 新增 — 返回结构化项目数据，供LLM生成风险分析
- `_generate_html_report()` 新增 WARN：LLM未设 `risk_analysis` 时打印用法提示
- `_build_analysis_section()` fallback 改为红色警告 + 可用数据展示，不再无声无息
  - 删除 `LLMInteractionRequired` 依赖交互（LLM 自己该干的事不要丢给用户）
  - `run_full()` 中若 LLM 已设 `self.dependencies` 则直接跳过
  - `prepare_estimation()` 注释明确：LLM 直接赋值 `state.dependencies`
- 组内子任务从「全部并行」改为「FS串联」（安全默认）
- `infer_dep_type()` 简化：默认返回 FS

### 新增
- `scripts/knowledge_schema.py` — **知识库标准化接口**
  - **标准格式**: 知识条目 = YAML frontmatter + Markdown（与 Obsidian/Hugo/Jekyll/Notion 同一格式）
  - **项目数据**: JSON 自描述格式 (`format: wbs-v1`)
  - `entry_to_markdown()` — 知识条目 → 标准化 YAML+MD
  - `parse_markdown_entry()` — 标准格式 → 知识条目（兼容 Obsidian/Hugo 风格 frontmatter）
  - `project_to_json()` — PipelineState → 标准 JSON
  - `parse_project_json()` — 标准 JSON → (phases, deps) 元组
  - **外部对接**: `detect_table_mapping()` 自动检测字段映射
  - **预置映射**: Obsidian / Notion 导出 / Hugo / Jira 导出
  - `generate_mapping_guide()` — 给 LLM 的字段映射指南
  - `validate_entry()` / `validate_project_json()` — 格式校验
- `scripts/project_knowledge.py` — 通用知识库引擎（SQLite + FTS5）
  - 搜索中文退化 LIKE 兜底
- 甘特图 SVG → HTML div-based：阶段性色块，关键路径红框，持续天数标签
- 参数表从平铺改为按 Phase 分组展现
- `_build_analysis_section()` 重写为维度驱动

### 新增
- `scripts/analysis_engine.py`: `infer_dep_type()` — 默认返回 FS。串行/并行取决于资源、能力、工期等现实约束，无法从名称可靠推断
- `references/risk-dimensions.md` — 7 类风险维度库（D1~D7）
- `scripts/risk_dimensions.py` — 按上下文自动匹配维度
- 任务重叠分析卡片 + 里程碑标记 + WBS 树卡片
- `validate_wbs()` 粒度检查：核心阶段≥5 WP，每阶段≥3，交付物完整性

### 修复
- `_build_wbs_tree_section()` 字符串拼接缺括号→WBS树内容被Python丢弃成空卡片
- `_build_analysis_section()` 新增 `self.risk_analysis`：LLM可设自定义风险分析，模板仅作fallback
- 根因：`wbs_to_dependencies()` 双分支同代码（全 FS），父节点检查形同虚设
- 根因：HTML 报告 SVG 被 `except: pass` 吞异常，甘特图/MC 从未渲染
- 根因：组内并行导致甘特图全部任务相同起点、不符合实际
- 根因：组内并行 + 仅首组员依赖导致工期被低估（34天）
- `_build_mc_section()` SVG 失败时连文字也看不到
- 甘特图单位硬编码 "h" → 可配置默认"天"
- `format_text_tree()` emoji → ASCII 标记，防 GBK 崩溃

---

---
### 新增
- `_generate_audit_report()`: 10项审计检查（CPM/MC/总工期/关键路径/P50P90/HTML报告/文档逐节检查）
- `_audit_and_fix()`: 三阶审计+自动修复（审→修→再审，3轮截断）
- 三类失格修复：计算失真→recalculate、内容失调→regenerate、规划失格→replan
- LLM误报筛查：审计报告含文件行号/数据上下文/附近代码段

### 修复
- `_generate_html_report()` 输出路径从 `skills/<name>/reports/` 改为 `.standardization/<name>/data/reports/`
- `save_document()` 输出路径从 `os.getcwd()` 改为 `.standardization/<name>/data/docs/`
- `sys.path.insert(0, SCRIPTS_DIR)` 确保跨目录 import 正确
- 修复 `_audit_and_fix()` 调 `run_estimate()` 导致递归死循环
- `project_docs_engine.py` 和 `runner.py` 添加 R-12 审计锚点 `DEFAULT_DATA_DIR_RAW`

---

## 1.6.2 (2026-06-03)

### 修复
- `save_document()` 使用 `os.getcwd()` 导致文档产物写到技能安装目录
  改为输出到 `.standardization/activity-duration-estimation/data/docs/` 数据目录

---

## 1.6.1 (2026-06-03)

### 修复
- `prepare_estimation()` 不识别已直接配置的 `self.phases`，缺少 `elif self.phases: pass` 分支
- 功能测试 83/83 全部通过

---

## 1.6.0 (2026-06-03)

### 新增
- `scripts/runner.py`: 新增 `LLMInteractionRequired` 异常类，流程需要LLM推理时抛出（WBS/依赖/OMP三个交互点）
- `PipelineState.run_full()`: 强制全流程入口（WBS→估算→HTML报告→文档），WBS全程模式下必做
- `_needs_wbs()`: 分支逻辑（含OMP时自动跳过WBS交互，仅用于单模式入口）
- `_wbs_passes_estimation_gate()`: WBS进入估算门控校验（缺OMP/违反O≤M≤P→阻塞）
- `_prompt_llm_for_*()`: 三个LLM交互点封装（wbs/omp/dependencies）
- `_generate_html_report()`: 自包含HTML评估报告自动生成（甘特图/CPM/MC/分析建议）
- Phase 5: 项目文档生成纳入全流程（WBS→估算→报告→文档完整闭环）

### 重构
- H1 标题改为 `activity-duration-estimation — 全周期项目管理`，体现全周期定位
- SKILL.md 从303行精简至193行（≤230行限制），Phase 0-4详细内容移至 references/
- `runner.py` 完全重写，流程控制从 Markdown 转移到 Python 代码

### 修复
- 修复 `_meta.json` 非标字段 `sub_skills`
- 修复 SKILL.md 非标 frontmatter 字段 `antipattern_count`, `faq_quality`
- 0 ERROR 2 WARN（WARN: R-19 FAQ质量 + R-23 文档代码一致性）

---

## 1.5.3 (2026-06-02)

### 修复
- 全量 skill-standardization 审计改造：0 ERROR, 3 WARN
- --fix 自动修正: meta_json, writing_standards（R-01 非标字段清理, R-10 版本同步）
- R-19: FAQ低质量条目重写（OMP来源从简短描述扩展为4种方法对比+组合建议）
- R-25 C-13: thinking-tools.md 加入渐进式索引表
- 版本三端一致 1.5.3

---

## 1.5.2 (2026-06-02)
### 新增
- `scripts/runner.py` — Python全流程编排层：PipelineState + run_pipeline() 三阶段一键执行
- LLM只需调用 `run_pipeline()` 即可自动串联 WBS→估算→文档，阶段顺序/验证/数据流转由代码硬编码保障
- 支持 mode="full" / "wbs" / "estimate" / "docs" 灵活选择执行范围
- PipelineState 状态管理：wbs_text_tree / estimate_summary / doc_content 等字段直接读取
- `references/thinking-tools.md` — 12个思维工具方法论
- **思维工具嵌入手动模式**：`output_manual()` 和 `assemble_mixed_document()` 自动在各章节末尾注入对应思维工具的框架说明+完整示例，用户/其他LLM拿到模板即可参考使用
- TOOL_REFERENCES 覆盖9个文档章节的8种工具映射（含SWOT/5W2H/SMART/MoSCoW/Pareto/PDCA/RACI/CPM等）
- 项目文档方法论文档新增"六、思维工具参考"章节，含章节-工具映射速查表

### 修复
- 标准化审计修复：H1位置 / tags同步 / 行数超限 / 文档-代码一致性
- 0-based → 1-based 依赖索引转换（wbs_to_dependencies 返回0-based，calc_cpm 需要1-based）

---

## 1.5.1 (2026-06-02)

### 修复
- audit --fix 自动修正: meta_json, version, writing_standards, progressive_loading_explicit

---

## 1.5.2 (2026-06-02)

### 新增功能
- 章节模式系统：每节独立配置 auto/manual/outline 模式，固化在模板中
- set_section_mode() + list_sections_by_mode() + get_template_mode_summary()
- assemble_mixed_document() 按模式混合组装文档
- outline 模式：LLM生成概要思路（短内容），用户在基础上扩展
- customize_sections 新增 set_mode 操作
- 模板可定义各章节模式 → save_template → 下次直接调用

---

## 1.5.1 (2026-06-02)

### 新增功能
- 模板定制系统：增/删/改/重排章节 + 另存为新模板（customize_sections / save_template）
- 新增：add_section / remove_section / reorder_sections / rename_section / delete_template 全套API
- 新增：get_template_structure_summary 章节预览
- 支持用户自定义章节类型（rich_text / fields / table / wbs_attachment 全支持）

### 文档
- project-docs-methodology.md 新增"四、模板定制"章节，含全部操作说明和调用示例
- antipatterns.md 新增 AP-D04（每次用同一套模板不改）
- SKILL.md 新增"模板定制"一行

---

## 1.5.0 (2026-06-02)

### 新增功能
- 项目文档子技能 `activity-duration-estimation:project-docs`：双模式文档生成（手动空模版/逐节自动）
- 4个P0模板：立项申请书(11节)、结项报告书(10节)、相关方登记册(4节)、风险登记册(5节)
- 手动模式：根据WBS/估算/CPM输出项目特化空模版，含章节结构+填充提示+已有资料引用，token≈0
- 自动模式：逐节独立LLM生成+逐节用户确认，不满意只重算该节
- 双模式互不冲突，可混用（手动出结构+自动填特定节）
- skill-sub 编排支持：project-docs 可消费 WBS 和估算的产出物

### 新增文件
- `references/templates/` — 4个JSON模板文件目录
- `references/project-docs-methodology.md` — 项目文档生成方法论
- `scripts/project_docs_engine.py` — 项目文档引擎（load/customize/manual/auto/assemble）

### 文档
- SKILL.md 新增:project-docs子技能入口、场景5示例
- _meta.json 新增 sub_skills.project-docs 注册
- antipatterns.md 新增 AP-D01~AP-D03 项目文档反模式
- faq.md 新增5个项目文档Q&A

---

## 1.4.0 (2026-06-02)

### 新增功能
- WBS子技能 `activity-duration-estimation:wbs`：基于3个参考模板+LLM自适应填充的项目规划与工作分解
- 四种输出格式：缩进文本树 / Markdown树 / JSON字典 / SVG树形图（用户可选）
- 100%规则启发式验证：结构性+语义性检查，标记问题不自动更新
- WBS→估算自动衔接：工作包自动映射为阶段参数+OMP+紧前关系
- 全流程支持：模糊需求→WBS→确认→估算→HTML报告 一键走通

### 新增文件
- `references/wbs-methodology.md` — WBS方法论（分解方法/模板/算法/验证/输出格式）
- `scripts/wbs_engine.py` — WBS引擎（WBSNode/WBSResult/模板/验证/输出格式化）

### 文档
- SKILL.md 新增WBS子技能入口、Phase -1 工作流、场景4快速示例
- antipatterns.md 新增 AP-W01~AP-W04 四个WBS反模式
- faq.md 新增5个WBS相关Q&A
- _meta.json 新增 sub_skills.wbs 子技能注册

---

## 1.3.2 (2026-06-02)

### 改进
- 使用示例重写：从1个紧凑示例扩展为3个完整场景（直接估算/多阶段CPM/搜索辅助），每个展示完整用户输入→系统响应→输出流程
- 触发场景压缩为联防格式，节省空间给核心示例
- Phase 2 紧前关系从代码块精简为自然语言段落
- 正文公式去除冗余行（normal_mean重复direct估算）
- SKILL.md 稳定在 230 行（≤230 合规）

---

## 1.3.1 (2026-06-02)

### 改进
- 新增"限制与边界"章节：任务数量上限(≤50)、OMP约束(O≤M≤P)、循环依赖检测、报告格式说明
- 快速开始新增完整对话示例：用户输入→系统推荐→确认→报告输出的完整链路
- FAQ新增"出错了怎么办？"（验证/约束冲突时的修复建议）
- FAQ新增"最多能算几个任务？"（容量限制说明）
- SKILL.md 触发场景从9行表格压缩为单行联防格式，释放空间给边界说明
- Phase 2依赖类型描述精简

---

## 1.3.0 (2026-06-02)

### 新增功能
- CPM支持四种依赖类型：FS(完成→开始)、SS(开始→开始)、FF(完成→完成)、SF(开始→完成)
- 新增合理性审查层：validate_cpm_input/validate_cpm_result/validate_mc_input/validate_mc_result/validate_overlap_tasks/validate_all
- 审查覆盖：工期非负、O≤M≤P、start≤end、无循环依赖、无自引用、P50≤P90、标准差非负

### 修复
- calc_overlap 空tasks返回缺少duration字段（与空segments返回结构不一致）
- report-template.md 示例日期硬编码（改为 date.today()）

### 改进
- calc_cpm 函数签名兼容新旧格式，旧格式 {2:[1]} 隐式FS保留

---

## 1.2.0 (2026-06-02)

### 新增功能
- CPM关键路径分析：前向传递(ES/EF)+后向传递(LS/LF)+总时差+关键路径提取+循环依赖检测
- 多分布蒙特卡洛：PERT-Beta/三角分布/泊松近似三种分布并行模拟
- 任务重叠分析：扫描线算法，最大重叠数+最长重叠时长
- 甘特图SVG生成：关键路径红色高亮标注，支持CPM结果渲染
- 多分布MC对比SVG：三种分布直方图叠加+均值线+P50/P90标记
- 紧前关系自动规划：自动FS顺序连接+字符串解析(1→2(FS))
- 报告中新增紧前关系表（CPM章节顶部，显示任务依赖及FS/SS/FF/SF类型）
- 分析建议扩展为5维度：工期结论/关键路径风险/重叠影响/进度缓冲/多分布对比

### 架构更新
- 工作流重组：4阶段→5阶段（新增Phase 2紧前关系规划，原Phase 2/3→Phase 3/4）

### 修复
- MC概率密度图和累计概率曲线图数据缺失（补density/binLabels/cumulative数组）
- 重叠分析返回空区间时缺少duration字段导致KeyError
- HTML模板REPORT_DATA注入方式改为{{REPORT_DATA_JSON}}占位符
- 模板header中{{METHOD_USED}}无值问题
- JS initReport未填充meta[1](SUBTITLE)

### 文档
- report-template.md重写为完整数据接口规范（REPORT_DATA 11字段+分析→格式化→报告标准化流程+LLM建议生成5维规范）
- 新增depTable数据接口文档

---

## 1.0.3 (2026-06-02)

### 修复
- 标准化改造+修复反模式格式+扩展FAQ内容+修复术语混用

---

## 1.0.2 (2026-06-02)

### 修复
- audit --fix 自动修正: writing_standards

---

# 更新日志 (Changelog)

## 1.0.1 (2026-06-02)

- 标准化改造：templates/ 迁移至 .standardization/ 数据目录
- 创建 scripts/ 目录（含 __init__.py）
- SKILL.md 拆分至 ≤230 行，符合 R-17 渐进式加载规范
- 添加渐进式文件索引表
- 删除全部耦合性词汇（"借鉴"等）
- 修复前端描述字段与 _meta.json 同步
- _meta.json 精简为 7 标准字段
- 修复 H1 位置（紧跟在 frontmatter 后）
- 修复代码块语言标识
- 修复 FAQ 格式为 Q:/A: 标准格式
- 修复反模式格式：`**错误做法**：`→`**错误做法：**`（冒号归入加粗）
- 修复术语混用："版本更新历史"→"版本更新记录"
- 扩展FAQ内容（OMP来源Q=34字/A=187字，内容完整）
- 修复 skill-standardization 的 fix.py import error（parse_simple_yaml_frontmatter 缺失）
- 扩展 fix_writing_standards 支持 R-18 反模式格式自动修正
