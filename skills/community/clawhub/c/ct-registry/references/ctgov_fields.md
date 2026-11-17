# CT.gov v2 字段与检索语法参考（离线手册）

> **用途**：本手册是 `ct-registry` 技能检索主功能（ClinicalTrials.gov v2 `/studies`）的离线参考。
> 当你要构造 `filter.advanced` 表达式、确认某个 `query.*` / `filter.*` 参数名、或核对枚举值时，直接查本文件，无需联网。
> **最后核实日期**：2026-08-13（对应 `search_ctgov.py` v0.3.85 落地态）。
> **权威来源**：
> - OpenAPI 规范 `https://clinicaltrials.gov/api/oas/v2`
> - 19 个 Search Areas `https://clinicaltrials.gov/data-api/about-api/search-areas`
> - Expert Search 语法 `https://clinicaltrials.gov/find-studies/constructing-complex-search-queries`
> - 字段/枚举定义 `https://clinicaltrials.gov/data-api/about-api/study-data-structure`
> - API 迁移指南（枚举映射）`https://clinicaltrials.gov/data-api/about-api/api-migration`

---

## 1. 端点与通用约定

```
GET https://clinicaltrials.gov/api/v2/studies
```

- **公开、无需认证、零保密数据输入**。
- **限流**：约 50 请求/分钟/IP（实测为软限流，超了会 429，稍后重试即可）。
- **通用参数**：

| 参数 | 规则 |
|---|---|
| `pageSize` | 默认 10，**上限 1000**（超出服务端强制降为 1000）。`--fast` 模式默认 500。 |
| `pageToken` | 分页游标，取响应 `nextPageToken` 循环。 |
| `countTotal` | `true` 时响应含 `totalCount`。 |
| `format` | `json`（默认）或 `csv`。 |
| `fields` | 逗号分隔字段名（如 `NCTId,BriefTitle`），大结果集瘦身省流量。 |

> ⚠️ **现代化数据管道（2025-08-26 生效）注意**：
> 1. 部分 markup 字段（富文本）格式与旧管线不完全一致。
> 2. 地理/地点数据改从另一数据库拉取。
> 3. **`COVERAGE` / `EXPANSION` 运算符在现代化 API 上未完全实现**——见 §5 警告。

---

## 2. `query.*` 词面检索参数（11 个）

`query.*` 做**加权词面检索**，影响相关性排序（`@relevance`）。每个参数对应网站检索表单的一个输入框，也对应下方 §4 的一个或多个 Search Area。

| API 参数 | CLI 参数 | 对应 Search Area | 字段数 | 说明 |
|---|---|---|---|---|
| `query.cond` | `--cond` | ConditionSearch | 7 | 疾病/条件框（Condition 权重 0.95） |
| `query.term` | `--query` | BasicSearch | 57 | 其他术语框（**支持 AREA[] 高级表达式**） |
| `query.intr` | `--intr` | InterventionSearch | 12 | 干预/治疗框（InterventionName 0.95） |
| `query.outc` | `--outc` | OutcomeSearch | 9 | 结局指标框 |
| `query.titles` | `--titles` | TitleSearch | 3 | 标题/缩写框（Acronym 1.0） |
| `query.spons` | `--sponsor` | SponsorSearch | 3 | 申办方/合作方框（LeadSponsorName 1.0） |
| `query.lead` | `--lead` | — | — | 仅 LeadSponsorName 字段 |
| `query.id` | `--id` | IdSearch | 5 | 研究 ID 框（NCT/OrgStudyId/SecondaryId 等） |
| `query.locn` | `--locn` | LocationSearch | 5 | 地点框（城市/州/国家/机构/邮编） |
| `query.patient` | `--patient` | PatientSearch | 47 | 患者友好搜索（通俗语言加权） |
| ~~`query.rmtln`~~ | — | — | — | ⚠️ **v1 遗留参数，v2 已移除**（真实 API 实测 HTTP 400）。远程/虚拟试验改用 `--query` 或 `--adv`。 |

> 全部支持 Essie 表达式语法（`OR` / `AND` / `NOT` / 括号 / 引号短语）。

---

## 3. `filter.*` 结构化筛选（5 个 + `postFilter` 同构）

`filter.*` 做**精确匹配筛选，不影响相关性排序**。v2 只有 5 个 `filter.*`——注意**没有**独立的 phase / studyType / sex / 日期参数，这些全部走 `filter.advanced`（见 §5）。

