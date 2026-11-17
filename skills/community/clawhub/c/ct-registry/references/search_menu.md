# 检索细节确认菜单框架 / Search Confirmation Menu (ct-registry 定制版)

> 本文件是 ct-base `references/search_menu.md` 在 **ct-registry** 上的定制实现。
> 它定义自然语言对话中，AI Agent 引导用户确认 **临床试验注册库检索参数** 的通用交互流程。
> 菜单结构、对话状态机与 ct-base 框架保持一致；参数表、推荐预设、异常处理按 ct-registry
> 的真实参数清单（见 `scripts/ct_registry.py`）定制。
>
> ct-registry 架构要点（影响菜单设计）：
> - **CT.gov 为必需直连源（Tier 1，纯 HTTP）**；搜英文关键字。
> - **EU CTR（legacy EudraCT）为可选直连源（Tier 1，纯 HTTP 解析）**；搜英文关键字。
> - **CDE / ChiCTR / ISRCTN / DRKS / WHO ICTRP 为可选外部服务工作流（Tier 2，Bearer token，无浏览器）**；
>   ChiCTR/ISRCTN/DRKS 经统一端点 `search_ictrp.py --source {chictr,drks,isrctn}` 接管（与 WHO/CDE 共用一枚 token，v0.3.30+ 已就绪），不再为 PLACEHOLDER。
>   **WHO ICTRP 端点已就绪**（`https://ct-search.coze.site/run`，`source="who"`）；
>   该端点**接受 Coze workload-identity (SPIFFE) JWT**（与 CDE 同为该类 token，CDE 已用 live token 验证可用），
>   该 token **本地化落盘后长期有效、不会过期**，无需每次取数前重签；仅极罕见情况下（token 文件损坏/被吊销/权限不足）返回
>   **403** "insufficient permissions"，届时再经 `search_ictrp.py --store-token` 重签即可。WHO ICTRP
>   一次镜像 14+ 注册库（jRCT/DRKS/ANZCTR/ISRCTN/CTRI/…），是低成本拓宽覆盖的首选。
>   **该统一端点同时服务中国 CDE**（`source="chinadrugtrials"`，由 `search_ictrp.py --source chinadrugtrials` 驱动；`ct_registry.py --with-cde` 默认走此路）。独立端点 `ct-searchcde.coze.site/run`（`CDE/search_cde_workflow.py`，已归档至本地 `CDE/`、不随包发布）已于 **2026-08-12 正式退役**，不再作为可用回退；统一端点异常时 `--cde-legacy` 仅打印废弃警告并自动回退统一端点。一枚 token（`config/ictrp.dat`）同时覆盖 WHO 与 CDE。
> - WHO ICTRP 的桥接/去重价值由 `aggregate.py` 内部**复现并强化**（不只替代），故菜单中**包含** ICTRP 选项。
> - **WHO 主路径 / 被覆盖源兜底策略（2026-07-28）**：仅当 `ct_registry.py --with-ictrp` 设置时启用。
>   此时 WHO ICTRP 为**主聚合器**，它已镜像的试验注册库（**CT.gov / EU-CTR / ISRCTN / DRKS / ChiCTR**）
>   降为**仅作备用**——WHO 检索成功则跳过这些源（WHO 已镜像，避免重复）；**仅当 WHO 无法检索**（调用异常 / 非 200 /
>   返回 `error_msg`）时才询问用户。失败时脚本打印 `[ct_registry][FALLBACK-PROMPT]` 列出备用源并**停止**（不自动扇出）；
>   用户确认后加 `--fallback-covered` 重跑，即对各覆盖源分别独立检索并聚合（**不含 CDE**；CDE 始终独立检索，见下）。
>   **例外 — CDE 始终独立**：中国 CDE（`--with-cde`）**不属**此回落集合——WHO 的英文标题匹配会漏掉中文注册的试验，
>   故 CDE 在 `--with-cde` 时**无论 WHO 成败都独立检索**。PubChem 富集不受影响（非试验注册库）。
>   **`--with-ictrp` 不设置时完全保持旧行为**（CT.gov 必跑，其余按各自 `--with-*` 标志）。
> - **关键字本地化**：同一检索词按源语言自动切换（CT.gov/EU CTR/ISRCTN/DRKS→EN；CDE/ChiCTR→ZH）。
>   国外源关键字若未命中术语表，会触发**确认门**（CONFIRM → ABORT），菜单需承接该确认。
> - **高级检索优先规则（v0.3.14）**：WHO AdvSearch（`trialsearch.who.int/AdvSearch.aspx`）提供
>   **Phases** 等结构化字段、CDE AdvSearch（`chinadrugtrials.org.cn/...prosearch.dhtml?pro=y`）提供
>   登记号/适应症/药物名称/药物类型/申请人/试验状态等（**无期次过滤**）。**当用户的提示词出现
>   参数组合（如 药物+分期、疾病+申办方+国家+年份）时，Agent 应首选构造结构化/高级检索载荷，
>   而非裸关键字检索**：WHO 用 `--who-condition/--who-intervention/--who-sponsor/--who-country/
>   `--who-phase` 等（自动 `mode=combined`）；CDE 用 `--reg-no/--indication/--drugs-name/--drugs-type/
>   `--appliers/--trial-status` 等（自动 `is_advanced_search`）。完整字段→CLI 映射见 SKILL.md
>   「Advanced search (高级检索)」小节。**关键警示**：`--who-phase` 服务端过滤用的归一化字段较窄，
>   会漏掉联合期/数字期（实测 `Olverembatinib` +I/II 仅返回 2 条，而 detail 真实 I/II 约 19 条），
>   故 `--who-phase` 仅作粗筛降量，**最终分期以 detail 归一化 `phase` 后筛为准**，切勿仅凭
>   `who_phase` 丢弃记录。

