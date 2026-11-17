# Changelog


## 1.0.1 · 2026-11-15 · 工作台三处线上缺陷修复（空态图标 / 端口自查 / 顶栏按钮）

基于 1.0.0 上线后的真实用户反馈与覆盖部署实测，修三处**只在具体环境条件下才暴露**的缺陷。功能与接口契约不变，均属健壮性修复：

- **首屏空态图标爆炸**（用户反馈「全新进入时检索结果区显示错误」）：空态 SVG 只写 `viewBox`、无内联尺寸，尺寸完全依赖 `tokens.css` 的 `.wb-empty-ic svg{width:100%}` + 父级 30px。CSS 未加载/命中旧缓存时 SVG 回退撑满容器，实测放大到 **1176×1176**，把「尚无检索结果」文案挤出可视区。修复：空态 SVG 补 `width="30" height="30"` 内联兜底（CSS 正常时仍以 100% 覆盖，视觉不变）。
- **覆盖部署启动自杀**（部署回执 `SITES_START_FAILED / 端口 3000 已被占用`）：`server.py` 的 `_port_free()` 用裸 socket（未设 `SO_REUSEADDR`）做「端口占用即退出」自查，覆盖部署时旧连接处于 `TIME_WAIT`，裸 socket bind 失败被误判为占用 → `SystemExit(1)`；而真正服务的 `ThreadingHTTPServer` 默认 `allow_reuse_address=True`，本可正常 bind。修复：移除该误判自查，交给 bind 自然失败 + 平台重启。
- **顶栏「反馈」「CT 首页」格式错乱**（用户反馈「右上角这两个按钮格式仍然不对」）：顶栏四控件中 `.wb-lang`（EN）与 `.wb-topbar .wb-pill`（已就绪）内联已写 `background:transparent` 兜底，**唯独 `.wb-topbar .wb-btn` 只覆盖了尺寸**，配色 100% 依赖 `tokens.css` 的 `:root[data-brand="ct-tier-a"]` 段。当 `--wb-panel` 可用而品牌档规则缺席（旧版 CSS 缓存 / 加载不全）时，这两个按钮回退到 `.wb-btn{background:var(--wb-panel)}` —— 蓝顶上的白底墨字方块。修复（逐项对齐 ct-base 权威模板）：① 内联补 `.wb-topbar .wb-btn` 及 `:hover` 的 ghost 全套；② `.wb-topbar .wb-pill` 描边改 `--wb-topbar-hairline`、补 `min-height:34px`（原 33px，与按钮差 1px 不齐）；③ 两图标 `stroke-width` 1.8 → 2.0（与 EN 一致）、CT 首页房子 path 换模板同款、补内联 `width/height="18"`；④ `#wb-bug` 补 `title` / `aria-label`，`#wb-cthome` 补 `aria-label`；⑤ `tokens.css` 引用加 `?v=20261115b` 版本号，断掉用户旧缓存。

**版本锚点统一 `1.0.1`**：`SKILL.md` frontmatter 与正文 `Deliverable language`、`README.md` / `README_zh-CN.md` 页脚、`AGENTS.md` 标题、`workbench/workbench.config.json`、`workbench/app.config.json`、`workbench/index.html` 内嵌配置兜底、`references/published_app.md` Version anchors 与冒烟清单、本条首记录；`workbench/publish/` 载荷按 Re-publishing protocol 重跑 `build_publish.py`。

**验证**：本地 Playwright 双场景（正常加载 / 拦截 `tokens.css` 并删掉 A·AB 档 ghost 块模拟旧版缓存）——四控件底色均 `transparent`、高度均 34px、图标均 18×18，两场景结果一致；空态图标 CSS 正常与缺失两场景均锁 30×30。线上实测：顶栏四控件 `top` 全为 18 齐平、空态图标 30×30、`/api/health` 返回 `mock:false`、console 无错误；`tokens.css?v=20261115b` 返回 200 / 51,712B。发布闸门：PRE / SECURITY（P0=0 / P1=0）/ POST 全 PASS，前端 8 资源字节级 MATCH。

**已知平台差异（记明）**：README 两份首屏展示图 `assets/screenshots/{en,zh}/01-home.jpg` 依赖 `.jpg`，**SkillHub 白名单不含位图扩展名，上传时会擦除该文件 → SkillHub 页面上该图 404**；GitHub / ClawHub 侧图片正常。判定为可接受的平台白名单限制（与 ct-literature 同款处置），仅影响展示图，不影响技能功能与文档正文。

## 1.0.0 · 2026-11-15 · 首个正式发布版（发布准备）

对齐 ct-base §16 与 Ct-Update 发布审计后升版 `0.14.5` → `1.0.0`。本次实质变更集中在文档规范与交付卫生，**功能层不变**：

- **README 案例按 ct-base §13 全面重写**：中英双版删除 6 个编造式「概要 / 示意」案例，改为 2 个双通道实跑案例（对话通道 CLI + 工作台通道 `/api/plan` / `/api/search` / `/api/download`）；章节重排为「两种使用入口 → 能力一览 → 使用案例 → 数据源与状态」；每案例具备「你这样说 / 助手会这样回 / 🖥️ 工作台」三要素；中文真源、英文逐句直译、数值集合同源；案例区技术细节零披露。劣势场景（中文表单 0 命中、WHO+CDE 全球检索回落、PubChem 双通道不一致）按 §13.21 淘汰并留实跑痕迹。
- **`SKILL.md` frontmatter `description` 与 `summary` 对齐**：中文段逐字一致，英文段删除 pytrials / Zero user-side 旧句，保持「英文在前 / 中文在后 + ` / ` 分隔」；正文与历史 CHANGELOG 中的 pytrials 功能说明属非 frontmatter 历史记录，未动。
- **冗余文件清理**：按精确白名单移除 94 个文件 / 13.47 MB（历史部署 zip、`.bak_*` 备份、`runs/` 运行时产物、`__pycache__`、临时脚本等），完整备份 + 逐文件 MD5 复核 + 回收站分批删除，0 残留；`workbench/publish/` 发布载荷、`.gitignore` / `.clawhubignore`、Coze 部署包均保留。
- **版本锚点统一 `1.0.0`**：`SKILL.md` frontmatter 与正文 `Deliverable language`、`README.md` / `README_zh-CN.md` 页脚、`AGENTS.md` 标题、`workbench/workbench.config.json`、`workbench/app.config.json`、`workbench/index.html` 内嵌配置兜底、`references/published_app.md` Version anchors 与冒烟清单、本条首记录；`workbench/publish/` 载荷按 Re-publishing protocol 重跑 `build_publish.py`（85 文件 / 1.53 MB / PRUNED 0），源与载荷关键文件逐字节一致。

**验证**：`spec_lint.py` ERROR 0（WARN 5，均为存量软上限）；`shared_sync_check.py` 漂移 0 / exit 0；`capability_parity.py` PASS（0 fail / 0 warn，version anchors 1.0.0）；`publish_gate.py` P0=0 / P1=0（WARN 2：SEC7 安全头、GZIP 待部署后带 `--app-url` 复核）；`publish_parity_check.py` DRIFT 0；`registry.py check` PASS。完整清单见 `ct-registry-release-1.0.0-check-20261115.md`。

## 0.14.5 · 2026-11-14 · 对照 ct-base v1.4.46 最新工作台界面规范整改

按 2026-11-14 晚间 ct-base 规范批次（§19.2 顶栏 `color-mix` 实底配方、§30.9 ④ 主内容区显式背景、§30-⑤ 白裸值废止、§32.5 状态三态色值、§11.8 窄屏 44px）整改 `workbench/index.html` 与 `workbench/wb-list.css`：

- 顶栏状态 pill 四态与中性控件（语言 / 反馈 / CT 首页）统一改 `--wb-pill-base` 实底配方，文字 `--wb-on-topbar`；清除全部硬编码半透明白与裸白值；spinner 改 `--wb-on-brand` 浅环；内容区「连接中」由自造蓝 hex 改警示色三件套。
- `.wb-main` 显式 `background:var(--wb-bg)`；正文链接按 §5.6.3-8 补 `.wb-main a` 并分面处理 `--wb-brand-soft` 对比度；状态 pill 文案包 `.wb-pill-t` 出省略号；运行记录「来源」列空值弱化为 `--`。
- `wb-list.css`：`16px` 改 `var(--wb-fs-lg)`（iOS 聚焦防放大不变），窄屏媒体查询补 `.wb-list-size select{min-height:44px}`。

同步：`references/term_map.json` 的 4 个新词回写 ct-base 真源；`workbench/publish/` 发布包重跑 `build_publish.py` 刷新；README 双版版本信息行对齐 0.14.5。另清理页面 zh/en 词典中 8 对零消费的孤儿键（`snapTip` / `historyEmpty` / `planWarnMiss` / `planRiskNone` / `planBtnClose` / `planApplied` / `planGroupsLabel` / `planPlanOnly`），配合 ct-base §29.2 判据修订，页面审计由 75 条 WARN 归零。

**验证**：主题机检 P1=0 / WARN=0；结构闸门 C1–C8 P1=0；契约 `--check` 全 unchanged（14 块）；共享件一致闸门 exit 0；`spec_lint` ERROR 0（剩 3 条存量软上限 WARN）；`build_publish.py` 重跑后 publish 与源逐字节一致。浏览器 1440×900 / 390×844 实测：顶栏四态 computed 全为不透明 `color(srgb …)`（对比度 7.84 / 7.17 / 9.80 / 11.20，均 ≥4.5）、窄屏每页选择器与顶栏按钮均 44px、`.wb-main` 显式底色生效、列表 `table-layout:fixed` + 6 `<col>`、来源列空值 `--`，console 无错误。

**后续（同日晚，随 ct-base v1.4.48 契约上移）**：窄屏 44px / 聚焦字号规则纳入 `@wb-contract:list-pagesize-mq` 并单源下发（含本页内联 `<style>` 段），不再留在契约外自由段；`.wb-cell-empty` 下沉 `tokens.css` 单源，本页删本地定义改引类；契约注释去掉 HTML 标签字面量，消除页面审计 `DUP-ID` 假阳性。发布包重跑后与源逐字节一致，390px 实测每页选择器 44px、搜索框 16px、顶栏按钮 44px、console 0 error。

## 2026-11-13 · 共享资产契约同步（§11 / §19.2，非 UI 决策变更，页面版本号不变）

按 ct-base 2026-11-13 增补批次同步共享资产：`workbench/wb-list.css` 注入卡片动作统一右列锚点（`.wb-list-cardacts-bottom` + `--wb-cardact-right` / `--wb-cardact-gutter`）；`workbench/tokens.css` 补 `--wb-pill-base` / `--wb-cardact-right` / `--wb-cardact-gutter`；`publish/` 下同名副本一并同步（另把 `index.html` 内联列表样式的旧 `right:10px` 改为新契约，publish 副本同步）。

采用**精确注入**而非整文件覆盖：ct-base 真源 `wb-list.css` 的字号仍是裸 px，多数叶子已自行令牌化；整文件覆盖会把字号退回裸 px，并可能丢失技能自有令牌/增强，故只替换契约部分、保留其余原文。

**验证**：CSS 花括号平衡；Playwright 实测 `--wb-cardact-right=10px`、`--wb-cardact-gutter=0px`、`--wb-pill-base` 生效，右上/右下动作规则均取 `var(--wb-cardact-right)`、`cardbody` 取 `var(--wb-cardact-gutter)`，页面 JS 错误 0；publish 副本与源逐字节一致。

## 0.5.02 · 2026-11-11 · CDE 英文关键词本地化 + 浏览器反检测 + fail-loud（端点，待部署）

> 2026-11-11 晚补（确认门审计修复，随本版本一并部署）：
> - **P0-1 `chictr_search_node.py`**：ChiCTR 节点接入 `_cde_localize_keyword` 本地化
>   （此前 L114-116 裸发英文），loc_log 透出 `keyword_localization`；ChiCTR 收录英文
>   题目 → fail_open 记录标 `untranslated_risk:false`（放行知会不阻断）。
> - **P1-2 `search_ictrp.py`**：①`_parse_response` 透传内层 dict 形态的
>   `keyword_localization`（此前仅字符串形态经 project_list_raw 保留）；②新增
>   `_gate_records_from_who_metas()`——WHO 中→英本地化 meta 转门契约记录（term_map/
>   online→whole、miss→fail_open+risk:false、same→native_en），主路径 run() 与
>   `_fallback_who_for_source()` 均并入信封。
> - **连带修复**：`cde_search.py` 补 `import os`（0.5.02 编辑遗漏，部署即 NameError）。
>
> 2026-11-11 晚补二（request_id 同请求多行归因，随本版本一并部署）：
> - **背景**：feishu_log_fetch 30 天诊断实证——registry 691 行中 292 行（42%）属
>   「同请求多行」语义（94 个时间簇），querystr 无任何请求标识，治理判重只能靠
>   时间窗猜。advisor 已用 request_id 解决同问题，registry 对齐。
> - **端点侧**：`state.py` GraphInput/GlobalState/FeishuWriteInput 三处声明
>   `request_id`；`feishu_write_node.py` 写入飞书**独立列** `request_id`（同
>   entry_point 模式），列未建时自动剥离该列重试（优雅降级不丢行）。
> - **调用侧**：`search_ictrp.py` `_attach_coze_contract()` 注入 `request_id`
>   （优先级 CLI --request-id > env `CT_REGISTRY_REQUEST_ID` > 进程内 uuid4，
>   args 缓存保证 escalation/fallback 重发同 ID）；`ct_registry.py` run() 顶层
>   生成一次并经 env 透传给全部子进程——同轮多源/多腿共享同一 request_id。
> - **分析侧**：ct-update `feishu_log_fetch.py` 新增 §6 request_id 折叠维度；
>   治理判重口径改为 (request_id, call_type)——同 ID 下 analysis/subcall 各一行
>   属合法分腿，同 ID 同 call_type 多行才是真重复。
> - **部署后手工步骤**：飞书 searchlog 表加文本列 `request_id`（列名精确小写）；
>   未加前写入自动降级（该列暂空），加列后自动恢复。

**背景**：auto_check 深挖发现 CDE 30 天 empty 率 77%（171/223），empty 中位
runtime 5.1s（159/171<10s）vs ok 中位 15.7s。经本地 headless Chromium 现场实测
（Anaconda Playwright，2026-11-11），根因分层定型——

1. **主因：CDE 中文库英文关键词 0 命中**。实测 `keywords=奥希替尼` → 20 条，
   `keywords=osimertinib` → 0 条。30 天 empty 关键词多为英文药名/公司名。
2. **公司名检索**：站点改版后 GET 结构化参数**已被支持**（2026-08-14「只认
   keyword」结论过时）——实测 `appliers=圣因生物` → 10 条、`appliers=北京安龙`
   → 5 条、`drugs_name=甲磺酸奥希替尼片` → 9 条；`keyword` 现也覆盖申办者文本。
3. **WAF（次因）**：站点部署瑞数类 WAF（HTTP 202 + JS 挑战页，特征 meta
   `id="9DhefwqGPrzGxEp9hPaoag"`）。本地实测 headless Chromium 可通过；云端
   此前 5s empty 另有原因（预热循环假成功——挑战页 25KB>1000 字节被当作
   「已通过」即开始抓取）。

**修复（全部编译通过 + 离线/实测验证）**：

- **`cde_search.py`**：
  - 新增 `_cde_localize_keyword()`——纯 ASCII 关键词经 `_cde_drug_zh.json`
    （en→zh 反查表，501 条，生成自 references/drug_name_map.json v1.1）翻译为
    中文；多词查询逐词映射；查无映射 fail-open 保留原词。接入全部 4 处 URL
    构造点（_build_search_url / _probe_cde_keyword / multi_keyword 主检索 /
    silent_fallback 补发）。
  - WAF 挑战页 fail-loud：命中挑战页指纹显式上报 `error="CDE_WAF_CHALLENGE: …"`
    （不再伪装 0 结果）；首页加载挑战重试最多 2 次。
- **`browser_utils.py`**：
  - 修复预热假成功：旧循环 `len(content)>1000` 在 25KB 挑战页上立即 break；
    新判据 = 内容正常且非挑战页（15×2s 窗口）。
  - 指纹增强：UA 升级 Chrome/120→131（旧 UA 本身是检测信号）、locale/时区/
    viewport/Accept-Language、plugins/languages/chrome 对象/permissions 伪装；
    is_waf_challenge() 单一真相源移至此处，cde_search 复用。
- **`feishu_write_node.py`**：① 文献族 source（lit_*/prospero/pubmed/
  citation_verify）skillname 归 `ct-literature`；② `skill_version` 归一（调用方
  前缀拆 `client_version` 单列）；③ resultstr 新增 `call_type` 与 `answer_hash`。
- **`search_node.py`**：检索层 error（含 WAF）透传到 project_list JSON。
- **新资产**：`src/graphs/nodes/_cde_drug_zh.json`（en→zh 反查表，自包含）。
- **翻译确认卡（对话/工作台层）**：结果 JSON 新增 `keyword_localization` 数组
  （original/localized/candidates/mode/ambiguous），所有输出路径（主流程/
  multi_keyword/silent_fallback/single_fallback，含空结果分支）均透出；
  `references/search_procedure.md` 新增 §Translation Confirmation Card——
  ambiguous 多候选或 fail_open 英文残留时对话层必须停下确认后重跑
  （`--cde-keyword` 注入用户确认的中文词），单候选仅知会不阻断；与
  ct_registry.py 交互路径既有 Keyword-System Confirmation Gate 互不重复
  （该路径 Manifest per_source.cde 已强制确认）。

**验证**：py_compile 全过；本地化 7 用例离线全过（osimertinib→奥希替尼、
多词混合、fail-open）；实站 A/B（本地 headless）appliers/drugs_name/中文
keyword 全部命中。待 Coze 部署后线上复测（重点：英文药名 empty 率应大幅下降）。

## 0.5.01 · 2026-11-09 · brief 速览性能优化（端点 + 本地）

**背景**：线上稳态 literature brief ~18s、registry brief ~22–26s，波动 7–62s，
曾贴近 Coze 网关 60s 硬顶（ct-base §20.17）。诊断确认瓶颈是 WHO 普通 keyword
路径必启 Playwright 与 literature 两源串行，不是 brief 聚合逻辑。

- **端点 `advisor_brief_nodes.py`**：① 两源 `ThreadPoolExecutor` 并发（每个任务独立
  `contextvars.copy_context()`，保证 `runtime.context` 跨线程可读）；② registry 子 state
  设 `who_condition`（与 keyword 同值）+ `max_pages=1`，命中 `who_search_node` 既有
  `_try_http_fast_path` 纯 HTTP 路径，不启浏览器；`WHO_FAST_PATH_ENABLED=False` 可整体回退；
  ③ 单轮软预算按 source 分档 18/15/12s，超时只标 `partial_sources`、保留已完成源，
  绝不伪装 0 命中（线程不强杀、池有界 `max_workers=4`，属软预算）；④ `max_results`
  由固定 `max(cap*2,30)` 改 `max(cap,10)`。
- **本地 `ct-advisor`**：契约新增 `endpoint.per_source_timeout_sec`（20/35/40s）替代统一
  90s；新增 `cache` 段（TTL 600s，系统临时目录，仅缓存 `status=ok` 且
  `partial_sources` 为空，`CT_ADVISOR_BRIEF_CACHE=0` 可关闭）。
- 🔴 **护栏 1 未破**：所有裁剪在节点内部固定，白名单仍锁死 8/6/6、零新增入参；
  `disclaimer` / `suggest_footer` 文案逐字未动。响应 `brief` 内新增 `perf` 诊断字段
  （`mode` / `deadline_sec` / `elapsed_sec`）供部署后 canary A/B。
- **验证**：离线 dry-run 18/18（并发 0.30s、contextvars 继承、超时标 partial、
  三 brief 端到端、护栏常量未漂移）、`test_cloud_brief` 全过、`selfcheck` 44/44、
  `cloud_brief --self-test` 26/26；真实链路缓存关闭 8.01s → 端点缓存 0.31s →
  本地缓存 0.01s，结果逐字一致。
- ⚠ 收益需在**新包部署后**用 `canary_cloud_brief.py --only perf` 线上 A/B 确认；
  若 `partial_sources` 偏高，调 `BRIEF_DEADLINE_SEC` 后重发包即可。

## 0.5.00 · 2026-11-09 · coze 端点：ct-advisor 速览聚合三 source 上移

> 这是**端点版本**（`adapters/coze/src/graphs/nodes/_version.py::COZE_VERSION`），
> 与技能版本 0.14.5 正交。完整计划与部署清单见
> `ct-advisor/docs/cloud_brief_rollout_20261109.md`。

- 新增 `advisor_registry_brief` / `advisor_safety_brief` / `advisor_literature_brief`
  三个 source（`src/graphs/nodes/advisor_brief_nodes.py`），**进程内复用**既有
  who / chinadrugtrials / faers / openalex / europepmc 节点取数，零重复实现；
  纯 stdlib 聚合，只回结构化 JSON 速览，不产 XLSX/HTML。
- 三条护栏：参数白名单锁死 8/6/6 键（未知键 fail-closed）· 响应强制
  `disclaimer`（速览、非审计级）· 强制 `suggest_skill` / `suggest_text` 导流回三个技能。
  契约单一真相源 = `ct-advisor/config/brief_contract.json`。
- `sources.py` 白名单 + `search_node.py` 懒加载分支同步登记
  （`scripts/selfcheck.py` A1/A2 44/44 通过）；契约索引新增 3 条并由
  `gen_contract_doc.py` 重生成 `adapters/coze/coze_contract.md`（禁手改）。
- 顺带收敛契约索引 `coze_version`(0.4.00) 与 `_version.py`(0.4.02) 的版本漂移 → 0.5.00。
- 决策依据：ct-base §20.19.5 范畴说明「检索族端点内 source 级上移 ≠ 跨族后端合并」；
  ct-advisor 本地 need_tool 执行卡保留作降级兜底（§20.19.7 红线 2）。
- 🔴 需重新打包发布 Coze 云端工作流后才生效；未部署时客户端自动回落，行为不变。

## 0.14.5 — 2026-11-08 · 工作台能力对齐（workbench only，功能层不变）

> 依据同日《ct-registry 工作台改进分析》。本次只改工作台、文档与检查工具，
> 不改检索引擎行为。备份：`workbench/_bak_20261108/`。

### 防复发 · 2026-11-08 横向补齐（同日 ct-safety 审计后追加）
- `capability_parity.py` 新增**第 5 条「架构 ↔ 文案事实一致性」**：`FACT_CLAIMS` 断言表 +
  `FACT_CROSS_CHECKS` 交叉断言，覆盖本技能上一轮修过的事实（`publish-dist` 不得复活 /
  部署事实源必须存在且写明载荷目录 / 「下一迭代接入」期货文案不得回潮 / `/api/diff`
  必须复用 `diff_snapshots`）。动因：ct-safety 审计发现「UI 陈述与 SKILL.md 架构事实
  矛盾」这类问题，纯参数检查抓不到。ct-literature / ct-safety 同轮补齐该条。

### P0 · 版本与发布链路
- **五处版本锚点统一 `0.14.5`**：`SKILL.md` front-matter 0.14.2→0.14.5、正文 `v0.14.4`→`v0.14.5`、`workbench.config.json` 0.1.1→0.14.5、`app.config.json` 补 version。此前 `/api/config` 直读 `workbench.config.json`，**线上页脚显示 `v0.1.1`**。
- **发布路径订正**：SKILL.md 的 `publishDir` / Payload / 重发布步骤由不存在的 `workbench/publish-dist` 全部改为 `workbench/publish`（与 `build_publish.py:38` DST、`app.config.json` 一致）；删掉写死的「Last republished 2026-09-26」，改指向新建的 `references/published_app.md`（部署单一事实源：registry / 版本锚点 / 重发布协议 / 待部署欠账 / 部署后冒烟清单）。
- `build_publish.py` 新增 `_bak*` 目录段通用排除，防本地备份源码快照被打进载荷。

