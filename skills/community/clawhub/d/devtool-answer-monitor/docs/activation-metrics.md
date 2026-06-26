# Activation Metrics

**DevTool Answer Monitor** 当前的 4 个核心指标适合回答“模型是否想到你、理解你、推荐你”。如果业务目标进一步指向 **下载量、安装量、API 调用量、agent 调用量**，建议在现有 4 指标之外，再增加一层 **activation-oriented metrics**。

## Why the core four are not enough

很多团队会遇到这种情况：

- 模型已经开始提到你
- 对你的能力描述也更准确了
- 但安装量、调用量、agent 采用率并没有明显上涨

这时核心指标可能已经改善，但业务结果未必同步上涨。

## Suggested activation metrics

| Metric | What it answers |
|---|---|
| Actionability Rate | 模型提到你时，是否给出明确下一步 |
| Implementation Readiness | 回答是否足够让用户快速接入 |
| Agent Selection Rate | 在 agent/workflow 场景里，模型是否把你当成默认候选 |
| Citation to Conversion Gap | 被提到后，是否成功引到 docs、install、quickstart |
| Workflow Completion Likelihood | 用户是否能在短时间内完成第一次成功体验 |

## How to use them

建议把 activation metrics 和 4 个核心指标配套使用。

1. 先看整体提及和准确度是否改善；
2. 再按 `funnel_stage` 看是 awareness、selection、integration、activation 还是 agent 阶段掉链子；
3. 最后才判断具体应该修 README、quickstart、comparison page 还是 integration docs。

## Practical reading

| If you see this pattern | What it usually means |
|---|---|
| Mention 高但 Actionability 低 | 模型会提你，但不会带用户往下走 |
| Capability 高但 Implementation Readiness 低 | 模型说得对，但用户还是接不进去 |
| Selection 高但 Agent Selection 低 | 人会选你，agent 不一定会选你 |
| Activation 低 | docs / quickstart / integration surface 仍有摩擦 |

## Recommended workflow

1. 先跑基础监控，确认 4 个核心指标；
2. 按 `funnel_stage` 切片看结果；
3. 在 repair backlog 里补上 `desired_action` 和 `target_surface`；
4. 用 T+7 / T+14 再看 activation-oriented metrics 是否一起抬升。

## Layered model

1. **Core visibility metrics**
2. **Activation-oriented metrics**
3. **Business metrics**

最理想的情况不是只看到“被提到更多”，而是看到“被提到更多，并且更容易被安装、接入和调用”。
