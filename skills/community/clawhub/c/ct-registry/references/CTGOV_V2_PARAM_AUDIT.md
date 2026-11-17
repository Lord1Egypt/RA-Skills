# ClinicalTrials.gov v2 检索能力审计（2026-08-13）

> **✅ 整改状态（2026-08-13，v0.3.85）**：P0 + P1 + P2 **全部落地**到 `scripts/search_ctgov.py`
> （纯参数层扩展，向后兼容；离线断言全过 + **真实联网回归已跑通**——见 §4.1）。
> 官方 v2 `/studies` 全参数覆盖：10 个 query.*（rmtln 为 v1 遗留、v2 已移除）+ 5 个 filter.*
> （含 postFilter 同构）+ sort + fields。落地细节见 §4.1。
>
> **结论先行**：本地 `scripts/search_ctgov.py` 只覆盖了官方 v2 `/studies` 端点**约 1/3 的检索能力**——
> 9 个 `query.*` 词面参数只支持 3 个（cond / intr / spons），5 个 `filter.*` 筛选只支持 1 个
> （overallStatus 且仅单值），**网站高级检索的核心组合能力（`filter.advanced` 的 AREA[] 表达式、
> sort、服务端日期区间、多值状态）全部缺失**。作为即将成为主功能的检索，必须补齐。
>
> 好消息：缺的都是**纯参数透传**层，不碰 normalize/聚合管线（`norm_ctgov` 读取的是
> 响应 `protocolSection` 结构，与查询参数无关），风险可控。

---

## 1. 官方参数全景（OpenAPI 规范 + Search Areas + Expert Search 文档，2026-08-13 核实）

### 1.1 `query.*` — 词面检索（对应网站检索表单各输入框）

| 参数 | 对应网站字段 | 说明 |
|---|---|---|
| `query.cond` | Conditions or disease | 疾病/条件框（7 字段加权） |
| `query.term` | Other terms | 其他术语框（57 字段 BasicSearch，**支持 AREA[] 高级表达式**） |
| `query.intr` | Intervention / treatment | 干预/治疗框（12 字段加权） |
| `query.outc` | Outcome measure | 结局指标框（9 字段加权） |
| `query.titles` | Title / acronym | 标题/缩写框（3 字段） |
| `query.spons` | Sponsor / collaborator | 申办方/合作方框（3 字段） |
| `query.lead` | — | 仅 LeadSponsorName 字段 |
| `query.id` | Study IDs | 研究 ID 框（NCT/OrgStudyId/SecondaryId 等 5 字段） |
| `query.locn` | Location terms | 地点框（城市/州/国家/机构/邮编 5 字段） |
| `query.rmtln` | Remote location | 远程/虚拟试验（高级表单） |
| `query.patient` | — | 患者友好搜索（47 字段加权） |

> 全部支持 Essie 表达式语法（`OR` / `AND` / `NOT` / 括号 / 引号短语）。

### 1.2 `filter.*` — 结构化筛选（仅 5 个；注意：**没有**独立的 phase/studyType/age/sex/日期参数，全部走 `filter.advanced`）

| 参数 | 格式/枚举 | 说明 |
|---|---|---|
| `filter.overallStatus` | 14 枚举，**管道分隔多值**：`RECRUITING\|COMPLETED\|...` | 状态筛选 |
| `filter.advanced` | Essie 表达式，如 `AREA[Phase]PHASE3 AND AREA[StudyType]INTERVENTIONAL` | **高级组合的核心** |
| `filter.geo` | `distance(lat,lon,dist)` 如 `distance(39.00,-77.10,50mi)` | 地理距离（1–500 mi / 1–805 km） |
| `filter.ids` | 管道分隔 NCT 号，如 `NCT04852770\|NCT04527068` | 按 ID 批量 |
| `filter.synonyms` | `area:synonym_id` 对 | 内部同义词（一般不直接用） |

> 另有 `postFilter.*` 同构 5 个——与 `filter.*` 等价但不影响相关性排序（排序需求敏感时用）。

### 1.3 排序 / 分页 / 输出

| 参数 | 规则 |
|---|---|
| `sort` | 最多 **2 个**；`fieldName` 或 `fieldName:asc/:desc`；特殊值 `@relevance`（默认）；仅日期/数值字段（如 `LastUpdatePostDate`、`EnrollmentCount:desc`） |
| `pageSize` | 默认 10，**上限 1000**（超出强制降为 1000） |
| `pageToken` | 响应 `nextPageToken` 循环 |
| `countTotal` / `fields` / `format` | 计数 / 字段裁剪 / json\|csv |

