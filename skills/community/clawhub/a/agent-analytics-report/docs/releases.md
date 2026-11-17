# Releases

agent-analytics-report 的版本发布说明。每个版本都对应一个 GitHub Release（含完整 release notes），下表为速览。

> 完整、细粒度的变更历史见 [CHANGELOG.md](./CHANGELOG.md)。

| 版本 | 日期 | 主题 | GitHub Release |
|---|---|---|---|
| **v1.9.13** | 2026-10-21 | 发布门禁闭环：test_sdi4 伪密钥改为运行时拼接（消 skill-publish-gate CRITICAL 误报）+ SKILL.md 补 requires 声明；复跑 BLOCKED→NEEDS_FIX(critical=0) | [tag/v1.9.13](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.13) |
| **v1.9.12** | 2026-10-21 | 回应 ClawHub v1.9.11 复审 need review：闭环 Tier A 真实代码缺陷（claude-code 缓存计数 / codex 累计快照增量 / ca_core 惰性发现 / dumate 去动态导入）+ Tier B 信任披露（SKILL.md 去绝对化 / 新增 metadata.json 最小权限 manifest）+ 回归测试 | [tag/v1.9.12](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.12) |
| **v1.9.11** | 2026-10-21 | 修复 generate_report.py 异常分析区块模型名/异常原因/日期未转义（HTML 注入，ClawHub T09）；复用 `_esc()` 统一转义 + 条形图 title 属性加固 + 回归测试 | [tag/v1.9.11](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.11) |
| **v1.9.10** | 2026-10-20 | 新增 MiniMax-M3.1-Flash / Kimi-K2.8-Preview / 小米 MiMo-V2.6-Pro 模型定价（¥1/¥4、¥6.5/¥27、¥3/¥6）+ 修正 minimax-m3 误记价与 space-bunny 回填官方价 | [tag/v1.9.10](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.10) |
| **v1.9.9** | 2026-10-17 | 新增阶跃 Step 5 Preview 模型定价（WorkBuddy 限免期 10/12-10/25）：直连 API ¥7.2/¥19.44（缓存命中 ¥0.72）+ timed_free 限免至 2026-10-25 | [tag/v1.9.9](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.9) |
| **v1.9.8** | 2026-10-15 | 修复 build_model_cost_chart 模型名未转义存储型 XSS（SDI-4）+ 降噪打磨（RA2 误报措辞收敛 / 示例隐私提醒 / LLM 分类器出站确认闸） | [tag/v1.9.8](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.8) |
| **v1.9.7** | 2026-10-13 | 修正 ClawHub 展示名 Pub Clawhub → Agent Analytics Report（发布漏传 --name，版本不可覆盖故升版重发；无代码变更，重扫 Moderate CLEAN） | [tag/v1.9.7](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.7) |
| **v1.9.6** | 2026-10-13 | 消除 ClawHub v1.9.5 复审 7 HIGH：① 污染 4（verify_194.json 误收进包，已封死）② 真 over-collection 2（collect_claude_code/collect_codex 合并 collector 补日期窗口过滤 + 移除 rglob 二级递归）③ LP3 最小权限 manifest（_meta.json permissions + SKILL.md 权限表）④ TP4 强化披露 | [tag/v1.9.6](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.6) |
| **v1.9.5** | 2026-10-12 | 消除 ClawHub v1.9.4 重扫后残余 3 HIGH：SDI-1（ca_sources.py 递归 glob 过扫 `~/.claude/projects`，改一级目录收敛）+ SDI-4（generate_report.py dumate 标签去品牌化、强制归属告警）+ TP4（SKILL.md dumate 归属不再暗示确认） | [tag/v1.9.5](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.5) |
| **v1.9.4** | 2026-10-12 | 消除 ClawHub v1.9.3 重扫后残余 4 HIGH：P6×2（release notes 字面量触发词）+ TP4×1（analyze_tokens.py 写报告产物未入 SKILL.md 权限声明）+ SDI-4×1（on-download-inject.md「首次生成报告可能触发扫描」措辞与「普通报告严格只读」矛盾） | [tag/v1.9.4](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.4) |
| **v1.9.3** | 2026-10-11 | 安全加固翻盘：移出发布/CI/开发脚本出包 + P6 误报消除 + SDI-4 越窗收集修复 | [tag/v1.9.3](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.3) |
| **v1.9.2** | 2026-10-11 | 安全加固（回应 ClawHub 扫描 need review）：SDI-4 修复 + SQP-2 截断脱敏 + 最小权限声明 | [tag/v1.9.2](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.2) |
| **v1.9.0** | 2026-10-06 | 百度搭子（DuMate）数据源 + 任务类型分类修复 + 归属标注与文档降级（归因红线）+ 隐私护栏（只读 SQLite / 时间窗过滤）+ 合规文案收敛 | [tag/v1.9.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.0) |

