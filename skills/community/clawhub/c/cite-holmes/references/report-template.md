# 报告模板与引用 schema（SYNTHESIZE 阶段照此输出）

> **30 秒入口**：何时读我——要写 research_refs.json 或组织最终报告时。最短路径：复制文末 JSON 骨架填字段；报告结构照 BLUF 头+表格+人工复核区三段即可。回 [INDEX.md](INDEX.md)。


## research_refs.json schema（VERIFY 阶段的输入）

研究过程中实时登记引用，每条：

```json
[
  {
    "id": 1,
    "title": "页面/文档标题",
    "url": "https://…",
    "source": "来源站点或机构（如 Anthropic / Nature / Reuters）",
    "year": 2026,
    "claim": "本报告用这条引用支撑的那句话",
    "triples": [{"subject": "...", "relation": "...", "object": "...", "span": "原文出处片段"}],  # L1 原子声明分解(v3.0.0)
    "semantic": {
      "claim": "与上层 claim 相同（或更细）",
      "support": "supported",   // supported | partial | not_in_source | contradicted | unclear
      "quote": "来源页原文关键句（人工复核抓手）",
      "note": "可选备注"
    },
    "found_via": "search#3",          // 哪轮搜索发现的，便于回溯
    "tier": "official"                // official | journal | preprint | media | community | blog | social
  }
]
```

`semantic` 字段由模型在语义验证时填写（v1.11 起推荐上面的结构化对象形式；旧的
字符串形式仍然接受，仅作注记不参与判定）。验证器把结构化判定带进
`--export auditjson` 的 `semantic_audit` 工作底稿与报告语义区；`not_in_source` /
`contradicted` 会把机械判定封顶为 `partial` 并转人工复核（来源存在 ≠ 来源认同）。
机械验证由 `scripts/verify_refs.py` 完成，两层的结果都要体现在最终引用表里。

## 置信度标记规范

| 标记 | 含义 | 判定标准 |
|---|---|---|
| 🟢 | 高置信 | ≥2 个独立来源一致，且至少一个是一手/权威源 |
| 🟡 | 中置信 | 单一权威源，或双源但均为二手 |
| 🔴 | 存疑 | 来源冲突、仅社区层证据、或数据过旧 |

标记挂在结论句末尾 + 引用编号，如：`缓存命中率提升约 40% 🟢[1][3]`。

## 报告骨架

```markdown
# {研究问题}

> 研究模式：FULL/QUICK · 检索 N 轮 · 引用 M 条（verified X / partial Y / …）
> 完成日期：YYYY-MM-DD · 覆盖时间窗：…

## 执行摘要（≤200 字，先给答案）
{直接回答研究问题的主要发现，2–4 条，每条带置信度标记}

## 主要发现
### 子问题 ①：{…}
{结论句 🟢[引用号]。证据展开：数字/事实 + 出处定位。}
{与结论相悖的证据如有，必须写。}

### 子问题 ②：{…}
…

## 分歧与存疑
{来源打架的地方：各自说法 + 各自来源 + 可能的成因（数据新旧/口径不同/立场差异）}

## 研究缺口
{预算内没能回答的问题、抓取失败的来源、需要付费/权限才能核实的数据}

## 后续值得追问
{2–3 个基于本次发现自然延伸的问题}

## 引用清单
| # | 标题 | 来源 | 年份 | 语义 | 机械验证 | 支撑论断 |
|---|---|---|---|---|---|---|
| 1 | … | … | … | supports | verified | … |

### 待人工复核（unverified / unreachable）
| # | 标题 | URL | 状态 | 原因 |
```

## 输出要求

- 正文结论**只能**引用 `semantic.support=supported`（旧字符串 `supports`）且机械验证非 `invalid` 的条目；`not_in_source`/`contradicted` 条目已由验证器封顶 `partial`，只可作对照线索。
- `partial_support` 只能支撑结论中它确实支持的那半句，并在句中注明。
- `unverified/unreachable` 一律只出现在"待人工复核"分区。
- QUICK 模式可省略"子问题"分节，直接：执行摘要 → 核查结论（含反证）→ 引用清单。
- 报告语言跟随用户提问语言；术语首次出现给中英对照。

## 收尾台账（finding ledger，REA 式纪律）

报告定稿前，回到研究计划的问题清单逐条标记：**answered / partially
answered / unresolved**——以证据为准，不以印象为准。预算台账（检索轮次/
调用次数）随报告附最后一行：用了多少、剩多少、未决问题清单。UNRESOLVED
不是失败——带着明确的未决清单收尾，好于用编造的完整感收尾。
