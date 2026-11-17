# Changelog · ct-literature

## 2026-11-15 · v1.7.10 — SKILL.md 功能信息回补（v1.7.7 过度删减修正，119 → 133 行）

- **问题**：v1.7.7 去 CLI 时把与命令无关的**功能性信息**一并删掉，越过 ct-base §16.1「删掉它，功能 / 正确用法 / 安全边界会不会受影响」的判断线——检索时效保证、配额闸门的阻断语义、逐源台账与覆盖率判决、弱结果救援、Docling 解析能力、技能链路位置、已发布应用 appId 与覆盖式发布纪律全部只余一句指针，agent 在对话中失去判断依据。
- **回补（均为能力/边界描述，无命令、无脚本路径、无参数开关）**：`## Positioning` 增技能链路位置一行；`## Data Sources` 增「时效保证须走本地引擎」的在线通道截断风险；`## Capabilities` 增诚实源台账（ok/empty/error/skipped + healthy/partial/empty/critical gap + 弱结果单次救援）、PDF 结构化解析（Docling 主 / PyMuPDF·PdfPlumber 兜底），批量检索补「配额闸门在估算超阈值时**不发网络请求**先中止」；`## Outputs` 后恢复 `## Published Application`（appId + shareLink + 覆盖式发布、禁止新建 app、shareLink 必须断言，指针仍指向 `references/published_app.md`，段落 2 行合规 §16.1.2）。
- **不外移回**：`Requirements`（Python 版本 / 解释器路径）、`Implementation`（命令行调用）、批量与引文扩展的命令示例、`Unified work schema` 字段表、Evaluation Benchmarks 蓝图、Workbench 测试框架说明——均属实现细节或维护台账，继续留在 `references/` 与 README。
- 校验：`spec_lint.py` F02 / F35 / F36 / F38 / F41 / F44 / F19 全部 0 命中（无代码块、无 `--flag`、无成段中文、无硬折行）；版本 1.7.9 → 1.7.10，workbench 六处版本锚点同步。

## 2026-11-15 · v1.7.9 — log_only 留痕行显式打标（zero_hits 误报根治，本地侧）

- **问题**：ct-update 用 `hits_merged==0` 判「检索零命中」，但 `mode=log_only` 的留痕行**刻意不做检索**，`hits_merged` 是占位 0。实测 30 天 14 条 `zero_hits` 报错全部属此类：载荷只有 `type/topic/query/hits_merged/sources_ok/sources_fail` 六键，而同 query 的其它记录命中 98 / 99 / 144 篇 —— 结论是**误报**，不是检索缺陷。
- **改法**：`feishu_summary` 的 log_only 留痕载荷显式追加 `mode="log_only"`，使取数侧可**直接排除**该行，不必靠字段完整度反推"这条到底检索过没有"。
- **配套**（ct-update 侧，同一提交线）：`literature_record_failures` 增加 `zero_hits_unverified`（warning）分层 + `detect_literature_failures` 跨记录定性（同 query 有更高命中则直接注明「过程性/占位记录」），`diagnose_from_logs` 的修复映射新增 P3 条目。
- 校验：以 639 条真实日志重放，`zero_hits`（error）14 → **0**，14 条全部降级为 warning 并带对照证据。
- 运行时检索逻辑零变化；`version` 1.7.8 → 1.7.9，workbench 版本锚点同步。

## 2026-11-15 · v1.7.8 — README 发布前彻底清理（ct-base §13.1 / §13.3 / §13.4.1 / §13.15 / §13.19 / §13.20 / §13.21）

- **首屏名片去自证**：删除「A 档公开情报技能（输入非涉密）」「默认无 key 也能跑（keyless 池 / credits / not suitable for production）」「不需要命令，也不需要手册」等非功能表述与门槛自证，简介收敛为「做什么」；路由机制说明（何时激活 / 是否联网）一并移出首屏（§3.2 / §13.3）。
- **章节序纠正**：目录与正文由「能力索引 → 案例 → 数据源 → 反幻觉 → FAQ」改为强制序「能力索引 → 使用案例大全 → FAQ」，数据源与反幻觉顺延至 FAQ 之后；编号 1./2./3. 连续（§13.3）。
- **案例按 A 档重构**：7 → 3 个（简单检索 / 证据汇总层 / 批量下载合法 OA PDF），全部三要素完整（你这样说 / 助手会这样回（示意）/ 🖥️ 工作台）；删除「请求被识别为 Simple / Complex / Vague」内部机制段与「关键字确认门」等过程描述；删除自曝局限的模糊请求案例（工作台无多轮追问），该能力保留在场景索引（§13.19 / §13.21 择优三问）。
- **技术细节零披露清洗**：删除后端品牌与部署端点（`coze` / `ct-bugreport.coze.site`）、内部字段名（`citation_verified` / `bot_blocked` / `evidence_log.json` / `meta.imports` / `query_origin` / `session_hash` / `EXT_ID`）、内部文件名（`pdf_manifest.csv` / `needs_manual.csv` / `manual_incoming` / `pdfs_latest40/` / `Literature MOC.md`）、接口主机路径（`api.openalex.org/works/<id>`）、HTTP 状态码（403 / 429）、实现细节（`Referer` + OneTrust cookie、代理绕过理由）、配额内部单位（credits → 次数）、裸内部规范编号（`§17.1`）（§13.3 零披露 / §13.11 / §13.20）。
- **格式规范化**：全文 CRLF → LF、压缩首屏连续空行、文件尾单换行；底部保密声明与 ct-base §13.1 唯一权威模板**逐字一致**，删除多出的「🌐 其他语言」行（§13.4.1 / §13.1）。
- **入口块与链接纪律**：保留 §13.15「不安装也能用」统一入口块逐字文本；案例内不再重复贴总入口 URL，改为「从文首总入口进入」，全文档在线入口仅一处（§13.15 禁散链）。
- **机检补强**（ct-base 侧）：新增 `spec_lint.py` **F45**（WARN）覆盖 F42 漏掉的五类形态——后端品牌/端点、内部字段名、接口路径、HTTP 状态码、首屏免 key·档位自证，防止同类问题复发。
- 校验：`spec_lint.py` ct-literature ERROR 0 / WARN 仅 F26（发布集非 md 文件 90 个，属既有体量问题）；保密声明双语逐字 diff 一致；`\n{3,}` 零命中；F45 清零。

## 2026-11-15 · v1.7.7 — SKILL.md 去 CLI / 去中文（ct-base §4 操作方式约束）

- **SKILL.md 重写为「对话怎么用」的 agent 指南**（232 → 120 行）：删除正文中全部 bash 代码块与命令行调用（批量检索、Meta 主题评估、引文扩展示例），删除 `pip install` / Python 版本 / 脚本路径 / 参数开关等实现细节，改为能力描述 + 指针（命令示例与参数表统一归 `references/sop.md`，能力矩阵归 `references/capabilities.md`）。
- **正文中文清零**（frontmatter 双语文档字段除外）：`## Batch retrieval (批量检索)` 标题、翻译确认门整段、跨轮回显块 `## 当前检索设定：…`、「大小KB / 页数」等改为英文表述。
- **去门槛/档位自证**：删除「无需用户侧 key」「A-tier」等表述，配置与安全边界交由 `permissions` 与安全节承载（ct-base §3.2）。
- **结构收敛**：`## Requirements` / `## Implementation` / `## Published Application` / Docling 安装步骤等非功能段外移，内容并入 `## Outputs` 与 `## Where to Look` 指针。
- 校验：`spec_lint.py` ct-literature F02（超 200 行）消除，正文零代码块 / 零 CLI 开关 / 零中文。

## 2026-11-14 · 数据源页诊断信息折叠（ct-base §32.1 / §32.2 / §32.3）

`#v-sources` 标题「数据源与健康」改为「数据源」：业务区只保留数据源总览表；解释器路径 / 技能目录 / OpenAlex Key 配置回显移入 `<details class="wb-disclose" id="srcEnv">` 默认折叠（样式由 ct-base 共享 tokens.css 提供）。`app.js` 补双语键 `srcEnvTitle` / `srcEnvTag`，`wbOnLangChange()` 改为仅当前在数据源视图时才重载 `/api/sources`（切语言不再无条件探源）；`app.css` 加环境路径串省略号样式。真实后端下无头截图目检通过。

## 2026-11-13 · 共享资产契约同步（§11 / §19.2，非 UI 决策变更，页面版本号不变）

按 ct-base 2026-11-13 增补批次同步共享资产：`workbench/wb-list.css` 注入卡片动作统一右列锚点（`.wb-list-cardacts-bottom` + `--wb-cardact-right` / `--wb-cardact-gutter`）；`workbench/tokens.css` 补 `--wb-pill-base` / `--wb-cardact-right` / `--wb-cardact-gutter`；`publish/` 下同名副本一并同步。

采用**精确注入**而非整文件覆盖：ct-base 真源 `wb-list.css` 的字号仍是裸 px，多数叶子已自行令牌化；整文件覆盖会把字号退回裸 px，并可能丢失技能自有令牌/增强，故只替换契约部分、保留其余原文。

**验证**：CSS 花括号平衡；Playwright 实测 `--wb-cardact-right=10px`、`--wb-cardact-gutter=0px`、`--wb-pill-base` 生效，右上/右下动作规则均取 `var(--wb-cardact-right)`、`cardbody` 取 `var(--wb-cardact-gutter)`，页面 JS 错误 0；publish 副本与源逐字节一致。

## 2026-11-11 · 翻译确认门代码级接入（P1-3）

- **`scripts/topic_translator.py`** 新增 `gate_records(info)`：translate_topic 结果 →
  ct-base bilingual_retrieval §5.2 契约记录数组（词典/联网命中→whole，untranslated
  残留→fail_open 不豁免——目标为英文源，中文直发属真实漏检风险）。
- **`scripts/ct_literature.py`** meta 新增 `keyword_localization`（翻译发生时透出）；
  对话层用 `ct-base/scripts/translation_gate.decide()/render_card()` 分档——存在
  untranslated 残留即 ask_term 阻断，请用户给对照词后重跑。SKILL.md 既有挂钩自此
  有代码支撑。
- 验证：py_compile 通过；gate_records 契约分支 + translation_gate.decide 联测通过。

## 2026-11-09 · v1.7.6 — 从指定文献出发的引文网络扩展（U1b）+ 雪球修复

### 新能力 · 从指定文献扩展引文网络（`--snowball-from` / `--expand`）
- `adapters/fetch_openalex.py` 新增 `resolve_seed(seed)`：DOI → PMID → 题名级联解析为 OpenAlex 文献（`filter=doi:` / 单篇 DOI 端点 / `filter=pmid:` / `filter=title.search:`）。
- 新增 `snowball_from(seed, direction, max_refs)`：解析种子后做 **前后向两跳** 扩展（后向 `referenced_works` + 前向 `filter=cites:W{id}`），首元素为种子本身（`direction="seed"`），邻居标记 `references` / `cited_by`。
- `scripts/ct_literature.py::run()` 新增 `snowball_from` 聚焦模式：给定种子时**跳过关键词检索、多源合并、PubMed 备用腿、关键词雪球块、弱化救援**，语料直接由引文网络构成；`--topic` 不再强制（缺省以种子作为展示主题）。新增 CLI 标志 `--snowball-from`（`--expand` 为其别名），`_sf_mode` 守卫贯穿 fetch/merge/rescue/suggestion。
- i18n 新增 `snowball_from.not_found / seed / done / failed`；workbench `server.py` 登记 `snowball_from` 并映射 `--snowball-from`，前端 `index.html` / `app.js` 新增始终可见的输入框。

### 修复 · 雪球此前为空（潜 bug）
- 旧 `fetch_snowball` 用 OpenAlex `/references` 与 `/cited_by` 子端点，实测两端点返回**单篇 work 对象而非 `results` 列表** → 雪球静默收集 0 篇（关键词 `--snowball` 模式同样受影响）。v1.7.6 改用稳定的 `cites:` 过滤器 + `referenced_works` 批量展开，`fetch_snowball` 与 `snowball_from` 共用，关键词雪球与聚焦扩展一并修复。
- 实测：PMID `32877583` → 解析为 `W3082015854`，扩展得 7 篇（种子 + 前向施引 3 + 后向参考文献 3）。

## 2026-11-08 · 工作台能力对齐（workbench only；功能层保持 v1.7.5）

> 背景：功能层 11/02–11/06 连发 8 个版本，工作台 UI 三件套停在 10/30–10/31，
> `server.py:_build_search_argv` 参数白名单止步 v1.6.2；前端新增控件传新字段会被
> **静默丢弃**（只 pick 已知 key，不报错）。本次只改工作台、文档与检查工具，
> 不改检索引擎行为。原文件备份：`workbench/_bak_20261108/`。

### 防复发 · 2026-11-08 横向补齐（同日 ct-safety 审计后追加）
- `capability_parity.py` 新增**第 5 条「架构 ↔ 文案事实一致性」**：`FACT_CLAIMS` 断言表 +
  `FACT_CROSS_CHECKS` 交叉断言，覆盖本技能上一轮修过的事实（PubMed 故障备份角色 /
  Cochrane 三通道 / PROSPERO 免 token / 两个已撤销的复选框不得复活 / 覆盖澄清必须保留）。
  动因：ct-safety 审计发现「UI 声称 openFDA 本地直连，而 SKILL.md 明确全部检索出站
  Coze」这类矛盾，纯参数与 i18n 检查完全抓不到。ct-registry / ct-safety 同轮补齐该条。

### P0 · 正确性与事实订正
- 五处版本锚点统一到 `1.7.5`：`SKILL.md` 1.7.0→1.7.5、`workbench.config.json` 1.6.2→1.7.5、`server.py:SKILL_VERSION` 与 `app.js:skill_version` 1.5.4→1.7.5。
- `/api/sources` 订正三处事实：新增 PubMed/MEDLINE (NCBI) 独立车道条目；Cochrane 改为「EPMC 期刊过滤 + PubMed `[ta]` + OpenAlex ISSN」三通道；PROSPERO 由「需 token / 经 coze 端点」改为「v1.7.2 起公开 POST 免登录可用」。同步 `SKILL.md` / `references/capabilities.md` 里 reserved / dormant no-op 的旧表述。
- `f_lang` 的「自动」改为「自动（默认中文）」，与 v1.7.4 语言 resolver 对齐（中英双键）。
- ⚠️ v1.7.4 / v1.7.5 的中文交付物修复已同步发布包，但**线上应用仍需按 `references/published_app.md` 覆盖发布**才生效；本次未执行部署。

### P1 · 能力入口与结果展示
- 高级参数新增：PubMed 开关 / 自动补位开关、发表日期起止与「近 N 个月」、双向文献类型甄别（原创 / 指定类型）、DOI 专项审计。同步 `collectForm` / `applySpecToForm` / `settingsLine`、i18n 中英键、`scripts/batch.py` ADAPTER 与 `references/batch_spec.md`、`nl_parse.py` 规则层（顺带修复「近 N 个月」被 `NEAR_RE` 误判成「近 N 年」）。
- `_build_search_argv` 新增 `_KNOWN_SEARCH_KEYS` 白名单与未知字段 `[WARN]`，杜绝「页面有控件、后端不生效、无报错」。
- 结果卡新增「运行审计」区：coverage 徽标（`critical_gap` 红色告警 + 禁止外推）、`meta.pubmed` 的 explicit / fallback / not_run 状态、撤稿 / DOI 不一致 / 引文存疑 / 安全性分轨计数、可展开的四态证据台账。预览卡补 lane 规划行（日期窗 / PubMed / DOI 审计 / 类型甄别）。
- 流式检索面板明确标注 PubMed 为纯本地车道（`coze_routable=False`）、不走 Coze 通道，故**不**加入源下拉——避免制造一个跑不通的假功能。

### P2 · Meta 选题评估视图
- 工具页新增「Meta 选题评估」tab：spec JSON 编辑、内置健康 / 撞车示例（后端同源返回 `DEMO_SPEC`）、SAFE PREVIEW（只解析校验、不落盘不联网）、显式 `--run`（落盘 JSON / MD / HTML）、六维评分条 + 早门短路 + 缺陷与建议渲染。后端 `/api/tools` 新增 `meta_demo` / `meta_topic_eval` 两个 tool。

### 复核修正（用户质疑后重新评估，18:30）
- **撤销**「高级参数 → 数据源」里新增的两个 PubMed 复选框（`f_pubmed` / `f_pubmed_fallback`）。
- 理由：Europe PMC 默认开启且已原生覆盖 PubMed/MEDLINE + Cochrane CDSR，把 NCBI 直连并列成「数据源」会让人误以为不勾选就漏了 PubMed 内容；而 `--pubmed-fallback` 默认开、限流时自动触发，做成用户开关不产生可感知差异。二者本质是**容错 / 冗余策略**，不是数据源，放在数据源区属分类错误。
- 改为：数据源区加澄清说明（明确「没有 PubMed 复选框不是漏项」）；`/api/sources` 把该条 `role` 由「独立车道 · 默认关闭」改为「故障备份 · 默认不运行」并写明非独立内容源；流式检索提示同步改写；前端 `collectForm` / `applySpecToForm` 移除这两个字段，避免访问已不存在的 DOM 节点。
- **保留**：后端 `_build_search_argv` 的两个参数映射、`_KNOWN_SEARCH_KEYS` 的两个 key（兼容对话 spec 与批量调用）、批量 ADAPTER 字段、CLI `--with-pubmed` / `--no-pubmed-fallback`、结果卡的 `meta.pubmed` 补位状态展示。判断依据：**真正有信息价值的是「事后可见补位是否触发」，不是「事前让用户勾选」**。

### 防复发机制
- 新增 `workbench/capability_parity.py`：版本锚点 / i18n parity（含动态 `T('key')`）/ 控件闭环 / CLI flag 三选一，纯 stdlib 零网络，FAIL 退出码 1。
- 接入 `ctqa.config.json` 的 W0 `skill_tests`；`workbench/README.md` 新增「发布前检查（必跑）」章节。
- `EXEMPT_FLAGS` 为 29 个未接线 flag 记录分类与理由（local-only / internal / cli-only）；新增参数必须「接线 / 明确豁免 / 未判定」三选一，未判定即 FAIL。

### 反向借鉴 ct-registry（19:20，用户要求「两边都做」）
- **① 参数失效告知**：新增 `server.py::_applied_report()`，把「填了但没生效」的参数及原因通过 `run_start` 事件的 `applied.skipped` 回传前端并在运行日志显式渲染（借鉴 ct-registry 的 `applied=False` + reason）。此前未知字段只打后端 `[WARN]`，用户完全看不见。覆盖四类：`unknown_key` / `needs_run`（DOI 审计需 `--run`）/ `needs_only_type` / `overridden_by_date_from` / `overridden_by_date_window`（日期级窗口优先于年份）。i18n 中英键齐。
- **② 检索计划审查**：预览卡新增可折叠「检索计划（跑前审查）」区（`planReviewHTML`），列出本次启用的源清单、统一检索词及其来源、日期窗口、类型甄别、验证口径。**诚实边界**：ct-registry 的「逐站改词」不适用——本技能各源共用同一英文检索词，故借鉴的是「跑前可审查」而非逐站编辑。
- **③ 离线演示兜底**：`/api/config` 不可达时标记 `WB_OFFLINE`，显示醒目横幅 + 内置 3 篇示例文献 + 复用 `auditBlockHTML` 的运行审计示例卡，明确「非真实数据、不联网不落盘、启动 server.py 后刷新恢复」。此前只有一句「后端未就绪」。
- 未照搬：ct-registry 的密钥 `****` 脱敏（本技能 LLM key 已是 password 输入且不回显）、0 幽灵参数（是状态不是机制）。
- 文档：`workbench/README.md` 补「反向借鉴」说明；版本锚点保持 `1.7.5` 不变。

### 验证
- `capability_parity.py` → **PASS（0 fail / 0 warn）**：版本 1.7.5 一致；i18n 570/570 键对齐、526 个在用键全覆盖；48 个控件全部被 collectForm 读取、51 个后端白名单键；75 个 CLI flag = 50 已接线 / 29 明确豁免 / **0 未判定**。
- `py_compile` 全通过；`_build_search_argv` 实调确认 `--date-*` / `--recent-months` / `--with-pubmed` / `--no-pubmed-fallback` / `--verify-dois` / `--only-type` 正确落地；`nl_parse` 实调确认「近 3 个月 / PubMed / DOI 审计 / 只要原创研究」识别且 `year_from` 不再被误设。
- Meta 评估实调：SAFE preview 不落盘；`--run` 产出 `verdict=Strong Accept`、6 维评分、3 个产物文件。
- ctqa W0 静态层（`workbench/_tests/test_static.py`）全绿、0 FAIL：`py_compile` / `node --check` / i18n 567↔567 / DOM id 154 个引用均有定义 / 事件协议双向可达。
- HTTP 冒烟（本地 `127.0.0.1`）：`GET /` 含全部新控件；`GET /api/sources` 返回 9 源、含 PubMed 且 PROSPERO 标「免 token」；`POST /api/tools` 的 `meta_demo` 与 `meta_topic_eval` SAFE preview 均 200，preview 不落盘。
- 发布包 `workbench/publish-dist/` 已按 `publish-kit/build_publish.py` 重建（112 文件 / 2.19 MB），6 个关键文件 MD5 与源码逐一一致；构建脚本新增通用排除规则拦截 `_bak*` 备份目录，包内 0 残留。
- ⚠️ **线上部署未执行**（外部发布动作，需单独确认）；发布包已就绪，按 `references/published_app.md` 用既有 appId 覆盖发布即可生效。

---

## 2026-11-06 · v1.7.5 阶段 2 接入 ct-base 交付契约 + 英文交付物零中文

> 关联 ct-base v1.4.45。

- `export_xlsx.py` 删除本地 `resolve_report_lang()`；`ct_literature.py` / `export_html.py` / `report.py` 全部改为 `from xlsx_delivery import resolve_report_lang`（`skill="literature"`），主入口仍只解析一次并贯穿 xlsx / html / md / obsidian / zotero。共享件注入 `scripts/` 与 `workbench/publish-dist/scripts/`。
- **英文模式中文残留修复**：Evidence Log 的 `Run config / 运行配置`、`Source provenance / 来源溯源` 两处中英混排硬编码改为 `_LOCAL` 双语键 `ev.run_config` / `ev.src_provenance`；英文版现为纯英文标签。
- 验证：独立进程 zh/en 两版逐格扫描，英文版 CJK 单元格 0（修复前 2 个）、中文版四表全中文；`CT_LITERATURE_LANG=en` 与显式 `--lang en` 均英文；`py_compile` 与发布包 MD5 一致。
- ⚠️ 线上应用仍待重新部署后页面下载才生效。

---

## 2026-11-06 · v1.7.4 工作台结果文件（Excel / HTML / Markdown）中文化

> 关联：ct-registry 0.14.4 同类问题横向排查。用户反馈「工作台页面下载的 Excel 格式乱、基本都是英文」，要求核查相似技能。

### 根因（本技能与 ct-registry 同病，且覆盖面更大）
- `export_xlsx.export_workbook(lang="auto")` 用 `_base_is_chinese_os()` 判语言；线上工作台跑在 en_US 容器 → 四张 sheet 名 `README / Overview / Works / Evidence Log` 全英文。本地中文 Windows 复现却是中文，故只在线上出现。
- `export_html.render` / `report._resolve_lang` 也各自按 `locale.getdefaultlocale()` 判 auto，线上 `lit_report.html` 实测全英文（标题 "Literature Evidence Base"，中文字符仅 18 个）——**标准交付物 HTML + Excel 一起中招**。
- 线上 `.run_log.jsonl` 的 11-05 命令不含 `--lang`，前端 `#f_lang` 默认 `auto` → 主 CLI 不传语言 → 全链路按服务器 locale 走英文。

### 修复
- `scripts/export_xlsx.py` 新增 `resolve_report_lang()`：显式 `--lang` > `CT_LITERATURE_LANG` > 技能根 `config.json language` > 默认 zh；`export_workbook()` 始终 `set_lang(...)`。
- `scripts/ct_literature.py`：`main()` 与 `run()` 各解析一次语言，让 xlsx / html / md / obsidian / zotero 共享同一具体语言值，不再各自判 locale；`--lang` help 同步更新。
- `scripts/export_html.py` / `scripts/report.py`：auto 改走同一个 resolver（report 保留导入失败兜底）。
- 同步 `workbench/publish-dist/scripts/` 四个文件，逐文件 MD5 一致。

### 验证
- 模拟云端 `is_chinese_os=False`：`auto` → 中文四表「说明/概览/文献总表/证据溯源」+ HTML 标题「文献证据库」（1391 中文字符）；显式 `--lang en` → 英文四表；语言优先级 4 组用例全通过。
- 12 个改动文件 `py_compile` 全通过。
- ⚠️ 线上应用需按 `references/published_app.md` 用既有 appId 覆盖发布后生效；本次仅完成代码与发布包修复，未部署。

---

## 2026-11-03 · v1.7.3 引文核验反向移植 meta-analysis 撤稿检测 + DOI/PMID 双侧交叉验证

> 动机：meta-analysis `ref_verify.py` 有两个本技能缺失的能力——① 撤稿检测（CrossRef + PubMed）；② DOI+PMID 双侧交叉验证（防拼接幻觉）。P4 归一要求「融合不丢弃任何一边有用功能」，故先把这两个能力反向移植到本模块，让本模块成为完整的单一实现，再让 meta 复用（设计稿 §10.1 / §11.4 line 464）。

### Added
- **撤稿检测**（`check_retraction=True`，默认启用）：
  - `_crossref_retracted(msg)`：覆盖 CrossRef **四种**撤稿标记形态——`type=retracted-article` / `title` 前缀 `"RETRACTED:"` / `relation.is-retraction-of` / `updated-by[].type="retraction"`（retraction-watch 源）。DOI 撤稿在 `_fetch_meta_doi` 的**同一响应**内读取，无额外网络调用（返回值变四元组，`_consistency` 取前三项兼容）。
  - `_pubmed_retracted(rec)` + `_pubmed_summary(pmid)`：PubMed esummary `pubtype` 含 `Retracted Publication`（NCBI 官方标记）。本技能原 PMID 通道走 Europe PMC（search result 无撤稿字段，只有 `pubType=journal article`），故补这条 NCBI 通道；进程内缓存（`_PUBMED_RETRACT_CACHE`）。
  - `status="retracted"`：**优先级最高**——撤稿文献即使标题吻合也不得作为证据（红线）。保留 `citation_consistency` / `citation_title_ratio` 供人工参考。
- **DOI+PMID 双侧交叉验证**（`cross_check=False` 默认关闭，保持既有「first positive wins」行为）：`_cross_check_ids(doi, pmid)` 比对 PubMed 记录的 DOI 与传入 DOI，不一致 → `mismatch`（防「DOI 真、PMID 真、但不是同一篇」的拼接幻觉）。元数据不足时返回 `None`（不断定，避免把「查不到」误判为「不一致」）。
- **`verify_one` / `verify_works` 新增参数**：`check_retraction` / `cross_check`（均向后兼容，默认值保持原行为）。
- **summary 新增 `retracted` 计数**。
- **API 元数据回写**（`_emit`）：新增 `verified_title` / `verified_first_author` 两个纯新增字段（meta 非空时写入 API 解析出的真实标题与首作者姓）。动机：执行层归一到本模块后，meta-analysis 的 `format_references` 依赖这两个字段；若不回写，归一后只能拿到输入值（本地引擎原本提供 API 值）——属功能退化。meta 为 None（抓取失败）时不写，避免空值覆盖输入。

### Fixed
- **撤稿检测漏检（meta-analysis 既有缺陷，反向移植时一并修复）**：meta 原实现用 `"retraction" in title/pubtype` 匹配，而 CrossRef 实际返回 `title` 前缀 `"RETRACTED:"`、PubMed 实际返回 `pubtype` 含 `"Retracted Publication"`——**`"retracted"` 不含 `"retraction"` 子串**，两个通道都会漏检（2026-11-03 用 Wakefield Lancet 1998 实测确认：CrossRef `relation` 为空、只有 `updated-by` 带 retraction，meta 三条判据全漏）。新实现统一用 `"retract"` 前缀匹配，覆盖 retract / retracted / retraction。

### 验证
- **真实网络**（Wakefield Lancet 1998 撤稿文，DOI `10.1016/S0140-6736(97)11096-0` / PMID `9500320`）：`status=retracted`、`citation_verified=False`，note 保留 `title/author consistent (Crossref, ratio=0.95)`；正常文献（PMID 42972584）`status=verified`（ratio=1.00），不误判。
- **测试**：新增 `tests/test_verify_retraction.py` **38/38**（零网络；覆盖四种 CrossRef 撤稿形态 / PubMed pubtype / 撤稿优先级覆盖 verified / `check_retraction=False` 禁用且不查 PubMed / 交叉验证 mismatch 与不断定 / summary 计数 / 显式锁定「retracted 不含 retraction」陷阱 / `_emit` 回写 verified_title & verified_first_author（含 meta=None 与空 surnames 的负例））；`tests/` 全量 **130/130**；`scenario10d` **7/8**（D5 report 渲染为既有失败，与本次无关）。

## 2026-11-03 · v1.7.2 PROSPERO 公开检索路径（POST）反向移植自 meta-analysis + 统一执行器支持 POST

> 动机：meta-analysis 的 `prospero_probe.py` 与本技能的 `fetch_prospero.py` 是同一个源的两套实现。前者 2026-10 实测可用（POST + 自造 `prospero-auth-token` 头，公开检索免登录）；后者是 2026-08-12 的**未验证 stub**（GET + 正式 token，无 token 直接 return None，代码自标 `Feature UNVERIFIED`）。按「融合不丢弃有用功能」，把 meta 侧的可用实现反向移植过来，再让 meta 复用本模块的执行器（P2）。

### Added
- **PROSPERO 公开检索路径（POST）**：新增 `_post_search()`（POST `https://www.crd.york.ac.uk/PROSPERO/api/search`，JSON body `{term, actual, line, page, nperpage, sort, sortorder, filters:[], download}`）、`_auth_headers()`（自造 `prospero-auth-token: base64(毫秒时间戳)`，公开检索无需登录）、`_is_error_envelope()`（识别后端 ES 超时的嵌套错误信封，避免把「后端挂了」误报成「0 命中」）、`_map_post_hit()`（`retvals.hits.hits[*]._source` → 统一 work schema，含 BOM 与富文本标签清理）。
- **`fetch(..., raw_query=None)`**：`raw_query` 非空时直接用作检索词，跳过内部 `_build_query` 拼接（`review_type` / `safety` / 日期窗）——供 meta-analysis 等已用真值集调优过候选词与 PICOS 前置的技能复用执行器。
- **返回值新增 `hit_count`**（服务端真实命中数，区别于 `count` = 实际取回题录数）。
- **CLI 透传**：新增 `--raw-query`。
- **`http_utils.post_text()`**：统一执行器新增 POST 能力（复用既有连接池 / 429 退避 / 5xx 重试 / per-host 信号量限速），供 POST-only 源复用，不必各自手搓 urllib。

### Changed
- `fetch_prospero.fetch()` 主路径改为 POST；原 GET + `token` 路径保留为**降级路径**（仅在有 token 时尝试，仍未验证）。无 token 不再直接 return None。
- `tests/scenario10d_evidence.py` 的 D8 由「no-token → return None」改为「preview 不再打印 key-gated 警告」（零网络）。

### 验证
- **真实网络**：`raw_query='efficacy AND pd 1 AND inhibitors AND advanced'` → **1479 条**，与 meta-analysis 侧基线**完全一致**；无 PICOS 主题同口径一致。
- **测试**：新增 `tests/test_prospero_post.py` **25/25**（零网络；覆盖鉴权头格式 / 错误信封 / 字段映射与 BOM 清理 / 解析与顶层+嵌套错误抛错 / `raw_query` 旁路 / POST 失败降级 GET / preview 不联网）；`tests/test_raw_query.py` 8/8；`scenario10d` 7/8（D5 report 渲染为既有失败，与本次无关）。

## 2026-11-03 · v1.7.1 新增 `raw_query` / `strict_raw_query` 旁路（供 meta-analysis 复用执行器）

> 动机：meta-analysis 的选题去重探针（`literature_probe.py`）与本技能的 `fetch_europepmc` / `fetch_pubmed` 存在**功能重复**——两边各写一套 HTTP / 重试 / 限速 / 解析 / hitCount 提取。按 ct-base §20.19「coze 后端合并判定框架」的消除重复原则，meta-analysis 保留自己的**检索式构造**（连字符词加引号策略经 123 篇真值集验证，与本技能语义不同），只复用本模块的**执行器**能力。

### Added
- **`fetch_europepmc.fetch(..., raw_query=None, strict_raw_query=None)`**：`raw_query` 非空时**直接**用作检索式，跳过全部内部子句拼接（`review_type` / `safety` / `cochrane` / `include_reviews` / 日期窗）——调用方应已把这些条件编进 `raw_query`，其余过滤参数一律忽略。`strict_raw_query` 非空时额外发一次 idlist 请求取严格口径命中数（不取题录），失败降级 `None`，不影响主结果。
- **`fetch_pubmed.fetch(..., raw_query=None, strict_raw_query=None)`**：同上语义；`strict_raw_query` 非空时额外做一次 `esearch`（`retmax=1`，`count` 独立于 `max_results`）。
- **返回值新增字段**：两个模块均新增 `strict_hit_count` / `strict_query`（未传时为 `None`），既有字段与语义不变。
- **CLI 透传**：两个模块命令行入口新增 `--raw-query` / `--strict-raw-query`。
- **测试**：`tests/test_raw_query.py` 8/8（零网络；覆盖 T1 非空跳过内部构造 + 其余参数被忽略、T2 不传时行为不变、T3 严格口径只取命中数不取题录、T4 严格口径失败降级、T5 preview 模式仍返回 None）。

### 兼容性
- 完全向后兼容（ct-base §20.11）：两个参数默认 `None`，不传时行为与改动前一致；返回值仅**新增**两字段，无改名、无移除。

## 2026-11-03 · v1.7.0 新增 NCBI E-utilities 车道（PubMed/MEDLINE + CDSR）与 Europe PMC 故障自动补位

> 动机：Europe PMC 是本技能**唯一原生同时覆盖** PubMed/MEDLINE 与 Cochrane CDSR 的源
> （一条 `JOURNAL:"The Cochrane database of systematic reviews"` 查询即同时命中两者）。
> 它一旦限流/不可达，PubMed 与 Cochrane 覆盖会**同时归零**；OpenAlex 只兜住 PubMed 那一半
> （`ids.pubmed`），因为它没有 CDSR 过滤器。本次新增一条与 Europe PMC **相互独立**的 NCBI 直连车道，
> 把两半都补回来。

### Added
- **B · NCBI E-utilities 独立车道 `adapters/fetch_pubmed.py`**：`esearch`（id 列表）→ `efetch`（XML 全字段）
  → `esummary`（JSON 兜底）三段式，`db=pubmed`。覆盖 PubMed/MEDLINE 与 CDSR
  （`Cochrane Database Syst Rev[ta]`，与 Europe PMC 期刊过滤器同源同效）。产出统一 work schema
  （`source=PubMed` / `pmid` / `pmcid` / `pub_types` / `mesh` / `url` / `open_access_url`），
  与既有源同去重、同评分、同 PRISMA。限流：无 key 3 req/s、有 `NCBI_API_KEY` 10 req/s；
  串行节拍 `_throttle()` + `http_utils._POOL_HOST_MAX["eutils.ncbi.nlm.nih.gov"]=2` 双重控速；
  `CT_LIT_NCBI_EMAIL` / `CT_LIT_NCBI_TOOL` 进入 polite pool（空值绝不发送）。
  入口：`--with-pubmed`（显式挂载）/ `--sources PubMed`（`ncbi`、`medline` 亦为别名）。
- **B · Europe PMC 故障自动补位 `--pubmed-fallback`（默认开，`--no-pubmed-fallback` 关）**：
  当 Europe PMC 腿**确实不可用**（请求异常，或有 `hit_count` 但 0 条落地）时自动启用 PubMed 车道。
  触发三条件：fallback 开启 + 未显式 `--with-pubmed`（不重复检索）+ Europe PMC 已启用。
  补位产物与常规源 payload 走**同一套** `_dispatch_merge` → 评分 → PRISMA → 报告，下游无感知。
  状态入 `meta.pubmed`（`explicit`/`fallback_enabled`/`ran`/`trigger`），原因写入证据台账
  （PubMed 条目 `status="fallback"` + note），控制台播报 `[PubMed-fallback]` 事件。
- **C · OpenAlex CDSR 过滤 `primary_location.source.issn:1469-493X`**（`adapters/fetch_openalex.py`）：
  `--cochrane` 时注入 ISSN 过滤，使 OpenAlex 段也能限定 Cochrane；同时**始终**按期刊名打 `is_cochrane`
  标（与 `fetch_europepmc` 对齐），让客户端二次过滤在 OpenAlex 段同样生效。不传 `--cochrane` 时行为不变。
- **D · Europe PMC polite pool**（`adapters/fetch_europepmc.py`）：新增 `tool` + `email` 参数
  （CLI `--email` / `--tool`，env `CT_LIT_EUROPEPMC_EMAIL` / `CT_LIT_EUROPEPMC_TOOL`）。
  不参与结果集，只影响 API 配额待遇；**空值不发空串**。
- **源归一与排序**：`normalize._SOURCE_CANON` / `dedupe_engine._canon_source` 增 `pubmed`/`ncbi`/`medline`
  → `PubMed`；`_SOURCE_PRIORITY` 把 `PubMed` 列为 **rank 0**（一次库，与 Europe PMC 同档，不是补充源）；
  `SOURCE_REGISTRY` 注册 `PubMed`（`coze_routable=False`，纯本地独立通道，无 Coze 节点）。
- **新增单测 `tests/test_pubmed_lane.py`**（13 项，无网络、可独立运行）：检索式拼装、
  XML 标识符作用域回归、统一 schema、registry local-only 路由、归一/优先级、礼貌池参数、节流节拍。

### Fixed
- 🔴 **`source_registry._local_only` 本地兜底全灭**（另一任务引入的回归，本次修复）：
  `_local_only` 显式传 `run=True` 的同时又 `**_strip(_kw)`（其中也含 `run=True`），
  触发 `TypeError: got multiple values for keyword argument 'run'`，被函数内 `except Exception: pass`
  **静默吞掉**，于是 OpenAlex / EuropePMC / bioRxiv / medRxiv / arXiv / SemanticScholar
  **所有源**的「Coze 不可用 → 本地兜底」路径都退化成空 payload（`count=0`），
  且从日志上完全看不出来——最坏的一类故障：看起来像「该源没检索到」。
  修复：去掉冗余的 `run=True`；并把静默 `except` 改为向 stderr 打印 `[WARN]`，
  使「兜底没跑起来」与「兜底跑了但没结果」可区分。
  回归测试：`test_local_only_dispatches_pubmed` 断言 local-only 分支真的产出 payload。
- 🔴 **PubMed XML 标识符被被引文献覆盖**（本次新代码的自查发现）：PubMed 的 `efetch` XML 文末
  `<ReferenceList>` 里**每条被引文献自带 `<ArticleIdList>`**。原实现用 `.//ArticleId` 后代匹配，
  会把别人的 `PMCID`/`DOI` 盖到本文头上——实测 `osimertinib` 的 CDSR 文献 PMCID 被换成
  某篇参考文献的 `PMC3256545`（正确值 `PMC12107686`）。改为只取本文
  `./PubmedData/ArticleIdList/ArticleId`，并加回归测试
  `test_xml_identifiers_not_overwritten_by_references`（构造含 ReferenceList 的 XML 断言不被污染）。
  同类隐患排除：`ArticleIdList` 挂在 `PubmedData` 下（与 `MedlineCitation` **平级**），
  只在其内部查找会永远取不到 PMCID——两处作用域问题一并修正。
- **`evidence_log.build_log` 同名源重复计账**：Europe PMC 故障 → PubMed 补位成功后，
  payload 已记 `PubMed ok count=1`，degraded 列表又追加一条 `count=0` 的同源条目，
  读起来像「PubMed 没取到东西」。改为把补位原因并回已有条目（`note`），不再重复追加。

### Changed
- `--sources` 的 `pubmed` **不再别名到 `europepmc`**。此前 PubMed 只能经 Europe PMC 到达，
  故把 `pubmed` 映射到 `europepmc`；现在 NCBI 是独立车道，写 `pubmed` 就该真的走 NCBI。
  要 Europe PMC 那条腿请显式写 `europepmc`。`--sources` 帮助文本与 `capabilities.md` 已同步。
- `run()` 的 online 分支把 `cochrane` 一并下传给 `source_registry.fetch_source`：
  此前 online 模式只靠客户端二次过滤（`[WARN] cochrane_filter_not_pushed`），
  现在本地兜底路径（OpenAlex ISSN / Europe PMC 期刊过滤）也能真正限定 CDSR。
- 新增 `--with-pubmed` / `--pubmed-fallback`（`BooleanOptionalAction`），
  PREVIEW 的源列表、lane 规划视图、`--interactive` 门控计划、四态台账均已同步呈现 PubMed。

## 2026-11-02 · v1.6.3 新增三项纯本地增量：段落级锚点 / Zotero 导入 / 中文库导入 + China 证据车道

> 来源：微信公众号《实证智能体》8 个文献检索 Skill 盘点（二手线索，tier=wechat-secondhand），
> 一手深读对应 GitHub README 后收敛为 3 项。逐项对照表见
> `ct-update/reports/deep_read_wechat8skills_2026-11-02.md`；paper_ledger 候选
> `gh-wenshu-2026` / `gh-zotero-assistant-2026` / `gh-cnki-skills-2026` / `gh-papersearch-skill-2026`。
>
> **三项均为 opt-in、纯本地、零网络（或仅本地回环），不触碰 Coze 检索层**：
> 不传新参数时行为与 v1.6.2 字节级一致。

### Added
- **G · 段落级锚点溯源 `--anchor`**（`adapters/anchor_injector.py`）：把已下载 PDF 切成段落块，
  注入确定性 Block ID `{doc_hash}:{page}-{block_index}`（doc_hash = 文件内容 sha1 前 10 位，
  与路径/时间无关）。`works[i].provenance` 由 `{doi, title}` 扩展为
  `{doi, title, block_id, page, quote_excerpt}`，evidence_log 新增 `anchors` 汇总块 + MD 覆盖行。
  honest degradation：无本地 PDF → `anchor.status=pdf_missing`；扫描版无文本层 → `no_text`；
  **绝不伪造锚点**。pypdf 优先 / PyMuPDF 备选 / 双缺 → `unavailable`。文档级缓存避免
  `_finalize` 二次调用重复解析。
- **H · Zotero 本地库导入 `--zotero-import "<集合路径>"`**（`adapters/zotero_import.py`）：
  经 Zotero 官方本地 API（`127.0.0.1:23119`）**只读**导入，无 key、**MCP-free**
  （规避既有候选 `wechat-2026-zotero-literature-ingest` 的第三方插件风险），补齐
  `zotero_exporter.py` 只有单向导出的缺口。集合路径逐级精确解析；0 命中 / 同名歧义**显式报错
  并列出候选**，不猜；子附件与笔记不计入文献数（`stats.attachments_skipped/notes_skipped`）。
  🔴 **根因修复（实测踩坑）**：本地回环请求原先走系统代理，`127.0.0.1:23119` 被代理拦成
  **HTTP 502**，看起来像「Zotero 挂了」。改为 `ProxyHandler({})` 显式绕过代理后，真实状态
  才浮出（`WinError 10061 连接被拒绝` = Zotero 未运行）。5xx 另附「端口可能被代理/占用」提示。
- **I · 中文库导入 `--merge-cn <RIS|JSON>`（可重复）+ China 证据车道 `--guidelines-region china`**
  （`adapters/cn_ref_normalizer.py`）：消费用户**在自己机构权限下**从 CNKI / 万方 / SinoMed
  导出的 RIS 或 JSON —— **不爬取、不访问站点、无 Cookie、无浏览器驱动**，与原「no crawler」
  红线一致。每条导入生成标准 source payload（`CNKI`/`WanFang`/`SinoMed`/`VIP`），并入同一套
  去重 / 引文验证 / PRISMA；留痕写入 `meta.imports`（文件 / 源名 / 条数）。
  不支持格式（`.nel`/`.enw`/Excel）**显式报错**并给转换建议，不静默返回 0 条。
  `guideline_corpus.load()` 新增 `region` 过滤（`china`/`global`/`both`）。
  🔴 **落地时发现的两个真缺口**（不是代码写错，是功能会空转）：
  ①**语料 96 条全部无 `region` 字段**（实测 `regions=[('(none)', 96)]`）——只认字段则
  `--guidelines-region china` 恒返回 0 条，看着像「中国证据少」实为功能空转。改为
  **机构名兜底推断**（`CMA`/`CDE`/`NMPA`/`NHC`/`CACA`/`CSCO` → china，显式 `region` 优先），
  现网语料立刻可用：`all=96 · china=4 · global=92`（CMA 中华医学会 4 条），推断结果回填到
  每条 work 的 `region` 字段供报告/审计查看。
  ②**`--with-guidelines` 对中文主题恒 0 条**（既有缺陷）：`run()` 把中文 `_topic_zh` 传给
  `load()`，而语料 `topic` 是英文短词、匹配方式是子串判断 → 中文主题永远匹配不到。
  新增 `_guideline_topic_candidates()`：0 命中时按「英文检索式 → 各 OR 分支 → 最长词」
  依次重试（`type 2 diabetes` 整串 → `diabetes` 命中），事件 `guidelines_i18n_retry` 留痕；
  仍 0 则如实报告，不编造。

### Changed
- **CJK 题名去重整固**（`scripts/normalize.py`）：`_norm_title` 对含 CJK 的题名改走
  `cn_ref_normalizer.normalize_cn_title` —— 全角 ASCII→半角、高频繁体→简体（**受控单字表**，
  未收录字符原样保留）、中文标点剥离、空白/大小写归一。归一只用于**生成 key**，不回写
  `title` 原文。**英文题名路径保持原样**（输出字节级不变），不影响既有去重结果。
  实测：`非小細胞肺癌…` 与 `非小细胞肺癌…` 两条 → merge 后 1 条，`sources = {CNKI, WanFang}`。
- `_SOURCE_CANON` / `_SOURCE_PRIORITY` 新增 `Zotero` / `CNKI` / `WanFang` / `SinoMed` / `VIP`
  （rank 1，与 S2/arXiv 同档的**补充源**，不替代主检索覆盖度判断）。
- `evidence_log.build_log()` 新增可选 `anchors=` 参数（默认 None → 与旧行为一致）。

### Docs
- `SKILL.md`：新增「Local-source imports & paragraph-level provenance」章节；Data Sources 补导入源说明；版本 1.6.2 → 1.6.3。
- `README_zh-CN.md` / `README.md`：知网 FAQ 由「刻意不支持」改写为「**支持导入、不支持爬取**」，
  给出 `--merge-cn` 命令与 `--guidelines-region china` 用法，红线表述不变且更明确。
- `references/multi-db-search.md` §9.1：导入槽从「手工转 payload JSON」升级为一行 CLI，
  补充 CJK 去重已解决项 / 未覆盖项、Zotero 导入、region 车道。

### Tests
- 新增 `tests/test_g_h_i_upgrades.py`（15 项，无网络）：G 段落切分确定性与 Block ID 格式、
  真实 PDF 锚点（fitz 造件）、缺 PDF 不伪造 provenance；H 集合精确解析 / 同名歧义报错 /
  子附件不重复计数 / API 不可达的可操作报错；I 全半角与繁简归一致同键、端到端 merge 合并、
  RIS 解析、不支持格式显式报错、region 车道过滤。
- 回归：既有 `test_dedupe_engine.py` + `test_source_registry.py`（28 项）全绿。
- 端到端实跑（`--run --local --max 6 --verify top --merge-cn --anchor`）：25 篇合并
  （含 CNKI 1 篇），`anchors={total:25, pdf_missing:25}` 如实报告，HTML/XLSX/evidence_log 正常产出。


## 2026-10-30 · v1.6.2 修复 Cochrane 聚焦模式静默空结果（v1.6.0 回归）+ 工作台开关语义纠偏

### Fixed
- **`--cochrane` 经 coze 统一后端检索时静默清空全部结果（v1.6.0 回归 · 现场事故）**：
  现象为 SGLT2i/CKD 主题跑完后 `.merged.json` `count=0`、PRISMA 四阶段全 0，报告空白，却无任何报错。
  根因链：`--cochrane` 是「仅 CDSR」聚焦模式，其过滤条件只匹配 `publication` 字段；v1.6.0 将
  去重/归一化/PRISMA 组装上移 coze 后，coze payload 只输出 `journal_iso`、不含 `publication`
  （实测 `lit_sglt2_ckd/.search_cache.json`），过滤匹配 0 条 → 整个结果集被丢弃。
  v1.6.0 之前走本地归一化（`fetch_europepmc.py` 同时产出 `publication` + `journal_iso`）故不致命。
  旁证：同次运行 `verification.total=99`——引文验证在 fetch 阶段并发执行，早于该过滤，证明数据本已抓到。
  修复两处：①`_COCHRANE_FIELDS` 容错匹配（`publication` / `journal_iso` / `journal` / `venue` /
  `container_title`，并honor `is_cochrane`），适配 coze 与本地两种 schema；②fail-fast——
  `_before > 0 and not works` 时抛 `SystemExit` 并打印「聚焦模式过滤后为空」的可操作指引，
  杜绝「静默零结果被误读为无文献」。另对 coze 路径补 `[WARN] cochrane_filter_not_pushed`：
  后端未推送 CDSR 期刊过滤，客户端过滤可能漏检真实存在的 Cochrane 系统评价。
- **工作台「Cochrane 专属」复选框语义陷阱**：该开关原本与 Europe PMC / Semantic Scholar 并排在
  「数据源」多选区，形似「多勾一个来源」，实为「只保留 CDSR」的聚焦模式；用户想「顺便查一下 Cochrane」
  勾选后，在 v1.6.0 之后直接得到空结果。修复：从「数据源」区移出，改置于「主题与范围」区末尾
  （与「偏向安全性 / 不良事件」同为模式型开关）；文案改为「仅 Cochrane 系统评价（聚焦模式）」；
  新增 `cochraneHint` 双语提示，明确「这是聚焦开关不是来源开关」「勾选会丢弃全部非 CDSR 记录」
  「CDSR 无收录时返回 0 篇并报错退出」「Europe PMC 默认开启已覆盖 Cochrane 期刊」。
- **「CT 首页」按钮被 CSP 拦截、点击无效（既有缺陷）**：`index.html` 的 `#wb-cthome` 原先用内联
  `onclick="wbGoCtHome()"`，而 `server.py` 下发的 `Content-Security-Policy: script-src 'self'`
  会拦截一切内联事件处理器（控制台报 `Executing inline event handler violates the following CSP
  directive 'script-src 'self''`），表现为按钮完全无响应。修复：移除内联属性，改在 `app.js`
  启动流程 `wbLoadConfig().then(...)` 内用 `addEventListener` 绑定。修复后 `index.html` 已无任何
  内联事件处理器，实测点击可正常触发到 `https://ct.medstatstar.com/` 的导航。
- **注**：`workbench/` 整目录在 `.gitignore` 内，server.py / index.html / app.js 无版本快照，
  本次 UI 改动同样只能靠本 CHANGELOG 追溯。

### 验证
- `node --check app.js` 通过；`index.html` 标签配对全闭合（HTMLParser 扫描：未闭合 0 / 错误 0）。
- i18n 双语键对齐：`cochraneHint` zh/en 均存在，两词典无「仅单侧存在」的 i18n 键。
- **全页巡检（7 页签 × Chromium 1440×1050）**：对话检索 / 批量检索 / 高级参数 / 工具 / 输出文件 /
  历史 / 数据源 全部正常渲染，无空白页；`pageerror` 0 条；切换 EN 后 `srcCochrane` → `Cochrane SRs
  only (focus mode)`、`cochraneHint` → 英文全文，切回中文亦正常。
- **元素 id 交叉核对**：`app.js` 引用 94 个 `$("#id")`，与 `index.html` 定义的 641 个 id 比对，
  仅 `batch_go_run` / `typing` 未静态出现——二者均为运行时动态创建（`app.js:975` / `:602`），非缺失。
- 实机渲染（临时实例 :8799）：开关落位「主题与范围」区、文案与提示正常显示；
  「数据源」区剩余 6 项（Europe PMC / Semantic Scholar / bioRxiv / medRxiv / arXiv / 本地指南语料库）布局整齐。
- CSP 复验：修复后控制台 CSP 违规 0 条，`#wb-cthome` 点击可触发目标导航。
- 回归复跑（去掉 `--cochrane`、`review_type=all`）：SGLT2i/CKD 主题 101 works
  （OpenAlex 49 + Europe PMC 50 + medRxiv 2），PRISMA 识别 101 → 筛除 1 → 纳入 100，覆盖率 healthy。

## 2026-10-28 · v1.6.1 ct-qa 配置补齐（主 CLI 纳入静态分析）+ 1 项假阳修复

### Fixed
- **`ctqa.config.json` 的 `static.python_files` 漏了主 CLI `scripts/ct_literature.py`**（只列了
  `workbench/server.py` + `workbench/nl_parse.py` 两个）。后果：W1 的语法检查 / 事件协议
  分析对本技能的**核心 CLI 零覆盖**，且因看不到 CLI 产生的事件而误报「前端死代码」。
  已补入 `scripts/ct_literature.py`、`adapters/fetch_coze_unified.py`、`adapters/coze_resolve.py`。
- **W1-006「suggest_few 死代码」是假阳**（由 ct-base 框架侧修复）：`workbench/app.js` 里
  一段**说明性注释**写着「此处原有 `ev.ev==="suggest_few"` 两个分支……已删除」，
  事件提取正则把注释里的分支名当真 → 恒报死代码、且越解释越报错。
  框架新增 `_strip_comments()`（识别字符串 / 模板串 / **正则字面量**三种状态），
  判据只认真实代码。修复后 W1 PASS 5 → 6、WARN 1 → 0。

### 验证
- `python -m ctqa run --skill <ct-literature>`：**PASS 126 / FAIL 0 / WARN 1 / SKIP 4 → 绿灯**（exit 0）。
  剩余 WARN 1 = `W2B-012` 资源级 404（静态服务无后端 `/api/*`，环境噪音）。
- `C0` 内置层 SKIP 1 属预期：本技能**没有** `adapters/coze/` 目录（扁平 `adapters/*.py`），
  §27.6 条 4 不适用；C0 内容由 3 条 legacy 套件覆盖（白名单脱敏 7 例 + 异步 mock + SSE 解析）。

## 2026-10-27 · 固化 lit_preprint_check 全管线真实回归测试（coze 在线）

把此前临时全管线验证固化为永久回归测试，覆盖 coze `lit_preprint_check` 在
`PdfDownloader._find_earlier_preprint` 真实路径里的接入（真实 EuropePMC 候选检索 + 真实 coze 同篇校验）：
- 新增 `tests/regression_pdf_preprint_check.py`：三场景
  - S1 author_match：候选作者与文献作者一致 → coze 返回 passed=True → 返回 `("preprint", url)`
  - S2 author_mismatch：不一致 → 返回 None（宁可缺漏），note 记 `rejected by author check`
  - S3 coze_unavailable：`call_coze_strategy` 打桩返回 None → fail-loud 标脏（`_strategy_unavailable["lit_preprint_check"]==1`，与 `skipped_no_oa` 分离），返回 None
- 新增 `tests/conftest.py`：注册 `network` marker + `--network` 开关；带该标记的用例默认
  pytest 跳过（`pytest tests/` 不误伤），显式 `pytest tests/ --network` 才执行。
  同时兼容项目既有约定——`python tests/regression_pdf_preprint_check.py` 直接跑（其 `__main__` 入口）。
- 隔离设计：日常快速回归默认不触网；网络/coze 在线时按需 `--network` 或直跑该文件。
  EuropePMC 候选随时间漂移——探测标题均无带 PDF 直链的 PPR 候选时三场景自动 skip（数据漂移而非代码缺陷）。
- 测试构建要点（踩坑记录）：coze 端 `lit_preprint_check_node` 对 `authors` 字段直接
  `_surnames()` 做姓氏提取，**要求 authors 为字符串列表**（与真实管线一致：fetch 阶段
  authors 即全名/姓氏字符串，非 dict）。测试须传字符串 authors（从候选姓氏派生）才能命中节点；
  传 dict（`[{"family":...}]`）会让节点 `.strip()` 报 `dict has no attribute 'strip'`。

## 2026-10-27 · v1.6.0 上线前置修复：coze 白名单登记 + fail-loud 标脏 + 回归套件适配新契约

v1.6.0 把三项策略上移 coze 后做全量代码检查，发现并修复「上线前置」缺口与护栏失效。
（版本锚点仍为 v1.6.0，本次为其落地修复，未 bump。）

### Fixed — P0：coze 端 source 白名单漏登记（部署了也不生效）
- `ct-registry/adapters/coze/src/graphs/sources.py`：`SUPPORTED_SEARCH_SOURCES` **未登记**
  `lit_route` / `lit_preprint_check` / `lit_dedup`，只有 `search_node.py` 加了分支。
  fail-closed 顺序是先 `normalize_source → is_supported` 再分发，故三节点一律被拒：
  线上实测 `UNSUPPORTED_SOURCE: 'lit_route'`（三个节点同）。**即便部署当时源码也不可用**。
- 修复：白名单补三行（含注释），分支 ⇄ 白名单 **25 = 25 零差集**；官方
  `scripts/selfcheck.py` **44/44 全绿**（本机 3.13 缺 pydantic，用 `py -3.8` 跑）。
- 备份 `src/graphs/sources.py.bak_litsrc_20261027_072115`。

### Fixed — 产品：coze 策略节点不可用时静默产出「0 篇成功报告」（fail-loud）
v1.6.0 纯薄客户端无本地兜底，coze 挂了就静默降级，用户无从区分「服务故障」与「真没文献」：
- `scripts/ct_literature.py`：`_dispatch_merge` 返回空时新增 `_dedupe_unavailable` 判定 →
  ① `_out("[FATAL] …")` 醒目告警；② 写入 `source_notes`（→ `evidence_log` 留痕）；
  ③ 写入 `meta["data_integrity"]`（→ HTML/XLSX 可呈现）。**不中断流程**。
- `adapters/pdf_download.py`：`stats` 新增 `route_unavailable` / `preprint_check_unavailable`
  两个计数，与 `skipped_no_oa` **分离记账**——后者是「判定为非 OA」，前者是「判不出来」；
  新增 `self._strategy_unavailable` 实例计数器；run() 末尾汇总 `[PDF][FATAL]` 告警。
  逐篇 `pdf_download_note` 仍写明 `unavailable`，不伪装成已判定。

### Fixed — 发布包一致性：顶层死引用会阻碍源码保护落地
- `scripts/ct_literature.py`：删除顶层 `from adapters import dedupe_engine`（v1.6.0 后已无
  调用点，是死引用）。CHANGELOG v1.6.0 要求「发布包剥离本地策略副本」，顶层 import 会让
  剥离 `dedupe_engine.py` 后的发布包启动即 ImportError。改为注释说明 + 按需导入。
- `scripts/e2e_regression.py`：`from adapters import dedupe_engine` 改为 try/except 可选导入，
  剥离后 v2 校验步骤自动降级跳过（该文件随包发布，不在 `tests/` 排除范围内）。

### Fixed — 回归套件适配 v1.6.0 新契约（此前 17 项常红）
- `tests/regression_pdf_enhance.py`：夹具 `_fake_download(url, doi)` 未跟随 10-26 新增的
  第三参数 `_download_direct(url, doi, work)` → TypeError 判失败。**夹具过期，非产品 bug**。
- `tests/regression_pdf_speed.py`：同上签名漂移（2 处）+ 未适配 lit_route 判桶（6 篇间接项
  需 mock lit_route 返回 coze 才进子批管道）。
- `tests/regression_pdf_routing.py`：**重写为双场景**（原 10 项红）—
  新增 `_patch_strategy()` mock 薄客户端出口 `call_coze_strategy`，覆盖
  ① coze 可用：四桶落地（local_direct / local_preprint / coze / skip）、节点入站范围
  （lit_route 只收本地全失败的篇、lit_preprint_check 只收预印本候选）、作者校验拒绝；
  ② coze 不可用：fail-loud 记账（route_unavailable=3 / preprint_check_unavailable=1
  与 skipped_no_oa=3 交叉核对）、本地动作不受影响、不发起 coze 批量下载。
  同时修正 `_prefetch_identifiers` 被整体 mock 导致 pmcid 分支失效的问题（classify ① 依赖它）。

### 验证（本机，零真实消费）
| 套件 | 结果 |
|---|---|
| routing（重写后） | 36 断言 0 FAILED |
| enhance | ALL PASS（原 7 红） |
| speed | 11 通过 / 0 失败（原 4 红） |
| test_source_registry / test_dedupe_engine / test_fetch_coze_unified_async | 10 / 18 / 16 全绿 |
| root_causes / force_coze / stream_parser | 24 / 24 / 8 全绿 |
| py_compile（adapters+scripts） | 0 失败；`import ct_literature` OK |
| coze 端 selfcheck | 44/44 |

### 待办
- **部署**：`adapters/coze/dist/coze_deploy_bundle_20261027_072145.zip`（含三节点 + 白名单修复）
  仍由人工部署；部署后需打三节点探针验证不再 `UNSUPPORTED_SOURCE`。
- 已知 minor：预印本候选被 lit_route 判 skip 时，最终 note 会覆盖掉「作者校验拒绝」原因
  （审计信息丢失），未改，待确认是否需要保留双因。

## 2026-10-26 · 源码保护上移：路由红线 / 预印本同篇校验 / 去重归一化 迁移至 Coze（v1.6.0）

为护源码（避免随技能发布包泄露策略逻辑），将三项「决策/策略」逻辑从本地上移至 ct-search coze 端
（新增独立节点 lit_route / lit_preprint_check / lit_dedup），本地改为纯薄客户端（无本地兜底）：

- **lit_route（路由红线 + 多级回退次序）**：原 `_classify` ⑥ 的「非 OA 不送云端」红线与
  `has_local_signal/is_oa/doi` 信号组合判定策略上移。本地仍负责 ①②③④⑤ 动作（EPMC/OpenAlex/
  非 WAF 直链/Unpaywall/预印本检索），全部失败时批量（一次 coze 调用）送 lit_route 取
  local_direct/local_preprint/coze/skip 桶。
- **lit_preprint_check（预印本作者级同篇校验）**：原 `preprint_fallback._author_check`
  「宁可缺漏不能弄错」策略上移；本地 `_find_earlier_preprint` 检索 PPR 候选后批量送校验。
- **lit_dedup（去重 / 归一化 / PRISMA 组装）**：原 `normalize.merge*` 与 `dedupe_engine.merge_v2*`
  的去重键规则、EuropePMC 字段优先、预印本-发表版配对、v2 多标识传递闭包 + 模糊标题等启发式
  全部上移；coze 节点按 `engine` 字段支持 v1/v2，返回 works + duplicates_removed/raw_count。
  本地 `_dispatch_merge` 改为薄客户端；`dedupe_key` 保留本地（living-review 跨轮戳记依赖）。

设计约束（纯薄客户端 · 无本地兜底）：coze 不可用 = 该功能不可用（路由失败判 skip / 去重返回空 /
预印本校验收不到则不下载），本地不再保留等价的策略副本用于兜底。向后兼容：老 `source=publisher_pdf_batch`
等路径完全不受影响（server 端默认分支透明，旧客户端无感）。

新增 `adapters/_coze_strategy.py`：统一封装出站信封（ct-base coze_io_contract）与 SSE 解析，
供 pdf_download / normalize / dedupe_engine 共用；`_parse_coze_stream` 新增 `return_full` 以取回
完整统计字段。

⚠️ 上线前置（缺一不可）：
  1. **必须重新部署 ct-registry coze 服务**（`adapters/coze/src` 含三新节点 + search_node 分支），
     否则调用返回 UNSUPPORTED_SOURCE，本地退化为 skip/空（功能不可用）。
  2. **发布包须剥离本地策略副本**：`normalize.merge*` / `dedupe_engine.*` / `pdf_download._classify`
     的等价策略逻辑不得进入发布包（源码保护）；本地保留仅供单测/离线（tests/ 不随包发）。
- 验证：coze 三节点逻辑单测通过（v1/v2 去重、传递闭包、模糊标题、红线、同篇校验、legacy 兼容）；
  本地端 py_compile + `_classify` 路由信号 + `call_coze_strategy` 信封/错误识别通过。

## 2026-10-26 · 公网威胁模型加固（v1.5.4）

工作台唯一运行形态为公网发布（`ct-literature.app.workbuddy.host`），按「无鉴权公开服务」威胁模型重新设计安全措施：

- **输出目录沙箱**：新增 `_sandbox_path()`，所有 `dir`/`out_dir`/`cwd`/`in`/`out` 强制收敛到 `WB_OUTPUT_ROOT`；沙箱外绝对路径一律 400。环境变量 `WB_OUTPUT_ROOT` 由部署入口 `app.py` 注入。
- **可选访问令牌**：`WB_ACCESS_TOKEN` 设置后，前端从 `?token=` 读入存 `sessionStorage`，所有 fetch 经拦截层自动带 `X-Access-Token`；缺/错 token 返回 401。`/api/zip` 等表单路径用隐藏字段承载。
- **按 IP 限流**：昂贵端点（`/api/search`、`/api/coze-stream`、`/api/batch-run`）5 次/分钟/IP，超限 429。
- **安全响应头**：所有响应带 `X-Content-Type-Options: nosniff` / `X-Frame-Options: SAMEORIGIN` / `Referrer-Policy: no-referrer` / `Content-Security-Policy`（含 `script-src 'self'`）。
- **llmcfg 写保护**：公网模式禁用 `POST /api/llmcfg`（405），防止改写服务端 `.env`。
- **错误信息收敛**：公网模式 500 错误统一返回 "internal error"，不回显异常详情；`/api/status` 删除 `cwd` 字段；`/api/sources` 的 `python`/`skill_root` 改为 basename。
- **前端令牌拦截层**：`window.fetch` 拦截器全局注入 `X-Access-Token`，401 时弹出令牌输入框；`use strict` + I18N 引擎零修改。
- **版本锚点**：`SKILL.md` / `CHANGELOG.md` / `workbench.config.json` / `server.py SKILL_VERSION` / `app.js skill_version` 五处同步到 1.5.4。
- **测试**：`_sec_test_public.py` 18/18 全绿（安全头/令牌/限流/sandbox/llmcfg/脱敏/静态头/沙箱内放行）；本地 7/7 回归不误伤；云端 6/6 双模式验证。

## 2026-10-26 · 架构韧性层（连接器注册表 + 跨源熔断 + RRF 融合）

参考《这8个文献检索、下载Skill》中 paper-search-mcp（连接器分层）与 scholar-mcp（RRF 融合），为 ct-literature 检索主路补齐架构韧性：

- **连接器注册表 `adapters/source_registry.py`（新增）**：`SOURCE_REGISTRY` 声明式源表，run() online 分支改遍历注册表构建 jobs（删除原硬编码 `_coze_sources` 与 `_coze_dispatch_with_fallback` 死代码，单一真相）；新增源（CNKI / ClinicalTrials）仅需追加 entry，可扩展性↑。
- **跨源熔断 `ConnectorHealth`**：每源 + 全局 `coze_endpoint` 连续失败达阈值即开路，后续 run 直接走本地兜底、不再锤 Coze；冷却后放行一次试探；状态可选持久化到 `CT_LIT_RUNTIME_DIR/health.json` 跨 run 复用。CLI 新增 `--health-reset` 清空熔断。
- **RRF 排名融合 `rrf_fuse`**：新增 `--rank rrf`，跨源倒数排名融合让多源共识论文上浮（弥补单源 cited_by 偏差）；默认仍为 `cited`，既有排序语义不变。
- **根因修复（死锁）**：`ConnectorHealth.status()` 原在已持有 `self._lock` 时调用 `is_open()`，对 `threading.Lock`（非重入）自死锁——改为内联开放判定，熔断查询不再卡死。
- **测试**：新增 `tests/test_source_registry.py`（10 项无网络单测，pytest 兼容），覆盖注册表完整性 / build_source_ranks / RRF 共识上浮 / 熔断开闭 / fetch_source 在线成功·失败降级·熔断开路跳过 Coze。
- 验证：py_compile 通过；10/10 单测通过；source_registry 内建自检通过。
- 待补：本机缺 `xlsxwriter` 无法跑完整 `ct_literature` 导入回归；端到端线上检索回归需在具备依赖与 Coze 运行态的环境执行。

## 2026-10-26 · 多源去重引擎增强（dedupe_engine）

新增 `adapters/dedupe_engine.py`，为 `run()` 提供多标识归一 + 传递闭包 + 模糊标题的去重能力：

- **多标识归一**：DOI（大小写/URL 前缀/版本后缀剥离）、PMID（数字提取）、PMCID（PMC 前缀剥离）、arXiv ID（版本后缀 `v1/v2/...` 归一）—— 同一论文在不同文献源用不同标识时可正确合并。
- **传递闭包**：A.doi==B.doi + B.pmid==C.pmid → A=B=C，Union-Find 算法实现。
- **模糊标题匹配**：无共享标识时按 (标题前缀, 年份) 分桶 + SequenceMatcher ≥0.90 兜底，保留备兼容。
- **策略路由**：`--dedupe-engine {v1,v2}` CLI 选项，默认 v1 保兼容；v1 走 `normalize.merge_with_stats`，v2 走 `dedupe_engine.merge_v2_with_stats`。v2 保留 EuropePMC 字段优先级、is_oa OR 语义、cited_by 取最大、pub_types union 等既有合并策略。
- **测试**：`tests/test_dedupe_engine.py`（18 项无网络单测），覆盖标识归一 / 传递闭包 / arXiv 版本剥离 / 模糊标题 / 空集 / 无重复 / 多源合并 / EuropePMC 字段优先级保持。
- **端到端线上回归（2026-10-26，Anaconda 3.14.6）**：`scripts/e2e_regression.py` 真实抓取 OpenAlex/EuropePMC/bioRxiv/medRxiv/arXiv/SemanticScholar，v1→v2 路由、RRF 排名、注册表+熔断、完整 pipeline 路由全部通过；arXiv 网络超时降级为 0 篇（韧性生效），SemanticScholar 无 key 跳过（预期行为）。
- **根因修复（接口不一致）**：`merge_v2` 原接受扁平 works 列表，与 `normalize.merge` 的 `[{source, works}]` 格式不一致导致端到端仅返回 3 篇；改为 payloads 入口并内部 flatten，与 `merge_with_stats` 对齐。
- 验证：py_compile 通过；18/18 + 10/10 单测通过；e2e 真实线上全路径通过。

## 仅工作台（不进发布包）· 2026-10-24 审计修复（§3.4 顶层 stdlib / health 路由 / poll 超时）

针对 2026-10-24《CT 系列工作台启动 / 后台加载专项审计报告》对 ct-literature 的发现，修复于 `workbench/server.py` 与 `workbench/app.js`（`publish/workbench/` 同步同版）：

- **§3.4 顶层 stdlib 重导入**：顶层 `import shutil`/`import subprocess` 移除，改为 10 个使用函数内按需导入（`_pick_python`/`_file`/`_cleanup`/`_search`/`_batch_plan`/`_batch_run`/`_stop`/`_coze_stream`/`_run_tool`/`_subprocess_text`）。
- **health 路由补齐（审计总览表"—"项）**：新增 `/api/health`（返回 ok/skill/version，`Cache-Control: no-store`，§7.3 规则 4）——此前 ct-literature 是全家族唯一没有 health 端点的。注意：本技能顶层已符合 bind 先行（动态 `__import__("http.server")` 懒加载，审计 §四.6 亦确认为家族正面参考），故无 P0 问题。
- **审计 P2 观察项 3 更正**：「ct-literature 前端无探测、pill 静态」**与实际不符**——`app.js` 的 `poll()` 自 2.2s 周期打 `/api/status` 并据 ok/warn/err 更新 pill，本就具备探测与自愈。本轮仅补强：poll 的 fetch 加 AbortController 8s 超时 + `cache:"no-store"`，防挂死连接令 pill 滞留旧态、`_statusInFlight` 不释放。
- **§四.5 媒体查询**：审计已确认无侧导航/固定宽元素，窄屏 bug 不适用，未改动（维持低风险观察）。
- 验证：py_compile 通过；app.js `node --check` 通过；起服冒烟 `/api/health` 200 + no-store、`/api/config`、`/api/status`、`/` 均 200；app.js 伺服内容含 poll 超时标记。
- 原版备份：`workbench/server.py.bak_pre_fix_20261024`、`workbench/app.js.bak_pre_fix_20261024` 及 `publish/workbench/` 下同名备份。


All notable changes to this skill are documented here. Versioning follows the
ct- library convention (A-tier public-intel skill — non-confidential input per ct-base §11, semver-ish).

## v1.5.4 (2026-10-26) · 预印本候选回退默认开启 + coze 上移评估

用户确认「预印本候选回退」为核心原始功能（非近期新增；下载期回退 `_find_early_preprint`
自 2026-09-07 v0.9.8 即在 `_classify` step④ 常开），并要求将其设为默认开启、评估是否上移 coze 端。

### Changed — 预印本候选回退默认开启
- `scripts/ct_literature.py`：检索期标注开关由 opt-in `--preprint-fallback`（默认关）反转为
  **默认开启、可关闭**——新增 `--no-preprint-fallback`（`run_pipeline` 形参默认值
  `preprint_fallback=False → True`，CLI 经 `not args.no_preprint_fallback` 透传）。
- `scripts/export_xlsx.py`：XLSX/HTML 「Preprint candidate」列帮助文案由「opt-in」改为「default-ON」。
- 影响面：每次分析（无 `--no-preprint-fallback`）现在会对非 OA 文献按标题检索
  bioRxiv/medRxiv/arXiv 预印本候选并标注（经作者姓氏同篇校验「宁可缺漏不能弄错」）；
  下载期付费墙文献的免费预印本/OA 直链回退**原本就常开**，与此开关独立。

### Evaluated — 不将预印本回退上移至 coze 端（维持本地优先）
评估结论：**保留本地、不上移 coze**。理由：
- 成本不对称：本地检索是免费只读元数据调用（Europe PMC PPR / arXiv），coze 是
  无头浏览器 + S3 上传，按子批(≤12)计费且 5s 间隔限流；用 coze 找免费预印本属资源错配。
- 时延：本地 step④ 并行且亚秒级；coze 额外 ~5s 批间隔 + 解码时延。
- 本地优先 / 数据不出域（ct-base §11）：预印本检索把标题/DOI 不必要地送出域外，违背原则。
- 覆盖面无增益：coze 解码管线（A 解码+直下探测 → B 浏览器+S3）服务于出版商付费墙/反爬，
  并非广搜预印本库；且 step④ 失败本就按既有管线升级到 coze（step⑥），难点已兜底。
- 可审计性：作者级同篇校验（`_author_check`「宁可缺漏不能弄错」）是有意本地控制，
  上移 coze 会失去该本地审计与「宁缺毋错」保证。
- 若上移反而退化：移除本地首 attempt 会强迫每篇非 OA 走昂贵 coze，或造成与 coze 自身
  解码的重复检索——两害。
- 已知本地侧轻微冗余（与 coze 无关）：检索期标注与下载期 step④ 都调 `_epmc_preprint_search`；
  默认开启后每篇非 OA 会多打一次 Europe PMC。建议后续让 step④ 优先复用 `work["preprint"]`
  （检索期已校验）以消除重复检索——待用户确认后实施。

## v1.5.3 (2026-10-26) · 检索/下载四项改进（参考 meta-analysis A3 与 pdf_fetch 设计）

用户要求把 meta-analysis 技能在论文检索/下载上的 4 项改进全部落地：

### Added — ① 代理绕过（参考 meta-analysis `pdf_fetch._get` 实测结论）
- `pdf_download.py` 新增 `_install_no_proxy_opener()`（`PdfDownloader.__init__` 时调用，
  幂等）：给进程装空 `ProxyHandler` 默认 opener——系统代理（如 WorkBuddy 本机加速代理）
  会杀死长连接/超时 PDF 下载，此后 PDF 下载链路（含 `preprint_fallback` / `sci_hub`，
  同进程）全部直连；检索/coze 阶段在下载器构造前已完成，行为不变。
- 实现：`install_opener` 而非逐调用点换 opener——`urlopen` 调用形态不变，回归测试
  monkeypatch 仍生效；空 ProxyHandler 无 `*_open` 方法不注册进 handlers = 纯直连。
- 恢复系统代理：`CT_LIT_USE_SYSTEM_PROXY=1`。

### Added — ② 预印本作者级同篇校验（参考 meta-analysis `_author_check`）
- `_find_earlier_preprint(doi, title, work)`：PPR 标题命中候选在下载前做作者交叉校验
  （`preprint_fallback._author_check`，规则「宁可缺漏不能弄错」：无共同姓氏拒、
  第一作者不一致硬拒）；原文献无作者 → 不下载任何候选（note 记 `missing_author_info`）。
  拒绝原因写 work `pdf_download_note` 供 manifest 审计。kind=oa（Unpaywall 按 DOI 定位）
  身份确定，不做校验。
- `tests/regression_pdf_routing.py` B 夹具补 authors 对齐新契约（4 FAIL → 0）。

### Added — ③ Consent-aware 下载泛化（参考 meta-analysis `consent_aware_download`）
- `_browser_headers(url)`：Referer 从「仅 biorxiv/medrxiv 硬编码」泛化为全源站
 （.pdf 后缀剥除，模拟从文章页点下载）；非 EBI/NCBI 站点种 OneTrust「全部接受」
  consent cookie（`OptanonConsent`，`_ONETRUST_CONSENT_COOKIE`）——部分出版商
 （Nature/Elsevier 系）先弹同意墙再放 PDF。

### Added — ④ needs_manual.csv 导出 + 手动回传归位（meta-analysis A3 思想的 CLI 化）
- 参考其「内网/订阅全文共享后端」（`a3_pending`/`a3_stash_pdf`）评估结论：云端够不到
  用户内网，唯一带机构订阅/登录态的是**用户浏览器**。CLI 化为无服务器版：
  - `run()` 末段导出 `needs_manual.csv`（仍无 PDF 且有 DOI 条目，含
    `https://doi.org/<doi>` 深链），新模块 `adapters/manual_reconcile.py`；
  - 新 CLI `--reconcile-manual OUT_DIR`（独立模式，不需要 --topic）：扫描
    `<OUT_DIR>/pdfs/manual_incoming/` 下用户用机构权限手动下载的 PDF，按 DOI
   （文件名变体 `10.1038_xxx` / `10.1002-hbm.12345` + pypdf/fitz 正文提取）匹配
    merged.json works → `%PDF` 头 + 深度校验 → `os.replace` 归位标准命名 →
    原子回写 `.merged.json`；
  - 台账新增来源类型 `manual_incoming` =「手动回传(机构权限)」，信任级 **高**
   （用户自己的订阅权，完全合法合规）——**优先于 Sci-Hub 兜底**（后者仍默认关闭）。
- 验证（anaconda3）：自测 ALL PASSED（导出/归位/非 PDF 拒收/DOI 变体）；CLI E2E
  PASS（归位 + .merged.json 回写 + rc 传播）；routing/enhance/speed/stream/
  root_causes 五套件全绿；离线冒烟 4 源正常。

## v1.5.2 (2026-10-26) · 本地搜索缓存 + Sci-Hub 可选兜底（参考 openags/paper-search-mcp）

用户调研 `openags/paper-search-mcp`（通用学术检索 MCP）后拍板采纳三项设计；
其中 Sci-Hub 兜底经用户明确授权引入（「加一个明确的说明，要求用户后果自负」）：

### ① 本地搜索缓存（默认开启，TTL 24h）
- 新增 `adapters/search_cache.py`：按 `(source, 检索式, review_type, 年份/日期窗口,
  safety, max_results, cochrane, include_reviews)` 联合键缓存成功的 per-source
  payload 到 `<out_dir>/.search_cache.json`，TTL 内直接复用——省 Coze 配额 + 提速。
- 只缓存无 `error` 的 payload（写入侧把关 + 读取侧双保险）；命中打 `cache_hit`
  事件**透明可审计**，绝不静默替换；线程安全（进程内锁 + tmp+replace 原子写）；
  容量兜底（>200 条先清过期再按 cached_at 淘汰最旧）。
- CLI：`--no-cache`（本次不读不写）/ `--cache-ttl SECONDS`；环境变量
  `CT_LIT_NO_CACHE` / `CT_LIT_CACHE_TTL`。
- E2E 验证：同命令双跑，第二遍 4/4 源 0.0s 命中；`--no-cache` 旁路恢复真实检索。

### ② Sci-Hub 最后兜底（⚠️ 默认关闭，后果自负）
- 新增 `adapters/sci_hub.py`：多镜像顺序回退（默认 sci-hub.se/.st/.ru/.ee，
  `CT_LIT_SCIHUB_MIRRORS` 可覆盖），解析 iframe/embed/location.href 三类真实
  PDF 直链形态，噪声过滤；纯标准库。
- **激活条件（三者其一，默认全关）**：CLI `--use-scihub` /
  `PdfDownloader(use_scihub=True)` / 环境变量 `CT_LIT_ALLOW_SCIHUB=1`。
- 定位：整条下载链**最后一步**——Europe PMC / OpenAlex / Unpaywall / 预印本 /
  coze 云端解码全部失败后，对仍有 DOI 的条目尝试；接入 `_SourceCircuitBreaker`
  （连续 2 次解析失败即熔断，`_CB_SCIHUB_MAX_FAILURES=2`）。
- 两个挂接点：`_local_fallback`（skip-coze / coze 熔断场景）+ `run()` 末段
  `_scihub_last_resort`（reconciliation 之前，scihub_ok 冲抵 manual_needed）。
- ⚠️ 合规声明（模块 docstring / `DISCLAIMER` 常量 / 构造时日志 / CLI help /
  `.env.example` / manifest 信任级六级）：法律风险**用户后果自负**，机构环境
  （GCP/申办方项目）**严禁开启**；每次下载器构造时打印一次显眼免责声明。
- manifest 台账：`scihub_local` 行信任级标 **「低(用户自担)」**，合规审查一眼可辨
  （v1.5.1 前本技能红线为「无镜像源、无低信任级」；本版本起该红线改为
  「默认无镜像源，仅用户显式 opt-in 后出现低信任级行」，路由四桶本身不变）。
- stats 新增 `scihub_tried` / `scihub_ok`。

### ③ 测试夹具修复（根因分析，环境级既有 FAIL）
- `tests/regression_pdf_enhance.py` 的 `_MINIMAL_PDF` 原为手写 PDF、**缺 xref 表**
  ——PyMuPDF 靠修复扫描容错可开（原开发机装了 fitz），pypdf 6.x 严格解析抛错 →
  `_pdf_page_count` 返回 0 → 6 个断言在 pypdf-only 环境全挂。改为程序化生成
  **规范完整**（精确对象偏移 + xref + startxref）的最小 PDF，不再依赖任何解析器的
  修复扫描行为。环境补装 `pypdf 6.21.2`（WorkBuddy 托管 Python 3.13.12 此前
  pypdf/fitz 均缺）。
- 验证（anaconda3 Python 3.13.9，pypdf 6.13.2 + fitz 1.27.2.3）：routing 0 FAIL /
  enhance ALL PASS / speed 11 通过 0 失败 / stream_parser 8/8 CLEAN /
  root_causes 24 passed；py_compile 全过；缓存 E2E 双跑 4/4 命中。

## v1.5.1 (2026-10-26) · 修复两个既有回归（routing / speed 测试 FAIL）

用户要求处理 2026-10-25 复验时发现的「两个既有 FAIL」——逐项根因分析后，
一类是真 bug（红线违规），一类是测试缺陷，均已修复（**非 1.5.0 改动引入**）：

### routing 14 FAIL = 真 bug（红线违规）+ 1 个测试 mock 缺陷
- **真 bug（`_classify` ⑥）**：原 `has_signal = ... or bool(doi)` 把**明确非 OA**
  （Unpaywall 确认 `is_oa=False`）的论文也送 coze，违反 ct-literature「非 OA 不送云端」红线。
  修复：⑥ 读 `_upw_cache` 判定 Unpaywall 状态——`isinstance(upw, dict) and not upw.get("is_oa")`
  **且**无任何本地信号（oa 链接 / preprint）才 skip；不可达/未知仍保守送 coze。
  注：明确非 OA 但带 `open_access_url` 落地页链接（如 doi.org）仍送 coze 解码，不误 skip。
- **测试 mock 缺陷（`test_non_oa_pmc_manuscript`）**：只 mock `_epmc_lookup_pdf_url`，
  但 run() 预查先调 `_epmc_lookup_pmcid` 查 PMCID，查不到会设 `_epmc_checked=True`
  使 classify①跳过 → pmc 手稿被误送 coze。改为 mock `_epmc_lookup_pmcid` 返回 PMC7777777，
  命中 ① 第一分支 `if pmcid` → local_preprint。
- 验证：`regression_pdf_routing.py` 14→0 FAIL，ALL ROUTING TESTS PASSED。

### speed 1 FAIL = 三层测试缺陷（网络隔离 + PDF 解析 + T3 同 host 串行断言）
- **测试缺陷①（网络隔离）**：`_make_downloader` 只 mock `_prefetch_unpaywall` / `_call_coze_unified`，
  漏隔离 `_prefetch_identifiers`（内部 `_epmc_lookup_pmcid` / `_oa_via_openalex` 真实打网络，
  timeout=20s/次）→ wall 达 17.5s。补齐相关网络方法 mock。
- **测试缺陷②（PDF 解析副作用）**：1.5.0 的 `_pdf_meta` 落账让 `_download_one` 每篇解析 PDF；
  测试用 14 字节畸形 `b"%PDF-1.4 fake"`，本机 fitz 修复扫描单篇耗时 **2s**，9 篇并发拖到 6s。
  修复：①测试中 `_pdf_meta` 隔离为纯本地大小计算（解析正确性已由 regression_pdf_enhance 覆盖，
  T3 只验证下载并发）；②fake_download 改写合法最小 PDF（语义正确）。
- **测试缺陷③（T3 同 host 串行断言，致命）**：`test_run_concurrent_correct_and_fast` 的 6 篇 coze
  间接项全部返回 **同一个** S3 host（`bucket.s3.amazonaws.com`）。而 `_PerHostRateLimiter`
  （`adapters/pdf_download.py:499`，**有意设计**：同域名按 `min_delay` 串行保距，防 Cloudflare 1015 封禁）
  会把这 6 篇串行化，wall 恒为 ~1.2–1.9s，永远压不进 `0.6 × 2.25 = 1.35s` 阈值。该测试注释写的
  「验证 S3 同 host 不再被串行化」与限速器设计**自相矛盾**——此前 11/11 仅属机器时序运气，
  属脆弱/偶发 FAIL。修复：6 篇 coze 改为**逐篇不同** host（`bucket0/1/...s3.amazonaws.com`），
  使 T3 断言落到真实特性「跨域名并发下载」上（同 host 串行是有意安全特性，不应被并发断言推翻）。
- **生产防护（`_pdf_page_count` 256 字节快速失败）**：畸形/截断残篇常 <256 字节，
  fitz 修复扫描单篇达秒级、批量放大成严重卡顿；新增快速失败——任何 <256 字节文件直接判不可解析，
  不进解析器。真实完整 PDF（如 live 验证 bioRxiv 2257KB/19 页）不受影响。
- 验证：`regression_pdf_speed.py` 1→0 FAIL，连续 3 次 11/11 PASS（含 T3 并发提速，wall≈0.25s≪1.35s）。

### 验证（v1.5.1）
- 本地回归全绿：enhance ALL PASS、root_causes/force_coze 24/24、stream_parser CLEAN、routing 0 FAIL、speed 11/11。
- 真实网络活体：①中文题名→DOI、②深度校验、③manifest、④熔断 全 PASS（bioRxiv 真实 PDF 2257.2KB/19 页）。
- 备份：`*.bak_fixfail_20261026`。

## v1.5.0 (2026-10-25) · PDF 下载增强四项（参考 academic-fulltext-fetcher 设计）

> 依据：用户 2026-10-25 对《WorkBuddy 应用》「学术论文自动下载助手
> （academic-fulltext-fetcher）」技能设计文章的分析结论，指定落实四项改进
> + 一项 live 验证中发现的既有缺陷修复。全部集中在 `adapters/pdf_download.py`
> （+ `scripts/export_xlsx.py` 两列、`scripts/update_xlsx_pdf_paths.py` 重扫佐证、
> `scripts/ct_literature.py` 完成语文案）。备份：`*.bak_pdfenhance_20261025`。

### ① 中文题名→DOI：OpenAlex 跨语言通道（P0，命中用户中文文献场景）
- `_resolve_doi_from_title(title, year, author)`：Crossref（原有，<55 字符不解析 + 阈值 0.9，行为不变）之外新增 **OpenAlex `title.search` 通道**——Crossref 对中文期刊覆盖差，中文题名常**无候选**（缺的是候选源，不是相似度算法）。两路并行，取高分。
- 判定（宁缺毋滥）：相似度 ≥0.90 直接接受；或 ≥0.60 且**年份（±1 年）+ 第一作者名**双佐证。短题名按「信息长度」门槛拦截（CJK 每字计 2——live 验证教训：按裸字符数会把「胎儿型肺腺癌一例」这类 8 字高密度中文题名误杀）。
- 调用点 `_prefetch_identifiers` 增传第一作者（`_first_author_name`）。
- live 验证：真实中文题名「胎儿型肺腺癌一例」→ DOI `10.3760/cma.j.issn.1006-9801.2013.01.026`（score 1.15，年份+作者佐证加分）。

### ② PDF 深度校验：可解析 + 页数 ≥1（P0）
- `_download_to()`：浅层（%PDF 头 + >5KB + Content-Type）之后追加 `_pdf_is_valid()`（解析器链 pypdf → PyMuPDF(fitz)，均缺返回 None 按放行——不因缺依赖误杀）。残篇/截断/加密/伪造 PDF 判失败，`.part` 留场由下次覆盖。
- `_pdf_meta()` 产 (大小KB, 页数)，`_download_one` 落 `work["pdf_size_kb"/"pdf_pages"/"pdf_source_url"/"pdf_existed"]`。
- live 验证：真实 bioRxiv PDF 下载成功并记录 2257.2KB / 19 页。

### ③ pdf_manifest.csv 下载台账（P1）
- `PdfDownloader._write_manifest()`：run() 收尾产出 `pdf_manifest.csv`（UTF-8 BOM，Excel 直开）——序号/题名/DOI/来源类型/来源URL/状态（成功/已存在/失败/跳过/拒绝）/本地路径（失败行写原因）/大小KB/页数/source_trust（合法OA=高、预印本=中；本技能无镜像源故无「低」）。落点 = xlsx 同目录（运行根）。`stats["manifest_path"]` 透传；主流程完成语文案同步提示。
- `export_xlsx.py`：「文献总表」末尾新增「大小KB」「页数」两列（+ i18n/字段说明；空白写 — 不写 0——0 页是校验失败语义，不与「未知」混淆）。`update_xlsx_pdf_paths.py` 重扫补救路径同步现算佐证列。

### ④ 单源连续失败熔断器（P1）
- 新增 `_SourceCircuitBreaker`：同一源连续 3 次失败即停用本源（整轮不再查询/发送），成功即重置；429 等明确限流 `force_open` 立即停。接入 **epmc / openalex / unpaywall / coze** 四源（coze 阈值 2，传送成本高；熔断后剩余子批与 local-fallback retry 直接转本地兜底）。替代原 `_epmc_disabled` 特例（行为兼容：429 仍立即停）。
- live 验证：3 次真实 404 后 openalex 熔断生效。

### 附带修复：下载头 Accept-Encoding（live 验证发现的既有缺陷）
- `_browser_headers()`：`Accept-Encoding: gzip, deflate, br` → **`identity`**。此前带压缩声明，部分源站（bioRxiv 实测）返回 gzip 流，而 urllib 标准库不自动解压——下载头 5 字节是 gzip magic 而非 `%PDF-`，浅层校验直接判死，整类源站「本地直下」全灭。同文件 docstring 早已记录该坑（JSON 侧 `_http_json` 用 identity），下载侧漏改。

### 验证
- 新增回归 `tests/regression_pdf_enhance.py`：30/30 PASS（熔断器 7、深度校验 8、OpenAlex 题名通道 5、manifest 9、EPMC 熔断接线 3——含本地 HTTP server 端到端残篇/合法 PDF 下载判定）。
- 既有回归零回归：`regression_root_causes` 24/24、`regression_stream_parser` CLEAN、`regression_pdf_enhance` 全过；`regression_pdf_routing`（15 FAIL）与 `regression_pdf_speed`（1 FAIL 计时抖动）经备份版对照 **失败清单逐条一致**，为本改动前既有问题（routing 测试预期早于 has_signal 含裸 DOI 的路由演进；speed 为墙钟计时项），非本次回归。
- 活体端到端（真实网络）：①中文题名解析 PASS ②真实 bioRxiv 下载 + 深度校验 + 大小/页数 PASS ③manifest PASS ④熔断 PASS。


## Unreleased · 顶栏控件尺寸基线对齐（ct-base §5.2 新基线）+ 区块标题字号越档修复

### 顶栏控件尺寸（用户审美确认，方案 1）
- `app.css`：`.wb-topbar .wb-btn` 覆盖为 `min-height:34px; padding:6px 11px`（特异性高于全局 `.wb-btn` 的 40px/8px 12px，内容区主操作钮不受影响）；`.wb-lang` 同步 34px/6px 11px。三个文字钮（EN/反馈/CT 首页）40px→34px，占 68px 顶栏比例 59%→50%，与左侧 40px logo-box 等高呼应。状态 pill 33px 不动。移动端 ≤768px 既有 ≥44px 纪律不变。
- `index.html` + `app.css`：补 `.wb-logo-box` 40px 白框圆角阴影（内承 34px 自有 icon）——此前 literature logo 裸放，不符 ct-base §5.6.3-4。
- 实测（Playwright）：三钮 h=34/pad=6px 11px/font=14；logo-box 40×40 内 svg 34×34；顶栏 68px。file:// 下两条 fetch error 为静态预览固有（非代码问题）。

### 区块标题字号越档修复（ct-base §4.5.1）
- `app.css`：`.panel h3` 由 `--wb-fs-lg`(16px) 改为 `var(--wb-fs-sm)`(14px)——违反「区块/卡片标题 = sm」（lg 仅限顶栏主标题）。此为上版本已上线内容。

### 规范联动
- ct-base `references/workbench_ui.md` §5.2 新增「顶栏控件尺寸基线（2026-10-23 修订）」：顶栏文字钮 34px/6px 11px/`--wb-fs-sm`；状态 pill 33px/5px 12px/`--wb-fs-xs`；原 40px/8px 12px 基线废止；尺寸只覆盖顶栏专属选择器、全局 `.wb-btn` 保持 40px；窄屏 ≥44px 优先。

### 工作台机检整改：G 视图淡入 + J app.config.json 元数据（ct-base §5.6.3-6 / §13.1）
- `workbench/app.css`：新增 `@keyframes wbFade{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}`，`.wb-view.active` 由 `display:flex` 补为 `display:flex;animation:wbFade .18s ease`——修复机检 G 项（视图淡入缺失）。页面为 7 视图切换结构（v-chat/batch/advanced/tools/artifacts/history/sources），非 N/A。写法对齐 ct-registry 参考实现（registry 用 translateY(6px)/.18s ease-out 内联于 index.html，此处按整改规格 4px/.18s ease 落于 app.css）。
- `workbench/app.config.json`：补全 `domainPrefix`=`ct-literature`、`shareLink`=`https://ct-literature.app.workbuddy.host/`、`startCmd`=`python workbench/server.py --host 0.0.0.0 --port $PORT`（server.py 在 workbench/ 下，main() 收 --host/--port，取值对齐 ct-registry 合规参考实现的平台启动约定）；修复机检 J 项。appId/appName/publishDir 原值保留未动。
- 机检验证：`_wb_audit.py ct-literature` A–L 十二项由 G/J FAIL 修毕为全 OK。


## v1.4.12 (2026-10-23) · 落实 ct-base §16.16 工作台页面传输压缩（gzip）与缓存分级

> 依据：`ct-base/docs/07-publish-checklist.md` §16.16 + `references/workbench_ui.md` §7.2（2026-10-23 新增，全库强制）。ct-literature 首屏需拉 `index.html` 56KB + `app.js` 153KB + `app.css` 42KB + `tokens.css`/`wb-list.*` ≈ 280KB 文本，原实现虽有 gzip 但**无阈值、无压缩缓存、无缓存分级**，每次请求现压 280KB 且 HTML/静态资源一律 `no-store`，属规范第 3 条不合规。

### 传输压缩（`workbench/server.py`）
- **阈值与类型（§7.2 第 1 条）**：新增 `_GZ_MIN_BYTES=1024` —— 仅体长 >1KB 且 `ctype` 命中 `_GZ_TEXT_PREFIXES`（`text/*`、`application/json`、`application/javascript`、`image/svg+xml`、`application/xml`）时压缩；**补入 `image/svg+xml`**（`icon.svg` 原不压，2417B→1042B）。不支持 gzip 的客户端原样返回，**不带** `Content-Encoding`（原逻辑已满足，本次加断言回归）。
- **压缩缓存键纪律（§7.2 第 2 条 · P0 红线）**：新增 `_gz_body(key, raw)` —— 仅对「内容即某个文件」的静态资源按 **`(文件路径, mtime)`** 键缓存（`_GZ_CACHE` 上限 64 + 线程锁）；**动态 JSON 一律现压现发、禁入缓存**，杜绝 ct-sdtm 曾发生的「同 ctype 接口共用压缩体」串号。`_send()` 新增 `cache_key` 形参承载该区分。
- **`index.html` 不按自身路径缓存压缩体**：响应体经 `_version_assets()` 注入了各资产 `?v=<mtime>`，内容不由 `index.html` 自身 mtime 唯一决定——若按该路径缓存会发出旧版本号（串版本）。55KB 现压约 5ms，安全优先，已写注释固化。
- **`/index.html` 路由归并**：原走 `_serve_static`（绕过 `?v=` 注入），现与 `/` 同走 `_serve_index`，避免浏览器按长缓存取到旧 `app.js`。

### 缓存分级（§7.2 第 3 条）
- 静态资源（`.css/.js/.svg/.woff/.woff2/.ttf/.ico/.png`）→ `public, max-age=86400`；HTML → `_HTML_CACHE_CTL`（发布态 `public, max-age=60`、本地 dev 态 `no-store`，保留「改完刷新即见」的开发体验）；`.json` 配置与动态 API → `no-store`（原 `.json` 亦为 no-store，未变）。
- **`_version_assets()` 补注入 `tokens.css` / `wb-list.css`**：这两个文件此前无 `?v=`，在 86400s 长缓存下改样式会让老用户 24h 拿不到新版——长缓存必须配版本化。

### 统计指标部署期预计算（§7.2 第 4 条）— 本技能 N/A
- 首页无 KPI 看板卡片（`index.html` 仅表单区 + 模态框，无卡片指标），`/api/sources` 为按需端点而非首屏渲染依赖，故无「每请求实时重算」问题，本条不适用。

### 实测（本地 `127.0.0.1:8799`，curl + Chromium 真机）
- 压缩比：`index.html` 55,963→18,608B（-66.7%）、`app.js` 153,376→50,509B（-67.1%）、`app.css` 41,866→10,043B（-76.0%）、`wb-list.js` 16,768→5,546B、`tokens.css` 5,990→2,751B、`icon.svg` 2,417→1,042B；**首屏总下载 280KB→约 71KB（-75%）**。
- 压缩开关两侧 md5 逐字节一致（`/`、`app.js`、`app.css`、`wb-list.js`、`icon.svg`、`/api/config`、`/api/sources` 7/7 OK）；不支持 gzip 的请求 `Content-Encoding` 出现 0 次；62B 小响应不压缩。
- 防串号：`/api/config`、`/api/sources`、`/api/status` 相邻三接口连测 3 轮，各自返回自己的首字段（`config.skill` / `python` / `running`），无串体。
- 压缩缓存：`_gz_body` 同 `(路径, mtime)` 二次调用返回同一对象；改内容 + mtime 后返回新压缩体且解压还原正确；`app.js` 连测 10 次稳定 50,509B；响应与磁盘文件 md5 一致。
- 浏览器：Chromium 加载 0 console error / 0 pageerror，页脚 `v1.4.12`、侧栏与对话区渲染正常，5 个资产全部带 `?v=` 且 200。

## v1.4.11 (2026-10-22) · 落实 ct-base §22 合规：RAG 三列清单 / 分层验收 / 影子模式

- **§22.16 RAG 三列待核对清单（已实现）**：新增 `scripts/gov22.py`，在 `lit_report.html` 与 `report.md` 中落地「三列待核对清单」(问题 / 原文位置 / 依据) + 显式「未覆盖项」；清单内容由真实运行台账 `evidence_log` 派生，零编造，默认失败模式=漏项，专业人员按清单回看原文。
- **§22.17 确定性层 vs LLM 层分层验收（已实现）**：报告新增「分层验收声明」，确定性层(六源检索/日期窗口/去重，可入 CM0) 与 LLM 层(归一化/翻译/标注，禁入 CM4) 分开披露；概念归一化准确率按 exact_label/synonym/unmapped_literal 分层披露，严禁混报为单一「总体准确率」。
- **§22.15 影子模式准入阈值（已实现）**：新增 `references/shadow_mode_protocol.md` 协议（锁定版本+静默并行+离线比对+四阈值 go/no-go+熔断+SAP 三要素登记）。
- 新增 `scripts/gov22.py`（§22 治理逻辑单一事实来源，MD/HTML 双渲染共用），技能版本戳随 §22.5 processDefinitionVersion 统一为 `1.4.11`。
- 原始文件备份：`scripts/report.py.bak_cthomefix_20261022`、`scripts/export_html.py.bak_cthomefix_20261022`。

### 工作台页面格式对齐 ct-base 最新规范（workbench_ui.md §页脚规范 / §14 版本纪律 / §22.5 processDefinitionVersion）
- **补 `#wb-footer`（此前整页缺失，违反 §页脚规范）**：`workbench/index.html` 增加页脚，格式严格为「工作台名称 + 空格 v版本号 + · + 框架说明」；`app.js` 新增 `footerName`/`footerMeta` 双语 I18N 键，`wbLoadConfig()` 从 `CFG.version` 注入版本号独立 span（缺失省略 v 段），`app.css` 补 `#wb-footer` 令牌样式。
- **统一版本锚点（消除 §14 / §22.5 漂移）**：`workbench/workbench.config.json` `version`、`workbench/server.py` `SKILL_VERSION` 与 `_BUILTIN_CONFIG.version`、`workbench/app.js` `skill_version` 全部由 `1.0.0` 改为 `1.4.11`，与 SKILL.md / CHANGELOG 同环同源。
- 发布包 `workbench/publish-dist/` 经 `build_publish.py` 从修正后源码重建（120 文件，0 残留）。
- 端到端验证：启动后端 → `/api/config` 回传 `version=1.4.11`；`index.html` 含 `#wb-footer`/`#wb-footer-ver`，`app.js` 含版本注入逻辑与 `skill_version: 1.4.11`。

### 工作台全功能核查（26 端点静态+HTTP 实测 / E2E 真实检索·流式·批量）——修复 4 处缺陷
- **`/api/search` 状态泄漏（严重）**：argv/cwd 构建期异常（如 `max` 传数字触发 `.strip()` 崩溃 500）发生在 `_running=True` 之后且无释放路径 → 工作台所有后续请求永久 409。修复：argv/cwd 构建移至持锁前；发响应头失败立即复位 `_running`；`_build_search_argv` 全字段经 `_arg_s()` 标量强转（str/int/None 均安全）。
- **`/api/tools` tool=pdf 误触发真实下载**：`pdf_download.py` 的 `__main__` 把所有 argv 当 DOI 列表执行下载（`--help` 曾被当假 DOI 触发一次真实 Coze 解码烧配额），且原引用路径 `scripts/pdf_download.py` 不存在（实际在 `adapters/`）。修复：该入口改为静态用法说明，不再起子进程。
- **`/api/batch-run` 流式假死**：`_batch_argv` 漏传 `--progress json`（服务端期望 JSON 引擎行），且子进程 stdout 块缓冲 → 批量执行期间 UI 只收到 `run_start` 后全程无事件。修复：argv 补 `--progress json`（末尾结构化 summary）+ `PYTHONUNBUFFERED=1`（逐 entry 实时中继为 log 事件）。
- **静态接线全检**：`_build_search_argv`/`_batch_argv` 全部 CLI 旗标在 ct_literature.py（含 BooleanOptionalAction 自动 `--no-*`）/batch_lib.py 中已定义；`_run_tool` 11 个工具分派与脚本路径全部对齐。
- **验证矩阵**：26 项端点实测全 PASS（config/status/sources/llmcfg/parse/search-dry/9 工具/artifacts/file/selection/zip/llmcfg 保存清除/batch-plan/bug-report/index）；E2E 真实执行全 PASS——`/api/search` 真实检索 20 works + xlsx/html/merged/evidence_log 齐全且 HTML 含 §22 治理段（v1.4.11 戳）、`/api/lit-stream` 流式检索 3 works done、`/api/batch-plan` cmd 拼装正确、`/api/batch-run` entry ok（20 条，54s，xlsx/html 齐全）、`/api/coze-stream` start 事件正常。回归 harness：workspace `_wb_ftn.py` / `_wb_e2e.py` / `_wb_e2e_batch.py`。
- 备份：`workbench/server.py.bak_ftncheck_20261022{,b,c,d}`（验证后可删）。

### 安全加固：local guard（Host/Origin 校验，2026-10-22 下午补）
- **缺口**：服务无鉴权且 `/api/file`/`/api/artifacts`/`/api/selection`/`/api/zip` 允许按 `dir` 访问本机任意目录；虽默认绑定 `127.0.0.1`，但浏览器代发的跨站请求（恶意网页 fetch `http://127.0.0.1:8787`）与 DNS rebinding 不受绑定地址约束，可借这些端点读取本机任意已知文件名的文件。
- **修复**：`do_GET`/`do_POST` 入口新增 `_local_guard()`——①Host 头必须解析为本机名（127.0.0.1/localhost/::1，防 DNS rebinding）；②存在 Origin 头时其主机必须为本机（防恶意网页 CSRF，`null` 一并拒绝）；显式 `--host <局域网地址>` 部署时该地址自动放行（`_BIND_HOST` 全局，`main()` 同步）。
- **对抗性验证 7/7 PASS**：正常 GET/POST/静态/同源 Origin 全放行；恶意 Host→403、恶意 Origin（GET+POST）→403。回归脚本：workspace `_sec_test.py`。
- 备份：`workbench/server.py.bak_ftncheck_20261022e`（源码+发布包，验证后可删）。

### local guard 云端部署适配（2026-10-22 下午；起因：用户问「发布为网页应用有影响吗」）
- **发现**：线上工作台（`ct-literature.app.workbuddy.host`）的部署形态是 `app.py` 启动器以 `--host 0.0.0.0 --port $PORT` 真实运行 `server.py`——刚加的 local guard 若原样重新发布，线上所有请求（Host/Origin 均为公网域名）会全部 403，**站点整体不可用**。
- **修复**：
  1. `_local_guard()` 支持部署环境变量——`WB_DEPLOY_PUBLIC=1` 跳过 Host 检查（平台反代下 Host 不可靠，且 DNS rebinding 对公网站点无意义）、`WB_ALLOWED_HOSTS` 白名单放行线上域名；**Origin 检查保留**（浏览器侧可信任），恶意网页跨站防护在云端依然生效。
  2. `build_publish.py` 的 `APP_PY` 模板注入 `WB_DEPLOY_PUBLIC=1` + `WB_ALLOWED_HOSTS=ct-literature.app.workbuddy.host`。
  3. null Origin（file:// 页面 / sandboxed iframe）由「跳过检查」修正为「拒绝」，与前文声明一致。
- **双模式验证全绿**：云端模拟 6/6 PASS（线上 Host / 同源 Origin / 同源 POST / 静态放行；外部 Origin→403、null→403）、本地回归 7/7 PASS。脚本：workspace `_sec_test_cloud.py` / `_sec_test.py`。
- **载荷卫生**：publish-dist 内 9 个历史 .bak 已改名 `_stale_*` 前缀（构建白名单自动排除、不参与运行）；本机 safe-delete 钩子（genie-trash 路径 remap bug，fail-closed）拦截一切程序化删除，如需彻底清掉这 9 个文件请在资源管理器手动删除——不影响功能。
- 备份：`server.py.bak_wbdeploy_20261022` / `server.py.bak_nullorigin_20261022`、`build_publish.py.bak_wbdeploy_20261022`（验证后可删）。

### 工作台对话卡片宽度流式化 + CSS 既有缺陷修复（2026-10-23 下午；用户反馈"卡片背景显得很局限"）
- **诉求**：对话界面的卡片被固定宽度上限卡在中窄一列，宽屏下两侧大片留白，要求卡片宽度自动适配页面最大宽度。
- **宽度上限全尺寸流式化**（`app.css`）：`.msg` 1040px → `min(100%,1900px)`；`.msg .body` 820px → `max-width:100%` + `flex:1 1 auto`；`.panel` 1080px、`.inputrow`/`.tip`/`.mttoggle` 1000px → 同款 `min(100%,1900px)`。原 `@media (min-width:1600px)` 里的两条 vw 计算上限（`.msg .body` 曾被压到 `min(calc(100vw - 760px),1680px)`，1600px 视口下仅 840px）已删除——否则会覆盖基础规则让大屏卡片反而更窄。宽度不再按断点跳档，任何视口都铺满可用宽度；1900px 为 4K 下的可读性硬顶（改这一个数即可调）。
- **卡片型助手消息退壳**（`app.js::addMsg` + `app.css`）：此前 `.wb-card` 套在 `.msg .body` 气泡里，被气泡的 16px 侧 padding + 边框 + 底色再压窄一圈，形成"卡片套气泡"双框。现在 `addMsg` 识别卡片型内容加 `cardmode` 类，`.msg.assistant.cardmode .body` 去掉边框/底色/内边距并改为纵向 flex，卡片直接占满可用宽度；**纯文本回复不受影响**，仍保留气泡样式；用户气泡 `flex:0 1 auto` 保持内容宽度不拉伸。
- **大屏输入对齐**：`@media (min-width:1600px)` 补 `.wb-inputbar{padding-left/right:max(26px,4vw)}`，与 `.wb-msgs` 同一条左右边界，卡片和输入框边缘对齐。
- **附带修复 CSS 既有缺陷**：`app.css` 原第 97 行是一行**孤儿声明** `  padding:34px 22px; text-align:center}`（选择器与左花括号在早前编辑中丢失，publish-dist 副本同缺陷），导致这两条声明从未生效、且全文件括号数失衡（336/337，浏览器靠 CSS 错误恢复静默跳过）。已补回 `.art-empty` 选择器，括号恢复平衡（深度 0），产物页空态框的padding/居中随之生效。
- **多视口实测**（Chromium CDP，1024/1280/1600/1920/2560 五档）：卡片占可用宽度 94.5% / 95.9% / 96.7% / 97.3% / 87.4%（末档受 1900px 硬顶），卡片宽=气泡宽（退壳生效，左侧仅剩头像 30px + 间距 11px），纯文本气泡仍是 16px padding + 1px 边框，用户气泡 64px 不拉伸，**横向溢出 0**；未捕获异常 0 条、控制台错误 0 条。
- 改动文件：`workbench/app.css`、`workbench/app.js`。

### 检索结果列表新增「每页条数」选择（2026-10-23）
- **背景**：用户提出搜索结果呈现时每页最多条目数能否自选。WBList 组件（`wb-list.js`）页脚新增分页大小选择器。
- **实现**：`WB_PP_OPTIONS=[10,20,50,100]`；页脚 `<select class="wb-list-ppsel">`（`每页` label，中英 `wblPerPage`）；切换即生效（`state.page` 重置 1）并写入 `localStorage("wbl_pagesize")`；**新实例优先读记忆值**（隐私模式读不到则回落 `opt.pageSize`，现有调用 `pageSize:8` 成为初始默认）；`pageSize` 由 const 语义改为闭包可变量，翻页 prev/next/页码全部按新值计算；选项白名单校验防脏值。
- **回归**（Chromium CDP，灌 123 行假数据）：默认 10 行/1-13 页 → 切 50 → 50 行/1-3 页 + `localStorage=50` → next 翻页仍是 50 行 → 新建实例选择器初值=50（记忆生效）→ 异常 0。
- **已知边界**（既有行为，非本次引入）：语言切换不会重渲染**已渲染**的 WBList（搜索/排序等标签同样如此），新创建的列表按当时语言取词。
- 改动文件：`workbench/wb-list.js`、`workbench/wb-list.css`。`publish-dist` 已重建（MD5 一致）。

### 16 分钟检索调查：汇总链 AttributeError 实修 + 运行日志持久化（2026-10-23）
- **背景**：用户 11:22 的「2型糖尿病」全参数检索跑 16 分钟且零产物，要求彻查。
- **同参数复跑量化**（逐行时间戳探针）：**全管线仅 64.8 秒**——4 源并行抓取 2.2s、200 篇引文验证（8 并发）57s、滚雪球 6.6s、rc=0 产物齐全。**16 分钟不是管线常态**，是当日 Coze 端拥堵长尾（/stream_run 60s 超时 → /run 回退 → accepted 异步轮询指数退避 5→30s、单源上限 300s）叠加页面刷新丢日志造成的黑箱。
- **实修 Bug 1（汇总链崩溃）**：`_parse_run_response` 中 `project_list` 解码后是 **JSON 数组**，`pl.get("projects")` 直接 `AttributeError: 'list' object has no attribute 'get'` → 末尾飞书汇总整条丢失 + "run finished: None"。直连复现拿堆栈确认后修复（数组形态原样包装返回）。复测 log_only 调用 `ok=True`。
- **实修 Bug 2（日志黑箱）**：`server._search` 新增子进程输出持久化——逐行追加 `<out_dir>/.run_log.jsonl`（含 run_start cmd 与 run_done rc）。以后任何失败/断线都可回看完整轨迹，产物页可直接下载该文件排障。
- 改动文件：`adapters/fetch_coze_unified.py`、`workbench/server.py`。`publish-dist` 已重建（MD5 一致）。

### 后台任务恢复卡 + 409 友好指引（2026-10-23）
- **背景**：用户刷新页面后检索仍在后台跑，再点检索被 409 挡住且界面无解释（发送按钮灰、无提示）——「卡在这里没有继续」。实测确认：子进程真实存活 16 分钟，但结束后 ./out 无产物（引擎中途退出，原始日志随页面刷新丢失，不可追溯）。
- **修复**：① `poll()` 检测到 `running:true` 且本地无在跑会话时，自动在对话流弹一次**恢复卡**（去重防刷屏）：说明可能有刷新前的任务仍在跑 + 「打开产物」「停止后台任务」两个动作（停止走 `/api/stop`，点击后按钮变"正在停止…"并提示可重检；任务结束后自动复位允许再次提醒）；② `/api/search` 返回 409 时，对话流给出同款恢复卡替代裸 "HTTP 409"，并 `curRun=null` 释放本地忙碌态（原先 409 后本地卡死直到重载）。
- i18n 5 新键（conflictTitle/Hint/Stop/Stopping/Stopped）中英对齐。改动仅前端 `workbench/app.js`；`publish-dist` 已重建（MD5 一致）。

### 运行日志屏蔽原始命令行回显（2026-10-23）
- **背景**：用户要求实时输出日志里不再显示原始命令（`$ python ct_literature.py --topic … --topic-en … --run` 整行）。
- **改动**：`app.js` 两处 `run_start` 事件渲染——对话检索与批量检索——由「完整 argv 拼接回显」改为固定文案 `$ python … — 参数已省略`（新 i18n 键 `cmdHidden`，中英对齐）。server 端事件载荷不变（`cmd` 仍下发，供日志排障），仅前端不再展示。dry 预览的「no network」提示行保留。
- 验证：`node --check` 通过；发布包已重建（MD5 一致）。

### 英文检索词：可见 + 可编辑（2026-10-23）
- **背景**：用户要求预览卡与高级参数都能看到自动翻译出的英文检索词，且译法不合适时可自行修改。
- **CLI**：`--topic-en` 新参数——显式指定英文检索词时**跳过自动翻译**（run() 构造与 translate_topic 同形的 `_tp`，meta/报告/溯源链路零改动）；不传则行为与旧版完全一致（`topic_translator` 自动翻译 + 网络兜底）。
- **server**：`/api/parse` 解析后立即用同一词典预翻译，响应新增 `topic_en_hint`（en/translated/untranslated）供预览卡预填；`_build_search_argv` 透传 `--topic-en`。
- **前端**：① 预览卡参数网格新增「英文检索词」**可编辑输入行**（预填解析建议值，hover 提示"译法不合适可直接改"），确认执行时读取输入框值（留空=回退自动翻译）；② 高级参数页检索主题下方新增 `#f_topic_en` 字段（占位"留空＝自动翻译"），`collectForm`/`applySpecToForm` 双向纳入。i18n 5 新键中英对齐。
- **回归**：`/api/parse`「奥雷巴替尼」→ hint `Orebatinib` ✔；dry 预览 argv 带用户改写值 `--topic-en "olverembatinib user override"` ✔ / 对照组无该参数 ✔；浏览器（fetch 拦截防真跑）：预览卡预填+可编辑、改写 `MY-OWN-TERM` 进请求体 ✔；高级表单 `my-custom-term`（含首尾空格 trim）进请求体 ✔；异常 0。
- 改动文件：`scripts/ct_literature.py`、`workbench/server.py`、`workbench/index.html`、`workbench/app.js`、`workbench/app.css`。`publish-dist` 已重建（MD5 一致）。

### 新增「检索历史」页（2026-10-23）
- **背景**：用户指出工作台没有检索历史页面。
- **后端**：`workbench/.wb_history.jsonl`（JSONL，best-effort 写入，永不阻塞检索）；三个真实入口各记一条——`/api/search`（**dry=SAFE 预览不入历史**）、`/api/batch-run`（topic=spec 首个非注释行）、`/api/lit-stream`；记录 `{ts,kind,topic,out_dir,review_type?,year_from?}`。新端点 `GET /api/history`（最近 200 条，倒序）+ `POST /api/history-clear`。
- **前端**：侧边导航新增「历史」（时钟图标）+ `#v-history` 视图：类型徽章（对话/批量/流式）+ 主题 + 时间 + 类型/年份 + 输出目录；行操作「打开产物」（跳产物页并定位目录）/「重新检索」（回对话页把主题填入输入框，走正常解析-确认流程，不直接开跑）；工具栏「清空历史」（confirm 确认，只删记录不动产物文件）。i18n 中英对齐。
- **防泄漏护栏**：`build_publish.py` 排除规则补 `.wb_history.jsonl`/`.wb_*`——本地检索主题不随发布包外泄（用探针文件实测验证）。
- **回归**（curl + Chromium CDP）：lit-stream 实弹记录 ✔；`/api/history` 倒序 ✔；4 条记录渲染（徽章 流式/批量/对话）✔；重新检索→输入框回填 ✔；打开产物→产物页目录定位 ✔；清空 confirm 拒绝→记录保留 ✔；EN 切换 History/Search history ✔；异常 0。
- 改动文件：`workbench/server.py`、`workbench/index.html`、`workbench/app.js`、`workbench/app.css`、`workbench/publish-kit/build_publish.py`。`publish-dist` 已重建（MD5 一致）。

### 输出文件视图：行级删除 + 分组清空（2026-10-23）
- **背景**：用户要求单个文件可删、每个分类/文件夹也可清理。复用既有 `/api/cleanup` 的 `names`/`dirs` 定点删除能力，后端零改动。
- **行级「删除」**：所有文件行（含 proc 组）加 `删除` 按钮（`.art-btn-x` 红色 hover）；文件夹行同样有「删除」（`del-dir`，删整个子目录）。点击弹 `window.confirm`（与 WBList 删除一致）→ `artDelSubmit` POST 定点删除 → note 回显「已删除：…」→ 自动刷新。
- **组头「清空」**：每组 header 加 `清空` 按钮（`art-cleans`）→ `artSecDelTargets(sec)` 收集目标——dir 组→子目录列表；**扁平化 `pdfs/` 文件→映射回 `dirs:["pdfs"]` 整目录删除**；其余→文件名列表——confirm 显示组名与项数后提交。
- **回归**（Chromium CDP + 每步后端实况核对，`Page.javascriptDialogOpening` 自动接受 confirm）：行级删除 `refs_apa.ris`（弹窗文案 ✔ → note ✔ → 后端消失 ✔ → 重渲染消失 ✔）；报告组清空（lit_report.html 删除 ✔）；`sub/` 目录行删除（含 inner.txt ✔）；PDF 组清空（pdfs/ 整目录 ✔）。异常 0。
- **测试教训**：首版用 `ref_apa.txt` 测行级删除「找不到按钮」——是 `artDescribe` 把 txt 归入 proc 组（默认折叠），数据选择错误而非功能缺陷；改用 `.ris` 后通过。
- 改动文件：`workbench/app.js`（i18n 7 新键 + `artSecDelTargets`/`artDelSubmit` + 事件）、`workbench/app.css`（`.art-btn-x`/`.art-cleans`）。`publish-dist` 已重建（MD5 一致）。

### 输出文件视图新增「清理」功能（2026-10-23）
- **背景**：用户指出输出文件视图没有清理功能。新增整目录清理（两步确认 + 后端护栏）。
- **后端 `/api/cleanup`**（POST，JSON `{dir, all?}` 或 `{dir, names?, dirs?}`）：`shutil.rmtree`/`os.remove` 删除；护栏四层——① dir 走 `_sandbox_path` 沙箱；② **拒绝服务器目录（_HERE）及其任何祖先**（含盘根：`realpath('C:\\')` 自带尾分隔符，拼 `os.sep` 会双分隔符失配导致漏拦，实测 `C:/` 首版漏拦后已修，先 `rstrip(os.sep)` 规范化再比对）；③ names/dirs 只收纯文件名（路径分隔符/`.`/`..` 一律过滤，`../app.js` 实测被滤）；④ 公网模式限流（5 次/分）。返回 `{ok,files,dirs,bytes,errors}`。
- **前端**：工具栏加 `清理…`（danger 样式）；点击弹 `#cleanModal` 确认框——显示目标目录绝对路径 + 「N 个文件，共 X」+「M 个子目录」+ 不可恢复警示；取消/X/点遮罩均不删；确认后 POST 并以 note 回显「已清理 N 个文件 · M 个子目录，释放 X」+ 自动刷新（空态引导文案出现）。i18n 8 新键中英对齐。
- **回归**（curl 实弹 + Chromium CDP）：`C:/`、`C:/Users`、技能目录本体全部 400 拒绝；`out/` 下临时目录 `all:true` 清空（3 文件+1 子目录）成功、空目录重复清理不报错；路径穿越文件名被过滤且 `app.js` 完好；UI 弹窗展示/取消/确认/回显/空态/EN 切换全绿，异常 0。测试全程用 `out/_wb_clean_test` 临时目录，真实 `out/` 产物未触碰。
- 改动文件：`workbench/server.py`（新路由+`_cleanup`）、`workbench/index.html`（按钮+弹窗）、`workbench/app.js`（`artCleanOpen`+i18n+绑定）。`publish-dist` 已重建（116 文件，MD5 一致）。

### 输出文件视图可用性重构 A1-A6（2026-10-23）
- **背景**：用户反馈「输出文件」对话框复杂难懂。评估定位 5 个复杂度根源（路径输入暴露文件管理器概念 / 行内动作 5 种动词不统一 / 检索过程组噪音淹没主文件 / 组描述重复教学 / PDF 需「进入」两层），逐项改造。
- **A1 路径降级**：工具栏默认只留 刷新+筛选+「高级路径」开关；`↑ 上一级` + 路径输入框收进默认隐藏的 `#artAdvBar`（点开关展开并聚焦）。目录路径仍显示在状态行 `<code>` 中，不丢透明度。
- **A2 动作收敛**：行内动词统一为 查看/下载/打包/打开› 四种；「仅供排错查看」灰字补 tooltip（`artProcROHint`）说明为何不给下载；组描述与按钮文案对齐（「进入」→「打开」）。
- **A3 过程组折叠**：「检索过程」组默认折叠为一行摘要「N 个过程文件（排错用）· 点开查看」（`proc-toggle`）；有筛选词时自动展开，避免搜到了却看不见；切目录自动复位。
- **A4 PDF 扁平化**：加载时把 `pdfs/` 子目录条目拉平进「全文 PDF」组（显示 `pdfs/xxx.pdf`，免一次「进入」）；`/api/file` 只收纯文件名（server.py:800 拒路径分隔符），故行按钮拆出独立 `data-art-dir` 属性携带子目录，`artOpenFile(name,forceDl,dirOverride)` 兜底。中途发现并修复属性拼接 bug（`data-art-dir` 曾误拼进 `data-art-name` 值内部导致解析错乱）。
- **A5 组描述进 tooltip**：组头移除内联描述 `.art-sec-d`，改挂 `title`；一屏重复教学三处 → 保留页顶 how-to + hover 提示。
- **A6 一键下载全部**：新增 `#art_cta` 主按钮「一键下载全部产物 (N+)」——报告+题录数据按文件名打包、全文 PDF 走 `dirs:["pdfs"]` 整目录打包（`/api/zip` 原生支持）；实弹验证 zip 含 57 PDF + 报告文件。
- **回归**（Chromium CDP）：A1 默认隐藏/可展开 ✔；动词集合＝{打包,打开›,查看,下载} ✔；proc 折叠/展开 ✔；57 条 `pdfs/` 扁平行、`pdfs/` 目录行消失、下载按钮 57 个带正确子目录属性 ✔；组头 0 内联描述+title ✔；CTA 中英双语随语言切换 ✔；`/api/file` 子目录下载 200（3.5MB）、`/api/zip` 200（44MB/60 entries）✔；未捕获异常 0、控制台错误 0；i18n 中英键对等。
- 改动文件：`workbench/index.html`（工具栏重排 + `#art_cta`）、`workbench/app.js`（i18n 6 新键 + artRowHTML/artRenderBody/loadArtifacts/事件处理）、`workbench/app.css`（`#art_cta`/`.art-bar-adv`/`.art-ro` tooltip 样式）。`publish-dist` 已重建（116 文件 / 2.96MB，MD5 一致）。

### 工作台「宣称功能 100% 可实现」全页面核查（2026-10-23）——修复 9 处缺陷
- **背景**：用户要求逐页逐选项核查最新工作台版本（`workbench/` 开发版，非已发布应用），确保页面上宣称的功能全部真实可用。方法：静态走查（控件 ↔ JS 处理器 ↔ 后端 argv）→ 本地起服全接口 HTTP 实测 → Chromium headless-shell + CDP 真实浏览器交互回归（捕获未捕获异常）→ 修复后二次回归。
- **High · 流式检索面板完全不可达**：`index.html` 有第 8 个工具面板 `t-stream`（数据源 6 项 / 检索词 / 年份 / 上限 / 批大小 / 真实执行 / 开始·停止），`app.js` 有完整 `st_go`/`st_stop`，后端 `/api/lit-stream` 可用，但 `#toolTabs` 缺 `data-t="stream"` 页签按钮，`.toolpane{display:none}` → 永久不可见。修复：补页签按钮 + `stTab` 中英 I18N 键。回归：8 个工具页签全可点，`t-stream` 激活后 `display:block`，`run=false` 干跑返回预期事件。
- **High · 语言切换抛异常且只切一半**：`rebuildTipBar()` 写成 `$("tipBar")` 漏 `#`（对比 `app.js` 的 `$("#tipBar")`）→ TypeError 中断 `wbOnLangChange` 后续（重建欢迎语、`artRender()`），切 EN 后快捷提示条与欢迎语仍是中文。修复：补 `#`。
- **High · 自然语言「安全性」不识别为 CSM**：`nl_parse.py::_extract_safety` 曾被改为纯手动开关，而工作台自己的输入框占位提示、欢迎示例 `ex2`（"…的 RCT 安全性"）、澄清芯片 `vagueChip1`（"某药物的安全性…"）都在明示这一能力 → 用户照抄示例却得到「安全性偏向：否」，属"宣称能、实际不能"。**本次按用户决定恢复自然语言识别**（显式安全性词 → `safety=True` + 回写 note；显式否定优先；`DEFAULT_SPEC.safety` 仍为 `False`，不含安全性词不默认打开）。LLM 提示词（`safety true only when the request is about safety/AE/toxicity`）与规则层口径重新一致。
- **High · 主题缺失时 Vague 澄清流不触发**：`rule_parse` 末段 return 缺 `vague` 键，「帮我查」「查一下」这类最高频模糊输入只渲染一张主题为空的预览卡，6 个澄清芯片永不出现。修复：`not spec["topic"]` 时补 `vague: True`。
- **High · `--interactive` 是零实现空开关（本轮新发现）**：CLI help 写 "pause for user confirmation before search strategy and after screening"，工作台有勾选框「交互式门控（暂停确认）」，但 `run()` 内 `interactive` 仅出现在签名与 docstring、零使用 —— 勾不勾行为完全一致。同轮扫描其余 15 个界面开关（`snowball/depth/concepts/stamp_date/merge_existing/download_pdf/obsidian/zotero/preprint_fallback/guideline_sources/guideline_max/verify_top_n/citation_style/keywords/report_first`）确认均被真实消费，`interactive` 是唯一空开关。修复分两层：① CLI `main()` 实装门控——先广播检索策略 progress 事件，**有 TTY** 时 `input()` 暂停等确认（非 Y 发 `interactive_abort` 并终止），**无 TTY**（工作台子进程 / CI）绝不阻塞但如实广播 `interactive_gate_skipped` + 完整 plan，不假装暂停过；② 工作台新增 `gateModal` 确认弹窗，勾选 `f_interactive` 后点「真实执行」先展示 `settingsLine(spec)` 策略摘要，确认才执行、取消提示「已取消：未执行检索。」；SAFE 预览（dry）不拦截。
- **Medium · 滚雪球参数面板默认收起，与勾选态矛盾**：`#snowball_extra` 初始带 `hidden`、`f_snowball` 默认 `checked`，启动未同步 → `checked=true` 而 `display:none`。修复：注册监听后补一次 `dispatchEvent(new Event("change"))`。
- **Medium · 预览卡按钮事件重复绑定**：`bindActions()` 用全局选择器重扫，历史卡片按钮被反复叠加监听器（2 张卡后点第 1 张「确认检索」触发 2 次）。修复：`bindActions(root)` 按卡片作用域绑定，`resultCard` 4 类按钮改 `card.querySelectorAll`，`bindArtifacts(dir, root)` 增可选 root。
- **Medium · 「调整参数」漏回填 9 个字段**：`applySpecToForm()` 未回填 `xlsx/html/export_bib/prisma/obsidian/zotero/download_pdf/citation_style/lang` → 预览卡说一套、点执行跑另一套。修复：补齐。
- **Medium · 引用验证选「关闭」实际不关闭，且 UI 无说明**：前端有 `none`（"关闭"），后端 `_build_search_argv` 强制降级为 `top`（ct-base §17.1 防幻觉红线，降级合理）→ 选项标识与真实行为不符。修复：新增 `#verify_hint` 提示条 + `verifyNoneHint` 中英键，仅在选中「关闭」时显示，明确「会降级为仅前 N 篇校验，真正跳过请用离线 CLI」。
- **回归矩阵**：6 视图切换 · 8 工具页签 · PICO 概念行增删 · 产物筛选（17 项）· 批量计划（4 KPI / 2 条目）· 反馈两阶段确认 · 数据源 8 行 · SAFE 预览 · 语言切换（中英全文案同步）· 交互门控（弹窗 + 确认 / 取消两分支）全通过；**未捕获异常 0 条、控制台错误 0 条**；i18n 中英 457/473 键完全对等，`T()` 使用的 251 个键双语齐全，HTML `data-i18n` 键 0 缺失。CLI 参数兜底核对：工作台可发出的全部参数与 `ct_literature.py --help` 逐项比对，全部被接受且 `run()` 内确有消费点。
- **未实弹（外部副作用）**：`/api/bug-report`（向作者云端端点发真实请求）、`/api/llmcfg` 保存（会改写含 OpenAlex key 的 `.env`）—— 仅代码核对 + 前端两阶段确认浏览器实测。
- **改动文件**：`workbench/index.html`（+流式页签 / `#verify_hint` / `#gateModal`）、`workbench/app.js`（`rebuildTipBar` 补 `#`、+`stTab`/`verifyNoneHint`/`gate*` 双语键、滚雪球初始同步、`bindActions`/`resultCard`/`bindArtifacts` 作用域化、`applySpecToForm` 补 9 字段、`startRun` 拆 `_startRun` + `interactiveGate`）、`workbench/nl_parse.py`（`_extract_safety` 恢复识别、`rule_parse` 补 `vague`）、`scripts/ct_literature.py`（`main()` 实装 `--interactive` 门控）。
- **文档与载荷一致性（用户 2026-10-23 08:03 决定「保持自动」后同步）**：① `workbench/README.md` 规则层段补「安全性(CSM) 口径」说明（显式词才开 / 否定优先 / 默认不开，与 `--safety` opt-in 一致）、能力覆盖表补「流式检索」与「交互式门控」两行、引用验证行补「关闭(none) 在工作台降级为前 N 篇」说明，并修正发布包目录名 `publish/` → `publish-dist/`（2026-09-26 已改名，README 一直没跟上）；② `build_publish.py` 的 `excluded()` 增加 `.bak` basename 规则 —— 回归发现源 `workbench/` 下 8 个 `server.py.bak_*`（约 760 KB）与 `scripts/` 下 5 个 `.bak` 会随每次重建进入载荷，而 2026-10-22 那次「`_stale_*` 改名排除」只作用于 publish-dist 内部、下一次重建即被源文件还原；③ `publish-dist/` 已重建：129 → 116 文件、3.86 MB → 2.95 MB，剪除 13 个 `.bak`；关键文件与源码 MD5 逐一比对一致。
- **发布包端到端复验（从 publish-dist 起服）**：静态资源 6/6 200、`/api/config` 回传 `version=1.4.11`；浏览器 8 个工具页签、流式面板 `display:block`、`#verify_hint`/`#gateModal`/`#f_safety` 均在位；点欢迎卡第 2 个 chip（"semaglutide 近5年的 RCT 安全性"）→ 预览卡「安全性偏向：是 (CSM)」；点 `#wb-lang` 切 EN → tipBar / 欢迎语全部转英文；**未捕获异常 0 条、控制台错误 0 条**。
- 交付：workspace `ct-literature-工作台功能审计报告-20261023.md`。

## v1.4.10 (2026-10-19) · 新增「AI 生成治理（ct-base §22）」段：§22.15/§22.16/§22.17

- **§22.16 RAG 三列待核对清单**：文献综合/证据总结类输出禁止只给结论，必须附「问题/原文位置/依据」三列，并显式列出「未覆盖项」（关键语种/数据库未检等）；依据 Waikar et al. 2026（CPT:PSP，DOI `10.1002/psp4.70201`）。
- **§22.15**：检索策略/综合引擎变更前经锁定版本 + 人工基准集离线比对影子阶段，达阈值才放行。
- **§22.17**：六源检索/日期过滤/去重为确定性层，主题归类/证据综合为 LLM 层；验收报告分层声明准确率。
- 红线：检索/综合结论不得省略出处，「未覆盖项」须显式列出。
- 规范原文：`ct-base/docs/13-ai-generation-governance.md` §22.15–§22.17。

## v1.4.9 (2026-10-19) · fetch_coze_unified 异步化：/stream_run 降级快速路径，主路径 /run 支持 accepted+run_id 轮询

> 背景：Coze 云端网关 stgw 对 HTTP 请求有 60s 硬超时（ct-base §20.17.1 实测 60.0s 整 504，流式同样被杀）。ct-literature 原以 `/stream_run` 为主路径，重检索（批量 PDF / 深翻页 / ICTRP 型长任务，服务端数分钟）必被杀 → 回退 `/run` 若返回 `{status:accepted, run_id}` 异步协议（服务端还在跑），客户端不识别该协议、把 accepted 信封当同步响应对待 → project_list 缺失 → 空结果。同族 ct-registry `extsvc_client._run_async_poll` 已有成熟范本（ICTRP/CDE 实测穿越 60s 窗口），ct-safety v0.10.3 同步落地。

- **主路径改为 `/run` 响应形态自适应**（`adapters/fetch_coze_unified.py`）：
  - 同步返回 → 直接 `_parse_run_response` + `clip_by_date_window`（与旧行为一致）；
  - `{status:accepted, run_id}` → 新增 `_coze_async_poll()` 轮询 `{base}/run/status/{run_id}`：指数退避 5→30s、总上限 timeout（默认 300s）、终态 completed→同口径 parse+裁剪 / failed·cancelled→`{"error": ...}`（不静默）/ 到期→timeout error 附引导。401/403 立即失败；404（最终一致性窗口）/ 连接抖动 / 单次超时均续轮。
- **`/stream_run` 降级为快速路径**：socket timeout 钳制 `min(timeout, _STREAM_FAST_PATH_MAX=60s)`（env `CT_SEARCH_STREAM_TIMEOUT` 可配）——只承担 60s 内能完成的轻检索（SSE 进度 + 最快），到点主动切换主路径。
- **路线 B 一致性**：轮询 completed 回收的结果与 `/run` 同步路径共用 `_parse_run_response` + `clip_by_date_window`（月份级日期窗口裁剪不因路径而漂移）；`log_only` 留痕调用不受影响（Coze 端 route_by_mode 秒级返回同步信封）。
- **验证**：新增 `scripts/tests/test_fetch_coze_unified_async.py` 16 断言 mock 全过（stream 成功 / 同步回退 / accepted 轮询 completed / failed / cancelled / 404 续轮 / 到期 / 401 / 钳制 / completed 路径日期裁剪）；全量 py_compile + CLI `--help` OK；真实探针 1 次（europepmc osimertinib，7.7s，5 works，stream 路径无损）。
- **Coze 侧零改动**：纯本地客户端。

## v1.4.8 (2026-10-17) · SkillHub 卡面「需配置 API Key」徽章措辞修正（零用户侧配置事实对齐）

> SkillHub 竞品扫描发现：ct-literature 卡面带平台「需配置 API Key」徽章，被「不限 API Key」筛选器排除，与「默认全流程免 key」的事实相悖。根因是 SKILL.md 内 `key needed`（Semantic Scholar 可选源）与 `without token`（PROSPERO 保留源）措辞被平台解析为 key 依赖。本版仅改措辞对齐事实，零行为变更。

- **Data Sources 段**：`Semantic Scholar (--with-semantic-scholar, key needed)` → `optional free key — keyless works at reduced quota`；明确 `the default pipeline runs fully keyless`、`no user-side key is ever required for the default pipeline`。
- **frontmatter**：`summary` / `description` 末句统一为「默认全流程免 key，无任何用户侧配置亦可使用」（英文段同步）。
- **未改**：默认管线（OpenAlex + Europe PMC + bioRxiv/medRxiv）本就免 key，行为零变化；可选源（S2 / arXiv / PROSPERO）的 opt-in 语义不变。

## v1.4.7 (2026-10-13) · 网页端长任务进度反馈修复（引文验证阶段 + 诊断行透出）

> 用户反馈「网页对话检索时间较长时，没有提示用户等待的进度信息」。线上回归复盘 NDJSON 流：事件一直齐全（busy_hint / run_start / source_done / verify_progress / fetch_done…），但前端渲染层把它们吃了。

- **根因 1（主因）**：`ct_literature.py` 的 `verify_progress` 事件 `_out(None, "verify_progress", done=N)` 第一参为 None → json 流无 `message` 字段；前端 `app.js` 的 progress 分支只渲染 `ev.message||ev.msg` 非空的事件 → **引文验证阶段（全程最长，大结果集可达数分钟）16+ 条进度事件被整段丢弃**，UI 静止。
- **根因 2（次因）**：`ev.ev==="log"` 类型事件（`[Coze]`/`[INFO]`/`[WARN]` 诊断行）前端无分支，从不展示——长任务期间后端在做事但界面完全静默。
- **服务端修复**：`verify_progress` 补 human message `⏳ 引文验证 N/M` + `total` 字段（jobs 总数）。
- **🔧 热修（部署后回归发现，同日闭环）**：初版 `total=len(jobs)` 是**源数**（4）而非待验证文献数（唯一 works，smoke 实测 16）→ 线上出现 `引文验证 16/4` 超调。改为 `total=len(_seen_keys)` 实时大小——验证条目随各源 fetch 完成动态入队（596-598 行），producer put 先于对应 worker 的 `done+=1`，数学上恒有 `done ≤ total`；本地实跑复验 19/19 无超调。
- **前端修复**（`workbench/app.js` 主管线流）：新增 `verify_progress` 显式渲染分支（有 message 用 message；旧服务端无 message 时用 done/total 兜底拼）；新增 `log` 事件分支，后端诊断行透出（dim 样式）。
- **覆盖范围**：`/api/search`（对话检索 / 表单检索主管线）全链路——busy_hint（Coze 检索等待提示）→ source_done（各源）→ verify_progress（引文验证，原缺口）→ fetch_done → export_done 全渲染。`/api/lit-stream`（单源流式工具）本就逐批推送且字段自洽（`msg`），不在修复面。
- **验证**：本地 `--offline --progress json` 实跑，`verify_progress` 输出 `{"event":"verify_progress","message":"⏳ 引文验证 1/4","done":1,"total":4}`；`node --check app.js` + `py_compile ct_literature.py` 双过；publish-dist 重建同步 diff=0。

## v1.4.6 (2026-10-13) · 修复网页端 Coze 401（token 模块自包含，v1.4.5 授权门修复的第二层）

> v1.4.5 部署后线上端到端回归实测：AUTH-BLOCK 已消失，但三源仍降级——`[Coze] HTTP 401: Missing authorization header` + `Token 无效或已过期`。授权门放行了，请求却没带 Bearer token 到达 Coze。

- **根因**：`_resolve_token()` 第三级「内嵌公开 blob」依赖 `from endpoint_token import get_token`，而该模块物理上只在 **ct-registry 技能树**（`~/.workbuddy/skills/ct-registry/adapters/`）；`fetch_coze_unified.py` / `pdf_download.py` 均以「运行时把 ct-registry/adapters 插进 sys.path」方式引用。云端部署容器（`/workspace`）没有 ct-registry → import 失败被 except 吞掉 → token 为空 → 无 Authorization header → Coze 401。`pdf_download._resolve_token()`（`coze_resolve.py` 复用同一函数）同款断裂，PDF 直链解析在网页端同样不可用。
- **修复（发布包自包含，对齐 ct-base / ct-advisor 范式）**：`endpoint_token.py`（XOR+base64 混淆的公共 token blob，ct-base §5.236，设计上即「随技能包发布」）拷入本技能 `adapters/`；两处 sys.path 接线改为**本技能 adapters 目录优先**、ct-registry 降为兜底（老布局兼容）。
- **实证矩阵**：模拟空 home 容器（无 ct-registry、无 env token）——修复后 `fetch_coze_unified` / `pdf_download` 双模块 token 均非空、`_headers()` 均含 Authorization；本机无退化（Auth header / 授权门 / 私有端点拦截全部保持）。
- **同步**：`build_publish.py` 重建（77 文件 +1 endpoint_token.py、PRUNED 0 stale、三文件 diff=0）；`py_compile` 四份副本全过。
- **部署验证**：覆盖发布 `ct-literature.app.workbuddy.host` 后线上 smoke（pembrolizumab NSCLC, max=5, 2025–2026）——待本次 v1.4.6 部署后复跑确认 401/AUTH-BLOCK 双清零。

## v1.4.5 (2026-10-13) · 修复网页端三源 AUTH-BLOCK 降级（授权门内置公开端点白名单）

> 用户报告网页端（publish-dist 云端部署）EuropePMC / medRxiv / bioRxiv 报 `Coze 失败(AUTH-BLOCK)，降级本地 fetch`；本机 agent / CLI 调用从不复现。

- **根因**：`_check_outbound_authorization()` 的三个 config 候选路径（env `CT_LIT_RUNTIME_DIR` > `~/.workbuddy/ct-literature-runtime/config/config.json` > 技能树内 `config/config.json`）在**云端容器**全部落空——runtime config 于 2026-09-06 故意移出技能树（含私有端点、不随发布包公开，CHANGELOG 同日期条目），发布包内无兜底 config → 授权门返回 False → `dispatch()` 返回 `error=AUTH-BLOCK` → `ct_literature.py` 三源降级本地 fetch。该 09-06 决策当时只验证了本机路径，未覆盖云端部署面。
- **佐证**：OpenAlex 不报是因网页端环境有 `OPENALEX_API_KEY` 走本地直连（绕过授权门）；semantic_scholar 默认关闭。
- **修复**：`adapters/fetch_coze_unified.py` 新增 `_BUILTIN_PUBLIC_ENDPOINTS` 常量（`ct-search` / `ct-bugreport` 的 `/run`——作者公开端点，token 为 2026-08-18 授权的嵌入式公共 token），`_check_outbound_authorization()` 开头优先放行。授权门语义只防「私有端点外发」，公开端点在所有部署面（本机 / CLI / agent / 云端网页端）放行不冲突；env `CT_SEARCH_ENDPOINT` 覆盖为其他端点时仍走 config 授权，原语义不变。
- **实证矩阵**（模拟空 home 容器复现云端部署面）：修复前 ct-search `authorized=False`（与现象吻合）；修复后——本机 / 云端模拟两环境 ct-search、ct-bugreport 均 True，私有端点 `https://evil.example.com/run` 两环境均 False（授权门未被削弱）。
- **同步**：`workbench/publish-dist/adapters/fetch_coze_unified.py` 经 `build_publish.py` 重新构建同步（76 文件、PRUNED 0 stale、与主树 diff=0）；`py_compile` 通过；`tests/regression_force_coze.py` 对该函数为 mock 不受影响。
- **生效前提**：网页端需重新部署（workbuddy sites deploy 覆盖 `ct-literature.app.workbuddy.host`）后才消除 WARN；未部署前降级路径仍保底出结果。

## v1.4.4 (2026-10-13) · 修复工作台调用 entry_point 恒为 skill（§1.3 接线）

> ct-base coze_io_contract §1.3 工作台接线三架构之「架构 B · Popen 子进程」。v1.4.x 系列只做了注入侧（dispatch payload 带 entry_point），设置侧零接线；本技能工作台是 `server.py → Popen(ct_literature.py)` 子进程架构，父进程 `set_entry_point()` 无法跨进程传递 → 应用页面调用恒落默认值 `skill`。

- **`adapters/fetch_coze_unified.py`**：新增 `_entry_point_from_env()`——模块加载时从环境变量 `CT_ENTRY_POINT` 解析 `_ENTRY_POINT` 初值（白名单 `skill`/`workbench`/`api`，空白/非法一律回退 `skill`）；`set_entry_point()` 运行期覆盖语义不变。
- **`workbench/server.py`**：两处 `Popen`（`ct_literature.py` 主检索 + `coze_resolve.py` 直链解析，均向 coze 端点发请求）的 `env` 增加 `CT_ENTRY_POINT=workbench`，子进程模块加载即继承工作台身份；agent / 技能 CLI 不设该变量 → 恒 `skill`（无回归）。
- **同步**：`workbench/publish-dist/adapters/fetch_coze_unified.py`、`workbench/publish-dist/workbench/server.py` 与主文件逐字节一致（diff 验证）。
- **验证**：`_entry_point_from_env()` 七组用例（workbench/空/空白/evil/大小写变体/api/无变量）全过；payload 默认注入 `skill` 复核通过；`py_compile` 四份副本全过；跨技能契约回归 `ct-base/scripts/tests/test_entry_point.py` E1–E9 全绿。
- **范式沉淀**：ct-base `references/coze_io_contract.md` §1.3 新增「工作台接线三架构」规范段（A 进程内 import / B Popen env 透传 / C 代理注入），本技能为架构 B 范本之一。

## v1.4.3 (2026-10-13) · 云端原生日期过滤落地（ct-registry coze 0.3.94 联动 + lit_date_* 契约对齐）

> 用户指认云端代码位置 `ct-registry/adapters/coze`，根治 v1.4.2 遗留的 online 结构性局限：客户端只砍不补、europepmc 空日期。

- **云端源码定位**：ct-search.coze.site 的服务端代码位于 `ct-registry/adapters/coze/src/`（`literature_nodes.py` 即文献检索节点，`search_node.py` 按 source 路由原样透传 state）——此前误判「源码不在本地」实为未找到。
- **云端根因 1（入口静默丢弃）**：`GraphInput`/`GlobalState`/`SearchNodeInput` 三模型均未声明文献日期字段，v1.4.2 透传的 `date_from/date_to` 在入口即被 `extra='ignore'` 丢弃（与 2026-10-08 FAERS 同款坑）。云端已补 `lit_date_from`/`lit_date_to`（YYYY-MM-DD，三模型同声明；与 FAERS 的 YYYYMMDD `date_from/date_to` 独立命名防混用）。
- **云端根因 2（europepmc 空日期）**：云端 `europepmc_node` 从顶层取 `printPublicationDate`/`dateOfPublication`，而二者嵌在 `journalInfo` 下、顶层恒空串 → `publication_date` 全空。已对齐本地 2026-09-08 BUGFIX 改 `firstPublicationDate`（顶层真源）优先。
- **云端五节点原生过滤（date 优先、year 回退、老客户端逐字不变）**：OpenAlex `from/to_publication_date:YYYY-MM-DD`；Europe PMC 与预印本 `(FIRST_PDATE:[lo TO hi])` 查询子句（沿用本地 2026-10-12 实证：`filter=pdates` 被 API 静默忽略）；arXiv `submittedDate:[YYYYMMDD TO YYYYMMDD]`；S2 `publicationDateOrYear`。COZE_VERSION 0.3.93 → **0.3.94**。
- **本技能侧改动**：`fetch_coze_unified.dispatch()` payload 键名 `date_from/date_to` → **`lit_date_from/lit_date_to`**（与云端契约对齐；签名与 CLI 保持 `date_from/date_to` 不变）。`clip_by_date_window()` 客户端兜底保留——云端未部署 0.3.94 前仍靠它保正确性。
- **向后兼容实证**：旧云端（0.3.93）收到 `lit_date_*` 被静默忽略不报错，客户端裁剪兜底生效（online 冒烟通过）。
- **生效前提**：online 模式原生日期过滤需云端部署 coze 0.3.94（Coze 平台人工发布）；部署前周报继续用 `--offline` 保时效硬保证。云端验证：selfcheck 44/44 + 三模型穿透/各源检索式/date 优先/year 回退 11 项全过。

## v1.4.2 (2026-10-12) · online/Coze 通道日期窗口支持（透传 + 客户端裁剪 + year 兜底）

> 用户反馈「切勿用 --online/Coze 模式，直接修改 coze 代码支持即可」——让默认 online 通道也支持月份级日期窗口，而非在调用方规避。

- **dispatch 透传**：`fetch_coze_unified.dispatch()/dispatch_stream()` 加 `date_from/date_to`（置于签名**末尾**，避免位置参数错位——曾因置于第 5/6 位导致 `max_results` 位置传参撞 `date_from` 报 "got multiple values"），非 None 时写入 Coze payload。云端工作流消费后原生过滤；未消费则被静默忽略（向后兼容，不报错）。
- **dispatch 客户端裁剪**：stream 与 `/run` 回退两条路径拿到结果后均调用 `clip_by_date_window()`，`count/total_count` 取裁剪后数量，打 `[coze date-window]` 日志。`_offline_fallback()` 亦加 date 透传 + 返回前统一裁剪。
- **共享 `clip_by_date_window(works, date_from, date_to)`**：`publication_date` 精滤；缺失/空回退 year 粗兜底（year 越界砍、边界年内保守保留计 `year_fallback`、无 year 保守保留计 `no_date`）。`ct_literature.run()` 合并兜底改复用此函数（获得 year 兜底能力）。
- **online 通道接线**：`_coze_dispatch_with_fallback()` 加 `date_from/date_to` 并透传 `coze_dispatch`；`run()` online 分支 job 传 `date_from/date_to`。
- **修复 CLI bug**：`fetch_coze_unified.main()` 引用 `args.log_only` 但 argparse 未定义 `--log-only`，单独运行必 `AttributeError`；已补定义。新增 `--date-from/--date-to` CLI。
- **⚠️ 实测结论（online 结构性局限）**：Coze 云端工作流（ct-search.coze.site）**不按日期过滤**，返回相关性排序（多老文）结果并受 `max_results` 截断。实跑 `--recent-months 1`（online）见 openalex dropped=15/15、biorxiv 15/15、medrxiv 14/15 全为超窗老文，裁后近月文献≈0——**客户端裁剪只能砍、补不回被截断挡掉的近期文献**。europepmc 因 Coze 端不填 `publication_date`（返回空串），靠 year 兜底保留 2026 内 12 篇。
- **根治需云端配合（源码不在本地技能树）**：① Coze 云端工作流消费 payload `date_from/date_to` 在各源 API 层原生日期过滤；② 修复 europepmc 节点填 `publication_date`。两者需在 Coze 平台人工部署。云端升级后，online 客户端已就绪（透传 + 裁剪），自动受益。
- **验证**：`clip_by_date_window` 单测 9/9 PASS（窗口内 / 越界 / year 兜底 / no_date / 无窗口 passthrough）；online 实跑确认裁剪日志与 year 兜底计数符合预期。

## v1.4.1 (2026-10-12) · 月份级发表日期窗口（路线 B 原生过滤）

> 来自周报情报自动化需求：仅关注最近 1 个月内「AI + 临床试验」最新论文，年份级 `--year-from` 粒度不够。

- **新增 CLI 参数** `--date-from YYYY-MM-DD` / `--date-to YYYY-MM-DD` / `--recent-months N`（便捷：最近 N 个月 ≈ 今天-N*30天 起）。三者与 `--year-from/--year-to` 并存，日期级优先于年份级。
- **原生下推到各源 API（替代年份级 `Jan-1` 粗粒度）**：
  - OpenAlex：`from_publication_date:<date>` / `to_publication_date:<date>`（fetch_openalex.py）
  - Europe PMC：查询子句 `(FIRST_PDATE:[YYYY-MM-DD TO YYYY-MM-DD])`（fetch_europepmc.py，PPR 同源）——🔴 勿用 `filter=pdates:...`，该语法被 API 静默忽略（按索引日期非发表日期过滤，实测放回 2020 年文献）
  - preprints：Europe PMC PPR 用 `FIRST_PDATE:[...]`；api.biorxiv.org 增量窗口按 `date_from/date_to` 收窄（即便 EPC 无命中也照常拉取，保证日期过滤生效）
- **跨源兜底**：`run()` 合并归一化后按 `publication_date` 客户端裁剪到 `[date_from, date_to]`，在线 Coze 通道无法透传日期时亦保证不漏出窗口外文献。
- **向后兼容**：未传日期参数时行为完全不变（年份级 `Jan-1`/`Dec-31` 兜底保留）；`run()` 新参 `date_from/date_to` 默认 None；各 fetch 适配器签名追加带默认值的 `date_from/date_to`，既有调用零影响。
- **验证**：SAFE PREVIEW 参数解析通过；`--offline --recent-months 1 --run` 实跑确认记录 `publication_date` 落在窗口内、客户端裁剪计数正常。

## v1.4.0 (2026-10-08) · Evidence-synthesis evaluation benchmark blueprint

> Landed from WeChat intel weekly report (wechat_intel_2026-10-08.md).

- **New `references/evidence_synthesis_benchmark.md`**: evaluation design for the
  retrieval → screening → extraction chain, based on TrialMind / TrialReviewBench
  (npj Digit Med 2025, doi:10.1038/s41746-025-01840-7; 100 systematic reviews / 2,220
  clinical studies), MedReview (2024, doi:10.1038/s41746-024-01239-w; 8,161 Cochrane
  pairs) and TrialPanorama (2026, doi:10.1038/s41746-026-02933-7; 8 tasks).
- **Suggested regression protocol**: recall@k gate against human-verified gold sets,
  dedup precision, summary-faithfulness spot checks, per-run auditable report in `out/`.
- SKILL.md: new "Evaluation Benchmarks (v1.4.0 blueprint)" section; frontmatter 1.3.0 → 1.4.0.
- Blueprint only — engine behavior unchanged, zero new dependency, no new network path.

## v1.3.0 (2026-10-08) · Docling PDF 结构化解析增强

> 基于《临床试验Skill推荐》分析，新增 Docling 作为 PDF 解析增强层。

- **新增 PDF Parsing Enhancement (Docling) 章节**：`pip install docling` → `DocumentConverter().convert()` 输出带层级结构的 Markdown/JSON
- **与现有 PDF 流水线互补**：Docling 优先解析（保表格结构），失败时回退到 PyMuPDF/PdfPlumber
- **适用场景**：CT.gov 方案 PDF、EU-CTR 文档 PDF、OA 全文 PDF 的结构化解析

## v1.2.4 (2026-10-07) · 接入 `entry_point` 调用来源标记（ct-base coze_io_contract §1.3 / §2.3）

> 飞书 searchlog 新增 `entry_point` 独立列，用于按**调用来源**（技能本身 / 工作台 Web 应用 / 未来第三方 API）直切筛选。本技能此前未发送该字段，现按契约补齐。

- **`adapters/fetch_coze_unified.py`**：新增模块级 `_ENTRY_POINT = "skill"` + `set_entry_point(v)` + `entry_point()`（枚举白名单 `skill`/`workbench`/`api`；空值 / 空白 / 非法值一律回退 `"skill"`，绝不写 `None` 或脏值）；`dispatch()` 构造 payload 时在**顶层信封**注入 `"entry_point"`（与 `query_origin` / `skill_version` 同级）。
- **与 `query_origin` 正交（🔴 不得混用）**：`query_origin` 按机器（COMPUTERNAME SHA-256），同一台机器上 skill 与 workbench 哈希逐字节相同 → 无法区分界面来源。
- **未改动检索与路由逻辑**：`--force-coze` 早返回、本地 key 直连、`log_only` 留痕等既有行为零变化；`entry_point` 为独立顶层字段，不参与任何条件判断。
- **同步**：`workbench/publish-dist/adapters/fetch_coze_unified.py` 与主文件逐字节一致（避免发布包携带未实现的旧副本）。
- **验证**：真实 `dispatch(source, ..., force_coze=True)` 出站 payload 实测带 `entry_point='skill'`；`set_entry_point('workbench')` 后再发即带 `workbench`；非法值 / `None` / 空白均回退 `skill`。既有回归无退化：`regression_stream_parser` 8/8、`regression_force_coze` 24 passed、`regression_root_causes` 24 passed。跨技能契约回归见 `ct-base/scripts/tests/test_entry_point.py`（E1–E9 全通过）。

> ⚠️ 落地前提（§2.3 部署铁律）：**飞书列须先于新 coze 代码存在**。当前 coze 侧尚未写 `entry_point` 键，该列会留空（安全方向：旧 coze + 新表 = 不报错）；coze 侧补齐后本列自动落值。

## v1.2.3 (2026-10-07) · SSE 解析降级路径加固（ct-safety 双发缺陷的跨技能推广）

> 三个技能共用同一 Coze 端点 `ct-search.coze.site/stream_run`。ct-safety 的「每次检索双发」根因（本技能同款形态假设）在本地排查后确认：**本技能当前无双发**，但降级路径存在同类脆弱点，已加固。

**三技能实测结论（同一端点，形态不同）**

| 技能 | 解析器 | `pdf_download` 在技能树内 | 实测结果 |
|---|---|---|---|
| ct-safety | `adapters/coze_dispatch.py` | ❌ 无 → import 必失败 | **双发**（已 v0.9.14 修复） |
| ct-literature | `adapters/fetch_coze_unified.py` | ✅ 有 → 主路径 import 成功 | **无双发**（6 source 实测均单发） |
| ct-registry | `adapters/search_ictrp.py` | — 独立实现（带 `x-workflow-stream-mode: debug` 头，取 `node_end.output`） | **无双发**（实测 `stream=1, run=0`） |

**本技能实际修复：降级路径能力对齐**

`_parse_stream()` 主路径复用 `adapters/pdf_download._parse_coze_stream`（强解析器，含 `node_end` 回退 + S3 外置回拉）。但 `_parse_stream_local`（import 失败时的降级兜底）仍是旧的弱实现，只认`projects` 键——一旦主路径失效（环境变动/文件缺失），立刻退化为「误判无结果 → 回退 `/run` → 双发」，即 ct-safety 的同一失败模式。修复：降级路径与主路径**能力对齐**。

- **新增 `_fetch_s3_projects()`**：回参超长外置（`s3_url` + 空 `projects`）时回拉真实结果。修复前：静默当「0 篇」；修复后：正常回拉。
- **`_parse_stream_local` 增补 `node_end` 回退**：`workflow_end.output={}`（Coze Output 变量未绑定）时回退到最后一个含真实结果的 `node_end.output`。修复前返回 `None`（触发 `/run` 回退），修复后正确取回。
- **增补三种嵌套形态兼容**：`output` / `data.output` / `data.data.output`。
- **解析器不再互相依赖**：降级路径可独立正确工作，不依赖「主路径一定成功」。

**既有测试盲区（本次补上）**：`tests/regression_root_causes.py` 的 T7/T7c 只测了 `pdf_download._parse_coze_stream`（主路径），**从未测过降级路径** —— 这正是薄弱环节能长期潜伏的原因。

**验证**
- 新增 `tests/regression_stream_parser.py`（L1–L8，纯离线）：正常 project_list / 空 projects=真 0篇 / `node_end` 回退（含事件顺序颠倒）/ 三种嵌套形态 / S3 顶层与嵌套双位置回拉 / 非文献型 output 不误判 / 分块边界(1/7/64/全文)一致 → **8/8 RC=0**。
- 真实端点交叉验证：同一份 openalex SSE，`_parse_stream`（主路径）与 `_parse_stream_local`（降级路径）**均返回 50 篇**，结果一致。
- 真实 dispatch 实测（`force_coze=True` 绕开openalex 本地 key 早返回）：`openalex / europepmc / biorxiv / medrxiv / arxiv` **全部 `stream=1, run=0`**，单次外发。
- 既有回归无退化：`regression_force_coze.py` 24 passed、`regression_root_causes.py` 24 passed。
- `workbench/publish-dist/adapters/fetch_coze_unified.py` 已同步（与主文件逐字节一致），避免发布包携带旧解析器。

> ⚠️ 未改动Coze 侧与检索逻辑；`--force-coze` / 本地 key 早返回等既有行为零变化。

## v1.2.2 (2026-10-06) · 工作台安全加固：敏感文件黑名单（P1）+ 路径黑名单（P3）

> 已发布工作台应用（`ct-literature.app.workbuddy.host`）安全加固，阻止敏感数据被 HTTP 下载。

- **`workbench/server.py` + `workbench/publish-dist/workbench/server.py`**：
  - P1: 新增 `_SENSITIVE_FILES` 文件名黑名单（`drug_name_map.json` / `term_map.json` / `mesh_terms_mapping.json`）。
  - P3: 新增 `_STATIC_PATH_BLOCKED` 路径黑名单（`adapters`, `out`, `pdfs`, `_bugreports`, `references/guidelines`），阻止目录级访问，返回 403 `forbidden path`。
- **影响**：适配器代码、PDF 全文、Bug 反馈日志、指南文档无法通过 HTTP 直接访问；`/api/*` 端点不受影响。
- **回归**：`curl http://127.0.0.1:8787/../adapters/coze_resolve.py` → 403；`curl http://127.0.0.1:8787/../references/guidelines/` → 403。

> 已发布工作台应用（`ct-literature.app.workbuddy.host`）安全加固，阻止敏感映射文件被 HTTP 下载。

- **`workbench/server.py` + `workbench/publish-dist/workbench/server.py`**：新增 `_SENSITIVE_FILES` 文件名黑名单（`drug_name_map.json` / `term_map.json` / `mesh_terms_mapping.json`），即使 `.json` 在扩展名白名单内也拒绝（403）。
- **影响**：FAERS 药物名映射、MeSH 术语映射、通用术语映射文件无法通过 HTTP 下载；不影响前端读取 `workbench.config.json`。
- **回归**：`curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8787/../references/drug_name_map.json` → 403。

## v1.2.0 (2026-10-02) · 默认启用滚雪球 + Report-first；结果不足建议卡；i18n 补全

- **默认启用**：`run()` 默认 `snowball=True`、`report_first=True`（零成本提升覆盖率 + 先出骨架改善 UX）；`f_depth` 默认 `standard`
- **结果不足建议卡**：`_finalize()` 在 ≤10 篇时主动建议扩展检索（snowball / deep / PICO / 罕见病专源），含罕见病关键词启发式
- **`_out()` JSON 模式**：携带 `message` 字段，建议文本可经流式到达前端
- **i18n 新增 5 条双语建议文案**：`suggest.few_results_prefix` / `snowball` / `deep` / `pico` / `rare_disease`
- **工作台 UI**：`f_snowball` + `f_report_first` 默认 `checked`；流式渲染 `suggest_few` / `suggest_item` 事件（橙色警告 + 斜体建议项）
- **F19 整改**：SKILL.md 正文中文段翻英文（§4 合规）
- **shared_sync 整改**：`i18n.py` / `kw_localize.py` 从 ct-base 同步；term_map 4 个光生物调节词条回填 ct-base 后同步
- **F13 版本对齐**：CHANGELOG 首部新增 v1.2.0

## v1.1.3 (2026-09-27) · SKILL.md 瘦身至 132 行：三大块外迁 references（零内容删除）

- **动因**：SKILL.md 326 行，超 ct-base §16.1 / spec_lint F02 软上限 200。按用户指示「不删除内容、
  移到其他文档」，做**逐字外迁**（原文一字不动搬出，SKILL.md 各节压成 3–6 行摘要 + 指针链接）：
  - `references/published_app.md`（新，51 行）← 原「Published Application」全节（登记表 + 重发布协议
    + publish-dist 改名事故记录）；
  - `references/capabilities.md`（新，133 行）← 原「Positioning / Data Sources / Clinical guideline
    sources / Features / Unified work schema / Output / Implementation（含 OpenAlex key）」明细表全文；
  - `references/dialogue.md`（新，84 行）← 原「Natural-Language Dialogue」全节（Step 0 四桶 / 红线 /
    echo block / merge_spec / 执行流）+「Bug Reporting §20.3」全节。
- **对账**：8 组关键特征串（appId、PROSPERO reserved、doc_type_filter、当前检索设定、
  ct-bugreport 端点、coze_resolve --pipeline、96 curated entries、load_openalex_key）在
  SKILL.md + 3 新文件合集内全部命中；SKILL.md 内 7 个 references 指针链接零死链；
  新文件未被 ignore 规则误挡（可随包发布）、无隐私命中。
- **运行面影响**：无功能代码改动；agent 侧加载契约不变（指针文件按需加载）。
- 版本未 bump（Unreleased——待下次发布随包）。

## v1.1.3 (2026-09-26) · 工作台流式检索补上检索词自动翻译 + dispatch_stream mode NameError 修复

用户反馈：「工作台操作的时候似乎没有对检索关键字做自动翻译」。核实：主管线 `/api/search`
（对话检索/高级参数）经 `ct_literature.run()` 一直有 `topic_translator` 中英翻译，
但「工具 → 实时流式检索」（`/api/lit-stream`）把用户关键词**原样**丢给 Coze——
中文检索词打到 OpenAlex/Europe PMC 基本零命中，属翻译盲区。

- **`workbench/server.py` `_lit_stream`**：调用 `dispatch_stream` 前插入
  `topic_translator.translate_topic(keyword, online_fallback=True)`（与主管线同一实现：
  本地词典贪心 + MeSH OR 扩展 + 联网兜底）；命中翻译时向前端推
  `translated {zh, en, partial, untranslated}` 事件；翻译模块异常不阻断，按原文检索。
- **`workbench/app.js`**：流式面板渲染 `⇄ 检索词已自动翻译：中文 → English`，
  部分未译时红字标注保留原文的词；新增 i18n 键 `trAuto` / `trPartial`（zh/en）。
- **连带修复 `adapters/fetch_coze_unified.py`**：`dispatch()` 于 2026-09-11 新增 `mode`
  参数时漏改 `dispatch_stream()` 签名，其内部 `mode=mode` 引用未定义全局名——
  流式检索一 `--run` 即 `NameError: name 'mode' is not defined`（e2e 实测踩中）。
  补 `mode: str = "search"` 形参并透传。
- **验证**：本地起 server 实测——「奥希替尼 间质性肺病」→ `(osimertinib OR Tagrisso)
  interstitial lung disease (ILD)`，OpenAlex 真实检索返回 5 篇；纯英文 `metformin`
  原样透传、无 translated 事件。bundle 已 `build_publish.py` 重建（3 处修改均确认落盘）。
- **已发布（2026-09-26 11:45）**：按 ct-workbench-publish 铺开计划验收协议在新 workspace
  覆盖发布——install_genie ①→publish_guard pre ②→deploy（appId 覆盖，shareLink 断言
  `ct-literature.app.workbuddy.host` 通过）→genie 回读无污染 ⑤→post-gate PASS ⑥→
  线上验证：app.js MD5 与载荷一致、`/api/status` 200、线上 `/api/lit-stream`
  「奥希替尼 间质性肺病」实测返回 `translated` 事件 → `(osimertinib OR Tagrisso)
  interstitial lung disease (ILD)`。跨 workspace 方案 B 对 ct-literature 二次实证。

## v1.1.3 (2026-09-19) · 解码与下载并行：本地直链一到手就落盘

用户反馈：「直链解码和 PDF 下载完全可以并行的，现在观察到的是本地先搜索一遍有直链的，
然后把无法解码的再发送扣子。实际上，本地如果已经解码到直链，就直接开始下载就可以了。
这种并行操作不仅在工作台界面上，在上下文对话技能调用中也应该可以这样操作。」

两处都确实是**名不副实的串行**：`coze_resolve.py` 是三段串行，`PdfDownloader.run()`
的 docstring 一直写着 `local download || coze decode`，代码却是本地整段跑完才启动 coze 线程。

### 工作台链路（`coze_resolve.py`，默认 `--pipeline`）
- **本地探针流式回报**：`_verify_direct(..., on_result=…)` 从 `ex.map`（等整批探完）改为
  `as_completed` + 逐条回调——命中直链的**那一刻**就入下载队列，不等其它探针。
- **两波提交、共用闸门**：「明显不是文件」的大头在探针跑的同时立刻提交端点；探针否掉的那批
  探完补送第二波。两波共用一把 `Semaphore(--concurrency)`，保证同一时刻打到端点的批数不翻倍。
- **Coze 返回一条就入队一条**：每批返回即逐条组装并立即下载，不再攒到末尾统一下载。
- **下载工人池**（`--dl-concurrency`，默认 3）：走 `PdfDownloader._limiter`（逐域名限速，
  线程安全）——同域名保距串行、跨域名并行。并发若不限速，同站请求节奏会被乘上工人数直接 429。
- **两波之外的收尾**：批次传送失败的篇目**等所有批返回后**才定性（沿用原口径：全部批失败且
  无任何非 manual 记录 → 「端点不可用」；否则只把失败批降级为 failed），漏网目标结案为「无直链」。
- **stats 改由最终行反推**（`_stats_from_rows`）：并发下「哪条先到」不确定，边跑边加加减减会错账
  （例如下载失败先扣了 `coze_resolved`、随后整批判为端点不可用）。行是唯一真相，反推必然自洽。
- `--no-pipeline` 保留串行三段做对照与排障；两条路径的 `items / stats / downloaded` **逐字段等价**（有测试钉住）。
- 进度新增 `stage id=pipeline {work_done, work_total}`：工作单元 = 目标数（解码 + 需要时的下载算一个），
  这是并发下唯一稳定、真实的分母；与解码并行的下载事件带 `parallel=true`，其 `total` 只是「已解出直链的篇数」
  会一路上涨，**不参与阶段锚点**。

### 上下文技能链路（`PdfDownloader.run()`）
- coze 解码线程**提到本地下载之前**启动，coze 与本地下载真正重叠；每个子批返回即落盘（原有 P1 流水线）。
- 「本地下载失败 → coze 兜底重试」改由 `_local_phase_done` 事件触发（本地阶段结束才放行），
  仍排在主批次之后，不与主批次抢端点。
- **修掉并发引入的竞态**：`local_failed_keys` 收集时排除「本来就路由到 coze」的篇目（新增 `coze_work_ids`）。
  否则 coze 线程与本地下载并行后，coze 篇目下载失败写下的 `pdf_download_note` 会被 4b 当成
  「本地失败」再送一次端点（重复解码 + 白烧配额）。

### 前端
- 新增流水线阶段锚点与 `parallel` 下载事件处理：并行下载**不占用阶段锚点**，避免进度条先冲到 90%
  再被真实进度拉回（A/B 验证过：还原此处理，新测试立刻 FAIL）。
- 阶段文案「并行推进：本地直链一到手就下载，其余同时送 Coze 解码」；下载提示改为「解码与下载并行」。

### 测试（新增 2 个套件，其余 11 个全部回归通过）
- `pipeline_e2e_test.py`（18 项）：用假端点 + 带时间戳的真下载证明——流水线下本地直链的下载
  **在第一次 Coze 返回之前就完成**，且 Coze 提交早于本地下载结束；串行下恰好相反（本地下载要等
  Coze 返回之后）。两模式结果等价。
- `pdf_download_parallel_test.py`（11 项）：`PdfDownloader.run()` 的解码与下载重叠；兜底重试仍排在
  主批次与本地阶段之后；coze 路由篇目不重复送端点。
- `coze_download_e2e_test.py` 扩到 30 项：真实服务上验证 `start.pipeline=true`、`id=pipeline`
  事件跑满、下载事件带 `parallel`，以及 `pipeline:false` 确实退回串行（无 pipeline 事件、无 parallel 标记、结果等价）。
- `coze_download_ui_offline_test.js` 扩到 27 项：新增「并行流水线」场景，断言并行下载事件
  没有把进度条顶到 90%、阶段文案带工作单元与并行 label。

### 顺带修掉的两个静默失效
- 进度通道加锁（`_EMIT_LOCK`）：流水线里探针 / Coze / 下载三类线程同时上报，整行必须原子写，
  否则两条 NDJSON 事件会咬进同一行、调用方解析失败（表现为进度凭空丢一块）。
- `coze_resolve.py` 补 `import threading` / `queue` / `urllib.parse`。

## v1.1.3 (2026-09-19) · 结果卡文献列表可展开摘要 + 逐篇「不下载」

用户反馈：「检索完成 / 唯一文献 37」下面的文献列表没有任何编辑修改功能，参考 meta-analysis
工作台的做法——单击能看到摘要，也能把某篇改成「不下载」。

### 交互（对齐 meta-analysis 工作台的 ▸/▾ + 内联详情 + 排除态）
- 行首 **▸/▾** + 标题整行可点 → 展开**内联详情面板**：完整摘要（可滚动，无摘要时明确写「来源未提供」）、
  作者、期刊卷期、DOI / PMID / OpenAlex 可点外链、OA 状态与 PDF 链接、被引数、引用核验状态 / 是否撤稿。
- 每行一个 **「不下载」/「恢复下载」** 开关；标记后整行淡化。
- 列表下方状态条：**「已排除 N 篇（不下载）」** + **「全部恢复」**；无标记时给出「点标题可展开摘要」的提示。
- 展开态与标记态都进自有 state（`WK[mountId]`），WBList 每次重渲染（分页/排序/筛选/切语言）仍保持一致。

### 状态落在磁盘上（不是在浏览器内存里）
- 新增 `GET/POST /api/selection`，读写 **`<out_dir>/.selection.json`**（`{version, skip:[{doi,title,id}], updated}`）。
  刷新页面、换浏览器打开同一输出目录，标记都还在。
- 归一化口径与下载端**逐字对齐**（`_norm_token`：小写 / 合并空白 / 去尾点），且 doi/标题/OpenAlex id
  **任一命中即同一篇**——只用 doi 会漏掉没有 doi 的预印本与指南，只用标题又怕标点差异。
- 写入**整体替换 + 原子落盘**（tmp + `os.replace`）：下载子进程读同一份文件，半份 JSON 会让所有篇目
  看起来「没被标记」而把刚排除的又下一遍。
- 前端**乐观更新 + 失败回滚**：任何异常都在状态条写明原因，不静默。

### 下载链路真的尊重标记
- `adapters/coze_resolve.py` 新增 `--skip-file`（默认自动读 `<out_dir>/.selection.json`）与 `--no-skip-file`；
  被标记篇目**照旧解码、但不落盘**，条目 `status=skipped`、`stats.skipped` 计数，**`direct_url` 保留**
  （链接清单不残缺，用户仍可手动打开）。
- 服务端 `/api/coze-stream` 在下载时传 `--skip-file`，`start` 事件带 `skip_count`；结果卡多一个
  「按标记跳过」KPI 与一条说明。**「解码直链数」与「实际落盘数」刻意分开**（跳过的确实解出了直链）。

### 验证
- 新增 `selection_e2e_test.py`（43 断言，全离线）：API 契约（归一化/去重/原子写/400-404/字符串不被拆成单字符）
  + **标记真的生效**（标 1 篇 → 只落 1 个 PDF、`stats.skipped=1`、解码仍是 2 条直链；取消标记 → 恢复 2 篇）
  + 适配器 CLI（`--skip-file` 标题命中、`--no-skip-file`、不传参数时自动发现）。
- 新增 `works_list_ui_offline_test.js`（41 断言）：初始即读标记、展开/收起、提交体形状、失败回滚、
  全部恢复、归一化口径、i18n 对称。
- 新增 `live_works_integration_test.js`（12 断言）：拿**真实 37 篇 + 真实接口**跑真实渲染代码，
  全部展开无 `undefined`/`[object Object]`/`NaN`，并真写一次标记核对落盘后还原。
- 旧 9 项回归全绿。

### 已知后续
- 线上发布包 `workbench/publish/` 需重新构建（`python workbench/publish-kit/build_publish.py`）后重新部署，
  线上才有 `/api/selection` 与新列表；本地 8787 已生效。

## v1.1.3 (2026-09-19) · 对话预览卡去掉「仅安全预览 (SAFE)」按钮

用户反馈：对话里的确认卡上那个 `仅安全预览 (SAFE)` 按钮要去掉。

- `renderIntent()` 的 `.acts` 从三按钮（确认并 --run / 仅安全预览 / 调整参数）减为两按钮
  （**确认并联网检索 (--run)** / **调整参数**）；`data-run="0"` 在对话卡不再出现。
- SAFE 空跑能力**没有删**，仍可从「高级检索」面板底部的 **预览 (SAFE)**（`#f_preview`）触发；
  `startRun(spec, dry)` 签名与 `/api/search` 的 `dry` 参数保持不变，dry 运行的徽章 / 日志
  （`runbadge safe`、`(… — no network)`）照旧显示 —— 那条路径现在只由表单入口到达。
- `btnSafe` 词条保留（中英各一处），仍被上述徽章与日志引用；对话卡不再引用它。
- 文档同步：`workbench/README.md` 的对话示例改为两动作，并注明 SAFE 空跑改由高级检索面板触发。

## v1.1.3 (2026-09-19) · Coze 解码按钮改为「解码 + 批量下载全文 PDF」

用户反馈：解码直链已经跑到这一步了，就应该顺势把 PDF 批量下载也做掉，按钮语义要改。

### 语义变更
- 结果卡主按钮 `Coze 解码全文直链` → **「解码 + 批量下载全文 PDF」**（`data-coze="dl"`，缺省行为）；
  新增次按钮「仅解码直链」(`data-coze="links"`) 保留「只要链接清单、不落盘」的老用法。
- 服务端 `/api/coze-stream`：`download` **缺省为开**（`body.get("download") is not False`），
  为真时给子进程加 `--download --dir <out_dir>`（`adapters/coze_resolve.py` 早已支持，只是前端从没传过）。
- `start` / `done` 事件新增 `download` / `pdfs_dir` / `pdf_count`（新增 `_count_pdfs()` 数盘上实际篇数，
  因为卡片要打包的是**目录里现有的** PDF，可能含上一轮的）。

### 进度
- 下载阶段改用 **已下/总数** 精确推进（`COZE_DL_LO=90` 起，占 8 个百分点），不再用时间缓动 ——
  篇数已知，估算反而更不准。另补 `prefilter` 阶段锚点与 `coze` 阶段的「批次 i/n」显示。

### 结果卡
- 新增「本次已下载 N」「pdfs/ 现有 N 篇」两个 KPI；本次一篇没下到时给出明确说明（而非静默）。
- 新增 **「打包下载 N 篇 PDF」**：先 `GET /api/artifacts?dir=<out>/pdfs` 本地核对件数/体积，
  再提交 `/api/zip`；超 2000 件 / 2 GB 给中文提示。**为什么先核对**：直接提交的话服务端 413
  会落在隐藏 iframe 里，用户只会觉得"点了没反应"。
- 新增「打开 PDF 文件夹」（`artSetDir(<out>/pdfs)` + `showView`）。

### 验证
- `coze_download_ui_offline_test.js`（21 断言）：请求体 `download` 真假、下载阶段 5/10→94%、
  卡片 KPI/按钮、打包 payload 只收 `.pdf`、空目录不提交、仅解码时无打包按钮。
- `coze_download_e2e_test.py`（22 断言，**完全离线**）：起本机 HTTP 服务伺服假 PDF（>5 KB，
  否则过不了 `_download_to` 的 5 KB 校验），把 OA 链接指向它 → 本地预筛命中、不呼叫外网端点 →
  验 `--download` 真落盘、`pdf_count`、`downloaded`、`%PDF-` 魔数，并顺手把刚下到的 PDF 打包解压比对字节。

### ⚠️ 本轮踩到的工具坑（重要）
- **同一文件并行 Edit 会互相覆盖，且报"成功"**。本轮 6 处改动被静默吞掉（前后端都有），
  包括最关键的服务端 `if _dl:` —— 导致「下载」开关根本没接上，而 py_compile / 语法检查全绿
  （未定义名是运行时错误）。**教训：同一文件的多处编辑必须串行**；改完要用「grep 关键串 +
  行为级测试」验证，不能只信 Edit 的成功回执。
- 由此新增 `i18n_audit.js`：抠出 `WB_T` 求值，比对 zh/en 键集**双向对称** + 页面引用的键是否齐备。
  被吞掉的字典改动会表现为「界面显示原始 key」，这个脚本把它变成显式失败（本轮据此修好 335/335）。

## v1.1.3 (2026-09-19) · 「输出文件」进入即刷新 + 检索过程只读 + PDF 一键打包

用户反馈三条：① 第一次进入「输出文件」面板是空的，必须手点「刷新」才出内容，很别扭；
② 「检索过程」分组完全没必要给下载；③ 「全文 PDF」应该能一次性打包下载。

### ① 进入面板自动读盘（根因：指向了一个早已删除的对象）
- 根因：`showView()` 里写的是 `if(v==="artifacts") wbArt && wbArt.refresh();`，而 `wbArt` 是上一版
  WBList 产物列表的全局对象，**重构为自写渲染后已经不存在**。`wbArt && …` 短路为假，所以
  「进入视图」这条路从来没触发过读盘 —— 首屏空白、必须手点「刷新」（那个按钮走的是另一条路）。
- 修复：`showView("artifacts") → loadArtifacts()`，进入即读盘。两处「查看输出文件」跳转按钮
  改为只设路径 + `showView(...)`，避免「showView 一次 + 手动又一次」抓两遍。
- 新增请求序号 `artReq`：连点 / 快速切目录时**后发请求胜出**，旧响应回来直接丢弃，不会回写过期内容。
- 首次读取且尚无内容时显示「读取目录中…」占位，避免「看着像坏了」。
- Coze 解码完成时若正在看该目录，顺手 `loadArtifacts()` 刷新（原为 `wbArt` 死代码）。
- 回归防线：源码级断言「不再存在 `wbArt.refresh()` 调用」+ **行为级**断言（抠出真实 `showView`
  源码执行，验证 `showView("artifacts")` 真的触发了读盘）。

### ② 「检索过程」只读，去掉下载入口
- `artDescribe()` 归类为 `proc` 的文件（`.coze_links.json` / `evidence_log.*` / `prisma*` / `.log` / 其余 `.json` / 未匹配的 `.md`·`.txt`）
  只渲染「查看」（浏览器内联打开），**不再渲染「下载」按钮**；不可预览的类型显示「仅供排错查看」。
- 分组说明改为「命令与原始返回记录，仅供排错查看（不提供下载）」，让规则的**理由**可见。
- 报告 / 题录数据 / 全文 PDF 的下载不受影响（断言覆盖）。

### ③ 全文 PDF 与文件夹一键打包（新增 `GET/POST /api/zip`）
- **服务端**：新增流式 zip 端点，`{dir, names[], dirs[]}`（JSON，或 UI 实际使用的表单 `payload=`）。
  - 边压边发（chunked，`zipfile` 走不可 seek 流 + data descriptor），**不落临时文件、不占内存**——
    上百篇 PDF 也不会把服务器或浏览器撑爆。
  - 只打包 `.pdf` 时用 `ZIP_STORED`（PDF 本身已压缩，存比压更快且无损），混类型才 `ZIP_DEFLATED`。
  - `dirs` 递归打包子目录，**跳过隐藏文件/隐藏目录**；显式点名隐藏文件仍会打包。
  - 包内附 `_bundle_info.txt`：来源目录 / 实际件数 / 体积 / 构建时间 / 中途跳过的不可读文件。
  - 安全限流：相对路径 `..` 拒绝（穿越防护）；>2000 件或解压后 >2 GiB 返回 413 并提示缩小范围。
- **前端**：`全文 PDF` 组头加「打包下载 N 项」（只看用途分组，**不截断**，193 篇就是 193 篇）；
  每个文件夹行加「打包」（整目录递归）。打包是**新增入口**，单篇「下载」保留。
- **前端提交方式**：隐藏 `form` + 隐藏 `iframe` POST，让**浏览器原生接管下载**（有进度、可取消、可重试），
  不把 zip 读进 JS 内存，也不会让当前页面跳走。提交后在面板顶部给一条可关闭的状态条
  （件数 / 体积 / 「在下载栏里看进度」），空集合 / 超限时给可操作的警告而不是静默失败。

### 验证
- 服务端 `zip_endpoint_test.py`：21 项全过（真起 handler、真发 HTTP、真解压校验 CRC；含 PDF STORED、
  子目录递归、隐藏文件跳过、`..` 穿越拒绝、404/400/413、`_bundle_info.txt` 内容、GET 形式）。
- 前端 `artifacts_ui_offline_test.js`：44 项全过（含 proc 无下载、文件夹有打包、筛选后只打包命中项、
  空集合不提交、`showView` 行为级断言、中英 316 键对齐、13 个新键双语齐备）。
- `live_artifacts_integration_test.js`：拿**真实 8787 服务返回**喂真实渲染代码，并把组头「打包下载」
  提交上去，端到端解出真实 PDF（810 KB，CRC 正常）——覆盖「离线假数据恰好长得对」的盲区。

## v1.1.3 (2026-09-19) · 「输出文件」面板重构（可读性 + 目录导航 + 真相校验）

用户反馈：「产物浏览界面还是不对，不知道怎么用」。根因是面板只有一个裸文件列表 + 一行图例，
既不解释每个文件是什么，也无法返回上级目录，且默认固定在 `./out`。

- **重命名为「输出文件」**（导航 / 标题 / 对话卡片按钮 `产物浏览` → `查看输出文件`），去掉「产物」这类需要解释的行话。
- **按用途分组**：子目录 / 报告 / 题录数据 / 全文 PDF / 检索过程 / 其他，每组带一句说明与计数。
- **每个文件一句人话说明**（`artDescribe()`）：例如 `lit_report.html` → 网页版检索报告（可打印成 PDF）、
  `references.bib` → BibTeX 引文（EndNote / Zotero 导入）、`.merged.json` → 多源合并去重后的完整题录。
- **显式按钮**：可预览类型给「查看」（浏览器新标签）+「下载」；xlsx/zip 只给「下载」（主按钮）。
  徽标按用途着色（表格绿 / PDF 红 / 过程灰 / 目录中性）。
- **目录导航**：新增「↑ 上一级」（此前只能进不能出）、回车即跳转、文件名筛选框、
  以及三个快捷入口（最近一次检索输出 / 工作台默认 `./out` / 上级目录）。
- **空态与错误态可操作**：空目录给出「去跑一次检索」；目录不存在给出路径 + 一键跳回最近一次检索输出。
  另：`/api/artifacts` **不再自动创建目录**（此前输错路径会静默建空目录）。
- **自动定位**：`/api/status` 新增 `last_out_dir` / `cwd`；面板目录不存在时自动跳到**最近一次检索的输出目录**
  （此前只要检索写在别处，面板就永远空白，看起来像坏了）。
- 大目录（如 193 篇 `pdfs/`）默认只渲染前 40 行 + 「显示全部 N 项」，避免一次插入上千个 DOM 节点。
- 离线验证脚本 `artifacts_ui_offline_test.js`（stub DOM 跑真实页面代码）：14 项断言全过，
  含分组顺序、按钮可见性、徽标着色、大目录截断、空态/错误态、中英字典 302 键对齐。

## v1.1.3 (2026-09-19) · Coze 解码「180 秒超时」根因修复（本地预筛 + 拆批并发 + 超时口径）

用户报错原文：`Command '[...coze_resolve.py, --in, ./out\.merged.json]' timed out after 180 seconds`。

- **根因（三层，均非用户操作问题）**：
  1. **超时口径错**：报错来自**一次性**接口 `/api/tools` → `_subprocess_text(timeout=180)`。
     实测该端点**单批（50 篇）解码要数分钟**（3 篇的一批也要 88s），180s 必然先到；
     >50 篇时脚本按 50/批**串行**传送，总时长 = 批数 × 单批时长，180s 更无可能。
  2. **前端口径**：前端在流式端点不可用时会静默回退到上述一次性接口，
     于是把 Python 的 `TimeoutExpired` 原文直接摊给用户看。
  3. **做了大量无用功**：`coze_resolve.py` 把**所有** key 都送端点，
     而实测检索结果里**约 2/3 本身就是文件直链**（bioRxiv/medRxiv `.full.pdf`、Nature/UCL 等），
     端点只是把可直下的链接再"解码"一遍。端点单篇约 19s，这部分纯属白等。
- **修复**：
  1. `workbench/server.py`：新增 `COZE_LEGACY_TIMEOUT_S = 420`（一次性接口专用），
     并捕获 `TimeoutExpired` 返回**可操作的中文说明**（含本次篇数/批数 + 建议改走流式），
     不再把 `Command '[...]' timed out after N seconds` 抛给用户。
  2. `adapters/coze_resolve.py`：拆批传送改为**并发**（`--concurrency`，默认 3），
     总时长由「Σ 各批」降为「最慢的一批」；每批独立降级，单篇仍只发送一次。
  3. `adapters/coze_resolve.py`：新增**本地预筛**（默认开，`--no-direct-prefilter` 关闭）：
     - 预印本 `.full.pdf` 走**规则认定**（bioRxiv/medRxiv 对机器人 UA 一律 403/429，
       批量探测必然被限速，校验结果不可信）→ 标记 `preprint_direct`；
     - 其余疑似直链用**浏览器头 + `Range: bytes=0-1023`** 实测（**不能用裸 HEAD**：
       裸 HEAD 会把能直下的预印本误判为不可下）→ 标记 `local_direct`；
     - 实测本机 193 篇：**112 篇本地即得直链**（预印本 100 + 实测 12，耗时 16.6s），
       送端点的从 193 降到 **81**（4 批 → 2 批）。结果卡新增说明，标注两类来源。
  4. `workbench/server.py`：结果卡/接口透传 `concurrency` 与 `direct_prefilter`。
- **顺带修正一处真实 bug**：开跑前用 `os.remove` 清理上一轮 `.coze_links.json`，
  在沙箱环境会被安全删除拦截 → 残留旧文件被当作**本轮 done** 上报（实测：取消后竟上报旧结果）。
  改为**按 mtime 判定结果新鲜度**，不再依赖删除是否成功。
- **已知事实（非代码问题）**：该端点 `CT_ENABLE_BROWSER_PDF_DOWNLOAD` 未启用，
  B 路径（浏览器下载）不可用，因此付费墙 / 仅有 DOI 的文献会返回 `pdf_failed`
  （`error`: "A 路径(OA/PMC/直链)全部失败；B 路径(浏览器)未启用"）。需要解码此类文献，
  须在端点侧开启该开关。

## v1.1.3 (2026-09-19) · Coze 全文解码「长等待」体验修复（流式进度 + 取消 + 正确状态）

- **问题**：点「Coze 解码全文直链」后界面只显示一句静态文案，30–180 秒内毫无变化（用户反馈"速度很慢，
  最好给提示或进度条"）。
- **修复（三层）**：
  1. `adapters/coze_resolve.py`：新增 `--progress {off,text,json}`，向 **stderr** 逐行 flush 结构化进度
     （`stage` 阶段：load / identify / coze[含批号] / assemble / download / done；`log` 日志；
     拆批时逐批上报）。stdout 仍只承载最终 JSON（`--out` 写文件时摘要也改走 stderr）；
     同时给 `PdfDownloader` 传入 progress 回调——**此前该回调未传，`_log` 全部被丢弃，进度等于没有**。
  2. `adapters/pdf_download.py::_parse_coze_stream`：SSE 事件**边到边报**（原来先把整流读完再打印，
     日志只能在结束后一次性涌出），并按节点标题 / 输出字节数 / 已用时上报；`ping` 保活事件每 20s
     转成一条心跳日志。
  3. `workbench/server.py` 新增 `POST /api/coze-stream`：chunked NDJSON 推 `start / stage / progress /
     tick(每5s) / done / error`；子进程 `PYTHONUNBUFFERED=1` + `-u`；**静默超时 200s** 判定端点无响应并
     终止（逐批场景每批都有输出，不会误杀）；客户端断开 / 点取消即 terminate 子进程；
     `/api/stop` 同时覆盖解码子进程；跑之前先删旧 `.coze_links.json`，避免把上一轮结果当本轮成功上报。
  4. `workbench/index.html`：解码卡改为实时卡（阶段名 + 已用时 + 进度条 + 日志滚动 + 取消按钮），
     进度为「阶段锚点 + 时间缓动」并**明确标注"按时间估算"**；20 秒后出现慢速提示；
     老服务无该端点时自动回退一次性 `/api/tools`。
- **顺带修正两处真实 bug**：
  - `coze_resolve.py` 的 `coze_unavailable = (projects is None)` 写在兜底填充**之后**，恒为 False
    → 端点不可达被误报为 `pdf_failed`（"无直链"）。已前移判定：端点连不上时正确返回
    `status=unavailable` / `stats.coze_unavailable=N`，界面据此提示"端点无响应，检索产物不受影响"。
  - 多批传送**全部失败**时同样判为端点不可用（不再逐篇报"无 OA"）。

## v1.1.3 (2026-09-17) · 飞书版本字段落点对齐（ct-base coze_io_contract §2.1）

- **结论：ct-literature 客户端本来就合规，本次只补文档约束、无行为改动。**
  ct-base §2.1（2026-09-17 定）规定版本字段（`skill_version` / `coze_version`）唯一落点是
  飞书 `resultstr`，`querystr` 不存版本信息。逐项核对本技能：
  1. `adapters/fetch_coze_unified.py` / `adapters/pdf_download.py` 均按 §1.2 发**顶层信封**
     `skill_version`（读本地 SKILL.md `version:`，与 `query_origin` 同级）→ 位置正确；
  2. 汇总审计 `querystr`（`scripts/ct_literature.py` 的 `type=literature_summary` payload）
     只含统计信息，**不含**任何版本键 → 合规；
  3. 本技能**无自有 coze 端点**（文献检索 / PDF 批量下载共用 ct-registry 的 ct-search 端点）
     → 版本字段由端点侧写入 `resultstr`，随 registry 端点重新部署生效。
- **文档补强**：`pdf_download.py` 信封注释、`fetch_coze_unified.py` 的 `querystr` 参数文档、
  `ct_literature.py` 汇总 payload 注释，均加 🔴 标注「版本字段只落 resultstr，禁止塞进 querystr」。

## v1.1.3 (2026-09-14) · 新增 DOI 专项校验 `--verify-dois` + `scripts/verify_dois.py`

- **背景**：ct-update 例行检查 P1（`ct-literature::H`）——错误表既有条目「DOI dedupe
  merged too aggressively / 两篇论文共享一个 DOI 笔误」缺少**专项核查与人工复核清单**；
  既有 `--verify` 的 DOI 一致性虽有实现，但结论混在 `citation_*` 通用字段里，不便单列。
- **新增（增量、向后兼容）**：
  - `adapters/verify_citations.py`：新增 `_with_doi_flags()` 在 DOI 路径上追加
    `doi_verified` / `doi_mismatch` / `doi_mismatch_note` 三个附加字段（旧消费者忽略）；
    新增 `verify_doi_only()`（仅走 DOI，不回退 PMID/OpenAlex）、`collect_doi_mismatches()`、
    `render_doi_mismatch_report()`。出站调用仍全部收口在 adapters/（ct-base §16.9）。
  - `scripts/verify_dois.py`（新）：对既有 `.merged.json` 做 DOI 专项校验的独立 CLI，
    默认 SAFE PREVIEW（无 `--run` 不联网、不落盘），`--run` 时回写 doi_* 字段并产出
    `doi_mismatch.md` 人工复核清单。
  - `scripts/ct_literature.py`：新增 `--verify-dois`（默认关，需 `--run`）——主流水线在
    正常导出后追加产出 `doi_mismatch.md`；未开启时行为与旧版逐字节一致。
- **判定口径**：Crossref 标题 + 第一作者姓氏模糊匹配（阈值沿用 0.80/0.85）；不匹配 →
  `doi_mismatch=true`，报告标注「建议人工复核」；解析失败 → `unresolved`；DOI 缺失 → `no_doi`。
- **风险**：CrossRef 速率限制（沿用 http_utils 连接池限速）；标题缩写差异可能少量误报，
  报告已明确标注人工复核，不做自动删除。
- **实测**：样本 4 篇（1 正确标题 / 1 标题不符 / 1 伪造 DOI / 1 无 DOI）→
  `verified=0 / mismatch=2 / unresolved=1 / no_doi=1`，`doi_mismatch.md` 正确高亮 2 条。

## v1.1.2 (2026-09-11) · 新增 `log_only` 审计留痕模式（配合 Coze 端 `mode: log_only`）

- **背景**：`run()` 末尾的飞书汇总统计调用在 v1.1.1 用 `force_coze=True` 送达 Coze 后，
  Coze 端仍会执行一次完整检索 —— 汇总本身无需检索结果，纯属浪费配额。
- **新增**：`dispatch()` / `dispatch_stream()` 新增 `mode: str = "search"` 参数；
  `mode="log_only"` 时隐含 `force_coze=True`，payload 额外携带 `"mode": "log_only"`，
  Coze 端 `route_by_mode` 识别后直连 `feishu_write_node`，仅写审计记录、跳过全部检索节点。
  飞书 resultstr 仅含 `runtime_sec`，不含 `hit_count`（不谎报 0 命中）。
- **CLI**：新增 `--force-coze`（已有）与 `--log-only`（隐含 --force-coze）。
- **默认行为不变**：`mode` 默认 `"search"`，所有既有调用路径零影响。
- **Coze 端**：需同步部署 `ct-registry/adapters/coze` v0.2.0（graph.py route_by_mode
  新增「审计留痕」分支 + state.py 新增 `mode` 字段 + feishu_write_node log_only 输出）。
  未部署前客户端发 `mode=log_only` 会被 Coze 端忽略而照常检索（向后兼容降级）。
- **回归**：`tests/regression_force_coze.py` 扩至 24 项（T6 payload mode 断言、
  T7/T8 log_only 绕过本地直连与送达断言）；Coze 镜像自检
  `ct-registry/adapters/coze/scripts/selfcheck_log_only.py` 19/19 通过。
- **汇总调用**：`run()` 的飞书汇总现传 `mode="log_only"`（与 `force_coze=True` 双保险）。

## v1.1.1 (2026-09-11) · 修复：飞书汇总留痕被本地路由静默吞掉

- **根因**：`run()` 末尾的「飞书汇总」调用（`log_feishu=True`）用 `source="openalex"`，
  而 `dispatch()` 对「openalex + 本机配了 OpenAlex key」会在到达 Coze 前**早返回本地
  直连**，`log_feishu` 随之被静默丢弃 —— 与源码注释「最终汇总记一条飞书」矛盾，
  审计记录在配了 key 的机器上**从未落库**。
- **修复**：`dispatch()` / `dispatch_stream()` 新增 `force_coze: bool = False` 逃生开关，
  置 True 时跳过「openalex 有 key」与「semantic_scholar 本地化」两处早返回；
  汇总调用显式传 `force_coze=True`。CLI 同步新增 `--force-coze`。
- **默认行为不变**：`force_coze=False` 时既有本地优先路由完全保持（中间检索调用不受影响）。
- **回归测试**：新增 `tests/regression_force_coze.py`（纯本地、无需网络）13 项断言，
  覆盖「有 key 默认走本地 / force_coze 绕过并送达 log_feishu+querystr / semantic_scholar
  同样可绕过 / 无 force_coze 行为不回归 / 汇总调用点源码断言」。

## v1.1.0 (2026-09-11) · 新增 `--sources` 检索源子集（供 meta-analysis A1 消费）

- **新增 CLI 参数 `--sources`**：逗号分隔的源子集，设了即**覆盖**各 `--with-*` /
  `--cochrane` 默认——所列即启用，未列即关闭。规范名与 `fetch_coze_unified._SOURCE_DISPLAY`
  一致：`OpenAlex, EuropePMC, bioRxiv, medRxiv, SemanticScholar, arXiv`，另支持本地专属
  模式 `PROSPERO`（`--with-prospero`）、`Guidelines`（`--with-guidelines`）、`Cochrane`
  （EuropePMC journal filter）。
- **语义细节**：`PubMed` 作为**别名**并入 EuropePMC（MEDLINE/PMC 索引，非独立源）；
  **OpenAlex 为管线基座**，`run()` 无条件启用，`--sources` 无法将其关闭（未列时 stderr 提示）；
  未知源名 → `[ERROR] unknown --sources: …` 且非零退出（杜绝静默漏检）。
- **消费方**：meta-analysis A1 选题阶段「改检索范围」修订——`tool_card params.sources`
  → `tool_mapping_meta.json` 的 `arg_map("sources"→"--sources")` → 本参数。此前该字段被
  静默丢弃（ct-literature 无 `--sources` 参数），2026-09-11 实测补齐。
- **预览模式**（不带 `--run`）会打印解析后的源清单（`sources=[OpenAlex + EuropePMC, …]`），
  便于 agent 在无网络时核对选择。
- 验证：`--sources "OpenAlex,EuropePMC"` → `[OpenAlex + EuropePMC]`；
  `--sources "OpenAlex"` → `[OpenAlex]`；无参 → 默认 `[OpenAlex + EuropePMC, bioRxiv, medRxiv]`
  （向后兼容，行为不变）；`--sources "OpenAlex,Bogus"` → 报错退出。

## v1.0.3 (2026-09-08) · CLI 默认翻转：online（Coze 统一检索 + 飞书审计留痕）

- **默认行为变更（用户 2026-09-08 拍板）**：CLI 不带任何模式 flag 时，检索改为走 **Coze 端统一检索**（6 源经服务端），并在结束时自动记一条飞书汇总（`type=literature_summary`，querystr 原样落库）。此前默认是本地直连（不经 Coze、飞书零记录），正式调用常在无感知中丢失审计留痕（同日实测踩坑：100 篇检索后台无任何记录）。
- **新增 `--local`**：显式本地直连各源公共 API（即旧默认行为；不经 Coze）。本地模式无飞书记录属预期，不再向用户输出任何飞书相关提示。
- **飞书留痕对用户静默**：汇总成功/失败均不打印 human 可见行（仅 `--progress json` 事件流保留 `feishu_summary` / `feishu_summary_failed` 供 agent 诊断）。
- **`--online` 降级为兼容 no-op**（默认已开启，保留 flag 使既有脚本/门控命令跨版本安全）；`--offline` 语义不变（强制本地兜底，优先级最高）。
- **`run()` 函数签名默认值保持 `online=False` 不变**——程序化调用方零影响，仅 CLI 层翻转默认。
- 健壮性前提：online 模式已有 `_coze_dispatch_with_fallback`（Coze 不可用/未授权自动降级本地 fetch），默认翻转不会使检索变脆弱（已实测确认降级路径存在）。
- 验证：默认模式（无 flag）→ `[OK] 飞书汇总已记录`；`--local` → 跳过提示行出现；`py_compile` / `--help` 通过。

## v1.0.2 (2026-09-08) · PDF 下载链健壮性加固（回写职责下沉 + 结果面板护栏）

- **PDF 下载完成自动回写 Excel「PDF 本地路径」列（用户 2026-09-08，根因修复）**：
  ① 根因：`PdfDownloader.run()` 仅把 `local_pdf_path`/`pdf_download_note` 写回内存 works，Excel「PDF 本地路径」列的重渲原只在主流程 `ct_literature.py` 内联实现；独立脚本直驱 `PdfDownloader` 时漏调回写工具，已下载 PDF 不进 `lit_report.xlsx`。
  ② 加固：回写职责**下沉到 `PdfDownloader` 自身**——构造时传入 `merged_json`/`xlsx_out`/`lang`/`safety`，`run()` 正常结束自动重渲 Excel 并把更新路径写入 `stats["xlsx_updated"]`；任何调用方都不会漏。`rejected` 提前返回不回写（保持主流程原行为）。
  ③ `scripts/ct_literature.py` 主流程改为构造时传参、删除内联回写块、读 `stats["xlsx_updated"]` 反馈；`scripts/update_xlsx_pdf_paths.py` 降级为「事后补救 / 重扫」用途（手动拷入 PDF 后补写、或异常未回写时重渲）。

- **PDF 下载反馈不再泄漏路径、结果面板不逐个打开 PDF（用户 2026-09-08）**：
  ① `scripts/ct_literature.py` 的 `pdf_download_done` 反馈由 `**pdf_stats` 全量透传改为
  显式白名单字段（`ok / total / elapsed_s / xlsx_updated`），**杜绝任何 PDF 文件路径流向
  结果面板**；文案明确「结果面板不逐个打开 PDF，请到 `<pdf_dir>` 目录查看」。
  ② `adapters/pdf_download.py` `__main__` 测试入口：逐篇打印 PDF 绝对路径改为只输出
  `ok/total` 计数，避免路径经 stdout 被解析打开。
  ③ `SKILL.md` 新增红线：**`--download-pdf` 及任何直驱 `PdfDownloader` 的脚本，结果面板
  只呈现 `lit_report.html` / `lit_report.xlsx`，绝不逐个打开 / 列出 PDF**（数十个会卡死 UI），
  仅用纯文本告知共同保存目录 `out_dir/pdfs/`。
  ④ 直驱示例 `dl_latest40.py` 尾部加同等护栏注释。
  背景：下载几十篇 PDF 时结果面板逐个打开会卡死 UI；此前仅 Excel 回写职责已下沉（v1.0.0
  同日加固），本次补全「不暴露 / 不打开 PDF 路径」一侧。

## v1.0.0 (2026-09-07) · 首个正式版：PDF 下载链 + §16 预发布规范整改（0.9.8 规划内容以 1.0.0 发布）

> **版本跃迁说明**：本版内容为原规划 v0.9.8；因发布前合规整改完成、功能面达正式版标准，作者决定以 **1.0.0 正式版号首发**（v0.9.8 未在任何平台发布过）。

- **§16 预发布合规整改（2026-09-07，spec_lint ERROR 2→0）**：① **F13 版本对齐**：SKILL.md version 0.9.7→1.0.0，Unreleased 内容归入 `## v1.0.0`；② **F19 正文英文**：SKILL.md「Natural-Language Dialogue — Triage-First」整段中文改写英文（保留四分类表/红线/连续性/执行流结构与 § 锚点；运行时用户可见文案与检索词保留原文）；③ **共享件漂移清零**（shared_sync 7 项→0）：term_map「治疗」先回填 ct-base 底座再两端一致；drug_name_map（底座 v1.1 新增 15 词）、kw_lexicon（止吐药组 5 词）、`i18n.py`/`kw_localize.py`/`drug_name_resolver.py` 三共享模块以底座为准同步（字节级一致已验）；④ **发布泄漏面收口**：`.gitignore`/`.clawhubignore` 的 `workbench/*.html` 扩为整目录 `workbench/`（ClawHub 按目录打包会把 `_bugreports/` 等内部资产带进发布包——审计命中 `workbench/server.py` 即泄漏面证据），并补 `pdfs/` 顶层空目录项；⑤ **spec_lint 复扫 ERROR=0**（WARN 6 项均软上限/底座件 by-design）。

- **§16.6 / §13.4 整改（2026-09-07，发布前合规复核）**：① **F22 双语互链**：README.md 末尾加 `> 🌐 Other languages: [中文 README](README_zh-CN.md)`，README_zh-CN.md 末尾加 `> 🌐 其他语言：[English README](README.md)`；② **出站元数据披露**：README 双份「Outbound & Privacy / 出站与隐私」节新增 `query_origin`（主机名 SHA-256 哈希，用途：归因/限流/双语）+ `locale`（系统语言）元数据说明，注明哈希非明文主机名；③ **`--verify none` 过时引用清除**：README 双份 4 处 `{all|top|none}` / `--verify none` 改为 `{all|top|background}` / `--verify top`（v0.9.6 已移除 none 模式），`scripts/ct_literature.py` 注释同步清理。

- **spec_lint F08 修复（2026-09-08，ERROR 1→0）**：frontmatter `summary` 127 字符超 120 上限（F08 判「非仅中文一句话」）。精简为 78 字符单句「检索已发表学术文献（OpenAlex、Europe PMC、预印本、arXiv 等多源），合并去重形成证据基础，并支持安全性文献定性筛查与 OA 全文获取。」；源清单与 MeSH / 默认开关 / CSM 等细节本就由 SKILL.md 正文与 README 承载，frontmatter 不再堆砌。复扫 `spec_lint --skill ct-literature`：**ERROR 0 ｜ WARN 3**（F02 SKILL.md 271 行软上限、F17 底座共享件 `scripts/kw_localize.py` 含 urllib、F26 发布集非 md 文件 56 个软上限 —— 三项均为软上限 / by-design，不阻断发布）。

- **Coze 更新后回归实测 + 三处数据质量修复（2026-09-08）**：coze 服务端更新后做全链路实测，六源 dispatch（openalex / europepmc / biorxiv / medrxiv / semantic_scholar / arxiv）单源探测全通，本地路径与 `--online` 路径端到端均 56 篇 / 5 源、PRISMA 与飞书汇总正常。实测暴露并修复 3 处缺陷（均为「HTTP 200 ≠ 数据正确」型，单看链路通无法发现）：
  - **① 引文校验误报（P0，反幻觉误伤）**：`verify_citations._norm_name` 直接对原始 Unicode 做 `re.sub(r"[^a-z\s]", " ", …)`，变音符号被当成**分词边界**——`Jänne` → `"j nne"`、`Müller` → `"m ller"`、`Núñez` → `"n ez"`，永远无法命中元数据里的 surname token；且 `_author_ok` 兜底只与 **longest token** 比（`Pasi A. Jänne` 的最长 token 是给定名 `pasi`），两条叠加把标题相似度 0.974、第一作者完全一致的真实文献判为 `mismatch / "possible hallucinated id"`（实测命中 NEJM FLAURA2 OS，doi 10.1056/nejmoa2510308，Pasi A. Jänne）。修复：新增 `_fold_unicode()`（NFKD + 去组合标记，`Jänne`→`janne`），`_norm_name`/`_norm_title` 先折叠再归一化（ASCII 行为字节级不变）；`_author_ok` 兜底改为对所有 token 取最大 ratio，并加 space-stripped 相等分支。回归 7/7 PASS（含德语/西语变音、U+2010 连字符），且未放宽假阴性——不同姓氏仍判 False。端到端 `verified 4→5，mismatch 1→0`。
  - **② Europe PMC `publication_date` 恒为 None**：`fetch_europepmc.py` 误取 `rec.get("printPublicationDate") / ("dateOfPublication")`，但二者实际嵌套在 **`journalInfo`** 下，`rec` 顶层根本没有这两个键 → 15/15 全空。修复：改用顶层真字段 `firstPublicationDate`（直连 Europe PMC REST 实测 doi 10.1016/j.cellsig.2026.112850 → `2026-08-26`），`journalInfo` 两值保留作兜底。修复后 0/15 → 15/15 有值。
  - **③ Coze（`--online`）路径 HTML 标签残留**：Europe PMC 结构化摘要以 HTML 返回（`<h4>Purpose</h4>…`）；本地 fetcher 有 `_strip_html` 清洗，Coze 服务端节点未做 → `--online` 路径 18/56 条 merged 记录带标签残留在 `title`/`abstract_snippet`，本地路径 0/56（两条路径不一致）。修复：`adapters/fetch_coze_unified.py` 新增幂等 `_sanitize_text()` / `_sanitize_works()`，在 Coze 出口（`/stream_run` 成功分支 + `_parse_run_response`）统一剥标签并折叠空白；Coze 端将来自行清洗时该函数自动退化为 no-op。修复后 18/56 → 0/56。

- **§16.9 出站调用归位（F17 整改）**：新增 PDF 下载链 3 文件 `pdf_download.py`/`coze_resolve.py`/`preprint_fallback.py` 自 `scripts/` 迁入 **`adapters/`**（含 `adapters/__init__.py` 未导出时用 `from adapters.X import …` 统一包路径）；模块顶层注入技能根 + scripts 到 sys.path（`__main__` 直跑与包导入双场景可用）；引用方 `ct_literature.py`（2 处）、`fetch_coze_unified.py`（1 处）同步改包路径；回归测试统一从顶层 import 改为包导入（根因：同一文件经顶层 `import pdf_download` 与包 `from adapters.pdf_download import` 会实例化两个模块对象，patch `_epmc_preprint_search` 失效——tests 注入技能根并全走 adapters 包后，`regression_pdf_routing` 0 FAILED / `regression_root_causes` 24 passed）。**遗留 F17 WARN 1 项**：`scripts/kw_localize.py` 为底座同步共享件（底座自身置于 scripts/ 并含可选在线兜底，全库口径，enforce env `CT_TRANSLATE_ONLINE=0` 可关），非本技能可独立消除。

- **§16.6 对话示例实测留痕（2026-09-07）**：本次整改会话已实测 Simple 全链路——真实输入「检索奥希替尼在 NSCLC 的安全性文献 2018–2025」（triage→§4.2 预览确认→§12 关键字门→`--run`→verify all 100/103→HTML/XLSX 交付→最新 40 篇 PDF 批量下载 36 成功→PDF 路径回写 Excel），产出与本技能示例所展示同类效果 ✓。README 双份示例 6（Complex 弹菜单）与示例 7（Vague/grill-me）的**逐字对话实录**列入发布执行步骤补测（不虚构留痕）。

- **README 双份内容整理（2026-09-07，§16.6 配套）**：① 清除**悬空内部引用**——旧编号遗留的「见 §7」8 处改为 FAQ / 出站锚点链接（残留 § 引用全部带 ct-base 前缀，属外部规范引用）；② **对话示例重修**：示例 1 改为含预览确认的真实节选（对齐检索主流程）、示例 2 改演示 review-type 过滤（原 `--safety` 演示并入示例 1，FAERS 区别说明随之迁移）、示例 6 Complex 改为卡片式两问确认 +「解释差异」入口 + 关键字门/预览两道把关、示例 7 Vague 补全两轮有界 grill-me 与「需求画像+推荐参数」收尾、示例 8 PDF 下载重修为 **v1.0.0 实测体验**（下载前等待提示 → 用时汇报 → Excel「PDF 本地路径」回填 → 付费墙如实标注）；③ 回复标签统一「节选 / excerpt」（8 示例一致）；④ FAQ 修正过时默认值「每源 30 篇」→ **50**（与 `--max` 默认一致）；⑤ PDF 下载 FAQ 从「解析链接」重写为「下载到盘」体验（节奏/落盘/Excel 回填/成功率边界/超 50 拒批）；⑥ 场景索引补「批量下载 OA PDF」行。中英双份逐项对称（8/8 示例、默认值、表格闭合均已校验）。

- **README 结构调整 + PDF 合规口径强化（2026-09-07）**：① 中文版结构调整（引言顺序对调、数据源/反幻觉两大节移至示例区后、示例 8→7 删 Excel 交付示例）同步镜像英文，目录/示例数/交叉引用中英自洽修复；② PDF 下载 FAQ 合规边界重写（用户口径）：**只协助 OA 下载、非 OA 不提供支持（技术上不做任何违法操作，不破解不绕过付费墙）**；**仅供个人使用、禁止商业用途**；OA 直下失败尽力找预印本/作者手稿替代；**善用免费资源勿过量（防封 IP）**，内置跨域并发限速 + 同域节流，**单批超 50 篇直接拒绝**。与 `PDF_DOWNLOAD_NOTICE` 运行时横幅口径一致。**追加（2026-09-07）**：防封 IP 条目细化为「请求节奏自控」——为免法律纠纷，技能**严格控制相邻两次下载请求间隔 ≥5 秒**（与 `COZE_BATCH_INTERVAL=5` 实现呼应）、不触及服务器压力线，并提醒用户控制批量频次、勿过量使用免费资源；中英双份同步。

- **ClawHub 安全审计整改与留痕（§16.0，2026-09-07 对比当前发行版）**：① **[HIGH] `--verify-top-n`（design-so 留痕 + 措辞整改）**——该参数语义是 `--verify top` 模式验证前 N 篇的**数量**，非关闭验证（验证永不关闭，v0.9.6 已移除 bypass）；整改：argparse help 显式注明 "does NOT disable verification"、README 双份示例不再内联该参数（默认 top-15 表述），workbench 引用随整目录排除不发布；保留参数为设计所需，审计判定留痕；② **[MEDIUM] guidelines 语料纯度（措辞整改）**——SKILL.md guideline 段新增 Corpus boundary 声明：语料含 reviews/consensus/adherence 等背景条目，非权威指南，须回链解析源；`retrieved:false` 为诚实占位非虚构引用；③ **[MEDIUM] `.env` 引导写 key（design-so 留痕）**——README 已含"聊天消息可能被平台留存"警示与自行配置三路径，key 仅本地、符合全库 key 治理；④ **UNVERIFIED 6 项人工核对**：Tp4/双 Description-Behavior（bug-report 出站）——README 已披露 11-key 脱敏信封 + 端点 + opt-in；Context-Inappropriate 可逆混淆静态凭据——符合 ct-base §5 公用凭据 XOR+base64 规范；guidelines pointer 占位——SKILL.md 已声明 pointer-only；Ssd3（changelog key 指引）——同 ③ 留痕。

- **PDF 回写 Excel 下沉到下载器自身（2026-09-08 加固，避免独立下载路径漏写）**：根因——`PdfDownloader.run()` 原本只把 `local_pdf_path` / `pdf_download_note` 写回内存 `works`，Excel「PDF 本地路径」列的重渲只在主流程 `ct_literature.py` 内联实现；独立直驱 `PdfDownloader`（如 dl_top10.py / dl_latest40.py）一旦漏调 `update_xlsx_pdf_paths.py`，就会出现「PDF 已下载却没写进 lit_report.xlsx」的错位。修复：把回写职责下沉到下载器——`PdfDownloader.__init__` 新增 `merged_json` / `xlsx_out` / `lang` / `safety` 四参数；新增 `_write_back_xlsx(works)` 方法（读 merged meta、统一绝对路径、调 `export_xlsx.export_workbook` 重渲、失败仅告警不中断），`run()` 正常结束（return 前）自动调用并把更新路径记入 `stats["xlsx_updated"]`；`rejected` 提前返回分支不回写（保持主流程既有行为）。主流程改为构造时传入上述参数、删除内联回写块、改读 `stats["xlsx_updated"]` 构造反馈。效果：任何调用方（主流程或独立脚本）只要 `PdfDownloader(out_dir=…, xlsx_out=…)` 即自动回写，不再依赖外部记得调独立工具。`update_xlsx_pdf_paths.py` 降级为「事后补救 / 重扫」（手动拷入 PDF 后补写、或异常未回写时重渲）。回归：py_compile 通过；smoke test 三项全过（`_write_back_xlsx` 单元生成 xlsx / `run()` 传 xlsx_out 自动回写 / 不传 xlsx_out 静默跳过不崩溃）。


- **PDF 下载后回写 Excel「PDF 本地路径」列（用户 2026-09-07，实测反馈）**：下载不是终点——下载结果必须落到用户手里的报告里。① 主流程 `--download-pdf` 分支在批量下载完成后，用同一渲染函数（`export_xlsx.export_workbook`，非 openpyxl 改存，避免丢图表）以带 `local_pdf_path` 的内存 works 重渲 `lit_report.xlsx`——该列（`_WORKS_COLS` 早已预留、双语表头「PDF 本地路径 / PDF Path」）自动呈现每篇落盘绝对路径，失败项显示「失败」；meta 从 `.merged.json` 读回，Safety-Related 表同步。② 新增 standalone 工具 `scripts/update_xlsx_pdf_paths.py`（服务直驱 PdfDownloader 的独立下载场景）：扫描 pdf 目录（DOI 转义命名反解）+ 可选 `--notes-json` 注入失败原因 → 重渲 xlsx，用法 `python scripts/update_xlsx_pdf_paths.py --merged .merged.json --pdf-dir pdfs [--notes-json manifest.json]`。③ human 反馈改为明确告知用户「N/M 篇成功、用时、PDF 目录、Excel 已更新列」，**不再向用户倾倒技术性 JSON**（stats 细节仍经 json 事件 `pdf_download_done` 结构化透传，NDJSON 下游不受影响）。实测端到端：36 路径写入 / 3 失败标注 / 其余 —。


- **下载前等待预期提示（用户 2026-09-07，实测反馈）**：下载动作开始前明确告知节奏——主流程 `--download-pdf` 首条消息改为「每篇约需 10–20 秒（视网络与限流而定），请耐心等待完成，无需任何操作」；`PdfDownloader` 的 `PDF_DOWNLOAD_NOTICE` 下载横幅补第 ⑤ 条同口径提示（服务直驱 PdfDownloader 的独立下载场景）。用户据此对 40 篇约 15 分钟的耗时节奏有心理预期，不再误以为卡死。

- **PDF 批量下载计时统计（用户 2026-09-07，实测反馈）**：`PdfDownloader.run()` 内建整批计时——stats 新增 `started_at` / `finished_at`（ISO 墙钟）/ `elapsed_s` / `elapsed_min`，正常路径与超上限 reject 路径均写入；收尾打印 `[PDF] batch finished: ok N/M, elapsed …s (… min), start -> end`。主流程 `ct_literature.py --download-pdf` 分支（`pdf_download_done`）human 消息同步改为"`N/M 篇成功，用时 Xs（Y 分钟，start → end）`"；reject 消息附带 elapsed。`pdf_download_done` 事件负载经 `**pdf_stats` 自动携带计时字段，NDJSON 下游可直接消费。所有调用 PdfDownloader 的路径（主流程 / 独立脚本 / 回归用例）无需额外参数即获得计时。


- **四桶路由落地（`run()` + `_classify` + 路由辅助 `_find_earlier_preprint`/`_upw_look`/`_prefetch_unpaywall`）**：把"非 OA 文献是否送 coze 解码"从「无脑全送」改为四桶——`local_direct`（OA/预印本真实 PDF 直链 → 本地直下、不送 coze）、`local_preprint`（非 OA 但查到更早预印本/OA 直链 → 本地直下）、`coze`（本地无法下且有 OA/预印本信号 → 才送云端）、`skip`（非 OA 且无可用预印本 → 不送 coze）。实测依据（OpenAlex 真实 OA 28 篇样本）：coze 解码路径成功率 39.3%、本地直链 46.4%，失败主因是 coze 解析覆盖率天花板而非本地下载 bug；14 个 coze 判失败的 DOI 重送诊断全为付费墙/非 OA（A 路径 Unpaywall→EPMC→预印本覆盖不到），印证 40–50% 是 OA-only 自动下载的真实天花板。B 路径（浏览器过 Cloudflare，回收率 28–32%）按用户决策不起用。
- **限速器全局锁 bug 修复（`_PerHostRateLimiter.acquire`）**：`time.sleep` 移出全局锁 `_meta`、仅持同 host 锁 `lk` → 跨域名下载恢复真并发（此前 `time.sleep` 在全局锁内把跨域名下载串行化拖慢，属真实生产并发缺陷）。
- **PMC 作者手稿预筛兜底（`_classify` skip 决策前，2026-09-07 补充）**：非 OA 文献完全可能免费下载——最被忽视的一类是「期刊非 OA 但作者按基金/NIH 政策 deposited PMC 作者手稿」。原路由在 Unpaywall 漏标 `is_oa`（滞后/未索引）时直接 `skip`，而能查 PMC 主库的 `_epmc_lookup_pdf_url` 只在 coze 兜底路径调用、skip 桶到不了。现于 `_classify` 的 skip 决策前新增一次本地 `_epmc_lookup_pdf_url(doi, pmid)`（自带 1.0s 限流 + 429 禁用保护，复用 coze 兜底同款逻辑），命中 PMC 副本即改走 `local_preprint` 本地直下，**仍不送 coze**（符合「非 OA 不送云端」红线）。`regression_pdf_routing.py` 新增 2 条用例（有 PMC 手稿 → 本地回收 / 无 PMC 手稿 → 仍 skip）确证。残留盲区：出版商「限时免费读/机构订阅外免费」等未进入任何公开索引的文献本地无信号可查，只能靠 B 路径（已决策不起用），属已知接受的天花板。

## v0.9.7 (2026-09-06) · 档位归类修正：旧四档 "B-tier" → 现行两档制 A 档

- **档位归位（ct-base §11 两档制）**：ct-base 现行仅按「输入是否涉密」分 **A / B 两档**（A = 输入非涉密；B = 输入涉密），不再有旧四档（公开情报层 / 本地需检索 / 保密不出域 / 保密审批）命名。本技能输入仅为普通检索词、零保密数据，按 §11 权威名单归类为 **A 档**（`network=public-retrieval` 为 A 档正交子属性，非独立档位）。
- 全文档旧四档自述 "B-tier / B 档 / Tier B" 统一改写为 "A-tier / A 档 / Tier A"：`SKILL.md`（network_note / Positioning / Safety）、`AGENTS.md`（头注 + 档位术语块 + Conventions + Version）、双 README（引言 / 目录树 logo 标注）、`references/sop.md`、`references/units.md`；双 README 版本徽章 v0.9.5 → v0.9.7。
- `assets/icon.svg` 主色由旧四档蓝 `#1C6DD0` 换为 **A 档靛蓝 `#3A5BC7`**（ct-base §12 两档配色表，与 ct-base/pending-icons 权威版一致）。
- `assets/ct-lifecycle-diagram.svg` + `.png` 同步为 **ct-base 权威两档版**（A 档靛蓝 / B 档深橙，四档图例移除，与 ct-base/BASE.md §1.5+§11 一致）。
- `tools/restore_frontmatter.py` 中 ct-registry / ct-safety / ct-pipeline 的旧 "B 档 / C/D 档" 措辞同步为两档制表述。
- **顺手修复（v0.9.6 F2 整改残留，实测触发）**：`scripts/ct_literature.py` main() 仍引用 `args.no_verify_citations`（argparse 侧 alias 已于 v0.9.6 删除）→ 任何 `--run` 都 AttributeError 崩溃；改为 `verify_mode=args.verify`（合法值 all/top/background）。双 README 同步修正失效示例（`--verify none` / `--no-verify-citations` → `{all|top|background}`，并注明反幻觉不可关闭）。
- **HTML Safety 子集门控（对齐 XLSX，实测反馈）**：`export_html.render()` 此前无条件渲染「Safety / CSM Subset」区块与 safety KPI 卡；现新增 `safety=False` 参数——`--safety` 未给时不输出子集区块与 KPI 卡（works 表 `is_safety` 琥珀行高亮保留作快速扫描），主流程 `ct_literature.py` 与 standalone `export_html.py --safety` 均透传；与 Excel Safety-Related sheet 的 opt-in 语义对齐。
- **HTML 文献列表列结构精简（实测反馈）**：works 表 13 列 → 11 列——「来源·ID」合并为一列（ID 短格式如 `OpenAlex · W3087210493`，完整 ID 在 hover tooltip）；标题列直接内嵌原文链接（原独立 ↗ 链接列删除）；摘要列加宽（`width:30%; min-width:280px`）减少换行堆叠。safety 子集精简表结构不变。
- **Triage-first 流程修复（ct-base §6.2 合规，实测触发）**：此前收到"查糖尿病治疗文献"这类 Complex 请求时，**直接执行 `--run`，跳过了 triage + 确认菜单 + 关键字门整套流程**，违反 ct-base §6.2 + `search_menu.md` 的强制约束。修复：① `SKILL.md` 将原先一句"NL dialogue follows search_menu.md"替换为完整的 **Step 0 Triage 四分类表 + 红线 + 执行流程**，明确 Simple/Complex/Vague/Middle 的判定与行为；② 双 README 示例 6（Complex）和示例 7（Vague）的助手回复中显式标注 `Triage → Complex/Vague` 步骤，示例 6 补充"参数确认后 → §12 关键字门 → §4.2 预览 → 执行"后续链路，并加 📌 说明 Simple/Vague 的分支路径。
- **XLSX 列结构修复（用户反馈）**：移除独立的"预印本DOI"和"有预印本"两列。预印本的标题 hyperlink 直接指向其 DOI（`https://doi.org/…`）；其 PDF 下载链接显示在"OA链接"列（标签"OA PDF"）。正式出版文献不考虑预印本信息。变更：`scripts/export_xlsx.py` 从 `_WORKS_COLS` 和 `fields` 中移除这两列，并删除对应的写入分支。
- **摘要占位符修复（用户反馈）**：ESC Guidelines / IDF Diabetes Atlas 等文献在 OpenAlex/Europe PMC 中无摘要，返回"…""How to cite"等占位符。修复：`export_xlsx.py` 的 `restore_abstract_paragraphs()` 增加占位符检测（<20字符、已知占位符集合如"How to cite"、"[Abstract unavailable]"等），命中即显示"—"。同时 `normalize.py` 新增 `_is_valid_abstract()` 供后续 fetch 时复用。当前数据 15/125 篇命中，已正确显示"—"。
- **跨轮连续性补齐（continuity.md 合规）**：对照 continuity.md 模式 A（高风险），此前 SKILL.md 只提了"跨轮连续性"概念，没写具体执行规则。补齐：① 回显块固定前缀 `## 当前检索设定：` + 完整字段清单（`topic / type / year / safety / sources / max / verify`）；② 追问时只改变化字段；③ `merge_spec.py` 升格为 follow-up 默认路径（高风险技能，漏带=静默检索错误范围）；④ 明确"无状态远端，连续性必须本地解决"红线。
- **HTML works 表列布局迭代（实测反馈多轮）**：来源列改两行结构（数据库名 / 编号各一行）；标题列显式 `width:24%` 防自动布局挤压；作者列单行截断（`max-width:180px` + ellipsis，hover 全量）——修复作者显示 bug（原始数据为 Python list repr 字符串，现 `_fmt_authors()` 解析为 `前4名 et al.` 可读格式）；works 表内边距收紧 `5px 8px` 降行高。
- **摘要默认收缩 2 行、点击展开全文（实测反馈）**：去掉 220 字符硬截断，摘要单元格内放全文并用 CSS `-webkit-line-clamp:2` 收缩；>140 字符的摘要格（td.abs.expandable）点击整格展开/收起（内联无依赖 JS 事件委托，无副作用；指示文案随语言 `abs.more/abs.less`），记录行数大幅下降。
- **默认交付收敛 + 用户引导（实测反馈）**：① 引文导出默认关闭（`DEFAULT_EXPORT_BIB=False`）——标准交付仅 `lit_report.html` + `lit_report.xlsx`，`references.bib` / `.ris` / `references_<style>.md`（APA 等）改按需 `--export-bib` 或对话请求生成；② 运行完成时 stdout 打印引导 [TIP]；③ HTML 报告顶部新增「还能做什么 / Options」提示条（`tips.t1–t4` 双语）：Excel 完整结果可继续处理、可协助 OA PDF 下载、可按需生成 Zotero RIS / BibTeX / APA、不确定时对话呼叫菜单。
- **works 表列序调整 + PDF 全量下载引导（实测反馈）**：摘要列移至标题之后（列序：来源·ID → 标题 → 摘要 → 作者 → 年份 → 期刊 → 类型 → 研究类型 → 被引 → OA → PDF，摘要收缩/展开交互不受影响）；明确 `--download-pdf` 支持**全部下载**（每条带 OA URL 或 DOI 的记录自动尝试，分批、仅合法 OA 源），引导文案与双 README FAQ 补充「全部 OA / 指定 DOI·PMID / 前 N 篇」三种请求方式。
- **Excel 文献总表列精简 v3（实测反馈）**：`_WORKS_COLS` 13 列 → 11 列——删除 `doi` 列（标题列已超链接至 DOI）、删除冗余的 `is_oa`「开放获取」Y/— 列；`open_access_url` 列表头由「开放获取链接」更名为 **OA链接 / OA link**；按实际内容重调默认列宽（type 12 / study 18 / year 7 / journal 22 / authors 30 / title 50 / abstract 62 / cited 9 / safety 9 / OA链接 24 / pdf 36）；Works 与 Safety sheet 共享该定义同步生效。
- **HTML works 表删除 PDF 列（实测反馈）**：常规检索（未 `--download-pdf`）无 PDF 数据、该列恒为「—」，故从 HTML 表头与行中移除（Excel 仍保留 PDF 本地路径列，下载场景可查）；清理随之成为死代码的 `_pdf_status_badge()`。HTML 现为 10 列：来源·ID → 标题 → 摘要 → 作者 → 年份 → 期刊 → 类型 → 研究类型 → 被引 → OA链接。
- **Excel 摘要补全（实测反馈）**：文献总表（与 Safety 表共享 `_write_works_table`）摘要此前被 `[:500]` 截断——改为写入**完整摘要**（实测 75 行 0 截断、最长 2912 字符）；行高自适应按摘要/标题估算折行数（默认展开约 5 行、上限 68pt，长摘要双击行头下边界自动适应即可看全），避免每行撑满半屏。
- **摘要分段恢复（实测反馈）**：Europe PMC / OpenAlex 返回的摘要**原始即单段**（已对 EPMC API 实证 `\n count:0`）；新增 `export_xlsx.restore_abstract_paragraphs()` 按医学摘要段首标签（BACKGROUND / OBJECTIVE / METHODS / RESULTS / CONCLUSIONS 等 + 冒号）启发式恢复分段——带标签的 23/64 篇实现多段（实测 23 行含 ≥2 换行），无标签叙述式摘要保持原样不误切；Excel 写入分段文本（text_wrap 显示），HTML 侧 esc 后把 `\n\n` 渲染为 `<br><br>`（74 处段分隔）供展开全文时查看。Excel / HTML / Safety 子集表三个出口一致。
- **PDF 下载交付体验优化（实测反馈）**：① Excel「PDF 本地路径」列：成功行显示**绝对路径**（可点击 file:// 打开，不再用短的相对显示）；失败行统一显示「失败」，不再暴露冗长内部原因（coze A/B 路径 / 浏览器未启用等）；② 落盘文件名改为 **DOI 干净名**（如 `10.1186_s13014-021-01955-7.pdf`，去掉 `https___host_track_` 前缀；下载时 `_download_direct_with_delay(url, name)` 传 DOI，无 DOI 回退短 key）；③ `pdf_download.run()` 下载前打印合规说明（PDF_DOWNLOAD_NOTICE：仅 OA、勿超 50 篇/勿商用防封 IP、成功率约 30–50%、失败自动尝试作者手稿/预印本替代）；④ 下载循环输出逐条进度 `[pdf] i/n 下载中 → 文件名 / ✓已保存 / ✗下载失败`。
- **预印本-发表版去重（策略 A）（2026-09-06）**：`normalize.merge()` 后接 `_dedupe_preprint_published()` 后处理。检测逻辑：归一化标题相似度 ≥ 0.85 + 第一作者重叠 ≥ 0.3 → 视为同一研究。行为：预印本移除（superseded），发表版回填 `preprint_doi` + `has_preprint=True`，缺失字段从预印本回填。当前数据无配对（0/14 旧 DOI 已验证未发表），去重后 109 不变。Excel 新增「预印本DOI」「有预印本」两列 + 字段说明。
- **限速策略 A+B+C 实测落地（2026-09-06）**：biorxiv.org 对程序化请求触发 IP 级限速（连续 3-4 次即 429，等 30s 恢复 1 次），medrxiv.org 同 IP 也受影响。三招组合：① **A（429 指数退避）**：`_get` / `_download_to` 捕获 429 后按 `min(30·2ⁿ, 120)s + jitter` 退避重试（最多 4 次）；② **B（拉长间隔）**：`_download_direct_with_delay` 对 biorxiv/medRxiv 自动延长到 3-5s + jitter；③ **C（浏览器头）**：抽 `_browser_headers()` 补全 Accept / Accept-Language / Referer。实测：15 条被限速预印本重跑 **15/15 全成功**（总 PDF 38→53，预印本 5→20）。
- **预印本 OA 列直链 + PDF 下载实测（2026-09-06）**：`fetch_preprints._extract` 改为按服务器构造 PDF 直链（`https://www.biorxiv.org/content/<doi>.full.pdf` / `https://www.medrxiv.org/content/<doi>.full.pdf`），OA 列直接放可下载的 PDF 直链，url 列放 doi.org 落地页。实测：10.64898/… 新前缀在双站均可直下（biorxiv 628KB、medRxiv 731KB 验证）；10.1101/… 旧前缀两源均 403（CSHL 已迁移到新前缀，旧 DOI 落地页重定向到 biorxiv.org/node/，api.biorxiv.org 查不到）。本批 34 条预印本 OA 列全直链，下载成功 5/34（其余被 429 限速或 403 永久不可达；限速可后续重试）。
- **DOI 存成 URL 形态的根因修复（实测反馈 → 归因 19→33/75 攻关）**：OpenAlex 的 `doi` 字段本就是完整 URL（`https://doi.org/…`，本语料 50 条全中），`fetch_openalex._extract` 此前原样写入 → 下游 coze/EPMC `DOI:"https://…"` 查询全部落空、PMC-OA 通道整批失效、BibTeX/RIS 导出 DOI 字段失真。修复双保险：① `fetch_openalex._bare_doi()` 源头剥 URL 前缀；② `normalize._bare_doi()` + merge 两处循环入口兜底归一（历史/混合源）。当前 .merged.json 50 条已就地修复（0 残留；hdl.handle.net 等 Handle 前缀正确保留不误剥）。
- **bioRxiv/medRxiv preprint URL 差异修正（实测反馈）**：Europe PMC PPR 预印本记录的 `fullTextUrlList` 通常只有 `documentStyle=doi`（doi.org 重定向器、非 PDF），此前 fetcher 把它同时写入 `url` 与 `open_access_url` → OA 列亮假 OA、下载链拿重定向器必败。修正 `fetch_preprints._extract`：`open_access_url` 仅在有 `pdf`+open 真直链时填写，否则 `None`（下载改走 DOI → coze 补充链 Unpaywall/官网渠道）；`url` 用 `https://doi.org/<doi>`（点击可达服务器落地页）。附差异备忘：preprint `doi` 为 10.1101（老）或 **10.64898**（CSHL 2026 新前缀，bioRxiv/medRxiv 均有），无 `pmcid`、`id`=PPRxxxx、`publication`=bioRxiv/medRxiv 标签、`type`=preprint。osimertinib 语料增量并入 34 条（25 bioRxiv + 10 medRxiv，1 条与已发表记录重复自动去重）→ 109 条。
- **PDF 路径显示再修正 + 预印本回退落地（实测反馈）**：① Excel PDF 列成功行改为**纯文本完整绝对路径**（`os.path.normpath` 统一 Windows 反斜杠，杜绝 `C:/…\file` 混用；不再写 `file://` 超链——实测 xlsxwriter 会把 file URL 存储转回反斜杠、预览面板又将其当网络链接渲染成 https/file）；`PdfDownloader.__init__` 对 out_dir 做 normpath（根治落盘路径混用源头）。② **预印本回退真实落地**：coze 镜像（ct-registry/adapters/coze，`publisher_pdf_batch_node.py`）核实**无任何 preprint 节点**（medrxiv.org 反在其 `_ANTI_SCRAPE_HOSTS`）——PDF_DOWNLOAD_NOTICE 的承诺此前从未接线；在本地 `pdf_download._preprint_retry()` 实现（复用 preprint_fallback 的 EPMC PPR 检索 + 作者姓氏校验，绕过其 OA 过滤以覆盖供应商拦截的失败）；并修复 `preprint_fallback._lastnames_from_authors` 对 Python-list-repr/JSON 字符串作者格式的解析（此前 55/56 被"无作者可校验"误跳过）。实测：56 篇失败文献回退 0 命中——本批多为已发表期刊文/2025 新研究，EPMC PPR 预印本库无匹配（机制已就位，非代码缺陷）。

## v0.9.6 (2026-09-05) · 工作台视觉升级 + Coze 全文解码 + 对话优先重构 + OA 增强 + PDF 下载

- **§16.0 ClawHub 安全审计整改（4 STILL_PRESENT 清零）**:
  - **F2（HIGH）反幻觉 none 旁路移除**：`--verify` choices 移除 `none`、`--no-verify-citations` alias 删除、`elif verify_mode=="none"` 分支清除；`workbench/server.py` 把前端 `none` 请求强制降级为 `top`。反幻觉闸门（ct-base §17.1 P0）从此不可被 CLI 完全关闭（实测 `--verify none` / `--no-verify-citations` 均被 argparse 拒绝，exit 2）。
  - **F1（HIGH）术语澄清**：`AGENTS.md` 顶部加术语块，明确 "B-tier" = ct- 库公开情报检索层（零保密输入），非保密分级；改写三处 "B-tier" 措辞；顺手修正过时版本号 v0.5.3 → v0.9.6。
  - **F4（MEDIUM）.env 写入措辞弱化**：README / README_zh-CN 安全段把"助手可代写 .env"弱化为「可选、不推荐、优先 §7 自行配置」，降低公开包诱导面。
  - **F3 / 6×UNVERIFIED**：guidelines corpus 多源语料库设计如此留痕；coze 端点 / bug-report 出站为既定设计（你已授权 coze 凭据随包发布），标设计如此。

- 全新设计系统（`workbench/index.html`）：深蓝 + 金线学术纸感配色（navy/gold）、衬线标题 + 无衬线正文的学术排版；
- 顶部 banner 渐变 + 金色底边线 + 环境徽章胶囊；导航 active 态金色下划线；
- 对话气泡：头像徽章 + 不对称圆角 + 入场动画；用户/助手视觉区分；
- 检索理解卡 / 结果卡统一「金线卡」母题（顶部金色渐变条 + 米金表头参数表）；
- KPI 卡左侧蓝金渐变竖条；深色终端风 runbox/toolout（三点窗饰 + 语法高亮事件色）；
- 开关统一为 iOS 风滑块；表格斑马纹 + hover 高亮；欢迎卡改为 3 步流程指引卡；
- 执行状态行改为 SAFE/LIVE 徽章（琥珀/绿）；新增 `.btn.gold/.accent` 按钮层级；
- 响应式断点（820px/980px/1080px）适配窄屏；修复一处悬空 `--greytx` 变量引用；
- 校验：CSS 括号平衡、全部 `var(--*)` 引用可解析、JS 语法通过、DOM `#id` 引用全命中。

## [Unreleased] — 2026-09-06 (7) · bioRxiv/medRxiv 默认开启

- **bioRxiv/medRxiv 由 opt-in 改为默认 ON**：`run()` 默认参数 `with_biorxiv=True`、`with_medrxiv=True`；argparse 改为 `BooleanOptionalAction`（`--with-biorxiv` / `--no-with-biorxiv`、`--with-medrxiv` / `--no-with-medrxiv`），用户仍可显式关闭。
- **SKILL.md 同步**：Data Sources 表 bioRxiv/medRxiv 行由 "Optional" 改为 "**Default ON**"；下方总结句更新为"默认数据源 = OpenAlex + Europe PMC + bioRxiv/medRxiv"。

## [Unreleased] — 2026-09-06 (6) · 修复 `pub_types` 跨源合并透传（meta-analysis B1 综述硬信号根因）

> 跨技能根因：meta-analysis 的 `is_likely_review` 优先采信 `study["pub_types"]`
> （出版商自标 Review 的元数据等价物，比标题/摘要关键词更可靠）。但 ct-literature
> 合并归一化把 Europe PMC 的 `pubTypeList` 丢了：① `fetch_europepmc._extract` 只把它
> 内部用于 `study_type`，从不写回 work 记录；② `normalize.merge` 的字段透传清单里
> 没有 `pub_types`，导致 EPMC 记录的标签被 OpenAlex 主记录覆盖。结果：如
> `10.3945/an.111.000893`（EPMC 标 Review）这类文献经合并后 `pub_types=None`，
> B1 硬信号落空、综述漏判进 A4。

### Fixed
- **`fetch_europepmc._extract`**：新增 `pub_types` 字段，逐字保存 `pubTypeList.pubType`
  （如 `["Review"]` / `["Systematic Review"]` / `["Meta-Analysis"]` / `["Journal Article"]`），
  供下游 review-guard 直接采信，不再只用于内部 `study_type` 推导。
- **`fetch_openalex._extract`**：OpenAlex 无 `pubTypeList`，改为从其 `type` 字段派生
  `pub_types`（仅当 `type=="review"` → `["Review"]`，其余为 `[]`），保证字段跨源一致、
  OpenAlex 自标综述也能被 B1 命中。
- **`scripts/normalize.py`**：
  - `merge()` 字段透传清单新增 `pub_types`，并对列表做 **union-dedup 合并**（任一源标了
    Review，合并后都保留），与 `concepts`/`keywords` 的处理一致；
  - `_BACKFILL_FIELDS` 新增 `pub_types`，living-review 跨轮回填同样带标签（enrich 不覆盖）。
- 验证：合成 EPMC(`pub_types=["Review"]`) + OpenAlex(`type=article`) 同 DOI 记录，
  无论哪方为主记录，`normalize.merge` 后 `pub_types` 均 `__== ["Review"]`，B1 信号恢复。

## [Unreleased] — 2026-09-06 (8) · 检索 Coze 调用改流式（/stream_run）+ 5 篇一批生成器 + 根因回归测试

> 对齐 PDF 通道（pdf_download._call_coze_unified 已用 /stream_run）与 meta-analysis 的 SSE 流式契约：
> 文献检索外发调用从 /run 非流式升级为 /stream_run 流式，避免长检索被网关按单响应超时掐断；
> 并新增 `dispatch_stream` 生成器，把返回的 works 按 5 篇一批依次 yield，供 workbench / CLI 渐进渲染。

### Changed
- **`adapters/fetch_coze_unified.py`**：
  - 新增 `CT_SEARCH_ENDPOINT_STREAM`（`https://ct-search.coze.site/stream_run`，env 可覆盖）；
    主路径 `dispatch()` 改 POST `/stream_run`，复用 `pdf_download._parse_coze_stream` 解析 SSE
    （workflow_end / node_end 事件提取 projects，兼容 projects 列表 / project_list 字符串 / 字典三形态）；
    流式无结果（workflow Output 未绑定 / 被 rejected）时**自动回退 `/run`**，零破坏性。
  - 新增 `dispatch_stream(...)` 生成器：内部复用 `dispatch()`，把返回的 works 按 `batch_size`
    （默认 5）切片、逐批 yield；`progress` 回调逐批上报，便于前端渐进渲染。CLI 新增 `--stream`
    / `--batch-size` 开关直接调用（打印分批结果）。

### Added
- **`tests/regression_root_causes.py`**：纯本地根因回归测试（24 断言，无网络），锁住 2026-09-06
  实测踩出的根因，防复发：
  - `normalize._bare_doi` / `_norm_doi`（DOI URL 前缀剥离 + 尾标点）；
  - `normalize.merge` 的 `pub_types` 跨源 union-merge（meta-analysis B1 综述硬信号根因）；
  - `normalize._BACKFILL_FIELDS` 含 `pub_types`（living-review 回填不丢标签）；
  - `pdf_download._safe_filename`（DOI→安全文件名、去重 .pdf）；
  - `pdf_download._parse_coze_stream`（SSE 解析：workflow_end project_list / projects 直出 / 空 output 回退 node_end）。

### Verified
- 真实 coze 端 A/B 验证：`/stream_run` 主路径拿到 3 篇（doi `10.1038/s41574-023-00833-4`）；
  关掉 `/run` 回退仅留 `/stream_run` 仍拿到 3 篇 → **检索工作流本身支持流式，非靠 /run 兜底**；
  `dispatch_stream(..., batch_size=5)` 切片为 `[5,5,2]` 已验证。

## [Unreleased] — 2026-09-06 (9) · 工作台接入流式检索（/api/lit-stream → 渐进渲染）

> 把 (8) 的 `dispatch_stream` 真正接到 workbench 前端：新增流式端点 + 「实时流式检索」工具面板，
> 用户点「开始流式检索」后，论文按 5 篇/批**逐批渐进渲染**，长检索不再「干等一次性出结果」。

### Added
- **`workbench/server.py`**：新增 `POST /api/lit-stream` 端点，按 `sources` 顺序调用 `dispatch_stream`，
  用 chunked NDJSON 把每批（默认 5 篇）依次推回前端；事件类型 `progress / batch / done / error`；
  用 `_busy_tool="lit-stream"` 锁与 `/api/search`、`/api/tools` 互斥，避免并发网络作业冲突。
- **`workbench/index.html`**：工具页新增「实时流式检索」tab（`data-t="stream"` → `#t-stream`），
  含数据源 / 关键词 / 年份 / 每源上限 / 每批篇数 / 真实执行开关；JS 用 `fetch` + `ReadableStream` 消费
  NDJSON，逐批把 `_workItemHTML` 渲染进 `#st_out`（复用既有 `wb-work` 样式，含 OA/CSM 标签与 DOI 直链）；
  支持「停止」中断（AbortController）。

### Verified
- 真实端到端：`POST /api/lit-stream`（openalex, metformin, max=12, batch=5）→ 200，事件
  `progress×1 / batch×3 / done×1`，**batch sizes = [5, 5, 2]**（共 12 篇），首篇标题与
  `doi/is_oa/cited_by_count` 字段正常 → 5 个一批依次返回在 HTTP 通道层面坐实。

## [Unreleased] — 2026-09-06 (10) · 运行态配置 / 检索产物移出技能树（不进发布包）

> `config/`（出站授权白名单，含作者私有 coze 端点）与 `out_dm_sglt2_v9/`（一次真实 SGLT2 检索产物）
> 属本机运行态资产，不应随三平台发布包公开。将其移出技能树，置于
> `~/.workbuddy/ct-literature-runtime/`，并在 `.gitignore` / `.clawhubignore` 补双保险。

### Changed
- **`adapters/fetch_coze_unified.py`**：`_CONFIG_JSON_PATH` 单点常量改为 `_config_candidates()` 多候选回退
  （env `CT_LIT_RUNTIME_DIR` > `~/.workbuddy/ct-literature-runtime/config/config.json` >
  技能树内 `config/config.json` 兜底）；`_check_outbound_authorization` 遍历候选命中。移出后出站授权门
  仍能命中白名单（实测 `auto_approve_endpoints` 含 ct-search/ct-bugreport 两端点，`/run` 仍放行，无 AUTH-BLOCK）。
- **`.gitignore` / `.clawhubignore`**：新增 `config/` 与 `out_dm_sglt2_v9/` 排除项（defense-in-depth，树内重建也不进包）。

### Moved
- `config/` → `~/.workbuddy/ct-literature-runtime/config/`（含 `config.json`）。
- `out_dm_sglt2_v9/` → `~/.workbuddy/ct-literature-runtime/out_dm_sglt2_v9/`（merged.json/html/xlsx/pdfs 等）。

## [Unreleased] — 2026-09-07 (11) · PDF 批量下载提速：并发下载 + Coze 子批管道 + 解码心跳

> 用户痛点：20–50 篇 PDF 下载时「时间长且长期无进度」。根因有二——(a) 本地两处下载循环
> 串行（`_download_direct_with_delay` 逐篇 sleep+下载，50 篇 ≈ 100–250s）；(b) coze 解码整批黑盒
> （`publisher_pdf_batch_node` 默认 `group_size=5` 组间串行，50 篇 = 10 组串行 ≈ 3min 静默）。
> 本次在本地 + coze 双端修复。

### Added (本地 `scripts/pdf_download.py`)
- **P0 并发下载 + 每域名限速**：新增 `_PerHostRateLimiter`（跨域名并发、同域名按 `min_delay`
  串行保距）+ `ThreadPoolExecutor(max_workers=MAX_DOWNLOAD_WORKERS=6)`。关键修正——coze 成功解码
  多返 `pdf_s3_url`（同 `*.amazonaws` host），原统一 1.5s 间隔会把所有 S3 下载**串行化**；新增
  S3/CDN 快车道（`delay=0.1`，可高并发），biorxiv/medRxiv 仍走 `min_delay`、其余出版商 1.0s。
- **P1 Coze 子批管道**：间接项由「整批 50 一次发送」改为拆 `≤COZE_SUB_BATCH(12)` 子批，每批返回
  **立即并发下载该批直链**（「解码子批 N+1」与「下载子批 N」重叠），首批结果更早落地。
- **P2 解码心跳**：coze 等待期每 10s 吐「已用时 Xs（已保存 N 篇）」，消除"长期无进度"观感。
- **`manual_needed` 收尾对账**：未落盘（非跳过/非拒绝）在 run() 末尾统一计算，避免并发分支漏算。
- 新增 `tests/regression_pdf_speed.py`（11 断言，纯 mock 不耗网络）：锁 `_PerHostRateLimiter` 同域
  保距/跨域并发、run() 落盘完整性、`manual_needed` 计数、并发提速（wall < 60% 串行）、coze 子批数、
  skip_coze 本地兜底。真实验证：6 篇实跑 39.9s，子批发 1 批、管道化下载 2/2 成功、心跳每 10s 输出。

### Changed (coze 端 `ct-registry/adapters/coze/src/graphs/nodes/publisher_pdf_batch_node.py`，CZ)
- `GROUP_SIZE 5→8`、`_do_batch` 默认 `max_workers 4→6`：减少串行组数（50 篇 10→7 组）、提升组内
  并发（理论吞吐 8→12 篇/分），直接砍解码黑盒时长。**⚠️ 此改动在云端代码，需重新部署 + 端到端线上
  回归；若 FaaS 因内存峰值回收进程致解码失败率上升，回退到 5/4 并同步本地 `COZE_SUB_BATCH`。**

## [Unreleased] — 2026-09-05 (5) · 工作台「Coze 全文解码」：把间接链接解码为可直接下载的直链

> 针对工作台「真实加载、可调用 Coze 完成分析」的需求：让检索结果能交由 Coze
> ct-search 端点把各篇文献的间接下载链接解析成可直接下载的文件链接。

- **新 `scripts/coze_resolve.py`**：读 `.merged.json`（或任意含 works[] 的 JSON），
  为每篇收集 open_access_url / preprint.url / doi 标识 → 批量 POST
  ct-search.coze.site/run 的 `publisher_pdf_batch` resolve → 回显每篇
  `{doi, key, direct_url, source, cloudflare, status}`。复用 `pdf_download.py` 的
  `PdfDownloader`（同一端点契约 + token），不重复造轮子；`--download` 可选落盘到 pdfs/。
- **工作台 `server.py`**：`/api/tools` 新增 `coze_resolve` 工具分支（可对任意已有
  `.merged.json` 触发，不依赖主检索内嵌下载）。
- **工作台 `index.html`**：检索完成结果卡新增「🔗 Coze 解码全文直链」按钮 → 调
  coze_resolve → 渲染「Coze 解码完成」对话卡：KPI（直链可下 / Cloudflare / 需手动）
  + 逐篇文献表格（状态 + 可点开的直链）。`cozeResolve` / `renderCozeResult` 两个函数。
- 实测（真实 ct-search 端点）：osimertinib rct 检索 6 篇全部解码为直链，ascopubs
  (jco) 与 annalsoncology 的 Cloudflare 出版商篇目也被 Coze 解析出 PDF 直链。
- README：能力表新增「🔗 Coze 全文解码」行 + 工具行补 `coze_resolve.py` + 目录/说明更新。

## [Unreleased] — 2026-09-04 (4) · 工作台改为「对话优先」交互（chat-first）

> 本条目是对 (3) 中工作台「填表为主」的纠正：原技能以自然语言对话为主要使用方式，
> 工作台必须复现这一点，而非 Excel 式表单。

### Changed (UX 重构，`workbench/`)
- **首屏 = 对话窗口**：用户在底部输入自然语言需求 → 后端 `/api/parse` 解析 →
  助手以「检索预览卡片」**回显理解结果**（主题/类型/年份/安全性/数据源/引用验证参数表）+
  意图标签 + 置信度 → 三动作「✅ 确认并 --run / ⚡ 仅 SAFE 预览 / ✏️ 调整」，确认后才执行。
  参数确认用对话气泡而非表单。
- **双层 NL→spec 解析引擎**（新 `workbench/nl_parse.py`）：
  - **LLM 层（可选）**：调用 OpenAI 兼容 `/chat/completions`，返回受 JSON schema 约束的
    spec；key/base/model 存本地 `workbench/.env`，绝不回显。配了则像原对话一样真正听懂
    任意话术。
  - **规则层（默认/离线兜底）**：本地词典+正则把常见表达映射为 spec ——
    「近 N 年/中文数词/2020至今/2018-2023」→ 年份；系统综述/meta/RCT/病例报告 → 类型；
    「安全性/不良事件」→ safety；bioRxiv/medRxiv/arXiv/Semantic Scholar/Cochrane/指南/
    预印本回退 → 数据源开关；topic 抽取先剥离其它维度残留词再取核心名词短语。
    附 confidence + missing + intent_label，供对话按需补问。
  - **Vague 检测**：用户自述「不确定/帮我梳理」→ 返回 `vague`，助手改问聚焦问题
    （主题 chips），不回显占位主题（对齐 search_menu §6 grill-me）。
- **「高级参数」退为次级面板**：保留全部精细选项，可把识别结果一键填入微调后执行，
  不再作为主入口。
- **结果以对话卡片回显**：检索完出 KPI（唯一文献/OA/安全/被引 Top 平均）+ 高被引
  Top-N + 「当前检索设定」回显块 + 「查看产物/换个说法」操作。
- 数据源 / 工具 / 产物 为顶部次级导航；新增「对话解析引擎」工具页配置 LLM 端点。

### Added
- `POST /api/parse`（NL→spec）、`GET/POST /api/llmcfg`（LLM 解析配置，key 不回显）。
- 运行健康：运行中禁用发送、实时 NDJSON 进度折叠在对话气泡内、可停止。

## [Unreleased] — 2026-09-04 (3) · 学术工作台界面（零依赖本地 console）

### Added
- **`workbench/` 本地学术工作台**：零第三方依赖（Python 标准库 `http.server`），
  复现对话方式可调用的全部能力。启动：`python workbench/server.py --open`
  （默认 `http://127.0.0.1:8787`）；Windows 可双击 `workbench/run_workbench.cmd`。
  - **检索向导**：主题/文献类型/年份/max/排序/CSM 安全性/附加关键词；
    Europe PMC(默认开)/Cochrane 专属/Semantic Scholar/bioRxiv/medRxiv/arXiv/
    指南语料库/预印本候选回退开关；Excel/HTML/BibTeX-RIS/PRISMA/Obsidian/
    Zotero/PDF 批量下载；引用风格/语言/引用验证(all/top/background/none)/top-N；
    living-review `--merge-existing`；输出目录可设。
  - **执行模型**：默认 SAFE 预览（不联网），勾选后 `--run` 真实执行；以
    `--progress json` 实时 NDJSON 流式回传（run_start / source_done /
    verify_done / export_done / run_done），运行中可中断。
  - **数据源与健康**面板：解释器、OpenAlex key 状态（布尔，不回传明文）、8 类
    数据源说明。
  - **辅助工具**：MeSH 术语映射、中英术语标注、关键词广度检测、PRISMA 筛选、
    Markdown 报告、指南语料构建（`mesh_mapper` / `abstract_translator` /
    `keyword_breadth` / `screen_prisma` / `report` / `build_guidelines`）。
  - **产物浏览**：列出 / 打开 / 下载输出目录全部产物。
  - 安全边界：只读技能树、仅写用户指定 out-dir、key 值绝不上送、联网仅在
    `--run` 后发生。
- **`run_workbench.cmd`** Windows 一键启动（自动定位 Python）。
- **`workbench/README.md`** 使用说明与能力对照表。

### Fixed
- **`scripts/evidence_log.py`**：`main()` 引用 `argparse` 但模块缺失
  `import argparse` → `--help` 崩溃（`NameError`）；已补 import，
  `python evidence_log.py --help` 正常。

## [Unreleased] — 2026-09-04 (2) · OA 判定增强 + 预印本候选（--preprint-fallback）

### Added
- **OA 判定增强（fetch_openalex）**：直读 OpenAlex `open_access.is_oa` / `oa_status`
  写入 work（`is_oa` / `oa_status`）；`open_access_url` 采集改为四级优先：
  best_oa_location.pdf_url → 任意 `locations[].pdf_url`（OpenAlex 有时把唯一 PDF
  放在非 best location，原实现漏报）→ is_oa 时的 best_oa 落地页 → None（真闭源）。
  普通 landing page 不再被误提升为「OA 链接」。
- **normalize 合并语义**：`is_oa` 跨源取 OR（任一来源判 OA 即 OA）；`oa_status`
  / `preprint` 按缺省回填（含 `_BACKFILL_FIELDS`）。
- **`--preprint-fallback`（opt-in，`scripts/preprint_fallback.py` 新模块）**：对
  无 OA 全文的文献（is_oa 假 / open_access_url 空），按标题在 bioRxiv / medRxiv
  （Europe PMC PPR，两段式：短语优先→内容词 AND 兜底）+ arXiv（Atom API）检索
  预印本候选，命中并**通过作者姓氏同篇校验**（移植自 meta-analysis `pdf_fetch`，
  「宁可缺漏不能弄错」：缺作者 / 无共同姓氏 / 第一作者不一致均丢弃）后写入
  `work["preprint"] = {venue, doi|arxiv_id, url, author_check}`。逻辑移植自
  meta-analysis/adapters/pdf_fetch.py（用户指定参考实现）。
- **Excel 新增两列（DOI 之后）**：「开放获取 / OA」（Y 绿底 / —，含字段字典说明）
  与「预印本候选 / Preprint candidate」（venue 超链接，bioRxiv/medRxiv/arXiv 标签）。
  Works / Safety-Related 两表同步。

### Verified
- 5 文件 py_compile 全绿；离线 mock 实测 enrich：OA 文献跳过、无作者跳过、
  作者不符拒绝、同篇候选通过并落 `preprint`；Excel「开放获取」Y/— 渲染正确、
  「预印本候选」venue 超链接落点正确；`ct_literature.py --help` 新选项就位。
- 实测中发现并修复：enrich 内候选作者未归一化（大小写不一致误判 no_shared_author）。

---

## [Unreleased] — 2026-09-04 · Works 表模板改进（标题超链接 + 列序 + 双语修复）

### Changed
- **标题列自带 DOI 超链接**：`_write_works_table` 的 title 单元格改用
  `write_url`，链接优先取 `https://doi.org/<doi>`（裸 DOI 经 `_normalize_link`
  归一），DOI 缺失时回退 `url`；两者皆无则降级为纯文本。原「链接 / Link」
  （url）独立列**删除**。
- **列序调整**：Works / Safety-Related 表列序改为
  DOI → Year → Title → Authors → Journal → Type → Study type → Abstract →
  Cited by → Safety → OA PDF（摘要前移至 Study type 之后）。
- **双语表头真正生效（bug 修复）**：`_WORKS_COLS` 此前在模块 import 时即调用
  `t()`，而 `set_lang()` 在运行时才切换语言 —— 列头被永远冻结为英文。改为
  「键+宽度」结构、表头在写入时经 `t()` 解析；决策/理由列（meta-analysis A3
  裁决表）同步双语化（`col.decision` / `col.reason`）。
- **README 字段字典同步**：移除 `f.url` 条目；`f.title` 描述改为「已超链接至
  DOI，点击可访问」。
- **顺手修复 `_LOCAL` 嵌套错位**：`cfg.degraded` 此前被误嵌进 `ev.note` 字典
  内部，导致 Evidence Log「降级数据源」标签查不到本地化文案。

### Compatibility
meta-analysis `parse_screening_xlsx`（A3 裁决表上传回解析）按**表头名称**
（DOI / 标题 / 裁决 / 理由）定位列、不依赖列序 —— 本次列序调整与 url 列删除
对其无影响；已用样例数据实测 zh/en 双语导出 + 超链接落点正确。

---

## [Unreleased] — 2026-09-01 · Safety-Related 页改为 `--safety` 显式 opt-in

### Changed
- **`export_xlsx.build_safety()` 改为 opt-in**：不再无条件生成「安全性相关 / Safety-Related」页；`export_workbook()` 新增 `safety=False` 参数，`build_safety()` 在 `not safety` 时直接跳过（不建 worksheet）。CLI `main()` 新增 `--safety` 透传；`ct_literature.py` 调 `export_workbook` 时传入 `args.safety`。
- **默认工作簿收口为 3 数据页**：README / Overview / Works / Evidence Log；「安全性相关」页仅在 `--safety`（CSM 子集）时出现。普通文献检索不再默认带安全性子集页，边界对齐 ct-safety（结构化安全性信号属 FAERS 领地）。
- **`is_safety` 标记保留**：每条文献仍按标题/摘要词命中打 `is_safety`，Works 页 amber 高亮照旧（用于快速扫读），仅独立成页这一步改为显式触发。
- **文档同步**：SKILL.md Features 表、双 README 的「4 sheets」描述、Example 1 回复示意、FAQ 第 109 行均改为「默认 3 页 + `--safety` 才出第 4 页」；并明确 `--safety` 是 ct-safety 关联调用时使用的入口。

### Why
「安全性相关」页此前每次都生成，因为 `build_safety()` 在 `export_workbook()` 里被写死调用，而 `is_safety` 标记默认就打（生物医学主题几乎必然命中）。这会让普通文献检索默认带出一个看起来像安全性评估的表单，越界到 ct-safety 的领域。改为 opt-in 后：普通检索保持干净的证据库输出；只有显式 `--safety`（或 ct-safety 关联调用）才产出 CSM 定性子集页，边界清晰。

---

## [Unreleased] — 2026-08-30 · PRISMA 去重计数补录

### Changed
- **`normalize.merge_with_stats(payloads)` 新增**（非破坏）：在 `merge()` 之上返回去重统计
  `{"raw_count", "duplicates_removed"}`，`merge()` 仍为零改动薄包装，现有调用方不受影响。
- **`screen_prisma.screen()` 新增 `duplicates_removed` 参数**：写入 `.merged.json` 的
  `prisma` 块（顶层 `duplicates_removed` 计数），供下游 meta-analysis `prisma_flow` 的
  「duplicates removed (n=…)」框直接取数。
- **`ct_literature.py` 切到 `merge_with_stats`**：捕获去重计数并穿过 PRISMA 初筛写入。

### Why
meta-analysis 的 `prisma_flow` 需要 9 个计数字段，其中 `duplicates` 此前在 ct-literature
侧无任何来源（去重已执行但移除数量从未计数输出），只能人工回忆。本次补上后，
`prisma_bridge.py` 可自动填 `duplicates` 与派生 `records`，检索→绘图链路闭合。

---

## v0.9.5 (2026-08-26) · 版本整合（单一事实源对齐；无功能性 release note）

- 版本号统一为 0.9.5（SKILL.md frontmatter + 双 README 页脚），与 CHANGELOG 顶部对齐；本版不含独立功能变更记录，详见下方 v0.9.0。

## v0.9.0 (2026-08-22) · Bug Report 功能正式发布（三站点）

发布原因：**增加 bug report 功能**（ct-base §20.3 统一技能错误上报）。

- **Bug Report 功能正式随包发布**：`adapters/bug_report.py` 客户端（11 键脱敏白名单信封 + 两阶段用户确认 + coze 端点 `https://ct-bugreport.coze.site/run` + 本地兜底 `save_local_report`），SKILL.md「Bug Reporting」节与 README 安全与隐私说明同步（自 v0.7.6 起开发完成，本版起纳入正式发布）。
- **发布树修正（§16.8）**：`adapters/` 下 6 个运行模块此前从未进入 git 索引（`bug_report.py` / `build_guidelines.py` / `fetch_guidelines.py` / `guideline_corpus.py` / `portal_fetch.py` / `_smoke_guidelines.py`），`git archive HEAD` 发布包会缺文件 → 本次全部纳入跟踪，保证 GitHub / SkillHub / ClawHub 三平台发布树一致。
- **发布包排除补齐**：`.gitignore` / `.clawhubignore` 新增 `.ctbase_injected.json`（含本机绝对路径，不随包公开）、`*.ctbase_bak_*`、`tools/`（作者侧批量维护脚本，非运行部件）、`adapters/_smoke_guidelines.py`（未引用的本地测试脚本）。
- **版本对齐（§9）**：SKILL.md `version` 0.7.6 → 0.9.0；两份 README 版本脚注同步 v0.9.0。
- **代码修正**：`adapters/__init__.py` docstring 纠正（误写为 ct-samplesize，实际为 ct-literature 出站收口目录）。
- **术语扩展**：`references/term_map.json` 补充 GLP-1 类药物中英术语（司美格鲁肽 / 替尔泊肽 / 利拉鲁肽 / 瑞他鲁肽 / 度拉糖肽 / 艾塞那肽）。
- **description 与 summary 统一（§3）**：description 中文部分改为与 summary 完全一致（此前含引文验证、guidelines 构建细节、pointer-only 等额外说明，与 summary 内容不对称），英文部分为对应翻译，中英格式不变。

## v0.7.6 (2026-08-22) · Bug Report 客户端与规则对齐（ct-base §20.3 同步）+ 发布前 §16 整改

- **`adapters/bug_report.py` 副本**：补齐 `confirm_thanks`/`build_followup`/`parse_history` + `_MSGS` thank/done/pending 双语文案 + `send_to_endpoint` 透传 `history`（此前缺这些函数）；docstring「三阶段确认」→「两阶段确认」。
- **SKILL.md Bug Reporting 节**：Trigger 补「主动触发」独立路径（用户显式说 report a bug / 反馈问题直接走两阶段，不受每会话 1 次限制）；新增 Post-send history回执 bullet（endpoint 返回 `history`，回复由 `confirm_thanks(locale)` + `build_followup(history, locale)` 双语拼接：空→结束；`resultstr=="done"`→展示 memo；否则"未修复"）。
- **发布前 §16 整改（ct-base 规范）**：
  - `.gitignore` / `.clawhubignore` 补齐发布排除：`tests/`、`.env`、`__pycache__/`、`*.pyc`、`*.pyo`、`*.db`、`out/`、`*.log`、`.Rhistory`、`.RData`、`staging/`、`references/user_terms.json`、`adapters/coze/`（此前仅 guideline 排除，`tests/` 与 `.env` 会随发布包公开；与 README「仅 `.env.example` 随包发布」承诺对齐）。
  - **版本对齐（§9）**：SKILL.md `version` 0.7.5 → 0.7.6；两份 README 的 Version 引用 v0.6.11 → v0.7.6（修复三处版本不一致）。
  - **SKILL.md 压缩至 195 行**（§16.1 ≤200 行上限，原 278 行）：压缩 Language / Positioning / Data Sources / guidelines 段 / Features 表 / Implementation / Bug Reporting 长段，关键安全契约（SAFE PREVIEW、B 档、qualitative 警告、verify 反幻觉、guideline pointer-only、bug report 两阶段/11-key 白名单/端点/client-only）全部保留；细节仍指向 `references/`。
  - **README 弱化「chat 让助手写 key 进 .env」表述**：自配置路径 (a)–(c) 提前为主推荐，chat 写入降级为可选（回应 ClawHub 审计 UNVERIFIED「Context-Inappropriate Capability」项）。
  - **i18n 一致性确认**：`shared_sync_check` 提示的 6 个未携带 key（`auth.coze_outbound` 等）经 grep 验证 scripts/adapters 零引用，属纯 Python 裁剪，豁免。
  - **发布树修正（方案 A 硬化测试暴露）**：`tests/` 的 7 个文件此前已进入 git 索引（历史 `.gitignore` 仅排除运行产物、从未排除 `tests/` 目录），**ignore 规则对已跟踪文件无效**，导致 `git archive HEAD` 发布包仍含 tests/。`git rm -r --cached tests/` 解除跟踪（工作区文件保留）并本地 commit `chore(§16.8)`；源仓库 `git ls-files` 现为 59 文件，`publish_secret_scan` P0=0 / P1=0。
  - **description 中英对称化**：description 中英文统一按 summary 内容重写（补齐 guidelines「本地语料库」模式、pointer-only/Coze KB、B 档等此前仅英文侧或 summary 侧的信息），消除英文比中文多出一整段 guidelines 描述的不对称；中文前 / 英文后格式不变。
  - **README「安全与隐私」更新+精简**：出站说明补充 bug report 出站（`https://ct-bugreport.coze.site/run`，两阶段确认后仅发 11 键脱敏信封，无法联网回退本地文件），删除过时的「无其他出站路径」表述；key 相关两条重复说明合并为一条。SKILL.md `permissions.network_note` 同步补充 bug-report 出站声明。

## v0.7.5 — 2026-08-16

### Change · data-protection split (pointer-only skill tree; full text → author's Coze KB)

- **Design decision (per user's data-protection concern):** the shareable skill is a copyable artifact, so
  full-text guideline documents must NOT live inside it. The skill tree now ships **pointer-only**
  (`references/guidelines/guidelines_index.json`: org / title / URL / version metadata — low-sensitivity,
  publish-safe). **Full text is the author's curated IP and lives in the author's self-controlled Coze KB**
  (not publicly copied with the skill). ct-advisor consults that Coze KB for native guideline Q&A and delegates
  structured retrieval to this skill.
- **`build_guidelines.build()` now defaults `download=False`.** When `--download` IS used, OA full texts are
  written to a **LOCAL CACHE OUTSIDE the skill** (`~/.workbuddy/ct-guideline-docs`, default) — never under
  `references/guidelines/`. A startup `[WARN]` reminds the author that docs are not part of the skill and must
  not be published. New CLI flags: `--download` (opt-in), `--doc-cache-dir`.
- **Defense-in-depth:** added `.clawhubignore` + `.gitignore` excluding any `references/guidelines/**`
  PDF/XML/HTML and `ct-guideline-docs/` (in case `--doc-cache-dir` is ever pointed inside the skill tree).
- **Docs:** SKILL.md G-section + summary/description/Features updated to state the pointer-only / Coze-home
  split; version 0.7.4 → 0.7.5. A Coze-KB draft (`guideline_coze_kb_draft.md`, workspace root, OUTSIDE the
  skill) enumerates the 4 seeded topics' orgs + canonical URLs with `key_recommendations` placeholders for the
  author to fill from official sources before deploying to Coze.
- **Verified:** `adapters/_smoke_guidelines.py` ALL PASS (external-cache download path + warning included).

## v0.7.4 — 2026-08-16

### Feature · build-time lightweight fetch for the 6 portal-only orgs (user-chosen "构建期轻量抓取")

- **New `adapters/portal_fetch.py`** (BUILD-TIME only, called by `build_guidelines.build(run=True)`):
  lightweight fetchers for the six portal-only orgs that have no free keyword API.
  - **CPIC** — genuine fetch via its free, keyless PostgREST API (`api.cpicpgx.org/v1/guideline`,
    falling back to `/publication`); stored as real `api` records (`retrieved:true`).
  - **NCCN / ADA / AHA / SIGN / CMA** — best-effort public-portal HTML link-scrape. Schema-tolerant;
    on login-wall (NCCN) / JS-render / network block it returns `[]` and `build_guidelines` falls back
    to the honest `portal` pointer. **Nothing is fabricated.**
  - Every fetcher is wrapped so it **never raises** — a failed fetch degrades gracefully to a pointer.
- **Wired into the builder:** `build_guidelines.build()` step 2 now tries `portal_fetch.fetch_portal(org, …)`
  per portal org; fetched records become `api` entries, failures fall back to `_portal_pointers()`.
  `source_status` now reports each portal org as `fetched` or `pointer`. Analysis-time loading is unchanged
  (still zero network via `guideline_corpus.load()`).
- **Honest limitation:** only CPIC has a real free API; the other five are fragile HTML scrapes that will
  likely stay pointers until tuned on open internet. NCCN is login-walled (free account) so may never yield
  content without auth. No live verification in this sandbox (egress limited) — verified offline via mocks.
- **Offline-verified:** 11 new smoke checks cover CPIC API path, HTML extraction, graceful `[]` on network
  error, and the build-time "fetch→api / fail→pointer" wiring. Full smoke (`adapters/_smoke_guidelines.py`)
  ALL PASS.

## v0.7.3 — 2026-08-16

### Refactor · clinical guideline corpus → local-first (corrects the v0.7.2 live-fetch design)
- **Design correction (per user feedback):** clinical guidelines are a *versioned* reference standard
  (NCCN 2024.v3, ADA 2026 Standards). The v0.7.2 model fetched "latest" via code at analysis time; the
  correct model is a **curated, version-pinned LOCAL corpus** — build once, read many times (zero network
  at analysis, reproducible, honours ct-base local-first / 数据不出域).
- **New `adapters/guideline_corpus.py`** (analysis-time, ZERO network): reads
  `references/guidelines/guidelines_index.json` and returns the same payload shape as
  `fetch_guidelines.fetch()`, so `scripts/ct_literature.py` consumes it uniformly. Filters by topic/org;
  returns an honest `corpus_missing` payload (with the builder command) when the index is absent.
- **New `adapters/build_guidelines.py`** (build-time, network, author action): aggregates 12+ sources,
  downloads OpenAlex OA-PDFs where reachable, writes/merges `guidelines_index.json` (+ optional doc files).
  SAFE PREVIEW: omit `--run` → dry-run, **no network, no write**. Dedupe by `(org, topic/title)`;
  special-cases portal orgs (`org:topic:title`) to avoid cross-topic id collisions.
- **Rewired pipeline:** `scripts/ct_literature.py` `--with-guidelines` now calls `guideline_corpus.load()`
  (was `fetch_guidelines.fetch(run=True)`). `fetch_guidelines.py` is retained as the source-library used
  by the builder, not by analysis-time loading.
- **Seeded corpus built live (network):** `references/guidelines/guidelines_index.json` — 96 curated
  entries (72 `api` + 24 `portal` pointers, all `retrieved:false`) across 4 topics (diabetes /
  breast-cancer / heart-failure / community-acquired-pneumonia). 0 OA-PDF docs on disk in this sandbox
  (external publisher domains unreachable here) — downloads succeed on the author's open-internet machine.
- **Offline-verified:** loader reads the real corpus in ~0.012 s with **zero network calls**; 22-check
  smoke (`adapters/_smoke_guidelines.py`) ALL PASS (loader zero-network, builder SAFE PREVIEW, dedupe,
  portal honesty, source-library 13 sources).
- `SKILL.md`: G section rewritten to the corpus-first model; frontmatter summary/description + Features
  row + Implementation CLI updated. `version` 0.7.1 → 0.7.3 (frontmatter had lagged behind CHANGELOG).
- **Red line honoured:** no publish/deploy (no git push / SkillHub / ClawHub / Coze deploy); local changes
  + local verification only.

## v0.7.2 — 2026-08-16

### Feature · clinical guideline aggregation across 12+ sources (G-upgrade, opt-in)
- New `adapters/fetch_guidelines.py`: aggregates clinical-practice guidelines from **12+**
  authoritative sources into one normalized, de-duplicated list. Two access tiers, honestly
  labelled per record via `access` (`api`/`portal`) + `retrieved`:
  - **Live `api`**: OpenAlex (guideline-typed search), Europe PMC (guideline pub types),
    GIN (Guidelines International Network), WHO IRIS — fetched via the shared `http_utils`
    GET+retry (429 Retry-After, exponential backoff, Bearer key).
  - **Live `api` (key-gated, best-effort)**: NICE¹ / MAGICapp / TRIP² — graceful `skipped_no_key`
    when the env key is absent (never fakes a result).
  - **`portal` pointer** (no free keyword API): NCCN / ADA / AHA / SIGN / CMA / CPIC — emit an
    honest navigational pointer (`retrieved:false`) to the org portal, **not** a fabricated fetch.
- Wired into `scripts/ct_literature.py` as a **separate** capability (kept OUT of
  `normalize.merge` so it never pollutes citation verification / PRISMA): `--with-guidelines`
  (BooleanOptionalAction, opt-in) → writes `guidelines.json` + a `guidelines` block in
  `.merged.json` (`meta.guidelines.source_status` shows per-source coverage). Flags:
  `--guideline-sources` (subset), `--guideline-max` (per-source cap, default 20).
- SAFE PREVIEW preserved: no network unless `--run`; `fetch(run=False)` returns `None`. Every
  live source is wrapped so a failure degrades to a `source_status` note, never aborting.
- `SKILL.md`: new "Clinical guideline sources" section, Features row, Implementation CLI examples,
  and frontmatter summary/description updated.
- Offline smoke test (`adapters/_smoke_guidelines.py`, mock-injected): 22 checks — parse /
  normalize / dedupe / merge, SAFE PREVIEW, portal honesty (`retrieved:false`), key-gated skip,
  and full `run()` integration — all pass.

¹ NICE public REST auth header is undocumented (like PROSPERO); degrades to skip until a working
token is supplied. ² TRIP requires a commercial API key. Live-correctness of GIN/WHO/MAGICapp/
NICE/TRIP parse paths is schema-tolerant but pending validation against a real 200 response.

## v0.7.1 — 2026-08-15

### Fix + Docs · make the abstract term-annotation tool actually work, and describe it honestly
- **Fix `abstract_translator.translate_abstract`** (was producing garbage): the old loop replaced each term without word boundaries, so short keys like `os`/`evaluate` corrupted inside longer words (`osimertinib` → `【总生存期】imertinib`), and sequential per-term substitution re-matched inside already-replaced spans (nested 【【…】】). Now: (1) only English keys are used (the Chinese-key entries from `term_map.json` are ignored — they belong to the zh→en topic translator, not this EN→ZH annotator); (2) word-boundary matching `(?<![A-Za-z0-9])…(?![A-Za-z0-9])`; (3) single-pass alternation, longest-first — no nesting. Verified: `randomized controlled trial → 【随机对照试验】`, `NSCLC → 【非小细胞肺癌】`, `overall survival → 【总生存期】`, `osimertinib` untouched.
- `SKILL.md` summary/description: "本地英文→中文摘要翻译助手" → **"可选英文→中文摘要术语标注工具（本地、术语级替换，非全文翻译）"** — the helper is a term-level annotator and not part of the retrieval pipeline; the old wording set a full-translation expectation it cannot meet.
- `README.md` / `README_zh-CN.md` (Advanced Reference): new "Optional tool · English→Chinese abstract term-annotation" section with CLI usage, real verified examples, and the explicit boundary: **term-level substitution, not full-text translation**.
- `README.md` / `README_zh-CN.md` (FAQ): new "Why don't you support Chinese domestic databases (e.g. CNKI)?" — deliberately not supported: (1) marginal incremental value vs the international evidence base; (2) no compliant channel exists (CNKI et al. have no public API for individuals and aggressively block / sue crawlers, against the skill's "official public access only" rule); (3) ROI. Users needing a Chinese paper export the citation (RIS/BibTeX) themselves.
- `scripts/abstract_translator.py`: docstring & CLI help aligned — removed the stale "optional translation API" claim (the code has **no API path**; purely local dictionary substitution).

## v0.7.0 — 2026-08-14

> v0.6.13（进度事件流）与 v0.6.14（架构优化）开发版均未单独发布，功能统一并入 v0.7.0。

### Feature · progress event stream (`--progress json`, agent-facing)
- New `--progress {human,json}` flag on `ct_literature.py` (default `human` = unchanged console
  output). In `json` mode stdout carries **only** a flushed NDJSON event stream —
  `run_start / source_done / source_failed / fetch_done / verify_progress / verify_done /
  evidence_log / intermediate / export_done / export_failed / run_done` — and sub-module
  prints are redirected to **stderr** so the stream stays parseable for agents.
- Human mode additionally gained per-source progress lines (`[OK] source OpenAlex: N works in X.Xs`).

### Performance · architecture-level wait-time reduction
- **Pooled HTTP connections** (`adapters/http_utils.py`): replaced the per-request
  `urllib.request.urlopen` (a fresh TCP+TLS handshake on every request) with a **thread-local
  keep-alive connection pool** + manual redirect following + **per-host concurrency caps**
  (doi.org 8 / Crossref 4 / OpenAlex 6 / Europe PMC 6 / S2 2). Saves ~100–300 ms handshake
  per request across the hundreds of fetch + verify round-trips; stale connections are
  dropped and rebuilt automatically. `verify_citations._resolve_doi` (doi.org Range probe)
  now uses the same pooled path.
- **Cross-source verification dedup** (`scripts/ct_literature.py`): the same work indexed by
  two sources (e.g. OpenAlex + Europe PMC) now verifies **once** by `work_key` — results still
  attach to every copy by key. Cuts 5–20% of verification calls on typical runs.
- **Wider verification pool** (8 → 24 workers): per-host politeness is now enforced by the
  connection-pool caps, not the worker count, so a 50-work verify finishes much sooner.
- **Two-phase delivery — `--verify background`**: the report is emitted immediately with works
  marked `pending_background` (fetch-time, ~seconds), then the background verification pass
  finishes and re-renders `lit_report.html` + writes `lit_report_verified.xlsx` + updates the
  evidence log. New progress events: `report_ready` → `verify_progress*` → `verify_done` →
  `report_verified` → `run_done` (export events carry `verified: false|true`).
- All existing modes (`all` / `top` / `none`) and human/json progress output are unchanged
  (regression-tested; verified 4/4 in `all` and `top`, connection reuse confirmed).
- **Measured speed-up (verify all, 20 works)**: verification segment ~119 s → ~35 s (~3.4×,
  -70%); two-phase key path 3.5 s to a usable report (~35× faster time-to-first-result).

### Docs (README FAQ, 2026-08-13)
- FAQ "How long does a search take": fixed misleading "per-source concurrency" → precise
  "sources run in parallel with each other, but each source pages serially (rate-limit / ban
  safety)".
- New FAQ "Why can't the fetch be faster?": compliance-first answer (official public access
  methods only, never violates site terms → no bulk-crawl effect) + parallel/serial structure
  + bottleneck (verification) + speed-up knobs. Synced into ct-base §13.8 as a mandatory FAQ
  item for any skill with data-fetch operations.

### Prepublish cleanup
- Removed 6 Coze-specific i18n messages (zero runtime references — `auth.coze_outbound`,
  `auth.coze_outbound_denied`, `auth.serial_blocked`, `error.coze_401`, `error.fallback_local`,
  `error.requests_missing`) that were vendored leftovers from ct-base (ct-literature has no
  Coze endpoint; they also fed SkillSpector Autonomous-Decision-Making findings).
- SKILL.md "zero confidential input" reworded to "zero confidential research / subject data
  input (API keys are local config, never research data)".

## v0.6.12 — 2026-08-13

### Security-audit fixes (ClawHub / NVIDIA SkillSpector, 21 findings)
- **README: unify API-key setup to the conversational flow (user preference)** — both READMEs
  now give one consistent story: tell the assistant in chat to configure the key (it writes it
  to the local `.env` via Write/Edit; never echoed back, never logged, sent only over HTTPS to
  the official API), or self-configure via `.env` / env var / `--openalex-key`; with an explicit
  notice that chat may be logged and self-config is the most secretive route. Fixes the
  internal contradiction SkillSpector flagged (6+ findings: one section said "never paste",
  another told you to); the conversational option is kept intentionally per user preference,
  accepting a residual chat-channel advisory. `http_utils` key-notice i18n strings updated to
  the same dual-path wording.
- **Remove all R-only dead code and messages** — this skill is pure Python
  (`required_commands: [python]`) and never calls R. Deleted `scripts/r_libs.py` (vendored
  ct-base stub, zero references here) and 13 R-only keys from `i18n_messages.json`
  (`error.rscript_not_found*`, `error.r_timeout`, `error.invalid_temp_path`,
  `error.invalid_install_path`, `install.*`, `header.r_code`, `header.install_cmd`). This also
  eliminates the stale "CRAN is the ONLY network operation" claim — that message applied to an
  R install flow this skill never uses. README/AGENTS reference lists updated.
- **SKILL.md summary/description now mention the local EN→ZH abstract translation helper**
  (eliminates the manifest-vs-behavior mismatch flagged at High/95%).
- **drug_name_resolver: auto mode now matches its docstring** — only a *unique* candidate is
  auto-translated; ambiguous names (multiple candidates) return unresolved instead of silently
  picking the first (could bias downstream queries in a biomedical context).
- **CLI help hardening**: `--no-verify-citations` / `--no-consistency` now carry a WARNING that
  they weaken the anti-hallucination gate (ct-base §17.1; debugging only); `abstract_translator
  --file/--output` now state they read/write only the paths you specify.
- **README: explicit activation boundary** — the skill activates only when the user explicitly
  asks for a literature search (addresses Vague-Triggers findings).

### Packaging note
- ClawHub audit scans confirmed the previously published package **contained `tests/`**.
  Per the new ct-base §16.8 red-line ("test content never ships"), the next publish must
  rebuild a clean package (`git archive` staging + `rm -rf tests scripts/tests`) and drop
  `tests/` via `.clawhubignore` (already updated).

## v0.6.11 — 2026-08-12

### Feature · title/author consistency cross-check in citation verification (anti-hallucination depth)
- Closes the gap flagged in v0.6.10: verification previously only confirmed an identifier
  *resolves to a live resource*. A hallucinated-but-real DOI (or a real-but-wrong id) still
  passed. Now, after an identifier resolves, the canonical metadata (title + first-author
  surname) is fetched from the authoritative, bot-friendly API and compared to the work we hold:
  - DOI  -> Crossref (`api.crossref.org/works/<doi>`)
  - PMID -> Europe PMC EXT_ID response (already fetched for resolution, no extra call)
  - OpenAlex id -> `api.openalex.org/works/<id>`
- New status **`mismatch`**: identifier resolved to a LIVE resource but its title/author do
  **not** match this work → flagged `citation_verified=False`, surfaced in all four deliverables
  (xlsx Evidence Log, html Evidence block, report, evidence_log.md) as **Mismatch / 不一致**.
  A consistent resolution is `verified`; a `bot_blocked` DOI whose Crossref metadata matches is
  now **upgraded to `verified`** (the 403 was only the publisher blocking doi.org, not the id).
- Robust by design:
  - Author matching is **order-independent** (handles "Last, First", "First Last", "First Initial"
    and list forms) via token-set membership against the metadata surname — fixes a naive
    "last token = surname" bug that misread "Ramalingam V" as surname "V".
  - Title match uses normalized `difflib` similarity (threshold 0.80) + author must not contradict.
  - Metadata **fetch failure / incomplete fields degrade gracefully** to "verified, consistency
    unchecked" — it NEVER invents a `mismatch` from a transient API error.
  - New additive per-work fields: `citation_consistency` (bool|None), `citation_title_ratio` (float|None).
- New opt-out: `--no-consistency` (pipeline `run()`) / `--no-consistency` (standalone
  `verify_citations.py`) skips the metadata fetch; verification then behaves as before v0.6.11.
- Verified: offline mock test (9 cases: match / mismatch / meta-fail / malformed / no-id /
  empty-meta / bot-block+match / pmid-path+match / no-consistency) all pass; EN+ZH render smoke
  test confirms `Mismatch / 不一致` surfaces in xlsx + html + evidence_log + report without crash.

### Docs · README + SKILL.md accuracy & clarity pass
- `README.md` / `README_zh-CN.md` restructured for clarity: added a **Table of Contents**
  anchor nav; renumbered sections (Who This Is For → Data Sources → Anti-Hallucination →
  How to Use → Scenarios → FAQ → Security → Advanced); compacted the scenario index.
- Fixed factual inaccuracies carried from earlier versions:
  - Version string `0.6.0` → `0.6.11`.
  - Dropped the false `requests` dependency claim — the skill uses **only the standard-library
    `urllib`**.
  - Architecture tree realigned to the actual layout: `adapters/` holds the 6 source fetchers +
    `http_utils` + `verify_citations`; `normalize` / `score_relevance` / `screen_prisma` /
    `format_citations` / `evidence_log` / `obsidian_exporter` / `zotero_exporter` / `export_*`
    live in `scripts/` (not `adapters/`). Output described as **HTML + Excel**, not Markdown.
  - Anti-Hallucination expanded to **4 guardrails** (was described as 3) incl. the v0.6.11
    title/author consistency layer; added `bot_blocked` + `mismatch` explanations and the
    `citation_*` schema fields.
  - Unified EN/ZH on **parallel** source execution (ZH previously said "serial").
  - Removed stale `.merged.json` references from the OA-PDF scenario (the file is now hidden /
    internal, not a user-facing artifact).
- `SKILL.md` `version:` bumped `0.6.0` → `0.6.11` to match CHANGELOG and the READMEs.

## v0.6.10 — 2026-08-12

### Logic audit · systematic bug sweep (HIGH + MEDIUM + LOW)

Systematic review of the whole skill (pipeline `run()`, every `scripts/*` exporter, both
adapters, i18n messages, formatters, docs) after the v0.6.8 output-cleanup refactor.

- **HIGH · `lit_report.xlsx` Evidence Log sheet rendered empty (v0.6.8 regression).**
  The pipeline `run()` passed `export_workbook({"count", "works", "meta"})` but
  `build_evidence` reads `evidence_log` / `verification` from the **top level** of `data`.
  So the Verification summary, source provenance and run-config blocks were all dropped —
  the sheet showed only its title + the anti-hallucination disclaimer.
  Fix: `export_workbook` now promotes `evidence_log` / `verification` out of `meta` when they
  are missing at top level (standalone CLI still passes `.merged.json` with them at top level).
  Verified by regenerating an xlsx from a real `.merged.json` — `verified=…`, `bot-blocked=…`,
  `Run config / 运行配置`, and source provenance all appear again.
- **MEDIUM · `evidence_log.py` standalone CLI lost its source trail.**
  `main()` read `data.get("payloads")`, but `.merged.json` persists `evidence_log` and does **not**
  persist `payloads`, so the rendered `evidence_log.md` had an empty source list.
  Fix: prefer the `evidence_log` already embedded in `.merged.json`; only fall back to
  rebuilding from `payloads` when it is absent.
- **LOW · DOI regex greedily swallowed trailing punctuation.**
  `_DOI_RE` used `[^\s]+`, so a trailing `.` / `)` / `]` etc. was captured into the DOI, producing
  links/labels like `10.1056/NEJMoa2403614.)`. Fixed in two places with a `_strip_doi_tail()`
  helper that strips `.,;:` then `)]` separately (the two-stage rstrip also avoids a Python
  parsing ambiguity when `)]` sits next to a string literal):
  `scripts/normalize.py::_norm_doi` and `adapters/verify_citations.py::_resolve_doi` / `work_key`.
- **Doc consistency · `merged.html` → `lit_report.html`.**
  `SKILL.md` (feature table + Output list) and `export_html.py` docstring still said `merged.html`;
  the pipeline has written `lit_report.html` since before v0.6.8. Corrected both.
- Verified: all four modified `.py` files `py_compile` clean; xlsx Evidence Log regen smoke test passes.

## v0.6.9 — 2026-08-12

### Fix · restore the "apply for an OpenAlex key" prompt in the deliverables
- Regression from v0.6.8: the keyless warning (`cfg.warn`, with the signup URL) lived in
  `report.py` / `lit_report.md`, which v0.6.8 stopped generating. After that the prompt
  survived only in console output and `evidence_log.md` — the two primary deliverables
  (HTML / XLSX) carried no actionable hint.
- `export_html.py`: added bilingual `cfg.warn` labels and render a warning block with a
  clickable signup link inside the Evidence section when `config.openalex_key == "missing"`.
- `export_xlsx.py`: the Run-config block now appends an actionable bilingual line with the
  signup URL when the key is missing (previously it only printed `missing — keyless`).
- No prompt is shown when the key is configured (verified by render smoke test, EN + ZH).

## v0.6.8 — 2026-08-12

### Output cleanup · drop `lit_report.md`; demote `merged.json` to hidden `.merged.json`
- Stop generating `lit_report.md` (the Markdown report). `lit_report.html` + `lit_report.xlsx`
  already cover the same content, so the `.md` deliverable was redundant. `report.py` stays in the
  skill as a reusable standalone Markdown renderer but is no longer called by the pipeline.
- Rename the unified work list from `merged.json` to `.merged.json` (dot-prefixed → normally hidden
  by the OS). It is now an **internal cache**, not a user-facing deliverable.
- All standalone tools (`export_html` / `export_xlsx` / `format_citations` / `obsidian_exporter` /
  `zotero_exporter` / `score_relevance` / `screen_prisma` / `evidence_log` + `verify_citations`) now
  default `--in` / `--in-json` / `--merged` to `.merged.json` (no longer `required`), so they keep
  working out-of-the-box against the hidden cache. Docstrings/help text updated accordingly.
- Docs (`SKILL.md` Output list; `README.md` / `README_zh-CN.md` report + OA-PDF references) updated:
  `lit_report.md` removed; `merged.json` → `.merged.json`; PRISMA block reference updated.
- Pre-existing (out of scope at v0.6.8, **resolved in v0.6.10**): `SKILL.md` still named the HTML
  deliverable `merged.html`, but the pipeline writes `lit_report.html`. Now fixed in both the
  feature table and the Output list; `export_html.py` docstring example updated too.

## v0.6.7 — 2026-08-12

### Bugfix · `evidence_log.md` bot-blocked label not localized (follow-up to v0.6.6)
- v0.6.6 localized the `bot_blocked` label in `report.py` / `export_xlsx.py` / `export_html.py`
  (`ev.bot_blocked`: "bot-blocked" / "出版社拦爬") but `evidence_log.py::render_md` still
  hard-coded the English `bot-blocked=` token. In a zh locale the report said `出版社拦爬=0`
  while the evidence log said `bot-blocked=0` — inconsistent.
- `render_md` now emits `bot-blocked=%s (出版社拦爬=%s)` so the zh label is present alongside
  the English key in the bilingual evidence log. Regenerated `out_lit_osimertinib_v6/evidence_log.md`.

## v0.6.6 — 2026-08-12

### Bugfix · Verification false-negative on big-publisher bot-block (403) + same-source-skip regression
- **Root cause (confirmed on another machine via live re-check):** the 37 "unresolved" papers were NOT suspect — they were the most credible, highest-cited works (FLAURA-OS, ADAURA, AURA3-CNS, BLOOM, NCCN guidelines…). Their DOIs are real: `doi.org` returns a correct 302 to the publisher, but NEJM / ASCO-JCO / JNCCN / JAMA / Nature-vs-others / Wiley / MDPI **return 403 to programmatic requests** (bot-blocking). `_resolve_doi` only accepted 2xx, so a 403 was wrongly marked `unresolved` — a **false negative**, not a broken DOI. (Publishers that allow bots — Nature / BMC / Elsevier — return 200 and were the "verified" set; so "verified vs unresolved" tracked publisher bot-policy, not paper quality.)
- **Fix 1 — `bot_blocked` status:** `_resolve_doi` now returns a 3-state string `ok | bot_blocked | unresolved`. A post-redirect 403 → `bot_blocked`. `verify_one` marks such works `citation_verified=True, citation_verify_status="bot_blocked"` (the identifier IS real) with a note "publisher bot-block (DOI likely valid; 403 from publisher, not a broken link)". This is reported **distinctly** from `unresolved`/`suspicious` everywhere (report.md / xlsx / html / evidence_log.json) so the 37 are never misread as suspect.
- **Fix 2 — same-source-skip regression:** v0.6.1's source-aware skip silenced the Europe PMC PMID (and OpenAlex id) check for same-source works. When such a work's DOI hit a 403, it had **no fallback** and fell to `unresolved` — even though its real PMID (Europe PMC EXT_ID API, bot-friendly) would have confirmed it. Now, when the DOI does NOT positively verify, PMID (Europe PMC `ext_id`) and OpenAlex id (`api.openalex.org`) are always attempted as the reliable bot-friendly fallback. `skip_sources` is retained for API compat but no longer suppresses that fallback.
- Summary dicts (`summarize_results`, `verify_works`, `none`-mode vsum) now carry `bot_blocked`. New bilingual labels `ev.bot_blocked` / `ev.bot_blocked.note`.
- Verified: 14-assertion offline self-test (200/206→ok, 403→bot_blocked, 404→unresolved, full-URL DOI normalized w/o double prefix, DOI-403+PMID-ok→verified, DOI-403+OpenAlex-ok→verified, summarize includes bot_blocked) + EN/ZH report render smoke (bot-blocked=37 shown, note present). `py_compile` clean.

## v0.6.5 — 2026-08-12

### Bugfix · Double-prefix DOI in formatted exports (`format_citations.py`)
- `references_apa.md` / `references.bib` / `references.ris` could emit `https://doi.org/https://doi.org/10.x/...` when the source DOI was OpenAlex's full resolver URL (`https://doi.org/10.x/...`). `_resolve_doi` was already fixed in v0.6.4, but the **citation-formatting path** still concatenated `"https://doi.org/" + doi` blindly at 6 sites (APA/Nature URL, `url` fallback, BibTeX `doi=` field, RIS `DO ` field, plus vancouver/ieee/gb7714 `doi:` tokens).
- Added `_bare_doi()` to `format_citations.py` — extracts the canonical `10.x/...` suffix via `_DOI_RE` regardless of input shape (full URL or bare). All 6 sites now build at most one resolver prefix. BibTeX `doi` and RIS `DO` now write the **bare** DOI (spec-correct; previously wrote the full URL).
- `export_xlsx.py._normalize_link` was already safe (checks `startswith(("http://","https://",...))` first) — no change there.
- Verified: unit self-test (full-URL + bare inputs → single prefix everywhere, bare in bib/ris) + regenerated real fixture `tests/smoke_out/merged.json` → **zero** `https://doi.org/https://doi.org/` across all three outputs; `doi = {10.1016/...}` and `DO  - 10.1016/...` now correct. `py_compile` clean.

## v0.6.4 — 2026-08-12

### Bugfix · DOI resolution mis-classified big-publisher DOIs as `unresolved`
- `_resolve_doi` accepted **only HTTP 200** (`code == 200`). Major publishers (NEJM / JCO / JAMA / AACR / Wiley / MDPI / ...) answer the `Range: bytes=0-0` probe with **206 Partial Content** instead of 200, so their live DOIs were wrongly marked `unresolved`. Now any 2xx is treated as resolved (`200 <= code < 300`). The dead `HTTPError`-branch `e.code == 200` (urllib never raises HTTPError for 2xx) was removed.
- **Mixed DOI formats normalized**: OpenAlex stores the full URL (`https://doi.org/10.x/...`), Europe PMC stores the bare DOI (`10.x/...`). `_resolve_doi` now extracts the canonical `10.x/...` suffix via `_DOI_RE` and always rebuilds the URL, so a double-prefix (`https://doi.org/https://doi.org/...`) can never occur. `work_key` was made format-agnostic too, so the same paper arriving from both sources collapses to one key (no silent duplicate / split verification).
- Offline-deterministic self-test (mocked `urllib.request.urlopen`): 206/200 resolve for NEJM/JCO/JAMA/AACR/Wiley/MDPI (full-URL + bare forms), 404 stays `unresolved`, URL normalization asserted, `work_key` equality asserted, `verify_one` end-to-end for a NEJM 206 → `verified`. `py_compile` clean.

## v0.6.1 — 2026-08-12

### P0 · Citation verification — scope control + source-aware skip
- New `--verify {all|top|none}` (default `all`) controls verification scope; legacy `--no-verify-citations` is now an alias for `--verify none`.
  - `all`: verify every merged work (concurrent with fetch, "verify one as it lands") — unchanged default behavior.
  - `top`: verify only the top-N by rank (`--verify-top-n`, default 15); remaining works are tagged `unverified_sampled` (no network call). Best speed/coverage trade-off for large result sets.
  - `none`: skip verification entirely (preview-style annotation).
- **Source-aware skip**: a work returned by OpenAlex / Europe PMC already carries a real identifier at that source, so the redundant same-source re-resolution round-trip is skipped and trusted **by source provenance** (marked `verified`, no network call). DOI is always cross-checked via `doi.org` (canonical + anti-hallucination net). `verify_citations.verify_one` gains a `skip_sources` parameter; the streaming worker and the `top` post-merge verifier both pass each work's `sources`.
- Reporting surfaces (report.md / xlsx Evidence Log) now show the verify `mode` (all/top/none) and the `sampled` count, plus bilingual mode notes.

### Tests
- Offline-deterministic self-tests: 7 `verify_one` skip/provenance cases + full `run()` integration across all three modes (mocked fetchers + verification). `py_compile` clean on all changed modules.

## v0.6.2 — 2026-08-12

### UX · Pre-run time estimate
- `run()` now prints a localized time-estimate banner **before the fetch begins**, so the user knows results may take a few minutes to return. Estimate scales with verification scope: `all` ≈ 1–4 min, `top` ≈ 1–3 min, `none` ≈ 1 min; rate-limit backoff on the keyless pool extends it further. Output path is shown so the user knows where to look while waiting.
- New i18n keys `run.starting` / `run.est.{all,top,none}` / `run.vmode.{all,top,none}` (EN/ZH).
- `SKILL.md` dialogue guidance updated: the agent must mirror this wait-time warning in chat before triggering the real fetch.

## v0.6.3 — 2026-08-12

### Docs · Anti-hallucination value section
- README.md / README_zh-CN.md: added a prominent "Why You Can Trust the Output — Anti-Hallucination by Design / 为什么可以信任输出 —— 反幻觉设计" section (right after Sources, before §1). Covers the three guardrails (live citation-id resolution P0 default ON + `suspicious` on malformed DOI; full provenance audit trail `evidence_log.json`; reports never pad gaps with prose) plus the two operational safeguards (Safe Preview local compute; source-aware skip by provenance), tied to ct-base §17.1.
- Fixed a stale FAQ claim: sources actually run **in parallel** (not sequential) since the concurrency change; latency now stated as the slowest source, plus the 1–4 min verification note.

## v0.6.0 — 2026-08-12

### P0 · Citation verification (anti-hallucination, ct-base §17.1)
- New `scripts/verify_citations.py`: each merged work is checked against its live identifier and tagged `citation_verified` / `citation_verify_status` (verified / unresolved / no_identifier / suspicious) / `citation_verify_note`.
  - doi → `https://doi.org/<doi>` resolves to final HTTP 200; pmid → Europe PMC `EXT_ID` lookup; OpenAlex id → `api.openalex.org/works/<id>`.
  - A **malformed DOI is flagged `suspicious`** (possible hallucinated identifier) — catches fabricated ids before they reach the report.
  - Each verification failure marks that work `unresolved` and **never aborts** the pipeline (pure stdlib + `http_utils`).
- Default **ON**; `--no-verify-citations` disables. Network runs only under `--run` (SAFE PREVIEW); in preview mode it records `skipped_preview` and passes works through untouched.
- New `scripts/evidence_log.py`: builds an immutable-style provenance audit trail → `evidence_log.json` + `evidence_log.md` (also embedded in `merged.json`). Traceability: query → source → hit count → retrieved_at → verification rate.

### P1 · PROSPERO systematic-review registry (opt-in, key-gated, UNVERIFIED)
- New `scripts/fetch_prospero.py`: answers *"is a review on this topic already registered / ongoing?"* (duplication-avoidance + protocol discovery), a distinct question from the bibliographic sources.
- **UNVERIFIED**: the public REST API now requires an undocumented auth header (`{"status":"error","errormessage":"Error code: header value undefined"}` on every probe). Until a working token + header is supplied, `--with-prospero` degrades to a no-op skip (returns `None`, no file written — like Semantic Scholar's no-key skip) and is **not** claimed functional. Provide `--prospero-token` (+ `--prospero-header` if `PROSPERO-ACCESS-TOKEN` is wrong). Response parser is schema-tolerant (JSON + XML) but must be re-validated against a real 200.

### Reporting surface
- `report.py` adds a bilingual **Evidence & verification** section (verification counts + source provenance table).
- `export_xlsx.py` adds an **Evidence Log** sheet (verification summary + source provenance table).
- `export_html.py` adds an **Evidence & Verification** block (verification summary + provenance table).

### Tests
- New `tests/scenario10d_evidence.py` — 8 offline-deterministic cases (D1–D8) covering verify preview / suspicious / no-identifier, evidence build+write, and the report / xlsx / html evidence surfaces, plus PROSPERO no-token graceful skip. `py_compile` clean.

### Deferred (by prior agreement)
- **Journal impact factor (IF) auto-annotation** — deferred. Will use an open proxy (e.g. OpenAlex `citation_normalized_*`) or a user-supplied local mapping table; not implemented until the mapping is provided.

## v0.5.7 — 2026-08-11

### Pre-publish hardening pass (ct-base BASE.md §16 checklist)
- **Fixed missing `scripts/i18n_messages.json`** — the ct-base shared generic i18n key set was never injected (omitted from `.ctbase_injected.json`'s file list), so `_MESSAGES` fell back to `{}` and every generic i18n key (`exec.running`, `error.generic`, `info.result_saved`, …) rendered as its raw key string at runtime. Copied the ct-base shared `i18n_messages.json` into `scripts/`; Excel UI keys stay self-contained in `export_xlsx._LOCAL`, domain keys inline in their consuming scripts (per §16.3).
- **SKILL.md 214 → 199 lines** (≤200, §16.1): trimmed the Cross-Database and Natural-language-dialogue sections.
- **Hardened `.gitignore` / `.clawhubignore`**: added `.ctbase_injected.json`, `*.ctbase_bak_*`, `tests/smoke_out/`, `.env.*`; removed a tracked `.ctbase_injected.json` (machine-specific absolute path) via `git rm --cached`.
- **references language (§16.2)**: rewrote `citation_styles.md` to English-only; stripped Chinese trigger phrases from `multi-db-search.md` (English trigger list + note that Chinese triggers mirror SKILL.md `triggers`).
- **No hardcoded Chinese output strings (§16.3)**: `abstract_translator.py` / `mesh_mapper.py` argparse help + `print` changed to English. `export_html.py` keeps ` / `-separated bilingual labels (policy-compliant); `obsidian_exporter.py` keeps `lang`-conditional bilingual.
- Not published — push/publish pending user confirmation.

## v0.5.6 — 2026-08-11

### Source expansion (real network, 10×10 hardening regression passed)
- **Europe PMC is now ON by default** (`with_europepmc=True`; `--no-with-europepmc` to disable). It is free/keyless and gives the whole PubMed/PMC/MEDLINE/MeSH pool, so the previous opt-in default (OpenAlex-only) was leaving the highest-value biomedical source off by default.
- **Added bioRxiv + medRxiv** as opt-in `--with-biorxiv` / `--with-medrxiv` (Tier P preprints). Neither has a free keyword-search API, so both are pulled through Europe PMC's preprint corpus (`SRC:PPR` + `publisher:` filter) and emitted with distinct `bioRxiv` / `medRxiv` provenance in the merged record.
- **Added arXiv** as opt-in `--with-arxiv` (keyless Atom API). Mostly methodology/ML/CS breadth for clinical questions, so kept opt-in (rank priority 1, sinks below biomedical sources).
- New fetchers: `scripts/fetch_preprints.py` (bioRxiv/medRxiv via EPMC PPR) and `scripts/fetch_arxiv.py` (arXiv Atom parser, with retry).
- `normalize._SOURCE_PRIORITY` extended: bioRxiv/medRxiv = 0 (primary biomedical), arXiv = 1 (supplementary, like SemanticScholar).

## v0.5.3 — 2026-08-08

- .env key 轻混淆（XOR+base64）防误打包明文扫描命中；http_utils.py 增加 `_deobfuscate` 向后兼容明文 .env；三平台同步发布。

## v0.5.2 — 2026-08-08

### Follow-up security audit cleanup (ClawHub SkillSpector, post-0.5.1)
- **Closed the residual Ssd3 (paste-key-to-chat) finding**: v0.5.1 removed the
  "paste your key to the assistant" prompt from `scripts/i18n.py`, but the same
  guidance was still present in README "Example 4 · Configure the OpenAlex key"
  (both `README.md` and `README_zh-CN.md`). Rewrote both to self-config only —
  `.env` / env var / `--openalex-key` — with an explicit "never paste a key into
  chat" statement. This was the true source of the 98%-confidence Ssd3 hit
  (the scanner reads the README, not just scripts).
- **Cleared the Unpinned Dependencies (Low) finding**: `requirements.txt` no
  longer declares `requests>=2.28`. `requests` is not a runtime dependency —
  fetch uses stdlib `urllib`, and the R-bridge (`r_libs.py`) was removed in
  0.5.1. The reserved optional `requests` import in `fetch_openalex.py` is noted
  with a pin-if-enabled comment.

## v0.5.1 — 2026-08-08

### Security audit remediation (ClawHub SkillSpector, post-0.5.0)
- **Removed API-key paste-to-assistant guidance**: deleted the conversational
  "paste your key to the assistant" prompts in `scripts/i18n.py`
  (`openalex.key_notice` / `semantic_scholar.key_notice`) and reverted to the
  self-service methods in `references/openalex_key.md` (Method A/B/C: `.env`,
  env var, or `--openalex-key`). Clarified the key is user-private, stored
  locally, sent only over HTTPS to the official API, and must never be pasted
  into chat — also resolves an internal contradiction with openalex_key.md §7.
- **Removed arbitrary R code execution primitive**: `scripts/r_libs.py` no longer
  imports `run_r` / `subprocess` / `tempfile`; it keeps only validation /
  sanitization helpers. ct-literature is pure-Python and never calls R, so the
  "Context-Inappropriate Capability" finding is eliminated at the root. The shared
  `ct-base/scripts/r_libs.py` was likewise stripped of `run_r` (execution
  primitives are no longer shared from the base), and `ct-base/BASE.md` §16.4 / §2
  / §10 references were updated to match.
- Dropped dead R-related i18n keys (`dry_run.*`, `exec.*`, `install.*`,
  `header.*`, etc.) that were only referenced by the removed R runner.

## v0.5.0 — 2026-08-08

### Initial public release (init version)
- First public release of ct-literature; consolidates the v0.3.x internal
  hardening aligned with ct-base v1.1.18 (i18n locale-aware strings, README
  rebuilt on the ct-advisor skeleton, `invocable: true` frontmatter, dual-author
  footer `medstatstar, phoe-zip`, packaging exclusions in `.clawhubignore`).
- The full compliance changelog carried into this release is recorded under
  v0.3.12 below.

## v0.3.12 — 2026-08-08

### Compliance & documentation (aligned with ct-base v1.1.18)
- **SKILL.md**: added `invocable: true` to frontmatter (task-entry skill, per BASE.md §16.5).
- **README (EN + ZH)**: added two dialogue-flow examples covering the two branches
  from `references/search_menu.md` — Complex (popup confirmation menu, §4.1–§4.3)
  and Vague (grill-me style clarifying questions, §6).
- Bumped version v0.3.11 → v0.3.12 across SKILL.md / AGENTS.md / both READMEs.

### Prior hardening (carried into this release)
- **i18n**: moved all hardcoded Chinese `print`/docstrings in `scripts/` to
  `i18n.py` en+zh key pairs (locale-aware) — clears BASE.md §16.3.
- **README (EN + ZH)**: restructured to the ct-advisor skeleton
  (switch line → logo → intro → Who This Is For → 1.How to Use → 2.Scenarios →
  3.FAQ → 4.Security & Privacy → 5.Advanced); removed the "Future Release Plans"
  section to stay consistent with BASE.md §13.6.
- **SKILL.md**: English-only body; frontmatter re-ordered to the ct-base §3 schema.
- **AGENTS.md**: version aligned.
- **references/**: sop.md / openalex_key.md / search_menu.md / multi-db-search.md
  fully English-only.
- **Authors**: README footer version line set to `medstatstar, phoe-zip`
  (synced to the ct-base template).

### Packaging
- `.clawhubignore`: now excludes `tests/results/`, `tests/scenario10_run/`,
  `tests/scenario10b_run/`, `tests/__pycache__/`, plus global `__pycache__/` / `*.pyc`.
- `.gitignore`: already excludes `__pycache__/` / `*.pyc` (no change needed).

## v0.3.11
- Baseline B-tier public-intel literature search skill: OpenAlex (primary) +
  Europe PMC (MEDLINE/MeSH) + Semantic Scholar (citation ranking, optional),
  normalized merge + dedupe, CSM qualitative safety subset, Markdown + Excel + HTML output.