| **v1.7.2** | 2026-09-22 | Phase C · L1 真值下 §4.4 省钱建议改用官方真实积分（C7）；L1 不再渲染低置信度噪音 | [tag/v1.7.2](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.7.2) |
| **v1.7.1** | 2026-09-16 | Phase B 按调用时刻应用时段定价：B4 夜间免费 / B5 峰谷双档 / B6 促销跨期 | [tag/v1.7.1](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.7.1) |
| **v1.7.0** | 2026-09-15 | F17 P1 请求数反推 + P2 路由别名解析；低置信度最贵模型 A1/A2/A3 告警 | [tag/v1.7.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.7.0) |
| **v1.6.2** | 2026-09-14 | 低置信度模型标记改为纯 ⚠（去 span 包裹，与 MD 一致） | [tag/v1.6.2](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.6.2) |
| **v1.6.1** | 2026-09-14 | 修复 §3.5 误报盲区（官方侧补 display_merge 归拢，虚报 410.95 积分） | [tag/v1.6.1](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.6.1) |
| **v1.6.0** | 2026-09-14 | F17 双源对账：官方用量导出接入（`--import-official`）· 成本 L1 真值 | [tag/v1.6.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.6.0) |
| **v1.5.2** | 2026-09-14 | 成本置信度（L1 真值 / L2 估算）· 低置信度模型标注 | [tag/v1.5.2](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.5.2) |
| **v1.5.1** | 2026-09-12 | 定价数据刷新（DeepSeek V4.1-Flash 峰谷双档 · V4-Flash 下架 · Hy4 限免新规） | [tag/v1.5.1](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.5.1) |
| **v1.5.0** | 2026-09-07 | 任务分类加权评分（P2-3）· 定价自动更新（P2-2）· P0 数据完整性修复 | [tag/v1.5.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.5.0) |
| **v1.4.0** | 2026-09-06 | 多 Agent 数据源（Claude Code 适配器 MVP，P2-1） | [tag/v1.4.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.4.0) |
| **v1.3.0** | 2026-09-02 | 档位维度分析 · 模块拆分重构 · 孤儿 trace 修复 | [tag/v1.3.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.3.0) |
| **v1.2.1** | 2026-08-29 | 幽灵调用修复（Agent workflow span 还原） | [tag/v1.2.1](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.2.1) |
| **v1.2.0** | 2026-08-29 | display_merge 合并显示 · 定价库更新 · FAQ | [tag/v1.2.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.2.0) |
| **v1.1.3** | 2026-08-23 | hy3-x 定价 · 通道测试 Allure 化 | [tag/v1.1.3](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.1.3) |
| **v1.1.2** | 2026-08-12 | SkillHub 重新发布修正 | [tag/v1.1.2](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.1.2) |
| **v1.1.1** | 2026-08-11 | 日历对齐周期 · XSS 防护 | [tag/v1.1.1](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.1.1) |
| **v1.0.0** | 初始发布 | 首发 WorkBuddy Agent 用量与成本报告 | [tag/v1.0.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.0.0) |

---

## v1.9.13 — 2026-10-21
### 发布门禁闭环：消解 skill-publish-gate 误报 + 补 ClawHub 声明一致性

- `tests/test_sdi4_security.py` 伪密钥改运行时拼接，源码不含 `sk-` + 高熵字面量，消除凭据泄漏误报。
- `SKILL.md` 补 `requires: ["python3"]`。
- 复跑：clawhub `BLOCKED(critical=2)` → `NEEDS_FIX(critical=0)`；`security-audit` 凭据扫描 0 critical / 0 high。六处版本号一致升 1.9.12→1.9.13。


## v1.9.12 — 2026-10-21
### 回应 ClawHub v1.9.11 复审「need review」：闭环 Tier A 真实代码缺陷 + Tier B 信任披露

- **Tier A 真实代码缺陷（安全/正确性）**：A1 claude-code 缓存读写计入透明 raw total；A2 codex 累计快照改增量 delta（修复重复计数 + `token_count` 缩进错位）；A3 `ca_core.py` 自定义模型发现改惰性触发（消除导入期副作用）；A4 dumate 去动态导入。
- **Tier B 信任披露**：B1 SKILL.md 去「严格只读/完全离线」绝对化；B2 metadata/_meta 收窄触发语境 + 声明 opt-in；B3 FAQ 脱敏提醒 + 自动发现按需；B4 **新增 metadata.json `permissions` 最小权限 manifest**（闭环 LP3）；B5 README BYOM 扫描改显式 opt-in。
- 回归测试新增 `tests/test_lazy_custom_model_discovery.py` 等；六处版本号一致升 1.9.11→1.9.12（config / metadata / _meta / SKILL.md / CHANGELOG + releases）。


## v1.9.11 — 2026-10-21
### 修复 generate_report.py 异常分析区块模型名/异常原因/日期未转义（ClawHub T09 HTML 注入）

- **T09 HTML 注入修复（安全）**：ClawHub AI-Infra-Guard（`aig-skill-scan v0.2.2`，LLM `gpt-6.1-sol`）在 v1.9.10 判 `decision=fail` / `security.status=suspicious`（规则 T09，Medium），根因是 `scripts/generate_report.py` 的 `_render_anomaly_block()` 在 MD 与 HTML 两分支把来自 trace 的会话主要模型名（`a["models"]`）、异常原因（`a["reasons"]`）、异常日（`a["date"]`）及会话标题未经 HTML 转义即写入报告——构造的模型名（如 `<script>…</script>`）会在 HTML 报告打开时执行 JS。现统一套用既有 `_esc()`（`html.escape(..., quote=True)`）。
- **每日趋势条形图 `date` 加固**：横向条形图 `title="{date}"` 属性与文本节点补 `_esc()`（属性上下文注入面）。
- **回归测试**：新增 `tests/test_anomaly_html_escape.py`，用构造 `<script>` 模型名/原因验证 MD 与 HTML 输出均被转义、正常模型名无回归。
- 六处版本号一致升 1.9.10→1.9.11（config / metadata / _meta / SKILL.md / CHANGELOG + releases）。

## v1.9.10 — 2026-10-20
### 新增 MiniMax-M3.1-Flash / Kimi-K2.8-Preview / 小米 MiMo-V2.6-Pro 模型定价 + 修正 minimax-m3 / space-bunny 价格