| API 参数 | CLI 参数 | 格式 / 枚举 | 说明 |
|---|---|---|---|
| `filter.overallStatus` | `--status` | 14 枚举，**逗号多值→管道分隔** | 状态筛选（枚举见 §6.1） |
| `filter.advanced` | `--adv` | Essie 表达式 | **高级组合的核心**：`AREA[Phase]PHASE3 AND AREA[StudyType]INTERVENTIONAL` |
| `filter.geo` | `--geo` | `distance(lat,lon,dist[km\|mi])` 或裸 `lat,lon,dist` | 地理距离（**1–500 mi / 1–805 km**） |
| `filter.ids` | `--ids` | 管道分隔 NCT 号 | 按 NCT 号批量取（竞品情报常用） |
| `filter.synonyms` | — | `area:synonym_id` 对 | 内部同义词，一般不直接用 |

> **`postFilter.*` 同构 5 个**（`postFilter.overallStatus` / `postFilter.ids` / `postFilter.geo` / `postFilter.advanced` / `postFilter.synonyms`）：语义与 `filter.*` 等价，但**不影响相关性排序**（排序敏感场景用）。CLI 对应 `--post-status` / `--post-ids` / `--post-geo` / `--post-adv`。

---

## 4. 19 个 Search Areas（权威清单）

Study 文档仅含 19 个 Search Area。下表列出每个 Area 的**请求参数**（若有）、**字段数**、**权重最高的核心字段**，便于理解"为什么某些词在某些框里搜得到/搜不到"。

| # | Search Area | 请求参数 | 字段数 | 核心字段（权重） |
|---|---|---|---|---|
| 1 | BasicSearch | `query.term` | 57 | Condition(0.81)、InterventionName(0.8)、BriefTitle(0.89)、BriefSummary(0.6) |
| 2 | ConditionSearch | `query.cond` | 7 | Condition(0.95)、BriefTitle(0.6)、ConditionMeshTerm(0.5) |
| 3 | InterventionSearch | `query.intr` | 12 | InterventionName(0.95)、InterventionType(0.85)、ArmGroupType(0.85) |
| 4 | InterventionNameSearch | — | 2 | InterventionName(1.0)、InterventionOtherName(0.9) |
| 5 | ObsoleteConditionSearch | — | 4 | Condition(0.95)、ConditionMeshTerm(0.8) |
| 6 | ExternalIdsSearch | — | 2 | OrgStudyId(0.9)、SecondaryId(0.7) |
| 7 | ExternalIdTypesSearch | — | 2 | OrgStudyIdType、SecondaryIdType |
| 8 | EligibilitySearch | — | 2 | EligibilityCriteria(0.95)、StudyPopulation(0.8) |
| 9 | OutcomeSearch | `query.outc` | 9 | PrimaryOutcomeMeasure(0.9)、SecondaryOutcomeMeasure(0.8) |
| 10 | OutcomeNameSearch | — | 4 | PrimaryOutcomeMeasure(0.98) |
| 11 | TitleSearch | `query.titles` | 3 | Acronym(1.0)、BriefTitle(0.95)、OfficialTitle(0.8) |
| 12 | LocationSearch | `query.locn` | 5 | LocationCity/State/Country/Facility(0.95)、LocationZip(0.35) |
| 13 | ContactSearch | — | 4 | OverallOfficialName(0.95)、CentralContactName(0.9) |
| 14 | NCTIdSearch | — | 2 | NCTId(1.0)、NCTIdAlias(0.9) |
| 15 | IdSearch | `query.id` | 5 | NCTId(1.0)、Acronym(0.85)、OrgStudyId(0.8) |
| 16 | SponsorSearch | `query.spons` | 3 | LeadSponsorName(1.0)、CollaboratorName(0.9)、OrgFullName(0.6) |
| 17 | FunderTypeSearch | — | 2 | LeadSponsorClass(1.0)、CollaboratorClass(0.9) |
| 18 | ResponsiblePartySearch | — | 5 | ResponsiblePartyInvestigatorFullName(0.9) 等 |
| 19 | PatientSearch | `query.patient` | 47 | Acronym(1.0)、Condition(0.95)、BriefTitle(0.9)、BriefSummary(0.65) |

> 带 `✓` 的字段会产生同义词（synonym）扩展。`query.term` 与 `query.patient` 覆盖最广（57 / 47 字段），是"兜底全文检索"首选。