### 1.4 Expert Search 高级语法（`filter.advanced` 与 `query.term` 共用）

- **字段定位**：`AREA[FieldName]value`，如 `AREA[InterventionName]aspirin`
- **布尔/分组**：`AND` `OR` `NOT`、`( )`、`"短语"`
- **匹配控制**：`COVERAGE[FullMatch|StartsWith|EndsWith|Contains]`（默认 Contains）
- **词形/同义**：`EXPANSION[None|Term|Concept|Relaxation|Lossy]`（默认 Relaxation）
- **来源运算符**：`MISSING`、`RANGE[MIN,MAX]`、`DISTANCE[lat,lon,r]`、`ALL`
- **评分**：`TILT[field]`（如 `TILT[StudyFirstPostDate]"heart attack"`）
- **转义**：运算符作普通词时加 `\`，如 `\MISSING`

---

## 2. 网站高级检索组合 → 本地实现差距矩阵

> 状态列已反映 v0.3.85 落地后视图（P0+P1+P2 全做）。

| 网站高级检索能做的组合 | 对应 API | 本地支持（v0.3.85） | 落地版本 |
|---|---|---|---|
| 疾病 / 条件 | `query.cond` | ✅ `--cond` | 原有 |
| 干预 / 治疗 | `query.intr` | ✅ `--intr` | 原有 |
| 申办方 / 合作方 | `query.spons` | ✅ `--sponsor` | 原有 |
| 状态（可多选） | `filter.overallStatus` | ✅ `--status` 逗号多值→管道 | v0.3.84 P0 |
| 其他术语（含专家表达式） | `query.term` | ✅ `--query`（支持 AREA[]） | v0.3.84 P0 |
| Phase 复选框 | `filter.advanced` → `AREA[Phase]PHASE3` | ✅ `--phase`（多值 `(A OR B)`） | v0.3.84 P0 |
| 研究类型（干预/观察/扩展） | `filter.advanced` → `AREA[StudyType]...` | ✅ `--study-type` | v0.3.84 P0 |
| 日期区间（首次发布/更新/完成/开始） | `filter.advanced` → `AREA[StartDate]RANGE[...]` | ✅ 5 组 `--*-since/--*-until` 服务端区间 | v0.3.84 P0 |
| 是否有结果 | `filter.advanced` → `AREA[HasResults]true` | ✅ `--has-results` | v0.3.84 P0 |
| 年龄组 / 性别 | `filter.advanced` → `AREA[StdAge]CHILD` 等 | ✅ `--age-group` / `--sex` | v0.3.84 P0 |
| 标题 / 缩写 | `query.titles` | ✅ `--titles` | v0.3.84 P1 |
| 结局指标 | `query.outc` | ✅ `--outc` | v0.3.84 P1 |
| 主要申办方 | `query.lead` | ✅ `--lead` | v0.3.84 P1 |
| 研究 ID | `query.id` | ✅ `--id` | v0.3.84 P1 |
| 地点 | `query.locn` | ✅ `--locn` | v0.3.84 P1 |
| 按日期/入组数排序 | `sort` | ✅ `--sort`（≤2 个，`field[:asc\|:desc]`/`@relevance`） | v0.3.84 P0 |
| 按 NCT 号批量取 | `filter.ids` | ✅ `--ids` | v0.3.84 P1 |
| 字段裁剪 | `fields` | ✅ `--fields` | v0.3.84 P1 |
| 地理距离 | `filter.geo` | ✅ `--geo`（裸格式自动包装 + 半径范围校验） | v0.3.85 P2 |
| 远程试验 | ~~`query.rmtln`~~ | ⚠️ **v1 遗留参数，v2 已移除**（真实 API 实测 HTTP 400，2026-08-13）——不提供；远程检索用 `--query`/`--adv` | — |
| 患者友好搜索 | `query.patient` | ✅ `--patient` | v0.3.85 P2 |
| 不影响排序的筛选 | `postFilter.*` | ✅ `--post-status/--post-ids/--post-geo/--post-adv` | v0.3.85 P2 |
| 资助类型（NIH/工业/其他） | `filter.advanced` → `AREA[LeadSponsorClass]...` | ⚠️ 需写 `--adv` 表达式（无独立参数，走原始通道） | 可选扩展 |

---

## 3. 缺口分级

### P0 — 主功能必需（✅ v0.3.84 已落地）
1. **`filter.advanced` 原始表达式透传**（`--adv`）：用户可直接粘贴网站 Expert Search 表达式，一劳永逸覆盖所有组合。 ✅
2. **便捷筛选参数**：`--phase`（映射 `AREA[Phase]`）、`--study-type`、`--age-group`、`--sex`、`--has-results`——内部组装进 `filter.advanced`（或直接作为独立 filter 拼接）。 ✅
3. **`sort`**（`--sort field[:asc|desc]`，支持 2 个、`@relevance`）。 ✅
4. **服务端日期区间**（`--first-post-*`/`--last-update-*`/`--start-date-*`/`--primary-completion-*`/`--completion-*` → `AREA[Field]RANGE[...]`），与旧本地 post-filter 并存（`--date-after` 保留）。 ✅
5. **状态多值**：`--status RECRUITING,COMPLETED` → 管道分隔。 ✅

### P1 — 常用补齐（✅ v0.3.84 已落地）
6. `--titles` / `--outc` / `--lead` / `--id` / `--locn`（各 `query.*` 透传）。 ✅
7. `--fields` 暴露（大结果集瘦身，省流量）。 ✅
8. `--ids`（按 NCT 号批量，竞品情报常用）。 ✅

### P2 — 可选（✅ v0.3.85 已落地）
9. `--geo`（`filter.geo`，裸格式自动包装 + 1-500 mi / 1-805 km 范围强制）、`--patient`（`query.patient`）、`--post-status/--post-ids/--post-geo/--post-adv`（`postFilter.*`）。 ✅
10. ~~`--rmtln`~~：**真实回归发现 v2 API 已移除 `query.rmtln`（HTTP 400，2026-08-13 实测）**——v1 遗留参数，未提供；远程试验检索用 `--query`/`--adv`。

---

## 4. 整改方案设计（落地建议）

在 `search_ctgov.py` 的 `_build_params()` 与 CLI 层做**纯参数透传**扩展，不改返回结构：

```python
# 建议新增 CLI（对齐官方参数名，降低心智负担）
--query TEXT        # query.term（支持 AREA[] 表达式）
--titles TEXT       # query.titles
--outc TEXT         # query.outc
--lead TEXT         # query.lead
--id TEXT           # query.id
--locn TEXT         # query.locn
--adv TEXT          # filter.advanced 原始表达式（可粘网站 Expert Search）
--phase PHASE       # 逗号分隔 -> AREA[Phase]PHASE3|... （或并入 --adv）
--study-type TYPE   # INTERVENTIONAL|OBSERVATIONAL|EXPANDED_ACCESS
--age-group AG      # CHILD|ADULT|OLDER_ADULT
--sex SEX           # FEMALE|MALE|ALL
--has-results       # AREA[HasResults]true
--sort FIELD[:asc|:desc]  # 可重复 2 次；@relevance 默认
--ids NCT1,NCT2     # filter.ids 管道分隔
--fields F1,F2      # 暴露已有 fields 参数
# --status 改为支持逗号多值 -> 管道分隔
```

组装规则（关键）：
- 多个 `--phase/--study-type/--age-group/--sex/--has-results` → 内部拼一个 `AND` 连接的 Essie 表达式放进 `filter.advanced`；若用户又给了 `--adv`，则合并（`(<便捷表达式>) AND (<--adv>)`）。
- `--sort` 可重复 2 次；`--sort @relevance` 显式默认。
- 日期区间统一走 `AREA[Field]RANGE[YYYY-MM-DD,MAX|MIN]`，`--date-after` 旧行为保留（向后兼容）。

**回归验收**（部署环境或本地可达网络时）：
- `--cond "non-small cell lung cancer" --phase PHASE3 --status RECRUITING,COMPLETED --sort LastUpdatePostDate:desc`
  → 结果应全为 Phase 3、状态 ∈ {RECRUITING, COMPLETED}、按更新时间降序。
- `--adv 'AREA[StudyType]INTERVENTIONAL AND AREA[StartDate]RANGE[2023-01-01,MAX]'` 应等价于网站对应高级检索。

### 4.1 实施记录（v0.3.84 P0+P1 / v0.3.85 P2，已全部落地）

`scripts/search_ctgov.py` 已按上述设计重写，新增：

| 类别 | 新增 CLI | 对应 API 参数 |
|---|---|---|
| query.* 补齐 | `--query` `--titles` `--outc` `--lead` `--id` `--locn` | `query.term/titles/outc/lead/id/locn` |
| query.* 补齐（P2） | `--patient` | `query.patient`（~~`--rmtln`~~ v1 遗留、v2 已移除，真实回归 400） |
| 原始表达式 | `--adv` | `filter.advanced`（与便捷子句 AND 合并，`(<便捷>) AND (<--adv>)`） |
| 便捷筛选 | `--phase` `--study-type` `--age-group` `--sex` `--has-results` | 组装为 `AREA[Phase](A OR B)` 等，多值用 `OR` |
| 多值状态 | `--status RECRUITING,COMPLETED` | `filter.overallStatus=RECRUITING\|COMPLETED`（管道） |
| NCT 批量 | `--ids NCT1,NCT2` | `filter.ids`（管道） |
| 地理距离（P2） | `--geo`（`distance(lat,lon,dist[km\|mi])` 或裸格式自动包装） | `filter.geo`，强制 1-500 mi / 1-805 km |
| 排序 | `--sort`（≤2 次，`field[:asc\|:desc]`/`@relevance`） | `sort=A\|B`（管道） |
| 字段裁剪 | `--fields` | `fields` |
| 服务端日期区间 | `--first-post-since/--until` `--last-update-*` `--start-date-*` `--primary-completion-*` `--completion-*` | `AREA[Field]RANGE[since,until]`（缺省 MIN/MAX） |
| postFilter（P2） | `--post-status` `--post-ids` `--post-geo` `--post-adv` | `postFilter.*`（语义同 filter.*，不影响相关性排序） |

- 枚举校验：phase（EARLY_PHASE1/PHASE1-4/NA）、study-type（INTERVENTIONAL/OBSERVATIONAL/EXPANDED_ACCESS）、age-group（CHILD/ADULT/OLDER_ADULT）、sex（FEMALE/MALE/ALL）非法值直接 argparse 报错；日期强制 YYYY-MM-DD 严格校验；`--sort` 超 2 个或格式非法报错；geo 格式 + 半径范围双重校验（`_normalize_geo` 幂等，`_build_params` 编程调用亦兜底）。
- 向后兼容：`--cond/--intr/--sponsor/--date-after` 行为不变；`--fast` 与默认路径共用 `_build_params()`，一处改全生效。
- 验证：py_compile ✓；离线参数组装断言（P0/P1/P2 全项 + 范围拦截 + 回归）全过 ✓；CLI PREVIEW URL 构造与非法参数拦截 ✓。
- **真实联网回归（2026-08-13，真实环境）**：
  - 基础 cond+status：total=1302 ✓；
  - P0 组合（`--phase PHASE3 --status RECRUITING,COMPLETED --sort LastUpdatePostDate:desc --start-date-since 2023-01-01`）：total=128，5/5 记录 phase=PHASE3、状态∈目标集、start≥2023、按更新时间降序 ✓（Phase 2/3 试验如 `['PHASE2','PHASE3']` 命中 PHASE3 属正常语义）；
  - P1：`--ids` 精确命中 2/2 ✓、`--titles` ✓、`--fields` 瘦身 ✓；
  - P2：`--geo`（上海 50km，total=414，命中含 Shanghai 地点）✓、`--patient`（total=14814）✓、postFilter（3/3 COMPLETED）✓、`--adv`（OBSERVATIONAL+China，3/3 命中）✓；
  - `--fast` 并发分页 ✓（返回 10/10）；
  - **发现并修正**：`query.rmtln` 为 v1 遗留参数，v2 API 返回 HTTP 400（与 `query.term` 对照确认）→ 已从 CLI 移除，文档注明替代方案（`--query`/`--adv`）。

---

## 5. 兼容性与风险

| 项 | 评估 |
|---|---|
| normalize 管线 | ✅ 不受影响（`norm_ctgov` 读响应 `protocolSection`，与查询参数无关） |
| 向后兼容 | ✅ 旧 CLI（`--cond/--intr/--sponsor/--status/--date-after`）全部保留，新增参数全为 opt-in |
| `--fast` 并发分页 | 需同步透传新参数（`search_fast()` 的 `_build_params` 调用点共用同一函数，改一处即可） |
| 配额/限流 | 服务端日期筛选可显著减少"拉回再裁剪"的数据量，省配额 |
| pageSize 上限 | 文档明确上限 1000，`--fast` 默认 500 合规 |

---

## 6. 附：权威信息源（2026-08-13 核实）

- OpenAPI 规范：`https://clinicaltrials.gov/api/oas/v2`（`/studies` 参数定义）
- Search Areas（19 区域字段权重）：`https://clinicaltrials.gov/data-api/about-api/search-areas`
- Expert Search 语法：`https://clinicaltrials.gov/find-studies/constructing-complex-search-queries`
- 注意：v2 **没有**独立的 `filter.phase`/`filter.studyType`/`filter.sex`/日期参数——这些在 v2 中全部通过 `filter.advanced` 的 `AREA[]` 表达式实现（与 v1 的 `filter.*` 扁平参数不同，这是常见误区）。
