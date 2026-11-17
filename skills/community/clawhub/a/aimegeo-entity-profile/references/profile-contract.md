# 实体档案合同 1.0

这是本技能自带的完整格式，不依赖宿主记忆目录、插件根路径或其他技能。可从[完整 JSON 样例](../examples/qinghe/品牌实体档案.json)开始，由 Agent 填入实际资料；不要将演示事实带入用户档案。

## 顶层字段

| 字段 | 格式与含义 |
| --- | --- |
| `schema_version` | 固定 `1.0`，字符串 |
| `data_mode` | `real` 为实际资料，`illustrative` 为演示/回归数据；示例不可作为线上证据 |
| `profile_id` | 非空稳定档案 ID，不依赖名称的唯一性 |
| `as_of` | `YYYY-MM-DD`，本次整理截止日期 |
| `primary_entity_id` | 本次主要交付的主体 ID，须在 entities 中存在 |
| `sources` | 来源数组，ID 唯一，可为空；无来源时仅允许未知字段 |
| `entities` | 至少一项，主体 ID 唯一 |
| `relationships` | 不同主体间有证据的关系，可为空 |
| `disambiguation` | 同名候选与区别记录，可为空 |
| `observations` | 已有 AI 回答或拟复测问题，可为空 |

## 来源与事实

来源包含 `id`、`kind`（`official_site/user_material/third_party/ai_response`）、`locator`、`acquisition`（`retrieved/user_supplied`）、`captured_on`、`subject_entity_ids`、`excerpt`。`locator` 是公开 HTTP(S) URL 或 `provided:` 开头的资料标识。所有日期用真实取得日期；用户转交网页摘录仍写 `user_supplied`，不能声称亲自访问。来源主题必须包括被引用主体；同一段同时描述公司和产品时可以包含两个 ID。

每项事实均为对象：

```json
{
  "status": "supported",
  "value": "Qinghe Tools",
  "evidence": [{"source_id": "S1", "quote": "青禾工具（Qinghe Tools）"}]
}
```

精确引文必须出现在来源 `excerpt` 中。脚本验证引文、引用完整性及数据约束；它不证明网页真实存在，也不判断引文是否足以支持结论。Agent 要核对主体、时间、否定句和原文含义，避免用一段无关真引文支持假事实。

| status | value 与证据要求 | 下游使用 |
| --- | --- | --- |
| `supported` | 非空值，至少一条证据；原文直接支持 | 可用于介绍；Schema 仅转换支持的字段 |
| `reported` | 非空值，至少一条用户资料证据 | 介绍注明“据用户提供资料”；Schema 不转换 |
| `unknown` | `null`、空 evidence、非空 reason | 明确未知，不能改为日期、零或否定结论 |
| `conflicting` | `null`、空 evidence、非空 reason；至少两条 alternatives | 不选胜者，列出待核实项 |

冲突的 `alternatives` 每项有非空 `value` 和独立 `evidence`，不同值不能丢失。例如两个来源分别给出 2020 和 2021，`founding_date.value` 仍为 null。若后续解决冲突，再更新状态和依据，不删来源记录。

## 主体字段

`id` 为稳定本地 ID。`type` 支持 `Organization`、`Brand`、`Product`、`SoftwareApplication`。`facts` 必须含以下七项，缺资料写 unknown：

| 字段 | 非未知时的值类型 | 关键边界 |
| --- | --- | --- |
| `canonical_name` | 非空字符串 | 规范展示名；未能确认时可 reported，不冒充法定名称 |
| `name_zh` | 非空字符串 | 中文名，不能把公司名当产品中文别名 |
| `name_en` | 非空字符串 | 英文名；没有官方英文名不自行音译为事实 |
| `aliases` | 字符串数组 | 简称、旧称、其他已证明为同一主体的名称；不放相关公司或产品名 |
| `description` | 非空字符串 | 有依据的中性定义，营销口号不直接当机器事实 |
| `website` | HTTP(S) URL | 主体的规范官网或产品页，用户提供未核实可 reported |
| `founding_date` | `YYYY`、`YYYY-MM` 或 `YYYY-MM-DD` | 仅 Organization 使用；产品发布日期另放 attributes，不反推公司成立时间 |

可选 `attributes` 是以业务字段名为键、以上述事实对象为值的对象，例如 `release_date`、`founder`、`registration_id`、`topics`。属性名有实际含义，值必须是 JSON 标量、数组或对象且带证据；脚本校验事实结构但不将这些扩展项自动投放为 Schema 属性。

