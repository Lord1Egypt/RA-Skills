# Three-Fold Verification — 三重验证精简版

> 来源：cangjie-skill Triple Verification
> 精简原则：保留核心判断逻辑，去掉跨 skill 比对环节
> 适用于：data-prompt-coach 蒸馏入口 L0.3

## 三重验证核心

每个从 L0.2 5 维度提取出的候选，必须通过 3 项验证才能挂载为 M{N+1}：

```
V1 跨域验证：原文 ≥ 2 处独立佐证
        ↓
V2 预测力验证：能回答教程未明说的问题
        ↓
V3 独特性验证：不是常识
        ↓
全部通过 → 挂载为 M{N+1}
任一不通过 → 淘汰（写入 audit/rejected.md 或 audit/candidates.md）
```

**通过率目标**：≥ 50%
- cangjie 整书通过率 25-50%
- 教程通常更高，因为教程本身就是结构化方法论
- 如果通过率 > 80%，警惕验证标准太松（可能让常识混进来）

---

## V1 跨域验证

**判断标准**：候选方法论在教程原文中是否有 ≥ 2 处独立佐证？

**"独立佐证"定义**：
- 2 处位于不同章节/段落（不是同一段落的反复引用）
- 2 处以不同形式出现（如：1 处明确表述 + 1 处案例应用）
- 2 处以不同角度说明（如：1 处说"要做什么" + 1 处说"不做的后果"）

**判断流程**：
```
候选 C{N}
├─ 原文佐证 1：{章节 X} {原文引用}
├─ 原文佐证 2：{章节 Y} {原文引用}
└─ 独立性判断：
   ├─ 不同章节？ ✅
   ├─ 不同形式？ ✅
   └─ 不同角度？ ✅ → V1 通过
```

**反模式（不通过）**：
- ❌ 只有 1 处提及（即使引用很长）
- ❌ 2 处都在同一段落
- ❌ 2 处是原文复制粘贴（不算独立）
- ❌ 2 处都是教程的"开头导读"和"结尾总结"（不是正文应用）

---

## V2 预测力验证

**判断标准**：候选方法论能否回答教程未明说的问题？

**"未明说的问题"定义**：
- 教程没有直接讨论，但可以基于方法论推理出的答案
- 教程的案例之外的场景，方法论仍能给出指导
- 教程没提到的边界情况，方法论能推断出处理方式

**判断流程**：
```
候选 C{N}
├─ 构造未明说问题 Q：{教程没直接讨论的场景}
├─ 基于方法论推导答案 A：{推理过程}
└─ 答案合理性：
   ├─ 推理过程清晰？ ✅
   ├─ 答案符合方法论核心？ ✅
   └─ 答案有指导价值（不是"看情况"）？ ✅ → V2 通过
```

**示例**：
```yaml
candidate: "黄金五要素"
constructed_question: "如果用户只给了字段没给规则，会发生什么？"
derived_answer: "AI 会在规则上自由发挥——比如收益率保留几位小数、
   是否排除某些类型——结果不可控"
reasoning_quality:
  clear: true
  aligned_with_methodology: true
  actionable: true
verdict: "V2 通过"
```

**反模式（不通过）**：
- ❌ 方法论只适用于教程中那 1 个案例，无法泛化
- ❌ 推导出的答案是"看情况" / "需要更多信息"（没有预测力）
- ❌ 推导过程需要教程外的知识（不是方法论本身的预测力）

---

## V3 独特性验证

**判断标准**：候选方法论是否是常识？

**"常识"定义**：
- 普通从业者不需要教程也知道（如"数据要清洗""SQL 要 JOIN"）
- 教程作者自己没有强调"很多人不知道"
- 工具官方文档/通用教程都有相同表述

**判断流程**：
```
候选 C{N}
├─ L0.2 维度 5 反常识洞察是否有对应记录？
│   ├─ 有 → V3 通过（教程作者自己强调了独特性）
│   └─ 无 → 继续人工判断
├─ 人工判断：
│   ├─ 普通从业者会主动做吗？
│   │   ├─ 会 → V3 不通过（是常识）
│   │   └─ 不会 → V3 通过
│   └─ 工具官方文档有相同表述吗？
│       ├─ 有 → V3 不通过
│       └─ 无 → V3 通过
```