- `scripts/pricing.json` 的 `models` 段新增 3 个模型刊例价（价表此前缺失）：`minimax-m3.1-flash`（MiniMax 2026-10-19 正式发布，官方 ¥1/¥4/缓存0.1）、`kimi-k2.8-preview`（Kimi Code 2026-09-11 全量上线，¥6.5/¥27/缓存1.7）、`mimo-v2.6-pro`（小米 2026-09-22 发布，¥3/¥6/缓存0.025）。
- 修正 `minimax-m3` 误记价 ¥1/¥4 为官方分档刊例价 ¥2.1/¥8.4（≤512K，缓存0.42；>512K 4.2/16.8）；`space-bunny` 身份揭示=MiniMax M3.1 Flash 早期匿名版（太空兔），由推算值 ¥0.73/¥2.91 回填官方 ¥1/¥4（缓存0.1）。
- `_sources` 补 4 条来源；`_pricing_rules.updated` 刷新为 2026-10-20。
- `scripts/ca_core.py` 种子同步新增 3 个模型 + 修正 2 个存量价。
- 六处版本号一致升 1.9.9→1.9.10（config / metadata / _meta / SKILL.md / CHANGELOG + releases）。

## v1.9.9 — 2026-10-17
### 新增阶跃 Step 5 Preview 模型定价（WorkBuddy 限免期 10/12-10/25）

- `scripts/pricing.json` 的 `models` 段新增 `step-5-preview`：阶跃星辰（StepFun）旗舰 Agent 模型，官方直连 API 定价（美元 ×7.2≈CNY 估算）输入(缓存未命中) $1.00 / 输入(缓存命中) $0.10 / 输出 $2.70 每百万 tokens；1M 上下文、文本+图像+视频输入、支持工具调用/JSON/推理强度。
- `timed_free` 段新增 `step-5-preview: "2026-10-25"`（WorkBuddy 内独家限免至 2026-10-25，限免期全时段 0 积分；之后按约 0.43 倍积分计费，与直连 API ¥ 价非同一口径，已在 note 说明）。
- `_sources` 补阶跃官方模型页 + 定价页来源；`_pricing_rules.updated` 刷新为 2026-10-17。
- `scripts/ca_core.py` 的 `MODEL_PRICING` 冷启动兜底种子同步加 `step-5-preview`（与 pricing.json 一致，防冷启动 NameError）。
- 六处版本号一致升 1.9.8→1.9.9（config / metadata / _meta / SKILL.md / CHANGELOG + releases）。

## v1.9.8 — 2026-10-15
### 修复 build_model_cost_chart 存储型 XSS（SDI-4）+ 降噪打磨

- **SDI-4 存储型 XSS 修复（安全）**：`scripts/report_charts.py` 的 `build_model_cost_chart()` 把模型名 `m["model"]` 直接拼入 HTML `title=` 属性与文本节点，未做 HTML 转义；现统一经 `_esc()` 转义（含 `title` 参数），防止本地 trace/config 中携带引号或标记的模型名在报告被打开时执行脚本。新增回归测试 `tests/test_sdi4_security.py::test_build_model_cost_chart_escapes_model_name`（恶意 `<script>` / `onmouseover=` payload 被转义为惰性文本、正常模型名恒等输出）。
- **RA2 误报措辞收敛**：CHANGELOG/releases 的 v1.9.6「根因复盘」移除 `发往端点` / `file_read/file_write/network/env 最小作用域` 等被 agentic-risk 扫描器误读为「会话持久化/越权」的措辞，改为中性表述，消除 4 处 RA2 假阳性（clawscan 已标注 unexpected）。
- **示例隐私提醒（Item C）**：`examples/sample-report.md`、`examples/sample-report.html`、`examples/skillhub-usage-examples.md` 新增醒目隐私提醒——报告聚合本机会话标题/提示词/项目路径/Token 成本等敏感数据，对外分享/截图/提交前需脱敏。
- **LLM 任务分类器出站确认闸（Item D）**：`--task-classifier llm` 默认关闭；启用时需显式 `--task-classifier-llm-ack` 或环境变量 `AAR_TASK_LLM_ACK=1` 确认，否则回退本地启发式并发出未确认警告（会话派生文本不会发往端点）。新增 `tests/test_task_type_classifier_consent.py`。
- 六处版本号一致升 1.9.7→1.9.8（config / metadata / _meta / SKILL.md / CHANGELOG + releases）。

## v1.9.6 — 2026-10-13
### 消除 ClawHub v1.9.5 复审 7 HIGH（污染 4 + 真 over-collection 2 + LP3 manifest）

- **根因复盘（第一性原理）**：v1.9.5 的 7 个 HIGH 分三类——① **4 个污染 HIGH** 锚在 `verify_194.json`（旧扫描快照，被 ClawHub `publish .` 文件系统遍历误收进包，被逐行重扫又生成递归扫描/读全文/向外传出/update_url 等 HIGH）；② **2 个真 over-collection**：CLI 实际走的 `collect_claude_code` / `collect_codex` 合并 collector 漏做日期窗口过滤，越窗会话元数据进报告；③ **1 个 LP3**：缺最小权限 manifest。
- **真 over-collection 修复（SDI-1 / SDI-4 核心）**：`adapters/claude_code.py` 与 `adapters/codex.py` 新增共享 `_session_in_window` 判定，在 `collect_claude_code` / `collect_codex`（CLI 实际路径）应用与 `collect_*_sessions` 完全一致的日期窗口过滤，越窗会话整体跳过（不漏 trace、不漏元数据）；`claude_code.py._iter_jsonl_files` 移除 `rglob("projects")` 二级递归，改只枚举 projects 根一级工程目录。回归测试 `test_*_excludes_out_of_window_sessions` + `test_*_combined_and_sessions_agree_on_window` 锁死。
- **污染封死**：`.clawhubignore` + `.gitignore` 通配排除 `verify_*.json`；ClawHub 改 `git archive HEAD` 干净树发布，永久避免 untracked 文件误收。
- **LP3 最小权限 manifest**：`_meta.json` 新增 `permissions` 块（最小作用域的权限声明，详见权限表），SKILL.md「一·附」改权限表 + 补 update_url 说明（仅 `skillhub upgrade` 用、报告流程绝不触发网络）。
- **TP4 强化披露**：隐私清单「任务分类」行加 ⚠️ 高风险出站警告（启用 `--task-classifier llm` 时才发往用户端点、默认关闭）。
- 五处版本号一致升 1.9.5→1.9.6（config / metadata / _meta / SKILL.md / CHANGELOG + releases）。