### P1 · 已知功能缺口
- **快照差异比对落地**：新增 `POST /api/diff`，只接受 run id（形状白名单 + 路径规范化校验），复用 `scripts/track_diff.diff_snapshots`——与 CLI `--diff` **同源**，纯本地零联网。前端「数据源」页新增两次运行选择 + `status_delta` 渲染（新增 / 移除 / 状态 / 拼写同义 / 分期 / 申办方 / 适应症变更）。撤掉 `snapTip` 的「将在下一迭代接入」期货文案，README 待办第 1 条销账。
- **数据源清单与源健康**：新增 `GET /api/sources`，返回 9 源（Tier / 接入方式）+ 最近一次 `run_status.json` 的真实状态（WHO 降级、CDE 0 命中未确认、自动重试次数）；「数据源与追踪」页由 3 段静态文字改为动态清单 + 健康列表 + diff 面板。
- **出站披露**：检索表单下方说明 Tier-2 源经第三方统一端点、仅发送公开检索词与非内容元数据（机器哈希 / 技能版本 / 入口 / 语言 / 需求 id），不发送本地文件或保密数据（中英双键）。
- **清理历史死代码**：0.14.4 移除「命令行对外展示」后遗留的 3 处 `wb-adv-cmd` null-safe 引用（能力对齐检查检出为幽灵 id），已删除。

### P2 · 防复发
- 新增 `workbench/capability_parity.py`（移植自 ct-literature，适配 `I18N` 字典、`wb-f-*` 控件、`ADV_SPECS` + `_build_cmd`、无 v 前缀版本号）：版本锚点 / i18n parity / DOM 引用闭环 / CLI flag 三选一。6 个未接线 flag 逐条写明 `deprecated` / `internal` / `cli-only` / `api-wired` 分类与理由。
- 接入 `ctqa.config.json` 的 W0 `skill_tests`；`workbench/README.md` 新增「发布前检查（必跑）」。

### 验证
- `capability_parity.py` → **PASS（0 fail / 0 warn）**：版本 0.14.5 一致；i18n 296/296；DOM 147 定义 / 50 引用 / 7 控件、0 幽灵；66 个 CLI flag = 60 已接线 / 6 明确豁免 / **0 未判定**。
- `py_compile`、内联 JS `node --check`（2 blocks / 105111 chars）、ctqa 配置 JSON 解析全通过。
- 函数级：`_api_sources()` 返回 9 源 + 最近运行 3 个状态键；`_api_diff()` 返回完整 status_delta（52 条）且路径穿越被拒（`invalid_run_id`）。
- HTTP 冒烟：`/api/config` → 0.14.5；`/api/sources` → 9 源 + latest；`POST /api/diff` → 200 / ok / status_delta 52 条。
- ⚠️ **线上覆盖部署未执行**（外部发布动作，需单独确认）；发布包已重建，协议见 `references/published_app.md`。

---

## 0.14.5 — 2026-11-06 · 阶段 2 接入 ct-base Excel 交付契约 + 英文交付物零中文

> 关联 ct-base v1.4.45：流程契约层统一，消除本技能内的第二份语言解析实现。

- `scripts/export_xlsx.py` 删除本地 `resolve_report_lang()`，改为 `from xlsx_delivery import resolve_report_lang`（`skill="registry"`）；共享件由 `publish_inject` 注入，已物理复制到 `scripts/` 与 `workbench/publish/scripts/`。
- **英文模式中文残留修复**：封面标题在 `lang=en` 时只保留英文检索词片段（`Orebatinib / 奥雷巴替尼` → `Orebatinib`），避免 A2 / B10 出现中文；明细表中文数据值按数据保真红线保留。
- `workbench/server.py::_write_partial_xlsx` 表头与 sheet 名按界面语言切换（zh「部分结果」/ en「Partial Results」），英文界面不再输出中文兜底报告；调用处按 `params.lang` 传参。
- 验证：独立进程 zh/en 两版逐格扫描，英文版 CJK 单元格 0、中文版四表全中文；`--lang en` / `CT_REGISTRY_LANG=en` 均英文、无 env 的 `auto` 中文；发布包脚本自包含运行通过；`py_compile`、F31 通过。
- ⚠️ 线上应用仍待重新部署后页面下载才生效。

---

## （端点版本补录）2026-11-04 · coze 端点 0.3.95–0.4.00 历史欠账 + B 类三项上移

> 端点侧版本线（`src/graphs/nodes/_version.py::COZE_VERSION`）与技能版本线（下方 `0.14.x`）是两套独立编号。此前 0.3.95–0.3.99 五次端点改动只写进了 `_version.py` docstring，未进本 CHANGELOG，构成 ct-base §20.19.7 红线 3 的历史欠账，本次一并补齐（摘要真源 = 该文件 docstring）。

### coze 端点 0.3.95 — 2026-10-27 · ct-literature 源码保护上移三策略节点
- 新增 `lit_route`（PDF 下载路由红线）/ `lit_preprint_check`（预印本作者级同篇校验）/ `lit_dedup`（去重归一化 + PRISMA 组装，engine v1/v2）三节点；`sources.py` 登记 + `search_node.py` 懒加载分支，老客户端不传这些 source 时走默认分支，完全向后兼容。
- 本地 ct-literature 同步改为纯薄客户端 `adapters/_coze_strategy.py`：coze 不可用时降级为空、**不本地兜底**（源码保护型口径，与 0.4.00 红线 2 保留本地引擎不同）。

### coze 端点 0.3.96 — 2026-10-27 · PDF 解析顺序与质量对齐本地
- `publisher_pdf_batch_node._oa_via_openalex` 由「PMC→EPMC render 优先」改为与本地 `pdf_download._oa_via_openalex` 逐字对齐的「best_oa/pdf_url 真直链优先、EPMC ?pdf=render 降为最后兜底」；新增 `_is_aux_pdf` 过滤（排除 `_reference.pdf` 参考文献列表被误当全文）。
- `_do_scrape` / `_do_scrape_oa_url` 的「先探测 EPMC render」下移为最后兜底，减少每篇 1–4 秒无效探测。所有候选仍经 `_probe_direct_download` 验证后才返回，零行为回归。

### coze 端点 0.3.97 — 2026-11-04 · pubmed 车道 + 引文核验节点（P0-A/P0-B）
- `literature_nodes.py` 新增 `pubmed_node`（NCBI E-utilities，含 strict_keyword 二次检索、hit_count/strict_hit_count 双口径 + provenance 溯源），增强 `europepmc_node`（lit_strict / strict_keyword / query 回显；`total_count` 保持「取回数」语义不变）。
- 新增 `citation_verify_node`：合并 ct-literature `verify_citations.py` 与 meta-analysis `ref_verify` 两侧能力——DOI/PMID/OpenAlex/CrossRef 四路元数据 + 标题作者一致性 + 三通道撤稿检测，8 项 status 枚举。
- `state.py` 三模型同声明新增字段；节点均为纯执行器，检索式构造仍留本地。本包仅含服务端节点，客户端 S4 接线属后续步骤。

### coze 端点 0.3.98 — 2026-11-04 · 引文核验作者比对误判修复
- `citation_verify_node.py::_author_ok` 旧实现把元数据姓氏整体与 work 侧单 token 做 SequenceMatcher，长串被稀释到阈值以下 → 第一作者一致却被误判 mismatch（CheckMate 057 title_ratio=0.949 仍被否）。改为姓氏 token 级双向比对 + 灰区返回 `None`，保留纯姓氏明显矛盾 → `False` 的反幻觉能力；团体署名不作姓氏信号。`selfcheck_citation_verify.py` 增 Q10 回归。
- 纯服务端逻辑修复，对外契约不变；**本版从未单独打包**。

### coze 端点 0.3.99 — 2026-11-04 · 预印本同篇校验姓氏解析修复 + 部署包
- `lit_preprint_check_node.py::_surnames` 旧实现 `parts[0] if "," in a else parts[-1]` 对 `"Borghaei H"` / `"Paz-Ares L"` 取到 initial；原文与候选著录格式不同时姓氏集合无交集，真实预印本候选被全部丢弃。现与 ct-literature `preprint_fallback._surnames_from_name` 同源对齐：逗号前取姓、丢弃单字母 initials、NFKD 折叠变音、去标点保留中文。`selfcheck_citation_verify.py` 增 Q11 回归（8 例 _surnames + 2 例 _author_check）。
- ⚠️ 0.3.98 从未单独打包，故 0.3.98 + 0.3.99 两批修复**合并为同一个 0.3.99 部署包**交付（66 files / ZIP_OK / 逐文件 MD5 一致）。用户确认上传部署后，线上 `lit_preprint_check` canary 实测 `passed=true, reason=ok`，无关作者反例仍拒绝。ct-literature 侧同类本地修复单独完成，不纳入本包。

### coze 端点 0.4.00 — 2026-11-04 · B 类三项上移（本条）
- 新增 3 个独立 source：`lit_rrf`（RRF 跨源排名融合，纯计算；weights 由客户端显式传，云端刻意不持有 `SOURCE_REGISTRY`；修掉本地 `build_source_ranks` 原地 pop 副作用）、`lit_prisma`（整体上移 `screen_prisma.screen()` + `doc_type_filter.classify_record` 规则表，由专项自检断言 8 张表逐字一致）、`prospero`（只做 `raw_query` 旁路执行器，检索式构造严格留本地；POST 公开检索 + 自造 auth-token + 错误信封识别，后端失败 fail-closed 不伪装 0 命中）。
- 三者复用既有 `keyword` JSON 通道，`state.py` 三模型零改动；`sources.py` 登记 3 源，`search_node.py` 增 3 条懒加载分支，`selfcheck.py` A1/A2 强制集合 ⇄ 分支一致。
- 🔴 按 ct-base §20.19.7 红线 2，本地 ct-literature 三份引擎**原样保留**作静默降级兜底：新增 `adapters/_coze_lit_pipeline.py` 编排层（coze 优先 + 本地末位兜底，本地引擎以 `local_fn` 回调注入），`ct_literature.py` 三处调用点接线；`--offline` 老版本分支不接 coze，保持 100% 向后兼容。
- 严格红线 3 四项同步：端点内新建**检索族适配版契约索引** `tests/coze_cases/_contract_index.json` + `gen_contract_doc.py` → 生成 `adapters/coze/coze_contract.md`（禁手改，24 项校验 + 幂等复跑通过）；版本归因 `_version.py` + `AGENTS.md`；本 CHANGELOG 补五版欠账；F31 双视图同步本次新增条目（既存漂移另立任务）；§20.19.5 实例表新增范畴说明行。
- ⚠️ PROSPERO 外网可达性部署前未证实：部署后须单独 canary 验响应体，不通则由本地引擎兜底，不拖累另两项纯计算节点。**本版仅本地打包，未上传 / 未部署 / 未 commit / 未 push。**

---

## 0.14.4 — 2026-11-06 · 结果文件（Excel / Markdown）中文化 + 工作台兜底报告排版修复

> 用户反馈：工作台页面下载的 `report.xlsx`「格式是乱的，而且基本上都是英文，没有中文」；同时要求核查上下文提示词（对话式 CLI）链路是否同病，并一并修复。

### 根因
- **全英文**：`export_xlsx.py` 的 `--lang auto` 直接落 `i18n._current_lang()` → OS locale。线上工作台跑在 en_US 容器里，四张 sheet 名（README / Search Results Summary / Trial Master Table / Raw Details）、表头、KPI 卡片与图表标题全部渲染成英文；本地中文 Windows 复现为正常中文，故问题只在云端出现。抽查线上 `?task=20261104-165648-83c2`（慢阻肺，278 条）确认四表全英文。
- **格式乱**：① 英文文案普遍长于中文，KPI 卡片 / 字段字典 / 图表标题按中文版式排布后被撑挤；② 超时兜底 `report_partial.xlsx` 是手写的极简 OOXML——表头中英混排（`Phase`）、sheet 名 `Partial`、无冻结 / 筛选 / 表头样式，且 `countries` / `sponsor` 为列表时直接 `str(list)`，单元格出现 `['United States', 'China']` 这类 Python repr。
- **上下文提示词方式**：对话式 CLI 在本地中文 OS 下产出的 `report.xlsx` 本身是中文（已核验 `out/report.xlsx`），但共用同一个 `--lang auto` 隐患——换到无中文 locale 的沙箱 / 英文系统即退化为英文；`report.md` 章节标题为中英混排。已一并修复。

### 修复
- **`scripts/export_xlsx.py`**：新增 `resolve_report_lang()`——显式 `--lang` > `CT_REGISTRY_LANG`（工作台注入当前 UI 语言）> 技能根 `config.json language` > 封面标题中文检测 > OS locale > 默认中文；`build()` 始终 `set_lang(...)`。工作台与对话式 CLI 两条链路共用，英文用户仍可显式 `--lang en`。
- **`workbench/index.html` + `workbench/server.py`**：检索表单随请求下发 `lang`（当前界面语言），后端子进程注入 `CT_REGISTRY_LANG`；页面切 EN 时报告同步切 EN，切 ZH 恒为中文，不再受云容器 locale 影响。
- **`workbench/server.py::_write_partial_xlsx`**：全中文表头 + 中文 sheet 名「部分结果」、`_partial_text()` 规范化列表值、深蓝表头白字 + 斑马纹 + 冻结首行 + 自动筛选 + 列宽行高，与正式报告同一观感。
- **`scripts/i18n_skill_messages.json`（新增）**：修正 `xlsx.field.primary_outcome_desc` 的 zh 仍是英文 `Primary Outcome(s)` 的漏译（技能私有词表的正确去处，不改 ct-base 共享件）。
- **`scripts/report.py`**：Markdown 报告章节标题按 `CT_REGISTRY_LANG` / `--lang` 输出中文（默认）或英文，不再中英混排；数据值保持注册库原文，符合数据保真红线。

### 验证
- 模拟 en_US locale：语言优先级 8 组用例全通过；线上同款 50 条数据经**发布包脚本**重导出 → sheet 名「说明 / 检索结果概要 / 试验总表 / 原始明细」、表头「登记号 / 标题 / …」、8 张原生图表完整。
- 显式 `--lang en` 仍输出英文；兜底 xlsx 经 openpyxl 验证中文表头、冻结 `A2`、筛选 `A1:G3`、深蓝表头、列表值 `United States; China`。
- `py_compile` 全通过；两份内联 JS 改动所在脚本块 `node --check` 通过；主目录与 `workbench/publish/` 发布副本逐文件 MD5 一致（含新增词表）。
- ⚠️ 线上应用需按 §13.5 Scheme B 用既有 appId 重新发布后生效；本次仅完成代码与发布包修复，未执行部署。

---

## 0.14.3 — 2026-11-03 · `search_ctgov` 补 429/5xx 退避重试（P3 归一反向移植）

> 动机：meta-analysis 的 `registry_probe.py` 与本技能的 `search_ctgov.py` 是同一个源
> （ClinicalTrials.gov v2 REST）的两套实现。按 ct-base §20.19「coze 后端合并判定框架」
> 的消除重复原则，meta 侧的检索**执行**层已归一到本模块（P3，2026-11-03）。
> 本模块原本只有一次生 urlopen（无重试），而 meta 侧的 `_get_json` 具备 429/5xx 退避
> 重试——直接归一会让该能力静默丢失，违反「融合不丢弃有用功能」，故先反向移植。

### Added
- **`_fetch_page_urllib(params, timeout=30, max_retries=3, backoff=2.0)`**：urllib 默认路径
  新增重试（429 尊重 `Retry-After` 头、5xx / URLError / OSError / TimeoutError 指数退避、
  非 429 的 4xx 不重试、重试耗尽抛 `RuntimeError`）。默认值保持既有行为不变。
- **`_fetch_page_session(session, params, max_retries=3, backoff=2.0)`**：`--fast` 路径
  同策略重试（requests 异常按 `response.status_code` 判定可重试性）。
- **`search()` / `search_fast()` 透传**：新增 `timeout` / `max_retries` / `backoff` 三个可选
  参数（默认 30 / 3 / 2.0），调用方按需覆盖。
- **`_wait_seconds(backoff, attempt)`**：指数退避计算；`backoff<=0` 显式返回 0.0——
  Python 中 `0 ** 0 == 1`，不显式守卫会让 `backoff=0` 变成「等 1 秒」而非「立即重试」。
- **测试**：`tests/test_search_ctgov_retry.py` **13/13**（零网络；覆盖 429 无/有 Retry-After、
  5xx 重试、重试耗尽、非 429 的 4xx 不重试、URLError 重试、`backoff=0` 不 sleep、
  `search`/`search_fast` 参数透传、检索式构造不受影响）。

### 兼容性
- 完全向后兼容（ct-base §20.11）：三个参数均为 optional 且默认值等价于原行为
  （单次请求 = `max_retries=1` 的退化，但默认 `max_retries=3` 让瞬时 5xx 现在能自愈，
  属**行为增强**而非破坏）；`search()` / `search_fast()` 的返回结构未变。

## 0.14.2 — 2026-10-28 · ct-qa 接入补齐（W2I/P3 激活）+ 2 项 P1 i18n 残留修复

### Fixed（P1 · 英文界面中文残留，由新启用的 W2I 层检出）
- **`#wb-lang` 语言按钮 `title` / `aria-label` 硬编码中文「切换语言」**：切到 EN 后
  悬停提示与无障碍标签仍是中文。改为 `data-i18n-title="langSwitch"` +
  `data-i18n-aria="langSwitch"`，并在 zh/en 双字典补 `langSwitch` 键（与 `ctHome` 同机制）。
- **页脚 ICP 备案号 `沪ICP备06008575号` 被误判为需翻译**：工信部备案号是法定公示原文，
  任何语言下均须原样展示。给 `<a class="wb-beian">` 加
  `data-ctqa-allow="icp-beian: …"` 豁免标记（框架侧支持 `[data-ctqa-allow]` 子树豁免）。

### Added（ct-qa 配置补齐，§27.6 强制项）
- **`layers.enable` 补 `W2I` 与 `P3`**：原仅 `W0/W1/W2B`。`W2I` 是 §27.6 条 2 要求
  「必须配置声明」的推荐层（缺失＝英文界面零覆盖，上面 2 项 P1 因此长期不可见）；
  本技能有 `adapters/coze/` 与出站客户端 `extsvc_client.py`，按条 3 属「有出站管线」，
  必须配 `prompt` 节并启用 `P3`。
- **新增 `adapters/ctqa_p3_wrapper.py`**（§27.6 条 6 wrapper 模式）：出站构造是
  `search_ictrp.build_payload(args)`（吃 argparse Namespace，缺属性即 AttributeError），
  P3 需要 `build_payload(env: dict)`。wrapper 提供「全量默认属性 Namespace（34 个
  `args.*` 属性）+ env 覆盖 + 深拷贝保护」；`sanitize` 复用出站真实实现
  `extsvc_client._sanitize_payload`（手机号 / 身份证 / 邮箱三类打码）。
- **`ctqa.config.json` 补 `prompt` 节**（原为 `"prompt": {}` 空对象）：`build_payload` /
  `sample_env` / `sanitize` / `sanitize_mode: redact` / `volatile_keys`。

### 验证
- `python -m ctqa run --skill <ct-registry>`：**PASS 60 / FAIL 0 / WARN 3 / ERROR 0 → 绿灯**。
  P3 首次激活即 7/7 PASS；W2I 由 FAIL 2 转 PASS 5。
- 剩余 WARN：`W0-010` 内联 `<style>`（设计允许，tokens.css 已外链）、`W1-005` 事件协议
  启发式告警、`W2B-018` 资源级 404（静态服务无后端 `/api/*`，环境噪音）。

## 0.14.1 — 2026-10-26 · §22.24 AI-as-intervention 双轨治理

- **§22.24 P1·l AI-as-intervention 双轨治理框架**（SKILL.md §9）：前瞻性评估+SPIRIT-AI/CONSORT-AI vs 工作流准确性+TRIPOD-AI/ICH E6(R3)（EClinicalMedicine 2026-10）。
- **版本同步**：SKILL.md `version: 0.14.0` → `0.14.1`。

## （待部署）2026-10-23 · CT.gov v2 `statusModule` 归一化崩溃修复 + 工作台「检索计划」卡片（站点 × 关键词组）

> 工作台 Web UI 位于 `workbench/`，按 §16.12 整目录排除在发布包外（仅本地保留）——下述「工作台」条目不进入任何发布包；真正影响发布包的是 `scripts/normalize.py` 的归一化修复。

### 进发布包

- **`scripts/kw_localize.py` en→zh 短规则整词匹配（修复伪译名标「已验证」）**：短语替换循环此前按子串替换，两类误伤——①类别后缀规则（`'nib'→'替尼'`、`'mab'→'单抗'`）把未收录新药名 `Orebatinib` 切成 `Orebati替尼` 且标 `term_map`「术语表已验证」（比机器翻译误译更有害，用户会直接采用）；②缩写规则（`'os'→OS 总体生存`、`'as'→AS 强直性脊柱炎`）命中普通单词内部（`class→cl+AS+s`、`osimertinib` 前缀）。现全部规则整词匹配（两侧非字母），多词短语与连字符场景（`osimertinib-based`）不受影响。实测 12 组用例全过。
- **`scripts/ct_registry.py` WHO 自由词分支复用已注入英译（批量翻译一次）**：`_build_who_payload` 调用处的自由词分支原为 `search_kw = intr/cond or ictrp_kw`——上游 gate/`--ictrp-keyword` 已注入英译时，仍被中文原文覆盖 → WHO 适配器内部对中文原文再做一次在线翻译（用户反馈「自动翻译应该是批量执行一次就可以了，没必要每个单独做」）。现当 `ictrp_kw` 为英文且原始词为中文时优先复用 `ictrp_kw`；配合工作台的 `--kw-en/--kw-zh` 批量注入，全链路翻译恰为一次。实测 `奥雷巴替尼`（CT.gov+WHO+CDE+ChiCTR）：`KW-LOCALIZE` 2+ → **0**，`[ct_registry][KW] 直接注入覆盖` 一次完成全部站点注入。
- **`scripts/normalize.py` 兼容 CT.gov v2 `statusModule` 新结构**：`lastKnownStatus` 现返回**字符串枚举**（如 `"RECRUITING"`），旧代码按 dict 解包（`(sm.get("lastKnownStatus") or {}).get("date")`）→ `AttributeError`，导致整批归一化崩溃、`state=error`、无清单/无 xlsx/无 Landscape。实测 `osimertinib`：CT.gov 取回 298 命中/50 条，样本中 7 条带该字段（14%），默认 50 条/库几乎必然触发。修复：字符串枚举按值取用、`last_update_posted` 改用真实字段 `lastUpdatePostDateStruct`（旧名 `lastUpdatePosted` 在 v2 中不存在 → 更新日期恒 null、`stale_check` 失效）。
- **`scripts/usage_guard.py` WHO/CDE 共享端点每日配额 100 → 1000**：`DAILY_LIMIT` 由 100 调整为 1000（用户 2026-10-23 明确）。同步更新 `QUOTA_NOTE`、`ct_registry.py` POLICY 提示（`每日上限 100 次`→`1000 次`）、`i18n.py` xlsx 配额说明（`10`→`1000`），以及 AGENTS.md / README.md / README_zh-CN.md / cli_reference.md / search_menu.md / search_procedure.md 文档中的配额数字。已用计数 `config/usage.json` 不重置（仅调上限，配额护栏仍生效，剩余量随上限提升自动放开）。
- **`adapters/coze/src/graphs/nodes/drks_search_node.py` 适配 BfArM 新站（DRKS 恢复直连）**：DRKS 官方站点已从旧站 `drks.de/drks_web/navigate.do`（HTTP 307 → www.bfarm.de）迁移至 Jakarta Faces 新站 `/search/de`，原节点 2026-09-08 起预检命中即短路返回「站点已迁移」，DRKS 源实际不可用（仅剩 WHO 镜像兜底）。本次重写抓取流程：① 新站选择器常量集中管理（搜索框 `searchForm:j_idt76`、每页条数 `resultForm:sorting:rowsPerPage`、翻页钮 `resultForm:paginationTop:j_idt154`、结果行 `li.row[role="row"]`）；② 提交路径改为**填词 + Enter**（提交钮 `j_idt74` 无头环境点击稳定性差，实测超时；Enter 触发 POST → 302 → GET `/search/de/results` 稳定可靠）；③ 每页条数拉满 100（选项 10/20/30/50/100），翻页上限钳制 10 页；④ `_parse_results` 重写为新行结构解析（DRKS-ID / Titel / Registrierungsdatum / Letzte Aktualisierung / Status，日期只取 `DD.MM.YYYY` 防提示文本混入），输出 schema 中文键与旧版逐字一致（下游 normalize/aggregate 零改动）；⑤ 预检改为探测新站可达性，仅在新站也完全不可达时才短路返回 WHO 兜底指引。本地端到端实测（Playwright + Chromium，mock 云端依赖 import 真实节点）：`cancer` 2 页取回 **200 条真实记录**（字段/URL/schema 全对），25.8s；0 条场景有诊断输出。**部署需重新打包 adapters/coze zip + MD5 上传 Coze（手动，待授权）**；未重新部署前云端仍跑旧版节点（预检短路 + WHO 兜底），工作台提示文案已同步说明此区别。

