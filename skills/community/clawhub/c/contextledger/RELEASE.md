# ContextLedger Release Notes

## Short Description

证据优先的知识审计卡，帮你追踪结论来源、判断资料时效、标记冲突，并区分证据和推断。

## Marketplace Card Copy

Title:
- 知识账本

Alternate title:
- ContextLedger

Short description:
- 证据优先的知识审计卡，帮你追踪结论来源、判断资料时效、标记冲突，并区分证据和推断

Install hook:
- 不是再做一遍总结，而是把结论背后的来源、时效和冲突讲清楚

## Announcement Copy

`知识账本（ContextLedger）` 不是一个新的知识库。

它解决的是一个更关键但常被忽略的问题：

当我们已经接了很多资料、写出了很多总结以后，
这条结论到底：
- 是从哪来的
- 还新不新
- 和别的资料冲不冲突
- 哪些地方是证据，哪些地方只是推断

所以它的定位很明确：

`不是再连更多来源，而是给知识加上审计能力。`

默认它会给出一张证据账本式结果：
- Best Current Judgment
- Source Ledger
- Oldest Or Stale Signal
- Where Sources Conflict
- Evidence Vs Inference
- What Would Change The Call
- Next Reliable Step

也就是说，它不是在重复总结，而是在回答“这个总结值不值得信”。

## Official Launch Post

今天做了一个我很喜欢的新 OpenClaw skill：`知识账本（ContextLedger）`。

很多知识类 skill 会停在这几层：
- 把资料接进来
- 把信息连起来
- 把内容总结出来

但真正影响用户是否信任一个结论的，往往是再下一层问题：
- 这个结论到底来自哪几份资料
- 哪份资料已经旧了
- 哪两份资料其实在互相打架
- 哪句话是证据，哪句话只是推断
- 现在最可靠的判断到底是什么

所以 `知识账本` 的目标不是“让我知道更多”，而是“让我知道这条结论能不能被检查”。

我给它定的一句话定位是：

`给知识加上审计能力。`

如果你也经常遇到这些情况：
- 信息很多，但不知道结论从哪来
- 摘要很顺，但不确定证据够不够
- 资料有日期差，但没人提醒你哪里可能过时
- 几份文档明明冲突，却在总结里被抹平了

那这个 skill 会很顺手。

## Suggested Tags

- latest
- knowledge
- knowledge-audit
- evidence-first
- source-traceability
- provenance
- freshness-check
- conflict-detection
- evidence-grading
- research
- trust

## Suggested Repo Name

- `openclaw-skill-contextledger`

## Manual Publish Command

```bash
clawhub publish /absolute/path/to/contextledger \
  --slug contextledger \
  --name "知识账本" \
  --version "1.0.0" \
  --changelog "Launch 知识账本 (ContextLedger), an evidence-first knowledge audit skill that traces which sources support a conclusion, flags stale evidence, surfaces conflicts, and separates evidence from inference." \
  --tags "latest,knowledge,knowledge-audit,evidence-first,source-traceability,provenance,freshness-check,conflict-detection,evidence-grading,research,trust"
```