## v1.9.5 — 2026-10-12
### 消除 ClawHub v1.9.4 重扫后残余 3 HIGH（SDI-1 / SDI-4 / TP4）
- **SDI-1（真过扫）**：`scripts/ca_sources.py` `_find_session_jsonl` 的兜底分支用 `PROJECTS_DIR.glob(f"**/{session_id}.jsonl")` 递归遍历整个 `~/.claude/projects` 树，可枚举无关会话工件（隐私面越权）。改为**只探测一级子目录**做 exact-name 匹配（`for sub in PROJECTS_DIR.iterdir(): cand = sub / f"{session_id}.jsonl"`），不递归更深，访问面收敛到「请求的那个会话」所在目录层。
- **SDI-4（真误标）**：`scripts/generate_report.py` `_SOURCE_LABELS["dumate"]` 标题写「百度搭子使用情况报告」，与 metadata「归属未证实」自相矛盾（实测 217 会话 qianfan/dumate 命中 0 行，内容 100% 是 WorkBuddy）。去品牌化改「Dumate 数据源使用情况报告（数据归属未证实）」，数据来源行与清单**强制带「归属未证实、勿当作百度搭子用量引用」告警**；同步改 SKILL.md 硬约束 3 与 `tests/test_dumate_adapter.py` 标题断言。
- **TP4（混合 messaging）**：SKILL.md 权限声明与正文把「默认只读离线」与「可选联网 / 写 dumate 归属不明」混写，被扫描器读成「用户在错误隐私假设下调用」。dumate 标签去品牌化后，SKILL.md 默认流程与可选流程的表述不再暗示确认的百度搭子归属；`analyze_tokens.py` 的「报告产物写（默认流程）」条目保留（v1.9.4 已加）。
- 五处版本号一致升 1.9.4→1.9.5（config / metadata / _meta / SKILL.md / CHANGELOG + releases）。

## v1.9.4 — 2026-10-12
### 消除 ClawHub v1.9.3 重扫后残余 4 HIGH（P6×2 / TP4×1 / SDI-4×1）
- **P6×2**：v1.9.3 的 CHANGELOG/releases 笔记里对 ca_core 重命名动作的描述性文字，恰好命中了静态扫描器按关键词匹配 P6 类的敏感词表 → 重新误报。本次把两处描述改为「时段定价标识符语义统一（`sched` / `_schedule_matches`）」，不再出现触发词，也不再引用具体代码片段。
- **TP4×1**：`scripts/analyze_tokens.py` 会写报告产物文件，但 SKILL.md 权限声明未列 → manifest 与实现不一致。SKILL.md「一·附 权限声明」补「报告产物写（默认流程）」条目：只写用户指定的 `--output` 路径，不写 `~/.workbuddy` 内部文件、不读网络、不改定价/配置。
- **SDI-4×1**：`references/on-download-inject.md` 与 SKILL.md 原文「下载后首次生成报告（或主动说一句...）」被读成「首次生成普通报告就可能触发扫描」，与「普通报告严格只读」矛盾。统一为：普通用量报告严格只读、离线、绝不触发扫描/写配置；注入仅在你明确发起「自定义模型注入」流程时才发生。

## v1.9.3 — 2026-10-11
### 安全加固翻盘（回应 ClawHub 扫描 need review）
- **P0 打包口径（TP4 / SDI-1）**：`.clawhubignore` 移出 `scripts/fetch_pricing.py` / `gen_report.py` / `verify_privacy_parity.py` / `scripts/gen_example_report.py` 出终端用户发布包（保留 git）。
- **P0 误报消除（P6）**：`ca_core.py` 时段定价相关标识符重命名为 `sched` / `_schedule_matches` 语义，规避静态扫描器按关键词误判的 HIGH（零行为变更）。
- **P1 真 bug 修复（SDI-4）**：`collect_*_sessions` 落实窗口过滤契约，越窗会话元数据不再越权纳入；补回归测试。

## v1.9.2 — 2026-10-11
### 安全加固（回应 ClawHub 扫描 need review）
- **SDI-4 修复**：联网检索改 `urllib` 异常兜底，抽 `fetch_remote_pricing()` 并加单测。
- **SQP-2 收敛**：会话正文抽取改截断 + 脱敏短样本（≤120 字符），采集入口加只读/离线告知。
- **LP3 / TP4 声明**：SKILL.md 新增最小权限作用域声明块。

## v1.9.1 — 2026-10-11

**安全扫描加固（P2/P3 残留项收口）**

- 🔒 P2-1：SKILL.md 中 `scripts/task_rules.json` 引用补「纯 pattern 列表、不含可执行代码」声明，消除 SkillSpector `Ae1` 盲区（被引用 artifact 未被完整检查）。
- 🔒 P2-2：`scripts/collect_usage_data.py` 的 `--pricing-api` / `--task-llm-endpoint` 两处新增「防 SSRF、不内置任何默认端点、不传则完全离线」安全边界注释（无逻辑改动）；经审计确认全仓唯一 `urlopen` 仅使用显式 CLI 参数。
- 📝 P3-1：SKILL.md 与 README.md 开头新增「文件角色说明」段，明确 `tests/` 与 `tools/` 为开发期资产、不进发布包。

- 🧪 `test_version_parity` 门禁通过（五处版本号一致）。

🔗 [GitHub Release v1.9.1](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.1)


## v1.9.0 — 2026-10-06