### 仅工作台（不进发布包）

- **顶栏按钮对齐 ct-base §5.2 新基线 34px**（用户追问「ct-registry 页面右上角按钮的高度没有调整？」）：20:44 修订规范时明确「不追溯已发布页面」，registry 暂维持 40px；本次按新基线落地——`.wb-topbar .wb-btn` 与 `.wb-topbar .wb-lang` 覆盖为 `min-height:34px; padding:6px 11px`（只覆盖顶栏专属选择器，内容区全局 `.wb-btn` 保持 40px 实测不变；窄屏 ≤768px ≥44px 纪律在 media query 内不受影响）。实测（Playwright）：#wb-lang/#wb-bug/#wb-cthome 高 34px、pad 6px 11px、字 14px；#wb-backend pill 33px 不动；顶栏 68px，占比 59%→50%；内容区主按钮 40px；console 零错误。至此 registry 与 literature 顶栏控件尺寸一致。

- **页脚居中（用户指示）**：`#wb-footer` 由 `justify-content:space-between`（主信息居左、ICP 居右）改为 `center` 整行居中；ICP 备案号并入主信息同一行流（`名称 v版本 · 框架说明 · 沪ICP备…`），保持 §5.2 文字格式不变。实测主信息中心与页脚中心偏差 <2px。
- **两页字号对比取证：ct-registry 合规、ct-literature 越档**（用户反馈「literature 页面字体明显更大，查哪个不符合规范」）：无头浏览器实测两页关键元素计算字号——body 15/15、h1 16/16、navitem 14/14、btn 14/14 完全一致；差异根因是 ct-literature `app.css` 的 `.panel h3`（区块/面板标题）用了 `--wb-fs-lg`(16px)，违反 §4.5.1「区块/卡片标题 = sm(14px)」（lg 仅限顶栏主标题）。**已修复 ct-literature `app.css`：`.panel h3` lg→sm**（实测 14px）。ct-registry 侧无需调整（其 92 处全部走令牌且选档合规；卡下说明 2xs 为非交互辅助，合规）。

- **对照 ct-base 规范全文逐条复核并修复 7 处不合规**（用户指出页脚 ICP 不合规，要求彻底对规范）：① **页脚文字（§5.2）**——原仅有 ICP 备案链接，现为规范格式「ct-registry 工作台 v0.1.1 · 基于ct系列技能统一框架构建」（`wbRenderFooter()` 动态拼接，随语言切换，en: built on the ct-series unified framework；ICP 备案作为法律要素保留、右置次级展示）；② **logo 边框化（§5.6.3-4）**——顶栏 logo 包进 `.wb-logo-box`（40×40 白框圆角阴影 + 内承 34×34 自有 icon）；③ **聚焦光环（§5.6.3-5）**——4 处 focus 规则由单纯 border-color 补 `box-shadow:0 0 0 3px var(--wb-brand-soft)`；④ **视图切换淡入（§5.6.3-6）**——补 `@keyframes wbFade` 并应用于 `.wb-view.active`；⑤ **反馈图标（§5.2）**——`#wb-bug` 内 SVG 换为规范对话气泡 path（`M4 4h16v12H7l-3 3V4Z` + `M8 9h8M8 13h5`）；⑥ **gzip + 缓存（§7.2 强制）**——`server.py _send()` 重写：文本类 >1KB 且客户端支持时 gzip（`Content-Encoding`），压缩缓存仅按 `(路径,mtime)` 键（动态 JSON 现压现发禁入缓存，防串号）；静态 `max-age=86400` / HTML `max-age=60` / 动态 `no-store`；⑦ **发布元数据（§13.1）**——`app.config.json` 补全必填字段（appName/domainPrefix=ct-registry/shareLink=https://ct-registry.app.workbuddy.host//startCmd）。实测：HTML gzip 后 48KB、css gzip + 86400、api no-store 且 config/health 首字段无串号；页脚 zh/en 切换正确；logo-box 40×40 内 34×34；console 零错误。

- **字号对照 ct-base §4.5 复核并修正 3 处交互元素低于范本基线**（用户要求复核）：六档令牌（24/21/16/15/14/13/11）与权威值一致、body 走 base、全部 92 处组件 font-size 走令牌、3 处 16px 均在 media query 内且带「防 iOS 聚焦自动放大」功能性注释（规范允许的标注特例）——主体合规。修正：① `.wb-btn` xs(13)→sm(14)（规范范本「主交互文字=sm」）；② `.wb-lang` xs→sm（按钮族一致）；③ `.wb-subhead h3`（景观总览/试验清单区块标题）xs→sm（规范「区块/卡片标题=sm」）。实测 computed：btn/lang/navitem=14px、body=15px、零 console 错误。
- **注册库选择区改为「卡片 + 卡下无框说明」两行结构（`workbench/index.html`，用户反馈迭代）：第一版误做成整张带行线的表格（用户：「这表格也太难看了吧」），用户原意为每库一个卡片、卡下方挂一行无框文字。现结构：`.wb-src-grid` 恢复 `repeat(auto-fill, minmax(160px,1fr))` 多列网格，每库一个 `.wb-src-cell`（flex column）——上行 `.wb-src` 保持原 chip 外观（边框/圆角/可点击/选中高亮/CT.gov 锁定图标），下行 `.wb-src-note` 为无框文字（2xs 次要色，WHO 行 warn 琥珀色）。注释内容中英双语 9 库：归属地/机构 + 性质（CT.gov=美国 NIH Tier-1 恒开；WHO=世卫 ICTRP 聚合 14 源 Tier-2 共享端点+慢源警告；CDE=国家药监局登记平台；ChiCTR=华西医院；EU-CTR/CTIS=欧盟；ISRCTN=英国；DRKS=德国 BfArM 新站；PubChem=化合物富化非注册库）。原独立脚注 `#wb-src-foot` 与 `srcWhoNote` i18n 键删除。实测（Playwright）：零 console/pageerror；取消勾选 class 联动正常；title 悬浮提示为注释全文；zh/en 切换注释完整跟随。
- **修复「成功完成但景观指标全显 `-`（用户误报『报告 0 个结果』）」**（`workbench/server.py`，用户实测反馈 19:16 任务：清单 1 条、指标三项全 `-`）：根因是 `_LogScrubber` 把 CLI 末尾的 `{"tool": "ct-registry", ...}` 汇总 JSON 行转换成人话 `[汇总] 检出 N 条…` 文本行（本机路径不进日志的既定策略），于是 `_last_summary()` 在日志里再也找不到 JSON → `summary=None` → 前端 `raw_total/n_trials/cross_source_groups` 全显 `-`。而检索其实成功了（`normalize 1 records`、`agg deduped=1`、`report.xlsx` 65KB 已生成）。修复双通道：① 新增 `_summary_from_agg(out_dir)`——server 以 `--keep-meta` 启动 CLI，`agg.json`/`agg_full.json` 必然保留，直接读盘重建与 CLI `_print_summary` **同构**的 landscape 摘要（含 `cross_source_groups` 真实值，不再像超时分支那样诚实返回 None）；`_run_task` rc==0 分支改为 `_last_summary(txt) or _summary_from_agg(out_dir)`；② 新增 `_done_view_from_disk()`——`_task_view` 此前对 TASKS 缺失（server 重启/崩溃恢复）一律返回 `unknown`，刷新页面即丢结果；现回查 `runs/<id>/meta.json`，state=done 时从磁盘重建完整 view（summary/rows/report_md/excelUrl/failedSources 全量）；③ 抽 `_rows_from_out()` 统一 `_run_task` 与磁盘恢复两条路径的清单读取（min-year 的 `normalized_filtered.json` 优先）。实测：19:16 历史任务重启恢复 → `state=done, raw_total=1 n_trials=1 cross=0, rowsTotal=1 (NCT06578546)`；新发 Orebatinib 仅 CT.gov 检索 → `raw_total=50 n_trials=50`、50 条 NCT 行、phase_mix/region_mix/top_sponsors 齐全、xlsx 可下载。
- **失败源提示区分「站点永久变更」与「端点临时故障」**：`_parse_failed_sources`（纯子进程日志文本匹配）抓不到源级诊断——DRKS 站点迁移这类信息只写在各源落盘 JSON（`<source>.json` 的 `error_msg`/`source_likely_down`/`is_timeout`）里，导致前端只显示笼统的「源本次不可用」，用户反复把站点迁移误判为网络问题重试。新增 `_source_state_msgs(out_dir)`（读各源 JSON 分类诊断）+ `_dedup_msgs()`（同源两路提示按状态词强度合并），`_run_task` 的 rc==0 分支改为双通道合并。文案分级：站点迁移（永久、重试无效、给 WHO 镜像替代路径，并注明「云端仍跑旧版节点需重新部署」）vs 端点超时/临时故障（可稍后重跑）。实测 19:11 任务目录：DRKS 迁移 + WHO/ISRCTN 临时故障三路提示正确分级、WHO 双路提示合并为一条。
- **新增「返回 CT 首页」按钮（ct-base workbench_ui.md §5.2 顶栏按钮簇梯度 v1.4.5 / 交付闸门 C7）**：用户指出右上角缺返回 CT 首页功能。现按规范补齐三件套：① 顶栏最右端（`#wb-bug` 之后，「离开」梯度位）新增 `#wb-cthome` 按钮——房子图标内联 SVG + 文字标签「CT 首页 / CT Home」；② JS 新增 `CT_HOME = "https://ct.medstatstar.com"` 常量（ct 系列统一门户，带协议防裸域名当相对路径解析）+ `wbGoCtHome()` 跳转函数（常量留空则仅 console.warn 不跳转）；③ I18N zh/en 双字典补 `ctHome` 键，按钮标签与 `aria-label`/`title` 同步走该键（`data-i18n-aria` + `data-i18n-title`），并给 `wbLocalize()` 补 `[data-i18n-aria]` 属性翻译支持（此前仅支持 `data-i18n` / `-ph` / `-title`）。C7 判据（节点 + 函数 + 常量三者齐备且非裸域名）核对通过；JS 语法校验通过。注：`https://ct.medstatstar.com` 为 ct 系列门户登记值（meta-analysis 为唯一特例指向官网，不适用于本技能）。
- **字号全面令牌化（ct-base workbench_ui.md §4.5 合规）**：此前 `index.html` 有 85 处裸 `font-size`（含 10.5px 低于 11px 可读下限、11.5/12.5/13.5/20/22px 等离群值），且未接入 2026-10-21 下沉的 `--wb-fs-*` 六档结构令牌。现：① 内联令牌区与 `tokens.css` 同步补入六档令牌（值同 ct-base 权威 `workbench/tokens.css`），`body` 引用 `var(--wb-fs-base)`；② `index.html` 79 处 + `wb-list.css` 10 处全部改走 `var(--wb-fs-*)`（10.5→2xs、11→2xs、12/13→xs、13.5/14→sm、12.5/xs、15→base、20/22→xl、16→lg）；③ 仅剩 3 处 media query 内 `16px` 为功能性特例（防 iOS 聚焦自动放大），已加注释标注。迁移后全文件仅令牌取值，后续调字号只改 `:root` 一处。
- **计划卡片可信度徽标真实化**：CDE/ChiCTR 行的 `verified` 不再按「翻译结果 ≠ 原文」误判——机器翻译（online）一律「未验证」，仅术语表命中（term_map）与原文直用（same/form）算「已验证」；zh 站点（ChiCTR）优先复用已翻译的 zh_kw（英文输入时 ChiCTR 不再拿到英文原词空查）。
- **自动翻译批量一次（用户反馈）**：`_build_cmd` 新增 `--kw-en/--kw-zh` 批量注入——工作台统一翻译一次（15 分钟记忆缓存）后，经 CLI gate 的 override 分支（`_kw_apply_override`）一次性设置 confirm-cond/intr、ictrp/cde/chictr 全部站点关键词，CLI 内各源不再各自 localize。有站点级 overrides 或显式 CDE 关键字时自动回退原路径（保护用户显式值）。配合上方 CLI 修复，全链路翻译恰为一次。
- **主按钮改两段式（先计划预览、确认后才检索），并删除独立「预览检索计划」按钮**：单击「检索注册库」→ `POST /api/plan` 生成检索计划卡片（标注「未发起检索」，各站点关键词可直接改写），主按钮变「确认并开始检索」；再次单击才带卡片内改写（`_planEdits` → `overrides`）提交 `/api/search`。检索/数据源/高级参数任何改动都会使待确认计划作废、按钮回到第一段；计划获取失败时明确报错且不发起检索。实证：卡片内改写 `osimertinib 719` 逐字进入实际执行命令的 `--confirm-cond`。专项 14/14；全套回归 88/88（26 回归 + 23 计划卡 + 17 高级参数 + 8 不结束专项 + 14 两段式）。
- **新增「高级参数」视图（第 4 个导航页，与检索直接联动）**：把 `ct_registry.py` CLI 的可选开关做成结构化表单——WHO ICTRP 高级检索（mode/condition/intervention/sponsor/country/phase/timeout）、CDE 高级检索（mode/multi-keyword/indication/drug name/type/applier/trial status/retry）、关键词体系（expand-intent / kw-en / kw-zh / 禁用在线翻译兜底）、输出与追踪（with-detail / download-docs / no-excel / lang / track / fallback-covered / CT.gov 与 CDE API key）。特性：①**命令预览实时联动**——任何改动立即反映到最终 CLI 命令（token 级一致）；②**依赖校验与「未生效」标注**——未勾选 WHO/CDE 时相关参数明确标灰并给原因（如 combined 需同时给出招募国家/Phases/申办方之一，否则回落自由词检索；multi_keyword 需先填多关键字）；③**密钥脱敏**——API key 进日志/命令预览一律 `****`；④**localStorage 持久化**，刷新保留；⑤「带这些参数去检索」一键跳回检索页并发起。后端 `_apply_adv()` 单点映射进 `_build_cmd()` 与 `_build_plan()`，`no_online_translate` 经 `CT_TRANSLATE_ONLINE=0` 环境变量同时作用于 CLI 与工作台自身本地化。新增 `--with-ctis`（EU CTIS 源）与 `ctis` 数据源芯片。
- **修复「超时部分结果：清单有数、报告数量为 0」**（`workbench/server.py`，用户实测反馈）：超时分支此前只回 `rows`，不回 `summary`——前端 metrics 读 `t.summary.landscape` 为空，三项指标全显 `-`，且 `excel=False` 无任何报告可下载，用户感知「报告数量为 0」。现：① 新增 `_partial_summary(rows)`，用已收集的行现算与 CLI `_print_summary` **同构**的 landscape 摘要（`raw_total`/`n_trials`/`phase_mix`/`region_mix`/`top_sponsors`；`cross_source_groups` 依赖被杀时不存在的 `dedup_summary`，诚实返回 `None` 显示 `-` 而非虚构 0）；② 新增 `_write_partial_xlsx()`——stdlib `zipfile` 手写最小 OOXML（零第三方依赖），超时场景生成可下载的部分结果清单；③ `/api/download` 增 `file` 参数白名单（`report.xlsx` / `report_partial.xlsx`）；④ `_runs_view` 历史列表兼容部分 xlsx。实测 30s 短超时：`raw_total=1 n_trials=1 phase_mix=[PHASE2×1]`，xlsx 下载 2427B（PK 魔数、zip 完整、XML 全部良构）。
- **修复「检索长期运行并不结束」**（3 处叠加缺陷，用户实测反馈）：
  1. **失败/超时后主按钮永久禁用**——`renderError()` 未复位 busy 态，主按钮一直转圈且不可点击，用户表现为「一直运行」且**无法再发起检索**。现于 `renderError()` 内 `wbSetBusy(false)` 并清理轮询定时器。
  2. **前端轮询超时检查被短路**——`pollTask()` 中「在途请求未回则跳过」的前置判断排在超时判断**之前**，一旦某次 `fetch` 卡住（`_pollInflight` 永不复位），超时逻辑永远不触发 → 页面无限转圈。现将超时判断前置，并新增「45s 无任何成功响应」的链路停滞熔断。
  3. **后端超时任务永远停在 `running`**——超时分支先把 `TASKS` 置为 `error` 再 `return`，`finally` 又用外层 `state` 覆写；此前 `state` 未赋值 → `UnboundLocalError`（线程崩溃，状态侥幸正确），修复预置值后又会把终态覆写回 `running` → 任务永不到终态。现超时分支同步置 `state="error"`，且 `finally` 不再覆写已是终态的条目。
- **「提交检索」不再被在线翻译阻塞**：原 `POST /api/search` 在请求线程里同步计算检索计划，中文未命中术语表时本地化会走在线兜底（MyMemory → Google，各 6s 超时）→ 提交后 6~12s 无响应，用户观感为「点了没反应」。现计划改由任务线程生成、随 `/api/task` 轮询下发（提交实测 **6~12s → 0.07s**），并对本地化结果加 15 分钟记忆缓存（计划与命令共用，避免重复调用外网翻译）。
- **超时改为终止整棵进程树**（`taskkill /T /F`）：此前 `proc.kill()` 只杀直接子进程，`search_ictrp.py` 等孙进程会变孤儿继续跑并持有 stdout 管道。
- **新增「已用 Xs / 后端上限 Ys」进度提示**（后端 `/api/task` 增 `elapsed` / `timeoutSec` 字段）：让长检索有明确边界，避免用户把「慢」误判为「不结束」。
- **修复「超时部分结果变垃圾 / 看起来像 0 条」**（`workbench/server.py`）：超时兜底 `_collect_partial` 用通用 `_canon` 解析各源原始 JSON，但 CT.gov v2 是**全量 study 嵌套结构**（`protocolSection.identificationModule.nctId` 等），`_canon` 的扁平键完全匹配不到 → 产出 `reg-` / `(untitled)` 占位垃圾行，用户感知为「0 条有效结果」。现新增 `_canon_ctgov` 专门解析 CT.gov v2 嵌套字段，`_collect_partial` 按源分派（CT.gov 走专门解析、其余走 `_canon`），并强化垃圾过滤（跳过 `reg-` 前缀与 `(untitled)`，任何提取不出真实注册号/标题的记录不再进入部分结果）。实测短超时场景：超时后返回 `NCT06578546 | Chemotherapy-free Regimen of Venetoclax…` 真实行，未完成的 WHO 正确标为 `pending`。

- **新增「检索计划」中间卡片**（`workbench/server.py` + `workbench/index.html`）：检索发起前/进行中/完成后均可查看——①**每个站点对应的关键词组**（CT.gov / WHO / CDE / ChiCTR / EU-CTR / ISRCTN / DRKS / PubChem，逐站列出实际下发的关键词、语言、来源徽标与对应 CLI 参数）；②**中文→英文翻译明细**（`term_map` 术语表已验证 / `online` 机器翻译未经验证 / `miss` 未命中）；③过滤条件及其**生效范围**（哪些过滤只作用于 CT.gov）；④最终执行命令全文。卡片内容由后端 `/api/plan` 返回，与 `_build_cmd()` **共用同一份解析结果 `_resolve_plan()`**，杜绝「卡片说一套、实际跑另一套」。
- **卡片内可直接改写任一站点关键词**并「应用调整并重新检索」：`overrides` 按站点生效（优先级 手工指定 > 表单填写 > 自动翻译 > 原文），逐站落到对应 CLI 参数（`--confirm-cond` / `--ictrp-keyword` / `--cde-keyword` / `--chictr-keyword` / `--euctr-keyword` / `--isrctn-keyword` / `--drks-keyword` / `--drug`）。
- **修复「勾选 PubChem 静默无效」**：CLI 分支为 `if args.with_pubchem and args.drug:`，工作台从不传 `--drug` → 勾选后什么都不发生。现于有干预/药物词时下发 `--drug` + `--confirm-drug`；无药名时在计划卡片与后端日志中如实提示「本次跳过化合物富化」。
- **修复「只填干预词时多站点被静默跳过」**：CLI 的 `base = args.cond or args.drug or args.sponsor`，工作台从不传 `--drug` → 仅填干预词时 `base=None`，WHO/EU-CTR/ISRCTN/DRKS/ChiCTR 全部报「needs --xxx-keyword or a base term」被跳过。现安全前提下补传 `--drug`（不改变 CT.gov 的 cond/intr 取值，也不改变已有 `base` 语义）。
- **修复「切语言后计划卡片不重渲」**：新增 `wbRefreshPlanCard()`，并实时保留用户手改值（`_planEdits`），避免语言切换丢失编辑。
- **修复「任务失联后主按钮永久禁用」**：轮询遇 `state=unknown` 时恢复主按钮与后端状态指示。

## （待部署）2026-10-20 · coze 端点迁移至 ct-base §20.18 反盗调入站准入（antiscrape）

> 取代下方 v0.14.0「query_origin 准入闸门」待部署条目——原 `_guard_query_origin` 内联闸门已整体移除，改为逐字同步 ct-base 标准件 `antiscrape.py`，覆盖 §20.18 全库统一规范的六级准入。改动在 `adapters/coze/src/main.py`（coze 部署源，被根 .gitignore 忽略，不进 git），需重新打包 zip+MD5 上传 Coze 生效（手动，待授权）。

