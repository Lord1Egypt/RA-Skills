---
name: evidence-cleaner
description: LLM通用证据清洗技能。将原始搜索结果、网页片段、OCR残片等原始材料清洗为可用证据，减少脏输入、伪实体、重复片段和错域材料对后续判断的污染。在搜索结果返回后、进入freshness判定或叙事生成前使用。触发条件：搜索结果质量差、证据量大但信噪比低、需要标准化证据格式。
---

# Evidence Cleaner — 证据清洗技能

## 核心职责

将原始材料（搜索结果、网页片段、OCR残片、RSS条目等）清洗为标准化可用证据。

**做什么：**
- 剥离 DOM/HTML/JS 噪声残留
- 检测并过滤伪实体（不存在的人物、机构、事件）
- 去重与压缩重复片段
- 降权错域来源（二手转载、匿名来源等）
- 将 snippet 标准化为统一格式

**不做什么：**
- ❌ 不生成主叙事或最终结论
- ❌ 不做搜索或补充信息
- ❌ 不做时间新鲜度判定（交给 freshness-judge）
- ❌ 不改写证据的语义内容（只做格式标准化）

## 最小输入

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `raw_evidence_items[]` | array | ✅ | 原始证据条目，每条含 `source_url`、`title`、`snippet`、`raw_text`（可选） |
| `primary_subject` | string | ✅ | 本次任务的主体对象（用于判断相关性） |
| `canonical_time_frame` | object | ❌ | `{start, end, granularity}` 时间框架，供下游 freshness-judge 使用 |
| `cleaning_goal` | string | ✅ | 清洗目标，如 "为新闻分析准备证据" / "为技术调研去噪" |

## 输出格式

```json
{
  "cleaned_evidence": [
    {
      "id": "ev_001",
      "source_url": "https://...",
      "title": "...",
      "cleaned_snippet": "标准化后的文本",
      "source_reliability": "A",
      "cleaning_actions": ["dom_stripped", "truncated_restored"],
      "original_index": 0
    }
  ],
  "removed_noise": [
    {
      "id": "noise_001",
      "original_snippet": "被移除的内容摘要",
      "removal_reason": "pure_advertisement",
      "noise_category": "ad"
    }
  ],
  "downranked_items": [
    {
      "id": "ev_002",
      "original_rank": 1,
      "new_rank": 15,
      "downrank_reason": "secondary_repost",
      "warning": "内容可能被篡改，建议交叉验证"
    }
  ],
  "warnings": [
    "3条证据包含疑似AI幻觉引用",
    "2条证据来源为匿名账号，建议谨慎使用"
  ],
  "cleaning_stats": {
    "total_input": 25,
    "kept": 18,
    "removed": 4,
    "downranked": 3,
    "snr_ratio": 0.72
  }
}
```

## 清洗 5 步流程

### Step 1: DOM 噪声剥离
从网页抓取结果中移除非内容噪声。
- 识别并剥离：HTML 标签残留、CSS 样式文本、JS 代码片段、Cookie 提示条文本
- 识别并剥离：导航栏、页脚、面包屑、侧边栏、"相关推荐"、广告文案
- 识别并剥离：阅读量/点赞数/评论数等元数据噪声
- **检测方法**：正则匹配 HTML 标签名/CSS 属性；特征词检测（"推荐阅读""为您推荐""猜你喜欢"）
- **参考**：[references/noise-patterns.md](references/noise-patterns.md)

### Step 2: 伪实体检测
检测证据中引用的人物、机构、事件是否真实存在。
- 检查人名/机构名是否为已知实体（对比上下文一致性）
- 检查事件引用是否有时间/地点等可验证锚点
- 标记 AI 幻觉产生的虚假引用（如引用不存在的论文/报告）
- 标记相似名称混淆（如 "中国银行" vs "中国人民银行"）
- **检测方法**：上下文交叉验证；已知实体库比对；逻辑一致性检查
- **参考**：[references/noise-patterns.md](references/noise-patterns.md) 伪实体模式章节

### Step 2.5: 同源矛盾检测

当多条证据来自同一机构/作者/数据源，且结论相互矛盾时，标记为同源矛盾。

**检测规则**：
- 同一机构（如MIT）在不同时间发布的两篇研究结论方向相反
- 同一数据源（如Gartner报告）在不同版本中数据点不一致
- 同一作者/团队在不同媒体上发表的观点矛盾

**处理方式**：
- 不丢弃任何一方（双方证据均保留）
- 在两条证据上均添加 `same_source_contradiction` 标记
- 在 `warnings[]` 中记录矛盾描述和来源
- 在 `cleaning_stats` 中新增 `same_source_contradictions` 计数

**输出示例**：
```json
{
  "cleaned_evidence": [
    {
      "id": "ev_003",
      "flags": ["same_source_contradiction"],
      "contradiction_note": "与ev_007同源(MIT)，结论方向相反"
    }
  ],
  "warnings": [
    "同源矛盾: MIT的两项研究(ev_003 vs ev_007)结论方向相反，建议交叉验证"
  ],
  "cleaning_stats": {
    "same_source_contradictions": 1
  }
}
```

### Step 3: 去重压缩
识别并合并重复或高度相似的证据条目。
- 精确去重：标题和 snippet 完全相同的条目
- 近似去重：snippet 文本相似度 > 85% 的条目（保留信息量最大的版本）
- 压缩合并：同一事件的多条报道，合并为一条并标注来源数量
- 转载链识别：A→B→C 转载链，只保留最早一手来源
- **输出**：去重后保留最佳版本，其他记入 `removed_noise` 并标注 `removal_reason: "duplicate"`

### Step 4: 错域降权
对来源不权威或与主题不完全匹配的证据进行降权。
- 二手转载（非原始来源）：降权 1 级
- 匿名来源 / 自媒体无认证：降权 2 级
- 缺乏时间标注：降权 1 级
- 与 `primary_subject` 相关度 < 60%：降权 2 级
- 来源域名信誉度低（农场号/聚合号）：降权 3 级或移除
- **参考**：[references/clean-vs-drop-rules.md](references/clean-vs-drop-rules.md)

### Step 5: Snippet 标准化
将保留的证据条目格式化为统一结构。
- 去除首尾空白和多余换行
- 修正编码问题（`&amp;` → `&`、`&#39;` → `'` 等 HTML 实体）
- 修正截断文本（检测 "..." 尾部并标注 `[TRUNCATED]`）
- 统一引号格式、全半角标点
- 保留原始来源 URL 和标题不变
- 为每条证据计算 `source_reliability` 评级（S/A/B/C）

## 决策快速参考

| 证据状况 | 处理方式 |
|----------|----------|
| 微格式错误、截断、编码问题 | **Clean** — 保留但修正 |
| 二手转载、匿名来源、缺时间 | **Downrank** — 保留但降权 |
| 纯广告、完全无关、纯噪声 | **Drop** — 彻底移除 |
| 伪实体引用、AI幻觉 | **Drop + Warning** — 移除并记录警告 |
| 高度重复 | **Merge** — 合并保留最佳版本 |

完整决策树见 [references/clean-vs-drop-rules.md](references/clean-vs-drop-rules.md)。

## 参考文档

- [噪声模式识别手册](references/noise-patterns.md) — 各类噪声的识别方法与示例
- [清理/降权/丢弃判定规则](references/clean-vs-drop-rules.md) — 决策树与边界案例
- [清洗用例集](references/examples.md) — 3 个完整用例演示
