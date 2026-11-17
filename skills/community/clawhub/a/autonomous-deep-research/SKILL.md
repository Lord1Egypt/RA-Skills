---
name: autonomous-deep-research
version: 1.0.0
description: |
  自主深度研究（整合与进阶·元能力）。给定一个开放研究问题，agent 自主完成：
  问题分解→多源检索(rag / web-fetch)→综合与交叉验证→反思覆盖度→迭代逼近答案。
  对标一线大模型智能体的「深度研究」能力（如 Deep Research），且可离线/在线双模运行、
  自带置信度校准与未解缺口标记。当需要对一个复杂、多侧面问题做有依据、可追溯、可迭代的研究时使用。
agent_created: true
visibility: public
---

# autonomous-deep-research —— 自主深度研究

把「提出好问题 + 检索 + 综合」熔成一条**可迭代、可追溯**的研究闭环。
这是目前一线大模型正重点攻关的方向，也是「强模型 vs 超级研究 agent」的分水岭。

## 闭环（research.py 真实实现）

1. **分解 Decompose**：把主问题拆成 3–5 个可独立检索的子问题（按连词/关键概念切分）。
2. **检索 Retrieve**：对每个子问题，优先调用 `rag`(本地知识库) 或 `web-fetch`(在线)；
   两者皆缺时降级为「本地启发式」，并显式标记 `needs_web` 供下一轮补齐。
3. **综合 Synthesize**：把各子答案按「主张 + 依据 + 置信度」结构聚合成研究报告。
4. **反思 Reflect**：检查每个子问题是否已有依据、是否存在自相矛盾，定位覆盖空洞。
5. **迭代 Iterate**：对空洞子问题进入下一轮检索（最多 `max-iter` 轮），逐步逼近完整答案。

## 使用

```bash
python autonomous-deep-research/scripts/research.py \
  --question "RAG 在 agent 架构里到底解决什么问题？和纯微调大模型相比边界在哪？" \
  --out report.json --max-iter 2
```

## 输出 `report.json`

```json
{
  "question": "...",
  "sub_questions": ["...","..."],
  "findings": [{"sub":"...","answer":"...","confidence":0.8,"needs_web":false}],
  "synthesized_answer": "结构化综合结论（含分节与依据）",
  "coverage": 0.85,
  "open_gaps": ["尚未用在线数据验证 X"],
  "next_steps": ["对 X 补一次 web-fetch 检索"]
}
```

## 自我进化

自带 `learner.py`（由 `skill-self-improve` 注入）。每次研究后把「哪类问题最难检索 /
哪类主张最易缺依据 / 迭代轮次与覆盖度提升的关系」记入 `learned_patterns.json`，
下一次自动调优分解粒度与检索策略。