- **标准件逐字同步**：`antiscrape.py` + `habit_analyzer.py` 从 ct-base 拷贝，`diff -q` 校验 VERBATIM MATCH；新增 `wrap_stream_release` 标准助手（流式并发槽延迟释放）。
- **接线四个算力端点 + OpenAI 兼容口**：`/run` `/stream_run` `/node_run` 全部挂接 `_admit_antiscrape(request, raw_body, payload)` + `request.state.antiscrape_admitted = True`；每个端点 `finally: _release_antiscrape(request)` 释放全局并发（`/stream_run` 经 `wrap_stream_release` 包裹生成器，把并发槽释放钉在流真正耗尽处，而非构造响应时——修复了旧写法并发上限对流式在途算力失效的反模式）。`/v1/chat/completions` 默认 `404`（§20.18.4：零合法流量模板端点 = 纯攻击面），经 `CT_ENABLE_OPENAI_COMPAT=1` 显式开启后受 `_admit_antiscrape_light(request, with_concurrency=True)` 轻量准入。
- **行为等价性（关键不变量）**：原 `_guard_query_origin` 两类拒绝（空值 / 占位哈希 `sha256:<64 位全同字符>`）→ 200 静默空体，已由 antiscrape `check_allow` 第 2 级统一覆盖（含 query_origin 双位置回退），本地冒烟测试 5 例全绿（空 / None / 缺 / 占位哈希 → 200 空体，合法 → 放行）。移除冗余内联 `_PLACEHOLDER_ORIGIN_RE` / `_REPEATED_CHAR_RE` / `import re`。
- **§20.18.4 信息收敛**：统一拒绝载体 `_response_from_admit`，429 固定体 `{"ok":false,"error":"rate_limited"}` + `Retry-After`，禁带 reason 区分键 / `X-AntiAbuse: deny:reason` 头；200 silent drop / 413 空体。
- **部署前平台 env 注入待办**：`CT_ANTISCRAPE_SALT` 🔴 必配固定盐（否则重启失效，三级回退缺省临时盐）；`CT_ANTISCRAPE_DENYLIST_TABLE_ID`（拒止表，缺省走本地 JSONL 降级）；`CT_ANTISCRAPE_FEISHU_APP_TOKEN` / `CT_ANTISCRAPE_FEISHU_TABLE_ID`（遥测，惰性 import 优雅降级）。

## v0.14.0（待部署·已撤销，被上方 2026-10-20 取代）2026-10-19 · coze 端点落实 ct-base §1.4 `query_origin` 准入闸门

> 随 ct-base v1.3.33 契约 §1.4 落实。改动在 `adapters/coze/src/main.py`（ct-search 工作流源码），**仅端点侧行为，不影响任何客户端出站契约**；部署需重新打包 zip+MD5 上传 Coze（手动，待授权）。

- **合并守卫 `_guard_query_origin()`**：原 2026-09-13 占位哈希闸门（静默空串）保留，新增 `query_origin` 空值拒绝（缺失 / `None` / 空串 / 纯空白 / 非字符串 → 返回 `""` 并拒绝处理、不调下游、不写飞书）。`/run` / `/stream_run` / `/node_run` 三调用点入口均已挂接。
- **动因**：飞书 searchlog 实测出现绕过客户端的裸 POST（query_origin 为空），端点需准入门禁。零误伤：全部 ct-* 客户端出站必带非空 query_origin（§8.6 + 兜底注入）。

## v0.13.4 (2026-10-17) · SkillHub 卡面「需配置 API Key」徽章措辞修正（零用户侧配置事实对齐）

> SkillHub 竞品扫描发现：ct-registry 卡面带平台「需配置 API Key」徽章，被「不限 API Key」筛选器排除，与事实相悖——端点 Bearer 是作者签发的**包内共享凭证**，用户侧零配置。根因是 `network_note` 与正文两处 `Bearer token REQUIRED` 措辞被平台解析为用户需自备 key。本版仅改措辞对齐事实，零行为变更。

- **`SKILL.md` network_note**：`Bearer token REQUIRED - verified: HTTP 401 without it` → `endpoint credential bundled in-package (shared public token, no user-side configuration — verified: HTTP 401 without it, i.e. the token ships with the skill)`。
- **`SKILL.md` 正文（CDE 端点段）**：同样的 `Bearer token REQUIRED (verified: HTTP 401 without it)` → `endpoint credential bundled in-package (shared public token, no user-side configuration; verified: HTTP 401 without it — the token ships with the skill)`。全文件 `REQUIRED` 措辞清零。
- **frontmatter**：`summary` / `description` 末句统一为「零用户侧配置：检索端点凭证随包分发，开箱即用」（英文段同步 `Zero user-side configuration — retrieval endpoint credentials ship in-package, ready to use out of the box`）。
- **未改**：端点调用契约、token 分发机制（XOR+base64 包内混淆）、CDE/ChiCTR/ISRCTN/DRKS/WHO 检索链路均不变；`--cde-api-key`（DXY 商业镜像，opt-in）语义不变。

## v0.13.3 (2026-10-13) · 修复云端部署「检索不返回结果」（授权门路径 / 药名译名 / 超时与失败可见性）

> 用户报障 https://ct-registry.app.workbuddy.host/ 长期检索不返回结果。实测定位四层根因：① 出站授权门只读家目录 config，云沙箱必然缺失 → WHO/CDE/ChiCTR/ISRCTN/DRKS 全灭（10-08 起云端实际只有 CT.gov 单源）；② CT.gov 直连在云沙箱间歇 TLS 握手超时（共享出口 IP 被限流），兜底又死于 ①；③ 阿西米尼不在任何词表，机翻成 "Assimini" → 0 命中且静默；④ 全源失败仍 exit 0 + 空报告，前端空态文案误导，超时口径三方不一（后端 60s / 前端 90s / 横幅 5 分钟）。

- **`adapters/extsvc_client.py`（P0 结构性）**：`_check_outbound_authorization` 原只读 `~/.workbuddy/skills/ct-registry/config/config.json`（家目录绝对路径）→ 新增 `_authorized_endpoints()`：**技能/应用根 `<root>/config/config.json` 优先 + 家目录回退**，两候选 auto_approve_endpoints 取并集。本地两候选实为同一文件（行为不变）；云端 publish-dist 布局（/workspace）首次可解析。
- **`workbench/publish-kit/build_publish.py`（P0）**：WHITELIST_DIRS 增加 `config`；`excluded()` 增加 config 文件级白名单——仅 `config.json` 随包发布（`usage.json` / `*.dat` / `kw_system_cache.json` / `config.local.json` 排除）。
- **`references/term_map.json`（P0）**：补 `阿西米尼 → asciminib`（606 词条；原三张词表全 miss，MyMemory 机翻产出错误拼写 "Assimini"）。
- **`workbench/server.py`（P1）**：`CTWB_TASK_TIMEOUT` 默认 **60s → 180s**（历史值把正常宽词检索误杀，前端 90s 轮询先杀）；新增 `_parse_failed_sources()`——从子进程日志提取失败信号（AUTH-BLOCK / TLS 握手超时 / 站点检索失败 / WHO 兜底失败 / TIMEOUT），经 `/api/task/<id>` 以 `failedSources` 透出；`/api/localize` 增 `verified` 字段（online 机翻 = false）；机翻关键词日志打 `[UNVERIFIED-MT]` 标记。
- **`workbench/index.html`（P1）**：前端轮询上限 **90s → 210s**（后端 180s + 30s 余量），`pollTimeout` / `runningBanner` 文案同步（10 秒 ~ 3 分钟）；`wbTranslateHintHtml` 对未验证机翻追加警示（新增 i18n `kwTranslatedOnline`，zh/en）；`renderDone` 在 0 结果时渲染 `failedSources` 失败清单（新增 i18n `failedSourcesTitle` / `failedSourcesTip`，zh/en），不再把「源全失败」显示成「0 条合法空结果」。
- **`workbench/server.py`（P1，回归顺带发现）**：CDE 关键词回退链补 `intr`（原链 cond-only，仅填干预词并勾选 CDE 时被静默跳过，日志打 `--with-cde 需要 --cde-keyword`）。
- **验证**：`_authorized_endpoints()` 在 publish-dist 布局下放行 coze 双端点；term_map 阿西米尼→asciminib（source=term_map）；publish-dist 布局实跑 intr=阿西米尼 全链路通（本地 CT.gov 不通 → WHO 兜底经授权门放行取回记录）；inline JS 语法校验通过；发布后线上回归见部署记录。

## v0.13.2 (2026-10-13) · 修复工作台调用 entry_point 恒为 skill（§1.3 接线）

> ct-base coze_io_contract §1.3 工作台接线三架构之「架构 B · Popen 子进程」（本技能为孙进程链：`server.py → Popen(ct_registry.py) → subprocess.run(search_ictrp.py)`）。v0.13.x 只做了注入侧（`_attach_coze_contract` payload 带 entry_point），设置侧零接线；父进程 `set_entry_point()` 无法跨进程传递 → 应用页面调用恒落默认值 `skill`。

- **`adapters/search_ictrp.py`**：新增 `_entry_point_from_env()`——模块加载时从环境变量 `CT_ENTRY_POINT` 解析 `_ENTRY_POINT` 初值（白名单 `skill`/`workbench`/`api`，空白/非法一律回退 `skill`）；`set_entry_point()` 运行期覆盖语义不变。
- **`workbench/server.py`**：`Popen(ct_registry.py)` 的 `env` 增加 `CT_ENTRY_POINT=workbench`。环境变量沿 `server.py → ct_registry.py → search_ictrp.py` **逐级继承**（`ct_registry.py` 的 `subprocess.run` 未显式传 env，自动继承父进程环境）→ **中间层 ct_registry.py 零改动**。agent / 技能 CLI 不设该变量 → 恒 `skill`（无回归）。
- **同步**：`workbench/publish-dist/adapters/search_ictrp.py`、`workbench/publish-dist/workbench/server.py` 与主文件逐字节一致（diff 验证）。
- **验证**：`_entry_point_from_env()` 七组用例（含大小写变体 `WORKBENCH` → 回退）全过；`_attach_coze_contract` 默认注入 `skill` 且 `skill_version` 完好复核通过；`py_compile` 四份副本全过；跨技能契约回归 `ct-base/scripts/tests/test_entry_point.py` E1–E9 全绿。
- **范式沉淀**：ct-base `references/coze_io_contract.md` §1.3 新增「工作台接线三架构」规范段，本技能为架构 B 范本之一（含孙进程链继承说明）。

## v0.13.1 (2026-10-13) · coze 0.3.94 文献检索月份级日期窗口（ct-literature online 原生过滤）

> 用户指认 `adapters/coze` 即 ct-search.coze.site 云端代码位置，要求让 online/Coze 通道原生支持月份级日期窗口（而非调用方规避）。客户端 ct-literature v1.4.3 联动。

**coze 侧（`adapters/coze/`，服务端私有 §16.7 · 本地已改，待发布）**

- **`src/graphs/state.py`**：三模型（`GraphInput` 入口投影 / `GlobalState` 图内传递 / `SearchNodeInput` 节点注入）**均显式声明** `lit_date_from` / `lit_date_to`（`Optional[str]`，YYYY-MM-DD）。与 FAERS/OpenFDA 的 `date_from/date_to`（YYYYMMDD）格式与语义均不同，独立命名 `lit_*` 防混用。🔴 漏声明即被 `extra='ignore'` 静默丢弃、节点恒 None——2026-10-08 FAERS 同款坑（当时只补了 GraphInput/SearchNodeInput、漏 GlobalState）。
- **`src/graphs/nodes/literature_nodes.py`**：五个文献节点全部改为 **date 优先、year 回退、老客户端逐字不变**：
  - `openalex_node`：`from_publication_date/to_publication_date:YYYY-MM-DD`（year 回退 Jan-1/Dec-31）
  - `europepmc_node`：查询子句 `(FIRST_PDATE:[lo TO hi])`（沿用本地 2026-10-12 实证结论：`filter=pdates:` 被 API 静默忽略、按索引日期放回老文；`PUB_YEAR` 仅作 year 回退）
  - `_fetch_preprints_epmc`（bioRxiv/medRxiv 共用）：同上 `FIRST_PDATE` 子句
  - `arxiv_node`：独立 filter 参数 `submittedDate:[YYYYMMDD TO YYYYMMDD]`（不拼 search_query 的教训保持有效）
  - `semantic_scholar_node`：`publicationDateOrYear:{date_from}:{date_to}`
- **🔴 根因修复：`europepmc_node` `publication_date` 恒空串**——`printPublicationDate`/`dateOfPublication` 嵌在 `journalInfo` 下，顶层 `rec.get()` 永远取空。改 `firstPublicationDate`（顶层真源）优先，对齐本地 `fetch_europepmc.py` 2026-09-08 BUGFIX（该修复此前漏同步到云端，2026-10-12 在线实测复证）。
- **`src/graphs/nodes/_version.py`**：`COZE_VERSION` 0.3.93 → **0.3.94**（升级纪律：只改本文件）。
- **验证**：`scripts/selfcheck.py` 44/44 PASS；三模型穿透（GraphInput→GlobalState→SearchNodeInput）+ 老客户端兼容、各源原生检索式打桩捕获（OpenAlex filter / EuropePMC·bioRxiv FIRST_PDATE 子句 / arXiv submittedDate）、date 优先于 year、year 回退逐字不变，共 11 项全过（coze `.venv` 实跑）。

**客户端（ct-literature v1.4.3，本仓库外）**

- `fetch_coze_unified.dispatch()` payload 键 `date_from/date_to` → `lit_date_from/lit_date_to` 对齐云端契约；旧云端（未部署 0.3.94）收到新键被静默忽略不报错（向后兼容已实证）。

**部署**：coze 0.3.94 需在 Coze 平台人工发布；发布前 online 通道仍依赖 ct-literature 客户端 `clip_by_date_window()` 兜底（正确性有保证，但近期文献召回受 max_results 截断限制）。

## v0.13.0 (2026-10-08) · pytrials + Docling 外部开源资产引用

> 基于《临床试验Skill推荐》分析，新增 pytrials 和 Docling 两个外部开源工具集成。

- **新增 External Open-Source Integrations 表格**：列出 pytrials（CT.gov 批量检索客户端）和 Docling（法规文档结构化解析）两个工具
- **pytrials 增强模式 (opt-in)**：使用 pytrials 作为官方 API 客户端批量拉取 CT.gov 字段，新增适应症分布热力图、终点设计对比、中心历史项目检索
- **增量兼容**：新增内容为可选引用，不影响现有 9 源检索体系和回归测试

## v0.12.1 (2026-10-07) · 接入 `entry_point` 调用来源标记（ct-base coze_io_contract §1.3 / §2.3）

> 飞书searchlog 新增 `entry_point` 独立列，用于按**调用来源**（技能本身 / 工作台 Web 应用 / 未来第三方 API）直切筛选。本技能此前未发送该字段，现**客户端 + coze 侧**一并补齐。

**客户端（本地出站信封）**

- **`adapters/search_ictrp.py`**：新增模块级 `_ENTRY_POINT = "skill"` + `set_entry_point(v)` + `entry_point()`（枚举白名单 `skill`/`workbench`/`api`，空值/空白/非法值一律回退 `"skill"`，绝不写 `None` 或脏值）；`_attach_coze_contract()` 在顶层信封注入 `"entry_point"`（与 `query_origin` / `skill_version` 同级，`setdefault` 保证显式传参优先 + 幂等）。
- **与 `query_origin` 正交（🔴 不得混用）**：`query_origin` 按机器（硬件 ID / 主机名 SHA-256），同一台机器上 skill 与 workbench 算出的哈希逐字节相同 → 无法区分界面来源；`entry_point` 按入口/界面，故须独立字段。
- **未并入 `querystr` / `resultstr`**（§2.3 硬约束）：`entry_point` 只作顶层信封，由coze 端分流到飞书独立列。

**coze 侧（`adapters/coze/`，服务端私有 §16.7 · 本地已改，待发布）**

- **`src/graphs/state.py`**：三个承载模型**均显式声明** `entry_point: Optional[str]` —— `GraphInput`（入口投影）/ `GlobalState`（图内传递）/ `FeishuWriteInput`（节点入参）。**漏声明会被 `extra="ignore"` 静默丢弃**，与已踩过的 `skill_version` / `total_count` 同一根因，故三处一个都不能省。
- **`src/graphs/nodes/feishu_write_node.py`**：record 字面量新增 `"entry_point": getattr(state, "entry_point", None) or "skill"`；模块 docstring 补§2.3 落点说明。
- **`src/graphs/nodes/publisher_pdf_batch_node.py`**：该节点自建 record（ct-literature PDF 批次表），同样补 `"entry_point"` 键，保持同表列名一致。
- **三镜像同表**：ct-registry / ct-samplesize / meta-analysis 共用同一飞书表（`DEFAULT_APP_TOKEN=Pog0bGNMbaCWMIsGRNpckHcnn9f` / `DEFAULT_TABLE_ID=tblQ8OQ0rXsXQWkh`，靠 `skillname` 列区分技能），故列名必须**精确统一为小写 `entry_point`**，否则 `batch_create` 报未知字段名。已核对三镜像列名一致。

**验证**

- 新增 `tests/test_coze_entry_point.py`（C1–C6，6/6 RC=0）：三模型声明齐全 / 两个 record 均含该键 / 列名精确小写 / 回退语义（脏值与空值均回退 skill，绝不写 None 或空串）/ 不并入 resultstr·querystr / **pydantic 2.13.5 模型层实测**（老客户端不带字段得 None→回退 skill，新客户端值投影保留）。
- 全链路贯通实测：客户端 payload → `GraphInput` → `FeishuWriteInput` → record 取值，`workbench` 全程保留；老客户端回退 `skill`。
- 跨技能客户端契约回归 `ct-base/scripts/tests/test_entry_point.py`（E1–E9，9/9）；`py_compile` 三个改动文件均通过。
- 既有 `tests/regression_harness.py` PASS=28 FAIL=2 —— **两个失败为既存问题**（case09/case10 引用的 `scripts/search_ictrp.py` 路径早已不存在，文件在 `adapters/`）。已用 `git stash` 对照证明：改动前后同为 PASS=28 FAIL=2，与本次无关。

> ⚠️ **部署铁律（§2.3）**：飞书列已存在（2026-10-07 表头可见），故部署新 coze 代码是安全方向 ——「新coze + 有列」正常落值，不命中 `batch_create` 未知字段名报错窗口。
> ⚠️ coze 侧 `adapters/coze/` 已被 `.gitignore` 忽略（服务端私有），**发布需手动同步到 Coze 控制台**，不在 git 发布链路内。

## v0.12.0 (2026-10-06) · 工作台安全加固：静态文件白名单（P0）+ 路径黑名单（P3）

> 已发布工作台应用（`ct-registry.app.workbuddy.host`）安全加固，阻止源码/凭据/敏感数据被 HTTP 下载。

- **`workbench/server.py` + `workbench/publish-dist/workbench/server.py`**：
  - P0: 新增 `_STATIC_ALLOWED` 扩展名白名单（12 种），非白名单扩展名返回 403。
  - P3: 新增 `_STATIC_PATH_BLOCKED` 路径黑名单（`adapters`, `runs`, `scripts`, `out`, `references`），阻止目录级访问，返回 403 `forbidden path`。
- **影响**：Coze 服务端源码镜像目录结构无法通过 HTTP 探测；`references/*.json` 映射文件无法访问（已由 P1 文件名保护，P3 再加一刀）。`/api/*` 端点（`/api/search`, `/api/runs` 等）不受影响——走独立路由，不经过 `_static()`。
- **回归**：`curl http://127.0.0.1:8790/../adapters/coze/src/main.py` → 403；`curl http://127.0.0.1:8790/../references/term_map.json` → 403。

> 已发布工作台应用（`ct-registry.app.workbuddy.host`）安全加固，阻止源码/凭据被 HTTP 下载。

- **`workbench/server.py`**：`_static()` 新增 `_STATIC_ALLOWED` 扩展名白名单（12 种：css/js/svg/png/ico/json/woff/woff2/ttf/map/html/htm），非白名单扩展名返回 403 `forbidden type`。
- **`workbench/publish-dist/workbench/server.py`**：同步上述白名单修复（发布副本）。
- **影响**：`.py` / `.env` / `.pyw` 等源码/凭据文件无法通过 HTTP 下载；前端静态资源（css/js/ico/json 等）不受影响。
- **回归**：`curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8790/../scripts/ct_registry.py` → 403。

## v0.10.0 (2026-09-18) · resultstr 检索侧审计摘要（status/ok/total/s3）+ 遗留字段补声明

> ⚠️ **归版说明（2026-09-29 周检补）**：SKILL.md 当前版本为 `0.10.0`，但本文件此前首部恒为
> `Unreleased`、全篇无 `0.10.0` 条目（ct-base §16.8 / spec_lint F13 ERROR）。现按「首条版本须与
> SKILL.md 一致」将本条归为 `v0.10.0`。**下方自 2026-09-17 起至 `v0.9.3 (2026-09-06)` 之前的
> 全部 `Unreleased` 条目同属 0.10.0 变更集**，建议发布前由人工一次性合并为单条 `v0.10.0` 记录。

- **背景（用户指令）**：飞书 `resultstr` 目前仅记 `runtime_sec` + 版本字段，信息不足以审计
  「分析是否 OK / 检索到多少条 / 是否走 S3」。参考 `publisher_pdf_batch` 已有的
  `status/ok/total/s3/runtime_sec` 摘要形态，registry 检索路径的 `resultstr` 也应携带同样结构，
  使同一飞书表、同一 `resultstr` 列的 record 形状一致、可按端点版本归因。
- **改动（均在 `adapters/coze/src/`，服务端，需重新打包上传 coze 才生效）**：
  1. `nodes/feishu_write_node.py` —— `resultstr` 检索侧新增 `status` / `ok` / `total` / `s3`
     （对齐 `publisher_pdf_*` 审计 schema，ct-base §2.2）；`hit_count` 重命名为 `total`、
     `returned` 并入 `ok`（project_list.projects 长度；不可用→信任 total_count）。
     `log_only` 模式仍只写 `runtime_sec` + 版本字段，不写检索统计（不谎报 0 命中）。
  2. `graphs/state.py` —— `FeishuWriteInput` **补声明** `total_count` / `project_list` /
     `error_msg` / `log` / `s3_stored`（该模型 `extra="ignore"`；未声明字段被 langgraph 投影
     丢弃、节点恒拿不到，与 §2.1 已修的 `skill_version` 同一根因）。**顺带修复 CHANGELOG
     2026-09-17 记录的遗留 bug**：此前 `hit_count`/`returned`/`error`/`log` 大概率恒不落库。
  3. `nodes/_version.py` —— `COZE_VERSION` `0.3.89` → `0.3.90`（resultstr schema 变更，需端点版本可归因）。
  4. `scripts/selfcheck_log_only.py` —— 断言从 `hit_count` 改为 `total`/`ok`/`status`（L16/L16b/L17），
     log_only 断言扩为「不含 total/ok/status/s3」。
- **文档**：`adapters/coze/AGENTS.md` 飞书审计小节 `resultstr` 行更新为检索侧摘要 schema。
- **验证**：`py_compile` 通过；`scripts/selfcheck_log_only.py` 全绿（L11-L17）。
- ⚠️ **契约变更**：`resultstr` 弃用 `hit_count`/`returned`，改用 `total`/`ok`（与 pdf 路径对齐）。
  旧审计看板若按 `hit_count` 解析需同步；端点版本 `0.3.90` 可作切换分界。

## Unreleased (2026-09-17) · 飞书版本字段落点统一（ct-base coze_io_contract §2.1）

- **背景（用户指令）**：版本字段写入位置不固定——registry 端点 `publisher_pdf_batch` 把
  `skill_version` 写进 `querystr`，而 meta/samplesize 又各自不同 → 飞书表里同一信息位置不一致。
  ct-base `references/coze_io_contract.md` §2.1 现规定：**版本字段一律写 `resultstr`，
  `querystr` 不再存任何版本信息**。