---

## 1. 对话状态机 / Dialogue State Machine

```
用户请求 → [识别意图] → 收集参数 → 【关键字体系确认门】(强制, 先于 Gate1) → [Gate1 检索前简报] → 执行检索 → [Gate2 列表确认] → (可选)详情/下载
                ↑________↓              ↑________↓              ↑________↓
                (参数缺失时追问)         (范围/词歧义→选择确认)   (≤100 直接详情；>100 先确认列表再详情)
                                       (国外源术语未命中 → 确认门)
```

## 2. 参数收集清单模板 / Parameter Checklist Template

| 参数 | 必填 | 默认值 | 追问话术 |
|------|:----:|--------|----------|
| `--cond` 疾病/适应症 | ✅* | — | "请告诉我检索的疾病或适应症（如 非小细胞肺癌 / NSCLC）" |
| `--intr` / `--drug` 干预/药物 | ✅* | — | "需要限定干预措施或药物吗？（如 osimertinib / 奥希替尼）" |
| `--sponsor` 申办方 | ❌ | — | "需要限定申办方（企业/研究者）吗？" |
| `--status` 试验状态 | ❌ | 不限 | "需要限定试验状态吗？（如 招募中 RECRUITING / 已完成）" |
| 数据源 sources | ❌ | CT.gov + EU CTR | "要覆盖哪些注册库？" |
| `--max` 每源上限 | ❌ | 50 | "每个注册库最多取多少条？（默认 50）" |
| `--with-pubchem` 药物靶点富集 | ❌ | off | "是否需要额外做药物→靶点（PubChem）映射？" |
| CDE 高级筛选 | ❌ | 关闭 | "是否对 CDE 启用结构化筛选（适应症/药物类型/试验状态）？" |

> \* `cond` 与 `intr`/`drug` 至少给其一即可继续（二者是检索主轴的两种表达）。

### 2.1 数据源选项 / Source Options