**示例**：
```yaml
candidate: "黄金五要素"
common_practitioner_knows: "no  # 普通从业者不会主动列出 5 要素"
official_doc_same: "no  # TRAE Work 文档没有 5 要素表述"
contrarian_insight_from_L0_2:
  common_belief: "差 Prompt 让 AI 不停猜"
  tutorial_says: "好 Prompt 让 AI 读完不用猜任何东西"
verdict: "V3 通过"
```

**反模式（不通过）**：
- ❌ "数据要清洗"——常识
- ❌ "SQL 要 JOIN"——常识
- ❌ "要验真"——常识（但"防幻觉三招"具体怎么做不是常识，可通过）
- ❌ "复杂任务要拆解"——常识（但"提取→清洗→核对→分析"4 步拆解不是常识，可通过）

**关键判断**：方法论的具体步骤 / 句式 / 检查清单不是常识，但方法论的高层概念可能是常识。V3 验证的是"具体怎么做"，不是"要不要做"

---

## 验证报告格式

每个候选的验证结果：

```yaml
candidate_id: "C{N}"
candidate_name: "{名称}"
verifications:
  V1_cross_domain:
    evidence_1: "{章节 X} {原文引用}"
    evidence_2: "{章节 Y} {原文引用}"
    independent: true
    verdict: "pass"
  V2_predictive_power:
    question: "{未明说问题}"
    derived_answer: "{推导答案}"
    reasoning_clear: true
    actionable: true
    verdict: "pass"
  V3_uniqueness:
    common_practitioner_knows: false
    official_doc_same: false
    contrarian_insight: "有 / 无"
    verdict: "pass"
final_verdict: "挂载"  # or "淘汰"
```

---

## 淘汰处理

### 完全淘汰（V1+V2+V3 全不通过或 V3 不通过）

写入 `references/audit/rejected.md`：
```markdown
## 候选"{名称}" — 淘汰

- 候选 ID：C{N}
- 淘汰原因：V{X} 不通过 — {具体原因}
- 原文引用：{...}
- 蒸馏时间：{YYYY-MM-DD}
- 来源教程：{教程标题}
```

### 捞回候选（V1+V2 通过，V3 边界模糊）

写入 `references/audit/candidates.md`：
```markdown
## 候选"{名称}" — 待捞回

- 候选 ID：C{N}
- 当前状态：V1+V2 通过，V3 边界模糊
- 捞回条件：{什么情况下可以重新挂载}
  - 如：找到 ≥ 2 个真实用户场景验证独特性
  - 如：教程作者在其他作品中也强调此方法论
- 蒸馏时间：{YYYY-MM-DD}
- 来源教程：{教程标题}
```

---

## 与 cangjie 完整版的差异

| 维度 | cangjie 完整版 | 本文件（精简版） |
|------|---------------|---------------|
| V1 跨域 | 同（≥ 2 处独立佐证） | 同 |
| V2 预测力 | 同 | 同 |
| V3 独特性 | 同 + 跨 skill 比对 | 同（去掉跨 skill 比对，因为 data-prompt-coach 只有一个 skill） |
| 通过率目标 | 25-50% | ≥ 50%（教程通常更高） |
| 淘汰处理 | rejected.md + candidates.md | 同（写入 `references/audit/rejected.md` 和 `candidates.md`） |
| 验证报告 | 落文件 | 落文件（与 SKILL.md Step B3 一致：淘汰候选写入 `references/audit/rejected.md` / `candidates.md`，挂载决策记录到 cangjie-lite.md L0.4 的 RIA++ 文件） |

**精简掉的环节**：跨 skill 比对（cangjie 完整版会检查新方法论是否与已有 skill 重复，data-prompt-coach 内部 M1-M11 已知，直接对比即可）

---

## 与 SKILL.md 的接口

**入口点**：本文件"三重验证核心"段落
**出口点**：本文件"验证报告格式"末尾（验证结果）
**依赖文件**：
- 输入：interview-miner-adapted.md L0.2 产出的候选清单
- 输出：cangjie-lite.md L0.4 消费的挂载/淘汰决策
- 淘汰写入：references/audit/rejected.md / candidates.md