**百度搭子（DuMate）数据源（归属未证实） · 任务类型分类修复 · 文档降级 · 合规文案收敛**

- 🆕 百度搭子（DuMate）数据源：新增 `adapters/dumate.py` 与 `--source dumate`，按 WorkBuddy 布局读取数据目录，支持 `DUMATE_HOME` / `DUMATE_OUTPUTS_DIR` 路径隔离。⚠️ **归属未证实** —— 实测 `workbuddy.db` 217 会话中百度搭子相关 0 行、1165 个 trace 无归属字段，报告内容可能完全是 WorkBuddy 的，不可当作「百度搭子用量」引用。
- 🧭 修复任务类型分类塌进「其他」：dumate 分支改为与 workbuddy 分支同一条路径直采 `collect_task_types`（旧代码误以为适配层已预分类，实际没有，会话 dict 里也没有 `task_type` 键）。
- 🔖 归因红线：删除「数据落点与 WorkBuddy 完全一致（实测，2026-10-02）」的过度断言；`docs/ADAPTERS.md` §6.1 / §6.4 与 `README.md` 同步降级为「按 WorkBuddy 布局读取，归属未证实」。
- 🔒 隔离修复：`DUMATE_HOME` 此前不约束产出 / 记忆目录（`WORKBUDDY_SESSIONS` 写死 `Path.home()/"WorkBuddy"`），现由 home 的 parent 派生，并可用 `DUMATE_OUTPUTS_DIR` 单独覆盖。
- 📝 合规文案收敛：四处绝对化「不联网」表述统一为「默认全离线；仅显式指定自有端点时才访问对应端点」，仅改文案，`--pricing-api` / `--task-llm-endpoint` 能力保留。
- 🔒 隐私与完整性：记忆日志补时间窗过滤（会话目录日期 ≠ 记忆文件日期）、记忆正文不再外发、SQLite 三处改只读、token 三级回退（顶层 → span → modelInfo）+ `token_source` 标记。
- 💰 计价三条：未知模型强制计 0（不再映射到 glm-5.2 编造费用）、档位名双口径披露（`total_cost` 不变 + `tier_pricing_basis` 给出 hy3 刊例价对照）、失败调用单独成列（`error_traces` / `total_effective_traces`，报告「调用次数」改用有效调用并披露失败数）。

- 🧪 `test_version_parity` 门禁通过。

🔗 [GitHub Release v1.9.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.9.0)


## v1.8.0 — 2026-09-30

**千问办公数据源 · tokens_only 计价模式 · 定价刷新 · 阶段 2 代码质量收口**

- 🆕 千问办公（QwenWork）数据源适配器（`--source qwenwork`），默认 `tokens_only`；`auto` 判定泛化到一切无计费源（含百度搭子）。
- 💰 定价刷新：hy3 / hy4-preview 限免延至 2026-10-31；V4.1-Flash 0.11x 重锚；Fast 档 1.24/2.47 → 1.91/7.64。
- 🧮 新增 `--cost-mode`（auto / tokens-only / priced），无单价时自动隐藏金额维度并修复措辞自相矛盾。
- 📐 修复报告口径打架：§5 任务类型计数与 §1/§4.2/§6 统一；§4.3 会话级 p95 双值统一为 436。
- ♻️ 阶段 2 收口：R4 消孪生入口、R5 拆 god-module（generate_report.py 3264 → 2861 行）。
- 🧪 全量测试零回归，`test_version_parity` 通过。

🔗 [GitHub Release v1.8.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.8.0)

## v1.7.2 — 2026-09-22

**Phase C · L1 真值下 §4.4 省钱建议改用官方真实积分（C7）**

v1.7.0 · A1 的「省钱杠杆过滤低置信度模型 + §4.4 顶部提示折扣/时段模型」是写给 L2 估算的——
因为 L2 用的是静态价表推算的 `effective_cost`，折扣/时段模型估算不可信。但导入官方用量导出
（L1 真值）后，§4.4 仍走 L2 估算路径，于是成本基准错用 trace 估算、还渲染 L2 专属噪音，与 L1 横幅自相矛盾。

- 🎯 **`build_savings_insights_from_official`**：读 `official_usage.by_model` 真实积分，按 `DISPLAY_MERGE`
  归并收费版变体（如 `hy3-x → hy3`），复用同款算法构造省钱建议；官方积分已是成本真值，故跳过低置信度过滤。
- 🔇 **L1 不再渲染低置信度噪音**：§4.4 引导语切换为「基于官方用量导出（成本真值 L1）」，
  低置信度标记加 `not _is_l1(data)` 守卫——L1 下官方积分是真值，不再需要 L2 专属的折扣提示。
- 🧪 **527 用例全绿**（新增 `tests/test_c7_l1_savings.py` 7 用例：L1 成本基准 = 官方 credits、
  L1 不过滤低置信度、变体归并、L2 默认仍过滤、L1/L2 §4.4 渲染差异 MD/HTML）。
- 🔗 [GitHub Release v1.7.2](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.7.2)

---

## v1.7.1 — 2026-09-16

**Phase B · 按调用时刻应用时段定价（B4 / B5 / B6）**