---

## 5. Expert Search / `AREA[]` 表达式语法

`filter.advanced` 与 `query.term` 共用 Essie 表达式引擎。**任意 study structure 字段均可经 `AREA[字段名]` 检索**。

### 5.1 运算符

| 运算符 | 语法 | 说明 / 示例 |
|---|---|---|
| 字段定位 | `AREA[FieldName]value` | `AREA[InterventionName]aspirin`、`AREA[LocationCountry]United States` |
| 布尔 | `AND` / `OR` / `NOT` | 优先级：NOT > AND > OR |
| 分组 | `( )` | `(acetaminophen OR aspirin) AND NOT (heart failure)` |
| 短语 | `" "` | `"back pain"`（词序固定） |
| 范围 | `AREA[Field]RANGE[min,max]` | `AREA[StartDate]RANGE[2023-01-01,MAX]`；边界 `MIN`/`MAX`；**不含无值记录** |
| 缺失 | `AREA[Field]MISSING` | `AREA[ResultsFirstPostDate]MISSING` |
| 全部 | `ALL` | 取全部记录 |
| 距离 | `AREA[LocationGeoPoint] DISTANCE[lat,lon,r]` | `≥1 mi/km`、`≤500 mi / 805 km` |
| 倾斜 | `TILT[field]"phrase"` | `TILT[StudyFirstPostDate]"heart attack"`（按日期倾斜相关性） |
| 匹配控制 | `COVERAGE[FullMatch\|StartsWith\|EndsWith\|Contains]` | 默认 `Contains`；`FullMatch/StartsWith/EndsWith` 仅能与 `EXPANSION[Concept\|Term\|None]` 合用 |
| 扩展控制 | `EXPANSION[None\|Term\|Concept\|Relaxation\|Lossy]` | 默认 `Relaxation`；`Lossy` 不可与 `COVERAGE` 合用 |

### 5.2 ⚠️ 现代化 API 兼容性警告

> 官方 API 主页明确：**`COVERAGE` 与 `EXPANSION` 运算符在现代化 ClinicalTrials.gov（2025-08-26 起）上未完全实现**。
> 因此本技能便捷参数（`--phase`/`--study-type`/`--age-group`/`--sex`/`--has-results`/`--*-since`/`--*-until`）**只组装 `AREA[Field]value` 与 `AREA[Field]RANGE[...]`**，不依赖 `COVERAGE/EXPANSION`。若要精确全匹配（`COVERAGE[FullMatch]`），请先用 `--query`/`--adv` 实测验证可用性，不要假设其生效。

### 5.3 常用 `AREA[]` 字段名

Phase、StudyType、StdAge、Sex、HasResults、StartDate、CompletionDate、PrimaryCompletionDate、ResultsFirstPostDate、StudyFirstPostDate、LastUpdatePostDate、EnrollmentCount、LeadSponsorName、LeadSponsorClass、CollaboratorName、ConditionName、InterventionName、InterventionType、LocationCity、LocationState、LocationCountry、LocationStatus、LocationGeoPoint、OverallStatus 等——均可用（枚举见 §6）。

---

## 6. 常用枚举值参考

### 6.1 OverallStatus（14 个，`filter.overallStatus` / `AREA[OverallStatus]`）

```
NOT_YET_RECRUITING    # 尚未招募
RECRUITING            # 招募中
ENROLLING_BY_INVITATION  # 仅邀约入组
ACTIVE_NOT_RECRUITING # 进行中、不再招募
SUSPENDED            # 暂停
TERMINATED           # 提前终止
COMPLETED            # 已完成
WITHDRAWN            # 入组前撤销
AVAILABLE            # 可获取（扩展使用等）
NO_LONGER_AVAILABLE  # 不再可获取
TEMPORARILY_NOT_AVAILABLE  # 暂不可获取
APPROVED_FOR_MARKETING     # 已批准上市
WITHHELD             # 撤回（数据保留但不公开）
UNKNOWN              # 未知
```

> `--status` 便捷参数**不做白名单校验**（14 值较长，交由 API 报错），可放心传上述任一值，逗号多值→管道。

### 6.2 Phase（`AREA[Phase]`，6 个）

```
NA            # Not Applicable（不适用）
EARLY_PHASE1  # 早期 Phase 1（原 Phase 0）
PHASE1 PHASE2 PHASE3 PHASE4
```