| 选项 | 注册库 | 层级 / 访问 | 关键字语言 | 说明 |
|------|--------|------------|-----------|------|
| ① CT.gov | ClinicalTrials.gov | Tier 1 直连（必需） | EN | 全球主源，字段最全，更新最频 |
| ② EU CTR | 欧盟（legacy EudraCT） | Tier 1 直连 | EN | 欧盟试验，纯 HTTP 解析 |
| ③ CDE | 中国药物临床试验登记平台 | Tier 2 外部服务 | ZH（静默降级，中文 0 条时自动补发英文） | 中国法定药物试验；已实测可用 |
| ④ ChiCTR | 中国临床试验注册中心 | Tier 2 外部服务 | ZH | 中国研究者发起试验；端点待 provisioning |
| ⑤ ISRCTN | 国际标准随机对照试验号库 | Tier 2 外部服务 | EN | 英国/国际；端点待 provisioning |
| ⑥ DRKS | 德国注册库 | Tier 2 外部服务 | EN | 德语区；端点待 provisioning |
| ⑦ WHO ICTRP | 国际临床试验注册平台 | Tier 2 外部服务 | EN | 一次镜像 14+ 注册库(jRCT/DRKS/ANZCTR/ISRCTN/CTRI/…)，低成本拓覆盖；本地 token 长期有效 |
| ⑧ PubChem | 药物→靶点映射 | Tier 1 直连（富集） | EN | 非注册库，用于机制/靶点背景 |

> 多选、可叠加；菜单为**引导**而非互斥树——例："看德国试验"既可从"区域"入口勾 DRKS，
> 也可从"全部源"入口勾 DRKS，路径互补（遵循 ct-base AGENTS.md §6 非互斥原则）。

## 3. 快速模式 / Quick Mode

当用户请求已包含 **≥2 个明确参数** 时，**跳过逐项追问**，直接进入预览确认。

**触发示例**：
- "检索 osimertinib 的招募中试验" → 含 intr + status，直接预览
- "查 NSCLC 在欧洲的试验" → 含 cond + EU CTR 源，直接预览
- "奥希替尼 高血压 中国试验" → 含 drug + 中国源（CDE/ChiCTR），直接预览

## 4. 菜单选项模板 / Menu Templates

### 4.1 初始确认菜单（参数不足时）

```
🔬 临床试验检索准备

当前已识别：
- 检索主题：{cond / intr}
- 申办方：{sponsor}
- 试验状态：{status}
- 数据源：{sources}

还需要确认：
1. 检索主题 — 疾病 / 适应症，或 干预 / 药物（必填）
2. 试验状态 — 不限 / 招募中 / 已完成 / 自定义
3. 数据源   — 仅主源(CT.gov+EU CTR) / +中国(CDE+ChiCTR) / 全球全部 / 自定义
4. 每源上限 — 默认 50
5. 药物靶点 — 是否附加 PubChem 富集（是 / 否）

请回复编号选择，或直接说"默认"使用推荐配置（CT.gov + EU CTR，状态不限，上限 50）。
```

### 4.0 关键字体系确认门菜单（参数齐全后、Gate 1 之前，强制）

> `ct_registry.py` 在 `--run` 分支、构建各源命令**之前**自动触发：调用 `expand_keyword()`
> 扩写出完整关键字体系（中英互译 + 同义/别名 + 药物类别枚举），渲染本菜单并**停止**，
> 待用户选「采用」（`--kw-adopt` 重跑）后才继续；用户显式 `--no-expand` 可跳过。

```
🔍 关键字体系（自动扩展 + 中英互译）— 请确认 / 补充后再检索

原文：{base} ｜ 意图：{intent_label}
【中文候选】{zh}
【英文候选】{en}

【按源分配】
  · CT.gov + WHO（英文·精确）：{per_source.ctgov.keywords}
  · CDE + ChiCTR（中文·子串）：{per_source.cde.keywords}
⚠ 风险提示：{risks}
📝 推测词（建议留意/可删）：{confidence.speculative 或 "无"}

请确认：
  1. ✅ 采用以上关键字体系（推荐）
  2. ✏️ 删除某些词（回复：删 <词>）
  3. ➕ 补充我自己的词（回复：加 <词>）
  4. 🔄 改用更窄 / 更宽范围
  0. ❌ 取消
（确认后才进入检索范围/配额确认 → 正式检索）
```

- 多轴（疾病 + 干预同时给定）用 `render_kw_system_menu_multi`：每组一块，末尾统一一个动作菜单。
- 同词本会话命中 `config/kw_system_cache.json` 缓存时不再弹门，直接采用（删缓存或换词即重确认）。

### 4.2 预览确认菜单（参数齐全后）