- **改动（均在 `adapters/coze/src/`，服务端，需重新打包上传 coze 才生效）**：
  1. 新增 `graphs/nodes/_version.py::COZE_VERSION = "0.3.89"` —— 端点版本常量单一真源。
     此前本端点**没有**版本常量，只以 `dist/coze_deploy_bundle_<ts>.zip` 时间戳区分，
     审计表无法按端点版本归因；取值沿 CHANGELOG 末条 `v0.3.88` 顺延。
  2. `nodes/feishu_write_node.py` —— `resultstr` 顶层新增 `skill_version` + `coze_version`
     （均非空才写）；新增 `_strip_version_fields()`：客户端透传的 `querystr` 若含
     `skill_version` / `coze_version` 一律剔除，保证落点唯一。
  3. `nodes/publisher_pdf_batch_node.py` —— `_build_querystr()` **移除 `skill_version` 入参**；
     `_build_resultstr()` 新增 `skill_version` / `coze_version`，元信息全空时与历史格式
     逐字节一致。
  4. `graphs/state.py` —— `FeishuWriteInput` **补声明 `skill_version`**（该模型 `extra="ignore"`，
     未声明字段会被 langgraph 过滤、节点恒拿不到，与 CHANGELOG 已记录的 `log` 同坑）；
     5 处 `skill_version` 描述改指 resultstr。
- **文档**：`adapters/coze/AGENTS.md` 新增「飞书审计：版本字段落点」小节（querystr 禁写 /
  resultstr 三键 / 升级纪律只改 `_version.py`）。
- **验证**：`py_compile` 4 文件通过；冒烟确认 `_strip_version_fields` 剔除版本键、
  `_build_querystr` 键集无版本键、`_build_resultstr` 空元信息与历史格式逐字节一致。
- ⚠️ **遗留（未修，超出本次范围）**：`FeishuWriteInput` 同样未声明 `total_count` /
  `project_list` / `error_msg` / `log` → `hit_count` / `returned` / `error` / `log`
  大概率同样恒不落库（与 CHANGELOG 2026-09-08 记录的 `log` 同一根因）。需另行补声明后打包。

## Unreleased (2026-09-08 20:08) · Coze 源码打包（feishu 审计 resultstr 重构）

- 相对上一包 `coze_deploy_bundle_20260908_101717.zip` 仅 1 文件变更：`src/graphs/nodes/feishu_write_node.py` —— 审计 `resultstr` 与入参列 `querystr` 彻底解耦（去掉 `mode`），`hit_count` 恒写（0 命中亦有审计价值），新增 `returned`（实际返回条数，仅在截断/外置与命中数不同时出现）与 `log`（节点日志摘要，截断 120）。
- `py_compile` 全量通过（src + scripts）。
- **新部署包**：`dist/coze_deploy_bundle_20260908_200835.zip`（56 files / 192,115 B / MD5 `2d17d3201270d07c9df8c04a1ba0f964` / ZIP_OK，回读逐文件 MD5 与磁盘一致）；同步覆盖根目录 `coze_deploy_bundle.zip`。**待用户上传 Coze 控制台**；本地未发布。
- ⚠️ 已知待办：`GlobalState`（`src/graphs/state.py`，pydantic `extra="ignore"`）**未声明 `log` 字段**，且无节点写入 → 新加的 `log` 审计键当前恒不落库（`getattr` 兜底不报错，非阻断）。需补 `log: Optional[str]` 并指定产出节点后再打一次包。

## Unreleased (2026-09-08 12:10) · SKILL.md description 重写：对齐 summary 写法

- description 从 964 → **703 字节**（较原始 1985 降 65%），对齐 summary 风格：中文源列表 + 英文源列表 + 用途，去掉 B 档/零保密/Coze 等内部细节。
- 本地未发布。

## Unreleased (2026-09-08 12:02) · SKILL.md description 瘦身 + 正文去中文

- `description` 从 1985 → 964 字节（-51%），保留双语但去掉逐源 WAF/token 细节（正文 Data Sources 表已覆盖）。
- Features 段（P0-A/B/C/D）中文说明全部英文化。保留的中文均为合理用例：实际用户输入（`光生物调节`/`反馈问题`）、中文服务字面报错（`字段类型错误`）、CDE 参数值示例（`列汀`）。
- 本地未发布。

## Unreleased (2026-09-08 10:44) · README 示例 1 重写：单源限定 vs 默认全球

- 示例 1（zh + en）重定位：从「快速注册库检索（默认 CT.gov）」改为「单源限定检索（用户明确说『只要 CT.gov』）」，与示例 2「默认全球检索」形成清晰对比 —— 不指定范围 → 默认全球；明确说单源 → 走单源直连。
- 残留话术扫描 CLEAN。本地未发布。

## Unreleased (2026-09-08 10:39) · README 示例 2 重写：从"跨源"到"默认全球检索"

- 示例 2（zh + en）重定位：从「跨源（CT.gov + CDE）· 用户显式要求全球和中国都要」改为「默认全球检索（WHO ICTRP 14+ 注册库 + CDE）· 无需额外指定范围」，与 `--source` 默认值 `who` 一致。
- 残留话术扫描 CLEAN。本地未发布。

## Unreleased (2026-09-08 10:33) · README 案例区评估与同步（双语）

- 对照 WHO HTTP 快路径改造评估 README：示例区（Example 1–6）语义未变无需重写；「数据源与状态」表已含最新状态。**4 处过时/缺失需更新，已双语落地**：
  1. 耗时提示段首 + 「等多久」bullet：WHO「不是秒回 / 通常 1–5 分钟」→ **按检索面宽窄分层**：≤100 条窄词 HTTP 直连数秒即回（不开浏览器）；大结果集才 1–5 分钟浏览器翻页。
  2. 吞吐表：窄词行改「HTTP 直连秒回 2–15s、≤10 页自动翻完」；中词/宽词行补充「>100 条后浏览器接管 / HTTP 探测首页 ~2–6s」。
  3. 错误速查表 ISRCTN 行：陈旧「公开 API 失效（2026-07-20）」→ 重写为官方 XML API（`/api/query/format/default`）+ 异常时自动 WHO 兜底。
  4. 「返回偏少」段：补「>100 条取回 10 页 ~80–100 条并标 is_partial 属设计内能力边界（非故障）」。
- 残留话术扫描 CLEAN（`不是秒回 / is not instant / 100-150 页 / 公开 API 失效` 均无）。本地未发布。

## Unreleased (2026-09-08 10:17) · HTTP 翻页 max_pages 上限返回修复（承 10:00 实测发现）

- 实测翻页时发现的逻辑缺陷修复：`_try_http_fast_path` 收尾原为「is_partial → 一律 None 降级 Playwright」。当调用方显式 `--max-pages 3`（只想要 3 页）且 total>30 时，HTTP 翻满 3 页 30 条后因 is_partial 被**丢弃并降级 Playwright 重新翻**（双倍浪费）。
  - 修正：**未取全但已到达调用方页数上限（`page_seq >= max_pages`）→ 直接返回 partial 结果**；仅「未取全且未达调用方上限」（撞 HTTP 10 页能力边界 / 中途停）才降级 Playwright。
  - py_compile OK。
- **部署侧翻页累计实测**（走 Coze 端点，云端 IP 不受本机 WHO 限流影响）：`thymoma` → 95 条/148（95/95 去重、跨页覆盖多注册库年代）；`penile cancer` → 80 条/120、2m12s。多页翻页真实工作；本机 IP 直连限流时「无新增→降级」防护亦被验证。
- **新部署包**：`coze_deploy_bundle_20260908_101717.zip`（56 files / 191,789 B / MD5 `dce93213c1b78e99677d1abedc949e52` / ZIP_OK）。**待部署**；本地未发布。

## Unreleased (2026-09-08 09:40) · WHO HTTP 通道升级：翻页真相 + 多页抓取

- **用户质疑「HTTP 翻页不可能？不应该」** → 深入排查推翻此前的「无法翻页」结论：
  - **真因 ①**：回发 payload 误带 `txtTitle/txtCondition/ddlPageSize` 等结果页**不渲染**的搜索控件字段 → ICTRP 服务端异常返回 2679B 软错误页。去掉即通（隔离测试：结果页 VS 三件套空回发成功 80527B；+空 txt 字段即 2679B）。
  - **真因 ②**：顶部 `dlPager` 的页码链接回发**静默返回重复页**（服务端忽略）；必须用**底部 `dlPager2`** 的 target（`ctl00$ContentPlaceHolder1$dlPager2_ctlNN$lnkPageNo`）。
  - **真因 ③**：高频连续回发触发服务端风控——翻页被**静默降级为首页缓存**（页无新增，非 2679B）。代码以「页无新增」为信号停止。
  - 干净窗口实测：cancer 连翻 P2–P6 全通、无重叠、~4–7s/页（22s 取 60 条）；diabetes 用 dlPager2 翻 P2 0 重叠。
  - 硬边界：结果页 pager 每屏仅渲染 10 个页码（1..10），第 11 页起无链接（GridViewSearch doPostBack 为 Playwright JS 专属）；`ddlPageSize=100` 搜索亦 2679B。→ **HTTP 封顶 10 页 × 10 条 = 100 条**。
- **`_try_http_fast_path` 升级为多页全量抓取**：
  - 新增 `_http_pager2_target()`（解析底部 dlPager2 目标页 target）与 `_http_page_hidden_fields()`（结果页 hidden 全集）。
  - 流程：搜索 → 0 条 / 首屏即全量 / max_pages≤1 → 直接返回；2..10 页 → 循环翻页（payload = 当前页 hidden + dlPager2 target，**严禁 txt*/ddlPageSize**；每页 2.0–3.5s 节流防风控——2026-09-08 09:37 用户要求上调，原 0.8–1.6s 在连续翻页时仍可能被限流）；翻页遇 2679B / 无新增 / 超预算 / total>10 页 → **返回 None 整体降级 Playwright**（保证取数质量不降）。
  - 验证（AST 复刻真实代码 + 真实站点，4/4）：osimertinib 2.9s 命中 2 条；无匹配词 2.0s 返 0；cancer 4.8s 探测后降级（日志证实「翻页无新增→限流判定→降级」防护路径生效）；复杂字段 0 开销降级。
- **`_wait_for_page_ready` + goto 等待修复（承 09:20 条目）** 保留：Playwright 路径作为 >100 条 / 复杂字段的兜底。
- **新部署包**：`coze_deploy_bundle_20260908_093749.zip`（56 files / 191,504 B / MD5 `19c0af9f97c3e941021a52e8ec5fa52c` / ZIP_OK）。**待部署**；本地未发布。翻页节流已按用户要求（09:37）从 0.8–1.6s 上调至 **2.0–3.5s**——0.8–1.6s 在连续翻页时仍可能被风控静默降级。

## Unreleased (2026-09-08 09:20) · WHO 节点改造：HTTP 首屏快路径 + 修复 fill 超时（方案 C）

- **诉求（彤）**：WHO 检索门户手工正常但节点超时，要求核查是否有官方 API 可用。核查结论：**无公开免费 API**（ICTRP Web Service 需付费申请；遗留 `.asmx` 端点已停用——返回 **HTTP 200 + 2679B** ICTRP 软错误页，勿按状态码判活，真 404 仅 103B）。但实测高级检索页支持**纯 HTTP POST 首屏检索**（1–15s，不触发 cookie/JS 挑战）。选型 **C = HTTP 快速探测 + Playwright 翻页兜底**。
- **`nodes/who_search_node.py` —— 新增 HTTP 首屏快路径**：
  - `_http_adv_first_page()`：`GET /AdvSearch.aspx` 取 VIEWSTATE 三件套 → `POST` 回传 + `txtCondition/txtTitle/txtIntervention/txtPrimarySponsor` + `btnSearch=Search`，内容判活（软错误页/无结果表 → 报错）。复用 `_parse_results_from_grid` / `_get_summary_and_pages` 解析，返回结构与原 Playwright 成功分支同构。
  - `_http_channel_suitable()`：仅 keyword / 简单文本字段、运算符 AND、无复杂筛选（国家/日期/阶段/招募状态/勾选）才走 HTTP，语义不可对齐一律降级 Playwright。
  - `_try_http_fast_path()`：接入 `_do_who_advanced_search` 入口（浏览器创建前）。**0 条 / ≤10 条（首屏即全量）→ 直接返回，不开浏览器**；大结果集 / 复杂字段 / HTTP 失败 → 返回 None 走原浏览器流程。
  - 实测（本地复刻真实函数 + 真实站点）：`osimertinib` **2.1s** 命中 2 条（原 Playwright 30s+ 超时）；`cancer` 3.3s 探测后正确降级（33366 条需翻页）；无匹配词 1.9s 直返 0 条；`who_country` 复杂字段直接降级零网络开销。4/4 断言通过。
- **`nodes/who_search_node.py` —— 修复 `Page.fill` 30s 超时根因**：
  - `_wait_for_page_ready()`：弃用 `networkidle`（Playwright 官方不推荐、对 GA/轮询页必超时且异常被吞）→ `domcontentloaded` + 显式等 `#ImgLoading` 遮罩隐藏 + 800ms 抖动。
  - 三处 `page.goto(..., wait_until="commit")` → `"domcontentloaded"`（等 DOM 就绪而非只等响应开始）。
  - 旧代码用 `"txtCondition" in content`（HTML 字符串）判定页面就绪是**误判**——元素在 HTML ≠ 可交互，这正是 fill 超时的直接原因。
- **已知边界**：ICTRP 服务端对所有回发（翻页 `dlPager` / 改每页条数 `ddlPageSize` 10–100 / 导出 XML）一律返回 2679B 软错误页（已排除缺 hidden 字段、缺 select、异步回发头等原因）→ HTTP 通道只做首屏 ≤10 条；翻页仍由 Playwright 承担。
- **新部署包**：`coze_deploy_bundle_20260908_091827.zip`（56 files / 189,389 B / MD5 `be25ba9dd67d19db89950d5bb89ff2cc` / ZIP_OK）。**待部署**；本地未发布。

## Unreleased (2026-09-08 08:45) · 合并检索源兜底拓宽 + README「数据源与状态」表

- **诉求（彤）**：① 对于有合并检索源的站点，原站点不通时应当使用合并检索源做备用方式；② 对于确实站点异常的情况，技能应该可以返回相应的提示信息；③ 多源检索的技能应在 README 中清晰列出各种源的情况（范式 = ct-literature）。同步沉淀为 ct-base §13.14 / §14.2 / §14.3。
- **本地 `search_ictrp.py` —— 兜底触发条件拓宽（关键修复）**：
  - **修复前缺陷**：WHO 兜底仅认 `empty_no_error`（0 条 + 无错误）。DRKS 站点迁移属**显式 error**（`error_msg` 非空），故 `empty_no_error=False` → **兜底永不触发**，只能拿到 0 条 + 迁移提示，拿不到 DRKS 数据。
  - **修复后**：WHO-COVERED 源（chictr/isrctn/drks/euctr）返回 0 条时——① 节点**显式报错**（迁移 / WAF 拦截 / 抓取失败 / API 异常）→ **直接判定原站点不通、跳过对照探针**（省一次调用）→ 立即切 WHO 线路；② 0 条 + 无错误 → 仍走**对照词探针**区分「真实零结果」与「节点故障」（探针有数据 = 真实零结果，不浪费 WHO 配额）。
  - `CONTROL_TERMS` 新增 `euctr`（WHO 亦镜像 EUCTR 记录，使探针对该源同样生效）。
- **兜底结果溯源标注**：兜底成功 → 回填 `records`/`total`，清 `error_msg` 与 `source_likely_down`（数据可用），并置 `fallback_used=who_ictrp` / `fallback_reason=<src>_down` / `<src>_records_via_who` / `note`（保留原诊断 + 说明来自 WHO 合并源）。
- **兜底失败（WHO 亦报错 / WHO 无该源记录）→ 保留明确 `error_msg`** 并追加 `[WHO 回退亦失败: …]`，`source_likely_down=True`——**绝不把「源不可用」伪装成「无结果」**。
- **README（中英双语同步）**：新增「## 数据源与状态」——一张主表（源 / 访问方式 / 角色覆盖 / **当前状态含实测日期** / 兜底策略）+「各来源如何配合」（CDE 始终独立检索、WHO 为合并兜底源、CTIS 非 WHO 一级镜像故无兜底）+「站点异常会返回什么」（DRKS 迁移 / ChiCTR 故障 / ISRCTN 拦截 / 真实零结果 vs 源故障的探针区分）。
- **验证**：
  - `py_compile` OK。
  - **离线补丁测试 4/4 分支符合规范**：① 显式迁移报错 + WHO 兜底成功 → 2 条回填、`fallback_used=who_ictrp`、`error_msg=None`、`note` 保留迁移诊断、**探针调用 0 次**（修复前此场景完全不触发）；② 0 条 + 探针判定故障 → 兜底成功；③ 真实零结果（探针有数据）→ **不兜底、不报故障**；④ 显式报错 + WHO 亦失败 → 保留 `error_msg` + `[WHO 回退亦失败: …]`。
  - **真实 DRKS 端到端实测**：迁移报错 → `[SOURCE-DOWN] DRKS 节点显式报错，判定原站点不通` → `[FALLBACK-WHO] 切 WHO ICTRP 线路查 drks 来源`；本次 WHO 节点自身 Playwright `Page.fill` 超时（站点/节点侧波动，约 1h 前 WHO 尚正常），故落到「保留明确提示」分支并正确追加 `[WHO 回退亦失败: …]`。
- ⚠️ **本次改动全在本地编排层，无需重新打包部署 Coze**（ISRCTN XML API 包 `coze_deploy_bundle_20260908_083106.zip` 仍需单独部署）。**本地未发布**。

## Unreleased (2026-09-08 07:40) · DRKS/ISRCTN 站点异常诊断 + EU-CTR/CTIS 默认翻页收敛

- **诉求（彤）**：部署后全源回归测试——EU-CTR/CTIS 误判"超时"实为测试参数错误（误用 literature 的 `max_results` 而非 `max_pages`，节点抓默认页数累积超时）；真实问题在 DRKS（站点迁移）与 ISRCTN（holding）。
- **服务端（`adapters/coze/src/graphs/`）**：
  - `nodes/drks_search_node.py`：**迁移预检短路**——新增 `_precheck_drks_migrated()`（requests `allow_redirects=False` 探测旧入口 navigate.do，1.1s 命中 HTTP 307 → bfarm.de），命中即快速返回明确错误 + WHO 兜底指引，不再 Playwright 每页 30s 空转（此前 0 条耗 60s+）；`_do_search` 0 条时回读 page_title/url 记入 `site_hint` 诊断。
  - `nodes/isrctn_search_node.py`：**改用官方 XML API 彻底替代 Playwright 爬网页**（根因纠正）。此前误判 ISRCTN 处于 `/holding` 维护页；实测该页实为 **cookie/JS 机器人验证挑战页**（"Please enable cookies and JavaScript to use ISRCTN"，靠 `CHK` cookie 做跳转），无头浏览器被拦截返回此页 → 解析不到 `/ISRCTN` 链接故 0 条（彤反馈手工浏览器/WebFetch 均正常返回数据：cancer 5613 条 / diabetes 4314 条）。官方 FAQ 明确「请勿爬取本站，XML API 是获取试验数据更高效的方式」。改用公开 XML API `GET /api/query/format/default?q=<kw>&limit=<n>`（无需 key，返回 XML，**绕开验证挑战**），解析 `trial.publicIdentifierCanonical`（含 ISRCTN 前缀）兜底 `trial/isrctn` 子元素 + `trialDescription/title`；`max_pages` 映射为 `limit`（下限 10 / 上限 100，符合官方「限制单次查询规模」建议）；多关键词仍按 project_id 取交集；真正 0 匹配（`totalCount=0`）不再误报「站点异常」。已用逐行复刻脚本对真实 API 功能验证：cancer/diabetes 正确返回 10 条、编号标题无误，无匹配词返回 0 且不报故障。
  - `sources.py`：drks/isrctn 白名单注释登记站点状态（307 迁移 / holding），防后续误判。
- **本地（发布包）**：
  - `search_ictrp.py` `_build_simple_payload`：euctr/ctis **无显式 max_pages 时默认收敛**——euctr=3 页（~60 条）、ctis=2 页（~100 条）；EU-CTR 单页实测 ~13s，此前默认 10 页累积 130s+ 易撞网关/客户端超时；显式 `--max-pages` 可覆盖。
- **验证**：`py_compile` 3/3；预检逻辑 standalone 复刻实测 **1.1s 命中 307→BfArM**；search_node 分支与 sources 白名单一致（selfcheck A1 无影响）。
- ⚠️ 服务端改动需**重新打包部署**到 Coze 控制台才生效。**本地未发布**。

## Unreleased (2026-09-07 21:00) · EU-CTR/CTIS 抓取上移 Coze + 新增 CTIS 源

- **诉求（彤）**：功能/代码保护——EU-CTR 上移 Coze（本地解析器随包发布属资产泄露）；调研发现 CTIS（EudraCT 继任者，2022+）有**公开无认证 REST API**（实测打通，纠正此前"CTIS 需 OAuth2"误判），一并新增 CTIS 源（search + detail）。
- **服务端（`adapters/coze/src/graphs/`）**：
  - `sources.py`：`SUPPORTED_SEARCH_SOURCES` + `euctr`/`ctis`；`SUPPORTED_DETAIL_SOURCES` + `ctis`（euctr 不做 detail——EudraCT 详情页是 ASP.NET postback 壳，本地本就只有 list）。
  - 新 `nodes/euctr_search_node.py`：移植本地 `search_eu_ctr.py` 的 HTML list 解析（纯 HTTP requests，无反爬无需 Playwright），修复标题 label 前缀残留；实测 osimertinib 20 条。
  - 新 `nodes/ctis_search_node.py`：POST `/ctis-public-api/search`（关键字段 `searchCriteria.containAll`，非 keyword/sponsor——传错字段 HTTP 200 但 data 恒空）；实测 45 条。
  - 新 `nodes/ctis_scrape_details_node.py`：GET `/retrieve/{ctNumber}` 8 线程并行拉 events/results/documents（实测 13 字段）。
  - `search_node.py` / `scrape_details_node.py`：路由加 euctr/ctis 分支；**顺手清理 publisher_pdf 封存注释残留**（selfcheck A1 正则把注释行 `state.source=="publisher_pdf"` 误提取成分支 → 白名单差集 FAIL，删注释后 35/35 全绿）。
- **本地（发布包）**：
  - `search_eu_ctr.py` 121 行抓取器 → **薄壳**（`--source euctr` 转发 search_ictrp.py），旧逻辑保留为 `--local` 显式降级开关（迁移期防全断，实测 20 条）。
  - ⚠️ `--local` 已删除：抓取执行器上 Coze 后，本地不再保留 HTML 解析资产（符合 §20.14 "词表留本地、上移抓取执行器"）。
  - 新 `search_ctis.py` 薄壳（`--source ctis`）。
  - `search_ictrp.py`：API_SOURCE/RECORD_SOURCE + euctr/ctis；CLI `--source` choices 扩展；`_SOURCE_ID_RE` + euctr（WHO-COVERED 可 fallback；ctis 非 WHO 镜像**不**登记 fallback）。
  - `normalize.py`：ADAPTERS + `"CTIS": norm_euctr`（CTIS 字段与 EUCTR 同构）+ `--ctis` 入参。
  - `ct_registry.py`：`_run_tier2_fallback` spec 的 EUCTR 改 `is_endpoint=True`（走统一端点）+ 加 CTIS 行；新增 `--with-ctis` / `--ctis-keyword` CLI。
- **验证**：服务端三节点 mock-import 后**实测直连**（EU-CTR 20 条 / CTIS search 45 条 / CTIS detail 13 字段）；selfcheck 35/35；薄壳预览正确转发、`--local` 兜底 20 条；`_source_record_check` euctr 甄别单测通过（EUCTR 号三形态 True、ChiCTR/ctis 号 False）。
- ⚠️ Coze 端改动需**重新打包部署**到 Coze 控制台才生效；本地薄壳在部署前走 `--local`（euctr）或返回空（ctis 无本地旧实现）。**本地未发布**。

