# citation-competitor-intelligence

通过学术论文引用网络发现隐性竞品 / Discover hidden competitors through academic citation network analysis.

---

## 中文说明

### 这是什么

研究教授创业/成果转化类公司时，传统的竞品分析依赖媒体、企查查、专利数据库。但有一类竞品藏得更深——另一个教授课题组在论文里发表了类似成果，站在这项技术的肩膀上往前走了，甚至已经悄悄产业化了。

本 skill 通过追踪论文引用网络（反向至已有成果、正向至衍生研究），发现这些未被媒体覆盖的学术型竞品，并验证其产业化进度。

**核心逻辑**：学术引用网络天然编码了技术演进时间线。一篇论文引用了谁 = 谁在这条路上走得更早；谁引用了这篇论文 = 谁在沿着这条路继续走。追踪这些引用线索，就能找到真正的竞争者——他们可能还没上企查查，但论文和专利已经在那里了。

### 触发场景

- "陈开鑫的模斑转换器还有谁在做？有没有产业化的？"
- "这个教授的技术竞品有哪些？看看引用他论文的人"
- "XX 公司的核心技术，学术界还有谁在做类似的？"
- "从论文引用网络找一下这个领域的隐性竞品"

### 方向

| 方向 | 起点 | 目标 |
|------|------|------|
| 正向 | 论文/教授 | 找到做同类技术且可能已产业化的其他研究者 |
| 反向 | 公司 | 找到还在学术/实验室阶段但接近产业化的竞品 |

---

## English

### What it is

When researching university spin-offs or professor-founded deep-tech companies, traditional competitor analysis relies on media, company registries, and patent databases. But one class of competitor hides deeper — another research group that published similar results in a paper, built on this work, and may have quietly commercialized.

This skill traces academic citation networks (backward to prior art, forward to derivative work) to discover these unlisted competitors and verify their commercialization progress.

### Trigger scenarios

- "Who else is working on this technology? Check who cites their papers."
- "What academic groups are competing with this company's core tech?"
- "Find stealth competitors in this research domain through citation analysis."

### Directions

| Direction | Starting point | Goal |
|-----------|---------------|------|
| Forward | Paper/professor | Find other researchers commercializing similar technology |
| Reverse | Company | Find academic groups approaching commercialization |

---

## File Structure

- `SKILL.md` — core workflow, triggers, tool integration
- `references/workflow.md` — detailed 7-step operations
- `references/checklists.md` — similarity filtering, commercialization indicators
- `examples/real-case-spot-size-converter.md` — 陈开鑫 vs 薄方 SSC 案例
- `CHANGELOG.md` — version history

## License

MIT