```
🔬 检索预览（Gate 1 · 检索前简报）

| 参数 | 值 |
|------|-----|
| 检索主题 | {cond / intr} |
| 申办方 | {sponsor} |
| 试验状态 | {status} |
| 数据源 | {sources} |
| 高级检索字段 | {adv_fields}（WHO: condition/intervention/sponsor/country/phase；CDE: 登记号/适应症/药物名/药物类型/申请人/试验状态；无则"无"） |
| 时间窗 | {year_filter} |
| 每源上限 | {max} |
| PubChem 富集 | {with_pubchem} |

⚠️ 关键字本地化提示：
- CT.gov / WHO 将以英文检索：{en_keyword}
- CDE / ChiCTR 将以中文检索：{zh_keyword}（CDE 默认静默降级：中文 0 条时自动补发英文）
{若国外源未命中术语表：→ 需确认英文译文（见下方"确认门"）}

💡 计费说明：合并为 1 个需求（demand_id={demand_id}）；**当前免费使用**，每日上限 1000 个需求，
配额与资源使用详情见 README「配额与资源使用」小节。

确认执行？
1. ✅ 直接执行（推荐）
2. ✏️ 修改参数（回复编号）
3. ❌ 取消
```

> **Gate 1 规则（2026-07-30）**：以上简报**每次检索前必出**。若范围 / 关键词翻译 / 解读存在
> 歧义或有 ≥2 个合理选项，则用选择菜单先与使用者确认；若一切明确，简报本身即通知，使用者仍可打断。
> 直连源（CT.gov/EU-CTR/PubChem）不计入共享配额；外部工作流源（WHO/CDE/…）按需求计 1 次。

> **Gate 2 规则（2026-07-30 更新）**：列表检索完成并生成报告后，**先展示列表**（总数、范围、若干样例、
> 以及"列表模式 phase/sponsor 为 Unknown"提示）。**详情（detail）抓取按条目数量分两档**：
> - **≤100 条** → 🟢 直接抓取详情，无需确认（列表摘要仅作参考展示）；
> - **>100 条** → 🟡 先请使用者确认列表条目是否正确，确认后再抓取详情。
> 文档（PDF）**绝不自动下载**，始终需使用者显式确认（独立于上述详情规则）。

### 4.3 修改子菜单（用户选择修改时）

```
修改哪项？
1. 检索主题（当前：{cond / intr}）
2. 申办方（当前：{sponsor}）
3. 试验状态（当前：{status}）
4. 数据源（当前：{sources}）
5. 每源上限（当前：{max}）
6. PubChem 富集（当前：{with_pubchem}）
0. 返回上级

回复编号 + 新值，例如："4 全球全部" 或 "3 招募中"
```

## 5. 推荐配置策略 / Recommended Presets

| 场景 | 推荐配置 |
|------|----------|
| 快速了解某病/药全球试验格局 | CT.gov + EU CTR（直连），状态不限，max 50 |
| 中国全覆盖（药物试验 + 研究者发起） | CT.gov + CDE（静默降级）+ ChiCTR |
| 全球竞品 / 格局调研 | CT.gov + EU CTR + ISRCTN + DRKS + CDE + ChiCTR + WHO ICTRP |
| 仅看招募中试验 | 上述任一配置 + `--status RECRUITING` |
| 药物机制 / 靶点背景 | 任一配置 + `--with-pubchem --drug <药名>` |
| 仅本国 / 区域试验 | 只开对应注册库（DRKS=德国、ISRCTN=英国、EU CTR=欧盟、CDE/ChiCTR=中国） |

> **「全球竞品 / 格局调研」预设与 `--with-ictrp` 的关系**：该预设同时勾选 WHO ICTRP 与其已覆盖的
> CT.gov/EU-CTR/ISRCTN/DRKS/ChiCTR（**不含 CDE**——CDE 始终独立，见下）。一旦加 `--with-ictrp`，这些"被覆盖源"即降为**仅备用**——
> WHO 成功时自动跳过（不重复取数），仅 WHO 失败时才询问用户是否 `--fallback-covered` 扇出。因此该预设
> 在 `--with-ictrp` 下实际是"WHO 主取 + 备用兜底"，而非五源各取一份（与 legacy 行为不同）。
> **CDE 例外**：无论是否加 `--with-ictrp`，只要 `--with-cde` 设置，中国 CDE 都独立检索，不受 WHO 成败影响。

