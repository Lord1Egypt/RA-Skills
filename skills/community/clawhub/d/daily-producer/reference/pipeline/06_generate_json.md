# 06 AI 生成日报 JSON

## 无脚本，由 AI 执行

这一步没有自动化脚本，由 AI 读取 candidates.json + profile.yaml，生成最终日报 JSON。

## 输入

- `output/raw/{date}_candidates.json` — 由 prepare_payload.py 生成的结构化候选
- `config/profile.yaml` — 用户画像（role、role_context、topics）
- `reference/daily_payload_example.json` — JSON 结构示例

## 输出

- `output/daily/{date}.json` — 符合渲染器契约的日报 JSON

## AI 需要做的事

### 1. 先读取目标条数，再做事件聚类

**第一件事：读取 `config/profile.yaml` 中 `daily.target_items` 的值（如 20），这是本次必须达到的目标条数。**
候选池通常有 40-80 条，数量足够，必须填满 target_items。

**禁止直接把单条 candidate 改写成 article。**

在写最终 JSON 前，必须先对 `candidates.json` 做**事件级聚类**：
- 将同一事件、同一发布、同一产品更新、同一融资/合作、同一模型发布的多条候选合并为一个事件簇
- 同一事件允许来自不同平台、不同媒体、不同语言的候选共同组成一个 article
- 只有在确认没有第二来源时，才允许单条候选独立成稿

**聚类判断信号：**
- 标题或正文中出现相同主体（公司 / 产品 / 模型 / 项目名）
- 标题或正文中出现相同动作（发布 / 融资 / 接入 / 开源 / 预览 / 上线 / 合作）
- 时间接近，且描述的是同一件事
- 一个是官方源，其他是媒体转述 / 社区讨论 / 视频解读

**选择标准：**
- 跳过明显噪音（如 "Agent" 指经纪人/执法人员的非 AI 内容）
- 同一事件在多平台出现 → 必须先合并，再写成一条 article
- 优先选择：官方发布 > 高热度社区讨论 > 媒体深度报道 > 背景信息
- 确保 topics 覆盖（不要全是同一个话题）
- 优先选择可形成多源交叉验证的事件簇，避免大量单源条目

**优先级分配（按 target_items 等比调整）：**
- `major`（约 15%，target=20 时约 3 条）：本周最重要的事件，产品/模型/平台级变化
- `notable`（约 25%，target=20 时约 5 条）：值得关注但影响范围较小
- `normal`（约 45%，target=20 时约 9 条）：有价值的信息
- `minor`（约 15%，target=20 时约 3 条）：背景信息或趋势信号

各档位合计必须等于 target_items，允许 ±1 条误差，**不允许差距超过 2 条**。

**多源硬规则：**
- `major`：必须至少 2 个来源，优先 3 个及以上
- `notable`：优先 2 个来源；若只有 1 个来源，必须确认 candidates 中确无第二来源可用
- `normal` / `minor`：允许单源，但若存在明显重复或转述来源，仍应合并
- 严禁明明存在可合并来源，却只保留 1 个 source 直接成稿

### 2. 为每条写 summary

```json
"summary": {
  "what_happened": "发生了什么（事实描述，不加观点）",
  "why_it_matters": "为什么重要（对行业/用户的影响）"
}
```

### 3. 为每条写 relevance

一句话说明与用户画像（role + role_context）的关系。

### 4. 生成 left_sidebar

- **overview**（3 条）：今日最重要的 3 个信号，每条含 title + text
- **actions**（3-4 条）：行动建议，每条含 type（learn/try/watch/alert）、text、prompt
- **trends**：rising/cooling/steady 各 3-4 个词，insight 一句话总结

### 5. 填写 credibility

```json
"credibility": {
  "confidence": "high/medium/low",
  "source_tier": "tier-1/tier-2",
  "cross_refs": 3,
  "evidence": "来源说明",
  "sources": [{"name": "xxx", "url": "xxx"}]
}
```

**写法要求：**
- `sources` 必须列出该 article 实际使用到的全部来源，而不是只放主链接
- `cross_refs` 必须严格等于 `sources` 数组长度
- 主 `url` 也应出现在 `sources` 中
- 若一个事件同时有官方、媒体、社区来源，应优先保留“官方 + 媒体”，社区来源作为补充
- 若只有 1 个来源，`evidence` 里应明确说明这是单源确认，而不是遗漏合并

**置信度建议：**
- 多源交叉验证，且含官方或主流媒体 → `high`
- 单源但来源可信 → `medium`
- 泄露、传闻、未确认、纯社区讨论 → `low`

## JSON 结构

必须严格遵循 `reference/daily_payload_example.json` 的结构。核心字段：

```json
{
  "meta": {"date": "", "date_label": "", "role": ""},
  "tools": [...],
  "left_sidebar": {
    "overview": [{"title": "", "text": ""}],
    "actions": [{"type": "", "text": "", "prompt": ""}],
    "trends": {"rising": [], "cooling": [], "steady": [], "insight": ""}
  },
  "articles": [{
    "id": "", "title": "", "priority": "", "time_label": "",
    "source_date": "", "source": "", "url": "",
    "summary": {"what_happened": "", "why_it_matters": ""},
    "relevance": "", "tags": [],
    "credibility": {"confidence": "", "source_tier": "", "cross_refs": 0}
  }],
  "data_sources": []
}
```

## 强制规则

1. **禁止跳过聚类**：在生成 article 前，必须先判断 candidates 中是否存在同事件多源；若存在，必须合并后再成稿
2. **禁止使用假 URL**：所有 `url` 和 `credibility.sources[*].url` 必须从 candidates.json 中的真实 URL 复制，不得编造（如 `https://weibo.com/example/xxx`）
3. **多源合并时保留所有原始 URL**：同一事件在多平台出现时，主 `url` 用最重要来源的 URL，其余放入 `credibility.sources` 数组
4. **cross_refs 必须有依据**：`cross_refs` 数值必须等于 `credibility.sources` 数组的长度，不能写一个数字但没列出来源
5. **主 URL 也必须计入 sources**：`credibility.sources` 不是“补充来源列表”，而是该 article 的完整来源列表，必须包含主 `url`
6. **没有 URL 就不写**：如果 candidates.json 中某条没有 url，对应 article 的 url 字段写空字符串，不要编造
7. **单源条目必须是明确例外**：若 `major` 只有 1 个来源，视为不合格；若 `notable` 只有 1 个来源，必须确认 candidates 中不存在第二来源，并在 `evidence` 说明
8. **禁止用重复 candidate 伪造多源**：相同 URL、相同文章的重复抓取只能算 1 个来源，不能把重复条目计为多个 cross_refs
9. **必须达到 target_items 条数**：不允许以"质量不够"为由大幅缩减数量。若单源条目较多，`normal`/`minor` 级别允许单源；确实凑不满时，可适当放宽聚类标准纳入边缘相关条目，但仍须在 target_items ±1 范围内

## 生成后

在运行 `validate_payload.py` 之前，先做一次自检：
- **`len(articles)` 是否等于 `profile.yaml` 中的 `target_items`（允许 ±1）**
- 每条 `article` 是否都检查过 candidates 中是否存在同事件多源
- 每条 `credibility.cross_refs` 是否等于 `len(credibility.sources)`
- `major` 是否都满足至少 2 个来源
- 是否有”明明 candidates 里有第二来源，但 JSON 里只写了 1 条”的情况

**必须运行 validate_payload.py 校验**，通过后才能渲染 HTML。