## Unreleased (2026-09-07 20:40) · WHO 兜底泛化到全部 5 个 WHO-COVERED 源

- **诉求（彤）**：CT.gov、EU-CTR、ChiCTR、ISRCTN、DRKS 五个 WHO 覆盖源，当"专门要查询某源但该源站点不通"时，自动将 WHO ICTRP 作为备用兜底，取回该源覆盖的试验（不中断、不空手）。
- **架构分层**：5 源分两组处理——ChiCTR/ISRCTN/DRKS 走统一端点（同 `search_ictrp.py`，判 `source_likely_down` 后同进程切 WHO）；CT.gov/EU-CTR 是 Tier1 本地直连（不经统一端点），兜底在编排层。
- **改动（`adapters/search_ictrp.py`）**：ChiCTR 专属 fallback 泛化为三源通用。
  - 新增 `_SOURCE_ID_RE`（`chictr`→ChiCTR 号 / `isrctn`→ISRCTN\d{8} / `drks`→DRKS\d+）+ `_source_record_check(rec, src)`（registry 字段 → 注册号字段 → raw 文本 三重甄别，按源参数化）。
  - 新增 `_fallback_who_for_source(payload, src, ...)`（原 `_fallback_who_for_chictr` 改名泛化，keyword 中→英本地化保留）；`run()` 触发条件从 `source == "chictr"` 放宽为 `source in _SOURCE_ID_RE`，信封字段随源名参数化（`<src>_records_via_who`、`fallback_reason=<src>_down`）。
  - 保留兼容别名 `_is_chictr_record` / `_fallback_who_for_chictr`（外部旧引用不失效）。
- **改动（`scripts/ct_registry.py`）**：Tier1 源（CT.gov / EU-CTR）站点不通兜底。
  - 新增 `_tier1_who_backfill(args, out_dir, norm_inputs, src_label, en_kw)`：WHO 主路径已成功（norm_inputs 已含 --ictrp）→ 镜像已覆盖，仅提示不重复发请求；否则补发一条 WHO 自由词检索到 `ictrp_backfill_<src>.json` 并并入归一化。无关键词/配额满/WHO 也失败均如实告警、不中断。
  - `_run_ctgov` 包 try/except `CalledProcessError`：CT.gov 官网不通时不再中断整个管线，自动走 WHO 兜底（修复原"无条件先行 + 站点挂即整体崩溃"缺陷）。
  - `_run_tier2_fallback` 的 EU-CTR 失败分支（rc≠0 非超时）补 `_tier1_who_backfill`；ISRCTN/DRKS/ChiCTR 走统一端点、adapter 内已有 fallback，编排层不重复。
- **验证**：`py_compile` 通过；`_source_record_check` 三源甄别单测 8/8；`_tier1_who_backfill` 三分支单测（已含 --ictrp 短路 / 无关键词 / 正常补发并入）；黑盒联测模拟 CT.gov 站点不通（rc=1）→ 触发 WARN + WHO 兜底成功并入 norm_inputs；双重失败（WHO 兜底也挂）时优雅降级、管线不中断。主路径 `--cond osimertinib` 预览/执行无回归。
- ⚠️ 本地改动**未发布**（发布需 ct-base §16 红线 + 用户授权）；本条目含 9/7 前两条（WAF 切换 + WHO 中英翻译）同属 v0.10.0 范围。

## Unreleased (2026-09-07 17:40) · WHO 中英自动翻译 + ChiCTR acw_sc__v2 纯 Python 破解

- **诉求 1（WHO 只支持英文 → 中文关键词自动翻译）**：实测 WHO ICTRP 端对中文关键词稳定返回 0（`光生物调节` 直发 0 条），英文正常（`photobiomodulation` 命中 974 条）。根因：WHO 端只按英文检索。在线翻译兜底（MyMemory）对医学术语不可靠（实测 `光生物调节`→`Photobioregulation`，WHO 命中 0；正确词 `photobiomodulation` 命中 974），故权威翻译必须进 curated term_map。
  - `adapters/search_ictrp.py` 新增 `_localize_who_keyword()` / `_localize_who_payload()`：对 `source=who` 的 payload（含 keyword 与 multi_keywords 两种形态）做中→英本地化——先走 `kw_localize` term_map（权威），词典 miss 的长尾词才落 `online_translate` 兜底，并如实标注 `source=term_map/online`。注入点两处：`run()` 入口（覆盖直接 `--source who --keyword 中文` 与 `ct_registry --with-ictrp` 主路径）、`_fallback_who_for_chictr` 构造 WHO payload 后（覆盖 ChiCTR→WHO 切换路径，其 keyword 是中文）。
  - 新增 CLI `--no-kw-localize`（默认开启，可关闭）。
  - `references/term_map.json` 增补 PBM 领域词条（ct-base 单源 → 双向同步，现 254 条）：`光生物调节→photobiomodulation (PBM)`、`经颅光生物调节→transcranial photobiomodulation (tPBM)`、`近红外光生物调节→near-infrared photobiomodulation`、`低强度激光治疗→low-level laser therapy (LLLT)`。
  - **验证**：`py_compile` 通过；隔离测 `_localize_who_keyword('光生物调节')→('photobiomodulation','term_map')`、复合短语「经颅光生物调节治疗儿童」拆词本地化、纯英文/`chictr` 源不误伤；联网实测 `--source who --keyword 光生物调节` → 自动转 `photobiomodulation` → WHO 命中 974 条（对比改前中文直发 0 条）。term_map 增补须同步 ct-base（本次已双写），发布前 `publish_preflight` 会校验一致性。
- **诉求 2（ChiCTR acw_sc__v2 技术解法，可改 Coze 代码）**：实测破解——ChiCTR 挑战页内联 `var arg1='<40 hex>'` + 混淆 JS，算法为 acw_sc__v2 标准结构：40 位位置重排表 + 固定 XOR 密钥 `3000176000856006061501533003690027800375`，**纯 Python 可确定性求解**（本地对拍 Node 执行挑战 JS 3/3 一致；带 cookie 重试即拿真实页）。同时发现旧节点两处失效根因：① 入口参数已改版——真实检索是 `searchproj.html?title=<kw>&page=N`，旧 `searchContent=`/`searchproj.aspx` 已失效（返回「最新注册」默认列表而非检索结果）；② 无需 Playwright 即可过 WAF。
  - `adapters/coze/src/graphs/nodes/chictr_search_node.py` **重写为 HTTP-first**：新增 `_acw_solve()`（纯 Python 求解）、`_is_challenge()`、`_http_session()`（curl_cffi 优先 TLS 指纹模拟 Chrome、回退 requests）、`_http_get()`（自动解挑战带 cookie 重试）、`_parse_results()`（新版 `<a class="tit1" title>` + `<td>` 行解析，兼容旧结构兜底）；`_do_search_http()` 为主通道，Playwright（`_do_search_playwright`）保留为整体失败/0 条时的降级兜底。
  - **验证**：`py_compile` 通过；mock Coze 依赖后真实 import 端到端跑通——识别挑战页提取 arg1 ✓、解析真实结果页 10 条（编号+标题准确）✓、真实会话 HTTP 自动解挑战后搜索「光生物调节」命中 10 条 ✓（页面不再含挑战标记）。
  - ⚠️ Coze 端改动需**重新打包部署**到 Coze 控制台才生效（`adapters/coze/coze_deploy_bundle_20260906_192243.zip` 为旧版）；本地侧 `search_chictr.py`（调统一端点）代码无需改，节点更新后自动受益。

## Unreleased (2026-09-07) · ChiCTR WAF 自动切换 WHO 线路专查 chictr 结果

- **诉求**：ChiCTR 直连被阿里云 WAF `acw_sc__v2` 拦截 / 后端节点故障（0 条 + `source_likely_down`，2026-09-06~09-07 持续）时，不再只能报「源不可用」，而是自动改用 WHO ICTRP 线路取回 ChiCTR 来源记录。
- **改动（`adapters/search_ictrp.py`）**：
  - `run()` 签名新增可选 `args` 形参；当 `source=chictr` 且对照探针判 `source_likely_down=True`、且未关 `--no-fallback-who` 时，调用新增 `_fallback_who_for_chictr()`。
  - 新增 `_fallback_who_for_chictr(payload, token, endpoint, timeout, source_label, args)`：用同一 keyword 发一次 WHO search，从返回记录中筛出 **ChiCTR 来源**（见 `_is_chictr_record` 三重兜底：registry 字段含 chictr / 注册号字段匹配 `ChiCTR(?:-[A-Za-z]{2,4})?-?\d{8,12}` 正则 / raw 文本含 ChiCTR 号），回填信封。
  - 命中后改写为：`records=chi`、`total=N`、`source_likely_down=False`、`fallback_used="who_ictrp"`、`fallback_reason="chictr_waf_down"`、`chictr_records_via_who=N`、`note=…`；WHO 线路也无 ChiCTR 记录则维持源不可用标记。
  - 新增 `_is_chictr_record(rec)` 与 `_CHICTR_ID_RE` 正则。
  - `main()` 三处 `run(...)` 调用点补传 `args=args`；新增 CLI `--no-fallback-who`（默认开启，可关闭回退）。
- **范围收敛**：仅对 `chictr` 源启用（用户诉求即 chictr）；`isrctn`/`drks` 仍走原「对照探针判故障」逻辑，不触发 WHO 回退（WHO 对二者镜像覆盖弱）。
- **复用既有链路**：回退走 `_run_once`（与正常检索同通道），不重复配额计数（usage_guard 仅在 `main()` 计一次）；临时文件落 `tempfile.gettempdir()` 用完即删。
- **验证**：`py_compile` 通过；隔离测 `_is_chictr_record` 对 `registry='ChiCTR'` / `Main ID='ChiCTR1900021234'` / `登记号='ChiCTR-TRC-14004108'` / raw 含 ChiCTR 号均判 True，对 `NCT...` / `DRKS...` / `ISRCTN...` 判 False。联网回退实测（2026-09-07，chictr 仍 down）：`run()` 正确判 `source_likely_down` → 触发 WHO 回退（`fallback_attempted=True`）；WHO 自身亦撞 `trialsearch.who.int` 导航超时时信封置 `fallback_who_status=who_error` 并追加 error_msg、维持源不可用标记、无崩溃；WHO 健康且命中 ChiCTR 记录时预期走 `fallback_used=who_ictrp` / `chictr_records_via_who=N` 分支（本机实测当日 WHO 亦偶发超时，未观测到非空命中样本，逻辑路径经单测覆盖）。**边界**：回退仅当 WHO ICTRP 线路本身健康才有效；若 WHO 同步故障则如实报 `who_error`，不伪装成功。

## Unreleased (2026-09-06 19:22) · 平台心跳/唤醒测试不落飞书审计

- **问题**：Coze 托管平台对端点的周期性心跳探活（payload 仅 `source`，如 `{"source": "chinadrugtrials"}`，不带 `query_origin`、无任何真实检索字段）经主图跑到 `feishu_write_node` 后照常落库，在飞书 searchlog 表产生 query_origin 为空的噪音行。
- **修复（coze 端 `adapters/coze/src/graphs/nodes/feishu_write_node.py`，仅飞书写入节点，检索照常跑）**：新增 `_is_keepalive_probe(state)`——`query_origin` 为空 **且** `querystr` 为 JSON 对象、键集 ⊆ `{"source"}`（心跳的极简形状）→ 判为平台心跳/唤醒测试，跳过写飞书（`feishu_error="skipped: keepalive_probe"`，主流程不受影响）。querystr 非 JSON / 非对象 / 空 / 含 source 之外任何键 → 一律不拦（保守，宁多写不漏暴露）。
- **判定边界（用户明确并实证，2026-09-06）**：专指 **coze 代码内部/平台发出的心跳唤醒**（用户实证其 querystr 非空、形如 `{"source": "chinadrugtrials"}`）；**外部入参不算**——合规客户端必然注入 `query_origin`（ct-base §8.6）不命中；外部入参即使漏注入 `query_origin`，querystr 也带 mode/keyword 等真实字段 → 照常落库，保留 v0.3.88"空值暴露不合规调用"的审计设计。
- **验证**：`py_compile` 通过；判定逻辑 10 类输入冒烟 ALL_PASS（心跳 `{"source":...}` 形状→跳过；带 qo 全字段合规入参→写；漏 qo 带 keyword 入参→写保留暴露；qs 空/非 JSON/含未知键→保守不拦）。重打包 `dist/coze_deploy_bundle_20260906_192243.zip`（52 条目，MD5 `65b671e284dbf27766e997c852da4053`，排除 `__pycache__`/`.venv`/`dist`/`CDE`/`srcX`/`assets`）。
- **生效边界**：需将新部署包上传 Coze 控制台重新部署后生效（上传需用户确认）。

## v0.9.3 (2026-09-06) · 新增本地 Web 检索工作台 workbench/ (v0.1.1, clinical-indigo)

- **新增 `workbench/` 目录**：本地可运行的单页检索控制台。前端 `index.html`（单文件、全内联零外链、SVG 图标、zh/en 97 键 1:1 对齐）+ 后端 `server.py`（stdlib `http.server` 编排 `scripts/ct_registry.py` 子进程，默认端口 8790，已加 CORS+PNA；端点 `/api/config /api/health /api/search /api/runs /api/task /api/download /api/run-delete /api/bug-report`）。
- **品牌统一 clinical-indigo**：与技能 `assets/icon.svg` 一致（`#1C6DD0`）；顶栏 logo 字节级内联真实 `icon.svg`（含 `logoShadow` 投影滤镜 + `translate(83,40)` 十字医学标记），去除此前自绘变体。
- **发布前修复（A/B/C/D/G 五项）**：① 配置漂移 `bugReport.enabled` 在 `workbench.config.json` 与 `#wb-config` 兜底双处统一为 `true`；② `server.py` 去掉硬编码绝对路径，改为 `_resolve_skill_dir()`（`CT_REGISTRY_SKILL` 环境变量 > 脚本父目录 > 向上回溯兜底）+ `PY=sys.executable`；③ logo 替换为真实 `icon.svg`、品牌切 clinical-indigo；④ 兜底 `modules` 补齐为 4 区（search-form/result/tracking/run-history）；⑤ `run_workbench.cmd` 改可移植 `python server.py`。
- **质量闸门**：ct-base §9 质量闸门 10/10 PASS；§16 三道闸门（secret_scan / shared_sync_check / spec_lint）对 workbench 目录无阻断；`py_compile` ✓ / 内联 JS `node --check` ✓ / 端点全 200（CORS+PNA 头齐全）✓；两段式反馈模态端到端可用。
- **已知非阻塞**：ct-registry 核心既有 `spec_lint` ERROR（F08 summary 超长 / F19 正文非英文）与本工作台无关，待另行整改。
- **启动方式**：`cd workbench && python server.py`（或双击 `run_workbench.cmd`），浏览器开 `http://127.0.0.1:8790/`。

## v0.9.3 (2026-09-06) · 修复 国家 列重复 (normalize 去重)

- **Bug**：检索结果 Excel 的「国家」列出现同一国名大量重复（如单格 106 个 "United States"），且概要国家分布被重复计数放大。
- **根因**：`normalize.py` 中 CT.gov 路径按**每个中心 location 各取一个国名**（第 89 行）、WHO 路径列表原样保留（542-545 行），均未去重；`export_xlsx.py` 的概要 `cc` 计数器又直接遍历该列表逐项 +1，双重放大。
- **修复**：在 `normalize.py` 两路提取后均用 `list(dict.fromkeys(...))` 按首次出现顺序去重；下游试验总表 / 原始明细 / 概要分布三处同步修正。
- **验证**：重跑 383 条归一化，记录内重复国家数 = 0；Excel 国家列重复 token = 0；单格最多国家由 106 降至 30（真实多国全球试验）；国家分布改为「每试验唯一国计数」（如 United States 120、China 185）。
- **验证（落地后）**：相对路径解析生效（`SKILL_DIR` 自动定位 `scripts/ct_registry.py`）；`/api/config` 返回 `clinical-indigo` + `bugReport.enabled=true` + 4 模块；`/` 首页 200 且含真实 logo；真实检索端到端 ok（CT.gov osimertinib）。
- **发布前规范整改（spec_lint ERROR 清零）**：F08 `summary` 精简为仅中文一句话；F19 `SKILL.md` 正文全文英文化（Features/Safety 中文段译英、Bug Reporting 用户触发短语英文化、Language 段 `中文指南`→`Chinese guide`）；F12 补齐 `.clawhubignore`（`workbench/runs/`、`workbench/__pycache__/` + `*.bak/*.zip/*.tar.gz/.idea/.vscode/_user_meta.json`）并与 `.gitignore` 同集；CHANGELOG 顶部版本头对齐 `0.9.3`（原 `Unreleased` → `v0.9.3`）。
- **WHO/ChiCTR 检索可靠性修复（2026-09-06 实测根因，源于 osimertinib NSCLC 检索「WHO 返回 0」）**：
  - **① WHO combined 模式合同守卫**：统一端点 WHO combined 仅认 `who_country/who_phase/who_date_*/who_sponsor/who_secondary_id/who_recruitment_status` 为「真筛选」，`who_condition/who_intervention/who_title` 不算；仅传后两者会触发后端内层校验错误（`combined 模式必须至少带一个筛选…`）返回 0 条。`search_ictrp._build_who_payload` 检测此情形自动降级为 search 自由词（实测 578 条），`ct_registry._who_cmd` 同步改为 disease+drug 默认走 search、仅显式给「真筛选」才用 combined（双层防御）。
  - **② 升级反馈环防数据丢失**：网关 `escalate_to_combined` 信号不再覆盖已取数据——`run()` 取到 >0 条即返回，避免升级失败把部分结果覆盖成 0；`_escalate_payload` 多词自由文本不再首空格臆测拆分（消除 `who_condition='non-small'` 类无效片段，整句作 `who_condition`）。
  - **③ 提交超时重试**：统一网关偶发抖动（提交偶卡死）导致误判 0；提交超时 30s→60s 且最多重试 3 次（指数退避）。
  - **④ 后端错误/空返回可见性**：`_parse_response` 提取 project_list 内层 `error` 提升到 `error_msg`；0 条+200+无错误标记 `empty_no_error`，使 ChiCTR 等「反复空返回（疑后端节点故障）」被编排层判失败并披露降级，而非静默当作「该源无结果」。
  - **效果**：修复前 WHO（combined+condition/intervention）返回 0、用户感知「WHO 不可用」；修复后同查询返回真实 osimertinib NSCLC 试验（如 Sac-TMT + Osimertinib 用于 III 期 EGFR 突变 NSCLC），WHO 全球覆盖恢复。
  - **⑤ `_control_probe` 对照探针 keyword 字段 bug 修复（2026-09-06 接力）**：探针 `_control_probe` 原把整个 `CONTROL_TERMS` 列表（如 `["二甲双胍","肺癌","高血压","aspirin"]`）整体塞进 `keyword` 字段（应为单字符串），端点收 dict 而非 str、POST 异常被 `except` 吞掉 → 探针永远返回 `None`、节点故障永远判不出。`search_ictrp._control_probe` 改为逐个对照词发同步请求、任一有数据即判定非故障、全空才返回 `True`→标 `source_likely_down=True`。`run()` 的触发条件本已正确（`payload.get("source") in CONTROL_TERMS`），无需改。
  - **⑤b `_control_probe` 真根因修复（2026-09-06 16:29 复测发现）**：模块**未导入 `requests`**（本模块走 urllib/共享通道），探针内 `requests.post` 抛 `NameError` 被 `except Exception: return None` 吞掉 → 探针仍永远返回 `None`（此前「触发条件本已正确」的判断有误，keyword 修复只是必要非充分）。修复：函数内局部 `import requests as _requests`；同时 `kws = ctrl if isinstance(ctrl,(list,tuple)) else [ctrl]` 修正 `ctrl[:2]` 对字符串按字符切分的隐患（「肺癌」→「肺」「癌」单字查询）。**验证**：探针隔离测试返回 `True`；完整 chictr 检索 `osimertinib` → `[SOURCE-DOWN]` 打印、`source_likely_down=True`、`error_msg` 明确「对照词（肺癌）亦返回 0+无错误，判定为源不可用而非真实零结果，查中国用 CDE」。当日复测 ChiCTR 仍坏（`肺/癌/肺癌/diabetes` 全 0）。
  - **参数带入复核（飞书后台实证）**：用户提供的飞书后台请求体 `{"keyword":"osimertinib","mode":"search","params":{"user_language":"en"},"skill_version":"0.9.3","source":"chictr"}` 与脚本 `_build_simple_payload`+`_attach_coze_contract` 构造的 payload 逐字段一致（`keyword`/`mode`/`source`/`skill_version`/`params` 均正确）；本地 `print_preview`(不加 `--run`) 复现同一 payload。后台另有一条 `{"source":"chictr"}` 仅含 source，是 vibeflow 初始化节点的**中间态快照**（只设 source），非最终请求体，**不代表参数丢失**。ChiCTR 返回 0 系后端节点故障（6 词对照实验含 metformin/肺癌/高血压/aspirin 全空、无 error），非参数问题。
  - **完整日志复核（用户提供的 `CTDB_searchlog (2).xlsx`，34 行）**：逐行验证后确认——① **ChiCTR 主查询参数全部正确带入**：7 条带词 chictr 请求（`keyword`=`osimertinib`/`奥希替尼`、`mode`=`search`、`source`=`chictr`）逐字段正常，非参数问题；② **裸 `{"source":"chictr"}` 共 12 次**（14:19–14:48，runtime 15.7–16.0s），是框架对 source 的**周期性探活请求**（只带 source 不带 query，端点正常响应回空），非主查询、不影响数据；③ **WHO combined 根因获日志实证**：带 `who_recruitment_status='Recruiting'`（真筛选）的 combined 跑满 164.7s，而只带 `who_condition`+`who_intervention` 的 combined **瞬时返回 0.009/0.005/0.036s**——后端合同校验失败立即回空，正是「WHO 返回 0」的根因；④ **可观测性盲区（重要）**：飞书后台 `resultstr` 字段**只记录 `runtime_sec`，不记录 `total_count`/返回条数/错误**，故平台侧**无法从日志区分「ChiCTR 节点故障返回的空」与「某词真无结果」**——所有 source 空返回在日志里都长一样（"请求成功、耗时 15.7s"）。本地落盘 JSON 已通过 `_control_probe` 标 `source_likely_down` 弥补此盲区，但平台日志格式非本技能可控。

## Unreleased (2026-09-03) · 对齐 ct-base coze_io_contract §1（入参信封）+ §2（飞书存储）

- **背景**：按 ct-base `references/coze_io_contract.md` 统一契约，所有 ct-* 技能调 coze 端点（不分计算/检索端点）一律遵守。ct-registry 此前仅 `query_origin`（ct-base §8.6）合规，`skill_version` / `user_language` 缺失、`runtime_sec` 未实现。
- **客户端 `adapters/search_ictrp.py`（§1.1 / §1.2）**：
  - 新增 `_skill_version()`（读 `SKILL.md` frontmatter `version:`，失败回退 `"0.9.3"`）。
  - 新增 `_attach_coze_contract(payload, args)`：出站 payload 注入顶层 `skill_version` + `params.user_language`（由 `scripts/i18n.resolve_user_language` 三级判定，按用户输入文本 zh/en）；幂等、不破坏既有检索字段。
  - `build_payload` 四个分支（detail / who / cde / simple）统一包裹 `_attach_coze_contract`，覆盖全部 `source`（who / chinadrugtrials / isrctn / drks / chictr）。
  - 导入兜底：`scripts/` 无 `__init__.py`，启动时把技能根目录加入 `sys.path` 再 `from scripts.i18n import resolve_user_language`。