> 默认推荐：**CT.gov + EU CTR**。二者均为 Tier 1 直连、已实测可用、无需 token；
> Tier 2 外部服务（CDE 已可用；ChiCTR/ISRCTN/DRKS 端点待 provisioning；**WHO ICTRP 端点已就绪、
> 本地 token 长期有效（无需重签）**）作为增量覆盖按需开启。要最便宜地拓宽到 14+ 注册库，优先勾 WHO ICTRP。

## 6. 追问策略 / Follow-up Strategy

### 6.1 优先级

1. **检索主题（cond / intr / drug）缺失** → 必须追问，无法继续
2. **数据源缺失** → 默认推荐 CT.gov + EU CTR，预览时提醒可叠加其他源
3. **试验状态缺失** → 默认「不限」，预览时提醒
4. **每源上限缺失** → 默认 50，预览时提醒

### 6.2 追问上限

- 连续追问不超过 **2 轮**
- 第 2 轮仍缺主题 → 使用默认值 + 预览提醒（但主题缺失时不可执行，需提示用户补全）

### 6.3 追问话术示例

```
# 检索主题缺失
"请告诉我检索的疾病/适应症，或干预/药物名。例如：非小细胞肺癌、osimertinib、PD-1 抑制剂"

# 数据源确认
"当前默认检索 CT.gov + EU CTR（直连、无需 token）。需要叠加中国(CDE+ChiCTR)、
 国际(ISRCTN/DRKS/WHO ICTRP) 或药物靶点(PubChem) 吗？"

# 试验状态确认
"当前不限试验状态。需要限定吗？可选：招募中(RECRUITING) / 已完成 / 进行中 / 自定义"

# 每源上限
"每个注册库默认最多取 50 条。需要调整吗？（如 100）"
```

### 6.4 确认门承接 / Confirm-Gate Handling

当国外源（CT.gov / EU CTR / ISRCTN / DRKS / WHO ICTRP / PubChem）关键字 **未命中术语表** 时，
脚本会打印 `[CONFIRM]` + 建议英文译文并 `[ABORT]` 中止。菜单应在预览阶段主动承接：

```
⚠️ 检索词「{原始词}」未命中术语表，为避免 CT.gov 漏检，请确认英文译文：
   建议：{suggested_en}
   处理：① 直接以英文重写（如 "NSCLC"）；或 ② 回复 "确认英文 <译文>" 后重跑；
         或 ③ 仅用于已知安全自动化时加 --auto-confirm。
```

## 7. 输出确认 / Output Confirmation（Gate 2 · 检索后列表确认）

检索完成并生成列表报告后，**先展示列表摘要**（总数、范围、若干样例、以及"列表模式 phase/sponsor
为 Unknown"提示）。**详情（detail）抓取按条目数量分两档**：

- **≤100 条** → 🟢 直接抓取结构化详情（填充 phase/sponsor），无需使用者确认；列表摘要仅作参考展示。
- **>100 条** → 🟡 先请使用者确认列表条目是否正确，确认后再抓取详情：

```
🔬 检索完成！（列表预览 · 待你确认）

- 检索主题：{cond / intr}
- 原始记录：{raw_total} 条（跨 {source_count} 个注册库）
- 去重后唯一试验：{deduped_total} 条（跨库重复组 {cross_source_groups} 组已合并）
- 状态分布：招募中 {n_recruiting} / 已完成 {n_completed} / 其他 {n_other}
- 时间窗：{year_filter}
- 数据来源：CT.gov / CDE / EU CTR / ...（实际命中的源）
- ⚠️ 列表模式 phase / sponsor 均为 Unknown（仅 detail 模式填充）

请先确认列表是否准确（如需调整范围/关键字，回复即可，重跑复用同一 demand_id 免费）：
1. ✅ 列表无误，继续抓取详情
2. ✏️ 调整范围/关键字后重跑
3. ❌ 结束
```