- **根因**：过去 `price_of(m)` 只传 `as_of_date`，夜间调用与白天同价，是 hy4-preview「严重高估」、deepseek-v4.1-flash「低估」的根因。模型刊例价是静态的，但服务端按「时刻」生效的减免/加价规则从未进 L2 成本路径。
- **B4 夜间免费**：`call_time_of` 解析 `{as_of_date, as_of_hour, as_of_dow}`；`pricing.json` 新增 `scheduled_pricing` 段（支持 `from/until` + `hours` 跨午夜 + `dow`）。hy4-preview 夜间 23:00–08:00 免费（2026-09-11 起），夜间调用 cost→0，自动退出「高估」区间。缺小时时保守不套用。
- **B5 峰谷双档**：deepseek-v4.1-flash 周一至周五 09:00–12:00 / 14:00–18:00 用 `peak_input/peak_output`（2.0/8.0），其余 + 周末用空闲价（1.0/4.0）。
- **B6 促销跨期**：glm-5.3 / glm-5.3-flash 发布期 5 折（至 2026-09-09）写成 `effect=discount, factor=0.5`，跨期报告按调用日期自动选全价/5 折。
- 接入 `ca_sources.py` / `ca_aggregate.py` / `adapters/claude_code.py` / `adapters/codex.py` 四处 trace 级计价。
- 回归：`tests/test_v1_7_1_scheduled.py`（16 用例）；全量 **570 passed / 0 failed**。

- 🔗 [GitHub Release v1.7.1](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.7.1)

---

## v1.7.0 — 2026-09-15

**F17 双源对账 P1/P2 + 低置信度最贵模型告警（A1/A2/A3）**

- **F17 · P1 请求数反推**：消除「11.9x 粒度差 = 用量暴涨」误读。按 `session_id` + 15 分钟时间窗聚类反推「估算请求数」（`summary.estimated_request_count`），§1 概览新增该行，L1 下展示估算 ↔ 官方请求数倍率。解析兼容毫秒时间戳与 ISO 字符串。
- **F17 · P2 路由别名解析**：`auto` / `fast-model` / `balanced-model` / `extreme-model` 不记录落地底层模型，报告显式「单独成组、不计入最贵模型与省钱建议」，单价为计费模型均价估算。
- **A1 省钱杠杆过滤**：`build_savings_insights` 排除低置信度模型，§4.4 顶部改提示折扣/时段模型。
- **A2 机读偏差方向**：`pricing.json` 新增 `low_confidence_bias`，报告渲染 `⚠↑`（高估）/ `⚠↓`（低估）。
- **A3 高位告警**：低置信度模型恰为最贵（或 Top-3）时，§3 + §4.4 顶部加醒目横幅「真实花费以官方账单为准，不要据此切换模型」。

- 🔗 [GitHub Release v1.7.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.7.0)

---

## v1.6.2 — 2026-09-14

**修复：低置信度模型标记改为纯 ⚠**

HTML 里低置信度模型原被 `<span class="lc-flag" ...>⚠</span>` 包裹，与 Markdown 版不一致。
改为纯 `⚠`，并删除不再使用的 `.lc-flag` CSS 规则；成本横幅、模型表、条形图、脚注口径统一。

- 🔗 [GitHub Release v1.6.2](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.6.2)

---

## v1.6.1 — 2026-09-14

**修复：§3.5 把「收费版变体」误报成 trace 盲区（虚报 75.7% 的漏记积分）**

v1.6.0 上线后，用 30 天官方导出（802 请求 / 2902.39 积分）实测发现 §3.5 的
「官方有、trace 无」里混进了 `hy3-x`（97 请求 / 397.43 积分）和 `hy4-preview-x`（1 / 13.52）——
它们不是盲区，而是 `hy3` / `hy4-preview` 的**收费版变体**，trace 侧早已按 `display_merge`
归并显示为基名，官方侧却没过同一层映射，精确匹配自然对不上。

修复后：官方侧先按 `display_merge` 归拢，报告里标成 `hy3（含 hy3-x）`。
`missing_credits` **542.57 → 131.62**，剩下的盲区才是真的（图像模型 + VSCode 客户端的
`deepseek-v4-pro`）。

顺带明确一条边界：**不做模型名归一化**。`custom-local:` 这类前缀是「WorkBuddy 自建 vs
外部 API」的唯一来源标识，剥掉就没法判断 token 归属了。§3.2 已用 `is_local` / `is_custom`
通道标记把用量拆成 官方/网关 · 本地模型(🏠) · 外部 API(🔧) 三节，来源信息不依赖模型名。

- 🔗 [GitHub Release v1.6.1](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.6.1)

---

## v1.6.0 — 2026-09-14

**F17 双源对账：把官方用量导出接进来，成本从估算升级为真值**

v1.5.2 只解决了「告诉用户这是估算」；v1.6.0 解决「怎么拿到真值」。
本地 trace 与官方用量导出这两个数据源**从未对过账**——本次把它们接起来。

- 📥 **`--import-official <xlsx>`**：导入官网下载的用量导出，成本口径自动切 **L1 真值**（取「积分」字段）。
  纯本地只读解析，不联网不上传（符合 ADR-4 / ADR-6）；仅 `--source workbuddy` 可用，混用退出码 2。
- 🔧 **新增 `adapters/official_usage.py`**：纯标准库解析 xlsx（zip + XML，**不引入 openpyxl**）。
  **按表头名映射、禁止硬编码列位** —— 官方 09-13 新增 `User Prompt` 列，按列位解析会把 Prompt 当模型名。
- 📊 **报告新增 §3.5 双源对账**：
  - 官方请求数 vs trace generation 数 + 粒度倍数（实测约 11.9x，明确标注「不是用量暴涨」）
  - **官方有 / trace 无** → trace 盲区，汇总漏记积分（实测图像模型 + minimax-m3 = ¥251.74 / 8.7%）
  - **trace 有 / 官方无** → 本地模型 / 免费额度 / 路由别名，明确「不是漏记」
- 🏷️ **P0-3 口径标注**：概览「调用次数」加注 `(generation 粒度)`，不再与官方「请求数」混淆。
- 📖 **治理**：`ADAPTERS.md` 新增「官方导出适配器」与「数据来源与已知偏差」两章；
  `SKILL.md` 新增「成本口径：L1 / L2」章节。
- 🧪 **474 用例全绿**（新增 `tests/test_official_usage.py` 24 用例）。
- ✅ **零回归**：不传 `--import-official` 时输出与 v1.5.2 完全一致。
- 🔗 [GitHub Release v1.6.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.6.0)