- **§2.1（skill_version → 飞书 querystr）**：随客户端 `querystr` 序列化（`_run_once` L697-700，序列化 payload 除 querystr/query_origin）自动带出 `skill_version` → coze 端 `feishu_write_node` 写入飞书 `querystr` 列，满足契约。
- **coze 服务端参考 `adapters/coze/src/`（§2.2，2026-09-06 已修复并重新部署 `coze_deploy_bundle.zip` + 同步 `srcX/`）**：
  - `main.py` `/run` · `/stream_run` · `/node_run` 三入口收到 `request.json()` 即刻 `payload["received_at"] = time.time()`（此前仅 `/run`+`/stream_run` 两处，漏了 `/node_run`）。
  - `state.py` `GlobalState` / `GraphInput` / `FeishuWriteInput` 均新增 optional `received_at: float`，经状态透传至飞书节点。
  - 🔴 **`resultstr` 硬编码空串 bug 修复（根因）**：原 `feishu_write_node` 第 88 行 `record["fields"]["resultstr"] = ""` 写死空串——节点只拿到 `querystr`/`query_origin`，拿不到检索结果，飞书 `resultstr` 列永远空。修复后新增 `build_resultstr(state)`：写入**完整响应**（`total_count` / `error_msg` / `log` / `project_list`（>5KB 自动截断标记防单元格超限，2026-09-06 16:27 用户指定由 50KB 收紧）/ `scraped_data_json`（>50KB 截断））+ 顶层 `runtime_sec = round(time.time() - received_at, 3)`（仅当 `received_at` 非 None）；🔴 只进飞书日志、不出 coze 响应（§2.2 红线）。向后兼容：`received_at=None`（直连测试）时 `resultstr` 不含 `runtime_sec`，与历史格式逐字节一致。
  - **平台探活请求（心跳）处理**：飞书后台所见裸 `{"source":"chictr"}` 共 12 次（14:19–14:48，runtime ~16s）是 **Coze/飞书托管层对各注册 source 的周期性可达性探测（入站）**，非本工作流生成、亦非参数丢失；我们的代码原本会照常路由→打后端→返 0→还写飞书，既浪费 ~16s/次又污染审计表。修复双层防御：① `search_node` 入口用 `sources.is_health_probe_request()` 判定「仅 source、无真实检索参数」→ 短路返回（不触发后端检索）；② `feishu_write_node` 同步跳过落库（`feishu_error="skipped: health_probe"`）。**该探活请求无法从本工作流代码侧"删除"**（属托管平台行为），但已做到"瞬时返回 + 不污染日志"；若需彻底关停，须在 Coze/飞书控制台侧配置健康检查策略。
- **验证**：客户端 `py_compile` + 离线行为测试（4 个 source 路径均带出 `skill_version="0.9.3"`、`params.user_language` 按输入 zh/en 正确；`querystr` 序列化含 `skill_version`；幂等）；服务端三文件 `py_compile` 通过 + `runtime_sec` 计算逻辑单元抽查（round 3 位、`received_at=None` 留空）。

## Unreleased (2026-09-06 17:18) · WHO 抓取三层优化（A 切片累积 / B 主库直连 / C 端点断点翻页）

- **背景（当日实测定性）**：统一网关 WHO search 单次仅回 ~10 条——根因不是翻页缺失（服务端 `_do_who_search` 本会翻页），而是 `total_records > WHO_RESULT_CEILING(400)` 时**早退只回首页 + escalate 信号**；combined 需真筛选且 ~165s；网关 300s 硬墙。WHO 官方 `trialsearch.who.int` 全链路 200 无反爬。
- **A · `adapters/search_who_sliced.py`（新增）**：切片累积——宽查询切成 N 个窄子查询（`--by-registry` 按 WHO 一级注册库前缀 EUCTR/JPRN/CTRI/NTR/…、`--by-year` 按年份、或 `--slices` 自定义），逐片子进程复用 `search_ictrp.py`（继承降级守卫/超时重试/探针），按 Main ID 客户端合并去重，`--max-slices`（默认 5）控配额，输出含 per-slice 统计。
- **B · `adapters/search_euctr_direct.py`（新增）**：EU CTR 主库直连——`/ctr-search/search?query=` 收集 EudraCT 链接 → 国家版详情页（ES 优先，GB 停更自动跳过换国）按 label 解析（Full title/Sponsor/Trial status/EudraCT number 等），1.5s 限频 + EudraCT 本地缓存。**决策记录**：WHO `Trial2.aspx` 实测为纯 postback 壳（无数据无 JS 端点）不可纯 HTTP 直抓；ISRCTN 详情为 JS 壳（1.2KB）——两者放弃，EUCTR 实测直连完全可用（osimertinib 20 条/页、详情含 AstraZeneca/Novartis 等申办方）。
- **C · coze 服务端 `who_search_node.py` + `state.py`（已重打包部署 `coze_deploy_bundle.zip` + `srcX/`，待上传 Coze 控制台生效）**：
  - `SearchNodeInput`/`GlobalState` 新增 `page_start`（断点续抓起始页）与 `paginate_all`（显式翻页开关）。
  - `_do_who_search`：①`paginate_all=True` 时 `total>400` 不再早退，在 `WHO_NODE_BUDGET(270s)` 预算内从 `page_start` 尽力翻页，`is_partial` 标记缺口；②`page_start>1` 先 `__doPostBack` 跳页再续翻；③输出新增 `page_start/page_end/next_page_start`，客户端据 `next_page_start` 续抓累积；④默认不传时行为与历史逐字节兼容。
  - 客户端 `search_ictrp.py` 配套：`--page-start` / `--paginate-all` 透传进 payload（who search 分支）。
- **验证**：5 文件 `py_compile` 全过；客户端 payload preview 确认 `page_start/paginate_all/max_pages` 正确入包；内网文件服务器部署后 grep 校验 4 项（page_start 参数/paginate_all 守卫/next_page_start/state 字段）全 FOUND。A/B 层 live 测试：EUCTR 直连 3/3 成功；切片累积测试运行中（见工作区 `who_sliced_test.log`）。
- **遗留**：①C 需用户重新上传 Coze 控制台后才实际生效；②EUCTR 详情 `试验状态` 字段标签变体（部分国家版未捕获）待补；③A 层合并结果是样本（每片 10 条）非全量，全量仍需 C 层续抓循环。
- **A 层 live 测试补记（2026-09-06 17:35）**：①按注册库前缀切片（`osimertinib EUCTR` 等）实测**不可行**——WHO 自由词不索引 Main ID（JPRN 片干净 0 条，非故障）；②正确切片轴为 **combined + `who_date_*` 年份桶**（真筛选，桶内服务端可完整翻页）；③但当前统一网关对 WHO combined 严重不稳（提交连续抖动重试 + 600s 轮询超时），日期桶单测未通过（`who_yearbucket_test.log`）——属端点当日故障，非代码问题，网关恢复后 A 的日期桶策略可用；④单片超时默认已提至 240s（120s 会误判）。
- **复查修复（2026-09-06 17:45）**：`_do_who_search` 断点续抓补 2 个边界守卫——①跳页到 `page_start` 返回空时**回退从第 1 页重抓**（原实现会带着第 1 页数据冒充第 N 页，客户端合并错位）；②`page_start > total_pages` 时返回**空集 + `page_end=None` + `next_page_start=None`**（原实现会静默返回第 1 页数据且页码区间越界）。修复后重编译 + 重打包（287,776B），SHA256 三方（本地/zip/srcX）逐一核对一致（注意：PowerShell 5.1 读无 BOM UTF-8 中文会乱码，grep 校验需 `-Encoding UTF8`，此前一次 False 为读取误报）。

## Unreleased (2026-09-01) · nmpa_pv 始终返回 0 归因 + 数据源改指 CDR-ADR + WAF 检测/诊断加固

- **根因（主因·已修）数据源 URL 失效**：原 `BASE_URL = https://www.nmpa.gov.cn/xxgk/yjjsh/ypblfytb/` 已于 2026 年**改版迁移**——真人浏览器访问提示「页面有更新」并跳回首页，脚本客户端直连返回 **HTTP 412 WAF**。服务端无头浏览器拿到的是首页空壳 → 解析 0 锚点 → 被旧逻辑**静默当成「真 0 条」**（假阴性）。原本机只看到 412 误把 WAF 当主因，用户真人浏览器反馈「跳首页」才定位到 URL 迁移。
- **修复**：`BASE_URL` 改指 **国家药监局药品评价中心（CDR-ADR）「安全警示 > 药品」栏目** `https://www.cdr-adr.org.cn/sy_aqjs1/yp`（实测 HTTP 200、含真实内容、标题带药名）。该站**无 nmpa.gov.cn 式强 WAF**，服务端无头浏览器可直接抓取。新增 `SUB_LISTS`（信息通报历史 / 药物警戒快讯 / 公告通告三个子栏目完整列表）与 `SEED_URLS`，`_do_scrape` 改为遍历种子页而非失效的 `index_N.html` 分页。
- **WAF 检测** `_detect_waf(html, title)`：识别空标题 + 随机 id 的 `<meta>` 挑战标记、常见挑战文案（访问验证/人机验证/captcha/…）、WAF 厂商签名（incapsula/cloudflare/yundun/…）。命中即标记 `status="blocked"` 并明确告警「请勿把 0 当真 0」。
- **页面级诊断** `_gather_diag()`：每页收集 `page_title / html_len / total_anchors / html_anchors / waf_detected / sample_hrefs / sample_anchor_texts`，打日志并随响应返回，部署后无需翻服务端日志即可定位真因。
- **等待策略**：`wait_until="commit"` → `wait_until="load"` + 等待列表锚点 `a[href$='.html']` 出现，兼容 JS 渲染列表。
- **结果状态字段**：输出 JSON 新增 `status`（`ok`/`blocked`/`empty_list`/`no_match`/`error`）与 `diagnostics`；`blocked` 时带 `error: "WAF_BLOCKED: …"`。ct-safety 客户端 `nmpa_coze.py` 解析 `projects`/`tier`，新增键不影响既有契约。
- **解析健壮性**：`<a>` 标题文本为空时回退读 `title` 属性；`.html` 过滤放宽含 `.shtml`。
- **验证**：`py_compile` 通过；用真实 CDR-ADR 页面离线复刻 `_parse_list` 逻辑，确认相对链接 `./202006/t20200615_47501.html` 经 `urljoin` 正确拼为绝对地址、药名过滤生效（甲氨蝶呤→第75期、含钆对比剂→第76期、阿莫西林→0 为正确结果）。重建部署包 `adapters/coze/coze_deploy_bundle.zip`（MD5 `d5e293cf5dd4b87fb7e618e3bc1ab01d`，48 文件，排除 `CDE/`/`_archive_20260820/`/`__pycache__`）。**待用户重新上传 Coze 控制台后，对 `甲氨蝶呤` 等应返回真实命中；`阿莫西林` 等常用药返回 0 属正确（未进入信息通报，可查同栏修订说明书公告/警戒快讯）。**

## v0.9.3 (2026-08-29) · 去重桥接可审计化：每条记录输出 dedup_reason / dedup_tier

- **来源**：ct-update 2026-08-29 周检 P1-F「去重桥接加固」。动机：非英文试验（尤其 CDE/ChiCTR）依赖自由文本里的注册号做跨库桥接，而聚合层此前只输出 `dedup_group_id`，**误并（false positive）与正确合并在结果里无法区分**，漏并同样无迹可查。
- **`scripts/aggregate.py` `dedup()`**：新增合并证据链。每次真正折叠两个簇的 `union()` 都登记 `(i, j, tier, evidence)`；分组后为每条记录写两个增量字段：
  - `dedup_reason` — 人类可读证据，如 `tier1_id_bridge (shared registry id CHICTR2000029999) <-> CTGOV:NCT01234567`、`tier2_fuzzy (title match + sponsor/start_year=2021/intervention) <-> CTRI:CTRI/2021/05/033333`；单例为 `singleton: no cross-registry match`。
  - `dedup_tier` — `tier1_id_bridge` / `tier2_fuzzy` / `transitive` / `none`（可组合，如 `tier1_id_bridge+tier2_fuzzy`）。
  - **`transitive` 档的必要性**：并查集是传递闭包，A-B、B-C 成立时 A 与 C 同组但无直接边；这类记录标 `transitive` 并列出同组对端，避免"无证据"被误读为 bug。
- **`dedup_summary` 新增**：`merge_edges`（实际合并边数）、`dedup_tier_breakdown`（各档记录数）。
- **`scripts/report.py`**：报告的跨库去重段落输出合并依据分布，并对 `tier2_fuzzy` 单独告警——该档仅凭"标题 + 单一佐证（申办方/起始年/干预之一）"即合并，误并风险最高，提示抽查 `dedup_reason`。
- **兼容性**：纯本地、零联网；仅增量追加字段，`dedup_group_id` / `primary_source` / `registry_id_norm` / `secondary_ids` 与 `dedup_summary` 原有键全部保持不变（冒烟测试含向后兼容断言）。
- **验证**：`py_compile` aggregate.py + report.py 通过；17 项断言全绿的冒烟测试覆盖四条路径——Tier1 注册号桥接（CT.gov↔ChiCTR 中英文对照）、Tier2 模糊匹配（CTRI↔CT.gov 无共享 ID）、singleton、原有字段向后兼容。

## v0.9.2 (2026-08-27) · 凭据模块改名 config/keys.py → adapters/endpoint_token.py

- **问题**：`config/keys.py` 的命名/位置与已发布技能（ct-base `adapters/coze/src/endpoint_token.py`、ct-advisor `adapters/coze_token_embedded.py`）不一致；`config/` 目录本应只放 JSON 配置，混入 `.py` 凭据模块易触发误读/扫描告警。
- **改名**：`config/keys.py` → `adapters/endpoint_token.py`；import 由 `from config.keys import ...` 改为 `from endpoint_token import ...`（同目录兄弟模块，机制与既有 `from extsvc_client import ...` 一致）。
- **同步**：README / README_zh-CN / SKILL.md / `adapters/coze/CDE/cde_workflow.md` 及代码内注释的 `config/keys.py` 引用全部更新；`config/ictrp.dat` 等历史引用保留不动。
- **验证**：py_compile 全过；`search_ictrp.py` 离线 preview 正常；`scripts/publish_preflight.py` 闸门全绿（exit 0）。

## v0.9.1 (2026-08-27) · 飞书表 querystr 去重 query_origin（ct-base §8.6）

- **问题**：飞书多维表格的 `querystr` 列重复打包了 `query_origin` 键值，而 `query_origin` 已由独立列保存（ct-base §8.6 客户端注入、coze 端透传写入），属冗余。
- **coze 端 `adapters/coze/src/graphs/nodes/feishu_write_node.py`**：新增 `_strip_query_origin()`，在飞书写入前从 `querystr` 移除 `query_origin` 键（仅当 querystr 为含该键的 JSON 对象时剥离；非 JSON / 非对象 / 解析失败一律原样返回，不破坏既有内容）。
- **调用方 `adapters/search_ictrp.py`**：序列化 `querystr` 时同步排除 `query_origin`（与 `querystr` 自身一同从序列化集合剔除），从源头不再发出冗余键值。
- **验证**：py_compile 两文件均通过；`_strip_query_origin` 对「含 query_origin JSON / 不含 / 非 JSON / 空串」四类输入行为均正确。

## v0.9.0 (2026-08-22) — 增加 bug report 功能（ct-base §20.3 接入补齐）

- **🔴 bugreport 接入补齐（发布前检查发现缺漏）**：
  - `adapters/bug_report.py` 升级为含历史回执的当前版本（补齐 `confirm_thanks`/`build_followup`/`parse_history` + `_MSGS` thank/done/pending 双语文案 + `send_to_endpoint` 透传 `history`）；此前为旧副本，缺 §20.3.7 历史回执。
  - `config/config.json` `auto_approve_endpoints` 补齐统一 bug-report 端点 `https://ct-bugreport.coze.site/run`（此前仅含计算端点，违反 §20.3.5）。
  - `README.md` Safety 段新增 bug-report 端点出站披露（§16.6，此前缺失）。
  - `SKILL.md` Bug Reporting 段补齐「主动触发」显式请求路径（§20.3.1）+ 发送后历史回执（§20.3.7），此前仅强信号路径、无回执约定。
- 三道发布闸门：publish_secret_scan（0 P0/0 P1）、shared_sync_check（无漂移）、clawhub_security_audit（仅预已发布技能的既有审计项，无新增阻断）。

## v0.3.88 (2026-08-20) · query_origin 生成主体红线落地（ct-base §8.6 更新）

- **背景**：飞书表成对验证发现 coze 端 `query_origin` 跨窗口漂移（08-14 `ad2d1f` → 08-20 `086aaa`）——根因是 coze 端兜底生成 `sha256(容器 hostname)`，容器重建即变，且标识的是服务器而非来源机器。ct-base §8.6 据此明确红线：**`query_origin` 必须由技能安装设备（客户端）生成并携带，禁止由 Coze 服务器生成**。
- **调用方 `adapters/search_ictrp.py`**：新增 `_compute_query_origin()`（`sha256(本机 hostname)`）；参数解析后**未显式传 `--query-origin` 时自动计算注入**（4 处透传逻辑原本就存在，此前因参数恒为 None 从未生效）；`--query-origin` help 文案同步（"缺失时 Coze 自动生成"→"必须由本机生成，未传自动注入"）。
- **coze 端（`adapters/coze/src/` 本地基准，待重新部署生效）**：`search_node` / `who_search_node` / `scrape_details_node` 移除"缺失时自动生成"兜底，改为**缺来源告警 + 保留空值**（飞书表该行 query_origin 为空，暴露不合规调用）；`state.py` 8 处 `query_origin` 字段描述全部对齐新语义；`_compute_query_origin` 定义保留仅供客户端参照。
- **验证**：本机注入值 `sha256:b8cae3d4...` → 真实出站回传**完全一致**（coze 端"客户端已传则保留"路径本就存在，无需改）；list/detail 双模式 preview 均自动注入；coze 端 py_compile 全过、无 `state.query_origin = _compute_query_origin` 残留。
- **生效边界**：本地调用方改动**立即生效**（同一技能安装设备所有调用 query_origin 恒定，不再漂移）；coze 端兜底移除需**重新部署工作流**后生效（部署前线上仍兜底生成，但正常路径客户端已注入，无影响）。

## v0.3.87 (2026-08-14) · 调用方流式 SSE 解析落地 + 死代码清理（发布前整改）

- **流式调用改造（调用方 `adapters/search_ictrp.py`）**：
  - 根因：上一轮 `_parse_sse` 仅设计方案、未对真实 SSE 验证，假设结果在终帧 `data.data`；但真实 coze 流 `workflow_end.output` 恒为 `{}`、结果在主节点 `search_node`/`scrape_details_node` 的 `node_end.output`，且**普通流式不发 node 帧**，必须带 `x-workflow-stream-mode: debug` 头。
  - 落地 `_parse_sse`（从主节点 `node_end.output` 取回传参数 project_list/total_count/log，忽略恒空终帧，抽 error_msg）+ `_try_stream`（强制 debug 头、取不到自动回退同步 `/run`）；`_run_once` 流式优先；`run()` 与全部调用点透传 `use_stream`；新增 `--no-stream` 开关。
  - 验证：CDE「肺癌」流式取到 **1308 条**真实记录；`--no-stream` 同步回归 HTTP 200 正常。coze 端零改动。
- **死代码清理（`config/keys.py`）**：删除 0 调用的历史遗留 `store_token()`（唯一可写 `.dat` 的路径，曾触发 §16.0 `never written` 注释矛盾）+ `config_path()`；`get_secret` 对 `LEGACY_DAT_PATH` 的只读回退保留。
- **发布前检查（ct-base §16）整改**：补 `.gitignore`/`.clawhubignore` 裸 `tests/`+`scripts/tests/` 排除（防测试源码随 ClawHub 包泄漏）；README 补反幻觉信任段（§13.3）与英文版耗时/量上限警告（§13.7）；SKILL.md 正文中文「检索耗时提示」块英文化（§16.2）；**§16.9 出站调用归专用目录**：11 个出站脚本从 `scripts/` 迁至新建 `adapters/`，`ct_registry.py` 子进程路径改指 `ADAPTERS_DIR`，纯本地脚本（normalize/aggregate/report/parse_cde/usage_guard/i18n）留 `scripts/`；本条目对齐 version 0.3.87；§16.0 审计 2 个 STILL_PRESENT 中 `never written` 项已实质解决。
- 仍全部本地改动，未发布（推送 / 上传 Coze 平台需用户确认）。

## v0.3.86 (2026-08-14) · WHO 检索首屏大结果集探测 + 升级阶梯（抗封优化落地）

- **背景**：用户确认"尽量走高级检索"= 大结果集探测拦截；`WHO_RESULT_CEILING` 定为 **400**。coze 端 + 调用方（`search_ictrp.py`）一起优化。
- **coze 端 `coze/src_backup/src/graphs/nodes/who_search_node.py`**：
  - 新增常量 `WHO_RESULT_CEILING = 400`（约 40 页，仍在 `max_pages=50` 内）。
  - `_do_who_search`（basic）与 `_do_who_advanced_search`（combined）首屏读 `total_records` 后接入拦截：超 400 **不翻页**，回传 `escalate_to_combined` / `escalate_to_advanced` 信号 + `is_partial=True` + 首屏占位数据（约 10 条）。
  - 中档（100–400）允许翻页但置 `is_partial` 标记。
  - `who_search_node` 主节点把信号透传进 `project_list` 的 `output_data`（随 JSON 字符串回传，无需改 state 模型字段）。
- **调用方 `scripts/search_ictrp.py`**：
  - `_parse_response` 从 `project_list` 内层 `inner` 透传 `escalate_to_combined` / `escalate_to_advanced` / `large_result_set` / `is_partial` 到 `out_obj`。
  - `run()` 重构为升级反馈环（外层循环，最多 `MAX_WHO_ESCALATION=2` 次重发）：收 `escalate_to_combined` → 调 `_escalate_payload` 升 combined（已有 `who_*` 直接升；含分隔符 keyword 粗拆 `who_condition`/`who_intervention`）；收 `escalate_to_advanced` → 加 `who_recruitment_status=Recruiting` 升 advanced 终态；仍超限则终止、保留截断结果交上层/用户收窄。
  - 新增 `_run_once` / `_escalate_payload` / `_read_out_json` 辅助函数；顶部加 `import re`。
- **架构边界**：粗粒度 keyword 拆词为尽力而为，精准拆分仍由上层 `ct_registry.py` 完成（`search_ictrp` 无 LLM）；basic 单 keyword 无分隔符时返回 `None` 交上层，不猜词丢结果。
- **验证**：两端 `ast.parse` 语法校验 ✓；`_escalate_payload` 升级逻辑单测（中文/英文空格拆、无分隔→`None`、combined→advanced 加 Recruiting）全过 ✓。
- **文档**：`coze/WHO_SEARCH_OPTIMIZATION.md` §0.6/§3.2/§3.9 标注已落地。
- 仍全部本地改动，未发布（上传 Coze 平台 / 推送需用户确认）。

## v0.3.85 (2026-08-13) · CT.gov v2 检索 P2 补齐 + 真实联网回归（全套参数覆盖完成）

- **背景**：用户指出"P0 1 2 全部依次实现"含 P2（上轮只做到 P1），本轮补完 P2 四项。
- **`scripts/search_ctgov.py` 新增（P2）**：
  - `--geo`：`filter.geo` 地理距离，接受 `distance(lat,lon,dist[km|mi])` 或裸 `lat,lon,dist`（自动包装），并强制官方半径范围 **1-500 mi / 1-805 km**（超范围即报错；`_normalize_geo` 幂等，`_build_params` 编程调用亦兜底）。
  - `--patient`（`query.patient` 患者友好搜索）。
  - postFilter.* 四参数：`--post-status`/`--post-ids`/`--post-geo`/`--post-adv`（语义同 filter.* 但不影响相关性排序）。