> **文档（PDF）下载**：独立于详情规则，**绝不自动下载**，始终需使用者显式确认。
> **详情自动执行边界**：仅 >100 条需先确认列表；≤100 条直接抓取，不再另设二次确认。

## 8. 异常处理 / Error Handling

| 异常 | 处理 |
|------|------|
| 检索主题完全缺失 | "请先提供疾病/适应症或药物名，否则无法检索" |
| CT.gov 网络超时 / URLError | "CT.gov 网络超时。请检查网络后重试，或仅保留 EU CTR 直连源" |
| 国外源术语未命中（CONFIRM/ABORT） | 见 §6.4，提示用户确认英文译文后重跑 |
| CDE 401 (统一端点) | "CDE 主路径走统一端点 ct-search.coze.site/run，缺少 Bearer token。请配置 ICTRP_WORKFLOW_TOKEN / --token / config/ictrp.dat（与 WHO 共用一枚 token）。旧版 --cde-legacy 独立端点已于 2026-08-12 退役（仅打印警告），如仍需本地调用则配置 CDE_WORKFLOW_TOKEN / CDE/cde.dat" |
| CDE 403 | "CDE token 校验失败（极罕见：文件损坏/被吊销/权限不足），请检查并重签后重跑" |
| ChiCTR/ISRCTN/DRKS 401/404 | "这三个源经统一端点 `search_ictrp.py --source {chictr,drks,isrctn}` 调用（v0.3.30+ 已接管，与 WHO/CDE 共用一枚 token）。若仍返回 401/404，说明统一端点后端未对该 source 供数——改用 CT.gov + EU CTR + CDE，或联系作者确认后端 provisioning" |
| WHO ICTRP 401/403 | "WHO ICTRP 端点返回 401/403 = token 校验失败（极罕见：文件损坏/被吊销/权限不足；本地化 token 本长期有效、不会过期）。请检查 `config/ictrp.dat` 并重签一枚 Coze workload-identity token（与 CDE 同类型即可，无需 PAT），执行：python search_ictrp.py --store-token \"<new-jwt>\" 后重跑" |
| WHO 无法检索（`--with-ictrp` 时） | "WHO 主路径检索失败（异常 / 非 200 / 返回 error_msg）。WHO 已覆盖的 CT.gov/EU-CTR/ISRCTN/DRKS/ChiCTR 已设为仅备用，不会自动扇出（**CDE 不在此列——`--with-cde` 时仍独立检索**）。请确认是否对其分别独立检索并聚合：如需执行，加 `--fallback-covered` 重跑；否则仅保留未受影响的源或显式指定需检索的源" |
| 全部源 0 结果 | "未找到试验。建议：放宽状态/年份、切换检索词、或扩大数据源（含 WHO ICTRP 以触达 14+ 注册库）" |
| ICTRP 相关请求 | "WHO ICTRP 已是本技能 Tier-2 数据源（search_ictrp.py，source='who'）。可直接勾选纳入检索" |

## 9. 多语言支持 / i18n

- 中文环境 → 中文菜单 + 中文报告
- 英文环境 → 英文菜单 + 英文报告
- 混合模式 → 菜单中文，报告双语（默认）
- 检索关键字语言由 `ct-base/scripts/kw_localize.py` 按源自动切换，无需用户手动提供双语词

## 10. 对话示例 / Dialogue Example

```
用户：帮我查 osimertinib 在中国的试验

Agent：
🔬 临床试验检索准备
当前已识别：
- 检索主题：osimertinib（干预/药物）
推荐配置：CT.gov + CDE（静默降级）+ ChiCTR（中国全覆盖）
确认执行？
1. ✅ 直接执行（推荐）
2. ✏️ 修改参数
3. ❌ 取消

用户：1

Agent：[预览→执行]
🔬 检索完成！
- 检索主题：osimertinib
- 原始记录：CT.gov 320 + CDE 156 + ChiCTR(待端点) → 实际 {raw_total} 条
- 去重后唯一试验：{deduped_total} 条
- 状态分布：招募中 / 已完成 / 其他
后续操作：1 查看报告 2 下载JSON 3 重新检索 4 串联 ct-pipeline
```

