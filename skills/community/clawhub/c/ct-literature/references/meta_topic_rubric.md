# Meta-analysis 选题评估 Rubric（--meta-topic-eval）

> **定位**：本 rubric 把 `Supervisor-Skills/idea-evaluator` 的**方法论骨架**（早期致命缺陷门控 + 真实检索新颖性核查 + 证据纪律 + 完整性门控）迁移到 `ct-literature`，但将 ML 论文专属的五维评分标度（`Higher/Faster/Stronger/Cheaper/Broader`）替换为 **Meta-analysis 专属六维**。检索与覆盖度判定复用 `ct-literature` 既有能力（`--cochrane`、PICO `--concept` 模型、`coverage` 字段），评估器本身不联网、纯 stdlib。

## 1. 方法学移植映射

| idea-evaluator 组件 | 处置 | 说明 |
|---|---|---|
| 早期致命缺陷门控（early gate）+ short-circuit | **保留** | 任何 CRITICAL 直接 `Reject and Pivot`，不做装饰性打分 |
| 真实检索新颖性核查（F1） | **保留** | 查 3–5 篇最接近 meta，指出差异轴；相似标题 ≠ 重复 |
| 证据纪律（Integrity gate） | **保留** | 每维评分须引证据，不 gut feeling；`[inspection]`/`[attestation]` 分级 |
| 资源/能力匹配 | **保留并改写** | 改为「团队/工具/数据可及性」匹配 |
| 五维 `Higher/Faster/Stronger/Cheaper/Broader` | **替换** | 见 §2 六维 |
| 范式转换探测（4 问） | **删除** | Meta 是证据综合，非颠覆式创新 |
| 学生周工时匹配 | **删除** | 面向临床统计专家 |

## 2. 六维评分 Rubric

每维 1–10，**从 5 起评**；分数移动必须有证据（检索命中数、具体 meta 标题/年份、`coverage` 判定）。证据缺失则该维锁定 5 并标 `no_grounds`。

| 维度 | 评分要点 | 证据来源（复用 CT 既有） | CRITICAL / MAJOR 触发 |
|---|---|---|---|
| **F1 重叠核查** | 已有 meta 数量、时效、差异轴 | `--cochrane` + CDSR/PubMed meta 检索 | 近 2 年高质 meta 且 PICOS 已覆盖 → **CRITICAL** |
| **F2 原始研究充分性** | RCT 数量、总样本量 | 预检索命中数 + `coverage` 字段 | 命中 <3 篇 RCT 或总 n 过小 → **CRITICAL(critical_gap)** |
| **F3 PICOS 清晰度** | 人群/干预/对照/结局可操作 | PICO `--concept` 模型 | 任一要素不可操作/模糊 → **MAJOR** |
| **F4 异质性可控性** | 预期 I²、可否分层/亚组 | 预检索异质性探测 | 高异质且无分层路径 → **MAJOR** |
| **F5 临床与增量意义** | 回答未决问题/监管缺口 | 指南缺口 + 与已有 meta 增量 | 与已有 meta 无增量 → **MAJOR** |
| **F6 偏倚与可重复性** | 发表偏倚、小样本效应 | 方法学审查 | 大量灰色/未注册试验风险 → **WARNING** |

## 3. 早期门控 CRITICAL 缺陷清单（Meta 特有）

运行六维打分**之前**先跑此门控；命中任一 CRITICAL 即 short-circuit 出 `Reject and Pivot`。

| ID | 缺陷 | 判定规则 | 防御 / 出路 |
|---|---|---|---|
| **D1** | 重叠撞车 | 已存在近 2 年、高质、PICOS 近似的 Meta（overlap 轴覆盖 ≥ 其他全部） | 换差异轴或缩 PICOS 做增量亚组 |
| **D2** | 原始研究枯竭 | `rct_count < 3` 或 `total_n` 低于合并所需下限（默认 200） | 改单臂/描述性综述或延迟至证据成熟 |
| **D3** | 数据不可及 | 关键 RCT 全文无法获取且无译稿 | 评估灰色文献 / 联系作者路径 |
| **D4** | PICOS 崩塌 | **已提供部分 PICO 但缺失关键要素**（完全未提供视为待补充，不误判 CRITICAL） | 补全 PICO 各要素后再评估 |

## 4. 评分纪律（Integrity gate）

- `[inspection]`：每维分数必须引用 `evidence` 字段（来自检索产出）；无证据则锁定 5 并标 `no_grounds`。
- `[attestation]`：异质性可控性/临床意义等需领域判断的维度，标注「由评估者确认」，用户负责最终核实。
- 裁决须与评分一致：`Strong Accept` 要求 ≥2 维 ≥8 且无 MAJOR/CRITICAL。

## 5. 裁决逻辑

| 裁决 | 触发条件 |
|---|---|
| **Strong Accept** | 无 CRITICAL、无 MAJOR；≥2 维 ≥8 → 进入 PROSPERO 注册 |
| **Accept with Revisions** | 存在可修复 MAJOR（缩 PICOS / 加预设亚组 / 补数据可及性） |
| **Reject and Pivot** | ≥1 CRITICAL（D1–D4）或 ≥2 MAJOR |

## 6. 输入 spec schema（对接 `ct_literature` 检索产出）

```json
{
  "topic": "PD-1 inhibitors vs chemotherapy in advanced NSCLC (ORR)",
  "picos": {
    "population": "advanced NSCLC, treatment-naive",
    "intervention": "PD-1/PD-L1 inhibitors",
    "comparator": "platinum-doublet chemotherapy",
    "outcome": "ORR",
    "study_design": "RCT"
  },
  "evidence": {
    "existing_metas": [
      {"title": "...", "year": 2025, "type": "meta", "n_studies": 12, "overlap_axes": ["population"]}
    ],
    "primary_studies": {
      "rct_count": 8,
      "total_n": 2400,
      "coverage": "healthy",
      "heterogeneity_i2_est": 0.45
    },
    "data_accessibility": {"full_text_available": true, "grey_literature_risk": "low"}
  },
  "context": {"clinical_gap": "...", "guideline_gap": true}
}
```

`existing_metas` / `primary_studies.coverage` / `heterogeneity_i2_est` 直接由 `ct_literature` 检索与 `--cochrane` 产出填充；评估器只读、不联网。

## 7. 输出格式

`meta_topic_eval.py` 产出 JSON + MD：

1. 一击印象 + 类型定位（= Meta 选题）
2. 早期门控表（缺陷 / 严重度 / 防御）
3. 六维雷达（维度 / 分 / 证据 / 提升建议）
4. 覆盖度判定（复用 `coverage` 字段）
5. 裁决三态 + Top 3 下一步（如「注册 PROSPERO」「预检索估算合并效应」）