> `--phase` 便捷参数白名单 = 上述 6 个（与官方一致）。多值用 `OR` 连接。

### 6.3 StudyType（`AREA[StudyType]`，3 个）

```
INTERVENTIONAL  OBSERVATIONAL  EXPANDED_ACCESS
```

### 6.4 StdAge（`AREA[StdAge]`，3 个）

```
CHILD       # 出生–17 岁
ADULT       # 18–64 岁
OLDER_ADULT # 65 岁及以上
```

### 6.5 Sex（`AREA[Sex]`，3 个）

```
FEMALE  MALE  ALL
```

### 6.6 AgencyClass（`AREA[LeadSponsorClass]`，常用 7 个，以官方 enum AgencyClass 为准）

```
NIH  FED  OTHER_GOV  INDUSTRY  INDIV  UNKNOWN  NA
```

> 无便捷 CLI 参数，需用 `--adv 'AREA[LeadSponsorClass]INDUSTRY'` 表达"工业界资助"。

### 6.7 HasResults（布尔）

```
AREA[HasResults]true   # 仅已有结果；CLI 用 --has-results
```

### 6.8 sort 可排序字段（常用）

`LastUpdatePostDate`、`EnrollmentCount`、`StartDate`、`StudyFirstPostDate`、`NumericChange`；格式 `FieldName:asc` / `FieldName:desc`；特殊值 `@relevance`（默认）。**最多 2 个**。

---

## 7. CLI ↔ API 参数映射表（`search_ctgov.py` v0.3.85）

| CLI 参数 | 对应 API 参数 | 备注 |
|---|---|---|
| `--cond` | `query.cond` | 疾病/条件 |
| `--intr` | `query.intr` | 干预/治疗 |
| `--sponsor` | `query.spons` | 申办方/合作方 |
| `--query` | `query.term` | 支持 AREA[] |
| `--titles` | `query.titles` | 标题/缩写 |
| `--outc` | `query.outc` | 结局指标 |
| `--lead` | `query.lead` | 主要申办方 |
| `--id` | `query.id` | 研究 ID |
| `--locn` | `query.locn` | 地点 |
| `--patient` | `query.patient` | 患者友好 |
| `--status` | `filter.overallStatus` | 逗号多值→管道；14 枚举 |
| `--ids` | `filter.ids` | NCT 批量；管道 |
| `--geo` | `filter.geo` | distance()；1–500mi/1–805km |
| `--adv` | `filter.advanced` | 原始 Essie 表达式 |
| `--phase` | `AREA[Phase]`（并入 filter.advanced） | 多值 OR；6 枚举 |
| `--study-type` | `AREA[StudyType]` | 3 枚举 |
| `--age-group` | `AREA[StdAge]` | 3 枚举 |
| `--sex` | `AREA[Sex]` | 3 枚举 |
| `--has-results` | `AREA[HasResults]true` | 开关 |
| `--first-post-since/--until` | `AREA[StudyFirstPostDate]RANGE[...]` | 服务端日期区间 |
| `--last-update-since/--until` | `AREA[LastUpdatePostDate]RANGE[...]` | 服务端日期区间 |
| `--start-date-since/--until` | `AREA[StartDate]RANGE[...]` | 服务端日期区间 |
| `--primary-completion-since/--until` | `AREA[PrimaryCompletionDate]RANGE[...]` | 服务端日期区间 |
| `--completion-since/--until` | `AREA[CompletionDate]RANGE[...]` | 服务端日期区间 |
| `--post-status/--post-ids/--post-geo/--post-adv` | `postFilter.*` | 同 filter.*，不影响排序 |
| `--sort` | `sort` | ≤2 个；`field[:asc\|:desc]`/`@relevance` |
| `--fields` | `fields` | 字段裁剪 |
| `--date-after` | （本地后过滤） | 旧行为保留，按 start-date 下限本地裁剪 |
| `--max` | `pageSize` | 默认 50；`--fast` 默认 500 |
| `--fast` | — | 快速路径：Session 连接池 + 并发分页（有 key/已知配额时用） |

> 便捷参数（`--phase/--study-type/--age-group/--sex/--has-results`/日期区间）内部拼为 `AND` 连接的 Essie 表达式放入 `filter.advanced`；若同时给 `--adv`，则合并为 `(<便捷>) AND (<--adv>)`。

---

## 8. 实用示例库

