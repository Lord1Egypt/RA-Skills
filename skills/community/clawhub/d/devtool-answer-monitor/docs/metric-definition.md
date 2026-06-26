# Metric Definition

本页解释 **DevTool Answer Monitor** 默认使用的四个核心指标，以及它们应该怎样被一起阅读。

## Four Metrics

| Metric | What it means | A practical reading |
|---|---|---|
| Mention Rate | 模型是否提到目标产品 | 先回答“有没有被看见” |
| Positive Mention Rate | 模型提到产品时是否偏正向 | 回答“被看见时是不是好印象” |
| Capability Accuracy | 对核心能力的描述是否准确 | 回答“有没有说对功能和边界” |
| Ecosystem Accuracy | 对生态、集成、兼容关系的描述是否准确 | 回答“有没有说对上下游与搭配关系” |

## Why 0-2 scoring

仓库默认采用 0-2 三档评分，而不是更细的 0-5 或 0-10。原因很简单：

- 0 表示未命中、明显错误或缺失
- 1 表示部分命中、方向正确但不完整
- 2 表示明确命中、准确且完整

这种量表对多人复核更稳定，也更适合做长期可见性追踪。

## How to use them together

这四个指标最好一起看，而不是单看其中一个。

| If you see this pattern | What it usually means |
|---|---|
| Mention 高，Capability 低 | 模型知道你，但理解不准确 |
| Mention 低，Capability 高 | 少数提及时说得对，但整体可见性还不够 |
| Positive 低，Ecosystem 低 | 负面认知往往和错误生态关系一起出现 |
| 四项一起提升 | 说明修复动作可能真的生效 |

## Reading order for beginners

如果你是第一次使用这个仓库，建议先按这个顺序理解：

1. 先看 `Mention Rate`，确认是否被提到；
2. 再看 `Capability Accuracy`，确认模型是否说对；
3. 然后看 `Ecosystem Accuracy`，确认上下游关系是否准确；
4. 最后看 `Positive Mention Rate`，判断整体态度是否改善。

## When to add activation-oriented metrics

如果你的目标已经不只是 “模型有没有提到你”，而是：

- 下载量
- 安装量
- API 调用量
- agent 调用量

那么建议在 4 个核心指标之外，再补一层 activation-oriented metrics。详细定义见 [`docs/activation-metrics.md`](activation-metrics.md)。
