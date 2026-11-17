---
name: "concept-radar"
description: "概念雷达——从一个链接或一批作者里，把「值得跟进的新概念」捞出来：去重、给证据、打分、可导出。治的是信息焦虑：不追热点，只留能落地的概念。Discovers, deduplicates, evaluates, and exports evidence-backed concepts from one URL or an author pool. Use when the user wants to track a field, mine an author's idea pool, or run recurring concept research; publishing is optional. Not a news feed — output is evidence-graded concepts, not breaking headlines."
version: 0.1.4
---

# Concept Radar

这是一个渠道无关、周期无关的概念发现流程。它支持：

- `single-url`：分析用户指定的单个 URL。
- `author-pool`：扫描配置中的作者来源（RSS/Atom 与 GitHub Gists）。
- 默认生成 Markdown 与 JSON；只有用户明确要求时才发布到飞书。

默认配置、状态与运行目录分别为：

- `.trae/concept-radar/authors.yaml`
- `.trae/concept-radar/state.json`
- `.trae/concept-radar/runtime`

## 执行顺序

1. 运行 `doctor`。默认只检查 Python、配置与状态，不检查或依赖飞书。
2. 按请求选择扫描模式：
   - 单 URL：`scan --url <URL>`
   - 作者池：`scan --mode author-pool`
3. 阅读本轮完整候选，按 [evidence-policy.md](references/evidence-policy.md) 和
   [quality-rubric.md](references/quality-rubric.md) 评估并合并重复概念。
4. 生成符合 [card-schema.json](references/card-schema.json) 的 selection JSON。
5. 运行 `validate-selection`。成功后默认生成 `concept-radar.md` 与
   `concept-radar.json`，不调用任何发布渠道。
6. 只有用户明确要求发布到飞书时，才先运行 `doctor --channel feishu`，再运行
   `publish --channel feishu`。

抓取失败不得解释为“无更新”，不得推进来源游标。空 selection 可以提交成功扫描，
但不得调用任何发布渠道。状态机与恢复规则见 [state-contract.md](references/state-contract.md)。

## 命令

```bash
# 默认 doctor：无飞书依赖
python3 .trae/skills/concept-radar/scripts/concept_radar.py doctor

# 单 URL
python3 .trae/skills/concept-radar/scripts/concept_radar.py scan \
  --url https://example.com/article

# 作者池
python3 .trae/skills/concept-radar/scripts/concept_radar.py scan \
  --mode author-pool

# 校验卡片并生成 Markdown + JSON
python3 .trae/skills/concept-radar/scripts/concept_radar.py validate-selection \
  --selection .trae/skills/concept-radar/examples/selection.example.json

# 可选飞书发布；仅在用户明确要求时执行
python3 .trae/skills/concept-radar/scripts/concept_radar.py doctor --channel feishu
python3 .trae/skills/concept-radar/scripts/concept_radar.py publish --channel feishu
```

## 卡片要求

每张卡片必须包含原有定义、价值、问题与旧范式对比字段，并新增：

- `maturity`：`hypothesis`、`emerging`、`growing` 或 `established`。
- `confidence`：0 到 1 的数值，表示证据支持度而非主观喜好。
- `action_recommendation`：带边界的下一步建议。
- `comparison_sources`：用于核验对比结论的来源列表。
- `evidence`：按字段关联原文短引文与 URL。

不得把成熟度写成热度，不得把置信度写成精确真值，不得用模型常识替代证据。
最终 Markdown 必须显式渲染成熟度、置信度、行动建议、对比来源和证据。

## 安全与隐私

Skill 内不得保存 token、cookie、open_id、抓取正文、一次性运行结果或用户私密数据。
发布包排除规则见 [RELEASE.md](RELEASE.md) 与 `.skillignore`。

## Related skills

- 概念雷达筛出「值得跟进」之后，用 `priority-coach` 决定「这周到底做哪一个」：一个治信息焦虑，一个治选择焦虑。