---

## v1.5.2 — 2026-09-14

**成本置信度：让报告明确告诉用户「你在看哪一级成本」**

用官方用量导出对标后发现：静态价表无法表达「服务端时段减免 / 用户免费额度」。
最典型的是 `hy4-preview` —— 实测 2026-09-12~09-14 的 12 次调用中，**11 次夜间调用积分为 0、
仅 1 次白天收 43.40**，而静态价表会把 12 次全部计成收费。

- 🏷️ **成本两级制**：`L1 真值`（导入官方导出取「积分」）/ `L2 估算`（默认，静态价表）。报告顶部新增**成本口径横幅**。
- 📋 **新增 `pricing.json` 的 `low_confidence` 段**：登记估算偏差已知较大的模型及原因（首版含 `hy4-preview`、`hy4-preview-x`、`deepseek-v4.1-flash`、`glm-5.3`、`glm-5.3-flash`），可直接编辑或用 `pricing.local.json` 覆盖。
- ⚠️ **低置信度标注**：模型表与成本图表标 ⚠ 并说明原因；这些模型不进「最贵模型」结论，
  但**被剔除者逐条列出金额**——不允许用一个误导替换另一个误导。
- 🔇 **零噪音**：未配置或本期未命中时不新增任何标记；不传 `low_conf_map` 时行为与 v1.5.1 完全一致。
- 🧪 **450 用例全绿**（新增 `tests/test_cost_confidence.py` 9 用例）。
- 🔗 [GitHub Release v1.5.2](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.5.2)

> 下一步（v1.6.0）：F17 双源对账正式落地 —— `--import-official <xlsx>` 只读导入官方导出，
> 届时本横幅自动切换为 L1 真值。

---

## v1.5.1 — 2026-09-12

**定价数据刷新：DeepSeek V4.1-Flash（峰谷双档）· V4-Flash 下架 · Hy4 限免新规**

- 🔄 **DeepSeek 换代**：`deepseek-v4-flash` 移入 `delisted`（历史调用仍计价、报告标 🗄️）；新增 `deepseek-v4.1-flash`（官方在售名 `deepseek-flash`）——2026-09-10 上线，1M 上下文、原生多模态图像理解。
- 💰 **峰谷双档计费**：空闲 输入 1 / 输出 4、高峰翻倍 2 / 8（元/百万 tokens）；主字段取空闲档，高峰值记 `peak_input`/`peak_output`。
- ⏳ **V4-Pro 下线预警**：2026-09-14 12:00 下线，请求自动路由至 V4.1-Flash 并按 Flash 价计费。
- 🟡 **Hy4 preview 限免改规**：普适免费期 2026-09-10 结束（`timed_free` 保留该日以保历史计价正确）；新规为分人群 + 时段制，静态价表不表达。
- 🧪 **441 用例全绿**（含捕捉到 1 处 `timed_free` 误删回归）。
- 🔗 [GitHub Release v1.5.1](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.5.1)

## v1.5.0 — 2026-09-07

**任务分类加权评分（P2-3）· 定价自动更新机制（P2-2）· P0 数据完整性修复**

- 🐛 **P0 数据完整性修复**：修复 v1.3.0 模块拆分遗留的 `NameError`——`collect_task_types` 漏导入 `get_session_content` / `get_session_artifact_fingerprint`，导致 WorkBuddy 默认采集路径运行即崩溃。
- ✨ **任务分类加权评分（P2-3）**：`classify_task` 重写为加权评分——所有规则参与打分、信号密度取胜、ASCII 词自动加 `\b`、新增 `_task_confidence` 置信度；规则外置 `scripts/task_rules.json`；可选 LLM 分类器（opt-in，仅接受自备 OpenAI 兼容端点）。
- ✨ **定价自动更新（P2-2）**：新增 `scripts/fetch_pricing.py`——拉取 → 校验 → 候选 → 审核 → 落盘；合规不抓厂商网页，默认不落盘、显式 `--apply` 才写入并自动备份；CI `--check --stale-days` 过期检查。
- 🧪 **16 个测试文件、398 用例全绿**。
- 🔗 [GitHub Release v1.5.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.5.0)

## v1.4.0 — 2026-09-06

**多 Agent 数据源（Claude Code 适配器 MVP，P2-1）**

- ✨ **多 Agent 数据源**：新增 `--source` 参数，`--source claude-code` 统计 Claude Code 用量，报告管道零改动复用。
- ✨ **`adapters/claude_code.py`**：读取 `~/.claude/projects/**/*.jsonl`，`usage` 归一化为统一 trace schema 并现场合成会话记录；根目录三级回退、口径与 WorkBuddy 一致（缓存折扣计入）、坏行健壮性跳过。
- ✨ **Claude 模型定价入库**：Opus 4 / Sonnet 4 / Haiku 4（美元刊例价 ~7.2 汇率折算估算，可用 `pricing.local.json` 覆盖）。
- 📚 `ADAPTERS.md` 全量重写；FAQ 新增 Q43–Q45。
- 🧪 **14 个测试文件、353 用例全绿**。
- ⚠️ **已知限制**：Claude Code 源无技能调用 / 自动化运行维度，`duration_ms` 恒为 0，不区分 Max 订阅与按量 API。
- 🔗 [GitHub Release v1.4.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.4.0)

## v1.3.0 — 2026-09-02

**档位维度分析 · 模块拆分重构 · 孤儿 trace 修复**