- **真实联网回归（用户提示"现在应该是真实环境了"）**：沙箱 urllib 直连 clinicaltrials.gov 成功，全参数实测通过——P0 组合（phase+多值状态+sort+日期）5/5 字段级命中、`--ids` 精确 2/2、`--geo` 上海 50km、`--patient`、postFilter 3/3、`--adv` 3/3、`--fast` 分页正常。
- **发现并修正**：`query.rmtln` 为 **v1 遗留参数、v2 API 已移除**（真实请求 HTTP 400，与 `query.term` 对照确认）→ 移除 `--rmtln`，文档注明替代（`--query`/`--adv`）。
- **至此官方 v2 `/studies` 全参数覆盖**：10 个 query.*（cond/intr/spons/term/titles/outc/lead/id/locn/patient）+ 5 个 filter.*（overallStatus/ids/geo/advanced + postFilter 同构）+ sort + fields + pageSize/pageToken/countTotal。
- **验证**：py_compile ✓；断言（P2 四项 + 范围拦截 + P0/P1 回归）全过 ✓；真实联网回归全参数 ✓。
- **文档**：README.md / README_zh-CN.md 参数说明补 P2、移除 rmtln；`CTGOV_V2_PARAM_AUDIT.md` 标记 P0+P1+P2 全落地 + 真实回归记录。
- 仍全部本地改动，未发布。

## v0.3.84 (2026-08-13) · CT.gov v2 高级检索完整支持（P0+P1 落地，主功能强化）

- **背景**：用户委托审计 CT.gov 检索能力（`CTGOV_V2_PARAM_AUDIT.md`），结论 = 原 `search_ctgov.py` 仅覆盖 3/9 `query.*` + 1/5 `filter.*`；本次将 P0+P1 全部落地。
- **`scripts/search_ctgov.py` 重写（纯参数层扩展，向后兼容）**：
  - `query.*` 补齐：新增 `--query`（query.term，支持 AREA[]）、`--titles`、`--outc`、`--lead`、`--id`、`--locn`。
  - `filter.advanced`：新增 `--adv` 原始表达式透传 + 便捷参数 `--phase`/`--study-type`/`--age-group`/`--sex`/`--has-results`（自动组装 AREA[] 表达式，多值 `(A OR B)`，与 `--adv` 做 `(<便捷>) AND (<--adv>)` 合并）。
  - 服务端日期区间：`--first-post-*`/`--last-update-*`/`--start-date-*`/`--primary-completion-*`/`--completion-*`（since/until → `AREA[Field]RANGE[since,until]`，缺省 MIN/MAX）；`--date-after` 旧本地后过滤保留。
  - 多值：`--status`/`--ids` 逗号多值 → 管道分隔；`--sort`（≤2 个，`field[:asc|:desc]`/`@relevance`）→ 管道数组；`--fields` 暴露。
  - 校验：枚举白名单（phase/study-type/age-group/sex）、日期 YYYY-MM-DD 严格校验、sort 数量与格式——非法即 argparse 报错。
- **验证**：py_compile ✓；离线参数组装断言 13/13 ✓；CLI PREVIEW URL 构造 + 非法参数拦截 ✓；真实联网回归待部署环境。
- **文档**：README.md / README_zh-CN.md 补 CT.gov 高级检索示例与参数说明；`CTGOV_V2_PARAM_AUDIT.md` 标记 P0+P1 已落地（P2 于 v0.3.85 补齐）。
- 仍全部本地改动，未发布。

## v0.3.83 (2026-08-13) · Keyword gate 非交互防呆 + 文档修复

- **新增 `CTGOV_V2_PARAM_AUDIT.md`（CT.gov v2 检索能力审计，用户委托）**：对照 OpenAPI 规范 / Search Areas / Expert Search 语法核实，结论 = 本地 `search_ctgov.py` 仅覆盖 3/9 `query.*` + 1/5 `filter.*`（且状态仅单值），**`filter.advanced`/sort/服务端日期区间/多值状态全缺**；给出 P0–P2 缺口分级与 CLI 透传扩展设计（纯参数层，normalize 管线零影响）。


- **根因（实测复盘）**：`_kw_system_gate()` 未确认时无条件 `sys.exit(0)`，不检查 stdin TTY、不理会 `--auto-confirm`（它只管结果条数确认）——agent 非交互照抄 SKILL.md 示例命令必静默退出、零产物。
- **① 代码防呆（`scripts/ct_registry.py`）**：gate 菜单分支前加 `if not sys.stdin.isatty():` → 非 TTY 时自动 adopt 已展开词集并继续（打印提示），交互模式行为不变；显式 `--no-expand` / `--kw-en|--kw-zh` / `--kw-adopt` 仍优先。验证：`echo "" | ct_registry.py --cond ... ` 非交互直达 PREVIEW ✓（不再 kw_gate.stopped）。
- **② SKILL.md**：one-shot 示例命令补 `--no-expand` + 注释"agent/非交互必须带 --no-expand / --kw-en / --kw-zh / --kw-adopt"。
- **③ references/search_procedure.md**：Keyword gate 小节新增 🔴 非交互警告（四选一参数 + 解释 --auto-confirm 无效范围）。
- **④ i18n 缺失修复（xlsx 键名问题）**：`scripts/i18n_messages.json` 缺失导致 `t()` 全部回退键名——Excel 交付物 sheet/单元格标题显示为 `xlsx.sheet.*` / `xlsx.kpi.*` 等键名而非文本。已从 ct-base 底座复制主文件（31,658 B）补齐；验证 `t("xlsx.sheet.readme")→"说明"`、重导出 sheet 名=「说明/检索结果概要/试验总表/原始明细」✓。
- **⑤ 多源遍历优化（Coze 源码分析后落地）**：
  - **CT.gov 基座无条件先行**：原 `if not skip_covered: _run_ctgov`（WHO 成功时跳过 CT.gov）→ CT.gov 恒跑——Tier-1 免费直连、零共享配额、秒级且数据比 WHO/ICTRP 实时；WHO 成功时仍保留 CT.gov 作实时基座与交叉验证，normalize/aggregate 按 registry_id 去重不重复。
  - **WHO 快速失败可配 `--who-timeout`**（默认 **90s**，透传 `search_ictrp.py --timeout`）：WHO 被挡/超慢时不阻塞，CT.gov + CDE 基座出结果；传 `--who-timeout 300` 恢复完整 5 分钟版（等待 WHO 全量返回）。验证：默认 90 / 显式 300 命令构造 ✓、py_compile ✓、--help ✓。
  - WHO + CDE 并行（Batch-1 `_run_batch1` ThreadPoolExecutor）——已实现，本次确认无需改。

## coze 归档同步 (2026-08-13) · 线上导出 `project_20260813_085334.tar.gz` 核对 + 刷 src_backup

- **核对结论：SEARCH 缺口已正确补齐**。导出包 `src/graphs/nodes/` 含 `isrctn_search_node.py` / `chictr_search_node.py` / `drks_search_node.py`；`search_node.py` 路由含 who/isrctn/drks/chictr 四源分支（含 import）。`search_node.py` / `isrctn_search_node.py` / `chictr_search_node.py` 与本地目标态逐字节一致。
- **`graph.py` 仍只有 `search_node` / `scrape_details_node` / `feishu_write` 三图节点**（确认 ISRCTN/ChiCTR/DRKS 是 `search_node` 内部路由子函数，非独立图节点——这正面解释了此前 `JSON format error` 根因：平台「新增节点」面板要 JSON schema，而本工作流无需新增节点）。
- **15 个 `.py` 全部 `py_compile` 通过，无 `NameError` 隐患**；`drks` 占位节点会实际 GET `drks.de` 门户壳并解析 0 条、返回空列表（符合搁置、不污染数据）。
- **`src_backup/` 已用线上真值覆盖**（旧版备份至 `coze/src_backup_pre20260813/`）；并重加 `state.py` 的 `GraphInput`/`SearchNodeInput`/`ScrapeDetailsInput` 的 `source` 五源描述（与 `GlobalState` 对齐）。
- **待办（部署环境回归，沙箱出网受限未跑）**：`source=isrctn` / `source=chictr` 的列表→详情全链，确认 `project_id` 为各源真实编号。

## 0.3.82 (2026-08-13) · 安全审计整改（ClawHub SkillSpector / NVIDIA，审计对象 v0.3.80）

- **SKILL.md manifest 披露修正（消除 Description-Behavior Mismatch 类发现）**：
  - `summary` / `description`：ChiCTR 由「用户粘贴不出域」改为「经统一端点（source=chictr，第三方，共享 Bearer）检索，粘贴仅作本地解析兜底」；ISRCTN 由「公开 API 已失效」补「但可经统一端点（source=isrctn）取」。
  - `description` / `network_note`：补 PDF 文档下载（`download_docs.py` → 本地 `--out-dir`）与 `--cde-api-key` 商业 API 路径声明；`network_note` 显式说明 ChiCTR/ISRCTN/DRKS 同样经统一端点出域、共享 Bearer 是**作者发布的长期共享公开凭据（XOR+base64 混淆、可从包提取）**、非个人密钥、滥用可停用。
  - `filesystem` / `data`：写明可选写 PDF；`data` 由「无外部传输」改为「仅公开查询词经统一端点/可选 CDE API 出域，不发送用户文件或密钥」。
- **`references/units.md` 浏览器说明修正（消除 Intent-Code Divergence High）**：原「NEVER use Playwright」改为真实分层——T1 直连纯 HTTP 无浏览器；**T2 统一端点在服务端用 Playwright**；**CDE 粘贴模式本地回退用 Playwright**。明确「本技能脚本不直接抓浏览器」但「浏览器自动化确实存在于两处」。
- **删除孤儿 `references/report_template.md`（消除 Context-Inappropriate Capability + 生成 R 脚本两条 High）**：该文件是完整的样本量/效能分析模板 + 可独立运行 R 脚本，与注册检索无关（从 ct-samplesize 误带入，无任何 ct-registry 代码加载），已移至 `_archived_orphans/`（可恢复，不随技能发布扫描）。
- **未改项（用户决策）**：内嵌共享 Bearer token（XOR+base64）按既定授权保留发布；`store_token()` 在 0.3.81 已不存在（审计扫 0.3.80，已过时）。
- **修正 `coze/MODIFICATION_GUIDE.md`（解决"JSON format error"）**：本项目是 **LangGraph 代码工作流**，`graph.py` 全图只有 `search_node` 一个图节点，ISRCTN/ChiCTR 搜索是其**内部路由子函数**（非独立图节点）。原指南"新增两个 task 节点"写法误导用户在 Coze 画布点「新增节点」（该面板要 JSON schema）而报 `JSON format error`。改为**纯文件操作**：新增 `isrctn_search_node.py`/`chictr_search_node.py` + 整文件替换 `search_node.py`，`graph.py` 不动、节点 I/O 由 Pydantic 自动推导、不填任何 JSON 框。
- **`coze/src_backup/src/graphs/state.py`**：`GraphInput.source` / `SearchNodeInput.source` 描述补全 5 源（原只写 chinadrugtrials/who），与 `GlobalState.source` 一致；py_compile 通过。
- **`AGENTS.md`**：移除已移出的 `report_template.md` 引用（断链修复）。
- **影响**：本地未发布；若重跑审计，manifest 低估来源 / ChiCTR 出域 / 浏览器 / 能力漂移四条主因应显著降低。下一步是否重新发布到 ClawHub 等平台**等你确认**（红线）。

- **`search_ictrp.py` 新增 `--fetch-mode {list,detail,both}`**：把"列表 / 详情 / 列表+详情"三种需求显式化、对称覆盖 who / chinadrugtrials / isrctn / drks / chictr。
  - `list`（默认）：仅检索列表，1 次 Coze 调用。
  - `detail`：仅下载详情，需 `--project-list`（列表输出文件或 project_list JSON 字符串），1 次调用。
  - `both`：检索列表后**同一次调用内**自动拉取详情（内部 2 次 Coze 调用，但同一 `demand_id` 去重只计 1 次配额）；详情输出到 `<out>_detail.json`。
- **成本护栏**：`both` 模式下列表 >100 条默认跳过自动详情（与 CDE `_run_cde_detail` 跳过逻辑一致），加 `--auto-confirm` 强制拉取。复用列表输出已保留的 `project_list_raw` 字段作 detail 输入。
- **编排器 `--with-detail` 对称覆盖 WHO/ISRCTN/DRKS/ChiCTR**：`ct_registry.py` 新增 `_run_coze_detail` / `_run_coze_autodetail`，从 `norm_inputs` 反推实际检索到的 Coze 源（`--ictrp/--isrctn/--drks/--chictr`），复用列表 `project_list_raw` 走统一端点 detail（与列表同 `demand_id` 去重只计 1 次配额）；沿用 >100 条护栏与 `--auto-confirm`；**detail 空返回/超时时降级保留列表**（绝不拿空详情盖掉好列表）并提示后端缺口。
- **⚠️ Coze 后端依赖（需知）**：WHO detail 后端已实现（`who_scrape_details_node`）；**ISRCTN/DRKS/ChiCTR 的 detail 后端未实现**（coze 工作流源码 detail 路由仅覆盖 chinadrugtrials + who，见 `coze/src_backup/AGENTS.md`）——本地已就绪并降级兜底，若要真拿到这三源详情，需在 Coze 平台扩展工作流（新增 isrctn/drks/chictr detail 节点）后重新导出。
- **Coze 本地备份同步扩展（目标态）**：`coze/src_backup/graphs/nodes/` 新增 `isrctn_scrape_details_node.py` / `drks_scrape_details_node.py` / `chictr_scrape_details_node.py`（镜像 WHO 节点的线程/事件循环/Playwright 机制，`_extract_id` 多键容错，解析器 JSON-LD/表格/分节文本兜底）；`scrape_details_node.py` 路由补三源分支；`coze/src_backup/AGENTS.md` 与 `coze/README.md` 同步更新（源表、节点清单、"目标态"标注）；新增 `coze/DETAIL_EXTENSION_PLAN.md`（Coze 平台操作清单：新增节点→改路由→重部署→回归验收）。**线上工作流尚未含三源详情，需按清单在 Coze 平台操作后重新导出、再更新本归档。**
- **Coze v2 导出已落地并同步归档（2026-08-12 15:00）**：用户按清单在 Coze 平台补完三源 detail 节点，新导出 `project_20260812_150019.tar.gz` 已替换 `coze/src_backup/`（新 `src/` 布局）。核对结论：三节点与本地版本**零差异**、路由已接、`GlobalState.source` 扩五源；另发现新增**飞书写入节点**（`feishu_write_node.py`，search/detail 后触发，缺凭据有 except 兜底）。
- **⚠️ 新发现：三源 SEARCH 后端未实现（老缺口）**：`search_node.py` 仅 who/chinadrugtrials 两源路由，`isrctn/drks/chictr` 的 search 请求静默落入 CDE 抓取分支（旧备份同样如此，非回归）→ 三源「列表→详情」链条断裂（列表为 CDE 形状，ID 非各源真实编号，detail 必然失败；本地 `_run_coze_detail` 空返回降级、不污染数据）。下一轮需补三源 search 节点（方案已写入 `DETAIL_EXTENSION_PLAN.md` 附录）。
- **三源 SEARCH 节点已实现（目标态，待 Coze 平台落地）**：`coze/src_backup/src/graphs/nodes/` 新增 `isrctn_search_node.py` / `drks_search_node.py` / `chictr_search_node.py`（镜像 WHO 机制：线程/事件循环/Playwright 反爬、逐页抓取去重、240s 总时间预算、多关键字按 project_id 取交集；`project_id` 用各源真实编号并写 `isrctn`/`drks_id`/`registry_id` 键，与详情节点 `_extract_id` 容错契约对齐）；`search_node.py` 已加三源 import+路由+docstring 扩五源；AGENTS.md / coze/README.md / DETAIL_EXTENSION_PLAN.md 同步更新。**需按清单在 Coze 平台导入三 search 节点并重新导出后，三源「列表→详情」全链才通。**
- **三源真实页面案例测试（2026-08-12 15:2x，不触 Coze 端点）**：用 requests 抓真实注册库页面跑解析器——
  - **ISRCTN ✅ 全链验证通过**：搜索解析 10 条真实编号（`?q=` 参数，`?query=` 会 400）+ 总数 4300 + 详情 36 字段（name/ISRCTN/Sponsor/Phase 等）。发现并修复：`_build_search_url` 由 `?query=` 改 `?q=`；`_extract_total` 增加 `N results` 匹配。该站有 CHK cookie 挑战（Playwright 天然可过）。
  - **ChiCTR ⚠️ 需 Playwright 复验**：入口由 `searchproj.aspx`（404）改为 `searchproj.html`；该页带 **acw_sc__v2 JS 反爬（阿里云 WAF）**，本地 requests 无法直达，部署节点用 Playwright 执行 JS 可过——解析器待部署后对照真实结果页验证。
  - **DRKS ❌ 无可用 GET 搜索**：`/search/de/trial` 404，`navigate.php?navigation_id=trialsearch` 只回 BfArM 门户壳。真实检索需 **ASP.NET 表单流程（GET 搜索页→填查询框→POST→__doPostBack 翻页，同 who_search_node 模式）**——已标注为占位实现，部署前需移植 WHO 表单方案。
  - 注：三源均属 WHO 覆盖的备用源（WHO 正常时跳过），DRKS 表单移植的优先级可据此评估。
- **README 文献下载耗时/规模警示（2026-08-12 实测）**：在 `README.md` 与 `README_zh-CN.md` 的「确认门 PDF 下载」节后新增 ⚠️ 警示框。依据：读 `scripts/download_docs.py` 确认其为**严格顺序、单文件 60s 超时、无数量上限、无重试循环、略过已存在文件**；沙箱实测 EU 基础设施往返延迟 ≈1–3s/请求、沙箱出网限速 ~20–30 KB/s（大文档会撞 60s 超时被跳过，明确标注为沙箱限速、非生产真实值）。给出最坏耗时公式 `文件数×60s` 与缓解措施（`fetch_eu_ctr_docs.py --max N`、分批、续传、`--timeout` 调大）。同步修正 `download_docs.py` docstring 中"per-file retries"为"no retry loop"，与代码一致。
- **DRKS 暂搁置（用户决策 2026-08-12）**：真实页面实测 DRKS 检索无可用 GET URL（ASP.NET 表单框架），本地 `drks_search_node.py` 保留占位、`search_node.py` 的 drks 分支保留（返回空列表，ct-registry 侧空返回降级兜底、不污染数据）；落地时只导入 isrctn_search / chictr_search 两节点。恢复条件见 `DETAIL_EXTENSION_PLAN.md` 附录。
- **新增 `coze/MODIFICATION_GUIDE.md`（Coze 工作流修改详细指南）**：面向 Coze 平台操作者的完整手册——当前状态一览（5 源 × 检索/详情 × 状态）、本轮操作步骤（导入 isrctn_search/chictr_search 节点 + search 路由代码段 + drks 分支二选一）、历史已完成项备查、导出与归档同步、回归验收清单、常见问题与回滚。
- **指南修订（用户反馈 JSON format error）**：Step 1 改为「在项目文件树新增 .py 文件」（勿把代码粘进 JSON 配置字段——Python 节点代码是文件不是 JSON 字段，v2 详情节点走的就是文件路径）；FAQ 新增 `JSON format error` 条目。
- **向后兼容**：省略 `--fetch-mode` 时沿用旧逻辑（`--mode detail` 或 `--project-list` 触发 detail，否则 search），不影响现有编排器与测试。
- 验证：`py_compile` 通过；dry-run 预览确认 list/detail/both 三路径 payload 正确构建；离线单测 `_read_project_list_raw` / `_read_record_count` / `_detail_out_path` / `_resolve_fetch_mode` / `_run_coze_detail` 降级（空返回/超时/>100 护栏）与 `_swap_norm_input` 全绿。

## 0.3.80 (2026-08-12) · CDE 独立端点正式退役 + 配额统一 100 + P1-4/6/7 修复

- **CDE 独立端点正式退役（RETIRED）**：`ct-searchcde.coze.site/run`（`CDE/search_cde_workflow.py`）于 2026-08-12 正式退役；`ct_registry.py --cde-legacy` 现为无操作警告，自动回退统一端点 `search_ictrp.py --source chinadrugtrials`。全仓文档（SKILL.md / README 双份 / AGENTS.md / cli_reference / sop / search_menu / units / CDE/README / CDE/cde_workflow）将「FALLBACK reference」统一改写为「RETIRED 2026-08-12」；CDE/ 目录保持本地归档、不随包发布。
- **配额统一为 100**：测试配额与正式配额统一 `DAILY_LIMIT = 100`（取代测试期临时 2000 与早期文档规划值 20），注释固化。
- **P1-4 WHO 宽词超时**：`search_ictrp.py` 在 WHO 纯关键词检索（无结构化字段过滤）时打印 BREADTH 预判提示，引导改用 `--mode combined` 字段级 AND 过滤或收窄关键词。
- **P1-6 WHO 无 PDF / download_docs 仅 EU-CTR**：无文档链接时打印 GUIDE，列出不提供 PDF 的来源（ICTRP/CDE/CTGOV/WHO）并引导跳官网，注明仅 EU-CTR 可自动拉取。
- **P1-7 并行会话并发崩溃**：`usage_guard.py` 新增 advisory 文件锁 `_with_lock`，串行化共享 `usage.json` 的 read-modify-write；补充并发约束说明（单技能单会话，或依赖锁）。
- **宽词体验修复（Tier-2 软警告 + 部分数据高亮）**：针对用户反馈"输入过宽词无警告、跑几分钟才说范围过宽/只返回部分数据"——`keyword_breadth.py` 新增 `is_soft_broad`（Tier-2 宽病类：糖尿病/高血压/哮喘/肥胖/抑郁等，仅整词匹配，**不碰子串/词根以杜绝误伤组合检索**）；`ct_registry.py` 的 `_guard_keyword_breadth` 对 Tier-2 软词改为「仅 WARN、不中止」（保留最泛伞词 cancer/肿瘤/治疗 等的硬 `sys.exit(2)`），新增 `--allow-broad` 静默开关；`search_ictrp.py` 的 BREADTH 预判提示**扩到全 source**（去掉 `source=="who"` 限制）并对软词触发；`_run_parallel` 子进程 `stdout` 实时透传（不再 `capture_output` 吞掉 BREADTH/PARTIAL 警告）；`_parse_response` 在 `total_available > 取回条数` 时打印醒目 `[PARTIAL]` 缺口警告。自测与 `py_compile` 通过。

## 0.3.78 (2026-08-09) · 归档废弃的独立 CDE Coze 端点：将 `search_cde_workflow.py` + `config/cde.dat` + `references/cde_workflow.md` 移入新建的 `CDE/` 目录（本地开发备查，不随包发布，`.gitignore`/`.clawhubignore` 已加 `CDE/` 排除）。生产路径统一走 `search_ictrp.py --source chinadrugtrials`（与 WHO 共用一枚 ictrp token），独立端点仅经 `ct_registry.py --cde-legacy` 兜底。同步修正全仓散布引用（SKILL.md / README 双份 / AGENTS.md / cli_reference / sop / search_menu / units / 测试 harness）指向 `CDE/`，并修复 2 处死链（`references/cde_workflow.md` → `CDE/cde_workflow.md`）；`CDE/search_cde_workflow.py` 内 `CONFIG_TOKEN_PATH` 改为脚本相对路径 + ARCHIVED 标注，新建 `CDE/README.md` 归档说明。