```
用户：查 非小细胞肺癌 的招募中试验

Agent：
⚠️ 检索词「非小细胞肺癌」未命中术语表，为避免 CT.gov 漏检，请确认英文译文：
   建议：NSCLC
   处理：① 直接以英文重写（"NSCLC"）；或 ② 回复 "确认英文 NSCLC" 后重跑

用户：确认英文 NSCLC

Agent：[执行，CT.gov 以 NSCLC、CDE 以 非小细胞肺癌(双检) 检索]
🔬 检索完成！...（status=RECRUITING 限定）
```

## 11. 与 AGENTS.md §6 的关系 / Relation to AGENTS.md §6

本文件是 ct-base AGENTS.md §6「Menu / Navigation Design — Non-Exclusive」在
**自然语言对话** 场景下的具体实现（对应 §6.1 Natural Language Dialogue）。

- **AGENTS.md §6** 定义的是**图形界面 / 菜单导航** 的 UX 基线（非互斥树，同一源可出现在
  多个入口下）。
- **本文件** 定义的是**自然语言对话** 中的参数确认流程（状态机 + 菜单模板），并按
  ct-registry 的 `--cond/--intr/--sponsor/--status/--with-*/--max` 等参数定制。

两者共同构成 ct-registry 的完整交互设计规范。

---

## 12. 关键字匹配菜单 / Keyword-Matching Menu

> 对应 ct-base §8「主题词拼写异常 → 您是否想检索：{suggestion}？」。当检索词**非标准 /
> 未命中术语表 / 是药物类别词**时，不要静默反复试错，而是**生成候选解释菜单**由用户选择。
> 完整规则与实测数据见 `references/keyword_match.md`。

> **衔接说明**：关键字体系确认门（§4.0）是**前置、体系级**的确认（在 Gate 1 之前，强制），
> 负责把用户窄词扩写成完整关键字矩阵并请用户过目；本节 `kw_match_candidates` 菜单是
> 类别词 miss 时的**次级**补救菜单，二者并存不冲突。

### 12.1 为什么（实测结论 2026-07-28）
- WHO (`source=who`) 为**英文标题/字段精确匹配**：裸类别后缀 `sartan` 仅 6 条（加 5 年窗→0），
  缩写 `ARB`=604、具体药名 `valsartan`=1243；结构化 `intervention=sartan`=0，须填具体药名。
- 中国 CDE (`source=chinadrugtrials`) 为**中文子串匹配**：`沙坦`=788（`沙坦类`=0，须去「类」），
  英文 `sartan`=10 / `valsartan`=0 → **CDE 必须译中文**。

### 12.2 菜单模板 / Menu Template
```
🔍 关键字解析 — {keyword}

未命中标准术语表 / 属类别词, 请选择检索解释 (避免反复试错):
1. [translate] {中文/英文译文}     — 术语表翻译
2. [class_suffix] 沙坦            — 类别词→中文类名后缀 (适合 CDE)
3. [enumerate] valsartan/losartan/... — 枚举类别具体成员 (适合 WHO)
4. [as_is] {keyword}             — 直接用原文 (可能漏检)
0. 取消

回复编号选择; 或显式用 --confirm-*/--cde-keyword 指定后重跑。
```

### 12.3 实现接入 / Implementation
- 候选生成：`kw_localize.kw_match_candidates(text, source)` → 列表（含 `strategy/value/note`）。
- 渲染：`kw_localize.render_kw_menu(text, candidates)` → 编号菜单字符串。
- `ct_registry.py` 已接入：
  - **CDE 路径**：`localize(base,"zh")` 命中即用；`miss`（英文无法译中文）时打印菜单并 STOP
    （`--auto-confirm` 时自动采用 `translate`/`class_suffix`）。
  - **CT.gov 确认门**：外文词未命中时除建议译文外也打印候选菜单。
- 词表扩展：中英术语改 `ct-base/references/term_map.json`；类别后缀改 `kw_localize._CLASS_EN2ZH`；
  具体药名改 `kw_localize._DRUG_EN2ZH` / `_CLASS_MEMBERS`。