`same_as` 为数组，每项有 `url`、`entity_id`、`status: supported`、`evidence`。只能记录同一主体的公开身份页。公司和产品有关系时写 relationships；关联方官网、普通新闻、搜索结果页不能当 sameAs。相同别名只提示候选，不自动合并。脚本阻止已知另一主体官网和消歧候选进入 sameAs，但外部未知页面的身份仍需 Agent 人工判断。

## 关系与消歧

关系包含 `subject_id`、`predicate`、`object_id`、`status`、`evidence`，证据必须同时覆盖两个主体。支持：

| predicate | 方向 | Schema 转换 |
| --- | --- | --- |
| `developed_by` | SoftwareApplication → Organization | 软件的 creator 指向公司 @id |
| `manufactured_by` | Product → Organization | 产品的 manufacturer 指向公司 @id |
| `brand_of` | Brand → Organization | 公司 brand 指向品牌 @id |
| `parent_organization` | 子公司 Organization → 母公司 Organization | 子公司的 parentOrganization |

仅 `supported/reported` 关系进入本数组，未决关系只记入消歧清单，不强行断言；仅 supported 转换 Schema。禁止自指关系和把关系伪装为别名。名称重名可真实存在，不能以此改名；遇到跨类型同名时保留原名并由 Agent 检查，脚本不按名称去重或推断身份相等。

`disambiguation` 每项包含 `entity_id`、`candidate_name`、`candidate_url`、`resolution`（`distinct/unresolved`）、`reason` 和 `evidence`。确定不同与尚不能确定都不加入 sameAs；候选网址也不成为本实体官网。候选使用非主页网址时，Agent 应核对是否同一机构的其他页面。

## 回答观察

仅在用户要求时记录实际取得或模拟的回答，并完整说明采集边界。`observations` 每项字段：`id`、`entity_id`、`platform`、`query`、`status`、`observed_on`、`source_id`、`answer`、`mentioned`、`citation_capture`、`native_citations`、`error`。native_citations 为去重的 URL 数组或 null。状态规则如下：

`ai_response` 来源另需保存 `platform`、`query`、`citation_capture`、`native_citations` 四项采集元数据。observed 记录的平台、问题及引用必须与来源一致。原文普通超链接不自动进入 native_citations；只有平台原生引用区已实际读取并完整记录后，才使用 complete。

| status | 允许的数据 |
| --- | --- |
| `observed` | 日期、真实回答、ai_response 来源及 mentioned 布尔值必填；answer 必须出现在来源摘录；来源获取日期应相同。`citation_capture: complete` 时引用为数组，包括确实零引用的 `[]`；未采集时 `not_captured + null`。error 为 null |
| `not_run` | 日期、来源、回答、mentioned、引用、error 均 null；citation_capture 为 not_captured |
| `query_failed` | 同 not_run，但 error 必填；失败不能产生零引用或零提及 |
| `simulated` | 可留演示回答，error/date/source_id/mentioned/引用均 null；citation_capture 为 not_captured，不计入真实分母 |

汇总只针对 status=observed；分母为实际回答数。只有已完整读取的原生引用才计数，汇总同时报告 `citation_complete_samples`、`citation_uncaptured_samples`。引用采集一个样本都没有时，计数是 null。`data_mode: illustrative` 的汇总永远不能用作真实监测结果。记录 AI 回答不等于证明 AI 说法属实，不把回答当作品牌创始日期等第一手来源。

## CLI 与退出状态

`python3 scripts/entity_profile.py {validate,schema,summarize} 档案.json`，无隐含网络操作、密钥、输出文件或外部目录依赖。成功输出 UTF-8 JSON，退出 0；业务或输入错误输出 `ok: false, errors: [...]`，退出 2。错误 code 为稳定标识，path 定位 JSON 字段。使用 shell 重定向前先 validate；schema 失败时不会包含 `@graph`。

Schema 输出为 `{"@context":"https://schema.org","@graph":[...]}`。每个节点的 @id 使用官网 URL 加 `#entity-本地ID`；已有 URL 片段先去掉再加稳定片段，部署时核对站点已有 @id。仅官网和规范名都 supported 的主体进入图；主要主体不满足则拒绝转换。属性包括名称、别名、描述、官网、成立日期、sameAs 及上述关系，不输出 null、内部证据或监测字段。这是转换草稿，不是搜索富媒体资格认证。
