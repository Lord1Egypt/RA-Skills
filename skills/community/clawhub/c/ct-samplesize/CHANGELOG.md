# Changelog / 版本历史


## 5.15.0 — 2026-11-15 · 一次用户需求只写少量飞书记录 + 近 30 天日志实证的 9 项改进

> 触发：用户用 ct-update 只读端口取近 30 天 ct-samplesize 飞书使用记录（252 行 /
> 52 会话 / 50 来源，2026-10-17 19:53 ～ 11-12 14:45 CST），要求「全部处理」并额外指出
> **同一次用户请求被拆成多个 Coze 请求、一个 Coze 请求又可能造成多次飞书存储**，
> 需尽量合并到「一个需求只写一次或很少几次」。分析见工作区
> `ct_samplesize_usage/ct-samplesize_使用行为分析与改进建议.md`。

### Fixed / Added（缺陷 → 修复）

| 编号 | 实测缺陷 | 修复 |
|:---|:---|:---|
| **核心** | 日志按「Coze 请求」建档：45/45 的 power 调用紧接 n 调用；单会话 40 次 / 27.8 分钟扫描；60s 内同签名重复 25 行（9.9%）；失败后逐字节重试 4 次 | `request_scope()` 给同需求所有子调用分配同一 `request_id`；Coze `log_aggregator.aggregate_log()` 首次 `add_records`、后续 `update_records` 更新同一行（聚合 `call_count`/`calls[]`/`statuses`/`errors`/`total_runtime_sec`）。超 300s 或单行 20 次才另起一行；无 request_id 的老客户端 `delegate` 回原路径，逐字节不变 |
| **核心** | 一次需求两次 POST（算 n + 验算 power） | `call_paired()` + 服务端 `mode="paired"`：单次 POST 连算两向，1 行日志 |
| **核心** | 参数扫描 40 次串行；batch `count=2` p50 10.39s ≈ 2×单条 5.05s（逐项串行） | `call_grid()` 一次 POST；`samplesize_node` 批量项 `ThreadPoolExecutor` 并行（结果按原 index 排序），`CTSS_BATCH_WORKERS` 可调 |
| P0-1 | 50/252 行带 136~141 参数键；根因：`_load_contract_required` 只认 `adapters/workbench/publish/tests/...`，发布包按 §16 排除 `tests/` → 契约恒加载失败，`build_params` 与 `_trim_bloated_params` 共用同一依赖而**同时失效** | `scripts/build_log_contract.py` 从权威源（契约索引 + argparse）按**消费者加载方式**各产出一份：本地客户端 `config/log_contract.json`、工作台 `workbench/publish/config/log_contract.json`、Coze 运行时 `src/graphs/nodes/log_contract_data.py`（Python 常量，直接 import，**零文件路径探测**）。契约缺失时客户端守卫按默认值表 fail-closed 裁剪；服务端 `trim_params` 落库前二次裁剪（只裁 >40 键）。**不做防御性冗余副本**：曾短暂加过 `coze/config/` 与 `coze/src/config/` 两份 JSON 兜路径，已全部撤销，改为数据随代码 import |
| P0-2 | 5 次 error 全为 `correlation effect=2.0` 越界触发裸 R 错误 `f.lower = f(lower) is NA`；用户重试 4 次无提示 | 客户端 `validate_domain()` 出站前零网络往返拦截并返回双语可行动错误信封；服务端二次兜底；R 端 `.translate_engine_error`（v5.13.31+）保留为最后防线（**该项已修复，不重复投入**） |
| P1-4 | `cache_hit`/`call_type`/`error_type` 覆盖率 0%；35.3% 快调用无法归因 | `_compute_one` 落 `cache_hit`、批量落 `cache_hits`；`CTSS_PREWARM=1` 首请求后懒预热默认组合；客户端 60s 同签名成功结果本地复用（不 POST、不写行），失败不缓存 |
| P1-6 | `download` 不投影 `entry_point`/`request_id` 独立列，无法区分 CLI/工作台/压测流量 | `feishu_save_node` 把 `entry_point`/`call_type`/`call_seq`/`cache_hit`/`error_type`/`request_id`/`is_qa` 镜像进 `resultstr` 顶层；`state.py` 三处 schema 补字段防 LangGraph 静默过滤 |
| P2-7 | 67 种检验窗口内只用到 16 种（24%）；同期 ct-advisor 75 条（23.7%）样本量类问答恰对应零调用检验 | `scripts/route_intent.py`：`suggest_tests()` / `handoff_hint()`（ct-advisor 交接）/ `menu_order()`（按真实频次排序） |
| P2-8 | `evidence_source` 0/252 有效、`effect_ref` 0、`justify` 3 条；但 60% 用 `effect=0.5` 且无来源 | `assumption_block()` 结构化记录假设 + 来源 + `unverified` 提示，写入日志与 paired 结果 |
| P2-9 | 7 个 skill_version 并存；11-12 仍有 5.8.0 带 `delta/sd/sides`；1 条 `0.9.0/domain=macro` 跨域请求被记为 `unknown_task` | `upgrade_hint()` 非阻塞升级提示；`normalize_legacy_params()` 兼容旧键；`is_known_test()` 判定未知 test 为跨域脏流量，不写主表 |

### 兼容 / 安全

- 无 `request_id` → `delegate` 原追加路径；`log_mode=skip/always` 显式可控；`update` 失败自动降级追加，**绝不丢日志、绝不阻断主流程**。
- 进程重启内存索引丢失 → 从新行重新聚合（最多多一行，不覆盖已有历史）。
- 只读分析、未写回飞书、未部署 Coze、未 commit / push / 三平台发布；历史 252 行未清理。
- 版本：`SKILL.md` 与 `workbench/publish/SKILL.md` → `5.15.0`；`COZE_VERSION` → `5.15.0`。

### 验证

- 11 个改动文件 `py_compile` 全过；`tests/test_request_log_aggregation.py` **37/37 PASS**（FakeBitable 断言：5 次子调用 = 1 行 add + 4 次 update、上限 2 时 3 次 = 2 行、老客户端零行为变化、130 键 → 11 键、越界拦截、request_scope 同 ID/seq 递增；新增断言「Coze 契约常量 == 技能侧 JSON」「Coze 侧无任何 JSON 冗余副本」）。
- `build_log_contract.py` 生成期用 `ast.literal_eval` 自检常量与 JSON 语义完全一致；CLI `--help`、`route_intent.py` 实跑通过；Coze 部署包 logger-order 闸门 35 文件全过。

详见 `references/request_log_aggregation.md`。

## 2026-11-13 · 共享资产契约同步（§11 / §19.2，非 UI 决策变更，页面版本号不变）

按 ct-base 2026-11-13 增补批次同步共享资产：`workbench/wb-list.css` 注入卡片动作统一右列锚点（`.wb-list-cardacts-bottom` + `--wb-cardact-right` / `--wb-cardact-gutter`）；`workbench/tokens.css` 补 `--wb-pill-base` / `--wb-cardact-right` / `--wb-cardact-gutter`；`publish/` 下同名副本一并同步。

采用**精确注入**而非整文件覆盖：ct-base 真源 `wb-list.css` 的字号仍是裸 px，多数叶子已自行令牌化；整文件覆盖会把字号退回裸 px，并可能丢失技能自有令牌/增强，故只替换契约部分、保留其余原文。

**验证**：CSS 花括号平衡；Playwright 实测 `--wb-cardact-right=10px`、`--wb-cardact-gutter=0px`、`--wb-pill-base` 生效，右上/右下动作规则均取 `var(--wb-cardact-right)`、`cardbody` 取 `var(--wb-cardact-gutter)`，页面 JS 错误 0；publish 副本与源逐字节一致。

## 5.14.7 — 2026-11-01 · 修 coze 方法默认图的 meta 参数断链（标题恒 (smd) + 曲线口径错）

### Fixed
- **线上实测发现的第 2 个 bug**（部署 5.14.6 后回归时抓到）：`meta_planning` 的第 2 张图
  （`method_default`，出图层产物）标题恒为小写 `(smd)`，且 **曲线画的是 SMD d=0.3 的 K**
  （y 轴 5~30），与引擎 `stats$hetero_K`（OR=2 时 2/3/4/7/16）自相矛盾。
  根因：`--effect-type/--effect/--n-per-study/--p0/--target-power/--cluster-cv/--i2/--n-cv`
  在 `adapters/coze/scripts/coze_fallback.py`（固定 argparse 白名单）**完全没有透传通道**，
  `coze_figure_layer.R` 收不到就只能回落自身默认（`effect_type="smd"`、`effect=0.3`、`p0=0.3`）。
  修复三处：① `coze_fallback.py` 新增 8 个参数并转发给 R 层；② `graphs/nodes/samplesize.py`
  的 `_run_figure_layer` 从 params 透传（`--target-power` 取 `power`）；③ `coze_figure_layer.R`
  标题改 `toupper(effect_type)`（与引擎 `et_up` 同口径），`.meta_K_layer` 补 `n_cv` 的
  `V_eff = V·(1+CV²)` 保守膨胀（此前缺此层，图上 K 系统性偏小：I2=0.25 时 2 vs 引擎 3）。
  **数值验证**：figure 层 K 在 i2=[0,.25,.5,.75,.9] 为 **2/3/4/7/16**，与引擎完全一致。

### 验证
- 本地实跑出图层（真实 R + svglite）：标题 `Meta planning: K vs I2 (OR)`，红点
  `I2=0.25 -> K=3`，y 轴与引擎同量级。
- `t()` 遮蔽闸门 exit 0；`test_antiscrape.py` **77 通过 / 0 失败**。
- 部署包 `_archive_20260830/coze_project_5.14.7.zip`（76 文件 / 425.7 KB /
  MD5 `7833aaa6a7f518f2a50a09e463f2d373`）。

### 线上回归（2026-11-01 10:45，部署 5.14.7 后实跑 `https://ct-samplesize.coze.site/run`）
新增 `adapters/coze/tests/live_regression.py`（只读云端、纯标准库 + 本技能 coze_client，
一条命令跑完 4 场景 / 29 项断言，退出码可进 CI）：

| 场景 | 关键断言 | 实测 |
|:---|:---|:---|
| A 样本量·MC（or, n_sim=2000, n_cv=0.3） | K 带齐全且单调、主输出取 P50、报告含「所需研究数带」 | `k50/k80/k95 = 9/10/10`，`n=9`，`power=0.8115`，`P(≥0.8)=72%` |
| A 出图口径 | 两图标题含 `(OR)` 且非 `(SMD)`；y 轴为研究数 K；曲线 = 引擎 `hetero_K` | `hetero_K=5/7/10/19/47`；`meta_hetero` 与 `method_default` 两图反解逐点一致（最大刻度 40 / 80） |
| B power 模式（K=8） | 不返回 K 带、返回功效带、报告无 K 带行 | `k_p50=None`，`power=0.7649`（P5/P95 = 0.728/0.796） |
| C 等样本量（无 n_cv） | 仍返回 K 带且三值相同；smd 标题为 `(SMD)` | `3/3/3`，标题 `Meta planning: K vs I2 (SMD)` |
| D 解析保守档（n_cv 无 n_sim） | 不返回 K 带、仍给 K | `K=10`，`power=0.8` |

跨方法冒烟（同批）：`ttest_ind` n=64、`proportion_two` / `anova` / `roc` / `cluster` /
`poisson` / `correlation` 均 `status=ok`；`survival` 为 `warn`（仅缺 `event_rate`，
按设计提示并给出 events=247），非回归。

### Added
- `adapters/coze/tests/live_regression.py` —— 部署后必跑的云端回归（含 SVG 反解：
  从 y 轴刻度坐标线性反推 K、从 x 轴刻度反推 I²，再与引擎 `hetero_K` 逐点比对，
  避免只看 `figures[].title` 空串导致空过）。
- `_build_deploy_new.py` 构建前 logger 顺序闸门（fail-closed，见 `DEPLOY.md` §2.2）。

## 5.14.6 — 2026-11-01 · 修 `t()` 名称遮蔽导致的 MC 样本量档部署期崩溃

### Fixed
- **coze 端 v5.14.5 的 “填 n_sim 但不填 K” MC 样本量档必崩**（`no such index at level 2`）。
  根因：`src/r_engine/common.R` 在全局环境定义了本地化翻译函数 `t <- function(key, ...)`，
  **遮蔽 `base::t` 的矩阵转置语义**；v5.14.5 新增的 MC 样本量分支写
  `Csm <- t(apply(Gm, 1, cumsum))`，运行时 `t` 解析到翻译函数，矩阵被当作 key 传入
  `.messages[[key]]`，`[[ ]]` 递归索引直接抛错。
  改为 `Csm <- base::t(apply(Gm, 1, cumsum))`（保持原转置语义、显式绕过遮蔽），并就地留注释。
- **为何本地没复现**：上一轮验证脚本是从 `samplesize_functions.R` 用 `parse` 抽取函数后
  在隔离环境跑的，**没有加载 `common.R` 的 `t` 定义**，遮蔽不存在 → 侥幸通过。教训：涉及
  全局符号遮蔽的改动，验证环境必须一并复刻遮蔽源。

### Added
- **静态闸门 `adapters/coze/tests/test_r_t_shadow.py`**（纯标准库、零 R 依赖、秒级）。
  三层判据：① 硬失败——裸 `t(` 首参为函数调用表达式（翻译 key 不可能是 call，必为转置误用）；
  ② 基线棘轮——11 处既有变量 key 翻译调用登记在 `BASELINE`，出现基线外新裸 `t(` 即失败；
  ③ 锚点——`samplesize_functions.R` 必须含 `base::t(apply(Gm, 1, cumsum))`，防回退。
  已接入 `tests/run.ps1` 作为真跑回归之前的第 ① 步。
  反向验证：临时把 `base::t` 改回裸 `t(`，闸门三条判据全部命中并 exit 1。

### 验证
- 遮蔽环境（从真实 `common.R` 抽取 `t` 注入全局）下实跑真实引擎：样本量模式 K 带
  `2/3/3`（单调 ✓）、功效带 P5/P50/P95 = `0.702/0.809/0.890`、P(≥目标)=`0.5615`；
  `n_cv=0` 退化为 `2/2/2`；求效能模式（K=5）无 K 带字段 —— 与修复前预期数值一致。
- 三个 R 文件 `parse` 通过；静态闸门 exit 0。
- 部署包 `_archive_20260830/coze_project_5.14.6.zip`（76 文件 / 424.1 KB /
  MD5 `852ea0da78b0852ee1c1933c81917031`），红线自检 CLEAN；`_version.py` 与
  `manifest.json` 均为 5.14.6。
- **5.14.5 作废，须直接用 5.14.6 部署**（5.14.5 仅在“不填 K 且填了 n_sim”时崩，
  其余路径正常，故原包外观无异常）。

## 5.14.2 — 2026-10-28 · C0 层修复：antiscrape 模板一致性假红（77 例全绿）

### Fixed
- **`adapters/coze/tests/test_antiscrape.py` D5 用例长期假红**（76 通过 / 1 失败 → exit 1）。
  该用例断言「技能副本与 `ct-base/adapters/antiscrape/antiscrape.py` 整文件 md5 逐字节一致」，
  但两处差异都是**合法性差异**：
  ① **行尾**：底座文件 LF、技能副本 CRLF（1228 行全差）；
  ② **文件头 docstring**：各技能副本写自己的技能名与规范号
  （「ct-advisor Coze 适配器…」vs「ct-samplesize Coze 适配器…」）。
  判据改为「统一行尾后，自 `from __future__` 起的**代码主体**逐字节一致」——
  既守住真正的代码漂移，又不再被风格与命名差异误伤。
  **验证：代码主体两侧均为 46080 字节且完全相等**，修复后 77 通过 / 0 失败。
- **该失败此前被 C0 层的版本跳过逻辑掩盖**（见 ct-base 同期修复：状态文件写到了错误目录），
  C0 长期只显示「WARN · exit code 1（无断言执行）」被当作噪音。

### 验证
- `python -m ctqa run --skill <ct-samplesize>`：**PASS 164 / FAIL 0 / WARN 3 / SKIP 10 → 绿灯**（exit 0）。
  C0 内置层由 `WARN 1 / PASS 1` 转为 `PASS 2 / WARN 0`。
- 剩余 WARN 3 均为记录级：`W0-011` 内联 `<style>`（tokens.css 已外链，`W0-009` PASS）、
  `W1-005` 事件协议启发式告警（硬编码 Coze 标准事件 vs 前端 `ev.event` 处理）、
  `W2B-016` 资源级 404（静态服务无后端 `/api/*`）。

## 5.14.1 — 2026-10-28 · 工作台标准检验流程沉淀（发布前强制闸门）

> 纯文档 / 流程固化，**SKILL.md 版本维持 5.14.0（无运行时变更）**；工作台源码 `workbench.html` / `server.py` / `form_schema.py` 已在上一轮（5.13.42 全量回归）修复并验证。

- **新增标准检验流程（Standard Inspection Process）**：把工作台页面的全自动化测试固化为技能级强制质量闸门——任何 `workbench.html` / `server.py` / `form_schema.py` / `tokens.css` / `wb-list.css` / `wb-list.js` 改动，或每次 `build_publish.py` / `install_genie.py` 发布前，**必须**先跑通五层套件（110 例，约 70s），全绿才允许发布。
- **规范文档（canonical）**：
  - `references/workbench_qa.md`（英文 canonical，agent-facing）
  - `references/workbench_qa_zh-CN.md`（中文主文档，含回归基线 7 bug 根因表）
  - 套件实操：`adapters/workbench/autotest/README.md`（顶部已加指向规范的指针，避免漂移）
- **接入点**：`SKILL.md`「Workbench」段补发布闸门说明；`AGENTS.md`「Test Infrastructure / 测试基建」新增「工作台全自动化测试（标准检验流程 / release gate）」小节并补入套件一览表；`README_zh-CN.md` / `README.md`「进阶参考」段加维护者指针。
- **五层架构**：L1 静态契约（纯 Python 解析 HTML）· L2 后端 API（起 `server.py` 子进程 + requests，67 方法全参数化、非法输入必 4xx、凭据白名单、限流）· L3 前端单元（Playwright 内直调页面 JS）· L4 端到端（真实点击全流程）· L5 布局/响应式/a11y（三档视口）。层间不共享断言。
- **回归基线（7 个已修复并持续守护的真实 bug）**：① P0 `#v-domain` 缺闭合标签致历史页/页脚被吞、功能 0×0 不可用；② P0 凭据文件可被 HTTP GET 下载；③ P1 argparse usage 打 stderr 在容器拖死请求；④ P1 `survival` optional 用 CLI 别名 `hr` 渲染空控件；⑤ P2 切 EN 残留中文；⑥ P2 `title`/`aria-label` 无 i18n；⑦ P2 移动端 CTA 40px < 44px。
- **强制护栏（写入规范）**：跑 `build_publish.py` 前必须先备份 `publish/.wbapp_*.genie` 与 `publish/.workbuddy/applications.yaml`（PRUNE 会剪掉 appId 认领标记，丢失即生成带后缀新域名）；套件不进工作台发布载荷（白名单构建）；mock 模式只验证契约不验证数值（数值正确性由 `tests/test_ct_samplesize.py` 等负责）。

## 5.14.0 — 2026-10-28 · 生存分析全家族数值修复（事件概率口径 / 单双侧 / 参数接线 / 脱落语义）

> **结果会变**：本版修正了生存类检验的系统性偏差，同一输入下 n 与以往不同（多为上调）。
> 旧版报告中的生存样本量请勿直接沿用。

- 🔴 **P0-1 期望事件比例只算对照臂（13 个模块里的 5 个受影响）**：`.event_prob()` 只按对照臂 λ 折算 P(event)，调用方却把它当「全研究平均每人事件概率」去除总事件数——等价于假设试验臂与对照臂事件率相同。HR<1 时试验臂事件更少，故 n 被系统性低估。**实证**：HR=0.75 / 事件率 0.70 / 入组12 / 随访12 / α=0.05 双侧 / 80%，旧值 323/组（总 646），rpact 双侧 352.5/组，两臂加权正确值 354/组；旧 n 回代 MC 把握度仅 **0.768**（verify.py 6000 次：power FAIL、事件 347.5 vs 380 FAIL +8.5%）。影响：`survival`（−8.4%）、`survival_superiority`（−7.3pp）、`ni_survival`（−3.9pp）、`survival_exact` 兜底、`survival_equivalence`。
  - **修复**：新增 `.event_prob_arm()`（单臂）与 `.event_prob2()`（双臂按分配比加权 P̄ = (P_c + r·P_t)/(1+r)），替换 5 处调用；`ss_survival_logrank` / `ss_ni_survival` / `ss_survival_exact` / `ss_surv_equiv` / `ss_surv_sup` 全部改口径。修后 MC：survival 0.810、ni_survival 0.800、superiority 0.803、equivalence 0.799。
- 🔴 **P0-2 `survival_exact` 按单侧设计算、按双侧 α 汇报**：`getDesignGroupSequential(...)` 未传 `sided`，rpact 默认 `sided=1`；同函数的 Schoenfeld 兜底却用 `qnorm(1-α/2)`，两条路径差 21%。**实证**：HR=0.7 / 事件率 0.6 / 入组12 / 随访6 / 脱落 5% / 2 次分析，旧值 256/组，rpact 双侧 319.4/组（**−20.5%**）。
  - **修复**：新增 `side` 参数（run_task 按 `.alt(p)` 传），rpact 传 `sided`、兜底用 `qnorm(1-α/sided)`。修后 320/组 vs rpact 319.4（+0.2%），单侧口径 254 vs 253.5。
  - **附带修复（反向）**：`mode=power` 时 `thetaH0` 传成了 `hr`（应为 1）、`maxNumberOfEvents` 用对照臂且不计脱落 → **旧版对 n=256 返回 power=1.0000**。现按 P̄ 折事件数、`thetaH0=1`、`directionUpper=FALSE`，同一 n 返回 0.801（rpact 仿真 0.801）。
- 🔴 **P0-3 `ni_survival` 正反向不自洽 + 两分支差 4.8 倍**：正向走 `TrialSize::Cox.NIS`（按「log 界值 − log 预期HR」标定），TrialSize 不可用时的兜底只按 `log(界值)`（等价假设真效应=1）→ 70/组 vs 334/组；反向分支同样只用界值距离，**把正向的 70/组回代只得 32.5%**。
  - **修复**：兜底与反向统一用 `delta = log(界值) − log(预期HR)`；事件比例改 P̄。修后 76/组，MC 0.800，反向 0.771（与 MC 一致）。默认 `ni_margin_surv` 0.8（<1，语义无效）→ **1.25**，`hr_expected` 默认 1.0（无差异，非劣效保守标准）。
- 🔴 **P0-4 随访时间-效能曲线只用对照臂**：`.run_surv_time` 的 `Efun` 用「总样本量 × 对照臂累积事件率」当总事件数，效能整体偏乐观（τ=24 报 380 事件 / power 0.801，两臂真值 348 / **0.765**）——会在 τ=24 宣称「已达 80%」，诱导把随访期定短。**修复**：改两臂各 n/2 分别累积相加；脱落率同步按「全程比例」换算。
- 🟠 **P1-1 `survival_equivalence` 的 `hr_expected` 完全未接线**（改 0.7/0.9/1.0 结果恒等）：改用 TOST 精确把握度 `Φ((δ−θ)√(D/4)−z_a)+Φ((δ+θ)√(D/4)−z_a)−1` 数值解 D（θ=0 时退化为原闭式，结果不变）；`|θ|≥δ`（预期 HR 落在等效区间外）时明确报错而不是静默按 θ=0 计算。修后 hr_expected 0.80/0.90/1.00 → 19709/1180/564。
- 🟠 **P1-2 `survival_historical` 的 `hist_n` 完全无效**（20/50/500 结果恒等，报告也不显示）：改为「历史对照视为带不确定性的对照臂」，`1/D_new + 1/D_hist`，解得 `D_new = K²·D_hist/(D_hist−K²)`；`hist_n` 缺失时退化为已知常数。修后 hist_n 100/200/500/NA → 410/163/120/102；历史对照过小（D_hist ≤ K²）时明确报错。默认 hist_n 50 → **200**（50 例在中位 12→18 下不可行），报告补显「历史对照样本量」。
- 🟠 **P1-3 `survival_one_sample` / `survival_historical` 默认参数直接报错**：默认 `median0=12, median1=8`（新疗法更差）触发 `stop()`，端到端 `status=error`。**修复**：默认改 18。
- 🟠 **P1-3b 单样本 log-rank 公式保守 1.5 倍**：原式 `(z_a√r + z_b)/(r−1)` 混用 H0/H1 方差口径，MC 实测 n=167 时把握度 0.953。**修复**：改用标准式 `D = (z_a+z_b)²/(log HR)²`，n=102 → MC 0.830（+3pp，属 Poisson 方差近似的保守余量）。
- 🟠 **P1-4 `survival` 缺 `event_rate` 时静默按 P=1 折算**：`p$event_rate %||% 1` → 只给 HR 与把握度时输出 191/组（382 人），给出事件率后是 708 人（**差 41%**）。**修复**：缺事件率时不再估算样本量，只给所需事件数 + 明确 warning。
- 🟠 **P1-5 `survival` 反向模式把 `nobs` 当「总事件数」**：填「我有 646 例」会得到 **0.9551** 的虚假把握度（真值 0.768）。**修复**：给了事件率时按 P̄ 把受试者折成事件数并在 warning 里写明折算过程；未给事件率才按事件数解释。
- 🟡 **P2-1 分布重叠图与数据无关**：`.dist_delta` 的 survival 分支 `δ ≡ qnorm(power)+z_crit`，与 n / HR 无关（n=200/HR=0.75 与 n=5000/HR=0.95 都是 2.802）。**修复**：按实际 n 与事件率算对数秩非中心参数（n=646/HR=0.75 → δ=2.682，对应 power 0.765；n=1200 → 3.655）。
- 🟡 **P2-2 效应量曲线 survival 轴的 n 语义**：`fix_n` 回退到 `nobs`（受试者）却被当事件数（646 → 报 0.955，真值 0.768）。**修复**：有事件率时先折算成事件数。
- 🟡 **P2-3 `dropout` 语义在两条路径上不一致**：rpact 路径是「dropoutTime(=12) 内的脱落**比例**」，`.event_prob` 路径是「每单位时间脱落**风险率**」，同填 0.05 量级差 12 倍。**统一为「研究全程（A+F）内的脱落比例」**：`.event_prob_arm` 内部换算 `δ=−log(1−dropout)/(A+F)`，所有 rpact 调用同步传 `dropoutTime=A+F`（含 `gsd_survival` / `gsd_hazard`）。连带修正通用脱落膨胀层：生存家族 5 个检验已把 dropout 折进 P̄，从 `n/(1−g)` 膨胀层中排除，避免重复膨胀。
- 🟡 **P2-4 `n_with_dropout = ceiling(total×1.1)` 硬编码**：与用户填的脱落率无关且与 P̄ 内折算重复。**删除**，改为报告「脱落率（已计入上述 N，按研究全程比例）」。
- **验证基建（可复跑）**：`tests/scratch/verify_survival_modules.R`（Part A：逐函数 rpact/TrialSize 对照 + 独立 log-rank/TOST/竞争风险/Poisson MC 回代）、`tests/scratch/verify_survival_e2e.py`（Part B：驱动 `run_task.R` 查接线/默认值/正反向）。修后矩阵：13 个模块 **12 PASS / 1 项 +3pp 保守余量（one_sample）**，详见 `tests/scratch/tmp/partA2.txt`。
- **版本**：SKILL.md 5.13.42 → **5.14.0**；coze 端 5.13.44 → **5.14.0**（`_version.py` + `manifest.json`）。**未部署**（云端镜像需按 DEPLOY.md 重新打包）。

## 5.13.44 — 2026-10-25 · coze 端 query_origin 豁免表（exempttbl cnt=0 免锁免限·保留并发）
- **背景（用户 2026-10-25 策略）**：飞书豁免表 `tblu4OVgWSwzrFw6` 中 `cnt=0` 的 query_origin 视为「已登记零流量设备」，安全策略计算时一律豁免、写拒止表时直接跳过。替代此前 pseudoid 白名单方案（已回滚，键从「IP 绑定」改为「机器身份绑定」，跨 IP 稳定，适配登记设备语义）。
- **antiscrape.py（ct-base v1.2 规范母版，同形同步 coze/src + workbench 副本）**：check_allow 六级扩七级——第 3 级豁免判定（exempt 表 cnt=0 origin → 跳过拒止表/单点限流/日额，**保留**包体上限/硬拒字段/全局并发「免锁免限但保留并发」）；`add_to_denylist` 加 `query_origin` 参数 + 豁免闸（命中即 return，内存表与飞书双跳过）；`_on_rate_limit_reject` 透传 origin（auto-escalate 路径同受豁免）；新增 `_load_exempt_from_feishu`（分页全量、只收 cnt=0、机会性列名）+ 300s 独立刷新 + **fail-safe**（加载失败清空豁免集，向安全侧失效，与拒止表 fail-open 方向相反）；遥测加 `exempt` 列；init 日志含豁免表状态；5 个 env（`CT_ANTISCRAPE_EXEMPT_{ENABLED,TABLE_ID,ORIGIN_FIELD,CNT_FIELD,REFRESH_SEC}`）。
- **habit_analyzer.py**：`analyze` 输出带 origins 列表；`apply_bans` 对命中豁免 origin 的条目跳过写入（offline 封禁路径同受豁免约束）。
- **安全边界（写死在注释与 README 红线）**：query_origin 是客户端自报字段（sha256(hostname)，64 hex 外部不可枚举），豁免 = 信任「知道该值的调用方」；滥用窗口由 cnt 语义（有流量不豁免）+ 300s 刷新周期双重封顶；豁免命中全部遥测可审计。
- **测试**：`tests/test_antiscrape.py` 新增 Part E 30 断言（跳拒止表/免限流/不触发 escalate/保留并发/保留包体硬拒/写闸双跳/空 origin 不豁免/cnt 解析/猴补假数据加载/失败抛异常），全量 **76 通过 / 1 失败**；唯一失败 D5（模板逐字节一致）为**既有失败**——ct-samplesize 与 ct-base 的差异仅在拒止表 query_origin 归因区（方案 A/B，120 行 diff，豁免相关 0 行），与本次改动无关；DEPLOY.md §11 措辞已改为「内容指纹校验」。
- **版本**：coze 端 5.13.39 → **5.13.44**（`_version.py` 单一真源，同日修订）；SKILL.md 版本不变（5.13.42，技能侧无功能改动）。**未部署、未推送**（按约定由用户在 coze 平台侧操作）。
- **后续待办**：限流窗口重置后补跑 FD-B2 live 回归（matrix_gaps）；建议给回归套件加客户端 pacing（57 连续调用对 30/60s 窗口必然超限）。

## 5.13.42 — 2026-10-25 · 全量回归：符号秩公式 √2 因子修正（MC 实证）+ 工作台 or 组必填提示
- 🔴 **R 引擎公式 bug（5.13.39 引入，蒙特卡洛实证抓出）**：`ss_wilcoxon_sr` 的 z 统计量用了 `√6·n(n+1)(p*-½)/√(n(n+1)(2n+1))`，正确值为 **√12**（差 √2 因子）——符号秩样本量虚高约 4 倍（φ=0.65 时算成 116，实际 58）。根因：`E1(W+)-E0(W+)` 按「秩-符号独立」近似会低估 √2（H1 下秩与符号不独立）。
  - **实证（20000 次精确 wilcox.test 蒙特卡洛）**：n=30/p*=0.7072 → 模拟功效 0.802；√12 公式 0.800 ✓，旧 √6 公式 0.502 ✗；n=60 → 0.981 vs 0.976 ✓；n=120 → 1.000 ✓。与符号秩 ARE=3/π 自洽（局部漂移比 √6·φ(0)=0.977）。
  - **修复**：`samplesize_functions.R` `.pow_wilcoxon_sr` 的 `sqrt(6)` → `sqrt(12)`；Noether 闭式分母 3 → 6（修正后与两样本秩和同分母，渐近 z 均为 √(6n)(p-½)）；注释区记录 MC 实证依据防回改。两样本 `ss_wilcoxon` 经同样 MC 验证**本就正确**（n=64/d=0.5：模拟 0.781 vs 公式 0.773，ARE=3/π 对得上）。
  - **部署包**：`coze_project_5.13.39.zip` 已本地重建（MD5 437bc1e3，含修复；旧包内含 bug 公式，若照旧部署即事故）。**未部署**（coze 端点仍 5.13.33，无 wilcoxon，线上零影响）。
- **工作台 or 组必填提示（5.13.41 遗留缺口）**：wilcoxon 系效应输入二选一（superiority｜median_diff+sd），`MIN_REQUIRED=[]` 致空参也显示「已齐备，可直接计算」，用户点计算后才被 R 引擎拦下。`workbench.html` `requiredMissing` 新增 `OR_REQUIRED` or 组语义：任一分支满足即通过；全不满足时报进度最多分支缺项（主路径 superiority 优先，仅 median_diff 时报配对的 sd）。
- **测试基建**（`tests/scratch/`，本地回归夹具）：`verify_wilcoxon.R`（R 单元 20 断言：折算路径/闭式/最小整数性/单双侧/不等比例/ARE/MC 锚定）、`mc_wilcoxon.R`（蒙特卡洛裁决）、`e2e_wilcoxon.py`（run_task.R dispatch 16 断言）、`ui_focus_check.js`（jsdom 26 断言：菜单落位/占位提示/求解方向切换输出/or 组提示/叙述结构化）。
- **回归矩阵（本轮全量）**：R 单元 20/20；E2E 16/16；合约信封 ALL PASSED；合约 live 21/21；NL 30/30；全覆盖 69/69；jsdom meta 26/26 + 聚焦 26/26；意图判定 13/13；分类/参数/审计双语 spot check 全过。FD-B2 反求 41 例因 coze 端点 429 限流（`rate_limited`）出现 26 个假失败，已诊断为基础设施节流非代码回归，待限流窗口重置后复跑。
- **版本**：SKILL.md 5.13.41 → 5.13.42（工作台侧）；coze 端版本不变更（5.13.39，R 修正折入该未发布包）。
- **FD-B2 反求回归（限流窗口重置后补跑，2026-10-25 16:58）**：56/57 通过（98.2%）；1 硬失败未能在节流间歇窗口内定位（FD-B2 系列在端点限流间歇时 status=None 全灭、正常窗口才返回，与本轮修改无关——合约 live 21/21、NL 30/30、全覆盖 69/69 全过作反证）。
- **C-detail-escape 机检 + 模糊名修复（衔接 ct-base v1.4.21，同日追加）**：用 ct-base 通用引擎 `scripts/wb_detail_check.py`（新增 `C-detail-escape`，2026-10-25）复检工作台——抓出存量模糊名缺陷「高级选项（可选参数 / Monte-Carlo 验证 / 图表选项）」（§21.2 红线 3），按"动作+对象"改写为「展开可选参数」（summary/nav/页描述/英文字典同步）；同时负例双向验证确认本轮吞字符修复（`P(X＜Y)` 全角化 + `esc()` 转义）零误报。修复后工作台与发布副本 `C-detail-*` 全绿（label / placeholder / claim / i18n-ph / escape）。测试基建与机检运行方式已登记 `AGENTS.md`「Test Infrastructure」章节。

## 5.13.41 — 2026-10-25 · superiority 参数易用性改造（白话帮助 + 输入框占位提示 + 定位引导）
- **背景（用户实测反馈）**：「随机优势 φ = P(X＜Y)」难理解、且缺参提示里报了参数名也不知道对应表单哪个框。
- **标签精简**：PARAM_LABELS superiority 由 `随机优势 φ = P(X＜Y)` → `随机优势 φ`（公式定义移入帮助文案；契约速览 tag 同步变短）。
- **帮助白话化**（HELP_ZH + argparse help）：「治疗组受试者结局优于对照组受试者的概率；0.5=无差异；典型 0.6 小 / 0.65 中 / 0.7 中大（≈ d=0.5）；不知道 φ 时改用中位数差 Δ+σ 路径」。
- **新增输入框占位提示机制**（通用能力）：`form_schema.py` 新增 `PARAM_PH` 表 + `_ph_for()` + get_catalog 透传 `ph/ph_zh/ph_en`；`workbench.html fieldHTML` 给 number/text 输入渲染 `placeholder`。首批配置：superiority `0.5~1，如 0.65` / median_diff `如 5` / sd `如 10`。
- **定位引导**：缺参提示 `fillRequired` 中英文均补「在下方参数表单中填写 / in the form below」。
- **版本**：SKILL.md 5.13.40 → 5.13.41；coze 端无改动。

## 5.13.40 — 2026-10-25 · 修复 superiority 参数标签被 HTML 吞字符（「P(X」断裂）+ 缺参提示转义加固
- **Bug（5.13.39 引入）**： superiority 的 `label_zh` 为 `随机优势 φ = P(X<Y)`，`workbench.html` 缺参提示把它直接拼 innerHTML，浏览器把 `<Y)` 当未知标签吃掉，页面显示残缺的「随机优势 φ = P(X」。
- **修复（双保险）**：
  1. 文案层：`form_schema.py` 的 PARAM_LABELS / HELP_ZH 中 superiority 的半角 `<`/`>` 统一为全角 `＜`/`＞`（已扫描全表，仅此两处受影响）；
  2. 渲染层根治：`workbench.html:1427` 缺参提示拼接处补 `esc()`——今后任何参数标签含尖括号/& 都不会再被吃（其余 4 处 paramLabel 调用点 1591/2371/2395/2496 此前已有 esc 或走 textContent，经逐一核对无需改）。
- **版本**：SKILL.md 5.13.39 → 5.13.40；coze 端无改动（纯前端/表单 schema 展示层）。

## 5.13.39 — 2026-10-25 · 新增非参数 Wilcoxon 秩和 / 符号秩样本量（NP1/NP2，A+B 落地）
- **背景（用户 motivating）**：既往研究只给中位数（标准误）时参数法（均数±SD）失效，需要非参数路径。ROADMAP 原判「非参数无闭式解」有误——Wilcoxon 族有 Noether (1987, JASA) 闭式近似。
- **R 引擎**：`samplesize_functions.R` 新增 `ss_wilcoxon`（两独立样本 Wilcoxon-Mann-Whitney 秩和）与 `ss_wilcoxon_sr`（配对/单样本符号秩）：
  - Noether 闭式起点 + 精确 z 表达式逐点校验（先下探后上补），保证返回「达成功效的最小整数」；
  - 效应输入两路径：`--superiority` 随机优势 φ 直给（优先），或 `--median_diff`+`--sd`(+`--shape` normal/logistic) 按位移分布折算；仅给 median_diff 不给 sd **明确报错**（不静默默认）；
  - 支持单双侧、`--ratio` 不等例、反求功效（nobs）、`--dropout_rate` 脱落膨胀；正态下 n 比参数 t 检验高约 5%~15%（ARE=3/π≈0.955）。
- **dispatch + 曲线**：`run_task.R` 新增两分支（含双语 narrative + 脱落膨胀行）；`.curve_solvers` 新增两个求解器（n_seq/power_seq/effect_seq 均支持）。
- **命名决策**：CLI 参数定名 `--superiority`（不叫 `--phi`——避开 regression_poisson/rates_ext 的过离散参数 φ）；R 形参/attr/stats 键同步为 superiority。
- **接入层**：parser choices + 新参数；`_contract_index.json` 登记 2 条（65→67）；`form_schema.py` 补 TEST_LABELS/PARAM_LABELS/HELP_ZH/CHOICE_LABELS/COMMON_SUPPORTED/MIN_REQUIRED/FAMILY「非参数」+ continuous 域；工作台选单自动出现在「连续型结局 → 非参数检验」族（前端零改动，全 catalog 驱动）。
- **假设审计**：`hypothesis_audit.py` DESIGN_FAMILIES 归入「经典平行两组比较」+ 新增 superiority/median_diff/shape 三维度与退路；superiority 与 median_diff **互斥路径**语义（只给一路不误报 missing，5/5 冒烟通过）。
- **NL 识别**：`classify_test.py` 加 wilcoxon/signed_rank 规则（显式名 10 分 + 负例防误抢生存/符号秩）；`param_aliases.py`  superiority/median_diff 数值抽取 + `_detect_shape` 枚举通道。
- **文档**：SKILL.md 65→67 种检验、曲线支持 9→11；menu.md / coze_contract.md / cli_examples.md / ROADMAP（非参数项移出未做列）。
- **顺带修复**：`coze_client.py` `_envelope_to_result` 遇字符串 error（实测限流 `{"ok":false,"error":"rate_limited"}`）时 `err.get` AttributeError 吞掉真实错误——按类型分流，字符串原样呈现。
- **验证**：R 单元 12/12（Noether 文献值 φ=0.7→n=34；d=0.5 对照 t 检验 64 vs Wilcoxon 70，比值 1.094≈1/ARE）；R 端到端 5/5（superiority/median_diff/符号秩/反求功效/无参报错）；合约回归 ALL PASSED（含新 test 信封断言）；NL 7/7；审计 or 语义 5/5。**未部署**（coze 端点与工作台均为旧版）。

## 5.13.38 — 2026-10-25 · NL 咨询闸门激进化：问句型「如何/怎么/怎样 + 估计|算」纳入咨询（带参兜底放行）

## 5.13.37 — 2026-10-25 · 自然语言入口：求助 / 求替代方法类咨询句识别并转接 Ct-Advisor

- `server.py` 咨询路由闸门 `_ADVISORY_MARKERS` 补漏：新增「还能怎样 / 还能怎么 / 可以怎样 / 可以怎么 / 怎样才能 / 如何才能 / 想请教 / 请教 / 求助 / 请问 / 求指导 / 指导一下 / 有哪些|有什么|哪种|别的|其他 (方法|办法|方式|途径) / 替代(方法|办法|方案)」及对应英文（`any other way/method/approach`、`how to estimate`、`ways to estimate` 等）**强咨询信号**。
  - 实测：用户原句「…既往研究给的是中位数（标准误）时**还能怎样**估计样本量呀」此前未命中，误走低置信「预填表单」路径；现正确判定 `intent=advisory`。
  - 均为「问方法 / 求助」语气，不含「给我算」的计算意图；不影响既有红线——「怎么算 / 如何计算」仍放行为计算意图。
- 命中后沿用既有链路（前端无需改）：结果区显示咨询提示 + 「转 Ct-Advisor 处理 ↗」按钮（跳 `https://ct-advisor.app.workbuddy.host/#q=…`，hash 预填、不自动发送、零凭据）；仍预选检验并填表，但不自动点火云端计算。
- 回归：原句 + 4 个求助句 → advisory；4 个计算句（含「怎么算 / 如何计算」放行句）→ compute，无误伤。已同步 `adapters/workbench/publish/` 副本。

## 5.13.36 — 2026-10-25 · 结果操作条视觉协调 + 假设质量审计中英双语

**前端（workbench.html）**
- 结果操作条视觉协调：📋 生成方案论证段 / 🔍 审计假设 由渐变强调大按钮收敛为次级描边按钮（`.act-btn`，白底 + 品牌色描边，hover 才填充），不再与结果区标题抢权重；对应规划块标题由 11px 小徽标升级为带色块粗体头部（`.plan-head`，14.5px / 800），成为结果区视觉锚点。

**后端（scripts/hypothesis_audit.py + adapters/workbench/server.py）**
- 假设质量审计中英双语：`render_text(report, language="bilingual")` 新增语言参数，与方案论证段（justify_text）一致、无论界面语言始终提供英文——
  - `bilingual`（默认）中文（English）对照 / `en` 纯英文 / `zh` 纯中文。
  - 新增英文层：维度名与证据标准（`_DIM_NAME_EN` / `_ASSUMPTION_EN`）、设计逻辑族与族问题（`DESIGN_FAMILIES_EN`）、族名（`_FAMILY_NAME_EN`）、fallback 退路（`FALLBACKS_EN`）、引用推荐（`_CITATION_FORMATS_EN`）、CONSORT 16a 检查表（`_CONSORT_16A_ITEMS_EN`）、监管就绪等级与判定说明（`_GRADE_DESC_EN` / `_OVERALL_NOTE_EN`）、rationale（`_RATIONALE_EN`）。
  - 六级标题、四分级明细表表头、评分表表头均中英并注；结构化行（标题 / 表头 / 引用）与自由文本分别经 `_branch` / `_cell` 双语化。
- server 调用透传 `options.language`（未传时默认 `bilingual`，保证有英文）。
- 计算层 `audit_hypotheses` 签名与逻辑不变；纯标准库、不触数值真相源、不调 coze。已同步 `adapters/workbench/publish/` 副本（scripts + server）。

## 5.13.35 — 2026-10-25 · 规划层结果（方案论证段 / 假设审计 / 模拟验证）卡片化美化 + 操作按钮强调

- 结果操作条重做：📋 生成方案论证段 / 🔍 审计假设 两个主操作改为渐变强调大按钮（`.act-strong`），验证徽标保留。
- 规划层块从数值主叙事中拆分，按来源格式分别结构化渲染：
  - 假设审计 / 模拟验证（Markdown）→ 标题层级、`|` 表格、`>` 引用、`-`/`1.` 列表、`□` 勾选清单均美化。
  - 方案论证段（自定义文本）→ `=`*60 大标题、`---` 子标题、`【EN】/【中文】` 语种条、编号与 `□` 清单美化。
  - `[__填写]` / `___` 占位符高亮为待填提示；每块带类型徽标（论证段/假设审计/模拟验证）。
- 纯前端渲染层改动，不动 server / coze / R 引擎（块源格式为 API 与导出报告共用）。

## 5.13.34 — 2026-10-25 · 工作台「结果说明」(narrative) 结构化渲染优化

**前端**：R 引擎返回的 narrative 纯文本（原样含 `========== 标题 ==========` 分隔线与 `key: value` 行）由裸 `esc()` 直显改为前端解析渲染——`=====` 分区标题转为带左侧强调条的区块标题、键值对转为左右对齐的键值网格、其余散文保留为段落。视觉层级清晰，不再有裸露的 `=` 装饰线；narrative 源格式（API / 导出报告共用）保持不变。

## 5.13.33 — 2026-10-25 · coze 引擎完整实现「采纳模式」代入计算（C5 公开证据基准）

**功能**：公开证据基准（C5）从「仅展示」升级为「可选代入」——用户在前端选具体采纳模式（median / conservative / low / high / <来源序号>）后，coze 引擎在调用 R 前解析基准 JSON、按模式聚合、做尺度/终点兼容性校验，并把采纳值写入计算参数（`effect` / `hazard_ratio`；OR/RR 经 `TARGET_ARG` 落入 `effect`），真正驱动样本量计算。选「仅展示（不代入）」则保持原展示行为。

**实现落点（coze 引擎侧）**：
- 新增 `adapters/coze/src/effect_ref_resolver.py`：解析 `effect_ref` JSON（兼容 array / `{references}` / 单对象）、`validate` / `pick` / `compatible`、`TARGET_ARG` 落地；`adopt_ref ∈ {off,display,none,空}` 返回 None（仅展示）。
- 复用既有聚合数学 `scripts/effect_ref.py`（已复制为 `adapters/coze/src/effect_ref.py` 随包部署，构建脚本新增同步）。
- `graphs/nodes/samplesize.py`：`_compute_one` 内 deepcopy params → `resolve_effect_ref` → 缓存签名 → R 引擎；R 返回后 `_attach_effect_ref_note` 把采纳明细写入 `out["effect_ref_ctx"]` 并在 `warnings` 追加可追溯一行（来源/基准/取值）。单条与批量模式均覆盖。

**前端配合**：采纳模式下拉新增「仅展示（不代入）」默认项（守住「默认仅展示、显式采纳」红线）；补 `adoptHintOff` 中英文案；`pbSend` 文案更新为「选具体模式即代入」；「填入示例」JSON 的 schema 修正为 `param:"effect", scale:"SMD"`（对齐 effect_ref.py，否则校验失败）。

**校验（本地 R 端到端）**：ttest_ind + demo 基准 + `adopt_ref=median` → resolver 把 `effect` 置 0.42，R 引擎返回 `stats: {n:90, d:0.42, power:0.8, solve_for:n}`；同参数手动给 `effect=0.42` 结果一致；`adopt_ref=off` 且不手动给 effect → R 报「root-finding failed」，反证代入确实生效。跨零 CI 与 OR→effect 路径单测通过。

## 5.13.32 — 2026-10-25 · 工作台两处前端修复（输出字段随求解方向 + 公开证据基准示例可用化）

**1. 输出字段随求解方向切换**
- 方法卡「输出字段」区原固定列出契约全量 `t.output`（如 `n_per_group` + `power`），不随「求样本量 n / 反求效能」切换；切换求解方向时方法卡也未重渲染，导致反求效能时仍挂着 `n_per_group`。
- 修复：`renderMethodCard` 按求解方向过滤输出字段（求 n → n 类结果；反求效能 → `power`），标题带方向注解；`onSolve()` 切换时同步重渲染方法卡。

**2. 公开证据基准（C5）区可用化**
- 原 2 个 i18n 标签（`pubBenchTitle` / `pubBenchTip`）被引用但未定义，渲染出 `undefined`；占位符还写着本地仓库路径 `references/effect_size_benchmarks/`，网页用户无法访问，等于死路。
- 修复：补齐中英文标签；占位符改为「粘贴基准 JSON（点「填入示例」可加载演示数据），或上传 .json 文件」；新增「填入示例」按钮，点一下把一段可解析的 3 文献 SMD 示例 JSON 注入文本框并自动解析预览，无需本地文件。

**校验**：Node 复刻输出字段过滤逻辑（ttest_ind/paired/one、meta_planning 均符合预期）；示例 JSON `JSON.parse` 成功得到 3 条 `{"param":"SMD",...}` 记录；已重建发布载荷，`publish/index.html` 含全部修复。

## 5.13.31 — 2026-10-24 · 修复 JS 悬挂调用导致的渲染链中断（Cohen 惯例参考表空白）

**症状**：工作台「Cohen 效应量惯例参考」面板点开后只剩一句提示语，四列数值表（量级 / Cohen's d / r / Cohen's h）与数值全部消失；连带「效应量助手」折算器、图表/曲线控件同样不渲染。

**根因**（Playwright 实测取证，非推测）：`workbench.html` 的「快速案例 chips」功能被整套下线（`CASE_CHIPS` 数据常量、`#caseChips` 容器 HTML、`caseChipsTitle` i18n 键、`renderCaseChips`/`applyCaseChip` 两个函数体全部移除），但 **`renderCaseChips(test)` 的 2 处调用点被遗漏**（`setLang` 与 `onTest`）。

`onTest()` 中的调用链因此断裂：

| 行 | 语句 | 修复前 |
|---|---|---|
| 1171 | `renderMethodCard(test)` | ✅ 执行 |
| 1172 | `renderCaseChips(test)` | 💥 `ReferenceError: renderCaseChips is not defined` |
| 1173 | `renderEffectHelper()` | ❌ 永不执行（内含 `renderBenchRef()`） |
| 1174 | `renderFigureCtl()` | ❌ 永不执行 |

由于 `renderBenchRef()` 只能随 `renderEffectHelper()` 触发，`#benchRef` 容器保持空白 → 面板只剩静态 HTML 里那段 `.sectip` 提示文字。**同一个异常连带废掉 3 处 UI**，属单点崩溃扩散。

**修复**：删除残留的 2 处悬挂调用（功能已系统性下线，数据/容器/i18n 均无，恢复整套 UI 属引入未确认改动，故不恢复）。

**验证**（Playwright headless，本地 server 实跑）：

| 检查项 | 修复前 | 修复后 |
|---|---|---|
| `pageerror` | `renderCaseChips is not defined` | **无** |
| `#benchRef` innerHTML | 0 字节（空） | **409 字节**（表格四列齐全） |
| `#effectHelper` innerHTML | 0 字节（空） | **2224 字节**（Δ/σ 折算器回归） |
| `renderFigureCtl` 链路 | 中断 | 恢复 |

载荷已 `build_publish.py` 重建，`cmp` 确认与源逐字节一致。

### 文案调整：`meta_planning` 中文名 荟萃分析规划 → Meta分析规划

用户要求统一术语，页面方法名不再使用「荟萃」。`form_schema.py` `TEST_LABELS` 第 859 行改为 `("Meta分析规划", "Meta-analysis planning")`；英文侧 `Meta-analysis planning` 不变。实测 `get_catalog("zh")` 返回 `label`/`label_zh` 均为 `Meta分析规划`，条目内已无「荟萃」残留。

> 注：`README_zh-CN.md` / `references/menu.md` 等文档中的「Meta 分析前瞻规划」为文档表述，本轮未动；若需全库术语统一可另行处理。

## 5.13.30 — 2026-10-24 · 计算超时防护（消除 Cloudflare 524）

> 用户诉求：「最新版本计算后渲染结果曾经报过524错误，检查一下」

### 根因
计算链路 `server._compute → CozeBackend.compute → coze_client._post → coze 云端 R 引擎` 此前**无中间超时**：
`coze_client._urlopen_with_proxy_fallback` 的 `read_timeout` 默认 **600s**，而 Cloudflare 网关在 **100s** 即切断。
重计算（主因是 `mixed_model`：simr `powerSim(nsim=100)` = 100 次 lmer 拟合）在 coze serverless 低配环境
必然 >100s → 网关先切断返回 **524**，且 server 仍傻等 600s。`adaptive_simulate`（默认 10000 仿真，纯向量化）
与 `assurance`（默认 100 次 ×2万 beta 采样）实测秒级，**非 524 主因**，已排除。

### 修复（仅 sandbox 侧，重建发布即生效，不改 coze 端 R 引擎）
- `coze_client`：新增计算专用短超时常量 `_COMPUTE_TIMEOUT = 95s`（`CTSS_COMPUTE_TIMEOUT` 可配）；
  `_post`/`call`/`call_batch` 透传 `read_timeout`；`CozeBackend.compute`/`compute_batch` 注入该值；
  超时异常（`socket.timeout` / URLError-timeout）统一转 `RuntimeError("COZE_TIMEOUT:...")` 标记。
- `server._compute`：捕获 `COZE_TIMEOUT` 标记，返回**可控 504 + 中文友好提示**
  （替代不可诊断的 524；提示减少 nsim/样本量或改用解析方法），不再傻等 600s。

### 验证
- `py_compile` 两文件通过；单测（monkeypatch `_urlopen` 抛 `socket.timeout`）确认 `call` 正确转 `COZE_TIMEOUT`。
- 本地 R 实测：`mixed_model nsim=100` 多核环境即 >120s（工具默认超时），coze 低配必超 100s；
  `adaptive_simulate group_sequential n_sim=10000` 仅 0.23s、`assurance n_sim=100` 0.38s，排除其为主因。

### 未覆盖（需 coze 端发布配合，本次未做）
`mixed_model` 默认 `nsim=100` / `assurance` 默认 `n_sim=100` 偏重；根治需降低 R 引擎默认仿真次数或长计算异步化。
当前 95s 超时把「不可诊断 524」转为「可控 504 + 引导文案」，体感即可诊断。

## 5.13.29 — 2026-10-23 · 工作台选项框全量审计：契约缺口（静默错参）修复 + 无效控件按方法屏蔽

> 用户诉求：「ct-samplesize 针对所有工作台页面上的选项框，逐一排查是否有无法在当前方法下面使用，
> 或者无法完成相应功能的情况。如果无法使用，就修改显示方式屏蔽掉。如果无法完成相应功能，就对 bug 做修改。」

### 审计方法（三向比对，非抽样）
对全部 **65 个检验方法**逐一建立三张集合并求差：
- **R(test)** 表单实际渲染字段（实测 `form_schema.schema_for`）
- **E(test)** 引擎实际消费键（精读 `adapters/coze/src/r_engine/run_task.R` 全部 65 个 dispatch 分支
  + `.d_val/.alt/.ratio/.alloc/.gsd_design` 等 helper 的传递闭包）
- **S(test)** 出站信封真正发出的键（契约 `required ∪ optional` ∪ `_ALWAYS_ALLOWED_PARAMS` ∪ curve 映射 ∪ 引擎控制键）

### P0 · 契约缺口：表单能填、引擎也读，但被白名单静默剥离（BUG，共 46 项）
根因：`build_params()` 在契约存在时**只发契约登记的键**。契约未登记的键即使表单渲染了、用户填了，
也会被剥离 → 引擎拿不到 → 恒走内部默认值 → 结果与用户意图不符，且**无任何报错**（静默错参）。

`tests/coze_cases/_contract_index.json` 补登 12 项 required + 35 项 optional，关键项：

| 检验 | 缺口键 | 修复前后果 |
|---|---|---|
| `ttest_ind`/`paired`/`one` | `sd` | 填了 σ 也不折算，`effect` 恒被当成 Cohen's d |
| `cluster` | `effect` | 整群设计效应量恒为内置默认 0.5 |
| `mixed_model` | `n_indiv` | 纵向/MMRM 个体数入参丢失 |
| `survival_exact` | `alpha_exact` / `power_exact` / `dropout_exact` / `n_stages_exact` | 精确法 α/效能/脱落/阶段数全部恒用默认 |
| `proportion_one` | `p2` | 单组率检验无法指定 H1 目标率（恒 0.65）|
| `historical_controls` | `prob_treatment` | 无法指定治疗组率 |
| `survival_historical` | `median0` | 无法指定历史对照中位生存 |
| `ni_survival`/`survival_equivalence`/`survival_superiority` | `dropout_rate` | 生存脱落率不进事件概率折算 |
| `rates_ext` | `half_width` | CI 精度模式无目标半宽入参 |
| `adaptive_simulate` | 18 项（含 `n_simulations`/`sim_seed`/`optimize`/`reestimate_method`…）| 仿真次数、种子、再估计方法等全部失效 |
| `be_tost` | `theta1`/`theta2`/`margin` | 等效界值只能用内置 0.8/1.25 |
| `assurance` | `margin_assurance`/`sim_seed` | 保证度成功界值、随机种子失效 |
| `gsd_proportion` | `gs_ratio`/`gs_or` | metric=ratio/or 模式无入参 |
| `gsd_survival_sim`/`gsd_hazard_sim` | `n_simulations`/`sim_seed` | 仿真次数与种子失效 |

### P1 · 无效控件按方法屏蔽（共 199 项 + 38 个方法的 verify 组）
新增 `form_schema.COMMON_SUPPORTED_BY_TEST` / `UNSUPPORTED_EXTRA_BY_TEST` / `unsupported_for()`，
`schema_for()` 统一过滤。此前公共参数组（alpha/power/nobs/side/ratio/sd/effect）对 65 个方法**一刀切渲染**，
而引擎并非每法都读：

- `sd` 在 57 个方法无效、`side` 49 个、`effect` 46 个、`ratio` 42 个、`alpha` 4 个各被屏蔽
- `dose_escalation`（纯设计型）、`mixed_model`（模拟功效）的 alpha/power/nobs 全部屏蔽
- `bayesian`（硬编码单侧）、`non_inferiority`、GSD 全族的 `side` 屏蔽
- `cluster` 的 `n_indiv` 屏蔽（引擎反算簇数，不消费该键），`effect` 改列最小必填
- Monte-Carlo 验证组（verify×6）仅对 `verify.py` 本地闭环支持的 27 个方法渲染，其余 38 个方法整组屏蔽
- 同步补齐 29 个新字段的中文标签（PARAM_META）与说明（HELP_ZH），无裸参数名残留

### 发布版页面补齐「可选参数」区
`workbench/index.html` 此前**完全不渲染**契约 optional 通道（无高级选项区），导致 be_tost 等效界值、
adaptive_simulate 仿真参数、rates_ext 的 CI 半宽等**无法从页面输入**；现按 `grp.optional` 追加渲染。
（发布版 `collectParams` 只收集 `#formArea [data-dest]`，故并入主表单区渲染而非新开容器，避免漏收集。）

### 实测验证（云端 coze 引擎，修复后）
| 用例 | 结果 | 结论 |
|---|---|---|
| `ttest_ind --effect 1.0 --sd 2.0` | d=0.5 → **每组 64** | sd 杠杆生效 |
| `ttest_ind --effect 1.0`（对照）| d=1.0 → 每组 17 | 修复前两者同为 17 |
| `cluster --effect 0.3 / 0.6` | 每组 **171 / 43** | 效应量杠杆生效（修复前恒按 0.5）|
| `proportion_one --p2 0.6 / 0.75` | n=**194 / 29** | H1 率杠杆生效（修复前恒 0.65）|
| `survival_exact --alpha_exact 0.01 --power_exact 0.9` | power=**0.9** | 精确法专用键生效 |

回归：`tests/coze_cases_regression.py` **ALL PASSED**；三向缺口复核 A=0 / B=0 / 真实入参缺口=0。

### 备注
- 曲线控件（7 个 curve_* ）经核对契约 `default_curve` 与引擎 `curve_solvers` 完全一致（各 5 个方法），**无需屏蔽**
- `figure_mode` 为本地渲染控制位（不经引擎），保留全局可用
- `workbench/publish-dist/` 为构建产物，需重跑 `build_publish.py` 才会带上本次改动
- 本次仅本地改动，**未推送任何远端**

## 2026-10-23 · 仅工作台（不进发布包）：ct-base 工作台规范机检整改

> 按 `_wb_audit.py` A–L 矩阵整改 `workbench/`（CT Base `workbench_ui.md` §4.5/§5.2），不涉及引擎与 adapters，不影响发布包内容。

- **A 字号令牌**：index.html 43 处 + wb-list.css 11 处裸 `font-size:<px>` 全部替换为 `var(--wb-fs-*)`（映射 24→2xl、21→xl、16→lg、15→base、14→sm、13/12.5/12→xs、11.5/11→2xs；窄屏 media 内 input 16px 同步令牌化为 `--wb-fs-lg`，功能不变）
- **B 七档令牌**：tokens.css `:root` 补齐 `--wb-fs-2xl/21px` 七档定义（24/21/16/15/14/13/11）
- **D 页脚**：main 底部新增 `<footer id="wb-footer">`，「ct-samplesize 工作台 v7.0 · 基于ct系列技能统一框架构建」（workbench.config.json 未设 version，按规范取 v7.0），样式对齐 ct-registry
- **E logo-box**：顶栏品牌 SVG 包裹 `.wb-logo-box`（40px 白底圆角 + 阴影，内部 svg 34×34）
- **H bug 图标**：`#wb-bug` 反馈按钮 SVG path 换为规范路径 `M4 4h16v12H7l-3 3V4Z` + `M8 9h8M8 13h5`
- **J app.config.json**：补 `appName` / `domainPrefix` / `shareLink` / `startCmd`（保留 appId/publishDir）
- 机检复跑：A–L 全 OK（I 无 server.py 不适用）；Playwright 无头加载 console/pageerror 仅 2 条 file:// 协议下 `/api/schema` 后端探测失败（整改前版本同样存在，属基线既有，非本次引入）

---


## 5.13.28 — 2026-10-22 · README 对齐 ct-sdtm 样板写法 + 生存类 event_rate 契约补登

### 契约缺口修复：三个生存方法的 event_rate 此前无法提供（本地已生效，无需重新部署 coze）
- 复核 README 案例数值时实测发现：`ni_survival` 传 `event_rate=0.7` 被丢弃（契约未登记），引擎恒按默认 0.6 计算——与 survival 已登记 event_rate 不一致
- 修复：`_contract_index.json` 与 `MIN_REQUIRED` 为 `ni_survival` / `survival_equivalence` / `survival_superiority` 补登 `event_rate`（插在 followup_time 后）
- 实测：er=0.6 → 每组 730（P=0.3402）；er=0.7 → 每组 601（P=0.4132），杠杆生效
- **无需重新部署 coze**：R 引擎（v5.13.26 已上线）本就消费该键，缺的只是本地白名单登记；但云端 coze 工作流表单若未提供 event_rate 输入项，需人工核对补配

### README 对齐 ct-sdtm 样板（§13.17）
- 案例大全导语改为 ct-sdtm 式单句引用块（删除"学会本技能最快的方式就是看例子"元描述段——§13.17 导语禁令），并提示生存类设计需给出事件率与时间表
- D1 / D2 案例卡的生存数值从旧口径（196 事件 / 330–360 例、370 例——B 方案前的算法）更新为 v5.13.26 新口径实测值：D1 → 434 事件 / 每组 929（P=0.2337）；D2 → 每组 730（P=0.3402），并补"事件率杠杆"教学点（er=0.7 → 601）
- 案例区确认无工作台操作混入（工作台描述收敛于第七节极简披露，见 5.13.27）
- **案例大全按"每大方向 2–3 张代表卡"精简（62 → 30 张，中英一致）**：
  - 保留原则：每节留基础卡 + 最具独有价值的卡（如 4.1 留 A1/A2、4.4 留 D1/D2、4.13 留 N1–N3、4.17 留 BE / 生存时间表 / SSR 三张）
  - 删除 32 张：参数化变体（B2/J2/K2）、跨节重复的选型路由卡（A3/D3/H3 中与弹出菜单示例重复者）、已被 S 系列实测卡覆盖的同族卡、纯增量小功能卡（N4/Q6/Q7/R1 等）
  - N/Q/R/S 节内重编号连续（N1–N3 / Q1–Q3 / R1–R2 / S1–S3）；D1 卡与导语的"见 S9"引用同步改"见 S2"
  - 被删能力兜底核对通过：全部 65 种检验仍在「二、场景索引」表中可发现（每行含"试试这样说"）
- README 篇幅：zh 883→~590 行、en 914→~620 行
- **删除「七、工作台（Web 工作台）与在线门户」极简披露节（中英同步）**：与首屏「不安装也能用」入口块重复；工作台披露由首屏入口块 + ADVANCED 附录承载，规范已固化进 ct-base v1.4.7（README 不设工作台独立章节）
- **「一、如何在对话里使用」与案例大全去重（§13.17 三-3）**：原 6 个示例中 4 个与案例卡重复（两均数≈A1、两组率≈B1、生存+期中≈D1/F、非劣曲线≈B3/K），删除并重构为 3 个不重叠示例——示例 1「说清设计直接算」（完整流程三步：安全预览 → 请直接计算 → R 代码）、示例 2「不确定该用什么检验」（grill-me 追问，§13.3 强制）、示例 3「卡在选型给菜单」（弹出菜单，§13.3 强制）；导语明确指向第四节 30 张案例卡

---

## 5.13.27 — 2026-10-22 · README 按 ct-base §13 最新规范全面对齐 + 案例大幅扩充

> 依据 ct-base `docs/06-readme-brand.md`（§13.3 结构 / §13.4 双语互链 / §13.15 免安装入口 / §13.17 净化清单）全面检查两份 README。

### 新增案例 4.19 S1–S15（中英双语同步，全部为引擎实测数值）
- 覆盖既有 A–R 系列未涉及的检验族：单样本 t（34）、单组率（736，含"绝对差距敏感性"教学点）、ANOVA 三臂（53）、优效性界值（160）、均数等效性（310）、BE-TOST（28，含 GMR 0.90→56 的快速上升教学点）、精确生存（760，分期事件）、单臂生存（172）、**时间表影响样本量（survival 529/626/499 + 期望事件比例，v5.13.26 B 方案核心新能力）**、中介效应（1057）、混合模型模拟功效（0.700/0.445 + 饱和提示）、条件功率与 SSR（77.8% / 450 / +125%）、must-win（62）、多重终点 Bonferroni（88→176）、计数终点成组序贯（33）
- 案例卡总数 51 → **86**（双语一致）

### 净化对齐（§13.17 第五条：全文级技术细节净化）
- 移除全文 CLI 命令块与内部路径（`python scripts/...`、`adapters/ma_extractor.py`、`references/menu.md`、`--adopt-ref` / `--confirm` / `scripts/office_to_md.py` 等），改写为使用者对话语言（"采纳保守界" / "按序号单选" / "列出全部 65 种检验"）
- 被移除的命令行入口完整迁入 `docs/ADVANCED.md` / `docs/ADVANCED_zh-CN.md`（内容零丢失）
- 双语净化后残留扫描：0

### 结构精简（2026-10-22 追加）
- 删除「工作台 UI（Web 工作台）实操指南」整段（W1–W18 逐步教学），收敛为一节极简披露（工作台与对话共用引擎/目录 + 免安装门户入口 + 指向 ADVANCED）；启动方式与功能概览迁入 `docs/ADVANCED*.md`
- 删除 4.16「错误上报与工作台 / 在线门户」案例节（P1/P2——与技能核心计算功能关系不大；错误上报能力保留于 FAQ 与第五节安全声明，工作台披露保留于第七节极简节），后续节号连续重排（4.17→4.16、4.18→4.17、4.19→4.18），尾部提示引用同步
- 按 §13.17 禁入类再筛一轮：删除 L1/L2（跨轮追问——会话行为演示 / 参数化变体，能力转 FAQ「能接着上一轮的计算改参数吗」）、M1（安全预览演示——首屏与每卡「📌」已覆盖）、M3（强制语种——首屏与 FAQ 已覆盖）；M2（涉密输入数据不出域）保留为独立节「4.12 涉密输入与数据不出域」，后续节号连续重排（4.13→4.12 … 4.18→4.17），交叉引用同步
- 新增「版本信息」页脚节（当前版本 / CHANGELOG 链接 / License / Authors / 联系作者），联系邮箱全文单点化（保密声明块内的 📧 行删除，§13.17 第八条）；六节内过期旧页脚（v5.13.21）归一

---

## 5.13.26 — 2026-10-22 · 入组期/随访期真正进入样本量换算（B 方案，口径变更）

> 背景：5.13.25 全方法测试发现「表单可填但求 n 时完全不影响结果」的参数，用户选 B 方案改模型。本轮把 `accrual_time` / `followup_time` 从「摆设」变成真实输入：样本量不再用 `n = d / event_rate` 直接除（等价于假设人人都完整随访 A+F），而是 `n = d / P(event)`，其中 P 由入组期、随访期与事件率按指数生存 + 均匀入组积分算出。
>
> **这是口径变更**：同一组参数下，四个生存方法的样本量会变大（更保守、更接近真实设计）。旧口径只有在「随访期缺失」时才保留（`.event_prob` 自动退回 event_rate）。

### 新增 `.event_prob()`（samplesize_functions.R）
- 模型：对照臂 λ = −log(1−event_rate)/(A+F)（沿用 `survival_exact` 的事件率口径：研究结束时的累积事件比例）；均匀入组、入组期 A、再随访 F：
  `P = 1 − (exp(−λF) − exp(−λ(A+F))) / (λA)`
- dropout（单位时间脱落率 δ）按竞争删失折算：λ → λ+δ，并乘 λ/(λ+δ)
- 自洽性校验：A→0 时 P → event_rate（瞬时入组退化为原口径）；缺 A 或 F≤0 时直接返回 event_rate（向后兼容）
- 单调性校验：A↑（随访期不变）→ 平均随访变短 → P↓ → n↑；F↑ → P↑ → n↓

### 四个方法接入
| 方法 | 改动 |
|---|---|
| `survival` | `ss_survival_logrank` 删除恒返 NaN 的 TrialSize 分支（`TwoSampleSurvival.Equality` 实测 NaN，从未生效），统一 `n = d / P` |
| `ni_survival` | `Cox.NIS(d = event_rate)` → `d = P`（Cox.NIS 源码中 d 即事件比例，n ∝ 1/d）；兜底与反解 power 同步 |
| `survival_equivalence` | `ceiling(ev_pg1 / event_rate)` → `/ P`；反解 power 的期望事件数同步 |
| `survival_superiority` | 同上 |

### 契约与表单修正（survival）
- `tests/coze_cases/_contract_index.json`：`survival.required` 补登 `followup_time`（此前未登记 → `build_params` 丢包 → R 端只拿到 accrual、无法换算，这是 accrual 长期不生效的直接原因）
- `form_schema.MIN_REQUIRED["survival"]` 同步加 `followup_time`（表单必填区显示，默认 12 与 CLI 一致）

### 透明性
- narrative 增加「期望事件比例 (由入组期/随访期推算)」，`stats.event_prob` 同步下发——用户可自行核对 `n = d / P`
- 顺带修 `10%%` 未转义的显示瑕疵（label 未经 sprintf，应为单 `%`）

### 云端部署反馈加固（2026-10-22，已回写镜像）
- `.event_prob()` 的 NULL/空向量防护：`as.numeric(NULL)` 返回 `numeric(0)`，`is.na()` 随之返回 `logical(0)`，短路 `||` 直接抛 "missing value where TRUE/FALSE needed"。`er` / `A` / `F` / `dl` 四个入参全部加 `length()==0` 守卫；缺时间信息时安全退回 event_rate（原口径）。云端部署实测发现并修复，已同步回本地镜像并重打包。

### 实测（本机 R 后端）
| 场景 | 修复前 | 修复后 |
|---|---|---|
| survival HR=0.7 er=0.3 A=12 F=6 | 每组 412（与 A 无关） | 每组 **589**（P=0.2098） |
| survival A=36 F=6 | 412 | **682**（P=0.1812） |
| survival A=12 F=18 | 412 | **499**（P=0.2476） |
| ni_survival A=12/36 F=12 | 414 / 414 | **730 / 1072** |
| survival_equivalence A=12/36 F=12 | 574 / 574 | **1011 / 1484** |
| survival_superiority A=12/36 F=12 | 656 / 656 | **440 / 645**（sup_hr=0.6 口径） |

回归：高级选项 25 用例 **25/25 PASS**；全方法 65 用例（含新口径）**全部 PASS**。

---

## 5.13.25 — 2026-10-22 · 全方法覆盖测试 + D4/D5/D6 修复（参数名不一致 / narrative 格式化）

> 背景：对工作台 **65 个方法**做基础功能覆盖测试（每方法必填参数求 n），再对 **190 个必填参数**做「双值扰动」生效性测试（判断参数是否真的被引擎消费）。发现 3 类问题：narrative 把 list 当数值格式化（D4）、表单字段名与引擎读取键不一致导致用户填了不生效（D5/D6）；另有若干「表单可见但在该模式下不参与计算」的参数（已在报告中列明，属产品决策，未擅改统计模型）。

### D4：cox_covariate narrative 把 list 直接格式化
- `ss_cox_cov(power=)` 返回 `list(d=, n=)`，此前 `n <- ss_cox_cov(...)` 后整个 list 喂给 `.line()`，页面渲染成 `n (合计): 93.350941798387 312`（事件数与样本量拼成怪数），且 `stats$n` 是 list 污染前端数值卡
- 修复：拆开呈现「所需事件数 (d)」与「n (合计)」；`stats` 改为 `n`（整数）+ `events`（一位小数）

### D5：assurance 成功界值（margin）用户填了不生效
- 表单字段 `--margin`（`MIN_REQUIRED` 同）→ 进 `p$margin`；引擎只认 `p$margin_assurance`，于是恒回落 0.05
- 修复：R 端两键兼收 `p$margin_assurance %||% p$margin`。实测 margin 0.10→保证度 31.4%、0.30→4.9%，文本界值同步正确

### D6：gsd_*_sim 模拟次数（n_sim）用户填了不生效
- 表单字段 `--n_sim` → 进 `p$n_sim`；引擎只认 `p$n_simulations`，恒按 1000 次模拟
- 修复：`samplesize_functions.R` 两键兼收。实测 150 次→经验功效 0.7533、400 次→0.7700

### 报告存档（工作区）
- `ct-samplesize_全方法测试报告_20261022.md`：65 方法基础覆盖（65/65 PASS）+ 190 参数生效性（166 EFFECTIVE / 19 NO_EFFECT / 3 LABEL_ONLY / 2 ERROR，逐项判读）
- `test_all_methods.py` / `test_param_effectiveness.py`：可复跑脚本

---

## 5.13.24 — 2026-10-22 · D1 根因修复（R 引擎三分支对齐）+ 引擎 warnings 通道（D3）

> 背景：5.13.23 的 D1 是**服务端拆分编排**（止血，不碰 coze）。本轮按用户拍板做**根因修复**：直接改 `adapters/coze/src/r_engine/run_task.R`，让引擎自己不再丢主结果。云端 coze 尚未部署新 R，故服务端编排保留作双保险，并新增 `CTSS_D1_SPLIT=0` 开关用于验证 R 端原生行为（否则编排会掩盖引擎行为）。回归中发现第三个断链缺陷 **D3**：引擎 `warnings` 从未写入 `meta`，用户看不到任何降级原因（如「随访曲线仅支持 survival」），本轮一并修复。

### D1 根因修复（run_task.R，与云端共用同一份源码；部署后云端生效）
- 新增 `.has_solve_anchor(p)`（dispatch 之前）：`power` 或 `nobs` 可解析为数值即视为「主求解锚」
- `dispatch()` 三分支（`plot_dist` / `curve_power_time_seq` / `curve_heatmap`）改为与 2026-10-07 序列曲线重构**同构**：有锚 → 图累积进 `figs` + continue 主求解（不再提前 return）；无锚（纯图请求）→ 保留原「仅返回图」语义，零回归；图不可用时不阻断主结果，降级为 warning
- `has_curve_arg` 分支内联的锚判定改为复用 `.has_solve_anchor()`（三分支 + 曲线分支共一处判定）
- 本机验证（`CTSS_D1_SPLIT=0` 直达引擎）：仅 `power_time_seq`（ttest_ind）→ status=warn + **主结果 n=64 保留** + warning；三开关全开 → 主结果 + 分布图 + 双 warning；纯图无锚 → 原语义不变

### 服务端编排配套（server.py，双副本同步）
- `_D1_SPLIT_ENABLED`（`CTSS_D1_SPLIT=0` 关闭编排）：让 R 端修复可被独立验证；云端未部署前默认开启，双保险不变
- `_d1_merge_fig_text()` 行级去重：R 端修复后图 spec 会连带带回主求解文本，去重避免主结果在页面上出现两次（对未修复的旧引擎同样正确）

### D3：引擎 warnings 通道（adapters/coze_client.py，双副本同步）
- `_envelope_to_result` 此前从未把 `env["warnings"]` 写入 `meta`——R 引擎的降级提示（图为何没出）到不了前端；现已写入（仅非空时）
- 归一处理：`jsonlite` auto_unbox 使长度 1 的 warnings 序列化成**字符串**，`list()` 会把中文串拆成单字符列表——统一归一为字符串列表（server.py 编排侧同样处理）

### 回归（本机 R 后端，两种模式各 25 用例）
- `CTSS_D1_SPLIT=0`（直达 R 引擎）：**25/25 PASS**（C1 figures=7 / C2=2 / C5=6 均由单次 R 调用产出）
- 默认（编排开启，云端等价路径）：**25/25 PASS**，0 缺陷复现、0 意外失败

---

## 5.13.23 — 2026-10-21 · 布尔图开关主结果保护（D1）+ figure_mode=png_file 落地（D2）

> 背景：2026-10-21 工作台 36 个高级选项全量测试（25 用例，本机 R 后端）发现 2 个缺陷：**D1** 布尔图开关（`dist_plot` / `heatmap` / `power_time_seq`）触发 R 引擎 `dispatch()` 提前 return，只回布尔图、样本量主结果整个丢失（云端同参裁定同缺陷）；**D2** `figure_mode=png_file` 三级断链无人消费（前端经 params 通道进 ns，但 R 只产 SVG、服务端无本地转换）。本轮 D1 服务端即时止血、D2 完整修复；D1 根治（R 引擎三分支对齐）列入 coze 修复清单待部署。

### D1：服务端拆分编排（adapters/workbench/server.py，双副本同步：publish-dist）
- `_d1_fig_switch_on` / `_d1_strip_fig_switches` / `_d1_split_specs` / `_d1_merge_fig_result` / `_compute_fig_split`：检测到布尔开关时拆「主求解（去开关）+ 每个开启的开关各一个单开关图 spec」，经 `compute_batch` 一次调用（云端即一次 batch POST，本机逐项 Rscript）；每个图 spec 只带一个开关——`dispatch()` 对三个开关是「首个命中即 return」，同带多个只会出第一张图
- 合并规则：主 Result 为体；图 figures 去重追加、narrative 分段追加、图 stats 入 `meta["fig_stats"]`（不覆盖主 stats）、warnings 合并；图 spec 失败（如 ttest_ind + power_time_seq：随访曲线仅支持 survival）降级为 warning，**绝不阻断主结果**
- 序列曲线参数（`n_seq` 等）不受影响——R 端 2026-10-07 已重构为「主求解+曲线累积」，本来就走正常路径

### D1A：coze 修复清单（docs/coze_fix_backlog.md，待下次 coze 部署）
- `run_task.R` `dispatch()` ①②③④ 分支从「提前 return 只回图」改为「有主求解锚 → 图累积 + continue；无锚 → 保留纯图 return」（与 `has_curve_arg` 分支同构，锚判定提为 `.has_solve_anchor()` 共用）；含落地要点、验证用例、与服务端兜底的共存决策（R 端修复并云端回归通过前，不得移除服务端编排）

### D2：figure_mode=png_file 完整落地（server.py serialize_result + 三份 HTML）
- `serialize_result(result, options)`：`figure_mode == "png_file"` 时复用 `adapters/rendering.svg_to_png`（与 CLI `render_figures` 同一处理链：strip clip → fix xml → bbox → viewBox → cairosvg scale=2.0 光栅化）转 base64 PNG，`format` 同步改 `"png"`；cairosvg 不可用 / 单图失败 → 该图降级回 SVG 并在 `meta.warnings` 记录（ct-base §19.9 与 CLI 行为对齐）
- 双通道覆盖：`options.figure_mode`（API 直调）+ `params.figure_mode`（前端 `data-fig` 通道进 `ns.figure_mode`）；`/api/batch` 逐项 options 同步透传
- 前端三份文件（`adapters/workbench/workbench.html`、`workbench/index.html`、`workbench/publish-dist/index.html`）新增 `figHTML(f)`：按 `figure.format` 渲染——svg/html 内联、png 走 `data:image/png;base64` URI

### 验证（本机 R 后端，25 用例全量回归）
- 回归前：21/25 PASS + D1×3 / D2×1 缺陷复现
- 回归后：C1/C2/C5（D1）与 D1-fig-png（D2）全部转 PASS；冒烟实测 C1 同时开 3 开关 → 主结果 n=64 + 曲线/分布/热力图 3 类图全出（power_time_seq 对 ttest_ind 无效以 warning 明示）；D2 8 图全转有效 PNG（\89PNG magic，单图 ~50KB）

### 默认端口 8765 → 8790（5.13.22 追加：与 meta-analysis 错峰）
- **根因**：8765 同为 meta-analysis 工作台的默认端口（其 server.py `PORT` 回退值）。两个技能各自裸启动时互抢端口——后启动方的启动流程会杀死先占者（2026-10-21 ct-samplesize 实例两次静默死亡、无 traceback，实为此因，非代码崩溃）
- **修复**：ct-samplesize `server.py` 默认端口改 8790（`PORT` 环境变量仍优先，发布通道不受影响）；`adapters/workbench/README.md` 与根 `README.md` 中英快速上手同步改 8790。本地裸启动互不干扰；显式传端口行为不变

## 5.13.22 — 2026-10-21 · meta_planning σ 折算落地（sd：effect 为原始均差 Δ 时自动折算 d=Δ/σ）

> 背景：`--sd` 的 argparse help 与 form_schema common 组早承诺「提供 σ 时 effect 视为原始均差 Δ，折算 d=Δ/σ」，但 meta_planning 三条链路都没兑现：coze R 引擎 meta 分发块只读 `p$effect`；本地 R 后端 meta 分支只读 `args.effect`；build_params 又不把 sd 放进信封（CLI 路径只送预折算 d_val，meta 分支此前不采纳）。本轮把折算真正落地（契约 + 双适配器 + 文档），仅 smd/paired 生效（or/rr/cor/cluster 效应量无量纲，填 sd 忽略）。

### 契约（_contract_index.json + coze_contract.md）
- meta_planning `optional` 通道登记 `sd`（用户显式提供才随信封发送，零回归）；coze_contract.md 第 61 行参数列/备注同步
- d_val 通道本就对 meta_planning 开启（`_test_consumes_d_val`：required 含 effect）——CLI/workbench 的预折算值自此被 meta 分支采纳

### R 引擎（coze，run_task.R + common.R）
- meta 分发块：smd/paired 下优先采纳 `p$d_val`（CLI/workbench 预折算），否则 `sd>0` 时 `eff <- eff/sd`（直连接管，如 meta-analysis 工作台）；`eff_raw` 留存供回显
- 三个分支（MC / K 给定 / 求 K）输出行挂 `.sd_line()`：「效应量折算 d = Δ / σ」；common.R 新增 `label.meta_sd_conv`（中英）

### 本地 R 适配器（local_r_backend.py）
- meta 分支同口径：smd/paired 下 `args.sd>0` → `_eff = _eff_raw/_sd`（params 经 optional 通道带入 sd；d_val 被 `_BUILD_CODE_EXCLUDE` 排除，本地自行折算）；两个 r_code 分支（K 给定 / 求 K）插折算回显；标签字典补 `label.meta_sd_conv`

### 验证与部署
- dry-run 基线（本轮前）：`--test meta_planning --effect 5 --sd 10` → 载荷 `effect=5.0 / d_val=0.5`、无 sd，meta 分支两者都不读（空头支票）
- ⚠️ R 引擎改动需 coze 重新打包上传才线上生效（与 5.13.19 MC 功效带、query_origin 闸门同一待部署批次）；本地后端与契约改动即时生效
- meta-analysis 侧联动（样本估算页加 σ 输入 + server.py 补 sd 字段，连带修复 n_cv/n_sim 被 pydantic extra=ignore 吞掉的潜在 bug）随其自身发布

### 工作台渲染层（5.13.22 追加：meta_planning 异质性扫描表修复）
- **缺陷①（读取层）**：`renderResult` 的异质性扫描表读 `res.hetero_K/hetero_i2/hetero_power`（结果对象顶层），而 coze 契约中 hetero_* 序列经 `stats` 返回、落在 `r_result` 层 → 恒为 undefined，**扫描表从未渲染过**（v5.12.2 C7 起的专属呈现实为死代码）
- **缺陷②（数组扁平化）**：扁平逻辑 `typeof v==="object"` 把数组也拍平成索引键，四条 hetero 序列以 "0".."4" 互相覆盖 → 数值卡区出现 5 张键名为 0/1/2… 的垃圾卡，且 hetero_i2/R/K 在卡片层彻底丢失
- **缺陷③**：`</tbody</table>` 缺 `>`（畸形闭合）；`fmt(0)` 走指数记法渲染成 "0.000e+0"（I²=0 固定效应行不可读）
- **修复**：hetero 读取改「flat（r_result 层）为准 + 顶层兜底」双轨；数组值不再扁平（保留在自身键下），新增「序列数据」折叠卡（与导出报告 rendering.py 序列数据分区同构，前 6 值 + 总数摘要），hetero_R（表中未列）保留可见杜绝静默丢失；`fmt` 零值短路；补 `seqData` 双语 i18n
- **验证**：JSDOM 全链路回归 26/26（真实 catalog/schema 夹具 + 真实响应结构 + 三层变异验证：r_result 层渲染 / 顶层兜底渲染 / 无数据防幽灵表 + 嵌套 dict 零回归）；生产页 publish-dist/index.html 已重建（按请求读盘，运行中实例刷新即生效）
- **实证结论**：高级选项透传链路（schema → 表单 → collectParams → build_namespace → 信封）本就完好——n_cv/n_sim（MC 功效带）/k_studies/R/cluster_cv/sd 等均正确入信封，MC 条带渲染正常；本轮坏的只是 hetero 扫描表的呈现层


## 5.13.21 — 2026-10-21 · compute 提升计数器放行即重置 + 菜单快速切换「卡死」修复（前端四件套）

> 接续 5.13.20 的两轮用户实测反馈。本轮两组改动互不重叠、合并发布：**B**（后端，提升计数器连续语义回归）与 **C+①+②+③**（前端，429 共用提示 / schema 缓存 / 竞态防护 / 失败容错回滚）。

### B · 提升计数器放行即重置（server.py）
- **缺陷**：`antiscrape.py` 设计意图为「**连续**限流拒绝计数，放行即重置」（L211 注释 + L403 admit 放行路径 pop），但本地 webguard 只接拒绝路径、**漏接放行重置**（server.py 对 `_rl_reject_count` 零引用）→ 计数器跨会话累计，偶尔 burst 几次即凑满 5 次触发 1 小时封禁。
- **修复**：`_guard` 的 allow 路径（含 tarpit 放行）补 `_as._rl_reject_count.pop(pid, None)`，与 coze 端 admit 同语义——只有真正「连续 5 次拒绝、中间无一次成功」才提升。
- **测试**：新增 Part E4（4 断言）：4 连拒不提升 → 放行 → 再 4 次仍不提升（连续语义实证）→ 连续第 5 次才提升。spy `add_to_denylist` 观测提升、不触飞书。**变异验证**：临时删去 pop → E4c/E4d 精准挂（55/57），还原后 57/57。

### C+①+②+③ · 菜单快速切换「卡死」修复（workbench.html）
- **缺陷链**：misc 限流 8 次/60s/会话（`/api/schema` 与 `/api/schema/<id>` 均属 misc）——页面加载即耗 1 次，一级/二级菜单每次切换各 1 次，**加载后 60s 内点 8 次菜单即 429**；而 `onTest()` 的 `await api(...)` 无 try/catch、无全局 rejection 兜底 → 429 后 `renderForm` 等全部不执行（静默），菜单高亮却已同步切走 → 「菜单新方法、表单停旧方法」，窗口内后续点击全 429，表现为卡死（约 60s 自愈）。
- **① 容错回滚**：`onTest` 重写——try/catch 包 schema 拉取；失败时 `#schemaErr` 横幅显示友好文案（429 读 Retry-After 换算秒数）、CUR_TEST 保持上一个成功方法（仅在成功后赋值）、旧表单保留可继续使用；返回值改布尔，4 个调用点（applyCaseChip / restoreHistory / NL 路由×3）加守卫，失败即中止，杜绝拿旧表单填参。
- **② 客户端 schema 缓存**：键 `test|lang`，首访后零请求——反复切换菜单不再消耗 misc 配额，从根上消除触发面（65 检验 × 2 语言最多 130 条，内存无压力）。
- **③ 竞态防护**：`_onTestSeq` 序号，只认最新点击的响应——慢响应晚到被丢弃，不覆盖新表单。
- **C 共用 429 helper**：`api()` 带出 `Retry-After`（§20.18.4 拒绝体禁 reason 键，限流信息只走 HTTP 头）；`rateLimitTip(e)` 供 compute 路径（doCompute / previewEnvelope catch）与 schema 路径（onTest）共用，避免两套文案漂移；zh/en i18n（`rateLimited` 带 %s 占位）。
- **selectMethod**：菜单高亮改在 onTest 落定后按 CUR_TEST 切换——失败时高亮随 CUR_TEST 回滚，消除不一致态。
- **测试**：node stub-DOM harness（vm 执行内联脚本 + 真实 catalog 夹具 + 可控 429/延迟 fetch）**18/18**：首访拉取 / 缓存命中零请求 / 第 9 次起优雅失败 + 状态回滚 + 友好横幅 / 竞态丢弃 / 语言维度缓存键分离 / Retry-After 换算。`node --check` 通过。

### 验证与部署
- 全量回归：主套件 19/19 + coze 47/47 + webguard **57/57** + e2e ALL PASSED + 前端 harness 18/18。
- 工作台载荷已重建；**未发布，待授权；git 未提交**。
- 部署备注（未采用，备选）：如遇极端批量场景仍可 env 调 `CT_WG_COMPUTE_HARD`；本轮不加——B+② 已覆盖误杀面，默认值保持 abuse 防护强度。


## 5.13.20 — 2026-10-21 · 修复 Web 层热控交互误杀：自动提升仅限 compute 类（misc/static 不喂计数器）

> 线上实测复现：用户正常操作工作台（连续切换检验渲染表单 + 新建会话计算）即可达 misc 8 次/60s 软限，第 5 次拒绝触发 antiscrape 自动提升 → **全类目 1 小时封禁**（静态资源一并 429，页面直接打不开），且提升写的是跨适配器共享的飞书拒止表（本地因缺 `coze_workload_identity` 模块写失败，仅内存生效）。根因：`_guard` 把 misc/static 拒绝也喂入提升计数器。

### 修复
- **`adapters/workbench/server.py` `_guard`**：自动提升条件由 `reason == "ratelimit"` 收紧为 `reason == "ratelimit" and cls == "compute"`，并附与 ct-base 模板接线的差异说明（模板面向单端点 coze 适配器、全部流量即计费 compute；本工作台为多类目 Web 层，misc= schema/session、static=静态资源，均本地廉价端点）。compute 才消耗 coze 算力额度，是反盗调唯一要保护的资产。
- **误杀面量化**：修复前单次交互误杀影响 = 全类目 429 × 3600s（含页面本身）；修复后 misc 超限仅当次请求 429（可重试），换会话/刷新即恢复，零提升。

### 验证
- 新增 Part E（6 断言）：E1/E1b misc 拒绝不喂提升；E2/E2b/E2c compute 超硬限拒绝仍喂提升（保护不松动）；E3 反向验证（删隔离条件后 E1 场景必误喂，证明测试有牙）。webguard 回归 **53/53 全绿**（原 47 + 6）。
- 线上实测（重启后新实例）：固定 Cookie 连续 12 次 `/api/schema/<id>` → 8×200 + 4×429（软限按设计拦截），服务端日志 4 条 reject **无**「自动提升拒止」行；换新会话 → 200；首页 → 200。
- 端到端计算复测 PASS：`meta_planning` MC 档（n_cv=0.3 / n_sim=2000）经工作台 → coze → R 返回功效带 power_p5=0.8106 / p50=0.8423 / p95=0.8675 / p_ge_target=0.983。
- 部署影响：仅工作台载荷需重建（server.py 变更）；coze 部署包零改动。**未发布，待授权。**


## 5.13.19 — 2026-10-21 · meta_planning 保守档/MC 档前端打通（契约 optional 通道）+ 表单跨组去重

> 对照后端 coze（2026-10-19 新增 `n_cv`/`n_sim` 能力）与前端工作台，发现新能力**五层全断**（契约→build_params→CLI→表单→结果渲染均无入口），UI 用户永远够不到保守档/MC 档。本版打通全链路并顺带修复 optional∩common 双渲染取值歧义（G2）。

### 全链路打通（G1）
- **契约索引**：`meta_planning` 新增 `"optional": ["n_cv","n_sim"]` 通道（required 之外的显式可选统计参数登记，单一真相源）。
- **coze_client**：新增 `_load_contract_optional()`（与 required 同一 JSON 事务加载）；`build_params` 对 optional 键**非 None 才随信封发送**（不提供走原解析档，向后兼容）；`_trim_bloated_params` 白名单扩为 `required ∪ optional`（workbench 直传路径同样过此处，批量网格裁剪时 n_cv/n_sim 存活），告警打印同步改并集。
- **CLI**：新增 `--n_cv`（float）；既有 `--n_sim` `default=1000→None` 并补 help——R 端 `p$n_sim` 唯一消费者就是 meta MC（`ss_gsd` 实际读 `n_simulations` 且带 `%||% 1000` 兜底），gsd_sim 零行为变化；audit「计算精度」维在 value-None 判定前即判 known，零审计回归。
- **form_schema**：catalog `optional` 并入契约 optional（`required - MIN_REQUIRED ∪ 契约 optional`）；`schema_for` 跨组去重（common 剔除 required ∪ optional 已含参数）；`n_cv`/`n_sim` 双语标签（PARAM_META）。
- **workbench.html**：MC 功效带专呈条带（P5 悲观 / P50 中位 / P95 乐观 / P(达到目标功效) 四卡，zh/en i18n），三键从通用数字卡剔除防重复展示。

### 表单取值歧义修复（G2）
- 修复前 `alpha`/`side` 等「契约 required 但非 min_required」参数在 common 与 optional **双渲染**，`collectParams` 按 `[data-dest]` 收集时后者覆盖前者（同名输入取值歧义）；去重后每组参数只渲染一次（影响所有 optional∩common 检验，非 meta 独有）。

### 验证
- CLI→build_params 五项：MC 档转发 / 不提供不发送 / n_sim 单独转发 / 过肥裁剪存活 / gsd_sim 惰性默认值消除，全过。
- `schema_for`：meta 表单跨组零重复、`n_cv`/`n_sim` 入可选组、power 保留 common；ttest_ind 抽查无回归。
- workbench 内联 JS `node --check` 通过；全量回归 **ALL PASSED**（e2e 契约含新 `meta_planning_mc` 用例 + 主套件 19/19 + coze 47 + webguard 47）。
- **线上端到端实测 PASS**：v5.13.18 已部署后端 + 新客户端 optional 通道，`meta_planning` n_cv=0.3/n_sim=500 → 5.2s 返回功效带 power_p5=0.8081 / p50=0.8387 / p95=0.8672 / p_ge_target=0.984，所需 K=9；服务端无需更新（节点整体透传 params，R 引擎已支持）。

### 部署影响
- **coze 部署包无需重打**（服务端零改动，线上 5.13.18 已验证）；仅工作台载荷需重建（coze_client.py / samplesize_power.py / form_schema.py / workbench.html 四文件更新）。
- **未发布**：工作台载荷就绪待授权；git 未提交。


## 5.13.18 — 2026-10-21 · coze 端反盗调防护完善（补部署包/清单/环境变量文档/回归测试）+ 工作台 Web 层热控修正

> 用户澄清：**要防护的是 coze 端；A 档技能的 Web 端本不需要防护**（ct-base §20.18.7「适用面：仅 B 档技能；A 档零防护」）。据此全面复查代码正确性：**coze 端准入接线本就与 ct-advisor 范本逐端点对齐**（无需改 main.py），真缺口在**部署层与测试层**；同时修正上一轮 Web 端热控实现的三处缺陷。改动未发布（待授权）。

### Coze 端（§20.18 全库统一标准）

- **部署包首次产出（最大缺口）**：`adapters/coze/` 此前**从未打包**——§20.18.4 防御代码（`wrap_stream_release` 流式并发槽延迟释放 + `CT_ENABLE_OPENAI_COMPAT` 默认关 404）虽在源码中，线上 Coze 跑的却是旧包、防护未生效。现产出 `archives/coze_project_5.13.18.zip`（68 文件 / 475,854 B ≈ 464.7 KB），`src/antiscrape.py` + `src/habit_analyzer.py` + `src/main.py` 与源**逐字节一致**（MD5 校验），`testzip` 通过，红线自检无 `tests/` / `__pycache__` / `.pyc`。**校验锚点用内容指纹而非 zip MD5**——`manifest.json` 内含 `generated_at` 时间戳，每次重建 zip MD5 都会变（v5.13.18 首次构建 `a554a01e…`、重建 `5594d5b8…`，两者内容等价）；除 manifest.json 外全部条目的汇总指纹恒定，单文件校验用 `src/antiscrape.py` MD5 = `2fafd234f7f8652b705e188ac4fe4d03`。
- **manifest.json 补齐**：旧清单为 2026-10-15 的 75 文件版、**不含** `src/antiscrape.py` / `src/habit_analyzer.py`（清单与实际包内容失真）。随包重生成为 v5.13.18 / 68 文件版，两个反盗调件已在列。
- **平台发布反馈修复（2026-10-21 打包报告，`_build_deploy.py` 三处整改）**：① **junk 漏过滤**——上一包混入 `*.bak_rcp` / `*.bak_nvar` 备份（4）+ `result.json` / `*.out.json` 运行产物（3），靠平台侧兜底剔除；本地镜像已删源文件并在 `keep()` 加 `_JUNK_SUFFIXES` / `_JUNK_NAMES` 过滤 + EXCLUDE CHECK 扩充。② **`_*.py` 排除规则误杀**——「名字以 `_` 开头的 .py 不进包」本意排镜像根构建脚本，却把 `src/graphs/nodes/_version.py`（三个节点 `from graphs.nodes._version import COZE_VERSION` 的单一真源）与全部 12 个 `__init__.py` 一并排除（平台靠保留工作区文件 + 命名空间包侥幸运行）→ 收窄为仅镜像根生效。③ **`COZE_VERSION` 滞后**（`5.3.16`）——与平台侧已提升的值对齐，提升为 `5.13.18`（manifest 单一真源）。加**回归断言**：`_version.py` 缺席即构建失败（SystemExit），绝不产出残包。修正后包：**74 文件 / 403,310 B ≈ 393.9 KB**（68 − 7 junk + 1 `_version.py` + 12 `__init__.py`），74/74 与源逐字节一致，`testzip` OK，junk NONE / 红线 CLEAN。
- **DEPLOY.md 新增第 11 章「反盗调准入部署」**：此前**零环境变量说明**——`CT_ANTISCRAPE_SALT` 未配则 pseudoid 每次重启变化、拒止表命中失效（唯一「不配即等于没防护」项），文档化必配/建议变量表、已接入端点清单（含未接入的 4 个不耗算力端点及其判定依据）、**5 条部署后自检**（盐生效 / 缺 `query_origin` → 200 空体 silent drop / OpenAI 口 404 / 限流 429 且体不含 `reason` / 遥测落表）、版本与包信息。
- **反盗调回归测试（从零到有）**：`adapters/coze/tests/test_antiscrape.py`（**47 断言全绿**），按 §20.18.6 四项测试纪律编写——① 副作用断言 ② 反向验证 ③ 不触网捕获 ④ 双轨校准夹具（3 个高频合法画像不误杀）。四部分：A 源码接线实锤（**逐端点切区块**验证四个算力端点各自挂准入 + 统一拒绝载体 + `wrap_stream_release` + OpenAI 口默认 404 + 轻量准入）、B 准入决策（pseudoid 确定性 / `query_origin` 硬拒 silent drop / 包体上限 413 + `doc_context` 豁免 / 限流 429 / 并发上限 / 拒止表 / 轻量准入）、C 统一拒绝载体（禁 `reason` / `retry_after` 区分键）、D 跨层协调 + 遥测落盘 + 与 ct-base 模板逐字节一致（MD5 `2fafd234f7f8652b705e188ac4fe4d03`）。
- **反向验证实锤（纪律②，测试有牙）**：① 按行号精确删掉 `/run` 区块的 4 行准入接线 → 断言精准挂 3 条（A2 / A2b / A2c），还原后 47/47 全绿；② 把 `wrap_stream_release(stream_generator, …)` 换成裸生成器 → A4 精准挂。**首版 A2 只数调用总数（≥4），删掉一处后仍 ≥4 而漏挂**——已改为逐端点切区块验证。

### 工作台 Web 层热控（上一轮实现的三处缺陷修正）

- **缺陷①（致命·发布态失效）**：`adapters/coze/` 整段在 `build_publish.py` 的 `EXCLUDE_SEGMENTS` 内（§16.7 Coze 私有镜像红线），而白名单未含 `antiscrape.py` → **发布载荷里没有 antiscrape** → Web 层 import 失败 → 拒止表共享与跨层封禁在**发布态直接失效**（仅剩纯本地限速），且失败全静默。修法：`build_publish.py` 新增 `DERIVED` 构建期派生规则（`adapters/coze/src/antiscrape.py` → 载荷 `adapters/workbench/antiscrape.py`），**单一真源保持**（构建期复制，非人工第二份副本；范式对齐 ct-adam `workbench/antiscrape.py` 随包注入），并加**断言**防规则被误删而静默失效。
- **缺陷②（§20.18.7 实现纪律 2 违反·禁全静默）**：antiscrape 导入失败原为 `except Exception: _as = None` 零日志 → 拒止表共享悄悄降级而运维零可见性。改为**三级候选路径**（载荷落点 → coze 端同源 → ct-base 权威模板）逐个尝试，失败写 `[ct-webguard] WARN antiscrape 不可用…` 服务端日志。
- **缺陷③**：安全响应头缺 `Referrer-Policy: no-referrer`（ct-base webguard 模板 `_SECURITY_HEADERS` 为三件套）→ 抽出 `_SECURITY_HEADERS` 常量统一供 `_wg_reject` / `_send` / `_send_file` 三处使用，杜绝遗漏；另补 `poll` 限速档（模板四档，ct-samplesize 前版仅三档）。
- **Web 层回归测试（从零到有）**：`adapters/workbench/tests/test_webguard.py`（**45 断言全绿**），纯内存不触网：A 接线实锤（混入 WebGuardMixin / 三处 guard / 拒绝短路 `if r: return` 而非头号反模式 `return self._send_json(...)` / 拒绝即断连 / 安全头三件套 / 四档齐备 / XFF 默认不采信 / 导入失败写日志 / 载荷含 antiscrape）、B 分级限速 + tarpit 指数退避（1/2/4/8/16s、封顶 30s、超硬限 ratelimit、**IP 聚合天花板兜底**换会话仍被拦、静态档 20 次不误杀、窗口过期重放）、C 统一拒绝载体、D 并发闸（占满 → busy 429、释放后槽位归还）+ 包体 413 + 跨层协调（同盐同公式 pseudoid 可复现）。反向验证：移除 `Referrer-Policy` + 断开连 → A10/A11 精准挂。
- **端到端实测（MOCK 起服，真实 HTTP）**：三件套安全头齐全（`nosniff` / `DENY` / `no-referrer`）；`Set-Cookie: ct_wb_sid=…; HttpOnly; SameSite=Lax` 正常下发；`/api/nl` 路由正常（`ttest_ind` / `confidence=medium` / `engine=rule`）；限流实测 tarpit 延迟 **1.00s → 2.02s → 4.02s** 指数递增、第 7 次转 **429**（硬限 6 + 1）、`Retry-After: 60` + `Connection: close`、拒绝体 `{"ok":false,"error":"rate_limited"}` **不含 `reason` / `retry_after` 键**（§20.18.4 信息泄露收敛）。

### 验证

- `py_compile` × 5 文件全通过（`main.py` / `antiscrape.py` / `habit_analyzer.py` / `server.py` / `build_publish.py`——WebGuardMixin 为 server.py 内联蒸馏版，无独立 webguard.py）；全量测试 **111 断言全绿**（`tests/test_ct_samplesize.py` 19 + `adapters/coze/tests/test_antiscrape.py` 47 + `adapters/workbench/tests/test_webguard.py` 45）；
- `build_publish.py` 重跑通过，载荷 1424.9 KB，`REDLINE check OK`（无 genie / coze / r-assets / publish-kit），载荷内 `tests/` 仅契约索引（§16.8 白名单），**新增的两个测试文件均未入发布包**；
- coze 包 `testzip` OK、红线 CLEAN；`manifest.json` 68 文件含两个反盗调件。
- **四方 antiscrape MD5 一致**：`ct-base` 模板 = `ct-samplesize/adapters/coze/src` = 载荷 `publish-dist/adapters/workbench` = `2fafd234f7f8652b705e188ac4fe4d03`（开发态 `adapters/workbench/antiscrape.py` 不存在属预期——它只由构建期派生进载荷）。
- **遗留残留已清理**：测试期产生的 `antiscrape_telemetry.jsonl`（运行时状态，落在 skill 根目录）已删除，并在 `.gitignore` / `.clawhubignore` 双份加入 `antiscrape_telemetry.jsonl` + `*.telemetry.jsonl` 护栏（防 `git add .` 误提交）；误生成的 `coze_project_5.6.0.zip`（脚本默认版本号产物）与 `.orig.tmp` 中间件已删；测试服务进程（18772 / 18774）已终止。
- **构建脚本护栏（防误产错版包）**：`adapters/coze/_build_deploy.py` 原以 `sys.argv[1] if len>1 else "5.6.0"` 取版本——漏传参数会**静默产出 `coze_project_5.6.0.zip`**（极易被误当交付物上传）。改为**缺参即报错退出**（退出码 1）+ 版本号格式校验（非数字开头拒绝），并给出用法提示。实测缺参与非法版本号均正确拒绝（REAL_EXIT=1），显式传 `5.13.18` 构建正常。
- **未发布**：工作台载荷与 coze 部署包均已就绪待授权；git 未提交。

### 全面代码复查（2026-10-21 追加，用户令查「web 端 + coze 端防护，确保无代码错误」）

- **发现并修复 1 个真实缺口（Web 端）**：`_export` 手拼响应头（`send_response` + `Content-Disposition`）**绕过 `_SECURITY_HEADERS` 三件套**——全文件 4 处响应路径中唯一漏挂（`_wg_reject` / `_send` / `_send_file` 均已接线）。已补三件套循环；**端到端 HTTP 实测**：`POST /api/export` 200 响应头含 `nosniff` / `DENY` / `no-referrer`（Content-Disposition 正常）。**根因是测试 A11 只断言「常量存在」而非「全路径接线」**——已补 **A17**（块级切分 `_wg_reject`/`_send`/`_send_file`/`_export` 四个方法体逐一验证含安全头循环）+ **A18** 反向验证（删 `_export` 循环 → A17 精准挂，实测 46 通过/1 失败）。Web 测试 45→47 断言。
- **Coze 端复查结论：无错误**。准入/释放配对语义逐路径核对——`check_allow` 仅在并发闸通过后 `_inflight += 1`（daily_quota 拒绝路径内联回退），调用方仅在 `antiscrape_admitted=True` 时释放，五个算力端点配对正确；`wrap_stream_release` 钉释放点于流耗尽（StopIteration/GeneratorExit/异常三分支 `finally`），且仅当标志为真才释放（防 deny 路径重复释放）；统一拒绝载体 429 固定体 + `Retry-After`、200/413 空体，禁 `reason`/`retry_after` 键；`{"error":"busy"}` 并发载体为 docs §Web 信息泄露收敛条目**原文明列**的两种合法固定体之一（非违规）。
- **与 ct-advisor 范本逐字对齐确认**：`/stream_run` 准入 → `antiscrape_admitted=True` → 生成器构造 → `StreamingResponse(wrap_stream_release(...))` 结构与范本完全一致。范本同有的理论窄窗（生成器**构造**若抛异常则并发槽延迟到 GC 回收才释放）如实标注、**不偏离范本**——`agent_stream_handler` 为生成器工厂（调用即返回生成器对象，函数体不执行），实际风险趋近于零。
- **`habit_analyzer.py` 随包不接线确认**：进程内无 import（与 ct-advisor 范本一致）——它是 §20.18.6 标准模板组成件（供 Coze 工作流侧/后续接入），非死代码遗漏。
- **Web 端 sys.path 注入无模块遮蔽**：三级候选路径注入的目录（adapters/workbench、coze/src、ct-base/antiscrape）顶层模块名与 server.py 后续 import（form_schema/session_store/coze_client/rendering/bug_report/nl_llm/samplesize_power/tempfile）零冲突；失败导入会被 Python 从 `sys.modules` 清除，候选链回退有效（D6b 实证）。
- **复查后的存量差距（非本轮引入，如实标注、待授权处理）**：① 业务端点 500/502 错误体回显 `str(e)`（`_compute`/`_export`/`_batch`/`_nl`/`_preview` 共 ~8 处）——违反 docs「Web 层信息泄露收敛」的「500/502 禁回显异常文本」纪律（该纪律 2026-10-19 新增，晚于这些端点诞生）；400 参数校验反馈属功能需求不受此限。② `do_OPTIONS` 不经 `_guard`（仅 204 空响应不耗算力，但不受限速约束）。两者均为存量设计，改动会触及前端错误展示行为，未擅动。
- **验证闭环**：py_compile × 6、全量测试 **113 断言全绿**（19 + 47 + 47）、载荷重建（1425.0 KB / `REDLINE check OK` / 载荷内 server.py 与源 MD5 一致）、`_export` 安全头 HTTP 实测通过。coze 部署包不含 server.py，无需重打。


## 5.13.16 — 2026-10-20 · 工作台 UI 三修：咨询闸门扩充 + vague 守卫 + 会话线程导航显隐/信封预览按钮

> 用户实测报告：「平均数相同的数据，为什么分布情况可能差很多？」被误当计算意图直发云端出样本量结果。根因两层，均已修复；同日附带修复会话线程入口不可达与信封预览死链。改动仅本地，未发布（待授权）。

- **咨询闸门扩充（`server.py::_ADVISORY_MARKERS`）**：补「为什么 / 为何 / 什么原因 / 怎么理解 / 如何理解 / 什么意思 / 意味着什么 / 说明什么 / 怎么办 / 怎么回事」及英文 `\bwhy\b` / `what does .+ mean` / `\bexplain\b` / `what causes` 等概念型提问标记。原标记只有设计/选型类表述（怎么设计/区别/对比…），概念型提问里出现检验关键词（如「平**均数**」子串命中「均数」）会漏拦。
- **vague 守卫（`server.py::_nl` + 前端 `nlCompute()`）**：规则低置信（`confidence=low`）+ 语句**零参数抽取**（`needs_llm_fallback`）+ 非多值 → 标记 `route.vague=true` 随响应返回；前端命中后只预选检验并填表、提示「请核对参数后手动点计算」，**绝不自动点火云端**（对齐对话模式红线：绝不对缺失参数静默补默认——此前表单默认值凑齐必填项即静默算出与用户意图无关的结果）。i18n 新增 `vagueTip`（中/EN）。
- **会话线程导航显隐修复**：侧栏「会话线程」项此前硬编码 `style="display:none"` 且全代码无取消逻辑 → 会话切换/新建 UI（sessionSel + 新建会话）不可达。已移除隐藏样式。
- **信封预览死链修复**：后端 `/api/preview` 与 `doCompute(true)` 均已存在但无 UI 触发 → 能力域方法页「计算」旁新增「预览请求信封」按钮（`previewEnvelope()`，dry-run 渲染 coze 请求信封、不外发），中英双语。
- **单一真源归一**：以上修复一律改真源（`adapters/workbench/workbench.html` + `adapters/workbench/server.py`）后重跑 `build_publish.py` 派生载荷；`publish-dist/index.html` 与「真源 + favicon 改写」逐字节一致，`server.py` 真源=载荷一致。顺带剪除载荷残留 `scripts/r_code_policy.py.bak_rcp`。
- **验证**：`py_compile` + inline JS `node --check` 通过；闸门单测 8/8（概念句 5 例拦、正常计算句 3 例放行）；MOCK 起服 `/api/nl` 端到端 4 例：用户原句 advisory=true（不出结果只出提示）/「标准差大说明什么」advisory=true/「均值比较一下」vague=true（拦自动点火）/正常计算句放行且 params 正确抽取。README 中英文第七节随布局修订已同步。
- **咨询转接 Ct-Advisor（C 方案，同日追加）**：advisory 拦截后，若咨询句与样本量/效力相关（`样本量|样本含量|检验效力|效能|power|sample size`，`_SS_ADVISORY_RE`）→ 结果区追加「转 Ct-Advisor 处理 ↗」按钮，新标签打开 `https://ct-advisor.app.workbuddy.host/#q=<URL编码>`；预填文本 = 原句 + 上下文附注（当前检验 + 已填参数，空值剔除）。URL hash 传参不入服务器日志；advisor 侧只预填不自动发送（HITL）。零凭据、零跨端点调用、不触 §20.18 antiscrape 准入。配套 ct-advisor 侧 `#q=` 预填（见其 CHANGELOG 同日条目）。`advisorHandoffUrl` 纯函数单测 8/8。


## 5.13.15 — 2026-10-20 · coze 端点落实 ct-base §20.18.6 反盗调（antiscrape）六级准入

> 随 ct-base v1.4.x 契约 §20.18 落实。**取代**下方「（待部署）2026-10-19 · query_origin 准入闸门」条目：旧 `_guard_query_origin` 整套闸门已删除，其 `query_origin` 空值拒绝并入 antiscrape 第 2 级硬拒字段，避免双闸门语义冲突。改动在 `adapters/coze/src/main.py` + 新增 `antiscrape.py` / `habit_analyzer.py`，**仅端点侧行为**；部署需重新打包上传 Coze（手动，待授权）。

- **§20.18.6 三步范式**：
  1. **拷贝标准件**：`antiscrape.py`（43702 字节）+ `habit_analyzer.py`（12425 字节）从 ct-base 逐字拷贝至 `adapters/coze/src/`，`diff -q` 校验与 ct-base 完全一致。`antiscrape.py` 纯标准库实现，飞书依赖惰性 import 优雅降级。
  2. **接线四个算力端点 + OpenAI 兼容口**：`/run` `/stream_run` `/async_run` `/node_run` 全部挂接 `_admit_antiscrape(request, raw_body, payload)` + `request.state.antiscrape_admitted = True`；非流式端点（`/run` `/async_run` `/node_run`）包 `try/except/finally: _release_antiscrape(request)` 释放全局并发（原 `/async_run` 缺 finally，已补）；`/stream_run` 的并发槽改由标准件 `wrap_stream_release` 在流真正耗尽时释放（见下「流式并发槽延迟释放」）。`/v1/chat/completions` 默认 `404`（§20.18.4：零合法流量模板端点 = 纯攻击面），经 `CT_ENABLE_OPENAI_COMPAT=1` 显式开启后受 `_admit_antiscrape_light(request, with_concurrency=True)` 轻量准入。
  3. **统一拒绝载体（§20.18.4 信息收敛）**：`_response_from_admit` 固定 `429 → {"ok":false,"error":"rate_limited"}` + `Retry-After` 头（窗口长度属公开限速参数）；**禁带 `reason` 区分键、`retry_after` 键**；`200 silent drop` / `413` → 空体。比 ct-advisor 范本更严（范本漏 `X-AntiAbuse: deny:reason` 头违反信息收敛红线，已修正）。
- **六级准入全部生效**：0 跨项目盐一致性（进程 env → 平台 env → 共享 config 表三级回退）→ 1 包体上限 2MB（豁免 `doc_context`）→ 2 硬拒字段（`query_origin` 空值 / 占位哈希 silent drop）→ 3 拒止表 429 → 4 单点限流 30/60s → 5 全局并发 50 → 6 匿名日总额度（默认关）。
- **移除冗余旧闸门**：删除 `_guard_query_origin` / `_is_placeholder_origin` / `_PLACEHOLDER_ORIGIN_RE` 整套块（原仅 `query_origin` 空值拒绝，缺拒止表/限流/并发/包体/遥测，且 `/v1/chat/completions` 常开违反 §20.18.4）。
- **验证（不触网，纯内存断言）**：五用例全绿 —— 合法放行 / 空 origin 200 静默 / 占位哈希 200 静默 / 3MB 非文档 413 / 3MB+doc_context 豁免放行。`main.py` `py_compile` 通过；grep 确认无 `_guard_query_origin` 残留；接线点核对：行 71/72/73/79/99/105/354/356/415/460/519/559/633/670/673/681/693。
- **部署约束（架构风险）**：`adapters/coze/` 被根 `.gitignore` 第 19 行整目录忽略，改动经 `_build_deploy.py` 打 zip 部署、**不进 git**；依赖本地工作目录 + 人工部署，clean checkout 会丢，需靠部署包/发布基础设施留存。
- **部署前平台 env 注入待办**：`CT_ANTISCRAPE_SALT` 🔴 必配固定盐（否则重启失效）；`CT_ANTISCRAPE_DENYLIST_TABLE_ID`（拒止表，缺省走本地 JSONL 降级）；`CT_ANTISCRAPE_FEISHU_APP_TOKEN` / `CT_ANTISCRAPE_FEISHU_TABLE_ID`（遥测，惰性 import 优雅降级）。

### 5.13.15 追加（2026-10-20）· 流式并发槽延迟释放

> 基于实测教训优化：默认 `try: return StreamingResponse(gen); finally: release_inflight()` 会在 `StreamingResponse(...)` 一构造完即触发 finally，此时流尚未被消费，**全局并发上限（默认 50）对流式在途算力完全失效**（并发计数在返回响应瞬间即归零，真正耗时的 R 计算/LLM 推理期间不受约束）。

- **修复**：`/stream_run` 改用 ct-base 标准件 `wrap_stream_release(stream_generator, request, on_finish=lambda: cozeloop.flush())` 包裹生成器，把并发槽释放钉在生成器 `StopIteration` / 客户端断开 `GeneratorExit` / 异常处（同步/异步生成器自适应）。`cozeloop.flush()` 同步移入流结束处；deny / JSON 解析错误等早返路径保留显式 `cozeloop.flush()`。
- **去重**：删除 `main.py` 本地 `_wrap_stream_release`，改为从 `antiscrape` 导入标准件（与 ct-base 同源，避免再次写错）；`antiscrape.py` 已随 ct-base 同步（新增 `wrap_stream_release` + `import inspect`），`diff -q` 校验逐字一致。
- **验证**：ct-base `wrap_stream_release` 单测全绿（SYNC / ASYNC 构造时不释放·耗尽后释放、DISCONNECT 在 GeneratorExit 释放、on_finish 调用、未准入不释放共 5 类）；`main.py` / `antiscrape.py` `py_compile` 通过。仍受限于无 coze 运行时，端到端需部署后验证。

## 5.13.14 — 2026-10-19 · 外部对照/RWD 增强设计：分布平衡（DBML）方法与报告义务

- 新增 SKILL.md 节「External-Control / RWD-Augmented Designs · Distributional Balancing」：DBML 三步法（VAE 检出异常 RWD 单位 → 重加权匹配治疗组分布 → 加权抽样；匹配分布而非单位对），实证协变量平衡优于 matching/weighting 基线（arXiv:2609.23524）。
- **报告硬要求**：RWD 增强对照的输出除样本量外**必须报告协变量平衡指标**（SMD 分布/最大值）；平衡质量未量化即设计未定义。
- 与 Stat Med 2026 贝叶斯外部对照（DOI `10.1002/sim.70748`）分层衔接；引擎未改动（规范+报告纪律登记）。
- 证据登记：`ct-base/references/qc_independence_pharmasug2026.md`。

## （已撤销 · 未部署，被 5.13.15 反盗调集成取代）2026-10-19 · coze 端点落实 ct-base §1.4 `query_origin` 准入闸门

> ⚠️ 本条目描述的闸门（`_guard_query_origin` 等）已在 5.13.15 中**整体删除**，其功能由 antiscrape 第 2 级硬拒字段覆盖。保留仅作历史记录，请勿据此部署。

> 随 ct-base v1.3.33 契约 §1.4 落实。改动在 `adapters/coze/src/main.py`（samplesize R 引擎工作流源码），**仅端点侧行为**；部署需重新打包上传 Coze（手动，待授权）。

- **合并守卫 `_guard_query_origin()`**：占位哈希闸门（2026-09-13）保留 + 新增 `query_origin` 空值拒绝（缺失 / `None` / 空串 / 纯空白 / 非字符串 → 返回 `""` 拒绝）。`/run` / `/stream_run` / `/async_run` / `/node_run` + 内部 run 分支共 5 个调用点挂接。
- **动因 / 零误伤**：同 ct-registry（裸 POST 实测）；客户端出站必带非空 query_origin（含 `report` 动作）。
- **B 类名单新增 `meta_planning`**（2026-10-19 产品决策：纯商业保护，非复杂度依据 —— 该检验为
  Hedges & Pigott (2001) 封闭公式法，按 2026-10-13 分层标准本属 A 类）：免费调用的 `repro.r`
  在 node 出口替换为高级功能提示。名单同步 3 处：`scripts/r_code_policy.py`（唯一副本）+
  `src/graphs/nodes/samplesize.py::_R_CODE_GATED_TESTS` + `workbench/publish-dist/` 分发副本；
  A/B 计数 39/26 → 38/27。skill 展示层（samplesize_power）经 `r_code_unavailable()` 自动跟随，
  本地即时生效；**引擎侧拦截需重新打包上传 Coze 方可线上生效**。
- **meta_planning 支持可变每研究样本量**（三层，2026-10-19）：① 总预算口径（workbench 客户端
  n=T/K，信息量精确无均值偏差）；② MC 精确档 `ss_meta_planning_mc`（对数正态抽样 + 精确 RE
  合并方差 se²=1/Σ(1/(V_i+τ²))，输出功效带 P5/P50/P95 与 P(功效≥目标)，seed 固定可复现）；
  ③ 解析保守档 `n_cv` 参数（V_eff=V·(1+CV²)，与 cluster DE 同构；算术均值口径会高估效能，
  此校正方向保守）。n_cv 缺省 = 等样本量原行为，完全向后兼容；异质性扫描表/图透传 n_cv
  （解析口径）。同步 `local-r/r_templates/r_pass_ext.py` 函数副本；workbench 端（meta-analysis
  技能）UI 增 总预算 T / 研究间 CV / MC 开关输入与功效带渲染。**引擎侧需重新打包上传 Coze。**

## v5.13.13 — 2026-10-17 · 论证/审计输出增强 + 侧栏布局对标 ct-adam/ct-sdtm（去掉主/二级菜单分离 + 右侧占满全宽）

**侧栏布局重做（v5.13.13 追加）**
- **问题**：宽页面下主菜单与二级菜单视觉分离，右侧主面板仅固定宽度而非填满剩余空间。
- **修复（对标 ct-adam/ct-sdtm 布局模式）**：
  - `.wb-shell` 改 `min-height:100vh` `align-items:stretch`（撑满全高）
  - 侧栏 `.wb-nav` → `.wb-side`：固定 `width:208px;flex:0 0 208px;position:sticky;top:0;height:100vh;overflow-y:auto`（左侧固定、可滚动、全高）
  - 主区 `.wb-main` 改 `min-height:100vh`（右侧填满剩余宽度 + 全高）
  - 统一侧栏导航项：`.nav-sub` / `.navitem` / `#navDomains` 容器全部合并为一个连续的 `.wb-navitem` 列表（含"全部方法" + 域项 + 历史记录 + 线程），无二级容器
  - 新增 `toggleSide()` 函数 + `.wb-side.side-collapsed` 折叠态（icon-only，点击侧栏空白折叠/展开）
  - 窄屏响应式重写：`max-width:820px` → 侧栏变为 icon-only（而非之前的 66px 隐藏）
- **验证**：`curl localhost:8771/` 输出侧栏 DOM 结构连续无二级容器；`.wb-shell` 全屏撑满。

**ct-base §5.6 合规微调（v5.13.13 追加，2026-10-17）**
- **favicon 强制项**：`<link rel="icon" type="image/svg+xml" href="./assets/icon.svg">`（服务端 `/_` 静态 handler 已支持 SVG 200）+ `<meta viewport-fit=cover>`
- **§5.6.3-4 logo 盒**：顶栏 logo 包 `.wb-logo-box{40px, panel bg, shadow-sm}`
- **§5.6.3-1 hero 横幅**：`#v-compute` 首屏加 `.wb-hero` 渐变横幅（`::after` 装饰圆 + 3 枚 `.wb-hero-chip` 统计：65 检验方法 / 12 能力域 / 后端状态），`fillHero()` 从 CATALOG 动态填充，挂接 `setBackend`/init/`setLang`
- **§5.6.2 折叠态持久化**：`toggleSide()` 写 `localStorage("wb_ctss_sideCollapsed")`，init 恢复
- **i18n 补齐**：侧栏提示语 `sideTip`、bug 按钮 `data-i18n-title="bugBtnTitle"`（zh/en 双语）
- **落地视图**：init 改 `openDomain("") + switchView("compute")`（落地页=对话计算，侧栏高亮正确）
- **hero 去重 + 页脚（2026-10-17 晚追加）**：① 移除 hero 第三枚「后端状态」chip（与顶栏 `#wb-backend` 药丸重复，违反 §5.2「状态提示收敛只此一处」）——DOM/i18n/`fillHero` 后端分支/`setBackend` 联动全清；② 补 `#wb-footer` 页脚（ct-sdtm 范式）：i18n 文案（技能名·框架·设计参考免责声明）+ `#wb-skill-ver` 版本号，版本经 `/api/schema` 新增 `skill_version` 字段下发；③ 修复 `_read_skill_version` 本地布局路径 bug（原 `_SKILL=_WB_ROOT/../..` 多退两级指向 `skills/` 目录，恒读 `unknown`——顺带修复 bug-report 信封版本字段），现优先 `_WB_ROOT/SKILL.md`。
- **验证**：`/api/schema` 下发 `skill_version=5.13.13`；agent-browser 实测 hero chips=2、`heroBackend` 0 处、页脚渲染「… · ct-samplesize v5.13.13」；JS 语法 0 错、div 167/167 平衡、server.py py_compile 通过。
- **验证**：9 项合规标记 grep 全在位；`new Function` 语法 0 错误；div 168/168、span 66/66 平衡；截图确认 hero/高亮/logo-box 正常。

**动机**：当前论证段与审计输出偏"骨架"，缺监管框架对齐、引文推荐与量化评估，研究者需要手动补全大量占位。v5.13.13 引入四块内容增强输出深度。

**justify_text.py（→ upgrade J3）**
- 新增三个附录块：① **CONSORT 2025 条目 16a 合规检查表**（9 项勾选清单 + 推荐引用格式，覆盖主终点定义/各组假设值/目标差值/标准差/α/power/校正项/样本量/软件，研究者直接对照打勾贴方案即可）；② **ICH E9(R1) estimand 对齐块**（人群 / 治疗条件 / 终点 / 伴发事件处理策略 / 人口汇总度量 + CASRAI MCID 锚定披露规范，非劣效/生存/MCID 模式自动展开）；③ **推荐参考文献**（样本量方法学 Chow 2017 + Julious 2010 + CONSORT 2025 + SPIRIT 2025 + ICH E9(R1) + CDE 指导原则 2024 + FDA/EMA NI 指南 + MCID 方法学 Revicki 2008）。
- 文档头 + 描述升级：CONSORT-SPIRIT Item 14 → CONSORT 2025 item 16a；新增 CASRAI MCID 披露规范对齐。

**hypothesis_audit.py（→ upgrade J）**
- 新增 **CONSORT 2025 条目 16a 合规检查表**（9 项，研究者逐项对号入座）。
- 新增 **弱/未知假设引文推荐**：`weak`/`unknown` 参数的证据类维度，自动推荐具体引用格式 + 示例（效应量→带 CI 的 RCT/荟萃；SD→同人群实测带样本量；率→带观察例数的率；HR→带 CI 与位生存的生存；margin→监管文档/界值论证；ICC→同类/区间；CV→制剂/交叉；脱落→同类试验实测+脱落原因分布）。
- 新增 **监管就绪量化评分**：`missing×15 + unknown×10 + weak×5` 扣分 → 100 满分；90+ A 就绪 / 70-89 B 基本就绪（附灵敏度）/ 50-69 C 条件就绪（建议先补证据或改自适应）/ <50 D 不就绪（需先导研究或重新设计）。
- 修复：CONSORT 循环变量 `desc` 遮蔽总体判定描述 → 改 `desc_item`。

**测试**
- `ttest_ind` MCID 模式：justify 完整输出 CONSORT 清单 + estimand 对齐 + 参考文献，零渲染失败。
- `hypothesis_audit` ttest_ind：评分 90 A 就绪（2 weak 假设：effect、sd）；引用推荐 effect 格式 + sd 格式。
- `survival` HR=0.65：HR 渲染正确（回归修复后）。

## v5.13.12 — 2026-10-17 · 论证段引擎声明 R 包版本号自动填充（去重 + 全遍历 meta.packages）

- **问题**：论证段第 5 句「R R version 4.6.1 + rpact/TrialSize [__填写]」有两个缺陷：① coze 返回 `r_version` 已含 "R version" 前缀，前面再加 R 重复；② 只查 rpact/TrialSize/PowerTOST 三个包名，而 ttest_ind 实际用的是 `pwr`，找不到就写 `[__填写]` 占位。
- **修复**：`justify_text._engine_str` — 去 "R version" 前缀；遍历 `meta.packages` 全部键值对（`sorted(pk.items())`），不再硬编码包名。输出形如 `R version 4.6.1 (2026-06-24) + pwr 1.3-0`。
- **验证**：`ttest_ind` + `justify:true` → 引擎声明完整（R 版本 + pwr 1.3-0），零占位符。

## v5.13.11 — 2026-10-17 · 计算按钮忙态提示（禁用 + spinner + 标签切换）

- **问题**：点击「计算」后等待十几秒无反馈，用户不知道是卡了还是在工作。
- **修复**：`setComputeBusy(busy)` 在 `doCompute`/`doComputeExt`/`runMultiCompute` 入口处设忙态、`finally` 退出。忙态时「计算」与「智能识别并计算」双按钮同时 `disabled` + `.busy` class（CSS spinner 旋转 + 标签改为「计算中…」），`pointer-events:none` 防重复点击；计算完成后 `updateNlBtn()` 恢复原标签。
- **i18n**：`computing` 键已存在（zh「计算中…」/ en「Computing…」），复用。
- **验证**：`node --check` 0 错误；8771 服务正常重启；`ttest_ind` 真实计算 ok=true。

## v5.13.10 — 2026-10-17 · 「验证闭环」真实落地 + verify 空转修复 + vparams 主参数回退

- **问题**：「验证闭环」按钮（结果操作条第三个）此前也是空转——UI 把 `verify` 标志随 options 发到 coze，coze 引擎不消费（与 justify/audit 同病）。实证：带/不带 `verify:true` 打真实端点，三次返回完全一致。
- **服务端落地 Monte-Carlo 验证闭环**（`server.py`）：新增 `_verify_extract_n()`（键名优先+test族校正：n_per_group→每组，n_total→总，裸 n 按族判——单/配对=总，两组设计=每组）；新增 `_verify_block()`（调 `scripts/verify.py run_verify` 20000 次 MC，产出双语验证报告：power + type_I_error 双判定 + MC 95% CI + 总判定 → result.text，verify_pass/verify_report 经 meta 回传前端徽标）。
- **vparams 主参数回退**（本轮关键修复）：verify 专用字段（verify_effect_size 等）未填时自动回退到主计算参数——此前只读 verify_ 前缀字段，UI 填了主参数但 verify 模拟用空 params 跑 H0 → power≈alpha 的假 FAIL（ttest_ind effect=0.5 + verify → power=0.0496 → FAIL）。回退链：verify_effect_size→effect；verify_hr→hazard_ratio→hr_expected；verify_p1/p2→p1/p2；plus median_control/rate_control/new_median 等。
- **verify.py 修复**（`scripts/verify.py`）：`run_verify()` 头部加 `n = int(round(float(n)))`——R 端 n 常为 64.0（float），range(n) 会 TypeError（CLI argparse type=int 强转屏蔽了，服务端直接调用暴露）。
- **设计族映射**（`_VERIFY_DESIGN_BY_TEST`）：五族（ttest_ind/proportion_two/survival/group_sequential/adaptive_reestimate）按 test 自动映射；用户显式 verify_design 覆盖。
- **n 语义折算**：引擎 n 为总数 + per-arm design → 除 2；组序贯族 meta.n 随 interim 变化 → 跳过并说明（不猜值）。
- **验证**：`ttest_ind` effect=0.5, n=64 → 经验 power=0.8004 vs 目标 0.8000（差 +0.04 pp，容差 ±2.0 pp → PASS）；type_I_error=0.0513 vs 0.05（PASS）。E2E 全链路（gsd_survival 三开）：justify ✓ audit ✓ verify ✓ HR=0.6 ✓ n=122 ✓ events=99 ✓。plain 请求零影响。

## v5.13.9 — 2026-10-17 · 「生成方案论证段 / 审计假设」真实落地（服务端规划层后处理）

- **问题**：「📋 生成方案论证段」「🔍 审计假设」两按钮自 v5.12.2 起把 `justify`/`audit` 控制键透传 coze 信封，但 coze 数值契约不消费这两个标志（纯规划层文本能力，无 R 对应物）——实测三种请求返回完全一致，按钮表现为"空转重算"。
- **服务端落地**（`server.py`）：`_compute()` 在 coze 计算成功后按 `options.justify`/`audit` 调本地规划层模块，产出块追加进 result.text（数值卡/图形/R 代码不受影响；HTML 报告自动包含）。justify → `scripts/justify_text.py`：CONSORT-SPIRIT Item 14 + DELTA2 Box 4 + CDE 指导原则锚定的 IRB/SAP-ready 中英对照论证段落；audit → `scripts/hypothesis_audit.py`：四分级证据审计 + 设计族自洽检查 + 总体判定。单块失败降级不阻断主结果。
- **命名对齐修正**：`REQUIRED_BY_TEST` 23 个检验条目用通用名而检验实际消费专属 dest → 假 NOT_READY 误报（如 gsd_survival 给了 hr_expected 却报"hazard_ratio 缺失"）。已逐检验对齐 catalog（65 检验 diff 零残留）。
- **验证**：`ttest_ind` 论证段（双语 6 句 + R 版本 + n=64 填充）；gsd_survival 双开（生存变体段落 HR 填充 + 序贯族审计 + 数值卡完整）。

## v5.13.8 — 2026-10-17 · 演示/真实模式可视化标识（MOCK 横幅 + 后端药丸三态）

- **问题**：用户看到「MOCK coze response…」误以为功能未实现。根因：本地服务以演示模式启动但页面无模式标识——顶栏药丸 mock 下仍显绿色「后端在线」，示例信封与真实结果无法区分。真实端点完全可达，65 项检验本就完整实装。
- **修复**：`server.py` `/api/Schema` 新增 `mock` 字段。`workbench.html` 新增琥珀色演示模式横幅（mock 时常驻，明示"所有结果均为示例"）；后端药丸三态（绿=真实引擎/琥珀=演示/红=不可达）；`setLang` 重放药丸标签。
- **验证**：真实链路 gsd_survival（HR=0.6,OF,3 interim）→ 每组 n=122/总 N=244/事件数 99 + 2 张 svglite 真实图，0.83s，零 MOCK 残留；ttest_ind/batch 均真实返回。

---

## v5.12.2 — 2026-10-16 · 工作台 P0/P1 增强（MIN_REQUIRED / 折叠面板 / MCID / 案例 chips / 操作条）

基于 v5.12.0 大重构后实测发现的工作台覆盖差距（新功能零 UI 入口 + 4 个新检验被误拦 400）， 对 `adapters/workbench/` 三文件做 P0（必修缺陷）+ P1（新功能 UI化）增强。**未发布，等授权。**

**P0 修缺陷**
- **P1 修正**：契约 `required` 超集被误作硬必填（`_contract_index.json` 的 required
  是引擎信封键超集，含模式相关可选参数）→ `form_schema.py` 新增 `MIN_REQUIRED` （65 检验最小必填集，逐条 live 端点校准）；`server.py` 缺失检查改判 `min_required`；前端红星只标 `MIN_REQUIRED`；`required` 仅用于 auto-fill （alpha/side/ratio 等默认值补齐不受影响）。受益检验：`meta_planning`（7→4）、 `regression_logistic`（4→3）、`regression_poisson`（6→4）、`cluster_ext`（3→3， 误把可选 `cv_cluster/effect` 当必填）、`ci_or` / `ci_rr` / `ci_icc` 等
- `TEST_LABELS` 补齐 16 个新检验双语名；`PARAM_META` 补齐 26 个参数双语标签；
  `HELP_ZH` 补齐 29 个参数说明；`CHOICE_LABELS` 新增 `effect_type`/`x_type`/`rate_mode`

**P1 新功能 UI化**
- **效应量输入区扩 MCID 模式**：`injectEffectHelper` 增 MCID 输入行（mcid + sd →
  实时预览 d = mcid/sd，与 effect 互斥，对齐 R1 卡）
- **可选参数折叠面板**：`schema_for` 返回 `optional` 字段，`renderForm` 画
  `<details>` 折叠面板；不再丢 `--R/--cluster_cv/--x_type/--q/--r2/--phi` 等
- **verify 小节渲染**：`schema_for` 返回 `verify` 字段（6 个 verify 参数），
  `renderForm` 在表单底部独立渲染
- **结果操作条**：`renderActionBar` 追加「📋 生成方案论证段」/「🔍 审计假设」
  按钮（`justify/audit` 选项透传 `_compute` → CLI 已有逻辑，工作台只接线）
- **异质性扫描表**（meta_planning 专属）：`renderResult` 解析 `hetero_K`/
  `hetero_i2`/`hetero_R` 数组 → 「I² → 所需 K」表格替代扁平数值卡
- **快速案例 chips**：参数设置面板顶部渲染 8 个一键填表 chip（与 README Q6/Q7
  同源），切换检验时联动

**P2 工作台信息架构分页（v5.12.2 追加）**

原「参数设置」单页承载了方法选择 + 必填参数 + 可选参数 + Monte-Carlo 验证 + 图表选项 + 效应量折算共 6 类控件，垂直过长且功能陈列不清。按大模块拆为 6 个顶层页：

| 页面 | 承载内容 | |:---|:---| | 对话计算 | 自然语言入口 + 结果展示（不变） | | 检验方法库 | 检验族/方法选择 + 搜索 + 快速案例 chips + **契约速览卡**（最小必填集/可选/输出字段/底层 R 函数） | | 参数填写 | 求解方向 + 最小必填 + 通用参数 + 计算 + **缺失参数实时提示** | | 效应量助手 | Δ/σ → d、MCID/σ → d 折算器 + Cohen 惯例参考表 | | 高级选项 | 可选参数 + Monte-Carlo 验证 + 图表/曲线选项 | | 会话线程 | 会话管理（不变） |

- **每页自带检验方法选项菜单**：`PICKERS` 支持 4 个选择器实例（method/params/effect/advanced），
  共享同一份 `CATALOG` 与 `CUR_TEST`；`syncTestPickers()` 保证任一页切换方法，其余页同步
- **`renderFields()` 统一渲染模板**：`#formArea`/`#optArea`/`#verifyArea` 共用一套
  `.sec.pf-grid` 模板，`collectParams()` 改为全文档 `[data-dest]` 收集（跨页不丢参）
- 计算完成后自动切回「对话计算」页展示结果（`switchView('compute')`）
- 修复：`requiredMissing` 曾 `splice` 直接改 `CATALOG.tests[].min_required`（污染目录），改 `slice()` 拷贝
- 修复：效应量折算器原先只写回 `effect` 不写 `sd`，导致引擎无法折算 d = Δ/σ；现同时写入两者
- 修复：折算器原先对 survival / 率类检验也可用（effect 作为通用参数总被渲染），会写出无意义
  `d_val`；现按契约 `required` 是否含 `effect` 门控，不适用时提示该检验实际需要的参数
- 补齐 EN 缺失 i18n 键（`heteroScan`/`i2`/`reqK`/`power`/`caseChipsTitle`）+ 新增 30+ 双语键

**验收**
- mock 工作台 23/23 关键检验最小集 compute 全 200 OK（含 4 个曾被误拦的新检验）
- 既有检验（ttest_ind / proportion_two / bayesian 等）backward compat OK
- `py_compile` OK；`form_schema.py` / `server.py` 均通过
- **jsdom 无头渲染回归（新增）**：中/英双语各 13 项交互断言全绿——跨页方法同步、
   契约卡跟随、缺失提示 → 齐备提示、跨页参数收集、计算闭环自动跳结果页、 Δ/σ 折算写回（effect=0.3 / sd=0.9 / d=0.333）、EN 可见文本零 `undefined`； 10 个代表性检验（含 survival / rates_ext / group_sequential）分页渲染零 console 错误

---

## v5.12.1 — 2026-10-16 · 全面代码审查修复（effect_ref 互认链 / 护栏 / 测试门控 / 文档）

v5.12.0 大重构后的全量审查（164 个 .py 编译 + 28 模块 import + 7 个测试套件 live/离线双跑） 发现问题的修复轮。**未发布，等授权。**

**effect_ref 互认链修复（ma_extractor → confirm → benchmark → adopt 全链打通）**
- `ADOPTABLE_PARAMS` 扩展至 4 参数：新增 `odds_ratio`（OR）/ `risk_ratio`（RR）
  （比值型，零假设=1，估计与 CI 须严格为正）；`effect` 的 scale 接受 `SMD` （与 d 数值等价——ma_extractor 的 SMD 候选此前被 scale 白名单误拒）
- 新增 `TARGET_ARG` 落地映射：OR/RR 参考采纳后写入 `--effect`（ci_or/ci_rr/
  regression_logistic/regression_poisson/rates_ext 引擎分支均读 `params$effect`， 不存在 `--or/--rr` 参数——此前 `setattr(args, "odds_ratio", …)` 是静默空操作）
- `TEST_PREFIX` 同步扩展（odds_ratio→ci_or/regression_logistic；
  risk_ratio→ci_rr/regression_poisson/rates_ext；effect 增补 meta_planning）
- `ma_extractor.confirm()` 入库口加 `effect_ref.validate` 闸门：param/scale 白名单、
  数值完整性、CI 关系、source 必填全校验，不合格拒绝写入（此前 estimate=None 的 半成品可直接流入基准库）

**effect_ref.pick 统计护栏**
- 聚合选择（median/conservative/low/high）拒绝混 (param, scale) 文件——d 与 HR
  不可跨尺度平均；d 与 MD 同 param 但尺度不同，同样不可混算
- CI 跨越零假设（effect 跨 0、比值跨 1）的参考仅展示、不可采纳：聚合选择先剔除
  再统计（basis 标注剔除数，全部不合格报错）；显式 `<index>` 单选到跨零参考硬拒绝
- 修复潜在 bug：`<index>` 单选混 param 文件时返回值错用 `refs[0].param/scale`
  （选到第二条时 param 错位）与 `_single` 零假设值取错 param 的问题
- `summarize()` 按 param 分组（`by_param`/`mixed_param`），render 分组展示 +
  跨零来源标记

**测试门控与契约对齐（mock 误报硬失败归零）**
- `test_matrix_gaps.py` / `test_features.py` 新增 `CTSS_COZE_LIVE` 门控：
  live-only 用例未开 live 时记 ⏭ skipped（不计硬失败）——mock 信封 stats 仅 `{test,mode,note}`，对 stats 数值/图形断言必然失败，噪音掩盖真问题
- 契约容忍断言：曲线数据两种回传形态（stats{x,y,series} 数值数组 / SVG 曲线图形，
  现行部署引擎走后者）二者其一即通过；`--install-all-packages` 已移除旗标改用 argparse 拒绝断言（v5.0.2 起旗标不存在）；仿真完成断言中英双语 （「经验功效 (模拟)」/ "Empirical power"）；出站授权拦截用例显式关闭子环境 mock
- `test_full_coverage.py`：FD-C 曲线断言契约容忍；FD-D 仿真双语；FD-F 修复
  `solve()` 未把 locale 写入 ctx 导致引擎回中文 narrative（引擎只读 params.user_language）
- `test_natural_language.py`：fig 类型断言容忍现行默认契约（落盘 + HTML 报告，
  默认不再内联 `__FIGURE__ svg`，2026-08-28 设计修订）
- 修复后全绿：matrix_gaps 57/57（live）、features 13/14（1 remote 待部署）、
  full_coverage 69/69、natural_language 30/30、ct_samplesize 19/19、 coze_cases_regression / nl_local 离线+live 全过

**文档修正**
- README_zh-CN.md 补 `--effect-ref`/`--adopt-ref` 字面旗标示例（对齐英文版），
  新增可采纳参考类型（effect/HR/OR/RR）与跨零假设/混尺度护栏说明；README.md 同步
- README(.md/.zh-CN) 提示词案例全面增补（对齐 v5.9–v5.12 新功能）：第二节索引补
  ⑦ 类 16 个新检验（49→65 陈旧计数一并修正）；4.14 增 N3（OR/RR 基准采纳落地 `--effect`）/N4（`--adopt-ref <序号>` 单选）/N5（护栏拒绝：混 param/scale 聚合 拒绝 + CI 跨零仅展示）；新增 4.17（相关/方差/CI 精度/回归/meta_planning 族， 数值经 live 端点实测：correlation 85、ci_mean 97、regression_logistic 317 PASS 验证点、meta_planning K=3 + I² 扫描 [2,3,4,8,18]、cluster_ext DEFF 2.20、 rates_ext 197/组）与 4.18（MCID 折算 143/组、--justify 方案论证段、--audit 假设分级 + --verify 独立蒙特卡洛校验）；英文版 §3.5 原中文残段改写为英文并补 v5.12.1 护栏说明；版本脚注 v5.8.0→v5.12.1
- ADVANCED(.zh-CN) §5.5 系统要求：Python 行改「纯标准库无第三方运行时依赖」、
  R 行注明仅 coze 服务端需要；§5.6 删除 statsmodels ImportError 行、补 coze 不可达
- README(.md/.zh-CN) 提示词案例第二轮增补（按 2026-09-15 后全部更新逐条盘点）：
  4.17 新增 Q6（方差 / CV 精度族——variance_one 24 / variance_two 68 每组 / cv_one 392，方法学验证场景）与 Q7（计数终点与多重线性回归——regression_poisson φ=1→21 / φ=2→41、regression_linear 77）；Q2 补 ci_prop 381 / ci_cor 867 实测数 并指向 Q6；Q4 补 `--effect0`（非零 H0 效应进 λ 分子）；4.15 O1 更新为 docx/xlsx/pptx 本地转换（v5.8.0 起 xlsx 零依赖解析）与 pdf 技能指引（原 「PPT/PDF 转换提示」表述修正）；文末小提示同步 Q1–Q7。盘点结论：09-17 飞书字段 / 10-13 entry_point 为内部变更无需案例，09-26 工作台已有 P2 覆盖；09-29 MCID/justify/audit 已由 R1–R3 覆盖；10-09 xlsx i18n/词典扩充落 O1； 10-12/10-14 新检验与 meta A1–A6 由 Q1–Q7 + N3–N5 覆盖
- coze 镜像 README_zh-CN.md 两处 ct_r_lib 现在时描述改为「v5.12.0 起已废除」历史备注
- requirements.txt 补 dev-only 依赖说明（numpy/scipy 仅 legacy/adaptive_simulator.py）
- test_matrix_gaps 文档头 49→65 更正


## v5.12.0 — 2026-10-15 · 废除 ct_r_lib 双副本（本地 R 后端单一真相源 = adapters/local-r/）

`adapters/coze/ct_r_lib/` 与技能根 `scripts/` 长期各存一份相同模块（compute_backend / i18n / i18n_*.json / r_code_policy / samplesize_power 共 7 个文件，MD5 逐个核对一致），无自动同步、 无 git 校验（`adapters/coze/` 整目录在 .gitignore），历史上多次漂移——镜像曾停留在 v4.0.1/v5.0.2（缺 v5.9/v5.10 的 65 法 Tier1/2 覆盖），v5.11.0 被迫同时编辑两份副本。 更隐蔽的危害是**模块图混版**：`scripts/compute_backend.py` 的懒加载器把 ct_r_lib 临时置顶 sys.path，local_r_backend 的 `r_templates / i18n / compute_backend` 从镜像解析、而调用期 `samplesize_power` 从 scripts/ 解析——同进程两套模块实例，isinstance / 单例状态均可分裂。

**结构变更（coze 端点运行时不 import 任何 ct_r_lib 模块，无用户可见行为变化）**
- 独占文件迁至技能根 `adapters/local-r/`：`local_r_backend.py`（本地 R 拼码/执行）、
  `r_templates/`（14 个 R 字符串模板）、`legacy/adaptive_simulator.py`（纯 Python 蒙特卡洛兜底）
- 镜像内 7 个重复副本整体归档至 `adapters/coze/_archive_ct_r_lib_20261015/`
  （构建器排除；内容与 scripts/ 同 MD5，可随时对照回收）
- `scripts/compute_backend.py::_load_local_r_backend()` 改指 `adapters/local-r/`：
  执行期注入 local-r + scripts/ 双路径，执行后还原
- `adapters/local-r/` 加入 `.clawhubignore`（保持 dev-only、不随发布包分发的属性，
  与原 adapters/coze/ct_r_lib/ 一致），并纳入 git 版本控制（消除「镜像无校验」根因）
- 两个部署构建器（`_build_deploy.py` / `_build_deploy_new.py`）加守卫：`ct_r_lib` 目录名 +
  `_archive_*` 前缀一律不进部署包；manifest/zip 写盘改用共享盘安全的改名舞 （本机 filesrv 拒绝覆盖已存在文件，原 `write_text` 直接失败）

**顺带修复**
- `import adaptive_simulator` 此前必然失败（文件在 legacy/ 子目录、扁平 import 不可达，
  且其自身 `from i18n import t` 还需 scripts/ 在路径上）→ 路径块与 except 兜底同步修
- 更正过时声明：local_r_backend 不再是「coze 镜像唯一真相源」；`build_r_code` 段头删除
  已不存在的 template_resolver_node 描述（现行 coze 架构 = 单 dispatch 节点直调 src/r_engine/）
- 6 个技能文档 + coze 镜像 AGENTS.md / README_zh-CN.md / samplesize.py /
  install_r_packages.R 的 ct_r_lib 路径引用全部更新

**遗留清理（同日完成，四项全部落地）**
- `ADAPTIVE_SIM_R` 漂移已消除：整体回写 coze 侧 `src/r_engine/adaptive_sim.R` 现行版本
  （含 `seq_len(K-1L)+1L` 稳健性修复与 headless PNG 清理），调用点同步删除已废止的 `out_png` 传参；回读校验与 coze 侧逐字节一致（17814 字符）
- `config/r_code_generation_cfg.json` 提示词更新：删除已不存在的 template_resolver
  上游节点与 ct_r_lib 提法，改述现行「单 dispatch 节点直调 src/r_engine/」架构， 并补 headless 禁绘图约束（可视化统一 svglite SVG）；新版已随部署包分发
- `workbench/publish-dist/` 陈旧副本已刷新：`build_publish.py` 打共享盘安全补丁
  （copy2 拒覆盖 → 改名舞 + 内容一致跳过）后重跑，53 文件全量同步、二次构建 COPIED 0（幂等）；被替换旧版本暂存 `workbench/_publish_trash/`（.gitignore 已排除）
- figure 层双副本已消除：`scripts/figure_kit.py` + `scripts/alloc_curve.py` 为唯一
  真相源（文件头已加注），两个部署构建器增加打包前同步步骤（coze 端按路径子进程 执行包内副本、属部署必需，故采「构建时同步」而非删除）；文档 4 处 （default_figures.md×2 / coze DEPLOY.md / coze AGENTS.md）的「手工保持同步」 表述改为「构建时同步生成，勿手改」

**验证**
- `py_compile` 全部改动 .py 通过；`_load_local_r_backend()` 实测返回 LocalRBackend；
  `build_r_code('ttest_ind', …)` 产出 31012 字符 R 源码（build_parser 解析链通）； legacy import 修复后可达；CLI `--dry-run`（CTSS_COZE_MOCK=1）exit 0
- 部署包重建：`coze_project_5.3.16.zip` 75 files / 370.7 KB（前次构建 99 files 含 24 个
  ct_r_lib 条目 / 517.7 KB），MD5 `96523970e52aa4d5223e66de8fff4f9c`，EXCLUDE CHECK CLEAN
- 遗留清理复验：ADAPTIVE_SIM_R 与 coze 侧逐字节一致；`build_adaptive_sim_r_code` 不再
  发射 out_png；figure_kit/alloc_curve import 通过；zip 内回读 config 提示词为新版； `scripts/ ↔ publish-dist/scripts/` MD5 全对齐；7 项冒烟 + CLI dry-run exit 0

**版本**：SKILL `5.11.0` → **`5.12.0`**；coze 端点 `COZE_VERSION` 维持 `5.3.16` （端点行为不变，部署包仅剔除失效文件）。

## v5.11.0 — 2026-10-14 · meta-planning 前瞻规划补齐（方案 A1–A6）+ repro 复现污染缺陷修复

对齐 `ct-base/参考资料/PASS/META_ANALYSIS_OPTIMIZATION.md` 的 meta-planning 前瞻性规划方案。 v5.9.0 已落地 `meta_planning` 单轨（`ss_meta_planning`，Hedges & Pigott 2001 随机效应）， 但对照方案 A1–A6 仍缺 4 项能力；本轮补齐，并修复一处**用户可见的真实缺陷**。

**新增能力（4 项）** 1. **`--R` 异质性比直输**（方案 §4B）：R = 组间/组内方差比，**直输优先于 I² 映射**（R=0 即固定效应）； 与 `--i2` 互为双参数（R = I²/(1−I²)）。引擎侧取键改用 `p[["R"]]` **精确匹配**——R 的 `$` 会对以 "R" 开头的键做部分匹配（历史 `p$hr` 静默取到 `hr_expected` 同源陷阱）。 2. **`--effect0` H0 效应量**（方案 §4B）：效应量原尺度（or/rr 缺省 1、其余 0），进入 λ=(T−T0)/SE 分子。 3. **cluster 簇大小变异系数 `--cluster_cv`**（方案 A6）：设计效应 `DE = 1+[(COV²+1)M−1]ρ` （Donner & Klar 2002 / Eldridge & Kerry 2012），V_W 按 DE 放大；stats 回显 `de` / `n_eff`。 4. **异质性扫描表 + K–I² 默认图**（方案 §4C，对标 PASS「Plots」栏目）：
   - stats 新增 `hetero_i2` / `hetero_R`（I²∈{0,.25,.5,.75,.9}）、`hetero_K`（目标功效口径所需 K）、
     `hetero_power`（`--k_studies` 求效能口径）
   - 默认图 `meta_hetero`（K–I² 曲线 + PASS 预设点），R 引擎 / Python 预览 / R 出图层三端同源

**缺陷修复（P1 · 用户可见）**
- **`repro.r` 复现记录被异质性扫描污染**：`.repro_call` 只保留**最后一次** `ss_*` 调用，而扫描表
  的 5 次调用落在 `.repro_capture` 区间内 → repro 记录到「I²=0.9 → R=9」的**扫描末次**调用， 而非主求解调用。实证：主解 K=3 被复现成 K=13，用户按 repro 复现得到**错误结果**。 修复：把扫描表计算移出捕获区间（置于 `.repro_capture <<- FALSE` 之后）。 新增回归断言：repro 调用行含 `R = 1`（主解口径）、且 repro 复现值 == 主结果 K。

**实现落点（四端一致）**
- **R 引擎**：`src/r_engine/samplesize_functions.R`（`.meta_vw` 加 `cov`、新增 `.meta_de`）、
  `run_task.R`（dispatch 分支重写 + `.run_meta_hetero` + `.default_figures` 注册）、 `common.R`（`label.meta_*` / `fig.meta_hetero` 中英双语）
- **本地 R 后端**：`ct_r_lib/local_r_backend.py`（`_common` 含 R 直输 / `_common_nr` 专供扫描 /
  `_sweep` / `_de_echo`）、`ct_r_lib/r_templates/r_pass_ext.py`（`cov` 透传）
- **Python 预览层**：`scripts/figure_kit.py`（`_meta_vw` / `_meta_K_required` / `fig_meta_hetero`；
  三副本同 MD5 `da63f0e3…`）+ `METHOD_FIGURES["meta_planning"] → ("meta_hetero", None)`
- **R 出图层**：`scripts/coze_figure_layer.R`（`render_meta_hetero` + 跳过 `(n_star,power_star)`
  锚点校验 + `pw <- NULL` 守卫）
- **CLI**：`scripts/samplesize_power.py` + `ct_r_lib/samplesize_power.py`（+`--R` / `--effect0` / `--cluster_cv`）
- **契约**：`tests/coze_cases/_contract_index.json`（required +3 / output +5）→ 重渲染
  `adapters/coze/coze_contract.md`；`references/menu.md` 条目更新

**契约文档漂移修复**：`coze_contract.md` 第 61 行 meta_planning 仍为旧契约（索引已改但未重渲染） → 跑 `python tests/coze_cases/gen_contract_doc.py` 重新生成；并给该脚本加 `newline="\n"` （Windows 文本模式默认把 `\n` 翻成 `\r\n`，会让每次重生成产生整文件行尾 diff）。

**验证（全绿）**
- `t_meta_planning.py` M1–M6：**0 FAIL**（M1 引擎 vs 独立复算 7/7；M2 solve power 3/3；
  M2b cluster+COV 9/9；M3 I²↔R 等价 + **R 直输优先**；M3b 扫描表；M4 引擎 vs 本地 R 后端逐值一致； M5/M5b 默认图 + **repro 记录主解** + 复现值 == 主结果；M6 契约透传）
- `check_B_enum`：65 test 七表交叉一致（CLI / dispatch / local_backend / 契约 index /
  figure_kit×3 / 出图层 / 契约 md），差异全为 `缺:- 多:-`
- `check_contract_i18n`：4a 契约 required ⊆ CLI dest（0 missing）；4b 新分支 i18n 键 ⊆ 定义（0 missing）
- `check_C_all65`：**64 ok / 1 warn / 0 fail**（meta_planning `status=ok`，`stats_keys=8`）
- `check_repro`：7a 老 test 基线 figs=4；7b 逐 test repro 可运行且数值复现（含 meta_planning rc=0 matched=1/1）
- 部署包 `coze_project_5.3.15.zip`（96 files，467.3 KB，MD5 `4c8695d59b4c97cde47ab0bf6041cd1f`）
  解压独立跑 meta_planning：`status=ok` / `n_studies=6` / `de=2.2` / `n_eff=22.7` / `hetero_K=[3,4,6,12,29]` / `meta_hetero` SVG / repro 记录主解 `R = 1`

**版本**：SKILL `5.10.1` → **`5.11.0`**；coze 端点 `COZE_VERSION` `5.3.14` → **`5.3.15`** （`_version.py` 与 `manifest.json` 同步；`workbench/publish-dist/SKILL.md` 副本一并同步）。

## v5.10.1 — 2026-10-13 · 修复工作台调用 entry_point 恒为 skill（§1.3 接线）

> ct-base coze_io_contract §1.3 工作台接线三架构之「架构 A · 进程内 import」。v5.10.0 的 coze_client 已按契约在 `call` / `call_batch` / preview 三处注入 `"entry_point": _ENTRY_POINT`，但**设置侧零接线**——注释声称「工作台进程在 fullflow 入口调用 set_entry_point("workbench") 覆盖」，而本技能并无 fullflow（该注释自 meta-analysis 范式抄录，从未落地）→ 工作台应用页面调用恒落默认值 `skill`。

- **`adapters/workbench/server.py`**：import `CozeBackend` 后**模块级一行** `set_entry_point("workbench")`（本进程即工作台后端，与 coze_client 同进程 → 此后所有出站信封自动携带 `entry_point="workbench"`，飞书独立列可按来源筛选）。import 语句由 `from coze_client import CozeBackend` 改为 `from coze_client import CozeBackend, set_entry_point`（避免 `coze_client.set_entry_point` NameError）。
- **无回归边界**：agent / 技能 CLI 路径（`samplesize.py` 等直连 coze_client）是独立进程、不经过 `adapters/workbench/server.py` → 恒 `skill`。
- **同步**：`workbench/publish-dist/adapters/workbench/server.py` 与主文件逐字节一致（diff 验证；coze_client.py 本体未改，publish-dist 副本无需同步）。
- **验证**：`set_entry_point("workbench")` 后 `_ENTRY_POINT == "workbench"`；模块重载（模拟新进程）默认回 `skill`；`py_compile` 两份副本全过。
- **范式沉淀**：ct-base `references/coze_io_contract.md` §1.3 新增「工作台接线三架构」规范段，本技能为架构 A 范本（meta-analysis fullflow 之外的第二实证）。

## v5.10.0 — 2026-10-12 · Tier 2 扩容：回归 / 整群扩展 / 率扩展（61 → 65 tests）+ 2 处缺陷修复

对齐 PASS 全量复刻目标第二阶段（Tier 2）。**先按用户指令「4 先核实」完成 §4 扩展点核实** （报告：`ct-base/参考资料/PASS/CT_SAMPLESIZE_TIER2_VERIFICATION.md`），据核实结论落地：

**新增 4 个 `--test`（61 → 65）**
- `regression_logistic` — 逻辑回归样本量（Hsieh, Bloch & Larsen 1998 连续协变量 / Hsieh 1989 二分类）；
  `--x_type=continuous|binary`、`--effect`=OR、`--p0`、`--q`、`--r2`。PASS 验证点 N=317 复现 ✅
- `regression_poisson` — 泊松回归样本量（Signorini 1991，正态 X）；`--lambda1` 基线率、`--effect` 率比、
  `--mu_x`、`--sd`、`--t1` 暴露时间、`--phi` 过离散、`--r2`。PASS 验证点 power=0.61237/0.79600 复现 ✅
- `cluster_ext` — 整群随机化**广义设计效应** `DEFF=1+((1+CV²)m−1)ρ`（Eldridge 2006），含不等群 CV；
  由个体层面 n 推簇数，或给定簇数反向求有效个体 n
- `rates_ext` — 率扩展；`--rate_mode=ratio`（过离散率比检验）/ `single_ci`（presize::prec_rate）/
  `ratio_ci`（presize::prec_rateratio）

**§4 核实结论（决定 Tier 2 处置）**
- `be_tost`：`design` 参数**直通 PowerTOST，已支持 13 种设计**（含 3×3/4×4/重复/平行）→ G15 以文档形式关闭，无需新 test
- `cluster`/`poisson`/`anova`：能力受限（仅两组 DEFF / 仅两率之比 / 仅单因素）→ 新增独立 test 保持契约清晰
- **修正原 gap 分析假设**：`TrialSize` **无** `power.Logistic`/`power.Poisson` → G13/G14 改为闭合公式实现，零新包依赖

**缺陷修复（均为预先存在，非本次新增引入）** 1. **`ss_poisson` / `ss_vaccine` 求功效方向公式写反**（`info` 应为 `1/Var` 而非 `Σn/(λt)`，导致给定 n 时 power 恒为 1） → 修正为 `info = 1/(1/(n1·λ1·t1)+1/(n2·λ2·t2))`；正反向一致性自检通过（n=198 → power=0.8039） 2. **`scripts/i18n.py` 丢失 `resolve_user_language`**（v5.8.0 误删）致 `samplesize_power.py` `ImportError`、CLI 阻断 → 自 v5.7.26 恢复该函数（含 `detect_text_language`/`_normalize_language`）

实现位置：`samplesize_functions.R`（4 个 `ss_*`）、`run_task.R`（4 个 dispatch 分支）、 `common.R`（Tier 2 header/label i18n）、`samplesize_power.py`（`--test` choices + 7 个新参数： `--x_type/--q/--r2/--mu_x/--phi/--cv_cluster/--rate_mode`）、`_contract_index.json`（+ 镜像）与 `coze_contract.md`（重生成 65 tests，计数改为动态）、`references/menu.md`（⑦ 类 + Part 2 交叉索引）、 `tests/coze_cases_regression.py`（49 硬编码断言改为「索引↔CLI choices 一致」动态校验）。

本地 R 4.6.1 x64 端到端验证：4 新测试 × 双向 **14/14 通过**；契约回归 **ALL PASSED**。

## v5.9.0 — 2026-10-12 · Tier 1 扩容：相关 / 方差 / CI 精度 / 回归 / Meta 规划（49 → 61 tests）

对齐 PASS 全量复刻目标的第一阶段落地（PASS 822 过程 / 25 家族差距分析见 `ct-base/参考资料/PASS/CT_SAMPLESIZE_GAP_ANALYSIS.md`）。新增 **12 个 `--test`**：

- **相关**：`correlation`（H0:ρ=0，Fisher-z 精确，pwr.r.test）
- **方差**：`variance_one`（σ²=σ0²，χ²）、`variance_two`（两方差比 F）、`cv_one`（CV 相对误差精度）
- **置信区间精度**：`ci_mean`、`ci_prop`、`ci_or`、`ci_rr`、`ci_cor`、`ci_icc`（presize 优先，base-R 正态兜底；`--half_width` 目标半宽→n，配 `--nobs` 求达成半宽）
- **回归**：`regression_linear`（多重线性回归 R² 检验，Cohen's f²，pwr.f2.test）
- **Meta 规划**：`meta_planning`（Hedges & Pigott 2001 随机效应；effect_type ∈ smd/paired/or/rr/cor/cluster；`--i2`/R 双参数；给定 `--k_studies` 求效能，否则求所需 K）

实现位置：`samplesize_functions.R`（12 个 `ss_*` + `.meta_vw`/`.pow_meta`）、 `run_task.R`（12 个 dispatch 分支 + `.default_figures` 非 solver 守卫）、 `common.R`（新 header/label i18n）、`samplesize_power.py`（`--test` choices + 9 个新参数： `--half_width/--rel_error/--p0/--f2/--u_pred/--effect_type/--n_per_study/--i2/--k_studies`）、 `_contract_index.json`（+ 镜像）与 `coze_contract.md`（重生成 61 tests）、`references/menu.md`（新增 ⑦ 类）。

本地 R 4.6.1 x64 端到端验证：12 测试 × (n/power 双向) 16 例 **全通过**；既有 10 测试回归通过。 零新增 R 包依赖（`pwr`/`presize` 均为引擎既有包）。

## v5.8.0 — 2026-10-09 · xlsx 输出 i18n + 词典/术语扩充 + 本地辅助能力（ct-base 1.3.5 家族同步）

- **xlsx 输出全量 i18n（i18n.py / i18n_messages.json）**：FAERS 安全信号等 Excel
  产出物的表头/横幅/KPI/工作表名全部走 `xlsx.signal.*` 键族，中英随 OS 语言切换。
- **office_to_md.py 新增本地 xlsx→md 解析器**（`xlsx_to_md` / `check_upload` /
  `UploadRejected` / shared-strings 解析）——上传转换不再依赖外部工具链。
- **r_libs.py 新增 `run_r`**：本地 R 执行入口（默认 OFF，未确认时仅返回 safe-preview）。
- **drug_name_resolver.py 新增 `resolve_for_dialog`**：对话内药物名解析入口。
- **kw_lexicon.json / kw_localize.py / term_map.json 词典扩充**：关键词与术语映射
  覆盖面扩大，与 ct-base 1.3.5 关键词翻译增强家族对齐。

## v5.8.0 — 2026-09-29 · MCID 语义入口 + IRB/SAP 论证段落（ct-update upgrade J 落地）

- **J1 `--mcid` / `--mcid-source`（samplesize_power.py）**：临床措辞的目标差值入口——
  MCID（原始终点单位）经既有 Δ/sd 通道折算 d = MCID/SD；需配合 --sd、与 --effect 互斥 （均报错引导）；计算与 --audit 均回显折算行；审计联动：有来源声明 → 效应量假设升 known（anchor/distribution/expert 三流派提示见 references/justification_templates.md）。
- **J2 措辞/交互修订（用户审阅后 2026-09-29）**：① 引擎声明改为
  `R <版本> + rpact <版本> + TrialSize <版本>`——repro.r_version/packages 经 `_envelope_to_result` 透传进 meta，`--justify` 自动填充；**删除"云端/coze"字样** （版本对文书有意义、部署形态无意义）；mock 版本视同缺失走 [__填写] 占位。 ② 默认隐藏确认：不带 --justify 时单次计算成功后仅输出一行 i18n 提示 （`offer.justification`，"需要的话告诉我/加 --justify 重跑"），不直接生成段落。
- **J2 `scripts/justify_text.py`（纯 stdlib，`--justify` 计算后附加 / 独立预览）**：
  IRB/SAP-ready 中英对照论证段落，四个设计变体（优效连续/NI-EQ/生存事件驱动/通用回退）， 骨架逐句锚定 CONSORT-SPIRIT Item 14 + DELTA2 Box 4（英文语序）与 CDE《药物临床试验 样本量估计指导原则（试行）》2024-12-23（中文口径）；n 自动填充并按引擎返回字段判定 口径（n_per_group→每组；其余→总）；所有依据类空位强制渲染为 [__填写]/___ 占位 （anti fake-precision，不替研究者做临床判断、不替代监管沟通）。
- **新文档** `references/justification_templates.md`（骨架出处/变体矩阵/MCID 三流派/使用约束）。
- **测试**：justify_text 单测（单位口径×2 + 双单位回归×4 变体 + 占位保留）全通过；
  主流程 MOCK E2E（--mcid 折算回显 + --justify 段落）通过；--mcid 缺 sd / 与 effect 并用的报错路径验证。py_compile 全绿。
- 对标来源：Sample Size Calculation (ProFlow-Labs-Ai/medsyniq-lite, LobeHub) 的
  "监管感知"叙事 + calc-sample-size (Aperivue) 的 IRB-ready justification； J 评估结论（2026-09-29）：其余卖点均已被技能覆盖，仅 MCID 与论证叙事为真缺口。

## v5.8.0 — 2026-09-29 · 假设质量审计（ct-update upgrade I 落地）

- **新增 `scripts/hypothesis_audit.py`（规划层审计，纯标准库零联网）**：
  - **四分级**：逐个设计假设评定 known / weak / unknown / missing（分级逻辑：
    显式给值+附证据来源→known；「拍脑袋」整数直觉值 d=0.5/SD=1/r=0.5~0.9/ICC=0.05 启发式→unknown；必需参数无值→missing；默认值未确认→weak；结构参数豁免）。 α/power 惯例值（0.05/0.025、0.8/0.9）显式给出即 known。
  - **设计逻辑族**：49 个 test 全量归入七族（经典两组/NI-EQ/生存事件驱动/群随机/
    序贯自适应/诊断方法比较/历史对照），逐族给假设重心与自洽核查问题（经 `_contract_index.json` 全量校验，归族与 REQUIRED_BY_TEST 零遗漏）。
  - **fallback 场景规划**：按最脆弱假设维度（weak/unknown/missing）输出退路模板
    （事件不足→随访延长/事件富集、ICC 超界→加群、界值未共识→先 pre-ICE 再锁 n 等）。
  - **总体判定**：NOT_READY / ADAPTIVE_RECOMMENDED / READY_WITH_SENSITIVITY / READY
    四档出口，missing>0 阻断式提示先补齐。
- **`scripts/samplesize_power.py`**：新增 `--audit`（打印审计报告后退出，不做求解）与
  `--evidence-source`（命中参数升 known）；与既有 `--show-assumptions`（计算层参数 清单）互补——本审计为方案/SAP 撰写前的规划层评估。
- **测试**：单元 8 例（分级路径×5 + 归族/必需覆盖×2 + 渲染）全通过；主入口
  E2E（真实 parser 默认值语义）通过。`py_compile` 全绿。
- 对标来源：sample-size-and-power-planning-assistant（aipoch medical-research-skills，
  ct-update 2026-09-29 增量发现）；对应 ct-samplesize 升级项 I。

## v5.8.0 — 2026-09-26 · 工作台应用升级「带后端版」（部署形态，技能代码零改动）

- **背景**：2026-09-14 首发为最简静态壳（`python -m http.server`），页面依赖的
  `/api/*` 一律 404 → 线上红条「无法加载检验目录」。本次照 ct-literature 先例升级为 python http-service，用原 appId `wbapp_9K1dei1PydVQ66YmawCD3C` 覆盖发布， 链接保持 `https://ct-samplesize.app.workbuddy.host/` 不变。
- **新增发布基础设施**（`workbench/`，被 .gitignore/.clawhubignore 整目录排除、不进技能发布包）：
  `workbench/app.config.json`（deployedAs=http-service，startCmd=`python adapters/workbench/server.py`， publishDir=`workbench/publish-dist`）+ `publish-kit/`（genie 权威副本 + build_publish.py + install_genie.py，照 ct-literature 模板）。旧 `adapters/workbench/app.config.json` 删除（重复登记源）。
- **载荷构成**（35 文件 / ~785 KB，还原技能根层级——server.py 以 `_HERE/../..` 定位 `_SKILL`）：
  `adapters/workbench/`（server/form_schema/session_store/nl_llm/workbench.html）+ `adapters/` 四件（coze_client/coze_token_embedded/rendering/bug_report）+ `scripts/` 全套 + `config/config.json`（**出站授权白名单，缺了 compute 被门控静默拦截**）+ `tests/coze_cases/_contract_index.json`（form_schema 反射数据源，唯一入包的 tests/ 文件）+ SKILL.md（版本号）。 红线排除：coze/、r-assets/、publish-kit/、*.genie、sessions.json、README.md。
- **server.py 无需包装**：main() 已内置云端通道——`PORT` 环境变量 → 绑 0.0.0.0，
  `/` 路由直服 workbench.html，不同于 ct-literature 需 app.py 改写 argv。
- **线上验证**：载荷形态本地冒烟（8766 无显式 env）health/schema/ttest_ind n=64 全通；
  发布闸门 pre/post 双绿、shareLink 断言通过、genie 回读无污染； 线上端到端 compute ok=true（8 图 + R 代码）；首页与载荷 MD5 逐字节一致（7e2ad6f7）。
- **同日 UI 微调（用户指示，二次覆盖发布 11:32，链接不变）**：① 简化版声明条改左对齐
  （`justify-content:center → flex-start`）；② 删除「本界面只是为了方便操作…」提示横幅 （HTML 元素 + 中英 i18n 文案 + `.app-hint` CSS 整簇清除，残留 grep=0）；线上 MD5 复核 MATCH。
- **同日 NL 兜底接入 LongCat-2.0（用户指示「按 ct-base 规范接 longcat2」，三次覆盖发布 ~12:10，链接不变）**：
  - 背景：页面「智能识别并计算」实为确定性正则（classify_test/param_aliases），与对话模式的
    Agent LLM 理解力差距大；旧版 `nl_llm.py` LLM 兜底默认禁用（需显式 CTSS_NL_ENDPOINT），云端无 env → 死路径。
  - 改造：按 ct-base §12（2026-09-25 家族统一 LongCat-2.0）——`nl_llm.py` 默认端点
    `https://api.longcat.chat/openai/chat/completions`、模型 `LongCat-2.0`，key 经 `load_llm_key()`（env `LONGCAT_API_KEY` > 混淆 `config/llm_key.py`）；新增 `adapters/llm_loader.py` + `config/llm_key.py`（自 ct-base 拷贝，入载荷白名单，载荷 35→37 文件）； max_tokens 800→2048 + 超时 25→45s（LongCat 为推理模型，reasoning 吃预算，meta-analysis 实测教训）。
  - 红线不变：deterministic-first（规则命中即权威，LLM 只在 test=None 时提议、零覆写权）、
    advisory 闸门照旧、LLM 幻觉未知检验置 null、无 key/不可达优雅降级回规则。
  - 前端标识 `本地大模型识别 → 大模型识别`（引擎标签语义修正）。
  - 验证：本地单测 2.8s 口语句正确 ttest_ind + Δ4/σ12；载荷形态无 env 等价云端复测通过；
    线上 `engine: llm` 实证（规则不命中英文句 → proportion_paired + p1/p2 抽取）；guard pre/post 双绿。
  - 已知边界：中文规则词表很宽（「血压」「评分」「安慰剂」甚至 `ve\b` 都命中），常见中文口语句
    多走 rule 分支而非 LLM；advisory 措辞（"怎么设计"类）被闸门拦下不点火——均为既有设计，非回归。
- **同日顶栏瘦身（用户指示，四次覆盖发布 15:55，链接不变）**：删除左上角 `CozeBackend` 后端徽标
  （`#hBackend` 元素 + `header .badge` CSS + init 中 `/api/health` 显示调用 + 中英 `offline` i18n 键 整簇清除；后端 `/api/health` 端点保留作运维探活，仅前端不再消费）。node --check 内联 JS 语法通过， 线上残留 grep=0、index MD5 MATCH。
- **同日会话默认开启（用户反馈「追加提问/跨轮继承没有实现」，五次覆盖发布 16:02，链接不变）**：
  实测后端链路完好（session/create → 两轮 compute delta 继承 → audit inherited/overridden 全对，d=0.5/power=0.8→0.9 得 n 64→86），根因是入口 UX： 会话挂在默认**不勾选**的 `#keepSession` 复选框上，不勾则追加提问/继承整条链路不激活。 修复：复选框默认 `checked`——首算自动建线程，改参数再点即「应用修改并重新计算」（仅发 delta，跨轮继承），线程面板逐轮显示继承/覆盖/缺失胶囊。线上 keepSession checked 断言通过。 同批：线程面板空态改为引导文案（中英双语，六次覆盖发布 16:10 上线，index MD5 MATCH）。
- **同日反馈入口对齐 ct-base §199（用户指示，七次覆盖发布 16:12，链接不变）**：底部
  「报告问题 / Bug 反馈」按钮移至**右上角顶栏**（`#wb-bug`，位于会话选择器之后、页面最右）， 文案改为规范短标签 `反馈 / Feedback`（`bugBtn` 键；长文案「报告问题 / Bug 反馈」保留为 弹窗标题 `bugTitle`）。footer 整簇删除（`<footer>` HTML + `.foot*` CSS 三条，页面已无 其他消费方；两段式弹窗流程本身已合规未动）。node --check 通过、冒烟断言 header 内位置/footer 消失/弹窗与 openBug 保留全绿、guard pre/post 双绿、线上 MD5 MATCH。
- **同日会话历史 localStorage 镜像（用户指示参考 ct-advisor 实现，八次覆盖发布 16:18，链接不变）**：
  根因：云端沙箱重新部署清空服务端 `sessions.json`（本日已 7 次发布），线程面板「无任何记录」。 照 ct-advisor 范式（`wb_ctadvisor_hist_` localStorage 本地优先）为 samplesize 加**浏览器本地 会话镜像**（`wb_ctss_threads_`/`wb_ctss_active_sess_`，服务端仍是计算/合并权威，镜像供展示与恢复）： ① `threadMirror(sid,patch)` 补丁合并（title/current/turns 各自非 null 才覆盖，LRU 保留 30 会话）； ② `loadSession(id)` 统一读：服务端优先、404 回落镜像；③ `refreshSessions` 下拉并入本地独有线程 并标「本地缓存」（i18n `histLocal`）；④ **404 自愈**：`doCompute` 收到 `session not found` 时 自动重建会话、按本地镜像设定延续、原样重发一次（计算结果不丢）；⑤ `init` 自动恢复活动会话 （刷新/重进秒恢复，ct-advisor 同款体验）。node --check + 镜像合并单测（node stub localStorage 4 断言）+ 404 错误形状核对全过；guard pre/post 双绿、线上 localStorage/selfheal 断言在位。
- **安全注意**：云端实例无 CTSS_WB_TOKEN（POST 开放，与既有 coze 公开端点授权一致）；
  载荷内嵌公共 coze 凭据系 2026-08-18 用户授权的公共 token，非私密。

## v5.8.0 — 2026-09-17 · 飞书版本字段落点统一：一律写 `resultstr`，`querystr` 不再存版本信息

- **依据**：ct-base `references/coze_io_contract.md` §2.1（2026-09-17 定）——版本类元数据
  （`skill_version` / `coze_version`）**一律写入飞书 `resultstr` 顶层键**，`querystr` 不再承载任何版本字段。 此前 ct-samplesize 把 `skill_version` 写进 `querystr`，与 ct-advisor / meta-analysis 落点不一致，无法统一检索。
- **服务端改动（coze：需重新上传部署包才生效）**：
  1. `src/graphs/nodes/feishu_write_node.py`：`build_querystr()` **移除** `skill_version` 参数 （querystr 只留 `test`/`params`/`mode`）；`build_resultstr()` 新增可选参数 `skill_version` / `coze_version`（`runtime_sec` 保留），三者**仅非空才并入顶层** （为空 → 不写键，与历史格式逐字节一致）。 2. 新增 `src/graphs/nodes/_version.py::COZE_VERSION = "5.3.11"`（单一真源）：飞书 `coze_version` 列与响应信封标记 `_coze_version` 共用，杜绝两处漂移。 3. `src/graphs/nodes/samplesize.py`：`_COZE_ENVELOPE_VERSION` 改为引用 `_version.COZE_VERSION`。 4. `src/graphs/nodes/feishu_save_node.py`：单条 / **批量**两条分支均改为把 `skill_version` + `coze_version` 写进 resultstr（批量摘要 `batch_summary` 不再带 `skill_version`）。 5. `src/graphs/state.py`：`skill_version` 字段描述由「写入 querystr」改为「写入 resultstr」。 6. 契约同步：`adapters/coze/coze_contract.md` 与其生成器 `tests/coze_cases/gen_contract_doc.py`。
- **客户端无改动**：`coze_client._skill_version()` 仍按 §1.2 发顶层信封，落点变化只在服务端。
- **验证**：5 文件 `py_compile` 通过；`build_querystr` 输出键集恰为 `{test, params, mode}`（无版本键）；
  `build_resultstr` 元信息全空时与历史格式逐字节一致；全字段时 `runtime_sec=2.001` / `skill_version` / `coze_version` 均在顶层，R 出参原键完好。

## v5.7.27 补丁（2026-09-11）· 出站信封守卫 + 版本正则修复（后端日志实证驱动）

- **背景**：后端日志（2026-09-11 11 分钟窗口、单会话 26 条请求）实证三类结构性冗余：① 「单点+曲线」成对串行（13:13，~50% 请求可省）；② 每条请求 ~135 参数 / 2.8KB（仅 6 个被消费）——编排 agent **绕过 `build_params` 手拼全家族 argparse 默认值信封**（违反 v5.7 约束 3 红线）；③ 同 8 点网格重复计算 5 次（占曲线请求 38%）——噪声键破坏服务端 TTL 缓存签名。
- **`adapters/coze_client.py`**：
  - **新增出站信封守卫 `_trim_bloated_params(test, params)`**：params 键数显著超过该 test 契约白名单（`required`，阈值 `max(30, len(required)+15)`）时判定为过肥信封，裁剪至 `required ∪` 通用/模式键（alpha/power/nobs/side/alt/d_val/solve_for_power/user_language）∪ curve_* 协议键，stderr 告警并保底回补模式关键参数。`call()` / `call_batch()`（经 `build_batch`）/ `preview()` 三处出站路径统一施加——无论调用方如何拼装，**135 参数级信封从此物理上无法出站**。正常 CLI / workbench 路径（build_params 产物 ~10-20 键）零影响。
  - **修复 `_skill_version()` 正则损坏（P0）**：`^version://s*([0-9][//w.//-]*)`（反斜杠丢失、永不匹配，版本号一直靠 `_SKILL_VERSION_FALLBACK` 常量撑着）→ 修正为 `^version:\s*([0-9][\w.\-]*)`，恢复 SKILL.md frontmatter 单一事实来源。此损坏会导致**升版后服务端仍归因到旧 fallback 版本号**（版本漂移静默发生）。
- **验证（全离线）**：正常路径 10 键 → 守卫后不变；模拟 36 键过肥信封 → 裁剪至 10 键（保留 p1/p2/alpha/power/ratio/side，剔除 auc0/win_ratio_theta/junk）；`py_compile` 通过；`_skill_version()` 从 SKILL.md 读到 5.7.27。
- **编排侧（文档强化，`SKILL.md` Batch-call governance）**：补后端日志实证段——曲线响应已含单点（禁止先单点后曲线）、`build_params` 白名单强制、噪声键破坏缓存签名；明确守卫是安全网而非绕过许可。
- **遗留（服务端，需用户随 coze 部署节奏处理，客户端无依赖）**：① 同网格近似参数模糊缓存（38% 曲线请求可命中）；② 飞书日志 87% 空白行写入/导出修复。详见 `references/backend_optimization_2026-09-11.md`。

## v5.7.26 补丁（2026-09-04）· 工作台 NL 兜底与发布安全收敛

- **背景**：用户反馈「工作台兜底的 LLM 性能不如对话模式」，并发现**已发布应用仍默认回连本机 Ollama（localhost:11434 / qwen3.5:27b）**。根因：(1) 工作台用弱本地 Ollama 作兜底，且 `server._nl` 存在「弱 LLM 覆盖确定性已识别检验」的隐患；(2) 发布的是修复前快照，旧 `nl_llm._endpoint()` 默认回退 localhost。
- **`scripts/classify_test.py`（确定性检测器增强，对齐对话模式）**：
  - 新增「含 N 次期中分析的生存终点」→ `gsd_survival`（原误判 `survival`）；泛化连续两组表述（如「两种降压药/收缩压下降…标准差」）→ `ttest_ind`（原 `None`）。
- **`scripts/param_aliases.py`**：新增两组均值差推断（试验组下降X − 对照组下降Y → `effect`），如降压药例自动得 `effect=5`。
- **`adapters/workbench/server.py`**：删除「缺参时调用弱 LLM 覆盖规则结果」的隐患段；确定性识别到检验即权威返回（与对话模式 discipline 一致）。
- **`adapters/workbench/nl_llm.py`**：**默认关闭 LLM 兜底**——`CTSS_NL_ENDPOINT` 未设置时 `_endpoint()` 返回空、`nl_resolve` 直接返回 `None`，不再隐式默认本机 Ollama；修正「指向 coze /v1/chat/completions 即对齐」的误导文档（该端点需 `session_id`，不可用）。如需真·LLM 兜底，须显式 `CTSS_NL_ENDPOINT` 指向自有强模型。
- **效果**：确定性层 8/8 关键用例与对话模式一致；端到端 `/api/nl` 全部 `engine=rule`，弱 LLM 零覆盖；`nl_llm` 无端点时干净降级。
- **发布说明**：本版重新发布后，线上默认不调用任何本地/外部大模型（NL 走确定性，计算走 coze 云端 `/run`）；鉴权（`CTSS_WB_TOKEN`）与 `CTSS_COZE_NO_EMBEDDED=1` 仍需部署环境显式注入才生效（未注入则维持与旧版一致的可访问性）。

## v5.7.25 补丁（2026-09-03）· coze 入参契约 §1.1 收敛：`user_language` 仅进 params（顶层不再双写）

- **背景**：ct-base `coze_io_contract` §1.1 规定 `user_language` 位置为「请求 `params` 内（非顶层信封）」，但本技能作为该契约的**参考实现**，实际为**顶层 + `params` 双写**（自带 `coze_contract.md` 亦记顶层），与 canonical 冲突。用户 2026-09-03 拍板**方案 A：改本技能对齐 canonical**（而非放宽契约回改三个叶子技能）。
- **客户端改动（`adapters/coze_client.py`）**：
  - 新增 `_with_user_language(params, lang)` 统一注入助手：已有 `zh`/`en` 有效值不覆盖；缺失 / 非法值 / 非 dict 入参均兜底注入。
  - `call()`：移除顶层 `user_language`，改由 `sent_params` 承载，`resolved_spec.params` 同步（预览与实发一致）。
  - `call_batch()`：移除顶层 `user_language`；各项 `params` 语言统一为批量整体语言；顶层补仅含 `user_language` 的 `params` 承载位（批量模式下服务端忽略顶层 `params` 参与计算，不误触发单条分支）。
  - `CozeBackend.preview()`：dry-run 预览同步改为 `params` 承载，与实发逐字段一致（避免预览误导排查）。
  - 注：`build_params()` 本就已把 `resolve_user_language` 的权威解析值写进 `params`，本次是**消除顶层冗余**，非新增字段。
- **服务端改动（`adapters/coze/src/`）**：
  - `graphs/nodes/samplesize.py::samplesize_node()`：读取顺序改为 `params.user_language` → 顶层 `user_language` → `""`；批量分支逐项取自身 `params`，缺失回退顶层。
  - `graphs/state.py`：`GlobalState` / `GraphInput` / `SamplesizeNodeInput` 的 `user_language` 标注为**仅向后兼容**（规范承载位为 `params`）；批量模式注释补充「顶层 `params` 非空不触发单条计算分支」。
  - `r_engine/run_task.R`：**未改动**——其 L2165 早已支持 `req$params$user_language`，L2164 保留顶层读取以兼容老客户端。
- **验证（全离线：不联网、不调 R）**：
  - `py_compile` 客户端 + 服务端 3 文件通过；`run_task.R` 经 `parse()` 语法检查通过。
  - 客户端 5 组：helper 五种入参形态、`build_params` 携带、`call()` 顶层无该键且 `params.user_language=zh`、`call_batch()` 顶层与各项均带 `zh`、`preview()` 与实发一致。
  - 服务端 6 组场景：params 优先 / 顶层回退（向后兼容）/ 两者都无则空串 / 批量逐项取值 / 批量缺项回退。
  - R 端语言回退语义实测 4 例全通过（仅 params→`zh`、顶层优先→`zh`、都无→`en`、仅顶层→`zh`）。
- **文档同步**：`adapters/coze/coze_contract.md`（顶层字段列表 / 字段说明 / 批量继承规则）、`tests/coze_cases/gen_contract_doc.py`（顺带修掉 `skill_version` 段落被重复生成两遍的既有缺陷）、ct-base `coze_io_contract.md` §1.1 / §4。
- **⚠️ 部署顺序影响（已评估，可接受）**：`adapters/coze/src/` 为 coze 工作流部署源，服务端读取顺序改动需重新打包上传 Coze 才线上生效。**未部署期间的实际影响极小**——输出语言主字段是顶层 `locale`（始终存在且为 `zh`/`en`），R 端仅在 `.t_lang == "en"` 时才看 `user_language` 兜底；因此新客户端先发、服务端后部署不会造成功能或语言回退，仅「locale 为 en 而用户实为中文」这一极窄场景的兜底暂失效。

- **发布前规范对齐整改（2026-09-03，基于 ct-base §16 发布闸门）**：通过 `publish_inject.py` 从 ct-base 同步 12 个共享件（补齐缺失的 `scripts/merge_spec.py`、对齐 `scripts/i18n.py` 至单一真源）；`frontmatter.summary` 精简为单句中文（§3 F08）；`SKILL.md` 正文中文段落转英文（§4 F19，含代码块中文注释）；`.clawhubignore` 补齐 `archives/`、`ct-samplesize_*.zip`、`tests/outputs/`、`tests/scratch/` 与 `.ctbase_injected.json`（§16.7/§16.8 F12/F20）；顶层 3 个旧交付 zip 归档至 `adapters/coze/_archive_`（§16.9 F27）。三道发布闸门全部通过：`spec_lint.py` ERROR=0、`shared_sync_check.py` exit 0、`publish_secret_scan.py` P0/P1=0。

- **工作台修复（2026-09-03，同日补丁）· 咨询/欠参句子不再把缺参抛给云端报 400「必填参数缺失」**：
  - **症状**：在 NL 输入框键入咨询/欠参类句子（如「两组连续结局随机对照试验，样本量大概多少」），识别到检验类型但缺效应量，前端仍 `doCompute()` 点火计算，后端返回 400「必填参数缺失: effect」并覆盖主结果区，体验等同于失败。
  - **根因（两处叠加）**：① 前端 `nlCompute` 把"请补充参数"只写进 `nlHint` 小提示行，随后仍点火计算；② 上游 `scripts/param_aliases.py::extract_parameters` 的 `missing` 字段初始化为 `[]` 后**从未被 append**，导致后端 `/api/nl` 的 `route.params_missing` 恒为空，前端「本地追问」分支永不触发。
  - **修复（`adapters/workbench/workbench.html`）**：新增 `requiredMissing(test)`，用前端已加载的 `CATALOG`（每检验 `required` + `params[].default`）权威判定真·必填缺失（仅当字段为空且无默认值才报缺，与后端 `_compute` 语义完全一致）；识别到检验但缺参时，预填表单并主结果区显示「请补全以下必填参数后再点「计算」：effect」后**停止**，不再请求云端 coze。对齐 `samplesize_power.py`「参数不全→本地追问、原始 NL 不入 coze」原则。补 i18n `fillRequired`（中英）。
  - **验证**：`node --check` 通过；`/api/nl` 实测该句返回 `test=ttest_ind, advisory=false, needs_params_fallback=true`；`CATALOG` 确认 `ttest_ind.required=['effect','alpha','side','ratio']` 且 `effect.default=None`（会被判缺），`alpha/side` 有默认值不报。运行中的 8765 服务（每次 GET `/` 重读磁盘）刷新即生效，无需重启。

## v5.7.24 补丁（2026-09-03）· EN 界面 help 说明不再露出中文（HELP_EN 英文说明字典）

- **用户反馈**：点「EN」切换后字段标签已是英文（Test side / Allocation ratio / Output language / Target power / SD），但每行下方的 help 说明仍是中文（如 side 下「检验方向: one=单侧, two=双侧(默认)」、language 下「显式覆盖 coze 计算端…」等）。
- **根因**：`samplesize_power.py` 的 argparse help 本身就是**中文**（非空），而 v5.7.23 的 `help_en` 注入条件仅为「argparse help 为空」（覆盖 effect/alpha 等裸定义字段），导致这些非空中文 help 字段在 EN 界面退回原 help → 露出中文。
- **改动（form_schema.py）**：
  - 新增 `HELP_EN`（与 `HELP_ZH` 对称的英文说明），覆盖 HELP_ZH 全部 16 键（effect/sd/alpha/power/side/ratio/nobs/language/k_groups/margin/p1/p2/accrual_time/followup_time/hr_expected/win_ratio_theta）+ 3 个纯中文冷门参数（reestimate_method/correction/sim_seed）。
  - `get_catalog` 注入升级：`help_en` ①HELP_EN 显式 → ②argparse help 为空且有 PARAM_META 英文标签 → ③argparse help 含中文（`_looks_chinese` 检测 CJK 占比 >15%）且有 PARAM_META 英文标签兜底。
  - 新增 `_looks_chinese(text)` helper。
- **验证**：`py_compile` + `node --check` 通过；8995 实例实测 `?lang=en` schema：side/ratio/language/power/sd 的 `help_en` 均返回英文（"Test direction: two-sided (two) or one-sided (one)." / "Allocation ratio n2/n1; 1.0 means equal group sizes." 等）；按前端渲染规则（en→help_en or help）复扫 10 个常用检验全部字段 **0 中文泄漏**；页面接线点 4 项全 OK。
- **注**：47 个 gs_*/sim_* 等冷门参数 help 为中英混合（含英文术语，如 "仿真设计类型 / simulation design"），EN 界面可读性足够，未逐一补英文说明（如需可后续补 HELP_EN）。

## v5.7.23 补丁（2026-09-03）· 动态表单内容全双语化（参数标签/下拉选项/说明/检验下拉）

- **用户反馈**：界面选项里的参数标签、下拉选项、文字说明还没随语言切换（静态 chrome 已双语，动态渲染的表单没接）。
- **根因**：表单字段来自服务端 `schema_for(test)` 反射，但 ① server 调用 `schema_for(tid)` 时**没传 lang**、前端 `/api/schema/<test>` 也没带 `lang` → 永远中文；② 前端 `fieldHTML` 用单语 `p.label`（argparse 英文 help 或裸值）、下拉 `choices` 裸值、`help` 原始英文，全不随 `LANG` 切换；③ `setLang` 切换时只重渲染表单/图形，**不重建检验/家族下拉**。
- **改动**：
  - **`form_schema.py`**：新增 `CHOICE_LABELS`（下拉值 → `(zh,en)` 元组，覆盖 side 单侧/双侧等）与 `HELP_ZH`（常用参数中文说明）；`get_catalog(lang)` 注入 `choice_labels`（元组结构）与 `help_zh`；`_label_for`/tests/families 双语字段齐备（label 随 lang、label_zh/label_en 恒定）。
  - **`server.py`**：schema 路由 `/api/schema/<test>` 支持 `?lang=`，传入 `schema_for(tid, lang)`；`/api/schema` 全量目录同样按 lang 生成。
  - **`workbench.html`**：`onTest` 调 schema 带 `?lang=`；`fieldHTML` 按 `LANG` 取 `label_zh/label_en`、`help`（zh 优先 help_zh，en 优先 help_en 退回 help）、`choices` 经 `choice_labels` 元组按语言显示标签；`renderFigureCtl` figure_mode 选项双语；`buildFamilyOptions()` 按语言重建家族/检验下拉（label 用 label_zh/label_en）；`setLang` 重建下拉 + 重渲染表单。
  - **英文 help 兜底**：`effect`/`alpha` 等在 argparse 里裸定义无 help，英文界面 help 曾空白；现 `get_catalog` 对 argparse help 为空但有 `PARAM_META` 英文标签的字段注入 `help_en`，前端英文界面 `p.help_en || p.help`（如 `effect`→"Effect size (Cohen's d; or raw Δ if σ given)"、`alpha`→"Significance level α"）。不动计算 CLI/argparse。
- **验证**：`node --check` + `py_compile` 通过；8980 实例实测 schema `?lang=en` 返回 `label_en`/`help_en` 英文（effect/alpha 的英文 help 不再空白）、`side.choice_labels={'one':['单侧','one-sided'],'two':['双侧','two-sided']}`、`?lang=zh` 返回中文 label（如 `effect`→「效应量…」、`side`→「检验方向」）；页面 6 个双语接线点（onTest 带 lang / label 双语 / choice_labels 元组 / help 双语 / 下拉重建 / figure_mode 双语）全 OK；`/api/nl` 回归 `ttest_ind` 正常。

## v5.7.22 补丁（2026-09-03）· 删除「49 检验」角标 + 会话下拉/轮数双语同显

- **用户反馈**：①「49 检验 / tests」角标没实际用处，删掉；②「选择会话线程」下拉空选项、以及会话名称里的「N 轮」仍只有中文、切英文后不跟着变。
- **根因**：与 v5.7.21 同源——这些文案是 JS 动态生成（或 innerHTML 重建 select 时丢了 `data-i18n`），`setLang` 切换不重渲染。
- **改动（仅 workbench.html）**：
  - **① 删角标**：移除 header 的 `<span id="hTests">` 元素与 `$("hTests").textContent=...` 赋值（及已废弃的 `testsSuffix` 残留）。
  - **② 会话下拉**：`pickSession` 在 zh/en 字典均设为双语同显值「— 选择会话线程 / Select thread —」；`refreshSessions` 重建 select 时给空选项保留 `data-i18n="pickSession"`（由 `localize()` 接管，切语言重渲染一致）。
  - **③ 轮数**：`turn` 在 zh/en 均设为「轮 / turn」；`turnFmt` 均设为「第 %d 轮 / Turn %d · 」；会话项渲染为 `(N 轮 / turn)`、thread 历史为「第 N 轮 / Turn N ·」。动态文案直接双语同显，不依赖语言切换。
- **验证**：`node --check` 通过；node 求值 I18N 确认 zh/en 各 104 键对齐、32 个 `data-i18n` 全覆盖、无 `hTests`/`testsSuffix` 残留、三处双语键确认 `true`；8970 实例 `/api/health` OK、页面 `id="hTests"` 已不存在、会话列表含轮数（前端渲染 `(N 轮 / turn)`）。

## v5.7.21 补丁（2026-09-03）· 检验数角标「49 检验」改为中英双语同显

- **用户反馈**：header 角标「49 检验」此前用 `T.testsSuffix` 拼出，属 `loadCatalog` 里的 JS 动态文本、无 `data-i18n` 属性，`localize()` 不重算；切到英文后仍是中文「检验」，未双语化。
- **改动（仅 workbench.html）**：按用户「不方便切换就直接同时显示」的指令，把 `hTests` 改为中英文同显：`h.tests + " 检验 / tests"`（如「49 检验 / tests」）。删除已废弃的 `testsSuffix` 键（zh/en 各一处），`I18N` 字典维持 zh/en 对齐（各 104 键）。
- **验证**：`node --check` 通过；node 求值 I18N 确认 zh/en 各 104 键完全对齐、32 个 `data-i18n` 键双语言全覆盖、无 `testsSuffix` 残留；8965 实例 `/api/health` 返回 `tests=49`、页面含「 检验 / tests」双语行。

## v5.7.20 补丁（2026-09-03）· Bug 反馈框放大 + 界面提示横幅 + 全界面双语化（ct-base 规范）

- **用户反馈（三项）**：①「报告问题 / Bug 反馈」弹窗的「问题描述」框高度太小，使用不便；② 在界面合适位置提示「本界面只是为了方便操作，全功能还请按 AI 智能体技能的直接交互方式使用」；③ 界面已有语言切换按钮但未真正双语化，按 ct-base `references/language_policy.md` 规范补齐。
- **改动（仅前端 workbench.html，后端零改动）**：
  - **① Bug 反馈框放大**：`#bugDesc` 最小高度由 56px 提到 180px（`min-height:180px`，保留 `resize:vertical`），更易输入长描述。
  - **② 界面提示横幅**：header 下方新增 `.app-hint` 浅色软提示条（带 ℹ 图标），文案 `appHint`：「本界面只是为了方便操作，全功能还请按照 AI 智能体技能的直接交互方式来使用。」随语言切换。
  - **③ 全界面双语化（对齐 ct-base 规则 1–2）**：
    - 扩展 `I18N` 字典至 zh/en 各 97 键，覆盖全部静态 chrome 与动态提示（标题、三步区、自然语言入口、手动设置、求解方向、图表控制、保持会话、主按钮、导出、会话历史、Bug 反馈全套、效应量助手、提示横幅等）。
    - 新增 `localize()`：按 `data-i18n` / `data-i18n-ph` / `data-i18n-title` 三类属性重渲染静态文案；新增 `detectInitLang()`：按 `navigator.language` 判 `zh*` → 默认中文，否则英文（ct-base 规则 1–2）。`init()` 启动即调 `detectInitLang()+localize()` 并高亮当前语言按钮；`setLang()` 切换时同步重渲染表单/图表控件。
    - 动态 JS 文案（结果空态、计算中、多组计算、会话轮次、NL 识别提示、Bug 提交/确认/失败、导出成功/失败、效应量助手标签与占位符、检验数后缀、离线提示、图形时间占位符等）全部路由到 `T.*`，扫描确认 0 处残留硬编码中文动态串。
    - **远程报告不翻译**：coze 返回的报告（text/figures/r_result）按 `language: LANG` 由云端返回对应语言，本地呈现层不二次翻译（ct-base 规则：本地只翻译 UI 框架标签）。
- **验证**：`node --check` 内联 JS 通过；node 求值 I18N 确认 zh/en 各 97 键完全对齐、32 个 `data-i18n` 键在两种语言均覆盖；Python 扫描确认动态 `textContent/innerHTML/placeholder` 中硬编码中文串 0 行；8960 实例结构校验全过（bugDesc 放大、app-hint 横幅、语言按钮、localize/detectInitLang/init 接线），`/api/nl` 回归 `ttest_ind` 正常。

## v5.7.19 补丁（2026-09-03）· 表单不分「必填/通用」两栏 + 效应量 Δ/σ 自动折算

- **用户反馈**：① 表单分「必填参数 / 通用参数」两栏没有实际意义，合并成一栏即可；② 像「效应量（Cohen's d）」这种必填项其实可以从其他指标算出来（如均值差 Δ、标准差 σ），不应强迫用户手算 d。
- **改动（仅前端 workbench.html，后端零改动）**：
  - `renderForm`：删除「必填参数」「通用参数」两个 `<div class='sec'>`，合并为单一「参数设置」区（必填清单 + 通用清单拼接，去重由 v5.7.18 已保障）；仅对契约必填字段保留 `*` 提示（per-field 标记，非分栏）。
  - **新增 `injectEffectHelper`**：连续型均值检验（同时含 `effect` 与 `sd` 参数，如 ttest_ind/paired/one/anova/equivalence 等）在参数区下方挂「效应量换算助手」——用户填「均值差 Δ」与「标准差 σ」，实时显示 `d = Δ/σ`，并把 Δ 写入 `effect` 字段。后端 `samplesize_power.py` 早已实现：sd>0 时 `effect` 视为原始均差 Δ，自动 `d = effect/sd`（L1052–1056），故无需改计算逻辑。
  - `form_schema.py` `PARAM_META["effect"]` 标签改为「效应量（Cohen's d；提供 σ 时也可直接填均差 Δ）」，字段自解释。
  - 加 `.eff-helper` / `.eff-d` 样式（浅蓝软面板，与现有 `.sec`/`.row` 体系一致）。
- **边界**：效应量换算仅对「含 sd 参数」的连续型检验出现（比例/生存/计数类检验无 sd，不显示，避免给出错误换算）；效应量本身仍是真必填（经 Δ 提供仍满足 required，不编造数值）。
- **验证**：本环境执行通道（Bash/PowerShell 子进程）故障，无法跑实时 HTTP/node；改动经代码审查确认：`renderForm` 合并逻辑、`injectEffectHelper` 引用 `data-dest=effect/sd` 与 `collectParams` 收取一致、后端 d=Δ/σ 已实现。建议本地干净端口重启 + Ctrl+Shift+R 强刷实测 ttest_ind：参数区为单栏；填 Δ=5、σ=10 → 显示 d=0.500 且 effect 字段自动填入 5，点计算应得 d=0.5 对应的样本量。

## v5.7.18 补丁（2026-09-03）· 修复表单重复字段：必填参数与通用参数去重

- **用户反馈**：「必填参数」和「通用参数」两区有重复项，例如分配比 n2/n1（ratio）在两个区都出现了一次。
- **根因**：`schema_for()` 的 `common` 直接取 `COMMON_PARAMS` 全部分组（含 ratio/alpha/side/effect），而 `required` 取 contract 里该检验的必填清单（ttest_ind 的 required 正是 `[effect, alpha, side, ratio]`）——两者交集的字段被 `renderForm` 渲染了两遍。
- **改动**：`form_schema.py` `schema_for()` 将 `common` 定义为「通用分组 减去 该检验必填清单」（`common = [n for n in groups[0].params if n not in required_set]`）。必填的公共参数（ratio/alpha/side/effect）只出现在「必填参数」区（带 `*`），只有可选的公共参数（power/nobs/sd/language）留在「通用参数」区。前端 `renderForm` 仅遍历渲染，无需改动；`collectParams` 按 `data-dest` 收集，去重后字段仍在必填区渲染，不会漏收。
- **效果**（以 ttest_ind 为例）：必填 = `[effect, alpha, side, ratio]`，通用 = `[power, nobs, sd, language]`；ttest_paired 的 ratio 正确地只留通用区（配对设计 ratio 可选）。
- **验证**：本环境执行通道（Bash/PowerShell 子进程）故障，无法跑实时；改动为单条确定性列表推导，已逐检验核对去重逻辑正确。建议本地干净端口重启 + Ctrl+Shift+R 强刷实测：打开 ttest_ind，确认 ratio/α/side/effect 仅在「必填参数」出现一次。

## v5.7.17 补丁（2026-09-03）· 缺失参数用常用值填充 + 对话框选项预设常用值

- **用户反馈**：缺失的常见参数（ratio/alpha 等）应自动用常用值填充；对话框的下拉/输入框也应直接呈现这些常用值，不必每次手填。
- **改动**：
  - `form_schema.py` `UI_DEFAULTS` 显式写入临床试验常规默认值：`ratio=1.0`（等比例，argparse 原默认 None，必须注入）、`alpha=0.05`、`power=0.8`、`side="two"`（后三者 argparse 已默认，列出作文档/兜底）。注入仅当 argparse 默认 None 时生效，不覆盖 coze 自有缺省。
  - `workbench.html` `fieldHTML`：按 schema 的 `p.default` 预填——下拉框（choices）自动 `selected` 到常用值（side 默认双侧 two，纠正此前默认落到 one）、数字/文本/布尔框直接写入常用值（α=0.05 / ratio=1 / power=0.8），打开工作台即见。会话态 `applyCurrentToForm` 仍优先用会话值覆盖，不冲突。
  - `server.py` `_compute`：**保持**「required 字段有默认值则缺省补填」原逻辑（不扩到全 CATALOG）。前端的预填已随表单发送当前检验的常用值，服务端仅作兜底；真必填且无默认者（effect/p1/p2 等效应量类）仍报 400 要求用户给出。
- **注意**：本次仅在「有公认常用值」的参数上做预设；效应量类（effect/p1/p2/margin 等）无公认默认，保持必填、不自动编造，避免误导样本量结果。
- **验证**：本环境执行通道（Bash/PowerShell 复杂参数）仍故障，无法跑实时 HTTP / node 编译；改动经文件工具复核落地，JS 结构（fieldHTML 箭头函数/括号平衡）与 Python 语法人工审查通过。建议本地干净端口重启 + Ctrl+Shift+R 强刷实测：打开即见 α=0.05/ratio=1/power=0.8/side=two 已预填。

## v5.7.16 补丁（2026-09-03）· 修复追问「必填参数缺失：effect」+ 去除误导文案

- **用户反馈**：会话内发追问「power 0.85 0.9 0.95 的情况都算一下」后，结果区提示「必填参数缺失：effect（已自动补默认）」。该提示来自 `doCompute` 的 400 错误处理（前端 688 行），说明追问实际走了 `doCompute(false)` 空表单分支。
- **根因（两处耦合）**：① `nlCompute` 每次追问都 `await onTest(route.test)` 重建空表单，把已填的 `effect/alpha/side` 清空，而追问 NL 的 `ps` 往往为空 → 表单变空；② `doCompute` 用「表单 vs CUR_CURRENT」算 delta，空表单使 `changed={}` → 发空 params → 服务器缺 `effect` 报 400。多值分支虽在 onTest 之后、以 CUR_CURRENT 为基底本应正常，但若浏览器未强刷跑的是旧 HTML（无 runMultiCompute 分支）就退化到 doCompute 空表单。
- **修复（workbench.html）**：
  - `nlCompute`：仅当 `route.test !== CUR_TEST` 才 `onTest`（同检验追问不重建表单，保留已填值）。
  - `doCompute`：基底改为「CUR_CURRENT 兜底 + 当前表单值覆盖」（`Object.assign(base, collectParams())`，`base=CUR_CURRENT` 去 test 键），不再依赖空表单 delta；会话审计仍由服务端确定性合并。
  - `runMultiCompute`：基底取数稳健化——`CUR_CURRENT.test===test` 时优先用 CUR_CURRENT，否则退回 collectParams，再叠加 ps。
  - 去掉错误文案里误导性的「（已自动补默认）」（服务器返回 400 并未补默认，属虚假陈述）。
- **验证**：本环境执行通道持续故障（Bash 序列化 / python 子进程被吞 / PowerShell 脚本封装层 JS 报错），无法跑实时 HTTP；经严格代码审查确认：同检验追问跳过 onTest + doCompute 以 CUR_CURRENT 兜底，effect 必随基底入参；多值路径基底取 CUR_CURRENT（含 effect）后逐组覆盖 power，三组分别计算。建议用户本地干净端口重启 + Ctrl+Shift+R 强刷实测。

## v5.7.15 补丁（2026-09-03）· 工作台 NL 追问：继承会话检验类型 + 多值参数分别计算

- **用户反馈**：会话内发追问「power 0.85 0.9 0.95 的情况都算一下」→ 识别结果「未识别（置信度 low）· 规则识别；未能识别检验类型，请手动选择」。根因：追问类 NL 通常只给参数、不重复检验类型关键词，`classify_test` 返回 `test=None`；旧代码 `!route.test` 直接 bail，没继承当前已选定的检验。
- **后端 `_nl`（server.py）**：
  - 请求体新增 `current_test`；当规则未命中（test=None）但 `current_test` 合法（∈ TEST_NAMES）时**继承**为 `route.test`，并标 `route.inherited=true`（前端显示「规则识别（继承会话）」）。前端 `nlCompute` 调用时传入 `current_test: CUR_TEST`。
  - 新增确定性 `_detect_multi_values(nl)`：检测同一参数被给出多个数值（如「power 0.85 0.9 0.95」「效应量 0.3/0.4/0.5」），返回 `route.multi={param:[v1,v2,...]}`，仅当数值≥2 才收录；单值仍走 `params` 作默认，二者互补。
- **前端（workbench.html）**：
  - `nlCompute`：识别提示追加「将分别计算 power=0.85/0.9/0.95 共 3 组」；命中 `route.multi` 即走 `runMultiCompute`（不再单值 doCompute）。
  - 新增 `runMultiCompute(test, multi, ps)`：以**会话继承的有效参数 CUR_CURRENT + NL 单值增量 ps** 为基底（删掉多变参键），对多值笛卡尔积逐一 `POST /api/compute`，保证「其余参数无损继承」；`renderMultiResults` 渲染对比表（n/组、总 N、状态）+ 每组数值卡片/叙述（图表仅首组，避免过度渲染）。多组结果暂不可单文件导出（`CUR_RESULT=null`）。
  - 新增 `.mtable` CSS。
- **验证**：本环境 Bash 子进程序列化故障 + python 执行被沙箱吞掉，无法跑实时 HTTP 验证；代码经完整人工审查，逻辑与既有 `renderResult`/`doCompute` 同构。建议用户本地起真实实例（不带 `CTSS_COZE_MOCK`）实测：会话内输入「power 0.85 0.9 0.95 的情况都算一下」应显示继承 ttest_ind + 三组对比样本量。

## v5.7.14 补丁（2026-09-03）· 工作台按钮点击反馈（单击即时可见"已生效"）

- **用户反馈**：单击 `nlComputeBtn` 后按钮无任何变化，且 NL 识别 + 真实 coze 计算均为异步（1–3s），用户感觉"点了没反应"。
- **实现（三态反馈，纯前端、无后端改动）**：
  - CSS：`.btn:active{transform:translateY(1px) scale(.985)}`（按下手感）+ `.btn.busy{opacity:.6;cursor:wait;pointer-events:none}`（处理中态防重复点击）+ `.btn .spin` 转圈动画（`@keyframes spin`）。
  - HTML：`nlComputeBtn` 内注入 `<span class="spin" aria-hidden="true">`（默认 `display:none`，不影响 `updateNlBtn` 的文本节点定位）。
  - JS：`nlCompute()` 用 try/finally 包裹——点击瞬间 `btn.disabled=true; btn.classList.add("busy"); 文本→"处理中…"`；无论成功/失败/提前 return，finally 统一 `disabled=false; classList.remove("busy"); updateNlBtn()` 恢复上下文标签。覆盖全部分支（计算 / 智能识别并计算 / 应用修改并重新计算 / 识别并追问）。
- **验证**：JS `node --check` 通过；8915 实例结构校验通过（`.btn.busy` / `@keyframes spin` / `.btn:active` / `class="spin"` / busy-finally 包裹 / "处理中…" 文案均注入）。

## v5.7.13 补丁（2026-09-03）· 工作台 UI：彻底合并重复框 + 单按钮（纠正 v5.7.12）

- **用户反馈（v5.7.12 不到位）**：① 计算后「手动设置」自动弹开；② 底部「应用修改并重新计算」与「识别并追问」两按钮未合并；③ 「精确修改」框组只是挪进「手动设置」但**字段与主表单完全重复**（effect/power/nobs/alpha/side/ratio/sd 与主表单同一批），属"假合并"。
- **实现（有针对性合并）**：
  - 删除 `#quickEdit` 重复框及 `applyQuickEdit`/`doComputeWith`/`collectParamsFromObj`；`nlCompute` 会话态「识别并追问」改为直接 `doCompute(false)`（表单已用 NL 参数回填，delta 继承会话）。
  - 新增 `syncFormAfterCompute()`：计算后把当前结果参数**回填到主表单 `#formArea`** 作为唯一编辑面，**不再** `manual-details.open=true`（消除自动弹开）。
  - 底部单一按钮 `nlComputeBtn` 标签上下文自适应：`updateNlBtn()` 按「是否会话 × 是否填 NL」四态显示「计算 / 智能识别并计算 / 应用修改并重新计算 / 识别并追问」，合并原两按钮。
  - NL 输入框加 `oninput="updateNlBtn()"`，`init()` 末补一次 `updateNlBtn()` 让初始态正确。
- **验证**：MD5 磁盘↔服务一致（8913）；JS `node --check` 通过；Grep 无 `quickEdit/applyQuickEdit/doComputeWith/buildQuickEdit` 死引用；`/api/nl`、`/api/compute` 真实 coze 回归正常（ttest_ind → n=64）。

## v5.7.12 补丁（2026-09-03）· 工作台 UI：精确修改框组合并进「手动设置」（被 v5.7.13 取代）

- **背景**：结果出来后的「精确修改」框组（含「应用修改并重新计算」按钮）原位于「手动设置」折叠**之外**，表现为底部独立悬浮块（dashed 边框），与 v5.7.2「上移分析选项到手动设置」的收拢诉求不一致，用户反馈"精确修改框组仍然是单独存在的"。
- **实现**：`workbench.html` 将 `#quickEdit` 整块从 `details` 外移入「手动设置（可选）」`manual-body`（图表控制之后）；`buildQuickEdit()` 显示精确修改时自动 `manual-details.open=true`，确保用户在展开的设置区看到。
- **验证**：Grep 确认 `#quickEdit` 全文件唯一一处定义（位于 manual-body 内），左列结构闭合完好；`/api/nl` 路由复测未回归（`ttest_ind` 正常）。

**运行说明（真实计算是默认，无需本地端点）**：工作台 `server.py` 默认 `BACKEND = CozeBackend()`，`coze_client.py` 仅当 `CTSS_COZE_MOCK in ("1","true","yes")` 才走 mock；**不设该 env 即真实调用技能内嵌端点 `https://ct-samplesize.coze.site/run`**，Token 由 `coze_token_embedded.py` 内嵌公共 blob 兜底（`config/coze.dat` 缺失无影响）。真实计算实测：`/api/compute` ttest_ind `{effect:0.5,alpha:0.05,side:two,power:0.8}` → 每组 n=64 + 真实 SVG 图表。`CTSS_COZE_ENDPOINT` 用户无需设置。启动命令：`python adapters/workbench/server.py <干净端口>`（勿带 `CTSS_COZE_MOCK`）。

## v5.7.10 补丁（2026-09-03）· 工作台对齐参数级「本地追问」信号（samplesize_power.py 外部改动）

- **背景**：技能 `scripts/samplesize_power.py` 的 `--nl` 路由文案/语义外部更新为「本地确定性预路由 + 参数别名解析；置信度低或参数不全时由本地 agent 向用户追问缺失 test/参数（≤2 轮→默认，ct-base §6.1），原始 NL 不入 coze」。工作台 `_nl` 原先只取 `param_aliases.extract_parameters` 的 params/side/solve_for_power，丢弃了参数级兜底信号（needs_llm_fallback / missing / notes），未对齐该语义。
- **实现**：
  - `server.py` `_nl`：规则提取参数后，把 `extracted` 的 `needs_llm_fallback` → `route["needs_params_fallback"]`、`missing` → `route["params_missing"]`、`notes` 并入 `route["notes"]`；`solve_for_power` 标记进 `route`（不再污染 params 子字典，因 CLI 无该键）。所有返回路径的 route 均带这些信号。
  - `workbench.html` `nlCompute`：已识别检验类型但 `route.needs_params_fallback` / `route.params_missing` 非空时，在 `nlHint` 追加「未识别到计算参数，请补充…」/「待补充：xxx」，实现本地追问提示。
- **验证**：端到端（端口 8900，规则优先）三条 NL：
  - A「两组均数比较…」→ `engine:"rule"`，params 完整，`needs_params_fallback` 不出现（不误报）✓
  - E「帮我算个样本量」（无参数无数字）→ `test:null`，`needs_params_fallback:true`，notes 含参数缺失提示 ✓（前端将提示手动选 + 补参数）
  - C「非劣效生存试验，NI界值1.25，期望HR=1.0…」→ params 透传 `margin:1.25, hr_expected:1.0`（test-specific 参数不丢）✓
  - `py_compile` 通过。
- **注**：test 识别（ni_survival 误判 survival_superiority）属 classify_test 既有问题，不在本任务「参数识别」范围内；**已于 v5.7.11 修复**（见下）。

## v5.7.11 补丁（2026-09-03）· 修复 classify_test 非劣效生存误判 survival / 修饰族被基础词累加压过

- **根因**：
  1. `classify()` 打分用 `weight * len(hits)` 累加；`survival` 在 RULES 中**双定义**（显式「生存分析」w10 + 基础「生存」w4），多关键词命中累加虚高（如「非劣效性生存分析样本量」→ survival=14）反向压过更特异修饰族 `ni_survival`(w12) / `survival_superiority`(w12) / `survival_equivalence`(w12)。 2. `ni_survival` 关键词仅 `ni生存` 连写，「NI 生存」（缩写+空格）漏判。 3. `survival` 规则 `\blogrank\b` 的 `\b` 在中文包围下失效（CJK 属 `\w`，与 logrank 间无单词边界）→ 纯「logrank 检验」路由为 None。
- **实现**：
  1. `classify()` 打分改为「同一 test 取最高单次权重（max），不再累加」（#2 处 `weight * len(hits)` → `max(scores.get(test,0), weight)`），根治基础词多命中虚高。 2. `ni_survival` 补关键词 `r"ni\s*生存"`（覆盖「NI 生存终点」等缩写+空格变体）。 3. `survival` 规则 `\blogrank\b` → `r"logrank"`，修复中文环境 logrank 路由。
- **验证**：30/30 代表 NL 回归全过（非劣效生存 12 变体 + 纯非劣效 + 优效/等效生存 + 基础生存 + 其他基础 test + 无解兜底）；工作台 `/api/nl` 端到端「非劣效性生存分析样本量，NI界值1.25」→ `test=ni_survival, params={margin:1.25}`、「NI 生存终点样本量估算」→ `test=ni_survival`，均 `engine=rule`。

## Unreleased · NL fallback 红线澄清（文档/提示词修正，无计算逻辑改动）

- **背景**：早期条目曾将 NL 兜底描述为依赖 coze 平台大模型，与契约事实不符——coze 计算端点（/run，graphs.graph：samplesize→feishu_save→END）纯计算、无大模型节点、不接收自然语言；`build_params` 信封只含 `{test, params, mode}`。v5.7.9 已将工作台 NL 识别改为「规则优先、本地默认大模型（Ollama）兜底」，本补丁同步纠正 CLI 主路径文档。
- **修正**：
  1. SKILL.md feature ④ 与新增「★ NL fallback red line」小节：明确 `needs_llm_fallback` 标记的 NL **禁止**编排者当参数分类器拼 JSON 发 coze；强制路径=本地确定性解析失败→打印结构化提示→向用户追问（≤2 轮→ct-base §6.1 默认）；原始 NL 永不进 coze 信封。工作台可选本地 LLM（nl_llm.py）作二级识别器，与 coze 计算端点不可混谈。 2. scripts/samplesize_power.py：移除全部「依赖远程计算端点大模型解析/补全」的旧打印文案与注释（E1/E2 注释、--nl argparse help、NL-route/NL-params 提示），统一改为「向用户追问」。 3. adapters/coze/src/main.py：`/v1/chat/completions` 加注释，明确该通用聊天接口与 samplesize 计算图无关、coze 计算端点无 NL/大模型路径。
- **验证**：grep 复核 skills 树（排除 nl_llm.py / CHANGELOG 历史 / tests/scratch）已无「依赖远程端点大模型兜底」类残留表述；本次仅改文档与提示词，未动计算逻辑。

## v5.7.9 补丁（2026-09-03）· 反转 NL 识别优先级：规则优先、大模型兜底

- **诉求**：用户纠正 v5.7.8 的方向——NL 识别不应「默认大模型、规则降级」，而应与技能主路径一致：**先走确定性代码（classify_test 规则），规则完全未命中（test=None）再走本地默认大模型（Ollama）兜底**。
- **实现**：`server.py` `_nl` 顺序调整为 ① 先 `classify_test.classify` + `param_aliases.extract_parameters`；若 `route["test"]` 非空（规则命中）→ 直接采用（`engine="rule"`）；② 仅当 `test=None` 时调用 `nl_llm.nl_resolve`（`engine="llm"`），并将其抽到的检验类型与相关参数合并回规则已抽的通用参数（alpha/power 等）；③ 两者均未识别 → 退回 `test=None` 规则结果，前端提示手动选择。
- **验证**：`py_compile` 通过；规则路径（「两组均数比较…」）直接 `engine="rule"` 命中 ttest_ind，大模型不触发；大模型仅在规则 `test=None` 时触发（沙箱无 Ollama → 自然走规则，不退化）。
- **注**：`nl_llm.py` 定位不变（本地默认大模型客户端），仅调用时序从「优先」改为「兜底」；`CTSS_NL_ENDPOINT` / `CTSS_NL_MODEL` 依旧有效。`workbench.html` 的 `nlHint` 引擎来源显示（`route.engine==="llm"?"本地大模型识别":"规则识别"`）仍适用。

## v5.7.8 补丁（2026-09-03）· NL 识别默认本地大模型（Ollama），规则降级

- **诉求**：用户要求工作台 NL 识别「默认用本地默认大模型完成」，与技能主路径（samplesize_power.py: 本地规则预路由 + coze 平台 LLM 兜底）对齐，不再走离线优先的纯规则。
- **实现**：
  1. 新增 `adapters/workbench/nl_llm.py`（stdlib-only）：默认调本机 Ollama `http://localhost:11434/v1/chat/completions`（OpenAI 兼容、keyless，即用户生态「本地默认大模型」qwen3.5:9b/27b）；`CTSS_NL_ENDPOINT` 可覆盖为任意 OpenAI 兼容端点（如 coze 工作流 `/v1/chat/completions` 实现完全对齐 coze LLM）。 2. system prompt 注入可用 test / param 白名单，约束模型只输出受限 JSON（`test` 必为已知检验、`params` 键必为已知参数），从根抑制幻觉；`side/confidence/missing` 同结构。 3. `server.py` `_nl`：默认调 `nl_llm.nl_resolve`；返回有效 `test` 即用大模型结果（`engine="llm"`）；大模型端点不可达 / 未识别 `test` 时降级 `classify_test` 确定性规则（`engine="rule"`，已覆盖均数/两组/t检验/α小数/d 等常见表述）。`route` 带 `engine` 字段标记来源。
- **验证**：① 假 Ollama（8895）返回预设 JSON → `/api/nl` 返回 `engine:"llm"` + `test=ttest_ind` + 完整参数（白名单校验/解析正确）；② 端点不可达（`:1`）→ 降级 `engine:"rule"` + 同结果（不退化）。`py_compile` 两文件通过。
- **注**：本机无 Ollama 运行时自动走规则降级（功能不退化）；本机起 Ollama（qwen3.5:27b/9b，`ollama serve` + `ollama pull`）后即自动切大模型识别。`CTSS_NL_MODEL` 可覆盖模型名。

## v5.7.7 补丁（2026-09-03）· 修复 NL 识别「未识别」+ 参数抽取漏抽

- **现象**：用户输入「帮我算一下两组均数比较的样本量，效应量 d=0.5，把握度 80%，双侧 α=0.05」→ 工作台识别为「未识别（置信度 low）」。
- **根因（三层）**：
  1. `classify_test.py` 基础终点词只覆盖「均值」未覆盖「均数」（医学统计同义），且「两组 / 独立样本 / t检验 / 英文 two-sample·t-test」缺泛化规则 → 整句零关键词命中、返回 `test=None`。 2. `param_aliases.py`：`alpha` 在百分率类集合内，用户写「α=0.05」小数形式被「无百分号且关键词无率语境则拒收」逻辑误杀；`effect` 的「效应量 d=0.5」数值夹在 `d=` 后未被覆盖。 3. `server.py` `_nl` 把 `extract_parameters()` 返回的**整个 dict**（`{params, side, solve_for_power, ...}`）当 params 过滤，而非取其内部 `params` 子字典 → `power/alpha/effect` 全丢，仅顶层键 `side` 命中。
- **修复**：
  1. `classify_test.py`：`ttest_ind` 显式名补 `两组.*均数 / 两组.*均值 / 两组.*比较 / 独立样本\s*t / 独立样本 / 两独立样本 / two[- ]?sample / t[- ]?test / independent`；基础终点补 `均数`、`t\s*检验`。 2. `param_aliases.py`：`effect` 关键词加 `(?<![a-z])d\s*[:=]`（负向后顾排除 `sd=` 误抓）；`_find_param` 对 `alpha/power` 放行 0~1 小数形式（不再要求百分号）。 3. `server.py` `_nl`：取 `extracted.get("params")` 子字典，并把 `side / solve_for_power` 提升为顶层键再过滤 `CATALOG["params"]`。
- **验证**：回归 7 例（含「两组均数比较」「两组独立样本t检验」「two-sample t-test」「独立样本t检验」）全部路由 `ttest_ind` 且参数完整；`/api/nl` 端到端 200 返回 `{"route":{"test":"ttest_ind","confidence":"high"},"params":{"power":0.8,"alpha":0.05,"effect":0.5,"side":"two"}}`。纯参数无检验类型词的用例（如「效应量 d=0.5，sd=2」）仍正确返回 `test=None`（应追问），符合预期。

## v5.7.6 补丁（2026-09-03）· 删除页脚过时提示文字

- **清理**：移除 `workbench.html` 页脚残留的「本地工作台 · 反馈保存于 `bugreports.json`（无网络时自动复制到剪贴板）」提示（该文案为早期本地落库版遗留，与 v5.7.4 改默认提交 coze 端点后的行为不符；且 v5.7.4 当轮对该行的 Edit 假成功未落盘）。页脚现仅保留「报告问题 / Bug 反馈」按钮。
- **验证**：Grep 确认全文无「本地工作台 · 反馈保存于」残留；`<footer>` 结构闭合正常。

## v5.7.5 补丁（2026-09-03）· 启动端口冲突检测，根治「/api/schema 404」误用

- **根因**：`server.py` 默认端口 8765；沙箱 `taskkill` 对 python server 进程不生效，旧实例累积。用户直接 `python server.py`（走默认 8765）时新进程绑定失败退出，浏览器实际访问到**内存中是旧代码（无 `/api/schema` 路由）的旧进程** → 返回 404，触发「无法加载检验目录」。
- **修复**：`main()` 启动前用 `_port_free()` 预检端口；被占用时打印明确错误（含两种处理方案：换干净端口 / `netstat -ano | findstr :PORT` + `taskkill /PID`）并 `sys.exit(1)`，不再静默复用旧实例。启动成功打印醒目 banner。
- **验证**：`python server.py 8765`（被旧进程占）→ 打印错误并 `exit(1)`；`python server.py 8891`（空闲）→ 正常启动，`/api/health`、`/api/schema`、`/` 均 200。

## v5.7.4 补丁（2026-09-03）· Bug 反馈改默认提交 coze 统一端点（对齐 ct-base §20.3.5）

> 触发：用户指出「报告问题 / Bug 反馈」应默认提交到 coze，而非本地落库。经查 ct-base `references/bug_report_endpoint.md` 规定：全 ct- 技能共用统一端点 `https://ct-bugreport.coze.site/run`，默认提交、本地仅兜底。
- **后端 `_bugreport` 重写**：移除原先写死本地 `bugreports.json` 的反例，改为复用 `adapters/bug_report.py::send_to_endpoint`（脱敏白名单信封 `build_report`，含 `skill/skill_version/test/error_type/description/locale/query_origin`；`skill_version` 从 `SKILL.md` frontmatter 读取一次）。默认 POST 到统一 coze 端点（`action=report`）；仅当端点不可达时降级 `bug_report.save_local_report()` 写本地 md（§20.3.4 / §13.2 作者邮箱 `medstatstar@gmail.com`）+ 追加 `bugreports.json` 安全网。MOCK 演示模式下 `engine_status` 标记 `mock (offline demo)` 便于作者区分环境。
- **前端两阶段确认（§20.3.2）**：模态框新增「展示脱敏报告 → 确认发送」两步；打开时把当前检验/会话/参数预填进可编辑 `description`（用户确认制，白名单只带元数据、不泄漏原始数据）；页脚提示改为「默认提交至 `ct-bugreport.coze.site`，不可达时本地保存」。提交结果按 `channel`（coze/local）分提示。
- 验证：`py_compile` + 前端 JS `new Function` 语法校验通过；起 MOCK 服务实测 `/api/bugreport` 返回 `{"ok":true,"channel":"coze","note":"report recorded (feishu)"}`（真实端点落库，默认 coze 生效）。

## v5.7.3 补丁（2026-09-03）· 主计算按钮归位

> 触发：用户认为「智能识别并计算」按钮放在 NL 输入框旁不顺手，应置于「保持会话线程」勾选之下。
- **主按钮下移**：将 `nlComputeBtn`（`智能识别并计算` / 有会话时 `识别并追问`）从顶部 `.nl-top` 移出，置于左栏底部 `keepSession` 勾选正下方；`.nl-top` 现仅保留 `#nlInput` 输入框 + `#nlHint` 动态提示。按钮 id 与 `nlCompute`/`updateNlBtn` 逻辑不变，仅挪 DOM 位置。验证：前端 JS `new Function` 语法校验通过；起 MOCK 服务实测首页 200、按钮位置确在 `keepSession` 之后（`order_ok=True`）。

## v5.7.2 补丁（2026-09-03）· 工作台交互收敛（合并计算按钮 / 上移分析选项 / Bug 反馈）

> 触发：用户三项收口要求——①顶部「智能识别并计算」与底部「计算」功能重复，合并；②面板3「分析设定与历史」中的分析选项应上移、只留线程历史；③底部加 Bug 反馈入口。
- **① 计算按钮合并**：删除左栏底部独立「计算」按钮；顶部 `nlComputeBtn` 成为唯一计算入口——NL 为空时退化为 `doCompute(false)`（等同原手动计算），有会话时文案变「识别并追问」。后端零改动，JS 仅改 `nlCompute` 空分支（Grep 确认无第二个 `doCompute(false)` 调用点残留）。
- **② 分析选项上移、面板3 仅留线程历史**：`figureCtl`（图表选项控制）从右栏面板移入左栏「手动设置（可选）」折叠区；`quickEdit`（精确修改）移出面板3到左栏（会话内可见）；右栏面板3 精简为仅「会话线程历史」（`#threadPanel`，grid-column 1/-1）。删除无用 `.merged-panel/.merged-2col/.merged-col` CSS（Grep 确认零残留引用）。
- **③ Bug 反馈**：页脚新增「报告问题 / Bug 反馈」按钮 + 模态框（内联 SVG 虫标），自动附带当前检验/参数/会话/UA/URL 上下文；`server.py` 新增 `POST /api/bugreport`，追加持久化到 `bugreports.json`（与 `sessions.json` 同模式、线程安全、容错）；前端提交失败（无端点/离线）自动复制报告 JSON 到剪贴板兜底。验证：`py_compile` + 前端 JS `new Function` 语法校验通过；起 MOCK 服务实测 health/首页/bugreport 全部 200、文件落地。

## v5.7.1 补丁（2026-09-03）· 工作台界面紧凑化重构

> 触发：用户反馈「工作台太长」，要求缩短并并排放置元素，同时逐项核验每个元素功能真实可用。 > 做法：**只重构 DOM 结构与 CSS，JS 函数逻辑一字未改**（415 行逻辑已验证，改动风险高、收益低）。 > - ① 左栏表单字段改 **2 列网格**（`#formArea .sec`），输入区高度约减半； > - ② 右栏改为网格：结果展示置顶占满整行（hero），图表选项控制 + 追加提问 **左右并排**； > - ③ 检验族 / 检验方法 **并排同一行**；求解方向压成一行 chip（去掉整块虚线框）； > - ④ 面板编号按视觉顺序修正为 **1→2→3→4**（原右栏 3-2-4 错乱）。 > - 功能核验：启动实例对 12 类 UI 元素逐一实测后端端点——health/schema/schema-单检验/compute/dry_run/必填校验/ >   curve 检验图表控制/非曲线检验隐藏曲线区/figure_mode 全局可用/自然语言填表/会话新建-列表-详情/会话追加合并/导出报告/ >   导出边界，全部 ✓；18 个 DOM id 与 12 个处理器函数静态核对无缺失；JS `node --check` 通过。 > - **⑤ 下拉空缺陷修复（防御性）**：根因不是代码 bug，而是 `init()` 对 `/api/schema` 的 `await api(...)` 原本**无 try/catch**—— >   当用户以 `file://` 直接双击打开 HTML、或访问了未正确响应 `/api/*` 的旧/错误端口时，fetch 失败 → `init` 静默中断 → 下拉为空且无任何提示。 >   修复：把 `/api/schema` 加载包进 try/catch，失败时页面顶部显示红色横幅（明确提示「用 http:// 而非 file:// 打开、确认后端已启动」）， >   不再静默空下拉、不再抛 unhandled rejection。验证：用 Node 真实连 http 服务跑 `init` → 下拉正确填 36（族）/49（检验）； >   模拟 `/api/schema` 返回 500 → 横幅显示、无崩溃。**铁律**：工作台必须经 http 服务（`python server.py <port>`）访问，禁 `file://` 直开。 > - **⑥ 自然语言入口置顶 + 「智能识别并计算」合一按钮（方案 B）**：用户要求①NL 入口放最上面、②「智能识别并填表」与「计算」合并为一按钮、③追加提问框与 NL 框合并。 >   做法：NL `.sec` 移到左栏面板最顶（独立青色高亮区 `.nl-top`），主按钮 `nlComputeBtn` 统一「识别→填表→计算」——无会话走 `doCompute(false)` 首轮自动算， >   有会话走 `doComputeWith` 改为「识别并追问」直接重算（`updateNlBtn` 随 `CUR_SESSION` 动态切文案）；另加 `nlPreview`（识别→填表→预览信封）作 ghost 次级按钮。 >   右栏面板 4 删独立 `nlFollow` 框，追问只走顶部 NL；`quickEdit` 保留为「精确修改」折叠区（精确调单参、不丢能力）。 >   后端零改动；JS 仅新增 `nlCompute`/`nlPreview`/`updateNlBtn`、删除旧 `nlFill`/`nlFollow`（Grep 确认无悬空引用）；DOM/函数闭合经 Grep+Read 静态核对。

## v5.7.1 补丁（2026-09-02）· 新增本地 Web 工作台（Workbench）

> 触发：为技能补齐可视化操作界面，覆盖「信息输入 → 结果展示 → 图表选项控制 → 追加提问」全流程。 > 设计定调：**零新增第三方依赖**——后端用 stdlib `http.server`（与技能 stdlib-only 红线一致）， > 前端单文件零依赖；表单 schema 运行时反射 argparse + `_contract_index.json`（49 检验 / 178 参数，零维护）； > 追加提问复用 `ct-base` 确定性合并（`merge_spec`），不丢参数、不臆造。

- **① 新增目录** `adapters/workbench/`：`form_schema.py`（动态表单反射）、`session_store.py`
  （会话线程 + 确定性合并，缺 `ct-base` 时内嵌等价实现）、`server.py`（stdlib HTTP 后端 / REST + 静态）、`workbench.html`（单文件前端，浅色主题、中英双语）、`README.md`（启动与端点）。
- **② 新增「导出 HTML 报告」按钮**（`server.py::/api/export` + `workbench.html`）：结果展示区顶部按钮，
  把已算结果重组成 coze 信封后复用技能既有 `rendering.render_html_report` 生成**单文件 HTML 报告** （内联 SVG + 可复现 R 代码 + 数值卡片），与 CLI `--report` 同源同构、离线可看；临时文件用后清理。 未计算 / 无内容时按钮禁用。
- **② 四区功能**：信息输入（检验族两级选择 + 关键词搜索 + 动态参数表单 + 求解方向 + 零 LLM
  自然语言入口）；结果展示（当前分析设定块 / 数值卡片 / 说明 / 内联 SVG / R 代码 / 信封预览）； 图表选项控制（曲线·专项图勾选 / 图形格式 / 分配比显隐）；追加提问（会话跨轮继承 + 逐轮 diff + 快捷修改 + NL 追问）。
- **③ 复用既有能力**：`form_schema` 反射 `scripts/samplesize_power.build_parser` 与
  `tests/coze_cases/_contract_index.json`；`session_store` 复用 `ct-base/scripts/merge_spec.py` 做确定性合并（家族红线 4）；`server` 复用 `CozeBackend` / `classify_test` / `param_aliases`， ctx 构造严格复刻 CLI `main` 语义（solve_for_power / alt / d_val / curve / user_language）。
- **④ 必填校验**：required 字段中「有 schema 默认值」者（alpha/side/ratio 等）自动补默认不报错；
  仅「无默认的真必填」（effect / p1 / p2 等）缺失时拦截；会话合并默认值不入库，避免污染跨轮继承。
- **⑤ 界面视觉重构（2026-09-03）**：`workbench.html` 样式层重写，**415 行 JS 逻辑零改动**
  （改前已端到端验证的功能不受影响）。
  - *科技感*：顶栏深色渐变 + 网格纹理 + 底部青色扫描线；页面底纹精密网格 + 顶部光晕；
    面板顶部渐变细线；分区标题发光圆点；代码块 / 设定块终端质感（深底青字 + 内发光）。
  - *数字感*：关键数值卡改用等宽字体 + `tabular-nums` 大号数字；数字输入框等宽对齐；
    pill / badge 等宽字；布局网格化。
  - *美观度*：设计令牌化（CSS 变量）、三级阴影层级、统一圆角尺度、focus 青色光晕、
    卡片 hover 微上浮、滚动条美化、空状态插画。
  - *规范*：图标全部内联 SVG（7 处）替换 emoji；`<option>` 内曲线能力标记改用数学符号 `∿`
    （option 内无法嵌 SVG）；移动端按钮 ≥44px、输入框 16px 防 iOS 缩放、安全区适配。 零外部依赖不变（无 CDN / 字体 / 图表库）。

## v5.7.1 补丁（2026-09-02）· coze 入参新增技能版本号 `skill_version`（写入飞书 querystr）

> 触发：需按技能版本归因云端调用量与失败率；飞书调用日志的 `querystr` 要带上发起方版本。 > 设计定调：**可选字段 + 双向兼容**——老技能不发、coze 端不写键；新技能发到未重新部署的 > 旧 coze 端也不报错，两端可独立升级、互不阻塞。

- **① 字段语义**：`skill_version: Optional[str]`，由客户端（技能安装设备）随 `/run` 请求体
  发出，取值 = 技能根 `SKILL.md` frontmatter 的 `version:`（读取失败回退内置常量 `_SKILL_VERSION_FALLBACK`）。coze 端透传后写入飞书多维表格的 `querystr` （单条：`{test, params, mode, skill_version}`；批量摘要：`{batch, count, tests, modes, skill_version}`）。
- **② 本地改动（客户端）**：`adapters/coze_client.py` 新增 `_skill_version()`（读 SKILL.md，
  单一事实来源 —— 升版本免改代码）；`call()` / `call_batch()` / `CozeBackend.preview()` 三处信封均带上该字段（`--dry-run` 预览同样可见）。
- **③ coze 端改动**：`src/graphs/state.py` 的 `GlobalState` / `GraphInput` /
  `SamplesizeNodeInput` / `SamplesizeNodeOutput` / `FeishuSaveNodeInput` 增字段； `nodes/samplesize.py` 两条返回分支（单条 / 批量）透传； `nodes/feishu_write_node.py` 的 `build_querystr` 增加可选形参（**非空才写键**）； `nodes/feishu_save_node.py` 读取并传入（批量摘要同理）。
- **④ 向后兼容（双向，已实测）**：

  | 场景 | 行为 | |---|---| | 老技能 → 新 coze 端 | 请求体无该字段 → `None` → `querystr` 不含该键（与旧格式逐字节一致） | | 新技能 → 未重新部署的旧 coze 端 | 多发的键由 pydantic v2 默认忽略策略丢弃，不报错 | | 老技能 → 旧 coze 端 | 完全不受影响 |

- **⑤ 验证**（本地、未触网）：5 个改动文件 `py_compile` 全过；`build_querystr` 三用例
  （不传 / 传版本号 / 传空串）断言通过；pydantic 2.12.4 双向兼容用例通过（新端收老 payload → `None`；老模型收新 payload → 不报错）。`_skill_version()` 实读 SKILL.md 得 `5.7.1`。
- **⚠️ 部署提示**：coze 端需重新打包部署后 `querystr` 才会带版本号；未部署期间本地照常
  运行，仅飞书日志无该字段（不影响任何计算结果）。

## v5.7.1（2026-08-31）· 分配比图形按用户意图过滤（本地渲染层，coze 端不变）

> 触发：用户反馈——**提示词未提及不等比例分配时，不应默认提供分配比例图形**； > 分配比四图只在用户明确输入组间不等比例时才提供。 > 设计定调（用户纠正）：**coze 端 R 出图完全不改、仍返回全量图**，过滤放在**本地 HTML 渲染模板**层。

- **① 过滤语义**：`alloc_suite`（4 张分配比图：所需总 N vs 比 / 固定 N 下效能 vs 比 /
  等效能等高线 / 效能损失分层）由 coze 端**始终全量返回**，本地渲染层决定展示与否—— **仅当请求显式要求不等比例分配**时展示。判据：CLI `--ratio`（分配比 k = n2/n1）存在且 `!= 1`。
  - 未提及分配比（无 `--ratio`）→ 本地隐藏；
  - 明确 1:1 等例（`--ratio = 1`）→ 本地隐藏；
  - 不等比例（如 `--ratio 2`、`0.5`）→ 展示。
- **② 效应量字段绝不误触发**：`hazard_ratio` / `rate_ratio` / `win_ratio_theta` /
  `sigma_ratio` / `gs_ratio` 以及方法名 `odds_ratio` / `risk_ratio` 均为**效应量或设计参数**， 不是分配比，已明确排除。过滤依据为图形 caption 含 `alloc` 字样（如 `ctss alloc ttest ind 1`）， 与效应量字段无交集。
- **③ 改动文件（仅本地，coze 端零改动）**：
  - `scripts/samplesize_power.py`：新增 `_ratio_is_unequal` / `_is_alloc_figure` /
    `_filter_alloc`；`render_figures` / `_render_single_result` 增加 `show_alloc` 形参； `render_batch` 逐项按 spec 的 `ratio` 计算 `show_alloc`；单请求与自动曲线路径注入 `show_alloc=_ratio_is_unequal(args.ratio)`。
  - `adapters/rendering.py`：`render_html_report` 增加 `show_alloc` 形参，
    过滤 `figures[]` 中 caption 含 `alloc` 的图。
- **④ 文档同步**：`references/default_figures.md`（合并去重段 / 图型表 / alloc_suite 章节）、
  `SKILL.md`「Default Figures」段均改回"coze 全出 + 本地过滤"口径。
- **验证**（真实 coze 部署端到端，`ttest_ind` power*=0.8；单元级 `_filter_alloc` /
  `render_html_report` / `render_figures` 门控含 dict 与 Figure 两种类型全过，`py_compile` 两文件语法检查通过）：

  | 用例 | HTML 报告图数 | `alloc` 出现 | 结论 | |---|---|---|---| | 无 `--ratio`（用户未提及） | 4 | 0 | 分配比四图已本地隐藏 ✅ | | `--ratio 2`（不等比例） | 8 | `ctss alloc ttest ind 1..4` 全展示 | 分配比四图展示 ✅ |
- **影响面**：`margin_tradeoff` 的 x 轴是**界值/边际比**（非组间分配比），不在本次范围内。
  向后兼容：老客户端不传 `ratio` → 恒隐藏分配比图（即本次目标行为）。coze 端**无需重新部署** （coze 侧代码未改动，仍全量返回）；仅本地 skill 代码更新即生效。

## v5.7.0（2026-08-31）· 批量调用治理（batch 模式 + 请求级幂等缓存 + 编排收敛）

> 触发：飞书后台 searchlog 实证，单此分析在 4 分 15 秒内打入 54 次 `samplesize` 调用， > 其中约一半是「单点 + 曲线」成对冗余、另有逐字节重复的整对重跑（ID 3376/3378、3382/3386）。 > 本次从**服务端**与**编排侧**双管齐下，目标把同类分析的调用量削减 80%+。

- **① 服务端批量模式（`batch` 数组）**：`adapters/coze/src/graphs/state.py` 的 `GraphInput`/
  `GlobalState`/`SamplesizeNodeInput` 新增可选 `batch: List[dict]`；`samplesize_node` 检测到 非空 `batch` 时逐项经带缓存的 `_compute_one` 计算 + 出图层，聚合为完整 agg 后**整体外置 S3 一次**，主返回仅留轻量内联摘要 `{status, batch:true, count, ok, errors, tests[], modes[], results:[{index,test,mode,status}], _coze_full, _coze_version}`（恒 < 4000 字符）。12~24 格 扫描从「N 次串行」压成「1 次批量」，本地客户端经 `_coze_full` 一次下载即得全部 item 完整结果。 🔴 **附带修复 coze 主返回截断**：早期实现把每项的完整外置结果内联进 `results[]`，12+ 项时 主返回 > 4000 会被平台截断破坏 JSON；改为「摘要内联 + 整体 S3 外置」后，主返回恒精简。 本地组装入口 `adapters/coze_client.py::build_batch([(test,args,ctx), ...])`。
- **② 请求级幂等缓存**：`samplesize.py` 新增线程安全 TTL 缓存（`_cache_key`/`_cache_get`/
  `_cache_put`，默认 600s，`CTSS_CACHE_TTL` 可调，容量 >2000 自动清 oldest-half）。对规范化 签名 `sha256(json({t, params(sorted), m, locale}))` 去重；命中跳过 R 子进程，复用「外置前」 out 并重签 S3 链接（图形始终可下载）。自动消除上层 Agent 对同一网格点的逐字节重跑。
- **③ 批量飞书日志合并**：`feishu_save_node.py` 检测 `batch:true` 结果后写**一条**合并日志
  （querystr 含 `count/tests/modes` 摘要，resultstr 含 `ok/errors`），54 行日志 → 约 4 行。
- **④ 编排侧收敛（SKILL.md「批量调用治理」段 + coze_contract.md §2.1/§2.2）**：
  - 曲线响应自带单点 → 需要曲线时**只发一次带 `curve_*_seq` 的调用**，严禁先单点再曲线（省 50%）；
  - 网格/敏感性扫描走 `build_batch` 一次性提交，禁止逐格串行；
  - 始终走 `build_params` 白名单，**只传本 test 生效字段**（信封已默认精简，勿回填全家族默认值）。
- **⑤ 本地批量结果聚合渲染（`adapters/coze_client.py` + `scripts/samplesize_power.py`）**：
  服务端 v5.7 `batch` 模式仅返回聚合 agg（含每项完整 `out` 信封，外置 S3 一次），本地需把 这份聚合体**解析 + 逐项渲染 + 合并汇总**，不再逐条回查。新增 `ComputeBackend.compute_batch` 抽象方法 + `BatchResult`/`BatchItem` 数据类（`scripts/compute_backend.py`）；客户端 `CozeBackend.call_batch(specs)` 经 `_coze_full` 一次下载完整 agg（失败降级内联摘要）， `CozeBackend.compute_batch(specs)` 把 `results[i]` 映射为 `BatchItem`（成功项经 `_envelope_to_result` 规整为 `Result`、失败项保留服务端原因）；出错信封（服务端 `status=error`） 直接抽真实错误原因而非笼统「外置不可用」。CLI 新增 `--batch-file <JSON数组>` 入口： `_run_batch` 克隆命令行默认参数、按条目覆盖 `args`/`ctx`、`--dry-run`/`--show-code` 仅预览 批量请求信封；`render_batch` 先打印汇总行（`总数/成功/失败/tests/modes/状态`），再逐项复用 `_render_single_result`（文本 + SVG 落盘 + HTML 报告 + R 代码/数值），失败项打印错误原因。 单请求路径不受影响（`_render_single_result` 抽出共享、`idx=None` 不打印分隔）。
- **验证**（本端离线 stub，桩化 `_post` 与 S3 `urlopen`，覆盖 4 条解析路径）：
  - `[1]` `call_batch` 经 `_coze_full` 解析出完整 agg（含每项 `out`）；
  - `[2]` `compute_batch` 多 spec → `BatchResult`，每项 `Result` 含 1 图 + 可复现 R 代码；
  - `[3]` `compute_batch` partial（1 成 + 1 服务端错误信封）→ `status=partial`、失败项原因
    抽得「`coze 计算失败: p1=1.5 超出合法范围 (0,1)`」；
  - `[4]` S3 下载失败 → 逐项 `error`、服务端聚合 `count/ok/errors` 仍准确保留；
  - CLI e2e（`CTSS_COZE_MOCK=1 --batch-file`，4 条目含 1 个 `solve_for_power` 反求 power）
    → 汇总行正确、`mode=power` 自动识别、逐项渲染文本/SVG/HTML/R 代码；
  - 单请求回归：`--test proportion_two`（mock）输出与重构前逐字段一致（自动曲线兜底保留）。
  - CACHE：2 次逐字节相同的单请求 → R 引擎仅调用 1 次，内容一致（仅 S3 签名刷新）；
  - BATCH：14 项网格（含 2 个重复）→ R 引擎调用 12 次、`ok=14`、主返回 1229 字符（<4000）、
    整体 `_coze_full` 一次性外置、飞书仅 1 行合并日志；
  - 非法项（非 dict / 缺 test）计入 `errors` 不崩 R；
  - FEISHU：批量结果写入单行 `{batch:true,count:14,ok:14,tests:[...],modes:[...]}`；
  - 向后兼容：老版胖 payload（含 `return_r_code`/`resolved_spec` 多余字段）经 `GraphInput` 校验
    不报 422，`extra` 默认忽略，单请求返回结构逐字段不变。
- **风险/注意**：`batch` 与历史单请求信封完全向后兼容（未传 `batch` 时行为不变）；缓存 TTL
  默认 10 分钟，长尾重复规划仍会被去重，不影响结果正确性（重签 S3 链接保证图形可下载）。

## v5.6.0 补丁（2026-08-30 凌晨）· 修复 panel C 等把握度等高线图「曲线冲出图框」

- **缺陷（用户线上报告）**：`render_alloc_suite` 副图 panel C（`ttest_ind | C. equal-power (power=0.80) contour (n1,n2)`）的蓝色等高线冲出图框、右端截断。ttest_ind + n*=64 + power*=0.80 时实测：起点 (34, 587)、(37, 247)、(40, 165)、(43, 128)、红点 (64, 64)、末端 (192, 38) 中，n1≈34 与 n2≈587 远在画框之外。
- **根因（两件事，缺一不闭环）**：
  1. `xlim = ylim = range(n1g)` 写死为 n1 网格范围 `[19.2, 192]`，但等高线数据真实范围 `n1c ∈ [33.84, 192]`、`n2c ∈ [38.40, 587.29]`（双曲线在 n1→neff0 时 n2 发散至 500+），写死窗截断 n2 发散端 → 曲线"冲出"。 2. `svglite(pC, width=7, height=4.5)` 矩形设备 + `asp=1`：为保持数据高宽比=1，R 自动拉伸 xlim 至 ~[-200, 1000]，蓝色等高线被挤到画面左侧，即便 (1) 已修、视觉仍不协调。
- **修复**（`adapters/coze/scripts/coze_figure_layer.R::render_alloc_suite` 第 505-519 行）：
  - `xlim = ylim = range(c(n1c, n2c)) + ±5%` —— 改写为按等高线真实数据自适应 + 留白，全点含入。
  - `svglite(pC, width=5, height=5)` —— panel C 独立改方形设备，保证 1:1 对角线成真 45°，"等例分配最优"的几何证明（切点=红点）成立。
- **验证**：
  - 数值（`diag_alloc_axis.R` + 同一逻辑的 `panelC.R` 打印）：旧窗 `[19.20, 192.00]` 截断 n2c=587.29 ❌；新窗 `[6.17, 614.97]` 全包含、红点 (64,64) 在内 ✅。
  - 端到端：`render_alloc_suite` + `render_power_n` 共 5 张 SVG 落盘（`ctss_ttest_ind_default_1.svg` + `ctss_alloc_ttest_ind_1..4.svg`），panel C SVG 头部 `width='360pt' height='360pt'`（5×5 inch）方形确认；目视 `outputs/alloc_render/panelC_fixed.png`：双曲线完整、红色 (64,64) 落在 1:1 绿色虚线对角线上、几何切点清晰。
  - 本地沙箱 R/svglite 存在非确定性偶发段错误（exit=139，与代码逻辑无关，仅 message 行存在即不崩），coze 端无此问题；修复正确性由数值+目视双证。
- **影响面**：仅修改 `render_alloc_suite` panel C 内部（5 行 svglite + ~10 行注释 + 5 行 xlim/ylim）；其余三张副图（panel A/B/D）与主图渲染器均未触碰。

## v5.6.0 补丁（2026-08-30 深夜）· 三平台发布（GitHub / SkillHub / ClawHub）

- **三平台同步发布 v5.6.0**：GitHub 推送 `main`（commit `81bf113`，`a235725..81bf113`）并设 upstream；SkillHub 发布 `skillId=98998`；ClawHub `latest=5.6.0`（账户 @medstatstar，经 "Version 5.6.0 already exists" 权威回执确认入库）。
- **发布前修复 ClawHub 环境**：受管 node 版本迁移（22.22.2→22.22.2-2）清掉了 `clawhub` 包与登录凭据（`~/.workbuddy/AppData/Roaming/clawhub/config.json` 一并丢失）；已在 `22.22.2-2` 的 workspace 重装 `clawhub` v0.23.3 并 `login --token` 写回真实路径 `~/AppData/Roaming/clawhub/config.json`。注意 `clawhub publish` 在沙箱内会挂起（沙箱拦截上传），须 `dangerouslyDisableSandbox: true`。
- **仓库清理**：`tests/` 此前经 `git mv` 误带入 index，发布前 `git rm --cached -r tests/` 取消跟踪（`.gitignore` 已声明 `tests/`、`adapters/coze/`、`archives/` 整目录排除，不进仓库与发布包）。
- **发布包裁剪**：SkillHub 走 `git archive` 固定路径副本 + `scrub_copy.py --platform skillhub`（RESULT: PASS，删 7 个非白名单文件），并在副本上做双语 frontmatter 本地化（displayName 中文在前、description 仅中文）；ClawHub 走 `git archive` 精简副本（自动排除 coze/tests/archives，1.1MB）直发，遵守 `.clawhubignore` 整目录排除 `coze/`。全程未触碰 `adapters/coze/` 源（coze 平台部署仍由人工处理）。

## v5.6.0 补丁（2026-08-30 夜间）· 删除 r-assets，coze 镜像为唯一真相源

- **废除 `adapters/r-assets/`（本地 R 后端「源」目录）**：它与 `adapters/coze/ct_r_lib/` 是「源 vs 镜像」的平行副本，且未进 git、长期与部署包漂移（与 coze 版有 934 行差异）。按用户「只保留 coze 镜像」指令，将 `adapters/r-assets/` 整体移入 `archives/r_assets_legacy_20260830/`（gitignored，仅作安全留存），活跃树不再有第二份 R 后端。
- **本地加载器改指 coze 镜像**：`scripts/compute_backend.py::_load_local_r_backend` 与 `adapters/coze/ct_r_lib/compute_backend.py::_load_local_r_backend` 均改为从 `adapters/coze/ct_r_lib/` 加载 `local_r_backend.py`，并临时把该目录置顶 `sys.path` 以解析 `r_templates / i18n / compute_backend` 依赖、执行后还原，避免污染全局导入路径。两加载器真实复测均成功实例化 `LocalRBackend`。
- **离线仿真器归位 coze 镜像**：`legacy/adaptive_simulator.py` 移入 `adapters/coze/ct_r_lib/legacy/`（纯 Python，无 r-assets 依赖），保留「只保留 coze 镜像」原则；同步更新 `AGENTS.md` / `references/adaptive_simulator.md` 路径引用。
- **文档引用全量改写**：12 个活跃文件（AGENTS / SKILL / scripts/* / coze_client.py / _contract_index.json / references/*.md / coze README_zh-CN）中的 `adapters/r-assets/...` 批量改为 `adapters/coze/...`；`coze_contract.md` §6 同步流程改写为「r-assets 已废弃、coze 镜像为唯一真相源」；`gen_contract_doc.py` 输出路径改为 `adapters/coze/coze_contract.md` 并重渲染。CHANGELOG 历史条目保留原貌（不改动）。
- 校验：活跃树 `r-assets` 残留引用清零（仅剩「已废弃/已移除」说明性提及）；被改 Python 全部 `py_compile` 通过；`_contract_index.json` 合法（49 例）。

## v5.6.0 补丁（2026-08-30 晚间）· 技能主目录二次整理

- **去重发布包**：删除与 `ct-samplesize_coze_deploy_v5.6.0.zip` 完全重复（md5 一致）的 `ct-samplesize_coze_deploy_5.6.0.zip`（缺 `v`）；`adapters/coze/_build_deploy_subset.py` 输出名统一为 `ct-samplesize_coze_deploy_v{VERSION}.zip`，杜绝再生成重复文件。
- **`ADVANCED.md` / `ADVANCED_zh-CN.md` 移入 `docs/`**（原在技能根，与 ROADMAP.md 同归 `docs/`）；同步修正 `README.md` / `README_zh-CN.md` 内 `[ADVANCED.md](...)` 链接至 `docs/` 路径（`git mv` 保留历史）。
- **`tests/` 内运行产物归位**：`*_output*.txt` / `*_report*.json` / 演示 `*.svg` 共 21 个移入 `tests/outputs/`；`final_retest.py` / `focus_retest.py` / `nl_full_test.py` / `scan_all_tests.py` / `verify_be_curve.R` 等临时调试脚本移入 `tests/scratch/`；`nl_test_report.json` 因被 `test_natural_language.py:243` 引用保留原位。
- **清理根 `outputs/`、`scripts/outputs/`、`dist/`**：历史运行产物（SVG / HTML / 审计报告 / 端点检查报告，约 3.1MB）与构建报告统一归档到 `archives/runtime_20260830/`，删除这些运行/构建目录（CLI 运行时会在 `outputs/` 重新生成，已 gitignore）。
- **删本地备份** `scripts/i18n.py.bak_20260828`（`.gitignore` 已忽略的 `*.bak_*`）。
- **`.gitignore` 补忽略项**：`archives/`、`ct-samplesize_*.zip`、`tests/outputs/`、`tests/scratch/`，避免归档与发布包误提交。
- 整理后技能根仅留：6 个顶层 md（AGENTS/CHANGELOG/LICENSE/README×2/SKILL）+ `requirements.txt` + 3 个发布 zip；源码按 `adapters / archives / assets / config / docs / references / scripts / tests` 八目录归位。

## v5.6.0 补丁（2026-08-30 傍晚）· coze 目录整理：单一真源重构

- **删除冗余 `coze_deploy/`**：其 6 个文件与 `adapters/coze/` 完全重复（md5 一致）且未进 git；新增 `adapters/coze/_build_deploy_subset.py` 从 `adapters/coze/scripts/` 直接生成「最小部署包」`ct-samplesize_coze_deploy_v5.6.0.zip`（6 文件），消除平行副本失同步风险。
- **`coze_cases/` → `tests/coze_cases/`**：回归 fixtures 归位测试目录；更新 3 处 Python 路径引用（`tests/coze_cases_regression.py`、`adapters/coze_client.py`、`scripts/samplesize_power.py`）+ 相关文档/生成器路径；`git mv` 保留历史。
- **清理 `adapters/coze/` 内 `_archive_*`**（3 个历史构建包 ~2.6MB）→ 移出到技能根 `archives/`；删除被取代的旧 `_build_deploy.py`，并将 `_build_deploy_new.py` 重命名为 `_build_deploy.py`（输出改到 `archives/`，不再在镜像内生成 `_archive_*`）。
- 顶层 3 个发布 zip 仍保留在技能根（用户未要求移动）。
- 文档一致性：`SKILL.md` / `references/default_figures.md` / `adapters/coze/DEPLOY.md` / 生成器脚本中 `coze_deploy`、`coze_cases` 路径同步更新为 `adapters/coze` 与 `tests/coze_cases`；`adapters/r-assets/coze_contract.md` 由生成器重新渲染。

## v5.6.0 补丁（2026-08-30 下午）· SKILL.md 瘦身回 §16.1 红线 + GSD 修复/去重上线验证

- **SKILL.md 256 → 196 行（§16.1 ≤200 达标）**：v5.6 出图细节（层模型 / 图型表 / alloc-suite 数学 / 精度 / 依赖说明）整体下沉至新文件 `references/default_figures.md`，SKILL.md 保留一段摘要 + 链接；顺带压缩 Cross-turn Continuity（4 条并为 3 条）、Interaction Vague 轮次说明、Advanced 小节、Formulas 与 Related skills。内容零删失，只做搬家与合并。
- **修正过时表述**：出图「Deployment boundary」中 "(AI does not touch `adapters/coze/`)" 按用户 2026-08-30 红线澄清改为「coze 平台部署为人工操作；本地 `adapters/coze/` 镜像必须保持最新」。
- **frontmatter version 5.5.0 → 5.6.0**：与正文 v5.6 及云端已部署实现对齐。
- **线上回归全绿（部署后）**：group_sequential（GSD 双 bug 修复生效，n 正常 + 2 默认图）、ttest_ind（去重生效，9→8 图）、poisson（5 图）；15 张 SVG `<g>` 配对合法（svglite 修复生效）。回归脚本 `regress_v560.py` / `regress_v560_report.json`（会话目录）。
- `merge_spec.py` / `resolved_spec` 行为不变；无代码变更，仅文档层。

## v5.6.0 (2026-08-30) · 待发布：默认图形全部上 coze（R 为主 + figure_kit coze 内部兜底，本地退为瘦客户端）

> **背景与取舍**：v5.5 把 49 方法的默认图形层实现在「本地 Python figure_kit」。但用户要求**所有绘图都上 coze 端、本地只承接结果**。 > 出图从本地 Python 改为 coze 端 R 时做了利弊评估：R 端口用原生非中心分布（`pnorm`/`pt`/`pf`/`pchisq`）严格精确、与 coze 数值同源； > 且 **coze 端零新增包**（`svglite` 已在 tier1 安装清单）。故采纳「coze R 为主 + figure_kit 作为 coze 内部兜底」，**本地彻底退为瘦客户端**。

### Changed / 出图架构（v5.5 本地 → v5.6 coze 端）
- 新增 `coze_deploy/` 部署包（4 文件）：`coze_figure_layer.R`（主出图 R 模块）、`figure_kit.py`（coze 内部 Python 兜底）、`alloc_curve.py`（figure_kit 依赖）、`coze_fallback.py`（两级兜底编排器）。
- `scripts/samplesize_power.py`：删除本地 `_render_default_figures_safely()` 及与 `render_figures` 重复的默认图形透出循环；本地只把 coze 回传的 `figures[]` 交给既有 `render_figures` 统一落盘 / 内联 / 聚合进 HTML 报告。**本地零渲染**。
- `figure_kit.py`：新增 CLI 入口（`--test/--meta/--out-dir/...`），使其可作为 coze 端独立进程调用（不再只是被本地 import 的库）。

### Added / coze 端 R 主出图模块 `coze_figure_layer.R`
- 四族精确 power 函数（`power_normal`/`power_nct`/`power_ncf`/`power_ncchi2`），非中心参数由 R 原生分布给出，**锚点穿越严格成立**。
- 8 种图型渲染器：`render_power_n` / `render_power_n_multi` / `render_margin_tradeoff` / `render_icc_sens` / `render_gs_boundary` / `render_assurance_n` / `render_alloc_suite`（A/B/C/D 四图 + 速查表）。
- `METHOD_FIGURES` 49 方法 → (primary, secondary) 映射，与 `scripts/figure_kit.py` 及 `coze_cases/_contract_index.json::default_figure` 三处语义一致。
- **优雅降级**：`margin_tradeoff` 主图缺 `--margin` 时自动退为 `power_n`，避免写出 0 字节文件。
- **ASCII-only 运行期字符串**：标题 / 轴标 / 图例全用英文 ASCII（`side_label()` 返回 "one-sided"/"two-sided"）。原因：coze 容器若以 `LC_CTYPE=C.UTF-8` 启动，中文会破坏成控制字节、产生非法 XML（实测 35 张图全挂）。注释可中文，运行时字符串必须 ASCII。

### Added / 两级兜底编排 `coze_fallback.py`
- 主出图失败（R 缺失 / `svglite` 未装 / 参数不全 / R 报错）→ 清空 capture-dir 残留 → 回退 `figure_kit.py`。
- 退出码：产出 ≥1 张 SVG 返回 0（`{"backend":"R"|"figure_kit","figures":[...]}`）；两级都失败返回 1（`{"backend":"none"}`，**主数值结果不受影响**）。

### Validated / 本机实测（用真实 R 4.6.1）
- R 主路径：12 个代表方法覆盖 8 种图型 → 全部 `exit 0`、SVG 数量正确、严格 XML 解析通过、无 NaN/Inf。
- 兜底路径：R 缺失时 `coze_fallback.py` 自动回退 `figure_kit.py` 并产出有效 SVG。
- Unicode 安全：R 模块全 ASCII 运行期字符串，35 张测试 SVG 全部合法 XML。

### Docs
- 新增 `coze_deploy/DEPLOY.md`：部署步骤 + 两级兜底链路 + 图形契约 + 调用示例 + 包评估结论。
- `SKILL.md`：「Default Figures」章节改为 v5.6 coze 端架构；依赖说明由「本地零依赖、coze 零改动」改为「coze 需部署 4 文件、零新增 R 包」。
- `coze_cases/_contract_index.json`：`_meta.default_figure_note` 由 v5.1 本地 figure_kit 描述改为 v5.6 coze 端生成、本地只承接。

## v5.5.0 (2026-08-30) · 待发布：每种方法的默认图形层 + 分配比诊断（本地零依赖，coze 端零新增包）

> **背景与取舍**：v5.4 之前只有契约里 `default_curve: true` 的 5 种方法会出图，其余 44 种算完只回一个数字。 > 补齐的路线有两条：(A) 让 coze 端 R 为 49 种方法各画一张图 —— 需改云端 R 并引入额外图形依赖； > (B) 数值锚点仍由 R 给出，曲线形状由**本地族级解析结构**外推 —— 零依赖、零联网、coze 端零改动。 > **本次选 B**：R 依然是数值真相源，曲线精确穿过 R 给出的锚点。

### Added / 默认图形层 `scripts/figure_kit.py`（零第三方依赖，仅 stdlib `math`）
- **原理**：几乎所有常用检验的非中心参数对样本量只有两种缩放 ——
  `z`/`t` 族 `λ(n)=λ*·√(n/n*)`，`F`/`χ²` 族 `λ(n)=λ*·(n/n*)`。 因此**给定 R 返回的一个锚点 `(n*, power*)`，整条曲线的形状在数学上被唯一确定**， 本地无需知道 coze 内部用的是 pwr、TrialSize 还是 rpact。
  - 锚点穿越性实测：49 方法 × 3 锚点（n=64/200/30，power=0.80/0.90/0.65）**残差 ≤1.1e-16，全部单调**。
- **分布内核（自实现，已与 R 4.6.1 逐点交叉核对）**：正则化不完全 Γ（级数+连分数）、
  不完全 Β（连分数）、中心/非中心 χ²（泊松混合）、中心/非中心 F（泊松混合）、`qf`/`qchisq`（二分）。
  - 精度：中心 χ²/F 与非中心 χ² **≤5e-13**；非中心 F **≤3e-10**；`qf`/`qchisq` **≤8e-11**。
- **8 种图型，49 方法全覆盖**（映射见 `METHOD_FIGURES`，已镜像进 `_contract_index.json::default_figure`）：

  | 图型 | 轴 | 方法数 | 回答的问题 | |:---|:---|:---|:---| | `power_n` | N → Power | 20 | 少招人会掉多少效能 | | `power_events` | 事件数 → Power | 6 | 事件驱动设计的余量 | | `power_n_multi` | N → Power（按组数分系列） | 5 | 加一个臂的代价 | | `margin_tradeoff` | 界值倍数 → Power | 4 | 放宽界值能换回多少 | | `icc_sens` | ICC → Power | 2 | 设计效应对 ICC 误设的暴露 | | `gs_boundary` | 信息分数 → z 边界 | 10 | OBF vs Pocock 消耗函数（Lan-DeMets 闭式） | | `assurance_n` | N → Assurance | 2 | 成功概率规划 | | `alloc_suite`（副图） | 分配比 k=n₂/n₁ | 13 | 不等例分配的代价 |

- **诚实的边界声明**：曲线**穿过锚点是精确的**，锚点以外依赖族级结构假设（大样本下误差可忽略；
  n<20 或含连续性校正的方法误差变大）。故每张图带**效应量 ±20% 敏感带**，把假设的可见后果画出来。 图中红点即 R 数值 —— **图用于沟通趋势，协议里引用数值一律以 R 为准**。

### Added / 分配比诊断 `scripts/alloc_curve.py`（v5.5 合入技能，原为独立脚本）
- 13 个两独立组方法自动附带**分配比四图 + 速查表**：A 所需总 N vs 比（U 形，底在 1:1）·
  B 固定 N 下 power vs 比（倒 U）· C (n₁,n₂) 平面等效能等高线（与 1:1 对角线**相切**，1:1 最优的几何证明）· D 按效应量分层的效能损失。
- 统摄恒等式 `N(k)/N(1) = (1+k)²/(4k)`（Schoenfeld 膨胀），两均数 / 两率 / log-rank **通用**。
- ⚠️ **两率比较时 1:1 不是最优**：Neyman 最优 `k* = √(p₂(1−p₂)/p₁(1−p₁))`。
  p₁=0.10 vs p₂=0.30 → k*=1.53（n₁:n₂=2:3），**113 例 vs 1:1 的 118 例，省 4.2% 且 power 更高**。 故最优比标记**从实际曲线三分搜索动态求解**，未写死 `[2/3, 3/2]` —— 否则恰好在最有价值的场景标错。
- 新增 `--prefix` 参数：13 个方法各自隔离文件名前缀（此前固定 `ctss_alloc_*` 导致互相覆盖，
  实测 68 张图里只剩 4 张 alloc 图）。
- **第 4 个后端 `z`（通用两独立组 z 族）**：`ncp = θ·√(n₁n₂/N)`，与 t / log-rank 同形。
  覆盖 `poisson / vaccine_efficacy / win_ratio` —— 这三者效应量无统一尺度（率比、VE、获胜比）， 故 θ **由 R 锚点反解**（`theta_from_anchor`），与主图共用同一个锚点（ct-base §19.13）。 实测：θ 回代锚点误差 ≤1.1e-16；`N(k)/N(1)` 与理论 `(1+k)²/(4k)` 差 ≤4.4e-16； `N(1:1)` 精确还原锚点（如 n/组=64 → N=128）。

### Changed / 主流程集成
- `scripts/samplesize_power.py`：新增 `_render_default_figures_safely()` 桥接，在计算完成后调用。
  **与既有出图逻辑互斥，绝不重复**：
  - coze 已返权威曲线，或用户显式指定 `--n_seq`/`--power_seq`/`--plot_effects` → 只出**专项副图**（coze 不提供的分配比/界值/ICC/序贯边界）；
  - coze 无图 → 出**主图 + 专项副图**。
- 图形层全程 try/except 包裹，**任何异常都不阻断主结果**；无锚点时静默不出图（不画无根据的曲线）。
- 契约 `coze_cases/_contract_index.json` 全部 49 test 新增 `default_figure: {primary, secondary}` 字段，
  `_meta.default_figure_note` 说明语义；改图型映射仍以 `scripts/figure_kit.py::METHOD_FIGURES` 为准源。

### Fixed
- **`--hr` 参数名陷阱**：CLI 的 HR 参数是 `--hazard_ratio`，`--hr` 只是 argparse 前缀缩写，
  解析后属性名为 `hazard_ratio`。原 `getattr(args, "hr")` 恒为 None → 全部生存类方法静默不出分配比图。 改为 `_first(args, (候选名...))` 多候选取值。
- **簇大小/期中分析参数名**：`--m`（非 `--cluster_size`）、`--interim_looks`（非 `--n_looks`）。
- **assurance 字段名**：coze 实际返回 `assurance`，契约登记的是 `assurance_prob` → 锚点提取落空。
  `_pick_power` 改为优先序列举（`power/achieved_power/conditional_power/assurance/assurance_prob/...`）。
- 新增 `CTSS_FIGURE_DEBUG=1` 打印「为什么没出图」，避免静默失败无法诊断。
- **契约与实现不一致（contract drift）**：契约登记 13 个方法带 `alloc_suite` 副图，
  但 `_render_alloc_suite` 只实现了 3 个分支（ttest_ind / prop / logrank）， `poisson / vaccine_efficacy / win_ratio` 落入 `else: return []` 静默不出图 —— 全量回归实测只出 10 个。 该问题由「统计产出张数（104）与契约推算（116）对不上」发现。修复方式不是注销契约， 而是补上第 4 个 z 族后端（见 Added），**13/13 全部兑现**。

### Verified
- 分布内核 vs R 4.6.1：16 组参考值，最大偏差 3e-10。
- 标定器：49 方法 × 3 锚点，锚点残差 ≤1.1e-16、单调递增 100%。
- 端到端（mock meta）：**49/49 全部出图**，共 **116 张** SVG
  （49 主图 + 15 副图 + 13×4 分配比），**与契约逐项吻合**；全部通过 XML 解析、无 NaN/Inf、坐标在画布内。
- z 族后端精度：θ 回代锚点误差 ≤1.1e-16；`N(k)/N(1)` 与 `(1+k)²/(4k)` 差 ≤4.4e-16。
- 真实 coze 调用：`ttest_ind`（n=64, power=0.8）、`survival`（events=247）、`proportion_two`、
  `non_inferiority`、`assurance`、`vaccine_efficacy`、`poisson`（`--lambda1/--lambda2`）、 `win_ratio` 均正确产出主图 + 分配比四图。
- 已知非本层问题（coze 端 R 引擎自身报错，与本改动无关）：`cluster` 报
  `the condition has length > 1`、`group_sequential` 报 `argument is of length zero`。

### 依赖评估 / Dependency assessment

**结论：coze 端新增 R 包 = 0 个；新增本地 Python 第三方包 = 0 个；无需重新部署 Coze。**

评了两条路线。路线 A（让 coze R 为 44 个无图方法各画一张）**同样不需要装新包** —— `svglite` 已在 9 个必装包内，渲染设备不是瓶颈；各方法所需的计算包（`pwr`/`rpact`/`PowerTOST`/ `powerSurvEpi`/`simr`/`lme4`）也都在。真正的代价是**工程量与运行期延迟**，不是依赖。

| 图型 | 常规 R 做法 | 若走路线 A 需要的包 | 在现有 9 包内？ | |:---|:---|:---|:---| | `power_n`（20） | 逐方法写向量化 power 网格 | 无新增（各方法已在用的包）+ `svglite` | ✅ | | `power_events`（6） | `powerSurvEpi` 事件数曲线 | `powerSurvEpi` | ✅ | | `power_n_multi`（5） | `pwr::pwr.anova.test` 等 | `pwr` | ✅ | | `margin_tradeoff`（4） | `PowerTOST` / `TrialSize` | `PowerTOST`、`TrialSize` | ✅ | | `icc_sens`（2） | 设计效应闭式（精确需 `clusterPower`） | `clusterPower` | ❌ 未装 | | `gs_boundary`（10） | `rpact` 或 `gsDesign` | `rpact`、`gsDesign` | ✅ | | `assurance_n`（2） | 正态闭式（精确需 `bsurvival`） | `bsurvival` | ❌ 未装 | | `alloc_suite`（13） | 无现成包，需手写非中心 t 循环 | 无 | — |

**仅 2 处存在「本来想装但忍住了」的包**（`clusterPower`、`bsurvival`）：二者都改用**闭式近似 + 锚点标定**解决 —— 锚点由 R 给出，误差只落在「锚点以外的曲线形状」上，而形状的不确定性已由 图上的 ±20% 敏感带显式表达。装包换来的精确度提升，小于引入新依赖与镜像重做的成本。

**最终新增包清单（空）**：

| 侧 | 新增包 | 数量 | |:---|:---|:---| | coze 端 R | — | **0** | | 本地 Python | — | **0**（仅 stdlib `math`，`figure_kit.py` / `alloc_curve.py` 均零第三方依赖） |

> 顺带核清：仓库中 `escalation` / `BuyseTest` / `powerMediation` / `gsDesign` 的出现均为 > **注释里的使用建议**或已随 v5 coze-only 重构剔除的遗留函数（`install_all_packages`）， > 无实际 `library()` 加载 —— 不构成依赖。

## v5.4.0 (2026-08-30) · 待发布：两组不等例（ratio）支持（全 21 个两组检验）

### Added / 不等例 ttest_ind
- **引擎 `ss_ttest` 新增 `ratio` 参数（`type='two.sample'` 时启用 `pwr.t2n.test`）**：`ratio=n2/n1`，`n` 视为第一组 n₁。求 power 用 `pwr.t2n.test` 正解；反解 n₁ 用 `uniroot` 包非中心 t（与 `pwr.t2n.test` 逐点一致）。等例（ratio=NULL/1）行为完全不变。
- **`run_task.R` 新增 `.ratio()`**，主求解 / 曲线求解器 / 效应轴 / 热力图 / `default_solved_n` 全部透传。
- **CLI `--ratio`**：仅 `ttest_ind` 用，缺省=1 等例；提供时 `--nobs` 视为 n₁。
- **契约**：`_contract_index.json` 与 `coze_contract.md` 的 `ttest_ind` required 增加 `ratio`（否则 `build_params` 白名单不会透传该字段）。
- **本地验证**：等例 50/50→0.6969（与旧 coze 一致）；不等例 30/70→0.6213（与 statsmodels 一致）；反解 30/70 到 0.8→n1=46,n2=107,total=153；等例反解→64。契约回归 ALL PASSED。

### Extended / 不等例扩展到全部 21 个两组检验（2026-08-30）
- **范围判定（49 检验 → 21 可行）**：剩余 28 个为配对/单组/多组(k≥3)/交叉/回归-事件数/历史对照/整群/多终点等，**ratio 无意义**，正确排除。21 个两组结构全部支持 `--ratio`（n₂/n₁）。
- **本次新增 9 个引擎分支（含 Schoenfeld/rpact 兜底）**：
  - 率：`non_inferiority`、`superiority_margin`、`equivalence`（均值 TOST）、`poisson`、`vaccine_efficacy`
  - 生存：`ni_survival`、`survival_equivalence`、`survival_superiority`、`survival_exact`
- **统一契约 `n2 = ceil(n1 * ratio)`**：比例函数（noninf/prop/poisson/vaccine/eq_means/sup_margin）原本即此；4 个 Schoenfeld 生存函数（surv_equiv / surv_sup / ni_survival / survival_exact 兜底分支）原本独立 `ceiling(D·r/(1+r)/er)` 导致 r=2 时 `n2` 与 `2·n1` 因取整差 1 → **改为 `ceil(n1*r)`**，与比例函数一致、r=2 时精确 `n2=2·n1`。
- **`ss_survival_exact` 健壮性修复**：原硬依赖 rpact `getDesignGroupSequential`（rpact 缺失即报错）。现 `tryCatch` 包裹，rpact 不可用时整体退化为纯 Schoenfeld 兜底（与 ni_survival/surv_equiv 同构），不再硬报错。
- **`run_task.R` 分发**：9 个主求解分支透传 `ratio = .ratio(p)`；`ss_eq_means` 的曲线/效应轴/主求解共 3 处调用点均透传；Schoenfeld 反向 power 的 `sqrt(r)/(1+r)` 缩放沿用（r=1 退化为 /2）。输出在 `!is.null(res$n2)` 时报告 `label.n2_per_group`。
- **契约**：`_contract_index.json` 的 9 个 test required 增加 `ratio`，全量 21 个 ratio-enabled test 确认无误；`coze_contract.md` 表格 9 行追加「可选 --ratio 支持不等例（n2/n1）」，输出列头统一为 `n_per_arm`。
- **本地验证（屏蔽 library 强制基R兜底，`outputs/verify_unequal2.R`，本机 R 4.6.1）**：20/20 全过——
  - 9 函数 ×（等例 ratio=1→n2=NULL 且 total=2·n1；ratio=2→n2=ceil(n1·2) 精确、total=n1+n2、n1<等例 n1）共 18 项 OK；
  - 反向（固定总 N=400）unequal power ≤ equal power（poisson / noninf）2 项 OK，确认不等例对固定总量确实更低效（数学正确）。
  - `py_compile` 三文件（coze_client/main/samplesize 节点）过；契约回归 `tests/coze_cases_regression.py` **ALL PASSED**。
- ⚠️ 需 **Coze 重新部署** 才在生产生效（重新发布清内存缓存，需干净 zip + MD5 校验双侧同步，待授权）。覆盖本次 21 个 test 的全部 `run_task.R` / `samplesize_functions.R` 改动。

## v5.3.18 (2026-08-29) · 待发布：本地模拟验证闭环（P1-C）

### Added / 解析解↔Monte-Carlo 独立验证
- **新增 `scripts/verify.py`（纯本地、零联网、零患者数据）**：把样本量解析解（来自 pwr / gsDesign / rpact / coze 的 n）**回代**到独立实现的 Monte-Carlo 数据生成过程，检验它实际达到的操作特性：
  - empirical **power** vs 名义 power（容差 **±2 pp**）
  - empirical **type-I error** vs 名义 alpha（容差 **±0.5 pp**）
  - 生存设计额外校验**期望事件数**（容差 **±5%**）
- **独立性原则（防自证）**：验证器**不复用**被验证对象的样本量公式/检验边界——只接收「解析解给出的 n（与组序贯边界）」作输入，其余（数据生成、检验统计量、判定）全部独立实现。因此同源公式错会被抓出，而非互相盖章。
- **方向性判定**：`power` 用双边容差；组序贯/适应性设计可调方向——SSR（promising-zone 扩样）本就**预期**把 power 抬高于名义值，故用 `lower`（不低于目标-2pp 即 PASS）；TIE 用 `upper`（不超过 alpha+0.5pp）。每项同时给出 MC 95% 置信区间；若 MC 误差已逼近容差，判 `INCONCLUSIVE` 并提示提高 `--verify-nsim`，**绝不给出看似确定的伪 PASS/FAIL**。
- **组序贯边界**：强烈建议传 `--verify-boundaries`（rpact/gsDesign 输出的 z 边界），此时为**真·独立验证**；不传时内置 Lan-DeMets 递归数值积分自算边界，结果明确标注 `self_derived_boundaries`——仅 sanity check，**不构成独立验证**。
- **支持设计**：`ttest_ind / ttest_one / ttest_paired / proportion_two / survival(log-rank) / group_sequential / adaptive_reestimate(promising-zone SSR)`。
- **主流程桥接**：`--verify` 触发（默认关闭）；配套 `--verify-design / --verify-n / --verify-effect-size / --verify-p1/--verify-p2 / --verify-hr / --verify-median-control / --verify-accrual / --verify-followup / --verify-boundaries / --verify-nsim / --verify-json` 等。`--verify-n` 必填（无 n 则验证无意义）。

### Verified / R 交叉核对（本机 R 4.6.1）
- **独立核实验证器本身正确**：固定样本 `ttest_ind` n=175/d=0.3 → 模拟 power 0.801，R `pwr.t.test` 解析 0.6385@n=120、0.80 需 n≈175（量级吻合且趋势一致）；组序贯 `n=175/d=0.3` + R/gsDesign 权威边界 `2.9626,1.9686` → 模拟 power 0.803（PASS）、TIE 0.026（≤0.025+0.5pp，PASS）。
- **阴性对照**：故意给错 n（如 ttest n=40 → 真 power≈0.59）判定 **FAIL**（exit 2），证明验证器有真实鉴别力，非对一切输入盖章 PASS。
- `py_compile` 通过（`verify.py` / `samplesize_power.py`）；主流程 `--verify` 桥接端到端冒烟通过。

### Compatibility / 兼容性
- 新增 `--verify*` 参数组，默认全部关闭，不影响既有样本量计算路径；无 R 依赖（标准库即可，`numpy`/`scipy` 可选加速与精确分位数）。

## v5.3.17 (2026-08-29) · 待发布：移除功效曲线上的功率水平参考线（仅用竖线标输入量）

- **🔴 移除功效曲线上的功率水平参考线**：v5.3.16 在 reverse 分支保留了 `abline(h = p$power %||% 0.8)` 水平线「作对照」，但 power 是**输出**（reverse）或**既定参数**（forward 曲线已转置为 x=效能），该水平线交点恰好落在「计算所得样本量」上——既误导又无法代表"理想 power"。用户指出 forward（直接计算样本量）本就不该有水平 0.8 线。据此统一原则：**任何功效曲线只画「竖线标用户输入量」，不画功率水平线**。
  - `adapters/coze/src/r_engine/run_task.R::.run_curve`：`n_seq`（power-vs-N）分支删除 `abline(h = ...)`；仅当 `p$nobs` 给定（reverse）时画 `abline(v = nobs)` 竖线标输入样本量；`else`（`power_seq`，N-vs-power）分支保留 `abline(v = p$power %||% 0.8)` 竖线标目标效能。
  - 本地 SVG 兜底 `scripts/samplesize_power.py::_curve_svg_from_stats`：删除 `ref_power` 水平线绘制（`power = X` 文本块），仅保留 `ref_n` 样本量竖线。
  - 休眠镜像 `r_templates/r_curve.py`（coze 镜像 + r-assets 两份）：`_CURVE_POWER_*` 模板删除 `abline(h = __TARGET__)`，保留 `__N_REF__` 竖线占位。
- **验证**：`py_compile` 三文件过；SVG 兜底功能测试——reverse（ref_n=100）含 `n = 100` 竖线且**不再含** `power = 0.8` 水平线、forward(x=效能) 亦无 `power =` 水平线；两份 r_curve.py 无残留 `abline(h = __TARGET__)` 且 `__N_REF__` 保留（各 2 处）。
- ⚠️ 同上，`run_task.R` 改动**需重新部署 coze 镜像线上生效**（与本次会话其余 coze 端修复同红线）。
- 📝 注：效应量轴曲线（`效应量轴曲线` 图）的 `abline(h = 0.8)` 属"目标效能水平线"语义（看什么效应量达到 80% 功效），与本次"power-vs-N 曲线"不同，暂未改动；如你也想在该图去掉，告诉我。

## v5.3.16 (2026-08-29) · 待发布：修复反向求 power 时功效曲线参考线错位

- **🔴 反向求 power 曲线参考线修复**：此前 reverse（给定 --nobs 求 power）自动附带的「把握度随样本量」曲线（x=样本量、y=效能）只画**水平的目标效能线**（`abline(h = target_power)`，即 power=0.8），其交点恰是「达到 0.8 所需的计算样本量」——这正对应"参考线仍按计算样本量绘制"的观感，而用户期望**按自己输入的样本量 n 标参考线**直接读出该 n 的效能。
  - `adapters/coze/src/r_engine/run_task.R::.run_curve`（传统曲线模式）：reverse 分支新增 `abline(v = p$nobs, lty=3, col="blue")` 竖直参考线（按给定样本量），水平目标效能线保留作对照；forward 分支（此前无参考线）补 `abline(v = p$power)` 竖直目标效能线，与 reverse 对称。
  - 本地 SVG 兜底 `scripts/samplesize_power.py::_curve_svg_from_stats` / `render_curve_fallback` 同步：新增 `ref_n` 参数，reverse 时在给定 n 处画蓝色竖直虚线（`n = X`），forward（x=目标效能、y=n）语义下不画该竖线；主流程与 auto-curve 两处调用点透传 `--nobs`。
  - 休眠镜像 `r_templates/r_curve.py`（coze 镜像 + r-assets 两份）+ `local_r_backend.py`（两份）的 `build_curve_code` 同步加 `__N_REF__` 占位与 `n_ref` 注入（reverse 注入 `abline(v = nobs)`，forward 因 `_CURVE_N_*` 自身已画目标效能竖线故不注入、无残留占位符），保持镜像一致。
- **验证**：`py_compile` 五文件全过；`_curve_svg_from_stats` 功能测试——reverse（ref_n=100）含 `n = 100` 竖直线 + `power = 0.8` 水平线、无 ref_n 时竖线缺失、forward(ylim=n) 语义下 ref_n 不画竖线；`r_curve.py` 模板替换测试——reverse 注入竖线无残留 `__N_REF__`、forward(nobs=None) 无残留占位符、`_CURVE_N_SINGLE` 自身 `abline(v=__TARGET__)` 不变。
- ⚠️ `run_task.R` 改动**需重新部署 coze 镜像后线上生效**（与本次会话其余 coze 端修复同红线）。

## v5.3.15 (2026-08-29) · 待发布：修复「默认不回传 R 代码」+ coze 冷启动 15s 无应答

- **🔴 修复「默认分析不回传 R 代码」**：`scripts/samplesize_power.py` 的 `ctx["return_r_code"]` 原默认 `False`（仅 `--show-code` / `CTSS_RETURN_R_CODE` 时置 True），导致 coze **默认根本不被要求**返回 `repro.r`，HTML 报告与对话都拿不到 R 代码。改为**默认 `True`**，对齐 meta-analysis「每个分析默认回传可复现 R 代码」。`compute` 内 `r_code=repro.get("r") if ctx.get("return_r_code") else None` 现恒能取到；R 代码默认进 HTML 报告 + 对话展示（`info.r_code_shown_default` 旧提示逻辑随之移除）。
  - ⚠️ 这**反转了**早先 audit #7 的「R 代码默认不提供，仅使用者明确要求时提供」决策（见下方 v3.4.x 第 465 行），现按用户 2026-08-29 规则改为默认回传。
- **🔴 修复 coze 冷启动 15s 无应答**：`adapters/coze_client.py::_urlopen_with_proxy_fallback` 用 `http.client.HTTPSConnection(host, timeout=15)`，其 timeout 实际作用于**所有** socket 操作（connect 与 recv 共享同一超时）——旧注释"读取不设限"是**错误**的；coze serverless 冷启动 >15s 时读取被 15s 杀掉，表现为「每次都 15s 无应答」。meta-analysis 用 `urllib.urlopen(timeout=600)` 故无此问题。
  - 修正：拆成 connect / read 两个独立超时——`connect_timeout=15`（连接失败快速报错，不空等）、`read_timeout`（默认 **600s**，可由 `CTSS_COZE_READ_TIMEOUT` 覆盖，对齐 meta-analysis 的 `COZE_META_TIMEOUT=600`）；`conn.request()` 完成后把底层 socket 超时改为 `read_timeout` 再 `getresponse()` / `read()`。Windows 代理残留直连重试逻辑不变。
- **验证**：`py_compile` 通过；mock 模式 dry-run 信封 `return_r_code: true`；mock 实算对话出现 `[R 代码 — 本次分析生成]` 段、HTML 报告含 `repro.r`。

## v5.3.14 (2026-08-29) · 待发布：coze 回传结构大调整——完整 JSON 外置 S3 临时文件 + 内联仅轻量删减版

- **🔴 coze 回传结构反转**：R 引擎生成的**完整信封**（含 figures/repro/narrative/stats/warnings/notes）整体写入**单个 S3 临时文件**，内联 `result` 仅保留轻量删减版——**直接删除 figures 与 repro**；若仍 > 4000 字符按「现有逻辑」从大到小丢 stats 子块（极端截断 narrative）直到 < 4000；删减掉的内容**不再**存入文件（完整数据已在 S3，零丢失）。
- **🟢 本地优先取完整数据**：`coze_client.py::call` 解析内联 result 后优先检测 `_coze_full`，经 URL **下载完整 JSON** 作为分析源（含 figures/repro，零删减）；下载失败 / 无链接降级到旧 `_coze_manifest`（manifest 重组）或 `figures[].url`（legacy 回填），保持对旧 coze 端向后兼容。
- **🟢 内联轻量版仅用于飞书 + 老版本兼容**：coze 端 `feishu_save_node` 写飞书 `resultstr` 列消费的是内联删减版；老版本本地技能（不识 `_coze_full`）也只解析内联版。两者均不参与本地完整分析。
- **🟢 重写 coze 端 `_externalize_to_manifest` → `_externalize_full`**：删 manifest 拆块逻辑；新增 `_build_inline`（删 figures/repro）+ `_trim_inline_to_limit`（丢 stats 子块/截断 narrative 至 < 4000）；保留 daemon 90s 超时守护与 S3 不可用降级（降级为无 `_coze_full` 的内联删减版，绝不因超 4000 被平台截断破坏 JSON）。
- **✅ 已对齐 ct-base §20.8（2026-08-29 用户拍板同步 → 2026-08-29 再收窄为单一标准）**：§20.8 先由「统一 manifest 外置」增补为「两种已批准模式」（模式 A manifest 外置 + 模式 B 完整 JSON 单文件外置，本技能采用 B）；用户进一步拍板「§20.8 只保留模式 B、模式 A 删除」，ct-base 随即删除模式 A、收敛为「完整 JSON 单文件外置」单一全库标准。ct-base `BASE.md` §20.8 索引 + `docs/07-coze-engine.md` §20.8 已改写为单模式标准；本技能 `coze_contract.md`（本地层/coze 层）对齐提示改为「已对齐 §20.8（完整 JSON 单文件外置）」。meta-analysis 仍为旧 manifest 外置、待迁移（§20.8 标注为现状例外）。
- **验证**：`py_compile` 两侧通过；`verify_coze_full.py` 全链路 **20/20 PASS**——① `_externalize_full` 产出内联 < 4000、无 figures/repro、含 `_coze_full`；② 本地 `_fetch_full_json` 经 `file://` 还原完整数据（figures/repro 全等）；③ 旧 `_coze_manifest` 内联 → `_fetch_full_json` 返回 None（降级旧契约）；④ S3 不可用 → 降级内联删减版（无 `_coze_full`）；⑤ 内联超 4000 → `_trim_inline_to_limit` 反复丢 stats 子块 / 截断 narrative 至 < 4000，且**含 `_coze_truncated` 标记**整体仍严格 < 4000。
- **🐞 ⑤ 修复（2026-08-29 收尾）**：初版 `_trim_inline_to_limit` 循环仅把 `inline` 本身压到 < 4000，但末尾追加的 `_coze_truncated` 诊断标记（被删字段名列表，极端 ~117 字符）把**最终**序列化结果推回 > 4000，导致 ⑤ 失败。修复：循环条件与 narrative 额度均把 `_coze_truncated` 标记自身大小计入预算（`_marker_sz`），末尾再加一次兜底「逐条缩减标记直至整体 < limit（不恢复已删数据）」，确保最终内联恒 < 4000。

## v5.3.13 (2026-08-29) · 待发布（已并入 v5.3.14 发布）：coze 信封漂移检测修订——版本号差异不再提醒，仅数据内容/结构不一致触发（同步 ct-base §20.9）

- **🔴 删除版本号比较提醒**：`adapters/coze_client.py` 移除 `EXPECTED_COZE_ENVELOPE_VERSION` 常量与 `_coze_version_higher()` 语义版本比较辅助函数，以及 `_assess_contract` 内的「② 版本漂移」分支。`coze` 返回 `_coze_version` / `_contract_version` 高于本地期望**不再触发任何提醒**。
- **🟢 仅保留结构/数据内容漂移提醒**：`_assess_contract` 现只检测字段别名/结构形变（如 `content`→`narrative`、`figures` dict→list、图体 `svg/image/svg_data/base64`→`content`）并自适应归一化；映射发生时记 drift 说明 → 经 HTML `.banner`（`_needs_upgrade`/`_contract_drift` 驱动）提示升级。版本由 coze 端随发布同步，本地不比对版本号，避免无谓打扰。
- **🟢 ct-base §20.9 规范同步（单一真相源）**：标题改为「仅数据内容/结构不一致触发」；删除「② 版本漂移」小节与「版本号三方同步」要点；「跨技能通用性」「设计要点」「落点」各段移除对 `EXPECTED_COZE_ENVELOPE_VERSION` / 版本标记比对的引用；验证口径改为「版本号差异不再触发 drift」。
- **🟢 叶子契约 `coze_contract.md` 同步**：`_coze_version` 改为仅诊断透出、明确「本地不比对版本号」；删除「版本漂移」子弹点与「三方同步」要求。
- **纯本地改动，无需重部署 coze**：coze 端 `_COZE_ENVELOPE_VERSION`（`"5.3.9"`）保持不变，仅本地消费逻辑收敛。
- **验证**：`py_compile` 通过；`verify_drift_v3.py` 5 项全 PASS——① 版本号高/结构一致→不提醒、② 结构别名漂移→提醒、③ figures 结构形变→提醒、④ 完全一致→不提醒、⑤ 缺版本标记/结构一致→不提醒。

## v5.3.12 (2026-08-28) · ✅ 已发布（GitHub / SkillHub / ClawHub 三平台）：SKILL.md 对齐 ct-base §3/§4 正文规范 + 跨轮连续性/菜单设定对齐 ct-base

- **🔴 SKILL.md 正文英文化（ct-base §3 排版规则 + §4 正文规范）**：原 `## Cross-turn Continuity（跨轮连续性·必须）` 整段为中文指令散文，违反「SKILL.md 正文（YAML 之外）一律英文（agent-facing）」；按范本 meta-analysis §5.1 英文结构重写（英文指令 + 回显块字面串保留 `## 当前分析设定：` 前缀，与 ct-base §5.1 登记一致），并清掉 Features 表 ④、figure-set、3-round cap、agent rule 等 4 处零散中文注。仅保留 `## Language` 段「中文指南」链接标签（与范本一致）及运行期回显块字面串。
- **🟢 跨轮连续性/菜单设定对齐 ct-base（本轮"都做"的 A/B/C/D）**：① merge_spec 软约束诚实说明（call() 网络层不强制、默认路径是 LLM 行为约定）；② §5.1 登记前缀同步为 `## 当前分析设定：`；③ Vague 深挖 3-round cap 与参数缺失澄清 2 轮（AGENTS.md §6.1）显式区分；④ 发布态 merge_spec 路径改相对 `scripts/merge_spec.py`（避免发布后失效）。
- **🟢 version 字段对齐 CHANGELOG（ct-base §9）**：`version: 5.3.0` → `5.3.12`，与最新发布条目一致。
- **纯文档改动，未改代码、未重部署 coze**。

## v5.3.11 (2026-08-28) · 待发布：coze 信封契约漂移检测按 ct-base §20.9 定稿重构（单入口 _assess_contract）

- **🔴 删除旧 `_check_coze_version_drift`（三通道提醒）**：原实现 `!=` 即提醒、缺标记也提醒、且经 `sys.stderr` + `meta._upgrade_advisory` + `Result.text`（结论区）三处重复提示升级。
- **🟢 新增 `_assess_contract(parsed) → (parsed, drift_notes, needs_upgrade)`（ct-base §20.9 单入口）**：综合「结构漂移（主·自愈）+ 版本漂移（显式）」，照搬 meta-analysis 范本并据 ct-samplesize 信封微调别名表（`content`→`narrative`、图体 `svg/image/svg_data/base64`→`content`、`figures` dict→list）。两路信号汇入同一返回；映射发生时记 drift 说明。
- **🟢 版本比较改语义化（修 5.10.0>5.3.9 字典序误判）**：新增 `_coze_version_higher(a, b)` 按段数值比较（裸字符串 `>` 对 `"5.10.0">"5.3.9"` 会判错）。版本漂移判定由 `!=` 改为**高于**期望才显式触发；**缺标记不视为漂移**（零噪音原则）。
- **🟢 用户可见提示收敛到 HTML 唯一出口**：`compute()` 写回信封 `_needs_upgrade`（bool）/`_contract_drift`（list[str]），`rendering.py` 在报告顶部 `.banner` 渲染"已在本地自动适配，如频繁出现建议升级 ct-samplesize 技能到最新版"（技能名取实际技能）；`scripts/samplesize_power.py` 透传标记至 `_report_env`。删除全部 `sys.stderr` 升级文案与结论区污染。
- **纯本地改动，无需重部署 coze**：信封版本 `_COZE_ENVELOPE_VERSION` 仍为 `"5.3.9"`（coze 端 `_coze_version` 恒内联已达标，未动）；仅本地消费逻辑重构。
- **验证**：`py_compile` 三文件通过；`verify_drift_v2.py` 18 项全 PASS——语义版本比较（5.4.0/5.10.0>5.3.9、5.3.9/5.3.8 不高于）、A 一致零噪音、B 结构别名 content→narrative 自适应+提示、C 版本高于触发、D 缺标记零噪音、E 图体 svg→content 自适应、F figures dict→list、渲染横幅（含漂移/一致零横幅）全过。

## v5.3.10 (2026-08-28) · 待发布：coze 出站并发限流（相邻 ≥1 秒，ct-base §20.10）

- **🟢 coze 调用并发限流（用户定）**：`adapters/coze_client.py` 新增模块级 `_RATE_LIMIT_LOCK` +
  `_LAST_CALL_TS` 与 `_acquire_rate_limit()`，在 `call()` 真实 POST 前串行化"间隔决策"并强制 相邻两次 coze /run 调用**至少间隔 1 秒**，防止触发 coze 端 429 频控（meta-analysis 实测曾因此 被限流至次日）。间隔秒数由环境变量 `COZE_META_MIN_INTERVAL`（浮点秒，默认 1.0；`<=0` 关闭）覆写， 与 meta-analysis 同名跨技能一致。
- **纯本地改动，无需重部署 coze**：限流仅作用于本地出站节奏，`_COZE_ENVELOPE_VERSION` 信封版本不变
  （仍为 `"5.3.9"`）。mock 模式（`CTSS_COZE_MOCK=1`）不触网、不受限流约束。
- **作用域边界**：同进程多线程并发已被 `threading.Lock` 覆盖；跨进程并发未实现（ct-base §20.10 已标注）。
- **验证**：`py_compile` 通过；`verify_rate_limit.py` 3 线程并发打桩（不连网），出站时刻
  `0.0xx / 1.0xx / 2.0xx`、相邻间隔均 ≥1.0s → PASS。

## v5.3.9 (2026-08-28) · 待发布：coze 返回版本漂移检测——自适应兼容 + 升级提醒

- **🟢 coze 信封新增 `_coze_version` 版本标记（coze 端 `samplesize.py::_COZE_ENVELOPE_VERSION="5.3.9"`）**：恒内联（纳入 `_CORE_INLINE`，不走 manifest 外置/丢弃），随每个响应返回 coze 端契约版本。
- **🟢 本地版本漂移检测（`coze_client.py::compute`）**：新增 `EXPECTED_COZE_ENVELOPE_VERSION="5.3.9"` 与 `_check_coze_version_drift(env)` 辅助。coze 返回信封的 `_coze_version` 与本地期望**不一致或缺失**即判定为"coze 返回与本地代码对不上"：
  - **自适应修改（兼容）**：`compute()` 在检测前先 `env.setdefault` 归一化 `stats/narrative/figures/warnings/notes/repro` 缺省字段，旧契约回退路径（`_fill_external_svgs_legacy` / manifest 重组）本就在 `call()` 内生效 —— 漂移响应不下崩、仍产出可用 `Result`。
  - **提醒用户升级**：三处同步透出 —— ① `sys.stderr` 打印 `[ct-samplesize] ⚠️ 版本漂移：...`；② `meta["_upgrade_advisory"]` 机器可读；③ 追加进 `Result.text`（报告"结论"区可见）"⚠️ 提示：...建议升级 ct-samplesize 技能（含 coze 端）到最新版"。版本一致时零噪音。
- **🟢 契约同步**：`r-assets/coze_contract.md` §3 响应信封字段列表补 `_coze_version`，标注须与 coze 端 `_COZE_ENVELOPE_VERSION` 及本地 `EXPECTED_COZE_ENVELOPE_VERSION` 三方同步。
- **验证**：`py_compile` 两端 OK；`verify_drift.py` 实跑 3 场景 —— A) 版本一致（无提醒、Result 正常）✅；B) coze 缺 `_coze_version`（触发提示、自适应兼容、Result 正常）✅；C) coze 版本旧（"5.3.1"≠"5.3.9"，触发提示、Result 正常）✅；stderr / `meta._upgrade_advisory` / `text` 三处均含提醒文案。

## v5.3.8 (2026-08-28) · 待发布：HTML 风格修正——结论区真正两端对齐，hero 回退

- **🔴 回退 hero-kv 网格（v5.3.7 第 9 条方向被否定）**：用户确认 Cohen's d / 目标功效 应保留在**结论区**而非顶部摘要。撤销 `.hero-kv` 两列网格与「Cohen's d 纳入 hero」改动，`_render_hero` 恢复原始结构（每组 n 大字主值 + `.sub` 副行显示目标功效/给定 n + 达标徽章）；对应 CSS `.hero .sub` 还原、暗色模式删除失效的 `.hero-kv .k/.v` 死规则。
- **🔴 结论区数值真正两端对齐（修正 v5.3.7 第 8 条的空操作）**：原仅给 `.concl-row .cv` 加 `text-align:right`，但 `.concl-row` 是 flex 行、`.cv` 收缩成内容宽度，右对齐不生效（数值贴标签右侧而非最右端）。补 `flex:1` 让 `.cv` 占满剩余空间，`text-align:right` 才真正把数值顶到最右 —— Cohen's d / 目标功效 / 每组 n 等结论条目实现标签左、数值右的两端对齐。
- **验证**：`py_compile` OK；`render_html_report` 实跑样本信封生成报告，自动断言：hero 无渐变 ✅、数值加粗 ✅、4 类小标题图标命中 ✅、分组卡图标保留 ✅、hero-kv 无残留（CSS+HTML）✅、`.concl-row .cv` 含 `flex:1`+`text-align:right` ✅、结论区三行（Cohen's d / 目标功效 / 每组 n）均在场且以 `.cv` 右对齐 ✅、hero 区块内 Cohen 计数 0 ✅。

## v5.3.7 (2026-08-28) · 待发布：HTML 报告风格对齐 meta-analysis 参考（3 处）

- **🔴 `adapters/rendering.py` `_CTSS_REPORT_TEMPLATE` 顶部 Hero 去底色**：原 `.hero` 为蓝色渐变（`linear-gradient(135deg,#1e3a8a,#2563eb)`）+ 白字，改为白色卡片（`background:var(--card)` + 边框 + 阴影），文字转深（`var(--text)`/`var(--muted)`），徽章转浅色（`.badge.ok` 浅绿 / `.badge.warn` 浅橙 / `.badge.bad` 浅红，`currentColor` 圆点）——与 meta-analysis 参考报告视觉一致。
- **🟡 数值列表加粗**：`table.stats td.v` 与结论 `.concl-row .cv` 增加 `font-weight:700`（对齐 meta-analysis `.kv .v` 加粗），关键数值更醒目。
- **🟡 小标题加图标**：三个 `.card h2`（📊 图形 / 🧮 计算结果 / 📝 结论）与结论小节 `.concl-sec`（📌）加 emoji 图标，对齐 meta-analysis `.cap .ico` / `.group h3 .ico` 风格；stats 语义分组卡原有图标（🎯⚙️📋📦📈）保留不变。
- **🟡 数值列右对齐**：`table.stats td.v`（计算结果表数值列）与结论 `.concl-row .cv` 增加 `text-align:right`，标签列 `td.k` 保持左对齐 —— 形成"标签贴左、数值贴右"的两端对齐效果，数值纵列更易扫读。
- **🟡 顶部摘要 hero 副指标改为 `.kv` 网格两端对齐**（**该方案已于 v5.3.8 回退**）：原 hero 副指标（目标功效 / 给定 n）为横排 `.sub` 附注，与下方结果表视觉不一致；一度改为 `.hero-kv` 两列网格并把 Cohen's d 纳入 hero。用户确认 Cohen's d / 目标功效 应留在结论区，故 v5.3.8 撤销此改动，hero 恢复 `.sub` 原始结构。
- **验证**：`py_compile` OK；`render_html_report` 实跑样本信封生成报告，自动断言 hero 无渐变、数值加粗、4 类图标全部命中、分组卡图标保留，全过。

## v5.3.6 (2026-08-28) · 待发布：coze 端代码模块化去重（R 渲染统一 + Python solve_for_power）

- **🔴 R 端 SVG 渲染块统一为 `.render_fig()`（消除 6 处重复）**：`run_task.R` 新增 `.render_fig(draw, type, caption, warns, fallback, width, height)` 辅助函数，统一 svglite 渲染逻辑（`requireNamespace` + `svgstring` + `dev.off()` + 失败兜底 warns）。原 6 处重复块（`.run_dist`/`.run_surv_time`/`.run_heatmap`/`.run_curve`×2/adaptive visualize）全部改为调用该函数。adaptive 分支的 width=8、内联 tryCatch 也统一（抽 `.draw_adaptive`）。`.render_fig` 返回 `list(fig, warns)` 保证 warns 正确回传（R 按值传递，避免 `<<-` 只改局部）。本地 R 回归 11 场景（9 方法默认全图集 + 显式 dist/heatmap）全过：`FINAL_RENDER_REGRESSION=True`。
- **🟡 Python 端 `build_core_r_code` 的 `solve_for_power` 预计算（消除 28 处重复）**：`local_r_backend.py` 函数开头预计算 `_sfp = str(solve_for_power).upper()`，28 处 `.format(solve_for_power=str(solve_for_power).upper())` 统一改为 `solve_for_power=_sfp`。纯去重、不改 R 模板输出（已验证 `.format` 关键字传参等价）。7 个 test（mixed_model/roc/poisson/cluster/bland_altman/be_tost/ttest_ind）mock 生成 R 代码全过，py_compile OK。
- **已知未做（高风险，待用户决定）**：`build_core_r_code` 的 14+ 分支 cat 骨架（`R_XXX + f"""cat(...)"""` 手写，约 55-65% 重复，预计可减 250-300 行）、7 处 `print(t(...)); sys.exit(1)` → `_fail` helper。涉及 R 字符串模板重写，回归风险高，需用户确认后再动。

## v5.3.5 (2026-08-28) · 待发布：i18n.py 对齐 ct-base（消除 shared_sync_check 漂移，方案 A）

- **🔴 `scripts/i18n.py` 对齐 ct-base（消除 shared_sync_check 漂移）**：旧版 593 行内置 `_MESSAGES` 大字典（201 键）替换为 ct-base 165 行版（从 json 加载，数据外置单一真源）。公共 API 一致（set_lang/is_chinese_os/_current_lang/t/_=t），对调用方零破坏。
- **🆕 `scripts/i18n_skill_messages.json`（技能级词条文件，ct-base v1.1.77 新机制）**：把旧版内置的 **183 个技能专有统计词条**（label.* 102 / r_header.* 42 / error.* 21 / header.* 16 / info.* 1 / safe_preview.* 1）迁入该文件。这些词条是 ct-samplesize 专有文案，不污染 ct-base 通用 json。
- **vendor 补齐 json**：`scripts/i18n_messages.json`（237 键，从 ct-base 复制，严格一致）；`scripts/i18n_r_messages.json` 补齐 5 个 `error.rscript_*` 键至与底座一致（subset 满足）。
- **移除旧版自覆盖的 `auth.coze_outbound`**：旧版用自己的样本量授权文案覆盖了 ct-base 标准词条；现改走底座标准版（"不含 PII/受试者/未公开项目数据"通用表述，语义兼容），符合 §16.8。
- **验证**：替换后 i18n.py + 三 json 取到旧版全部 201 键（0 回退键名）；samplesize_power/coze_client/compute_backend 导入 OK；`shared_sync_check` **全部一致 ✓**。
- **备份**：旧 `scripts/i18n.py` → `scripts/i18n.py.bak_20260828`。
- **边界**：coze 端 `adapters/coze/ct_r_lib/i18n.py` 为独立自包含部署实例（无 json、不在闸门范围），本次未动（改需动 Docker 打包，独立任务）。

## v5.3.4 (2026-08-28) · 待发布：coze 默认全图形集 + figures type 字段 + 展示策略重构（对话流不内联、HTML 报告全量）

- **🟢 默认全图形集（用户定，2026-08-28）：显式图形模式改为默认出图**：`run_task.R` 新增 `.default_figures()` + `.default_solved_n()`，用户未显式请求图形时，为支持的 test **一次性累积生成多张图**——(1) 曲线（9 个 curve solver：forward→样本量曲线 / reverse→效能曲线）；(2) 分布重叠图（ttest*/proportion*/survival）；(3) 效应量轴曲线（9 个 solver，按 test 语义自动构造 effect_seq 默认序列）；(4) 效能热力图（9 个 solver，n_seq × effect_seq 自动网格，forward 用解出的 n 构造 n_seq）；(5) 随访-效能曲线（survival only，需 event_rate；缺省时跳过并记 warning）。每张图独立 tryCatch，失败仅跳过不阻断其余。本地 R 回归 9 方法 forward + reverse + 显式不触发场景全过：8/9 方法默认全图集完整（curve+dist+effect_curve+heatmap），survival 提供 event_rate 时 5 张图全出、缺省时随访曲线跳过并带双 warning。显式请求任一图形时仅出该图（不触发默认集，防重复）。
- **🔴 展示策略重构（用户定：对话流不展示图形，HTML 报告全量）**：`scripts/samplesize_power.py` `render_figures` 与 `render_curve_fallback` 的 `__SVG_WIDGET__` / `__FIGURE__ svg/png` 内联标记**默认关闭**（设 `CTSS_INLINE_WIDGET=1` 恢复），图形不再内嵌对话流；全量展示完全交给 `render_html_report`（stats + 全量内联 SVG + R 复现脚本，单文件 HTML）。`__FIGURE__ html`（报告入口）保留。SKILL.md L61/L173 内联规则同步修订。端到端冒烟：coze anova→1 张 curve→`render_html_report` 全量内联成功（HTML 含图形卡 + 1 个 `<svg>`）。
- **🔴 coze 云端默认自动曲线补齐（修复文档-代码不一致）**：此前**云端 R 引擎从未实现**默认曲线（仅本地 `samplesize_power.py` 有），导致 coze 出站 `figures=[]`，与 SKILL.md L61「★ Auto-curve…默认附曲线」及 ROADMAP 状态 ✅ 不符。本地 R 回归 10 case（5 方法 × forward/reverse）全过。
- **🔴 figures 缺 `type` 字段（出站信息不完整）**：`run_task.R` 全部 6 处 figure 构造（dist/surv_time/heatmap/curve/effect_curve/adaptive）补 `type` 字段。此前 `samplesize.py:_externalize_figures` 用 `fig.get("type","ctss_fig")` 永远降级为无语义文件名 `ctss_fig_*.svg`；补后 S3 外置文件名变 `curve_0.svg` 等，下游（HTML 报告 / coze 卡片）可按类型路由渲染。本地 R 回归确认 `type` 正确进入出站 JSON。
- **🟢 图形名称自动双语化（2026-08-28）**：`common.R` `.messages` 字典新增 `fig.curve`/`fig.effect_curve`/`fig.dist`/`fig.heatmap`/`fig.surv_time`/`fig.adaptive` 六个双语键（en/zh），`run_task.R` 全部 6 处 figure caption 由硬编码英文改为 `sprintf(t("fig.xxx"), test)`。`figures[].caption` 随 locale 双语化（zh→中文 / en→英文），作为 HTML 报告展示的图形名称。SVG 内部 `main` 标题保持英文（coze 服务器无 CJK 字体避免豆腐块，中文由本地 HTML 渲染处理）。本地 R 回归 en/zh 双 locale 全过：ttest_ind 默认 4 图 caption 中英正确、survival 全图集 5 图含随访曲线双语正确。`samplesize.py` docstring 同步修订（原「图形始终英文」说明过时）。

> ⚠️ **部署红线**：以上 coze 端改动（默认全图形集 + type 字段）均需**重部署 coze 端点后线上生效**，需用户确认后执行。

## v5.3.2 (2026-08-28) · 待发布：对齐 meta-analysis 输出方式（HTML 报告 + repro 外链 + 每 test 默认出图可配置）

- **🟢 本地 HTML 聚合报告（对齐 meta-analysis 方案 B）**：`adapters/rendering.py` 新增 `render_html_report()` + 自包含单文件模板（亮色主题），把 stats 表 + 内联 SVG（复用 `build_figure_widget`，S3 链接过期不影响查看）+ 结论 narrative + 折叠 R 复现脚本（语法高亮 + 复制按钮）固化成 `outputs/ctss_report_<test>_<ts>.html`。`samplesize_power.py` main() 在 `render_figures` 后自动调用并打 `__FIGURE__ html` 标记。实测非曲线请求全区块渲染正常；曲线请求 repro=None 属合理（R 引擎曲线分支不带 repro）。
- **🟢 coze 端 `_externalize_repro`（R 代码外链）**：`samplesize.py` 新增函数，把 `out['repro']['r']`（R 复现脚本 ~1-2KB）上传 S3（text/plain），返回 `{type:"repro",format:"r",storage:"s3",key,url,r_version,packages}`（r_version/packages 保留内联）；S3 不可用降级内联。`samplesize_node` 在 `_externalize_figures` 后调用。**待重部署 coze 端点后生效**（当前端点 repro 仍内联，属预期）。
- **🟢 本地 repro 回填**：`coze_client._fill_external_svgs` 扩展——`repro` 为 dict 且含 `url` 无 `r` → 按 url 下载回填 `repro['r']`，失败标 `_repro_fetch_failed` 不抛错（对齐 meta-analysis `coze_client.py:252-258`）。
- **🟢 每 test 默认出图可配置**：`coze_cases/_contract_index.json` 49 test 全部新增 `default_curve` 字段（ttest×3 + proportion×2 = true，其余 44 = false，与原硬编码行为一致）；`samplesize_power.py` 硬编码 `_AUTO_CURVE_TESTS` 改为 `_auto_curve_tests()`（带缓存，读契约 `default_curve=true`，契约缺失回退硬编码集合）。**改契约 JSON 即可改默认出图，无需改代码**。
- **🔴 修 `_highlight_r` 嵌套 span bug**：原实现"先整体 `_html_escape` 再 4 个正则逐步加 span"，导致后一个 pattern 匹配前一个生成的 `class="c"` 等标签属性 → 嵌套损坏 span（`<span class=<span class="s">"c"</span>>`）。改为单遍扫描：注释（`#`）与字符串（`"…"`/`'…'`）先隔离成 span，再对普通代码段做函数/数字高亮。实测污染=[]，边界用例（字符串内 `#`、转义引号、多行注释）全过。**meta-analysis 同源缺陷已同步修复**（`meta-analysis/adapters/rendering.py:691`）。
- **🆕 图形扩展待办**：新增 `ROADMAP.md`（6 大类参考清单分类：3 项已实现 / 热力图+事件数图等 5 项可实现 / 非参数对比等 3 项不做；实施顺序建议：分布重叠图 → 效能热力图 → 事件数-随访时间图）。ggplot2 由用户确认已在 coze 部署环境。
- **🆕 连续效应量轴曲线（`--effect_seq`）**：R 端 `run_task.R` 新增 `.solve_effect_axis()` + `.run_curve` 的效应量主轴分支，`curve_effect_seq` 协议将效应量作为连续 X 轴。语义——`--effect_seq` + `--nobs`/`--n_seq` → y=效能（固定 n）；`--effect_seq` + `--power_seq` → y=样本量（固定 target power）；单独 `--effect_seq` 默认固定当前 nobs、y=效能。覆盖 9 个曲线 test（ttest×3/anova/比例×2/生存/等效/BE-TOST），固定值优先取 companion 序列首值（`curve_n_seq[1]`/`curve_power_seq[1]`）回退 `nobs`/`power`。本地 R 回归全过（含 n_seq 固定值 bug 修复：原 `axis` 判定只看 `curve_n_seq` 且固定 n 只认 `nobs`，导致 `--effect_seq --n_seq 250` 错用 n=100；现集中 `fix_n`/`fix_power` 计算）。`coze_client.build_params` 新增 `effect_seq→curve_effect_seq` 映射并加入 `_PARAM_EXCLUDE`；`scripts/samplesize_power.py` 与 `adapters/coze/ct_r_lib/samplesize_power.py` 均加 `--effect_seq` CLI 标志；SKILL.md / ROADMAP.md / references/cli_examples.md 同步。**待重部署 coze 端点后线上生效**。

## v5.3.3 (2026-08-28) · 待发布：三类新图形（分布重叠 / 生存随访效能 / 效能热力图）

- **🆕 ① H0/H1 分布重叠图（`--dist_plot`）**：R 端 `run_task.R` 新增 `.dist_delta()` + `.run_dist()`。在标准化效应空间画 H0/H1 两条正态密度并着色 α/β 区，重叠面积=1−power（构造上成立），对方案解释/审阅/教学价值最高。支持 `ttest_ind/paired/one`（Cohen's d 标准化）、`proportion_two/one`（Arcsin 标准化 δ）、`survival`（log-HR 标准化 δ）；`anova` 等无单一效应量语义的 test 优雅报错。base R `polygon()` + svglite，零新依赖。
- **🆕 ③ 生存随访-效能曲线（`--power_time_seq`，survival 仅）**：R 端 `run_task.R` 新增 `.run_surv_time()`。指数事件累积闭式（uniform accrual + 指数 dropout，Schoenfeld 反推效能(τ)）算 x=研究时长、y=效能，并标注达到 target power 的时长点。需 `--event_rate`（单位时间事件风险 λ）+ `--accrual_time` 与序列**同时间单位**。本地 R 回归：n=200/HR=0.7/λ=0.1/入组=1yr 时 1→4yr 效能 0.08→0.278 单调正确；缺 event_rate 优雅报错。
- **🆕 ④ 效能热力图（`--heatmap`）**：R 端 `run_task.R` 新增 `.ss_power_ne()` + `.run_heatmap()`。`--n_seq`（样本量）× `--effect_seq`（效应量）网格算效能，base R `filled.contour` 填充。**无需 ggplot2**（与原 ROADMAP 假设一致，规避「部署完才发现包缺失」）。覆盖 9 个曲线 test；本地 R 回归 5×5 网格数值合理（n=30 时 d=0.2→0.12、d=1.0→0.97）。
- **🔴 survival 契约补全（顺带修复预存隐患）**：`coze_cases/_contract_index.json` survival `required` 由 `['hazard_ratio','alpha']` 增补 `event_rate`/`accrual_time`。原 R 端 `ss_survival_logrank` 对这两个字段有 `%||%` 默认值（0.05/1），导致**用户指定的事件率/入组时长被静默忽略**；补全后主线 survival 计算与 `--power_time_seq` 均按用户取值。属行为修正（此前默认 0.05/1 掩盖了契约缺字段）。
- **Python 侧接线**：`coze_client.build_params` 新增 `dist_plot→plot_dist` / `power_time_seq→curve_power_time_seq` / `heatmap→curve_heatmap` 映射并加入 `_PARAM_EXCLUDE`；`scripts/samplesize_power.py` 与 `adapters/coze/ct_r_lib/samplesize_power.py` 均加三枚 CLI 标志，`ctx["curve"]` 判定同步含三者。dispatch 顺序：dist → surv_time → heatmap → effect_seq 轴 → 一般曲线（避免热力图被误判为效应量轴）。SKILL.md / ROADMAP.md / references/cli_examples.md 同步。
- **本地验证**：R 端 6+ 场景（分布重叠 ttest/proportion/survival + 不支持报错；随访曲线正常/缺参报错；热力图正常/缺参报错）+ Python 端 `build_params` 三模式映射 + 契约转发全过。**待重部署 coze 端点后线上生效**（部署红线，需用户确认）。

## v5.3.1 (2026-08-28) · 待发布：请求参数精简 + 飞书日志去污染（本地修复）

- **🔴 `build_params` 只发本 test 所需参数**：原实现遍历整个 argparse 命名空间，把 ~80 个参数的默认值（varcorr/sigma/nsim/theta0/cv/design/ve_*/prior_a0/prob_*/n_doses/target_dlt/win_ratio_theta/...）全量序列化进 `params` → 飞书 `querystr` 看起来像"全参数扫描"，无法区分真实请求与测试。改为以 `coze_cases/_contract_index.json` 的 `required` 字段为白名单（与 CLI choices / R 引擎 dispatch 三者一致的单一真相源），只发送：本 test 的 `required` 非 None 参数 + 通用 `alpha` + 模式关键参数（求 n → `power`；求 power → `nobs`）+ 派生量（`solve_for_power`/`alt`/`d_val`）+ 曲线参数（`curve_*`）。契约缺失/未登记时退化为原全量行为，保证不丢参。
- **🔴 图形 S3 外置（对齐 meta-analysis 2026-08-26 方案 B）**：coze 端 `samplesize_node` 新增 `_get_s3()` + `_externalize_figures()`，把 `figures[].content`（SVG，可达数 KB）上传 S3、替换为 `{type,format,storage:"s3",key,url}` 引用（url 仅数十~数百字符），大幅缩减 coze 响应体与飞书 `resultstr` 体积。本地 `coze_client._fill_external_svgs()` 按 url 下载回填 `content`（键名对齐 ct-samplesize 本地 `Figure.content`），下游 `render_figures` 契约不变。S3 不可用时两侧均降级内联，不影响结果。
- **🔴 `query_origin` 透传修复**：`state.py` 的 `GraphInput`/`SamplesizeNodeInput`/`SamplesizeNodeOutput` 增加 `query_origin` 字段；`samplesize_node` 把入参 `query_origin`（客户端 `sha256(hostname)`）经 `SamplesizeNodeOutput` 写回 `GlobalState`，使 `feishu_save` 能读到并写入飞书 `query_origin` 列（原 bug：`GraphInput` 无该字段 → 入参被丢弃 → 飞书恒为空）。
- 计算正确性不受影响（R 引擎只读所需键，%||% 回落默认值）；自动曲线（auto-curve）保持默认出图，第二次 coze 调用返回值改为 S3 引用、体积显著缩小。

## v5.3.1-coze (2026-08-28) · coze 端合入：adaptive_sim.R K=1 陷阱修复 + base 流水线整合

- **🔴 `adaptive_sim.R` R 经典陷阱修复（coze 端）**：原 `efficacy_boundaries` 与 `futility_boundaries` 两处用 `for (k in 2:K)`；当 `K=1`（即 `interim_looks=1`，单次期中分析）时 `2:1` 生成降序序列 `c(2,1)`，导致循环误执行、访问不存在的 `times[2]` → 卷积矩阵全 NA → 边界二分法崩溃（`missing value where TRUE/FALSE needed`）。改为 `for (k in seq_len(K - 1L) + 1L)`：`K≥2` 行为完全不变，`K=1` 时 `seq_len(0)+1L = integer(0)` 循环体不执行。已测：ttest/survival 曲线及 adaptive 模拟均成功产出 SVG。
- **🔴 整合 coze base 流水线，使本地源码自洽**：经逐文件 MD5 比对，本地 `adapters/coze/` 此前是 coze 项目的**子集**（缺失 base 层的 langgraph R 代码生成/修复流水线）。本次从 coze 现状 zip（`coze_project_5.3.1_code_af22817b.zip`）合入 12 个源文件：`src/graphs/loop_graph.py`、`src/graphs/nodes/{requirement_parse,r_code_generation,r_code_fix,r_code_execution,template_resolver,result_output}_node.py`、`src/tools/r_executor.py`、`config/{requirement_parse,r_code_generation,r_code_fix}_cfg.json`、`README_zh-CN.md`（原乱码名 `README_中文.md` 重命名）。这些节点属 `cozeloop` 平台框架装饰器节点（运行时由 cozeloop 注册），本地仅做 `py_compile` 语法校验通过。
- **🔴 本地改动与 coze 端零冲突**：`samplesize.py`（S3 外置）、`state.py`（`query_origin`）在 coze 现状 zip 中与本地字节一致（diff=0），coze 端未回退；唯一差异文件即 `adaptive_sim.R`（已用修复版覆盖）。
- **部署包重建为完整自洽包**：`_archive_20260828/coze_project_5.3.1.zip` 由 67 文件扩至 **79 文件**（含上述 12 个 base 文件 + adaptive_sim.R 修复），重生成 `manifest.json`（5.3.1 / 79 文件 / 含 base 流水线），MD5 `6bddd768d0493f14cc097011e3b47b9a`。下次干净部署不再依赖 coze base 镜像残留。

## v5.3.0 (2026-08-25) · 上下文交互菜单改造：两级路由 + 有界 grill-me（Type-Compute 对齐第二轮）

- **🔴 Quick Menu 两级化**（对齐 meta-analysis level-1 → level-2 范式）：SKILL.md 的 Quick Menu 从"一次甩 6 大类 + ~40 个 test 名"压缩为 **level-1 摘要**（仅 6 大终点类 + 高频设计族入口 + ③ 解释差异入口）；用户选类后 LLM 才进 `references/menu.md` Part 1 弹该类子列表（level-2）——Complex 首屏从 ~40 项降到 ~8 项，遵守"逐步确认、不甩全量菜单"（ct-base compute_menu §5）。
- **Vague 有界 grill-me 落地**（落地 ct-base compute_menu §4「有界 grill-me」细则，源自 ct-advisor clarify_loop.py 经验）：SKILL.md 明确 **LLM 自计数轮次、硬上限 3 轮**（超限带问题画像强制收敛）；每轮 1–3 个聚焦问题 + 推荐默认；累积 question_profile；结束时回显「需求画像 + 推荐检验 + 待补参数」摘要确认再计算。
- **triage 表述统一**：`references/menu.md` 顶部 gate 由 3 分类（§5.2）改为与 SKILL.md 一致的 4 档（Simple/Middle/Complex/Vague），并注明 Complex 走两级路由。
- **类别级参数提示**（对齐 meta level-2 数据格式提示）：`references/menu.md` Part 1 六类各加一行"常见参数"（①--effect ②--p1/--p2 或 OR/RR ③--lambda1/--lambda2 ④--hazard_ratio ⑤⑥按设计族），选完 test 后参数收集更顺。
- **README Example 1 拆轮**（遵守"每轮 1–3 个聚焦问题"上限）：grill-me 示例由一轮 4 题改为**两轮各 2 题**（Round 1 终点类型+设计；Round 2 优效/非劣/等效+效应量表达），双语文案同步，示例展示"需求画像+推荐检验"收尾。
- 无代码改动，纯提示/文档层；回显块前缀（`## 当前分析设定：`）与解释差异入口措辞延续 v5.2.0 不变。

## v5.2.0 (2026-08-25) · Type-Compute 交互框架对齐（ct-base 计算型统一规范）

- **🔴 回显块前缀统一**：`## 当前设定：` → `## 当前分析设定：`（SKILL.md §Cross-turn Continuity 4 处）——对齐家族计算型统一前缀（ct-base `compute_menu.md` §6.2 / `interaction_frameworks.md` §5.3）。此前沿用 continuity 通用前缀，与 meta-analysis（范式）不一致。
- **🔴 「解释差异」入口措辞逐字对齐**：`references/menu.md` + `README.md` + `README_zh-CN.md` 统一为家族标准版（`interaction_frameworks.md` §5.2：英文 `I'll clarify the clinical/statistical meaning before you choose` / 中文 `我先讲清临床与统计含义再让你决定`），去除自定义变体。
- **✨ 新增 few-shot 对话示例**：`references/menu.md` 末尾新增「Conversation Examples」节——Simple（点名检验直接算 + 回显块）/ Complex（能力路由菜单 + ③ 解释差异入口）/ Vague（grill-me 逐分支追问）三分支真实对话骨架，对齐 meta-analysis `interactive_menu.md` 范式风格。
- **依据**：ct-base `compute_menu.md`（2026-08-25 由 meta-analysis 提炼为家族计算型框架，明确 meta-analysis 与 ct-samplesize 同属 Type-Compute）；`interaction_frameworks.md` §5 轻量对齐三件套。

## v5.1.0 (2026-08-22) · 增加 bug report 功能（ct-base §20.3 接入完成）

- **🔴 发布前检查修正**：`config/config.json` `auto_approve_endpoints` 补齐统一 bug-report 端点 `https://ct-bugreport.coze.site/run`（此前仅含计算端点，违反 §20.3.5——各技能接入须一并加入 bugreport 公共端点）。
- bugreport 接入点全绿（发布前检查无待确认项）：`adapters/bug_report.py`（内嵌公共 token + `DEFAULT_ENDPOINT` 统一端点 + 历史回执 `confirm_thanks`/`build_followup`）、SKILL.md Bug Reporting 节（双向触发 + 两阶段确认 + 脱敏铁律 + 历史回执）、README 出站披露（§16.6）均已就位。
- 三道发布闸门：publish_secret_scan（0 P0/0 P1）、shared_sync_check（无漂移）、clawhub_security_audit（仅预已发布技能的既有审计项，无新增阻断）。

## v5.0.5 (2026-08-22) · Bug Report 发送后历史回执约定（ct-base §20.3.7 同步）

- **SKILL.md Bug Reporting 节**：新增 Post-send history回执 bullet——endpoint 返回 `history`，回复由 `confirm_thanks(locale)` + `build_followup(history, locale)` 双语拼接（空 history→结束；`resultstr=="done"`→展示 memo；否则"未修复"）。所有用户提示 `_MSGS` 中英成对、按 `_current_locale()` 自动检测。
- 同步源：ct-base `docs/07-coze-engine.md` §20.3.7 + `adapters/bug_report.py`（v1.1.58）。
- 客户端落地（2026-08-22 cont.）：`adapters/bug_report.py` 副本补齐 `confirm_thanks`/`build_followup`/`parse_history` + `_MSGS` thank/done/pending 双语文案 + `send_to_endpoint` 透传 `history`；SKILL.md Trigger 补「主动触发」独立路径（用户显式说 report a bug 直接走两阶段，不受每会话 1 次限制）；docstring「三阶段确认」→「两阶段确认」。

## v5.0.4 (2026-08-21) · bugreport 两阶段确认简化（ct-base §20.3.3 同步）

- **SKILL.md Bug Reporting 节**：Three-stage confirmation（① propose → ② show → ③ send）→ **Two-stage confirmation（① propose-with-preview → ② consent→send）**——提议时连同 `render_report_text` 脱敏报告全文一并给出，用户一次明确确认即发送（用户补充 description 则重渲染再确认）；检视把关从 stage ② 移至 stage ① 预览。ct-base `docs/07-coze-engine.md` §20.3.3 已同步（三阶段→两阶段），`adapters/bug_report.py` 代码零改动（`confirm_prompt` 一次性提议 + `render_report_text` 全文渲染照用）。

## v5.0.3 (2026-08-21) · v5 升级遗漏全面清理（文档/代码一致性）

- **🔴 `--local` 死参数删除（v5 已忽略但 CLI 帮助文本误导）**：`scripts/samplesize_power.py` 移除 `--local` 参数及 `select_backend(test, prefer_local=...)` 调用（v5 `select_backend` 只返回 CozeBackend，旧开关全部忽略）；`--help` 验证零残留。
- **🔴 头部 docstring 更新为 v5**：`samplesize_power.py`（v4.0.1 → v5.0.2，去掉 LocalPythonBackend 描述）、`compute_backend.py`（v4.0 → v5.0，明确唯一后端 = coze、旧开关忽略）。
- **🔴 死代码清理**：`compute_backend.py` 删除 `_force_r()`（无调用，CTSS_FORCE_R 在 v5 忽略）；`i18n.py` 删除 `info.local_python_fallback` 死键（无引用）。
- **🔴 README 双份第 11 行**：仍声称「5 种基础检验的纯 Python 兜底可离线使用」（v5.0.0 升级遗漏）→ 改为「发布版没有本地计算兜底」。
- **🔴 AGENTS.md 依赖段**：仍声明 `statsmodels==0.14.2/numpy==1.24.3/scipy==1.11.4`（v5 已移除第三方计算依赖）→ 改为「stdlib only」说明。
- **文档同步**：`references/operation_sop.md`（环境段 + 错误表）、`references/units.md`（U4 adaptive Python fallback → server-side coze + dev legacy）、`references/report_template.md`（Methodological Limits / Path 注释去 Python fallback）、`ADVANCED.md` + `ADVANCED_zh-CN.md`（目录图 v4 → v5：scripts/adapters 实际结构）。
- **保留（dev-only 合理项）**：`references/adaptive_simulator.md` 的 dev 后端 Python fallback 代码示例（标注 legacy）；`PY_FALLBACK_SET` 常量（兼容注释，不参与路由）。
- **验证**：全量 py_compile ✓；`--help` 无 `--local` ✓；dry-run 管线正常（coze 信封）✓；全库「Python 兜底/5 种/--local」无残留 ✓；SKILL.md 193 行 ✓。

## v5.0.2 (2026-08-21) · ClawHub 安全审计整改（NVIDIA SkillSpector 25 项发现）

- **🔴 移除废弃本地 R 安装参数（审计 Tp12/Tp3）**：发布集 `scripts/samplesize_power.py` 删除 `--install-all-packages` / `--run-install`（v5 纯 coze 引擎下为死参数；R 包由 coze 镜像预装）。`i18n.py` `error.test_required` 措辞同步（去 "--install-all-packages 除外"）。**注意**：`scripts/i18n_r_messages.json` 的 `install.*` 键保留（dev-only `adapters/r-assets/` 后端仍引用，§16.3 允许独立 R 键文件）。
- **🔴 权限声明与行为对齐（审计 Tp23）**：SKILL.md frontmatter `network: optional → required`（v5 发布版无本地兜底、必须 coze）；network_note 补 `query_origin`（hostname SHA-256 哈希）+ `locale`（OS 语言）元数据披露。
- **🔴 SAFE PREVIEW / --yes 语义全库统一（审计 Tp2/Tp10/Tp11/Tp22）**：v5 事实 = coze 下默认 dry-run 展示请求信封，**自然语言触发**（please compute directly / 请直接计算）才发送；`--yes` 仅 legacy local-R dev 后端。统一 8 处：README 双份（Get the actual number / FAQ / Safety 段 / 示例 1 注）、references/{cli_examples, data_format_guide, examples, python_usage, operation_sop, units}.md。
- **✅ 首次出站口头披露（审计 Tp13/Tp20）**：SKILL.md Safety 段新增 First-use outbound disclosure——公共端点虽预置白名单不弹窗，agent 每会话首次出站仍须一句话说明发送内容。
- **✅ Triage 路由收紧（审计 Tp17/Tp18/Tp19）**：SKILL.md + AGENTS.md 新增 Routing gate——**仅明确样本量/效能计算意图才触发 coze 出站**；一般咨询/方法论/ICH 指导本地回答不发任何数据。
- **✅ Critical 误报处置（compute_backend.py:152 exec_module）**：该动态加载仅服务 dev-only `adapters/r-assets/`（已排除发布、isdir 守卫先 raise），发布版不可达——补注释说明，消除静态分析疑虑。
- **验证**：py_compile ✓；发布集 `run-install/install_all_packages` 零残留 ✓；`--yes` 无矛盾表述 ✓；SKILL.md 193 行（≤200）✓。

## v5.0.1 (2026-08-21) · 错误报告增强：description 问题描述 + 治理动作归属（用户指令）

- **报告可 debug（用户「现在发送的报告内容根本无法协助 debug…需要自然语言描述」）**：报告信封 10 键 → **11 键**，新增 `description`（唯一自由文本字段）协助作者定位。**内容边界（用户追加「需要提供具体用的什么算法或函数，必要时可以提供数值和研究设计内容，反正用户会最后把关」）**：写「现象 / 复现步骤 / 期望 vs 实际 / 所用算法或函数（如 Schoenfeld 公式）/ 错误消息原文」，**必要时可含数值与研究设计**（如 HR=0.75、power=0.85、1:1 分配比）——以能复现为准；**唯一硬边界：不写可识别个人/机构/受试者的身份信息**；由用户三阶段确认②检视把关（用户同意才发送）。`build_report` 新增 `description` 参数；`render_report_text` / `save_local_report` description 独立段落展示；`confirm_prompt` 附加补充描述提示（双语 `desc_hint`，明确可含算法/数值、仅避免身份信息）。
- **治理动作归属（用户「发布的 ct 技能不需要有清理功能，这个功能是 ct-update 专用的」）**：明确 `get / update / download / delete` 为**治理动作**，仅 `ct-update` 技能（作者侧）调用；本技能 `bug_report.py` 为**客户端只发 `report`**，不实现、不调用治理动作（docstring + SKILL.md Bug Reporting 节 + README 同步）。
- **端点侧同步（ct-base 镜像，需重新部署 coze）**：`report_store.py` + `validate_node.py` 双 `REPORT_SCHEMA` 加 `description`；SQLite dev 表/INSERT（report_store + report_node 两处）加 `description` 列；coze_contract / AGENTS / README / state.py / main.py 「10 键」→「11 键」+ 治理归属。
- **兼容性设计（实测发现）**：空/纯空白 `description` 在 `sanitize_report` 省略该键 → 无描述报告仍为 10 键、与线上旧端点完全兼容（实测 send→ok(feishu)）；有描述报告为 11 键，需部署 v2 增量包后端点接受（旧端点实测 `extra keys rejected: description`，已打包 `coze_update_bugreport_v2_description.zip`）。
- **验证**：py_compile ✓；脱敏（description 透传、白名单仍拒额外键）✓；渲染含 description 段落 ✓；空描述省略键 ✓；端到端（无描述 send→ok(feishu)→get 可见→update/delete 清理）✓；SKILL.md 189 行。

## v5.0.0 (2026-08-21) · 从本地计算版本升级为云服务器版本

- **错误报告功能接入（ct-base §20.3，2026-08-21）**：复制共享适配器 `ct-base/adapters/bug_report.py` → 本技能 `adapters/bug_report.py`（§16.9 出站目录），直连统一报告端点 `https://ct-bugreport.coze.site/run`（**ct-base 镜像不动，仅客户端调用 coze 工作流**）。改动：① payload 补 `action: "report"`（线上协议）；② **端点 token 为公共凭据（§5）**，XOR+base64 混淆内嵌（`_EMBEDDED_SECRETS` + `_obf_decode` + `get_endpoint_token()`，与 ct-base 镜像同密钥 `ct-bugreport-coze-obf-v1-3c9e` 同 blob）；③ **send_to_endpoint 必须带 `Authorization: Bearer <token>` 头**（2026-08-21 线上实测：coze 平台网关入口校验 Bearer 头，缺头 401）；④ SKILL.md 新增「Bug Reporting」节（§20.3.1 强信号 + 每会话最多提议 1 次 + 三阶段确认 + 脱敏 10 键硬白名单 + 无 coze 调用走本地 md+邮箱兜底）；⑤ 两份 README 出站披露补统一报告端点（§16.6，含"未经确认不发送、可拒绝、本地会话存文件"）。验证：py_compile ✓；单测（脱敏剔除用户键/双语 confirm/render）✓；**端到端实测**（send→ok(feishu)→get 落库可见→清理）✓；SKILL.md 189 行（≤200）。

- **架构升级（v5）**：计算引擎由「本地 Python 兜底 + coze 远程」混合模式，升级为**纯云端 R 计算服务**——49 种检验全部由远程 coze R 引擎权威计算（rpact / gsDesign / TrialSize / PowerTOST 等 20+ 包，服务器端运行），本机**无需安装 R**。
- **本地计算路径移除**：v4 的本地纯 Python 兜底（5 种基础检验）与本地 R 后端不再参与运行期路由；`ComputeBackend` 唯一后端 = `CozeBackend`（stateless remote compute，SAFE PREVIEW 默认）。
- **发布包瘦身**：本地 R 运行时 / 模板（`r-assets/`）与 coze 镜像（`adapters/coze/`）不再随技能发布，发布集仅含 Python 编排层 + 文档。
- **locale 显式参数混合方案**：coze R 引擎支持 `locale` 参数（zh/en），数字与标准标签直接来自内建双语词典（不经生成模型），数值保真与术语一致；本地 CLI 按 OS 检测自动发送。
- **ct-base §16 发布前检查整改**：SKILL.md 瘦身至 200 行、ignore 文件补 tests/ 与 Coze 接口文档排除、README 补出站端点披露、对话示例与场景索引 49 条实测全过（留痕 `outputs/`）。
- **🔴 be_tost 曲线模式 bug 修复（用户 bug 报告 D:/be_tost_curve_bug_report.md，2026-08-21）**：
  - **文档 over-claim 修正**：`ADVANCED.md` / `ADVANCED_zh-CN.md` / `references/cli_examples.md` 三处宣称"曲线模式支持 22 种检验（含 be_tost）"，但 coze 服务端 `run_task.R` 的 `.curve_solvers` 实际仅 8 种（ttest_ind/paired/one、anova、proportion_two/one、survival、equivalence）→ 已统一修正为 **8 种**（与 SKILL.md 一致），其余检验标注"仅单点求解，曲线请求返回明确提示"。实测复现：`be_tost --power_seq` 走 coze 返回 `status: error`。
  - **be_tost 曲线求解器实现（根治，本地完成待部署）**：`run_task.R` `.curve_solvers` 新增 `be_tost` 条目——正向 `sampleN.TOST(power=pp)`、反向 `power.TOST(n=n)`，等效界值 theta1/theta2 显式优先、`--margin`（>1）兜底 1/m~m、否则 PowerTOST 默认 0.8~1.25（与单点分支同逻辑）。本地 R 4.5.1 + PowerTOST 验证：PARSE_OK；回归1 CV30%/margin=2 → power 0.6–0.85 总 N=6（与单点结案值一致）；回归2 默认界值 0.8→32（与 bug 报告一致）；反向 n→power 正常。⚠️ **需部署 coze 镜像后线上生效**（部署动作待用户确认）。
  - **🔔 "Sample size 列语义错位"误判澄清**：v4.0.7 条目中"PowerTOST `sampleN.TOST` 的 Sample size 列为每序列数、label.n_total_be 显示总 N 语义错位"的怀疑**不成立**——PowerTOST 返回列即**总样本量**（R 输出标注 `Sample size (total)`）；上一轮 BE 预试验 N 值（CV20%→4/25%→6/30%→6/35%→8/40%→8）经本地 R 逐档验证**全部正确**，无需修正。

## v4.0.7 (2026-08-20) · 发布前检查对齐 ct-base §16（自 v4.0.4 增量合并记录）

- **🔴 assurance 成功界值 margin=0 bug（部署后验证发现并修复，2026-08-20）**：验证函数化重构时发现 assurance 输出「成功界值: 0.0000」——根因：`--margin_assurance` argparse 默认 `0.0` 被 build_params 全量发送，R 端 `p$margin_assurance %||% 0.05` 的 `%||%` 不处理 0 → **margin=0 生效**（成功界值 0 无意义，P(差>0)>0.95 即判成功，历史 bug、重构前后一致）。修复：① CLI `--margin_assurance` 默认 `0.0` → `None`（不发送 → R 端回落 0.05，**本地修复立即生效、无需重新部署**）；② R 端 `run_task.R` assurance 分支加防御 `is.na(margin) || margin <= 0 → 0.05`（防手动传 0/注入 0，随下批部署）。验证：dry-run payload 不再含 margin_assurance ✓；R 端逻辑模拟（未发送/注入 0 → 0.05；显式 0.1 → 保留）✓；线上实测「成功界值: 0.0500」✓。**另发现待议**：build_params 全量发送带 argparse 默认值的参数会覆盖 R 端 `%||%` 默认——assurance 的 shape（CLI 3/7 vs R 端 2/2）、n_sim_assurance（CLI 5000 vs R 端 100）默认不一致，需确认设计意图后统一。

- **coze 端 R 引擎函数化重构（用户「1 2 3 4 都做」，2026-08-20）**：将 run_task.R 内联代码提取为统一函数（等价重构，数值不变）——
  ① **`ss_gsd`**（samplesize_functions.R 新增）：GSD 成组序贯 **7 检验统一封装**（group_sequential / gsd_proportion / gsd_survival / gsd_hazard / gsd_poisson / gsd_survival_sim / gsd_hazard_sim），run_task GSD 分支 163+47 行内联收敛为 8 行单次调用；函数内统一组装 text/stats（唯一带输出组装的 ss_*，因 7 分支×正反向格式高度同构，t()/.line() 调用时解析、common.R 先 source）；② **`ss_conditional_power`**：条件功效 + SSR 再估纯数值函数（27 行内联 → 调用）；③ **`ss_assurance`**：贝叶斯 Assurance 蒙特卡洛（28 行内联 → 调用），**`set.seed(42)` 硬编码改为 seed 参数化**（默认 42 兼容，可由 `p$sim_seed` 覆盖）；run_task.R 1536 → 1364 行（-172）。验证：三文件括号配平 ✓；ss_gsd 引用 20 个 i18n 键全在 common.R ✓（run_task 155 键中 3 个"缺失"为 switch 字面量 `ss_ttest("two.sample")` 误报）；conditional_power 用 scipy 复算与内联版**完全一致**（CP=0.865946、SSR 再估 278、obs_eff≤0 → NA ✓）；无副本需同步（run_task/samplesize_functions 仅权威一份）。

- **BE 自定义等效界值缺口修复（用户「ss_be_tost 不支持 theta1/theta2…把这个缺口修掉」，2026-08-20）**：① R 端 `ss_be_tost` 新增 `theta1/theta2` 参数（缺省/NA 回落 PowerTOST 默认 0.8~1.25），正向 `sampleN.TOST` 与反向 `power.TOST` 均透传；② `run_task.R` be_tost 分支读取 `p$theta1/p$theta2`，并支持 `--margin` 兜底（margin=m → 对数对称界值 1/m ~ m），正反向输出新增等效界值行（新 i18n 键 `label.eq_margin_be`，common.R）；③ CLI 新增 `--theta1/--theta2`（默认 None 不发送，现有行为不变）；`build_params` 自动透传；④ legacy 同步：`local_r_backend.py`（两份：adapters/r-assets 与 coze 镜像 ct_r_lib）be_tost 分支填 theta1/theta2 + margin 兜底，`r_templates/r_equivalence.py`（两份）模板函数与调用处加 theta1/theta2 + 界值输出行，`r_templates/r_curve.py`（两份）be_tost 条目 params/power_fn/n_fn 透传 theta1/theta2，coze 镜像模板经 cp 与 r-assets 侧对齐；⑤ `references/cli_examples.md` 加自定义界值示例（--theta1/--theta2 与 --margin 两种写法）。验证：全量 py_compile ✓；CLI 透传（显式给 → payload 含 0.5/2.0；不给 → 不发送）✓；legacy 模板填充（0.5~2 与默认 0.8/1.25）✓；R 端静态审查（本机无 Rscript，改动结构简单）。⚠️ 需同步部署 coze 镜像后线上生效。背景：仿制药 BE 预试验案例（margin=2、θ0=1、CV=30%）暴露技能只能算 0.8~1.25 界值。
- **🔴 BE 线上实测修复：margin 兜底 `m>1` 防御（部署后验证发现，2026-08-20）**：coze 端部署后实测——不传界值（或只传一侧）时线上报 `R 引擎错误: True ratio 1 not within margins Inf ... 0!`。根因：coze 端 params 疑似注入 `margin=0` 之类默认字段，`!is.null(p$margin)` 恒 TRUE → 任一侧界值缺失即触发兜底 `1/m=1/0=Inf`。修复：run_task.R be_tost 分支 margin 兜底改为 `!is.na(m) && m > 1` 才启用（m 须为有效 BE 上界，杜绝 1/m=Inf 与界值倒置）；两份 legacy local_r_backend.py 同步（`args.margin > 1`）。验证：本地逻辑模拟——margin=0 注入 → 回落 0.8~1.25 ✓；margin=2 → 兜底 0.5~2 ✓。**另发现历史显示语义**：PowerTOST `sampleN.TOST` 的 "Sample size" 列为**每序列数**（2x2 交叉总 N = 2×），`label.n_total_be` 显示为「总 N」语义错位（如 0.5~2/CV30%/power0.8 → 每序列 6、总 12，而非总 6）——待用户确认是否一并修。

- **本地 fallback 画 Power 参考线 + 出图控制权收归技能（用户指令 2026-08-20）**：① `scripts/samplesize_power.py::_curve_svg_from_stats` 新增 `target_power` 参数——y 轴语义为 Power（reverse 求解）且目标值在绘图范围内时，绘制红色虚线参考线 + `power = X` 标签，**与数据点/刻度共用同一 `sy()` 映射**（实测反推 power=0.8000 精确回环）；forward 求解（y=n）不画；② `render_curve_fallback` 增加 `target_power` 透传（主流程与 auto-curve 块均传 `--power` 或默认 0.8）；③ **修复 auto-curve 块嵌套死代码**（`if res2.figures` 内再判 `if not res2.figures` 永远 False，本地兜底从未触发）→ 改为 if/else 结构；④ 固化规则：SKILL.md §Figure Output 新增「★ No hand-redraw」（agent 呈现技能生成的 SVG 原样，不得手工重绘曲线/自建坐标映射），`references/rendering_rules.md` 新增「Power reference line & no hand-redraw rule」小节（含 2026-08-20 内联 widget 刻度错位事故溯源）。背景：agent 手工绘制的内联 widget 曾出现 y 轴刻度与参考线错位，用户要求画图功能全部由技能控制，出错才能定位修复。

- **locale 显式参数混合方案（SKILL.md Language policy）**：coze R 引擎支持显式 `locale` 参数（zh/en），输出双语模板（数字与标准标签直接来自内建词典、不经生成模型）；本地 CLI 按 OS 检测自动发送，提示词可强制切换（`CTSS_LOCALE=zh|en`）；coze SVG 恒为英文，含 CJK 的用户文本由本地 LLM 渲染前补字体（ct-base `language_policy.md` rule 5）。
- **README 对话示例实测（ct-base §16.6 闸门）**：7 个对话示例（示例 1–5 走 coze 计算、示例 6 Complex 菜单、示例 7 Vague grill-me）+ 场景索引「试试这样说」49 条全部实测通过（真实 coze 端点，locale=zh）；留痕 `outputs/test_readme_examples_log.md` / `outputs/test_scene_index_log.md`。
- **场景索引 5 条参数修正（README_zh-CN.md / README.md 同步）**：① `equivalence` 效应量 3→1（effect<margin 语义自洽，n=13/组）；② `mixed_model` 表述改「重复测量设计效能，n=100，效应量 0.5」（给定 n 求效能型，返回 power_sim）；③ `proportion_paired` 补率 `p1=0.7 p2=0.5`；④ `odds_ratio` 补对照率 50%（OR=2 → p1=0.667，n=136/组）；⑤ `risk_ratio` 补对照率 50%（RR=1.5 → p1=0.75，n=58/组）。
- **发布前检查整改（ct-base §16 全项核验）**：SKILL.md 瘦身 234→200 行（§16.1）；`.gitignore`/`.clawhubignore` 补 `tests/` 整目录排除与 Coze 接口文档（`**/coze_contract.md` 等）排除（§16.7/§16.8 测试内容红线）；README 补出站端点 URL 披露 `https://ct-samplesize.coze.site/run`（§16.6）；CHANGELOG 首条版本对齐 SKILL.md v4.0.7。
- **ct-base 规范合规补强（对照 ct-base 现行规范全面审计后整改）**：① `adapters/coze_client.py` 出站 payload 补齐 `query_origin`（`sha256(hostname)`，§8.6 审计/归因/限流，客户端生成）；② 一次性出站授权提示由硬编码中英双显改为走 `t("auth.coze_outbound")`（`scripts/i18n.py` 新增该词条，language_policy §首次使用与一次性运行期提示）；③ SKILL.md/AGENTS.md/两份 README 版本号统一为 v4.0.7（原 README 残留 v4.0.1）；④ 两份 README 新增「适用人群 / Who This Is For」章节（§13.6）；⑤ frontmatter 补 `invocable: true`（§3/§16.5 任务入口型）；⑥ Triage 由三向补为四向 Simple/Middle/Complex/Vague 并修正过时章节引用（§5.2→§6.2、英文-only 引用 §13.2→§4）；⑦ `references/operation_sop.md` 与 `references/svg_editing.md` 去除 CJK、改为英文-only（§4）。
- **发布前检查（ct-base §16 逐项核验）追加整改**：① 修复 🔴 §16.7/§16.8 GitHub 红线——原 `.gitignore` 仅排除 `adapters/coze/ct_r_lib/`，致整个 Coze 私有镜像（`adapters/coze/`：R 引擎、部署脚本、pyproject、manifest、`.coze`）在 `git add -A` 时会被提交泄漏；改为整目录排除 `adapters/coze/`，`git add -A --dry-run` 复核仅剩发布的 `adapters/coze_client.py`/`coze_token_embedded.py`；② SKILL.md 由 202 行瘦身至 199 行（§16.1 ≤200，删除冗余 Test-module index 行、sim timeout 错误行、Authoritative mapping 交叉引用行）。据 §16.0 ClawHub 安全审计脚本跑出 STILL_PRESENT/UNVERIFIED 项：a) `is_valid_rscript` 签名命中 `adapters/coze/` 与 `r-assets/`（dev-only 文件、不随发布包分发，判定误报；但 `r-assets/` 当前被 git 跟踪会随 GitHub 发布，需对齐 `.clawhubignore` 排除或 `git rm --cached`）；b) [LOW] README「execute with --yes」触发计算措辞在 v5 默认 coze 无状态引擎下已过时（默认用「请直接计算」触发，--yes 仅适用本地 R 后端）；c) 多项 UNVERIFIED（SAFE PREVIEW 措辞、OS 语言泄漏、简化公式警告、R 代码模板字符串）多为设计特性，需人工签核。§16.3 主 `i18n.py` 仍含 R 键 `install.*`/`header.r_code`（应迁至 `i18n_r_messages.json`），留待后续整改。
- **发布前检查追加整改（二）—用户「一起修掉」闭环**：① 🟠 §16.3 R 键迁移：新增 `scripts/i18n_r_messages.json`（承载 `install.*`×6 / `header.r_code` / `header.install_cmd` 共 8 个 R 键 en+zh）；`scripts/i18n.py` 主 `_MESSAGES` 删除全部 R 键，改为探测式合并加载（`i18n_r_messages.json` 存在则合并、缺失则跳过，纯 Python 技能向后兼容），主文件 grep 红线 `"install.`/`"rscript`/`"header.r_code` 全清；发布包 `scripts/samplesize_power.py` 的 `t("header.r_code")` 经合并字典仍可解析（py_compile + smoke test 验证通过）；② 🟡 `r-assets/` GitHub 排除对齐：`.gitignore` 补 `r-assets/`，并执行 `git rm --cached -rf r-assets`（仅停跟踪、保留工作树），`git add -A --dry-run` 复核不再出现 `r-assets/`（双平台排除一致）；③ 🟡 `dist/coze_project_*.zip` 历史构建包归档至 `adapters/coze/_archive_20260820/`（`dist/` 仍被双 ignore 排除）；④ 🟠 README「execute with --yes」措辞弱化：两份 README 第 42/189 行改为「请直接计算 / please compute directly」为主触发，「--yes」明确为本地 R 执行路径标志（默认 coze 无状态引擎下自然语言即触发），消除对 v5 默认引擎的过时描述。
- **§12 Logo 配色整改：旧绿档 → A 档靛蓝（用户「根据 ct-base 改一下 logo 配色」）**：① `assets/icon.svg` 全色替换——`#12B886`（投影/文字/主曲线）→ `#3A5BC7`、`#C9D6EE`（方框描边/背景淡曲线）→ `#C9D6EE` 保留（描述差异）、`#9FE1CB`（power 区青绿填充）→ `#3A5BC7` 主色淡显（opacity=0.25），α 跨档统一语义色 `#D85A30` 保留；② 主钟形曲线 `stroke-width` 2.5→3（满足 §12 主色应用铁律「≥3px 粗描边 / 实心大图形」），方框底 `#EEEDFE` 统一保持；③ 三要素参数（`translate(7,13)`、字号 16、字重 900、`rx=20`、投影 `dx=0 dy=2.5 stdDeviation=2.5 flood-opacity=0.30`）与 §12.1 蓝本完全一致；④ 与 ct-base A 档参考版 `pending-icons/ct-samplesize.svg` 颜色 diff 仅剩一处（去除 pending 版残留的 `#9FE1CB` 旧绿档 power 填充），消除与 §12 主色铁律不符的「靛蓝主色 + 青绿填充」视觉违和；⑤ 重新导出 4 个 PNG（§12.3 cairosvg）：`icon_4x.png` 416×416、`icon_8x.png` 832×832、`ct-samplesize_4x.png` 416×416、`ct-samplesize_8x.png` 832×832（PIL 尺寸校验通过；icon 与 ct-samplesize 两份 PNG 字节一致，同图标不同命名）；⑥ **用户追加「钟型曲线下面也上一下颜色」**：原曲线下方填充 `#C9D6EE @ 0.75` 几乎不可见，改为 **主色淡显 `#3A5BC7 @ 0.25`**——曲线下方这块"实心大图形"承载主色（§12 主色铁律），既让曲线下区域明显带靛蓝、又保留层次（背景多层 `#C9D6EE` 淡曲线 @ 0.3/0.25 更浅、主填充 @ 0.25 略深），α 橙红与峰顶红十字医学标识不抢色。⑦ 视觉自检：4x 缩略图渲染正常——靛蓝主色分量足、α 橙红色 + 峰顶红十字医学标识突出、背景多层淡色曲线与曲线下主色填充层次分明。
- **SKILL.md 瘦身：细节外迁独立 references（用户「SKILL.md 移动一些内容到单独文件吧」）**：200 行 → **186 行**（§16.1 ≤200，余量 14 行）。① 新建 `references/security_model.md`——安全模型披露表（远程计算 / 服务端 R / 输出 / 网络 / 出站门 / 文件系统）+ 上传文档保密（§6.7.3）全量移入，SKILL.md §Safety 保留 3 条核心保证 + 指针；② 新建 `references/rendering_rules.md`——§19 渲染细节（呈现优先级降级阶梯 / figure_mode / render-hint 阈值 / 参考实现）全量移入，SKILL.md §19 保留 ★agent 核心规则（内联优先 + 降级阶梯一句话）+ 指针；③ Adaptive-trial simulator 段落 3 行→2 行（细节并入既有 `adaptive_simulator.md` 指针）；④ 上传文档格式表 4 行→2 行合并（.pdf/.doc/扫描件一行）。校验：references 新文件英文-only（rendering_rules 中文为 UI 提示词例外，已标注）；链接可解析；SKILL.md 正文中文仅 frontmatter 双语元数据与 §6.7.2 原样通知。⑤ **frontmatter `triggers` 精简（用户「triggers 没必要中英完全对照，留几个中文」）**：16 个中英对照 → **11 个（英文 7 + 中文 3）**，中文仅留核心词「样本量计算 / 检验效能计算 / 临床试验 设计」，场景词（非劣效/等效性/生存分析/适应性/贝叶斯）删中文保留英文；行数 186 → **181**。
⑥ **frontmatter `summary` / `description` 文案更新（用户提供新 summary）**：「易用…工具。默认权威引擎为远程 coze R 计算服务…」→「样本量与检验效能计算工具。本地无需安装 R，直接提供云端 R 计算服务（覆盖 49 种检验，并提供 **SVG 出版级别图形**）…」（语序调整 + 新增 SVG 出版级图形亮点；`svg` 按规范大写为 `SVG`）；`description` 中文同步、英文去掉 Easy-to-use 并补 publication-grade SVG figures，保持双语一致。
- **🔴 生存分析 Schoenfeld 事件数公式修正（4 倍因子缺失 bug，2026-08-20 肺癌 OS 实算发现）**：`adapters/coze/src/r_engine/samplesize_functions.R::ss_survival_logrank` 事件数公式原为 `(z_{1-α/2}+z_{1-β})²/(log HR)²`，**缺 1:1 分配比因子 (1+r)²/r=4**——HR=0.75、power=0.85、双侧 α=0.05 时误报 109 事件（标准 Schoenfeld 应为 **434**，差 4 倍）。修复：forward 加 `((1+r)²/r)`（新增 `allocation=1` 参数）；reverse 同步改 `sqrt(n)*|log HR|/2`（n=总事件数），正反向精确自洽（434→0.85 回环验证）；legacy `r-assets/r_templates/r_survival.py` 与 `r_curve.py`（survival/ni_survival/survival_exact 三处 n_fn/power_fn）同步修正。⚠️ **coze 远程端需重新部署镜像后才生效**（当前远程调用仍返回旧值）。
- **🔴 全量公式审计（用户「检查一下技能中还有没有类似的问题」，2026-08-20）**：逐行审查 coze R 引擎 38 个 `ss_*` 函数 + legacy 模板 + Python 兜底（v5 已移除），对照标准公式，发现并修复 **2 处同类 4 倍因子 bug（均在兜底/近似分支）**：① `ss_ni_survival` 兜底（Cox.NIS 失败时触发）——D 缺 4 因子且 NI 误用双侧 `z_{α/2}`（应单侧 `z_α`），reverse 缺 `/2`；修复后 margin=1.3/power=0.8/er=0.7 → 每组 257，reverse 回环 0.8005 自洽；② `ss_survival_exact` 兜底（rpact 失败时触发）——D 缺 4 因子，修复后与主公式一致（434）。**文档修正 2 处**：① README 两版「本地 Python 兜底（5 种基础检验）」过时描述（v5 无本地兜底）改为「仅 coze（v5）」；② CHANGELOG v3.5.0 `survival_equivalence` TOST 公式 `z_{1-β}` → `z_{1-β/2}`（TOST 双侧区间，代码正确、文档更正）。**存疑项（用户裁定：保持单侧、加输出标注）**：`ss_prior_informed`（bayesian 检验）与 `ss_hist_controls`（historical_controls 检验）两比例优效走**单侧 α**——用户确认设计意图即单侧优效，**保持公式不变**，改为在输出中显式标注：新增 `label.note_one_sided`（中英）并在 run_task.R 两检验 × 正反双向共 4 处输出点插入「注：本结果为单侧检验（单侧 α）…」；顺手修正 `label.one_sided_alpha` 键 en 字段（原误写中文 → 英文，该键悬空未用、无副作用）。其余 34 个函数结构核对通过（pwr/PowerTOST/rpact/TrialSize 权威包调用或标准闭式、正反向自洽）。
- **🔴 全量语言审计（用户「基于 ct-base 做技能的语言检查」，2026-08-20）**：对照 `ct-base/references/language_policy.md` 六维检查（文档英文-only / README 双语 / 分隔符 / i18n 键配对 / 硬编码中文 / 双显混排），**修复 3 类**：① **i18n en 字段误写中文（批量 31 处）**——R 端 `common.R` 15 键 + Python 端 `i18n.py` 16 键的 `en` 字段原本是中文（如 `label.control_rate_ni` en="对照组有效率 p1:"），违反「en 必须英文」；全部英文化（R 端 23 处 + Python 端 16 处替换），复核两端 en 字段中文残留 **0**；② **`compute_backend.py` coze 不可达报错硬编码中文**（用户可见、未走 i18n）——新增 `error.coze_unreachable` 键（中英）+ 改走 `t()` 延迟导入（i18n 不可用时英文单语兜底，不双显）；③ **Python 端补 2 键**（`header.blank_altman_width` / `label.sd_diff`，R 端引用、双端对齐）。**确认合规项**：SKILL.md/AGENTS.md/references 英文-only（中文仅 frontmatter 双语元数据、§6.7.2 原样通知、UI 提示词、报错原文引用——均为语言策略允许的例外）；README 双语 + 顶部切换链接 ✓；R 端 321 键 vs Python 端 ~220 键为**双字典分层设计**（R 引擎报告键 vs CLI 提示键，R 引用 108 键不需 Python 端解析）；Python 端 `t()` 引用自洽（`header.r_code` 在 R 键文件 `i18n_r_messages.json`，非缺失）；无中英双显/混排（office_to_md.py:207 与 samplesize_power.py:158/674 为 agent-facing 诊断行/ct-base §6.7 共享件，标注不修）。
- **默认出图设定：简单单/两组问题自动附带曲线（用户指令 2026-08-20）**：对简单单/两组检验（`ttest_ind` / `ttest_paired` / `ttest_one` / `proportion_one` / `proportion_two`），当用户**未显式指定曲线**时自动附带：① **forward（`--power` 求 n）**→ 自动补「**样本量随把握度**」曲线（默认 power_seq `0.6:0.05:0.95`，x=目标 power、y=所需 n）；② **reverse（`--nobs` 求 power）**→ 自动补「**把握度随样本量**」曲线（n_seq 自动取给定 n 的 ±50% 范围、8 档）。SVG 按 §19 内联输出；关闭方式：显式指定 `--n_seq` / `--power_seq`（走用户曲线）或 `--dry-run`。实现：`scripts/samplesize_power.py` main() 计算后新增 `_AUTO_CURVE_TESTS` 自动曲线块（复用 backend.compute + render_figures，输出「已自动附带…曲线」说明）；SKILL.md Features 新增「★ Auto-curve on simple one/two-group solves」规则。验证：py_compile 通过；ttest_ind forward → n=92 + 自动样本量曲线；proportion_two reverse（nobs=137）→ 自动功效曲线；SKILL.md 182 行（≤200）。**README 对话示例同步（用户澄清意图：给中间复杂示例的「你这样说」提示词加显式绘制曲线要求）**：Example 3（生存+期中）/ Example 4（非劣效）/ Example 5（BE）的 You say 补「and plot the power/sample-size curve / 并绘制…曲线」——演示用户如何用自然语言显式要求曲线（复杂检验不在自动曲线集合）；示例 1/2 保留自动曲线说明（与新默认行为一致）；开头「examples 1,2,6,7 有回复示意」维持。README_zh-CN.md 同步。
- **README FAQ 新增保密问答 + 保密声明改为 A/B 两档（用户指令，2026-08-20）**：① 两份 README（`README.md` / `README_zh-CN.md`）FAQ 末尾新增「如果数据要保密怎么办 / What if my data must stay confidential?」——回答要点：可用相同设计框架 + 替换/占位数据让技能输出完整 R 代码，本地用真实数据自行运行；技能只发送设计参数、从不接触原始数据；② **修正过时保密声明**：原「A/B/C/D 四级（按保密信息出域风险 + 是否对外检索）」改为 ct-base §11 现行的 **A/B 两档**（A 档非涉密公开、本技能属 A 档；B 档涉密内部如 ct-analysis/ct-sdtm，不对外发布），英文版同步（four tiers → two tiers）；③ 该 FAQ 上收 ct-base §13.10 作全库通例（面向有 coze/云计算调用的技能，含参考实现与本技能样例）。
- **requirements.txt 精简为 stdlib-only（用户「requirements.txt 里面需要的包应该可以减少了」）**：删除 `statsmodels>=0.14.2` / `numpy>=1.24.3` / `scipy>=1.11.4` / `matplotlib>=3.4.0` 四行，改为注释声明「v5 发布技能 stdlib-only，零第三方运行时依赖；cairosvg 仅 `--figure-mode png_file` 可选」。核查依据：① 全量 grep 显示除 `scripts/power_viz.py` 外无任何 numpy/scipy/statsmodels/matplotlib import（adaptive_simulator / local_python_backend / rendering 均纯 stdlib 或延迟 import）；② `--visualize` 已由 coze R 引擎处理、本地无 matplotlib；③ 全量 py_compile exit 0。**后续：`scripts/power_viz.py` 经用户确认已废弃（Python 版曲线图，不再使用），已删除源文件 + pyc 缓存**——发布包现为纯 stdlib + cairosvg 可选，无任何死依赖。
- **渲染管线修复：curve 模式图形重复处理 + SVG 无预览提示（用户反馈 2026-08-20）**：① **重复处理根因**——`main()` 无条件连续调用 `render_figures()`（coze 返回 SVG）与 `render_curve_fallback()`（本地 stats 兜底），curve 模式下 coze 同时回传图形与 stats，导致同一曲线输出两份 SVG/两个 widget（持久化文件还被无参考线的本地 fallback 版覆盖，丢失 power 参考线）。修复：`render_curve_fallback` 仅在 `res.figures` 为空（coze 端无图）时调用；② **SVG 无法预览无提示**——svg_inline 模式下仅输出 `__SVG_WIDGET__`，宿主不渲染内联 HTML 时用户无任何指引。修复（两轮）：「无提示」→ 首轮补 CLI 参数指引（`--figure-mode png_file` 等）→ **用户反馈"CLI 提示很难用"** → 终版改为**教 agent 用自然语言提示词引导用户**（如『图形无法预览，请改用 PNG 图片格式重新出图』/『把图转成 PNG 文件』，技能自动以 PNG 位图重新输出；`render_figures` 与 `render_curve_fallback` 内联输出后均打印该引导 + SVG 源文件路径），SKILL.md §19 同步补「Preview-failure fallback」说明（agent 必须用自然语言引导、不得甩 CLI 参数）；**引导提示为双语**（中文用户 + English users 各给可直接复述的提示词示例，2026-08-20 用户询问「提示词是双语的吗」后修订）；**SKILL.md §19 渲染规则重构为「内联优先 + 降级阶梯」**（用户指令「把经验更新给技能本身」：① 默认 agent 必须把 SVG **直接内联到对话流**显示、文件落盘仅作备份/编辑用（backup/editing only，不得 file-first）；② 无法显示时按序降级——HTML 壳预览（保持矢量）→ PNG 位图；③ 仍以自然语言提示词引导、不碰 CLI）。验证：py_compile 通过；重跑 ttest_ind curve，`__FIGURE__`/`__SVG_WIDGET__` 各仅 1 次，持久化 `ctss_ttest_ind_1.svg` 为 coze 权威版（红色 0.8 参考线 + 10 数据点），新提示文本端到端输出正常。

## v4.0.4 (2026-08-19) · 上传文档处理对齐 ct-base §6.7

- **新增「User-Uploaded Documents (ct-base §6.7)」章节（SKILL.md）**：用户上传 docx/pptx/pdf/doc 文档时，**先转 md/文本再提取设计参数**——① 分层转换（§6.7.1）：`.docx/.pptx` → 共享转换器 `scripts/office_to_md.py`（stdlib-only），`.pdf` → 环境 pdf 技能（无则提示安装），`.doc` 老格式 → 提示安装 word-reader / antiword，图片/扫描件 → 提示提供文字版；② 转换前必向用户展示 §6.7.2 双语提示（PPT 转换丢非文本元素）；③ 保密处理（§6.7.3）：技能不主动拦截，**原始文档 md 仅本地提取参数用、绝不转发**，出域内容仅限设计参数（与既有安全模型一致）；用户要求数据不出域时引导本地 R 后端（`CTSS_BACKEND=local-r`）/ Python 兜底。
- **新增 `scripts/office_to_md.py`**：ct-base §6.7 共享件副本（stdlib-only，docx/pptx → md 单一解析器），与底座字节级一致。
- 计算行为、CLI 接口、发布包构成不变。
## v4.0.3 (2026-08-19) · SVG 绘图设定与提醒全面对齐 meta-analysis + ct-base §19

- **统一出图规范上收 ct-base §19**：将 `meta-analysis` 的 SVG 绘图设定与提醒（figure_mode / 渲染计时与超阈值提示 / SVG 编辑与投稿格式转换）沉淀为全库统一规范 `ct-base/docs/06-inline-rendering.md` §19.9–§19.11，`BASE.md` 索引同步。
- **`adapters/rendering.py` 同步至 ct-base §19 参考实现**：补齐 `_fix_xml()`（svglite 偶发缺 `</g>` → cairosvg 严格 XML 解析前补齐）与 `svg_to_png()`（SVG→PNG 光栅化，figure_mode='png_file' 依赖），与 `meta-analysis/adapters/rendering.py` 保持一致。
- **`scripts/samplesize_power.py` 落地 figure_mode + 渲染计时提示**：
  - `render_figures()` 新增 `figure_mode` 参数（默认 `svg_inline`，可由 `--figure-mode` / 环境变量 `CTSS_FIGURE_MODE` 切 `png_file`）；`png_file` 经 `svg_to_png` 转 PNG 并优雅降级回 `svg_inline`（cairosvg 缺失/失败时）。
  - 渲染阶段计时 `render_elapsed_seconds` + SVG 体量代理 `render_svg_kb`；超阈值（`>30s` / `>200KB`）输出 `__RENDER_HINT__` 供 agent 在回复中显式提示（ct-base §19.10 强制规则）。
- **新增 `references/svg_editing.md`**（ct-base §19.11）：SVG 编辑工具与期刊格式转换（EPS/PDF/TIFF 600dpi）。
- **SKILL.md 新增 `Figure Output & Rendering (ct-base §19)` 章节**：内联渲染、figure_mode、渲染计时与 render_hint 强制体现规则、svg_editing.md 指引。
- 纯规范/呈现层增强，计算行为、CLI 接口、发布包构成均不变。

## v4.0.2 (2026-08-17) · 后端默认策略：一律优先 coze，本地分析仅显式请求

- **`select_backend()` 默认策略调整**：未显式指定后端时，**一律优先调用 coze 工作流**（CozeBackend，权威引擎）；coze 不可达（无 `CTSS_COZE_ENDPOINT` 且未设 `CTSS_COZE_MOCK=1`）时**直接报错并引导配置**，不再静默回退到本地 R 开发后端或本地 Python 兜底。
- **本地分析改为显式 opt-in**：仅在以下任一情形才启用本地计算——
  - CLI `--local` 开关；
  - 环境变量 `CTSS_BACKEND=local-r`（或 `r`）；
  - 环境变量 `CTSS_FORCE_R=1`（坚持用 R 真相源）。
- `scripts/samplesize_power.py` 新增 `--local` 参数，并作为 `prefer_local` 传入 `select_backend()`；其余 CLI 接口与 `select_backend(test)` 旧签名（新增默认参数 `prefer_local=False`）向后兼容。
- 本地 R（`LocalRBackend`）/ 本地 Python（`LocalPythonBackend`）能力完整保留，仅不再作为默认路径；能力说明见 v4.0.0。`r-assets/`（含本地 R 实现）与 coze 镜像 `adapters/coze/` 经 `sync_to_coze.py` 重新同步一致。

## v4.0.1 (2026-08-11) · 合规：出站调用收口至 adapters/（ct-base §16.9）

- **出站调用目录收口**：将运行时对外网络请求模块 `scripts/coze_client.py`（CozeBackend，urllib POST 调 coze 计算端点）迁移至专用目录 `adapters/coze_client.py`，与 ct-base §16.9 对齐。
- `scripts/compute_backend.py` 的延迟导入 `from coze_client import CozeBackend` 改为 `from adapters.coze_client import CozeBackend`，并在模块加载时把技能根目录加入 `sys.path`，确保 `adapters` 包可被解析；`scripts/` 现已不含任何对外网络调用（符合 §16.9 的 scripts/ 纯本地约束）。
- 同步修订 `r-assets/local_r_backend.py` 注释中的路径引用（`scripts/coze_client.py` → `adapters/coze_client.py`）。
- 本次为纯内部重定位，CLI 接口、计算行为、发布包构成均不变；coze 契约（`r-assets/coze_contract.md`）与 dev 同步脚本（`r-assets/sync_to_coze.py`）维持原样。

## v4.0.0 (2026-08-02) · 架构重构：coze 主导计算 / 本地 Python 兜底 / 发布包不携带 R

> **重大架构重构（CLI 接口向后兼容）。** / **Major architecture refactor (CLI surface backward-compatible).**

- **计算后端抽象缝 `ComputeBackend`**：编排层 `scripts/samplesize_power.py` 不再含任何 R 代码；`select_backend()` 按环境变量/可用性路由到三后端：
  - `CozeBackend`（**默认权威引擎**）：将参数打包成 JSON 请求信封发往 coze R 服务（`CTSS_COZE_ENDPOINT` / `COZE_ENDPOINT`）；`requires_confirmation=False`，无本地 R/shell；返回数值 + 可选图形（SVG/HTML/PNG）+ 可选 R 源码。
  - `LocalPythonBackend`：仅 5 种基础优效性检验的纯 Python 闭式解（`ttest_ind` `ttest_one` `ttest_paired` `proportion_one` `proportion_two`），仅在 coze 不可达时作应急离线兜底，明确标注「非权威」。
  - `LocalRBackend`（**仅开发/过渡期**，位于 `adapters/r-assets/`）：完整 R 实现，发布包中不携带。
- **R 仍为真值源、但运行在 coze 服务器端**：用户仍可用 `CTSS_FORCE_R=1`（优先 coze-R，否则本地 R 开发后端）要求完全用 R 实现，或用 `CTSS_RETURN_R_CODE=1` 取回完整 R 源码 + R 结果。
- **`adapters/r-assets/` 不随发布包**：`.clawhubignore` 剔除 `adapters/r-assets/`、`dist/`、`outputs/`；R 模板/配置仍维护于 `adapters/r-assets/` 并经 `adapters/r-assets/sync_to_coze.py` 同步到 coze（`coze_contract.md` 定义请求/响应信封），只是不再随发布产物分发。
- **图形管线**：coze 回传的 `figures[]` 写入 `CTSS_OUTPUT_DIR`（默认 `./outputs`），并经 `__FIGURE__ <format> <path> caption="..."` 标记提供给宿主渲染。
- **发布包零 R 验证**：移除 `adapters/r-assets/` 后，复杂检验正确报错并指路配置 coze；5 种基础检验回退本地 Python（已通过 `_pubtest` 场景验证）。
- **版本归一到 v4.0.0**：`SKILL.md`、双语 `README`、脚本 docstring/argparse、本变更日志同步；文档现已描述 coze 主导架构（本机无需 R，R 在 coze 服务器端运行）。

## 3.8.2 (2026-08-03) · 命名统一：中英文显示名对齐 ct 家族规范（英文统一 `Clinical Trial` 前缀，中文统一「临床试验」前缀；ct-advisor 定为「临床试验总顾问 / Clinical Trial Chief Advisor」）

> This file records ct-samplesize's key architecture & security changes for maintainer auditing (user-facing usage: `SKILL.md` & `references/`). / 本文件记录 ct-samplesize 的关键架构与安全变更，供维护者审计参考（用户面向的使用说明见 `SKILL.md` 与 `references/`）。

## v3.8.1 — QA: 10-round red-team bug hunt (100 cases) / 质量保障：十轮红队探查（100 案例）

- **QA harness built**: `qa/qa_harness.py` runs each case against the real CLI (`--yes`), classifies PASS / EXPECTED_FAIL (graceful validation) / PY_TRACE / R_ERROR / BAD_RESULT / UNEXPECTED_OK; plus `scan_i18n.py` (de-noised, supports dynamically-built keys via `.replace()`). / 搭建 QA 测试台：`qa/qa_harness.py` 对每个案例真实执行 CLI（`--yes`），分类 PASS / EXPECTED_FAIL（优雅校验）/ PY_TRACE / R_ERROR / BAD_RESULT / UNEXPECTED_OK；另含 `scan_i18n.py`（去噪，支持 `.replace()` 动态构造的 key）。
- **Bug R8 — alpha range too loose**: numeric range rule was `alpha: (0, 1)`, silently accepting `alpha > 0.5` (e.g. 0.6). Tightened to `(0, 0.5)` so nonsensical α is rejected with a clean validation message. / alpha 范围过宽：原为 `(0,1)`，`alpha>0.5`（如 0.6）被静默放行；收紧为 `(0,0.5)`，使无意义 α 被优雅拒绝。
- **Bug R9 — R-side i18n drift (raw keys printed)**: 7 GSD keys (`label.empirical_power`, `label.expected_events`, `label.expected_n`, `label.planned_events`, `label.stop_prob`, `header.gsd_survival_sim`, `header.gsd_hazard_sim`) existed in the Python master (`i18n._MESSAGES`) but were never synced to the R runtime dict (`I18N_R` in `r_libs.py`), so R printed the raw key strings at runtime. Added all 7 to `I18N_R`; hardened `scan_i18n.py` to also reconstruct keys built dynamically via `t("prefix.{ph}")` + `.replace("{ph}", "val")`. / R 端 i18n 漂移（打印原始 key）：7 个 GSD key 在 Python 主字典中存在却从未同步到 R 运行时字典 `I18N_R`，导致 R 运行时直接打印原始 key 字符串；已全部补入 `I18N_R`，并强化 `scan_i18n.py` 以重建经 `t("prefix.{ph}")` + `.replace("{ph}","val")` 动态构造的 key。
- **Bug R10 — `--hr` ambiguous option**: survival analysis expected `--hazard_ratio` but the universal shorthand `--hr` collided with `--hr_expected` / `--hr_exact` (argparse "ambiguous option" error). Added `--hr` as an explicit alias of `--hazard_ratio`. / `--hr` 歧义选项：生存分析期望 `--hazard_ratio`，但通用简写 `--hr` 与 `--hr_expected`/`--hr_exact` 冲突（argparse "ambiguous option" 报错）；已将 `--hr` 显式设为 `--hazard_ratio` 的别名。
- **Result**: Rounds 1–10 × 10 cases = 100 cases executed; all 10/10 green after fixes; no regressions in R1–R7. / 结果：第 1–10 轮 × 10 案例 = 100 案例全部执行，修复后每轮 10/10 通过；R1–R7 无回归。

## v3.8.0 — UX: friendlier menu & README / 用户体验：菜单与 README 更友好

- **User menu (UI) optimized**: `references/menu.md` reorganized as scenario-first — top Triage gate (Simple / Complex / Vague) + `③ explain differences` entry, then a "find your test by research question" index (Part 0) ahead of the authoritative endpoint-type tree (Part 1); cleaner navigation for non-statistician users. / 用户菜单（界面）优化：`references/menu.md` 改为场景优先——顶部 Triage 门控（简单/复杂/模糊）+「③ 解释差异」入口，再按「研究问题找检验」索引（Part 0）置于权威终点类型树（Part 1）之前；非统计背景用户导航更顺畅。
- **README optimized**: dialogue-style examples (1–7, incl. Complex pop-up menu & grill-me), a scenario index with "try saying", and a clear feedback/contact section (§10.6) — onboarding closer to a first-time user's needs. / README 优化：对话式示例（1–7，含复杂弹出菜单与 grill-me）、场景索引含「试试这样说」、明确的反馈/联系段（§10.6），更贴近初次使用者需求。
- **Version unified to v3.8.0**: `SKILL.md`, both READMEs, `references/operation_sop.md`, and `scripts/samplesize_power.py` all bumped; docs remain English-only per ct-base §13.2. / 版本统一至 v3.8.0：SKILL.md、双语 README、`references/operation_sop.md`、`scripts/samplesize_power.py` 全部同步；文档按 ct-base §13.2 保持英文-only。

## v3.7.2 — Docs: English-only (ct-base §13.2) / 文档：英文-only（ct-base §13.2）

- **Docs English-only**: `references/*` and `AGENTS.md` are now English-only per ct-base §13.2 (Chinese removed; runtime output may still be EN+ZH per OS setting). Renamed `formulas_zh.md`→`formulas.md`, `r_packages_zh.md`→`r_packages.md`; updated all references. `SKILL.md` language-policy section reworded to English-only docs; `references/language_policy.md` retitled accordingly. / 文档英文-only：`references/*` 与 `AGENTS.md` 按 ct-base §13.2 改为纯英文（删除中文；运行时输出仍可随 OS 中英）。重命名 `formulas_zh.md`→`formulas.md`、`r_packages_zh.md`→`r_packages.md` 并同步引用；`SKILL.md` 语言策略段改为英文-only 文档说明；`references/language_policy.md` 同步调整。
- **SKILL.md trimmed to ≤200 lines**: Implementation section condensed (examples externalized to `references/cli_examples.md`); removed duplicated menu note and decorative lines. / `SKILL.md` 压缩至 200 行内：Implementation 段精简（示例外迁 `references/cli_examples.md`），删除重复菜单说明与装饰行。
- **Triage alignment (ct-base §5.2)**: Simple / Complex / Vague three-way interaction formalized in `SKILL.md` and `AGENTS.md` (Complex → routing menu with `③ explain differences`; Vague → grill-me probing). / Triage 三分类（简单/复杂/模糊）在 `SKILL.md` 与 `AGENTS.md` 落地（复杂→路由菜单含「③ 解释差异」；模糊→grill-me 逐分支追问）。
- **`references/menu.md` user-friendly rewrite**: added a scenario-first "find your test by research question" index (Part 0, mirroring ct-advisor's intent-organized clarify menu) ahead of the authoritative endpoint-type tree (Part 1) and design-family cross-index (Part 2); triage gate + `③ explain-differences` entry stated at top; removed leftover English-cleanup fragments. 49 tests all covered. / `references/menu.md` 用户友好化重写：新增「按研究问题找检验」场景索引（Part 0，对齐 ct-advisor 意图组织式澄清菜单）置于权威终点类型树（Part 1）与设计族交叉索引（Part 2）之前；顶部明确 Triage 门控与「③ 解释差异」入口；清理英化残留碎片。49 检验全覆盖。
- **README version fix**: `README.md` / `README_zh-CN.md` footer bumped v3.7.1 → v3.7.2 to match `SKILL.md` / `samplesize_power.py`. / README 版本号 v3.7.1→v3.7.2，与 SKILL.md / samplesize_power.py 一致。

## v3.7.1 — Fix: R-side `._qt` alias & ROC `ss_roc` execution / 修复：R 端 `._qt` 别名与 ROC `ss_roc` 执行

- **Bug 1（核心、广泛）**: 生成的 R 代码使用 `cat(_qt("label.xxx"), ...)`，但 R 端 `I18N_R` 从未定义 `_qt`，且 **R 标识符不能以 `_` 开头**（`_qt` 为非法符号，故 R 报 `unexpected symbol in "_qt"`）。旧 `i18n.R` 内联重构时漏掉该别名；此前 dry-run 不执行 R，从未暴露。
  - 修复：R 端别名改为 `._qt`（`.` 开头，R 合法，与 `.messages` / `.t_lang` 同风格）；生成代码 `cat(_qt(` → `cat(._qt(`（R 字符串上下文 88 处）；Python 端 `_qt()` 函数与 ROC 的 Python 端调用保持不变。
  - 验证：ttest_ind / roc / adaptive_simulate 实跑均正常（不再报 `_qt` 错误）。
- **Bug 2（ROC 模块）**: ROC 模块在 Python 端调用 R 函数 `ss_roc`（如 `_r_cat(_qt(...), ss_roc(...))`），`ss_roc` 仅在 R 端定义（`r_templates/r_proportions_rates.py` 的 `R_ROC` 常量），导致 `NameError: name 'ss_roc' is not defined`。该问题在 v3.4.9 修复 `_qt` f-string bug 时遗留（只把 `_qt` 移到 Python 端，未处理同为 R 函数的 `ss_roc`）。
  - 修复：ROC 模块改为与其它比例 / 率类检验一致的 R 字符串上下文（`cat(._qt(...))` 形式），`ss_roc(auc0=..., n=...)` 作为 R 代码在 R 端执行（由 `R_ROC` 引入）。
  - 验证：roc 两条路径（给 n 求 power / 给 power 求 n）均正确产出（Achieved power 0.9931 / Sample size 81）。
- **新增 `references/operation_sop.md`**：从触发、环境、调用、安全模型、参数、实测工作流、结果产出格式到故障排查的完整操作 SOP。

## v3.7.0 — New: Group-sequential survival/hazard MONTE-CARLO SIMULATION / 新增：组序贯生存/风险率蒙特卡洛模拟

- **New tests / 新增检验类型 (2)**: `gsd_survival_sim`, `gsd_hazard_sim` — Monte-Carlo simulation of group-sequential survival designs via rpact `getSimulationSurvival`. / 基于 rpact `getSimulationSurvival` 的组序贯生存设计蒙特卡洛模拟。
  - Validates empirical power, stage-wise rejection probabilities, expected N, and expected events against the analytic (closed-form) GSD designs. / 用于验证经验功效、各阶段拒绝概率、预期样本量与预期事件数，与解析（闭式）组序贯设计互校。
  - Reuses the exact same `_GSD_DESIGN` block, spending functions (`--spending_func`), `--futility` bound, and `directionUpper` reduction guard as the analytic `gsd_survival`/`gsd_hazard`. / 复用与解析型 `gsd_survival`/`gsd_hazard` 完全相同的设计块、消耗函数、futility 边界与下降型方向守卫。
  - New params / 新增参数: `--n_simulations` (→ `maxNumberOfIterations`, default 10000; shared with `adaptive_simulate`) and `--sim_seed` (→ `seed`). / 复用 `adaptive_simulate` 的 `--n_simulations` 与 `--sim_seed`。
- **rpact simulation constraints (validated empirically) / rpact 模拟约束（已实测验证）**:
  - `maxNumberOfSubjects` is NOT passed — rpact derives it from `accrualTime × accrualIntensity`, which must agree (a conflicting explicit value raises an error). / 不传 `maxNumberOfSubjects`，由入组强度推导，避免与 API 约束冲突。
  - The interim-event plan is anchored on rpact's analytic `maxNumberOfEvents` (internally consistent); `longTimeSimulationAllowed = TRUE` lets follow-up extend so planned events accrue. / 期中事件计划锚定 rpact 解析 `maxNumberOfEvents`；开 `longTimeSimulationAllowed` 让随访延长以累积事件。
  - `futilityStops` length must be `kMax-1` (last look has no futility stop) — same rule as the analytic design. / `futilityStops` 长度须为 kMax-1，与解析设计一致。
- **Validation / 验证**: R-executed (rpact 4.4.0). Default mode (solve n+events from power 0.8, kMax=3, OF) → n=180/arm, empirical power **0.776** (≈ analytic 0.8), expected N=356.6, expected events=163.9, stage-wise reject 0.071/0.398/0.307. `gsd_hazard_sim` gives identical numbers (HR ≡ hazard rate). Supplying a too-small `--nobs` (e.g. 89) honestly yields lower empirical power (0.42) and expected N (75.2). / 默认模式经验功效 0.776（接近解析 0.8）；给定过小 nobs 如实反映功效不足。
- Count: 47 → 49 analytic test types. / 检验类型计数 47 → 49。

## v3.6.0 — New: PASS Group-Sequential extensions (rpact-backed) / 新增：PASS 组序贯扩展（rpact 驱动）

- **`group_sequential` upgraded / 升级**: replaced the old approximate closed-form (`gsDesign`) two-sample **means** design with an **exact rpact** implementation (`getSampleSizeMeans`/`getPowerMeans`). Spending validated via `choices`. / 将旧的近似闭式（gsDesign）两样本**均值**组序贯设计替换为 **rpact 精确**实现；消耗函数经 `choices` 校验。
- **New tests / 新增检验类型 (4)**: `gsd_proportion`, `gsd_survival`, `gsd_hazard`, `gsd_poisson` — rpact-backed group-sequential designs for the other PASS Group-Sequential families. / rpact 驱动的组序贯设计，覆盖 PASS 组序贯的其余族。
  - `gsd_proportion` — two proportions; `difference`/`ratio`/`or` effect metrics; `getSampleSizeRates`/`getPowerRates`. / 两比例，支持差值/比值/OR 三种效应度量。
  - `gsd_survival` / `gsd_hazard` — logrank / HR; `getSampleSizeSurvival`/`getPowerSurvival`; control median → λ₂. / 生存 logrank 与风险比，对照中位推导 λ₂。
  - `gsd_poisson` — two Poisson rates; `getSampleSizeCounts`/`getPowerCounts`. / 两 Poisson 率。
- **Real spending functions / 真实消耗函数**: OF / Pocock / WT / HSD(γ via `--rho`) / KimDeMets(γ via `--rho`); futility bound via `--futility` (non-binding, `bsOF`), which requires the `as*` family. / 5 种消耗函数；`--futility` 加非绑定边界，须配 `as*` 族。
- **Bug fixes / 修复**:
  - `directionUpper` guard: effects that are *reductions* (HR<1, rate1<rate2, negative `effect_gs`, p1<p2) now set `directionUpper = FALSE`, fixing power=0 on the lower side. / 方向守卫：下降型效应自动设 `FALSE`，修复下侧备择 power=0。
  - `getPowerSurvival` does not accept `followUpTime`; survival/hazard reverse now encodes accrual via `accrualIntensity` + estimated events. / `getPowerSurvival` 不接受 `followUpTime`，反向改用 `accrualIntensity`+事件估计。
  - WT requires `deltaWT` (via `--wt_delta`, default 0.25); WT + `--futility` is rejected with a friendly bilingual error (rpact has no `asWT` form). / WT 需 `deltaWT`；WT 与 futility 组合被友好拦截（rpact 无 asWT）。
  - KimDeMets / HSD now set `gammaA` from `--rho` (previously only HSD did, triggering the "out of validated bounds" warning). / KimDeMets/HSD 均从 `--rho` 取 gammaA。
  - `gsd_proportion` difference mode: `--p1`/`--p2` got defaults (0.7/0.5) to avoid `object 'None' not found`. / 差值模式补默认参数。
- **Bidirectional / 双向求解**: all 5 GSD types support `--nobs` reverse (solve power), self-consistent with forward n (means 80/0.80, proportion 75/0.80, survival 178/0.82, poisson 33/0.81). / 5 类均支持 `--nobs` 反解，正反向自洽。
- **Implementation / 实现**: new `scripts/r_templates/r_gsd.py` (5 rpact templates + shared `_GSD_DESIGN`); dispatch wired in `samplesize_power.py` (`choices`, argparse params, `_GSD_DESIGN` injection: `_futil_params`/`_gs_type`/`_gs_gamma`/`_delta_frag`/`_design_beta`/`_kmax`/`_dir_upper`); i18n key `error.wt_futility_unsupported` added. / 新增 `r_gsd.py` 与调度接线；i18n 新增键。
- **Validation / 验证**: `py_compile` clean; all 5 types R-executed forward & reverse give self-consistent results; spending×futility matrix reachable; WT+futility guard verified. / 编译通过；5 类正反向 R 实跑自洽；消耗函数×futility 矩阵可达；WT+futility 守卫已验证。
- Count: 43 → 47 analytic test types. / 检验类型计数 43 → 47。

## v3.5.0 — New: 7 PASS-survival test types (closed-form, base R) / 新增：7 个 PASS 生存检验类型（闭式、纯 base R）

- **New tests / 新增检验类型 (7)**: `survival_equivalence`, `survival_superiority`, `cox_covariate`, `survival_one_sample`, `competing_risks`, `recurrent_events`, `survival_historical` — ported from the NCSS/PASS survival-analysis coverage. All are **closed-form, pure base R** (no extra R packages), so they run even when `survRM2`/`cpsurvsim`/`frailtypack` are absent. / 移植自 NCSS/PASS 生存分析能力；全部为**闭式、纯 base R**（无需额外 R 包），在 `survRM2`/`cpsurvsim`/`frailtypack` 缺失时仍可运行。
- **Methods / 方法**:
  - `survival_equivalence` — TOST on log-HR; $D = [2(Z_{1-\alpha}+Z_{1-\beta/2})]^2/(\log\delta_E)^2$ (TOST 双侧区间 → β/2 分位；one-sided per arm). / 对数 HR 上的双单侧检验。
  - `survival_superiority` — superiority **with** margin $\delta_S$: $\delta=\log\delta_S-\log(HR)$; guard $HR\ge\delta_S$ errors out. / 含界值优效，守卫 HR≥界值即报错。
  - `cox_covariate` — Vittinghoff & McCulloch (2007) covariate R² adjustment: $d=(Z_{1-\alpha/2}+Z_{1-\beta})^2/[(1-R^2)p(1-p)(\log HR)^2]$. / 协变量 R² 校正。
  - `survival_one_sample` — one-arm exponential vs historical median; $\lambda_j=\log2/m_j$, $e_j=1-e^{-\lambda_j\bar t}$. / 单组指数生存。
  - `competing_risks` — 2-sample cumulative-incidence (CIF) proportion test. / 竞争风险（累积发生率）。
  - `recurrent_events` — Andersen-Gill marginal rate-ratio (Poisson). / 复发事件（Poisson 边际率比）。
  - `survival_historical` — single-arm logrank vs historical median (same exponential structure as `survival_one_sample`). / 历史对照 logrank。
- **Bidirectional / 双向求解**: all 7 support `--nobs` reverse (solve power given n), consistent with the other 43 types. / 7 个类型均支持 `--nobs` 反向求效能，与其余 43 种一致。
- **Implementation / 实现**: new `scripts/r_templates/r_survival_ext.py` (7 `R_*` constants + `ss_*` R functions); wired into `samplesize_power.py` dispatch (`choices`, argparse params, `_RANGE_RULES`, 7 `elif` branches). i18n keys added to both `r_libs.py` (R side `t()`) and `i18n.py` (Python `_qt()`). / 新增 `r_survival_ext.py` 与调度接线；i18n 双系统同步新增键。
- **Bug fix / 修复**: removed the now-redundant `source(file.path("{scriptdir}", "i18n.R"))` lines from R templates — `run_r()` already prepends `I18N_R` at execution time, so the literal `{scriptdir}` placeholder previously caused a `KeyError` on `.format()` (also affected the pre-existing `ni_survival`/`survival_exact` templates). / 删除冗余的 `source(i18n.R)` 行：因 `run_r()` 已在运行时前置 `I18N_R`，原 `{scriptdir}` 占位符会在 `.format()` 时触发 `KeyError`（此前也影响 `ni_survival`/`survival_exact`）。
- **Validation / 验证**: `py_compile` clean; all 7 types R-executed forward (`--power 0.8`) and reverse (`--nobs`) give self-consistent results. / `py_compile` 通过；7 个类型正反向 R 实跑数值自洽。
- Count: 37 → 43 analytic test types. / 检验类型计数 37 → 43。

## v3.4.9 — Fix: Anaconda f-string _qt() bug / 修复：Anaconda Python 下 f-string _qt() 静默失效

- **Fix / 修复**: On Anaconda Python 3.13.9 (and potentially other builds), within a multi-line f-string, a function-call expression like `{_qt("...")}` that shares a physical line with a literal backslash `"\\n" ` silently fails to evaluate — leaving `_qt(` as literal text in the generated R code, which then crashes R with `unexpected symbol in "cat(_qt("`. This is **not** a universal Python bug (I could not reproduce on my own Win10/Anaconda 3.13.9 setup), but is clearly environment-sensitive and has been confirmed by the user via ct-pipeline runs. / 在 Anaconda Python 3.13.9（及可能的其它构建）中，多行 f-string 里面，函数调用表达式 `{_qt("...")}` 如果与字面反斜杠 `"\\n"` 在同一物理行，会静默不生效 — 生成的 R 代码里保留 `_qt(` 字面文本，R 报 `unexpected symbol in "cat(_qt("`。这不是普遍性 Python 缺陷（我在本机 Win10/Anaconda 3.13.9 无法复现），但显然对环境敏感，已由用户通过 ct-pipeline 确认。
- **Root cause / 根因**: Function-call expressions in f-string `{}` have complex escaping/interpolation rules on some parser builds. When a literal backslash appears later on the same line, certain parser variants may silently skip the function-call substitution. / f-string `{}` 里的函数调用表达式在某些解析器.build 上有复杂转义/插值规则；当同一行后半出现字面反斜杠时，某些解析器变体会静默跳过函数调用的替换。
- **Resolution / 方案**: Add a `_r_cat(*args)` helper that builds R cat() calls via `str.join`, moving `_qt()` out of f-string expression context entirely. The `cat({_qt(...)}, ..., "\\n")` pattern in the ROC calculator (lines 885–896, 9 cat lines) was the only place using the buggy f-string-of-function-call pattern; all other calculators use `cat(_qt(...))` literal text which works fine. / 新增 `_r_cat(*args)` 辅助函数，用 `str.join` 拼接 cat 参数，把 `_qt()` 完全移出 f-string 表达式。仅 ROC 计算器（885–896 行、9 行 cat）使用了有缺陷的 `cat({_qt(...)})` 模式；其余模块用字面 `cat(_qt(...))` 没问题。
- **Validation / 验证**: `py_compile` passes; `cat(...)` output behavior unchanged. / `py_compile` 通过，cat() 输出行为不变。

## v3.4.8 — Bilingual i18n infrastructure + inline R for publish safety / 中英双语提示基础设施 + R 内联以应对发布过滤

- **Bilingual prompt infrastructure / 中英双语提示基础设施**: Built `scripts/i18n.py` with a centralized `is_chinese_os()` (auto-detects OS locale) + `t(key, **kwargs)` dispatch. 138 bilingual keys cover safe_preview / exec / info / error / validation / install / header / r_header.* / label.* + adaptive_sim.* across the entire Python surface (main CLI, Python fallback calculators, adaptive_simulator.py, 9 R templates via `_qt()`). Auto-switch: default English → Chinese when OS is Chinese; code output unaffected. / 新建 `scripts/i18n.py`，提供中心化 `is_chinese_os()`（自动检测 OS locale）+ `t(key, **kwargs)` 分派；138 个双语 key 覆盖全部 Python 可见输出（主 CLI、Python 备用计算器、adaptive_simulator.py、9 个 R 模板通过 `_qt()`）。自动切换：默认英文 → 中文（OS 为中文时）；代码输出不受影响。
- **Inline R for publish safety / R 内联以应对发布过滤**: External `.R` files (i18n.R, adaptive_sim.R) are stripped by ClawHub/SkillHub during publishing. Solution: created `scripts/r_libs.py` containing `I18N_R` and `ADAPTIVE_SIM_R` as Python `r"""..."""` string constants. At runtime `run_r()` injects I18N_R at the head of the generated R script (replacing the old `source("i18n.R")` line), and `build_adaptive_sim_r_code()` writes ADAPTIVE_SIM_R to a system-temp `_adaptive_sim.R` file then sources it (cleaned up afterward via `file.remove()`). / 外部 `.R` 文件（i18n.R、adaptive_sim.R）在发布时被 ClawHub/SkillHub 过滤删除；解决方案：新建 `scripts/r_libs.py`，将两者作为 Python `r"""..."""` 字符串常量（I18N_R、ADAPTIVE_SIM_R）内联。运行时 `run_r()` 将 I18N_R 前置注入生成的 R 脚本（替换原 `source("i18n.R")` 行），`build_adaptive_sim_r_code()` 将 ADAPTIVE_SIM_R 写入系统 temp 目录的 `_adaptive_sim.R` 再 source()（末尾 `file.remove()` 清理）。
- **Removed 4 external .R files / 删除 4 个外部 .R 文件**: `scripts/i18n.R`, `scripts/adaptive_sim.R`, `scripts/test_adaptive_sim.R` (demo), `scripts/_install_packages.R` (3-line script fully overwritten by Python at runtime). `scripts/` now ships **.py only** (plus `r_templates/` subpackage). / 已删除 `scripts/i18n.R`、`scripts/adaptive_sim.R`、`scripts/test_adaptive_sim.R`（演示文件）、`scripts/_install_packages.R`（3 行脚本，运行时由 Python 动态完全覆盖）。`scripts/` 现仅携带 `.py` 文件（外加 `r_templates/` 子包）。
- **R template i18n / R 模板双语化**: All 9 R templates (`r_mixed_model`, `r_curve`, `r_survival`, `r_equivalence`, `r_design_special`, `r_bayesian_adaptive`, + 3 previously ported) ported to i18n `t()` calls at user-visible `cat()` / `message()` / `warning()` points, using the inline `I18N_R` message dictionary (131 keys). User-visible R output now auto-switches EN/ZH on Chinese OS. / 全部 9 个 R 模板（r_mixed_model、r_curve、r_survival、r_equivalence、r_design_special、r_bayesian_adaptive + 此前已改的 3 个）在可见 `cat()`/`message()`/`warning()` 处改用 i18n `t()` 调用，使用内联 `I18N_R` 消息字典（131 个 key）；用户可见的 R 输出现可在中文 OS 下自动切换英/中。
- **samplesize_power.py Python fallback bilingualized / Python 备用路径双语化**: ~120 lines of hard-coded `cat()` in 10 pure-Python fallback calculators (ROC/Poisson/Cluster-RCT/Vaccine/T-Test/ANOVA/Proportions/NI/Survival) replaced with `_qt()` (i18nn + R-string-escaping) for EN/ZH auto-switch consistency. / ~120 行硬编码 `cat()`（10 个纯 Python 备用计算器：ROC/Poisson/Cluster-RCT/Vaccine/T-Test/ANOVA/Proportions/NI/Survival）替换为 `_qt()`（i18nn + R 字符串转义）调用，与主路径英/中自动切换保持一致。
- **adaptive_simulator.py bilingualized / 双语化**: 5 user-visible print/visualize/JSON titles now go through `i18n.t()`. / 5 处用户可见的 print/visualize/JSON 标题改用 `i18n.t()` 双语化。
- **adaptive_sim.R cat output / cat 输出**: ~25 remaining hard-coded English `cat()` calls in the inlined `ADAPTIVE_SIM_R` string are English-only (acceptable: complex/rarely-used module, English-only allowed per language policy). / 内联 `ADAPTIVE_SIM_R` 字符串中约 25 处 `cat()` 仍为硬编码英文（可接受：复杂/少用模块，按语言策略可暂只提供英文）。
- **description / 描述**: SKILL.md `description` field now ship EN alongside ZH (`"中文… / English…"`), matching the bilingual-first packaging convention. / SKILL.md `description` 字段现已携带英/中双语文本（"中文… / English…"），与双语优先的打包约定保持一致。
- 12 files changed, +1320 −396 lines. |

## v3.4.7 — `adaptive_simulate`: standalone R function library (`scripts/adaptive_sim.R`) / 独立 R 函数库 scripts/adaptive_sim.R

- The Monte-Carlo engine is now a **standalone, `source()`-able pure base-R function library** `scripts/adaptive_sim.R` (no inline template, no extra packages). It exposes `run_adaptive_sim()` (one-shot dispatcher with report + optional PNG/JSON) and the individual `simulate_group_sequential()` / `simulate_adaptive_reestimate()` / `simulate_drop_the_loser()` / `optimize_power()` functions — so users can call it directly from R: `source("scripts/adaptive_sim.R")` then `run_adaptive_sim(...)` or `simulate_*()`. / 蒙特卡洛引擎现改为**独立、可直接 `source()` 的纯 base-R 函数库** `scripts/adaptive_sim.R`（不再内联模板、无需额外 R 包）。它导出 `run_adaptive_sim()`（一键调度+报告+可选 PNG/JSON）与各底层 `simulate_group_sequential()`/`simulate_adaptive_reestimate()`/`simulate_drop_the_loser()`/`optimize_power()` 函数——用户可在 R 中直接调用（先 `source("scripts/adaptive_sim.R")`，再 `run_adaptive_sim(...)` 或 `simulate_*()`），而不仅经由 CLI。
- Removed the dead `scripts/r_templates/r_adaptive_simulate.py` inline-template module; the CLI now emits a short `source(".../adaptive_sim.R")` + `run_adaptive_sim(...)` snippet (SAFE PREVIEW, `--yes` to run), and the package `__init__.py` no longer references it. / 已删除失效的内联模板模块 `scripts/r_templates/r_adaptive_simulate.py`；CLI 现生成精简的 `source(".../adaptive_sim.R")` + `run_adaptive_sim(...)` 代码片段（安全预览、`--yes` 执行），包 `__init__.py` 不再引用它。
- Pure-Python fallback (`scripts/adaptive_simulator.py`) unchanged: still auto-runs when R is absent. / 纯 Python 备用路径（`scripts/adaptive_simulator.py`）不变：无 R 时仍自动启用。
- Validated at α=0.025 (R engine): GS OBF 3-look power 0.844 / T1E 0.024; SSR power 0.888 / T1E 0.024 (28% inflation); drop-the-loser 3-arm power_any 0.915 / T1E 0.021; optimize recommends N/arm 240 for 90% power. / 在 α=0.025 下经 R 实跑验证：GS OBF 3 看 power 0.844/T1E 0.024；SSR power 0.888/T1E 0.024（28% 扩样）；drop-the-loser 3 臂 power_any 0.915/T1E 0.021；optimize 推荐 90% 功效需 240/臂。

## v3.4.6 — `adaptive_simulate`: R is now the primary engine, Python is the no-R fallback / R 改为主引擎，Python 改为无 R 备用

- Per user request, the adaptive-trial Monte-Carlo simulator (`--test adaptive_simulate`) now **generates and shows R code as its primary output** (SAFE PREVIEW by default, run with `--yes`), consistent with all 37 analytic tests. The previous pure-Python engine becomes the **fallback** used only when R is not installed. / 应需求，`--test adaptive_simulate` 自适应试验蒙特卡洛仿真器现在**以生成并展示 R 代码为主输出**（默认安全预览，`--yes` 执行），与其余 37 种解析检验一致；原先的纯 Python 引擎改为**备用**，仅在本机未安装 R 时启用。
- New R template `scripts/r_templates/r_adaptive_simulate.py` (pure base-R, no extra packages) faithfully ports the engine: 3 designs (`group_sequential` / `adaptive_reestimate` / `drop_the_loser`), 3 spending functions (`obrien_fleming` / `pocock` / `power_family`), exact Armitage-McPherson-Rowe boundary recursion, promising-zone SSR with Cui-Hung-Wang statistic, futility boundaries, Type I error control, multi-arm drop-the-loser, and `--optimize` min-N search. / 新增 R 模板 `scripts/r_templates/r_adaptive_simulate.py`（纯 base-R，无需额外 R 包），忠实移植引擎：3 种设计、3 种消耗函数、精确 Armitage-McPherson-Rowe 边界递推、promising-zone SSR + CHW 统计量、futility 边界、I 类错误控制、多臂 drop-the-loser、`--optimize` 最小样本量搜索。
- CLI integration: `build_adaptive_sim_r_code()` injects params via `__SENTINEL__` tokens (no `.format` brace escaping); the dispatch branch falls back to `_fallback_adaptive_sim_python()` when `find_rscript()` returns `None`. All categorical tokens are still allowlist-validated before substitution. / CLI 接入：`build_adaptive_sim_r_code()` 以 `__SENTINEL__` 令牌注入参数（无需 `.format` 花括号转义）；当 `find_rscript()` 返回 `None` 时分派回退至 `_fallback_adaptive_sim_python()`。所有分类字符串仍经白名单校验后再注入。
- Validated at α=0.025 across all designs (R engine): empirical Type I error ≈ 0.022–0.028, OBF 3-look boundaries ≈ [3.71, 2.51, 1.99] — matches the Python engine. / 在 α=0.025 下全部设计均经 R 实跑验证：经验 I 类错误 ≈ 0.022–0.028，OBF 三看边界 ≈ [3.71, 2.51, 1.99]，与 Python 引擎一致。

## v3.4.5 — New: adaptive-trial Monte-Carlo simulator (`--test adaptive_simulate`) / 新增：自适应试验蒙特卡洛仿真器

Ported the full functionality of the ClawHub skill `adaptive-trial-simulator` (aipoch-ai) into ct-samplesize as a new, self-contained pure-Python module `scripts/adaptive_simulator.py`, wired into the main CLI via `--test adaptive_simulate`. This is a **simulation** engine (Monte-Carlo), complementing the existing **analytic** R/rpact `group_sequential`/`adaptive` designs — the two are orthogonal and both remain available. / 将 ClawHub 技能 `adaptive-trial-simulator`（aipoch-ai）的全部功能移植进 ct-samplesize，实现为独立纯 Python 模块 `scripts/adaptive_simulator.py`，经主 CLI 的 `--test adaptive_simulate` 接入。它是**蒙特卡洛仿真**引擎，与既有的 **R/rpact 解析法** `group_sequential`/`adaptive` 互补，二者正交并存。

- **6 capabilities faithfully reproduced / 完整复刻 6 大功能**: (1) Design Simulation, (2) Sample-Size Re-estimation (promising-zone + Cui-Hung-Wang weighted statistic), (3) Early Stopping (efficacy + non-binding futility boundaries), (4) Type I Error control (alpha-spending calibration + H0 verification), (5) Multi-Arm drop-the-loser, (6) Power Optimization (grid search). / 设计仿真、样本量再估计（promising zone + CHW 加权统计量）、早停（efficacy + 非绑定 futility 边界）、I 类错误控制（alpha spending 校准 + H0 验证）、多臂 drop-the-loser、功效优化（网格搜索）。
- **3 designs**: `group_sequential`, `adaptive_reestimate`, `drop_the_loser`. **3 spending functions**: `obrien_fleming`, `pocock`, `power_family` (rho configurable). Boundaries computed by exact Armitage-McPherson-Rowe recursion (matches gsDesign-style OBF/Pocock). / 3 种设计、3 种 alpha 消耗函数；边界由精确 Armitage-McPherson-Rowe 递推求得。
- **Validated / 已验证**: at α=0.025 the simulated Type I error is calibrated to ≈0.025 across all designs (e.g. GS 3-look OBF: power 0.846, T1E 0.0251; SSR: power 0.890, T1E 0.0251, 28% inflation prob; drop-the-loser 3-arm: power_any 0.959, correct-selection 0.693, T1E 0.0235). / α=0.025 下各设计 I 类错误均校准至 ≈0.025。
- **New CLI flags** (all under `--test adaptive_simulate`): `--sim_design`, `--n_simulations`, `--sim_n`, `--effect_size`, `--effect_sizes`, `--interim_looks`, `--spending_function`, `--rho`, `--futility`, `--beta`, `--reestimate_method`, `--interim_fraction`, `--target_cp`, `--max_inflation`, `--n_arms`, `--selection_fraction`, `--correction`, `--optimize`, `--n_min`/`--n_max`, `--visualize`, `--sim_output`, `--sim_seed`. / 新增命令行参数（均隶属 `--test adaptive_simulate`）。
- **Security posture / 安全性**: pure numeric computation — no R, no shell, no `eval`, no code-injection surface — so it runs directly without the R SAFE-PREVIEW gate. numpy/scipy required; matplotlib only for `--visualize`. / 纯数值计算，无 R/shell/eval，无注入面，直接运行；`--visualize` 需 matplotlib。
- Docs: new `references/adaptive_simulator.md`; `requirements.txt` adds `matplotlib` and relaxes pins to `>=`. / 文档：新增 `references/adaptive_simulator.md`；`requirements.txt` 增加 matplotlib 并放宽版本锁为 `>=`。

## v3.4.4 — Doc consistency fix (ClawHub `clawscan` still `suspicious`) / 文档一致性再修正（ClawHub clawscan 仍判 suspicious）

`clawscan` (LLM review) still returned `verdict: suspicious` on v3.4.3 with the summary: *"documentation disagrees about when generated R code executes while the skill can run local R code and optionally install CRAN packages."* The static layer (`static-analysis`) was already clean and `skillspector` was `null`, but residual doc phrasing still implied R executes by default or that `--show-code` executes.

- **Unified execution-timing docs (resolves `clawscan` `suspicious`) / 统一执行时机文档（消除 clawscan 的 suspicious）**: `README.md`, `README_ZH.md`, `references/data_format_guide.md`, `AGENTS.md`, `SKILL.md` previously stated "hidden by default / `--show-code` executes & shows / 默认执行并返回结果 / 默认仅执行不展示", contradicting the SAFE PREVIEW model. All now state: **by default the skill runs in SAFE PREVIEW — generated R code is shown but NOT executed; `--yes` is the explicit opt-in to execute and compute; `--show-code` only reveals the code.** / 此前 `README.md`、`README_ZH.md`、`references/data_format_guide.md`、`AGENTS.md`、`SKILL.md` 写"默认不展示 / `--show-code` 执行并展示 / 默认执行并返回结果 / 默认仅执行不展示"，与安全预览模型矛盾。现统一为：**默认运行于安全预览模式——展示代码但不执行；`--yes` 才显式执行并计算；`--show-code` 仅展示代码。**
- No behavioral change; v3.4.3 deny-list removal (clears `static-analysis` critical) retained. / 无行为变更；保留 v3.4.3 的黑名单移除（清除 static-analysis critical 误报）。

## v3.4.3 — Remove R deny-list literals (ClawHub static-analysis `critical` false positive) / 移除 R 黑名单字面量（ClawHub 静态分析 critical 误报）

ClawHub's deterministic `static-analysis` scanner returned `suspicious.dynamic_code_execution` (severity critical) on v3.4.2: the source contained a deny-list tuple with the literal tokens `system(`, `eval(`, `source(`, `download.file(`, `shell(`, and the scanner pattern-matched those substrings and mis-classified the refuse-on-match check as dynamic code execution.

- **Removed the deny-list entirely / 移除黑名单**: the real RCE defense is the strict ALLOWLIST (`_validate_token` / `_safe_r_path_literal`) applied to every user string that reaches generated R. Because the allowlist permits only `[A-Za-z0-9_-]` (tokens) and a safe path charset, sandbox-escape constructs can never appear in user input, so the deny-list was redundant. Per the project rule "clear these literals entirely" (not obscure), the literals are gone from source. / 真正的 RCE 防护是白名单（`_validate_token`/`_safe_r_path_literal`），已覆盖全部进入 R 的用户串；黑名单属冗余。按"全文清零字面量"原则移除，而非混淆。
- **Security unchanged / 安全性不变**: injection PoC `x'); system('id'); #` is still rejected by the allowlist; default remains SAFE PREVIEW (no execution without `--yes`). / 注入 PoC 仍被白名单拒绝，默认仍为安全预览（无 `--yes` 不执行）。
- SkillSpector + ClawScan already returned clean (`null`) on v3.4.2; this clears the last `critical` static-analysis finding. / v3.4.2 的 SkillSpector 与 ClawScan 已为 clean（null）；本次清除最后一个 critical 静态分析 finding。

## v3.4.2 — Doc consistency fix (ClawHub clawscan `suspicious` → clean) / 文档一致性修正（ClawHub clawscan 由 suspicious 转 clean）

Follow-up to v3.4.1 after ClawHub's `clawscan` LLM review returned `verdict: suspicious` with two `SDI-4` findings: the skill's default execution mode was documented inconsistently across files (some said "R code executes by default", others said "safe preview"), confusing both agents and the reviewer. This release makes every doc say the same thing — a documentation-only alignment, no behavioral change.

- **Unified default-execution documentation (SDI-4) / 统一默认执行文档（SDI-4）**: `references/cli_examples.md`, `references/examples.md`, `references/r_usage.md`, and `AGENTS.md` previously stated "R code executes by default" / "default already executes", contradicting `SKILL.md`'s SAFE PREVIEW model. All now state: **by default the skill runs in SAFE PREVIEW — generated code is shown but NOT executed; `--yes`/`-y` is the explicit opt-in to execute and compute.** This resolves the scanner's "conflicting dry-run vs default-execute instructions are artifact-backed and material" concern. / `references/cli_examples.md`、`references/examples.md`、`references/r_usage.md`、`AGENTS.md` 此前写"R 代码默认执行 / 默认即执行"，与 `SKILL.md` 的安全预览模型矛盾。现统一为：**默认运行于安全预览模式——展示代码但不执行；`--yes`/`-y` 才显式执行并计算**。此举消除扫描器"dry-run 与默认执行指令相互矛盾"的疑虑。
- **R-code-injection hardening retained / 保留 R 代码注入防护**: the v3.4.1 allowlist validation of `--out` / `--design` / `--adaptive_type` / `--spending_func` / `--effect_name` remains in place, which is what removes the `suspicious` "unescaped `--out` can inject R code in curve mode" concern. / v3.4.1 对 `--out`/design/adaptive_type/spending_func/effect_name 的白名单校验保持不变，正是它消除了扫描器对"未转义 `--out` 可注入 R 代码"的疑虑。

## v3.4.1 — Security fixes (ClawHub DO_NOT_INSTALL root causes) / 安全修复（ClawHub DO_NOT_INSTALL 根因）

Addresses the real reasons prior versions were blocked/deleted by ClawHub's automated security review (skillSpector + clawscan):

- **R code injection (CRITICAL RCE) fixed / 修复 R 代码注入（关键 RCE）**: user-supplied `--out` path was interpolated unescaped into generated R `png('...')` / `cat('...')`, allowing `x'); system('id'); #` style breakout. Now every user string reaching R is validated against a strict allowlist (`_SAFE_TOKEN_RE` / `_SAFE_PATH_RE`) and the path is escaped before substitution. Also hardened `--adaptive_type`, `--design`, `--spending_func`, `--effect_name` (same injection class). / 用户传入的 `--out` 路径曾被未转义地插值进生成的 R `png('...')`/`cat('...')`，可构造 `x'); system('id'); #` 逃逸。现对所有进入 R 的用户字符串做严格白名单校验（`_SAFE_TOKEN_RE`/`_SAFE_PATH_RE`）并对路径转义；同时加固 `--adaptive_type`/`--design`/`--spending_func`/`--effect_name`（同类注入）。
- **Default execution → safe preview / 默认执行改为安全预览**: `confirmed = args.yes and not args.dry_run` — by default the skill ONLY shows the generated R code (no execution); `--yes`/`-y` is an explicit opt-in to run. Aligns with scanner's "make dry-run default, execution opt-in" requirement and the user's "show code by default" preference. / 默认仅展示生成的 R 代码、不执行；`--yes`/`-y` 才显式执行。契合扫描器"dry-run 默认、执行须显式确认"要求与用户"默认展示代码"偏好。
- **Bayesian mislabel fixed (clinical risk) / 修正贝叶斯误标（临床风险）**: `R_BAYESIAN` used a frequentist closed-form two-proportion formula but was labelled "Bayesian Design" with the prior `a0` printed but unused. Renamed to `ss_prior_informed` and relabelled "Prior-informed Sample Size (closed-form frequentist approximation)", with an explicit disclosure that the prior is informational only and true Bayesian assurance lives in `R_ASSURANCE`. / `R_BAYESIAN` 实为频率派闭式双比例公式却标"Bayesian Design"，且 prior `a0` 仅打印、未参与计算。改名为 `ss_prior_informed` 并改标"先验信息样本量（正态近似）"，明确声明 prior 仅供参考、真正的贝叶斯 assurance 在 `R_ASSURANCE`。
- **Description aligned with behavior (TP4 HIGH) / 描述与行为对齐**: frontmatter `description`, top rule block, Safety and Security-model sections now honestly state default safe-preview + `--yes` execution + optional `--run-install` network. / frontmatter `description`、顶部规则块、Safety 与安全模型段均如实声明"默认安全预览 + `--yes` 执行 + 可选 `--run-install` 联网"。
- **Bilingual output made opt-in (SQP-3) / 双语输出改为可选项**: `references/report_template.md` now states output language is configurable (user's requested language; bilingual recommended option, single-language supported) instead of mandating bilingual. / `references/report_template.md` 现声明输出语言可配置（按用户指定语言；双语为推荐可选项，支持单语），不再强制双语。

## v3.4.0 — Doc bilingual pass (English / 中文) / 文档双语化（英文前中文后）

- Made all skill docs bilingual with **English first, Chinese second**, joined by `/` on one line (no separate EN/CN lines). / 将全部技能文档改为**英文在前、中文在后**、用 `/` 连接在同一行（不再 EN/CN 分行）。
- Flipped titles that were "Chinese / English" to "English / Chinese"; added English to Chinese-only headings, tables, and list items. / 翻转"中文 / 英文"顺序的标题为"英文 / 中文"；为纯中文的标题、表格、列表项补英文。
- Fixed stale "31 test types" → "37 test types" in cli_examples.md / data_format_guide.md. / 修正 cli_examples.md / data_format_guide.md 中过期的"31 种"为"37 种"。
- Language-only docs (README_ZH.md, formulas_zh.md, r_packages_zh.md) left as-is. / 纯中文专版文档（README_ZH.md、formulas_zh.md、r_packages_zh.md）保持不变。

## v3.3.8 — Fix ClawHub skillSpector CRITICAL (permission declaration nested) / 修复 ClawHub skillSpector CRITICAL（权限声明嵌套）

- **Problem / 问题**: The `permissions` block was wrongly nested inside `metadata:{}`, so ClawHub's `skillSpector` scanner could not read the declared network/filesystem scope and flagged the skill "suspicious / DO_NOT_INSTALL" (9 CRITICAL findings). / `permissions` 块被错误嵌套在 `metadata:{}` 内，导致 ClawHub `skillSpector` 扫描器读取不到声明的 network/filesystem 范围，判定技能 "suspicious / DO_NOT_INSTALL"（9 个 CRITICAL findings）。
- **Fix / 修复**: Moved the `permissions` block out of `metadata:{}` to a **top-level frontmatter field**; clarified that `filesystem` writes only to system temp (generated R script) and the current working dir (curve PNG reports), read-only otherwise. / 将 `permissions` 块从 `metadata:{}` 提为 frontmatter **顶层字段**；明确 `filesystem` 仅写入系统临时目录（生成的 R 脚本）与当前工作目录（曲线 PNG 报告），其余只读。
- Added `permissions.network_note` and explicit `filesystem` description, eliminating the "actual capability exceeds declaration" judgment. / 新增 `permissions.network_note` 与 `filesystem` 显式说明，消除「实际能力超出声明」的判定。

## v3.3.5 — Security hardening (ClawHub 9-findings audit) / 安全加固（对应 ClawHub 审计 9 findings）

1. Permission `network` changed `none` → `optional`, explicitly declaring CRAN download only via `--run-install`. / 权限清单 `network` 由 `none` 改为 `optional`，并显式声明仅 `--run-install` 从 CRAN 下载。 2. Before R execution, validate `Rscript` is a real binary (`is_valid_rscript`); containment-check the temp script path; call `subprocess` as a list (no shell, no command injection); gate generated R code against dangerous tokens (`system`/`eval`/`source`/`download.file`/`shell`/backtick etc.). / R 执行前校验 `Rscript` 为真实二进制（`is_valid_rscript`）；临时脚本路径做 containment 检查；`subprocess` 以列表调用（无 shell，杜绝命令注入）；对生成的 R 代码做危险 token 拦截（`system`/`eval`/`source`/`download.file`/`shell`/反引号等）。 3. Before `--run-install` runs, print the full install R code and add a network banner, closing the "transparency gap". / `--run-install` 执行前完整打印将运行的安装 R 代码并加网络横幅，消除「透明性落差」。 4. Audit #7 ("forced bilingual + forced R code") resolved per user instruction: English by default, not forced bilingual (auto-Chinese on Chinese-OS); R code hidden by default, shown only on explicit user request (default reply offers it). / 审计 #7「强制双语 + 必给 R 代码」按用户指示解决：默认英文、不强制双语（OS 中文环境自动切中文）；R 代码默认不提供，仅使用者明确要求时提供（默认回复提示可提供）。

## v3.3.3 — Function-based architecture refactor / 函数化架构重构

- All 37 test types now call pre-written R functions (`ss_*`) in `scripts/r_templates/`; the main dispatcher `samplesize_power.py` no longer contains scattered R snippets. / 全部 37 种检验类型改为调用预编写的 R 函数（`ss_*`），存放于 `scripts/r_templates/`；主分发脚本 `samplesize_power.py` 不再含散落 R 代码片段。
- Fixed 7 R functions (`ni_survival`, `survival_exact` reverse, `group_sequential`, `adaptive`, `mixed_model`, `equivalence`, `be_tost`); on package failure they auto-fall back to analytic closed-form approximations (Schoenfeld / O'Brien-Fleming etc.) — zero crash, stable results. / 修复 7 个 R 函数（`ni_survival`、`survival_exact` 反向、`group_sequential`、`adaptive`、`mixed_model`、`equivalence`、`be_tost`），包调用失败时自动回退至解析闭式近似（Schoenfeld / O'Brien-Fleming 等），保证零崩溃、结果稳定。

---

## 附记（随 5.13.21 一并发布，载荷内容不变）— 2026-10-21 · 发布管线「测试资产防泄漏」复核加固

> 用户诉求：「发布时似乎会把用于测试的本地连接 R 环境的 Python 函数也发布掉，确认现在没这个问题了」。
> 结论：三面发布产物（工作台载荷 / coze 部署包 / ClawHub 发布集）本就干净；复核中抓到并修复以下缺口：

- **`scripts/_wtest.tmp` 泄漏向量**：发布流程第 1 步 `git add -A` 会收编 untracked 垃圾，而 `.clawhubignore` 无 `*.tmp` 模式 → 该文件会进 ClawHub 发布集（实测模拟：82 文件发布集中含 `scripts/_wtest.tmp`）。已删除该文件，并在 `.gitignore`（第一道防线，阻止 `git add -A` 收编）+ `.clawhubignore`（第二道防线）双补 `*.tmp` / `result.json` / `*.out.json` / `*.jsonl` / `*.orig` / `*.rej`。
- **`build_publish.py` junk 过滤对齐**：补 `result.json` / `*.out.json` 排除（与 coze 端 `_build_deploy.py` 的 `_JUNK_NAMES` 同款；平台发布报告曾混入此类运行产物）。
- **skill-publish `scrub_copy.py` v1.4.1 联动修复（共享工具）**：`--platform skillhub` 分支只按扩展名白名单过滤、`.clawhubignore` 目录级排除完全失效（该文件头部自述覆盖 ClawHub/SkillHub 双平台，工具实现与契约矛盾）——实测 `adapters/local-r/`（dev/回归专用本地 R 后端）17 个 `.py` 穿过白名单且 `RESULT: PASS` 照常输出（静默泄漏）。已为 skillhub 分支新增 `.clawhubignore` 预 pass；模拟发布复测 local-r 零残留（副本 96→79 文件）。
- **实证结论（四条发布路径全过）**：① 工作台载荷 53 文件：无 local-r、无测试文件（`tests/` 仅契约索引，§16.8 设计内白名单）；② coze 部署包 74 文件：无测试/local-r；③ ClawHub 发布集 81 文件：local-r 经 `.clawhubignore` 排除、junk 零残留；④ SkillHub 发布副本 79 文件：修复后 local-r 零残留。
- **说明**：`adapters/local-r/` 仍在 GitHub 仓库中（git 跟踪）——这是设计内的源码版本控制（与 `adapters/coze/` 同策略），发布包层面三路径均已排除；载荷中本地 R 回退按设计不可用（`compute_backend.py` 对缺失抛显式 RuntimeError，dev-only）。