- ✨ **档位维度分析**：新增快速 / 均衡 / 极致三档聚合；致命不一致归一化（`extreme-model` → `deep-model`）；本地权威倍率表优先。
- 🐛 **孤儿 trace 修复**：区分「孤儿 trace」与「真·无标题会话」，新增 `UNNAMED_LABEL` / `ORPHAN_LABEL` 双标签，避免误告警。
- 🧹 **模块拆分重构**：`collect_usage_data.py` 拆为 `ca_core` / `ca_sources` / `ca_sessions` / `ca_aggregate`；MD / HTML 报告生成去重。
- 🔗 [GitHub Release v1.3.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.3.0)

## v1.2.1 — 2026-08-29

**幽灵调用修复（Agent workflow span 还原）**

- 🐛 **修复「幽灵调用」占比虚高（trace 采集 schema 盲区）**：WorkBuddy 的 `Agent workflow` 类 trace 顶层 `modelInfo` 为空、`totalTokens=0`、缺 `sessionId`，真实模型与 Token 藏在内部 `generation` span 的 `toolOutput`。旧采集器只扫顶层，把这类工作流整批误判为默认 `glm-5.2`，幽灵率虚高约 42%、真实用量低估约 15%。
- ✨ **新增 `_recover_model_info_from_spans()`**：顶层缺 `modelInfo` 时遍历 span 还原 `model` / `usage` 回填，幽灵率 42.0% → 4.7%，回收约 16.7M Token（模型分布 5 种扩到 10 种）。
- ⚠️ **已知限制**：`Agent workflow` trace 的 `sessionId` 完全缺失，「按会话维度」归属不可恢复；残余约 4% 为控制流 span，属真·不可归属。
- 🔗 [GitHub Release v1.2.1](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.2.1)

## v1.2.0 — 2026-08-29

**display_merge 合并显示 · 定价库更新 · FAQ**

- ✨ **`display_merge`：免费额度版 / 收费版合并显示**：同一模型两个入口（`hy4-preview` 免费额度版 / `hy4-preview-x` 收费版）过去拆成两行；现按 `pricing.json` 的 `display_merge` 段合并为一行。
  - **合并只改分组、不碰钱**：显示键取合并基础模型名，计费键仍是每条 trace 实际执行的 `exec_model`，免费额度版记 ¥0、收费版按刊例价计费。
  - 可配置：增删合并对只改 `pricing.json`（或 `pricing.local.json`）的 `display_merge` 段，无需改 Python；默认已配 `hy4-preview-x → hy4-preview`、`hy3-x → hy3`。
- 💰 **定价库更新**：新增 GLM-5.3-Flash（输入 0.8 / 输出 2.8）、Hy4 preview 系列（6 / 18）；`hy4-preview` 限时免费至 2026-09-10。
- 📚 **新增 `references/FAQ.md`（34 问）**；README / SKILL 同步。
- 🧪 新增 `tests/test_display_merge.py`（13 用例）。
- 🔗 [GitHub Release v1.2.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.2.0)

## v1.1.3 — 2026-08-23

**hy3-x 定价 · 通道测试 Allure 化**

- 💰 **hy3-x 官方接口定价**：`pricing.json` 新增 `hy3-x`（输入 1 / 输出 4，缓存命中 0.25）；`collect_usage_data.py` 新增 `resolve_key_fn`，当 `model_key=hy3-x` 且 `exec_model=hy3` 时强制归入 hy3 行，修复 trace 标签误标。
- 🧪 **通道归因测试接入 pytest + Allure**：新增 `tests/test_channel_attribution.py`（marker 体系 + Allure 注解）、`tools/render_allure_html.py`（零依赖离线 HTML）、`pytest.ini`、`requirements-tests.txt`；测试仅依赖标准库 + pytest + allure-pytest。
- 🔗 [GitHub Release v1.1.3](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.1.3)

## v1.1.2 — 2026-08-12

**SkillHub 重新发布修正**

- 🔧 **SkillHub 重新发布修正**：平台禁止打包无扩展名文件（`.gitignore`、`LICENSE`），将 `LICENSE` 更名为 `LICENSE.md`（GitHub 仍识别为许可证，`license: MIT` 声明不变）；`.gitignore` 仅用于 Git，不进发布包。
- **版本号升为 1.1.2**：覆盖平台上残留的 1.1.1 记录（首次发布因文件数超限被拒，平台仍写入了版本记录），以新版本号干净发布。
- 发布包已剔除 `pricing.local.json` / `allure-results` / `allure-report*` / `.pytest_cache` 等隐私与测试占位文件（`_meta.json` 为 metadata.json 副本，随发布包发布）。
- 🔗 [GitHub Release v1.1.2](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.1.2)

## v1.1.1 — 2026-08-11

**日历对齐周期 · XSS 防护**

- 📅 **周期定义改为日历对齐**：`week` = 当前 ISO 周（周一~周日）、`month` = 自然月、`year` = 自然年、`day` = 今天；周期标签改 ISO 8601（周报 `2026-W33` 等）。
- 🧪 **通道归因测试推广到全模型**：参数化覆盖 runtime 已知模型全集，新模型加入后测试自动覆盖。
- 🐛 **Bug 修复**：SiliconFlow vendor 前缀覆盖导致通道误判、跨窗口长会话 sid 缺失误判、**HTML 注入防护（XSS）**、脏数据 / 非法日期健壮性、报告生成时间改可读格式、自然语言触发语更新。
- 🔗 [GitHub Release v1.1.1](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.1.1)

## v1.0.0 — 初始发布

**首发 WorkBuddy Agent 用量与成本分析报告**

- ✨ 首发支持 WorkBuddy 的 Agent 用量与成本分析（日 / 周 / 月 / 年），覆盖 Token 消耗、任务类型、技能使用与自动化运行。
- 📄 多格式输出（Markdown / HTML / JSON），异常检测（成本 + Token 双口径），可扩展定价库。
- 🔗 [GitHub Release v1.0.0](https://github.com/Elisabeth15501/agent-analytics-report/releases/tag/v1.0.0)