```bash
# 1) 疾病 + Phase 3 + 状态多选 + 按更新时间降序
python search_ctgov.py --cond "non-small cell lung cancer" --phase PHASE3 \
  --status RECRUITING,COMPLETED --sort LastUpdatePostDate:desc --run

# 2) 观察性研究 + 中国（AREA[] 组合）
python search_ctgov.py --adv 'AREA[StudyType]OBSERVATIONAL AND AREA[LocationCountry]China' --run

# 3) 2023 年起启动、已完成、入组≥100
python search_ctgov.py --cond diabetes --start-date-since 2023-01-01 \
  --status COMPLETED --adv 'AREA[EnrollmentCount]RANGE[100,MAX]' --run

# 4) 地理距离（上海 50km，裸格式自动包装）
python search_ctgov.py --cond cancer --geo "31.23,121.47,50km" --run

# 5) 某申办方 + 已有结果
python search_ctgov.py --sponsor "National Cancer Institute" --has-results --run

# 6) 患者友好搜索（通俗语言）
python search_ctgov.py --patient "chemo for breast cancer" --run

# 7) 专家表达式：儿科 + 干预性 + 招募中（等效网站高级检索）
python search_ctgov.py --adv 'AREA[StdAge]CHILD AND AREA[StudyType]INTERVENTIONAL AND AREA[OverallStatus]RECRUITING' --run

# 8) 按 NCT 号批量取（竞品情报）
python search_ctgov.py --ids NCT04852770,NCT04527068 --run

# 9) 字段裁剪省流量（只要 id + 标题 + 状态）
python search_ctgov.py --cond asthma --fields NCTId,BriefTitle,OverallStatus --max 200 --run

# 10) 远程/虚拟试验替代方案（rmtln 已移除，用 term 表达）
python search_ctgov.py --query "remote OR virtual OR decentralized" --run

# 11) 工业界资助的 Phase 2/3（AgencyClass 走 --adv）
python search_ctgov.py --cond melanoma --adv 'AREA[LeadSponsorClass]INDUSTRY AND (AREA[Phase]PHASE2 OR AREA[Phase]PHASE3)' --run

# 12) 不影响相关性排序的二次筛选（postFilter）
python search_ctgov.py --cond "heart failure" --post-status COMPLETED --run
```

> 不加 `--run` 时脚本只打印 `PREVIEW` 请求 URL（不联网），便于先核对参数。

---

## 9. 常见陷阱（写检索表达式前先看）

1. **v2 无独立 `filter.phase` / `filter.studyType` / `filter.sex` / 日期参数**——这些在 v2 全部通过 `filter.advanced` 的 `AREA[]` 实现（与 v1 扁平 `filter.*` 不同，常见误区）。
2. **`query.rmtln` 已移除**（v1 遗留，v2 返回 HTTP 400）——远程试验改用 `--query`/`--adv`。
3. **`COVERAGE` / `EXPANSION` 现代化 API 未完全实现**——本技能便捷参数不依赖它们；精确匹配请先实测。
4. **`geo` 半径限制**：1–500 mi / 1–805 km，超出报错（`_normalize_geo` 强制校验）。
5. **`sort` 最多 2 个**；格式非法或超量直接 argparse 报错。
6. **`pageSize` 最多 1000**；`--fast` 默认 500 合规。
7. **`RANGE[...]` 不含无值记录**——做过日期区间后，无日期的试验会被排除（与本地 `--date-after` 后过滤的"无日期者保留"语义不同，注意区分）。
8. **`--status` 无白名单**，但 `--phase/--study-type/--age-group/--sex` 有白名单，非法值立即报错。
9. **`filter.*` 不影响 `@relevance` 排序**；若既要筛选又要按相关性排，用 `filter.*`；若仅要硬筛选且不关心排序，可用 `postFilter.*`。

---

## 10. 权威信息源（核对用）

- OpenAPI 规范：`https://clinicaltrials.gov/api/oas/v2`
- 19 Search Areas：`https://clinicaltrials.gov/data-api/about-api/search-areas`
- Expert Search 语法：`https://clinicaltrials.gov/find-studies/constructing-complex-search-queries`
- 字段/枚举定义：`https://clinicaltrials.gov/data-api/about-api/study-data-structure`
- API 迁移指南（枚举映射）：`https://clinicaltrials.gov/data-api/about-api/api-migration`
- 关于 API / 现代化改造：`https://clinicaltrials.gov/data-api/about-api`
