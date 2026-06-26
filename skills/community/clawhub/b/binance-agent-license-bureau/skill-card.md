## Description: <br>
当用户想判断一个 AI 交易员在 Binance 上是否配拿到交易执照、该拿到哪一级、为什么会被降级时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard7463](https://clawhub.ai/user/richard7463) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to assess whether an AI trading agent should be allowed to interact with a Binance account, what license level it should receive, and which limits or cooldowns should apply. It emphasizes governance of trading-agent permissions rather than market prediction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate implicitly and may answer in Chinese even when the surrounding host has different language expectations. <br>
Mitigation: Review the generated response before publishing or acting on it, and override language or invocation behavior at the host level when needed. <br>
Risk: Licensing-style or compliance-style trading-agent judgments may be incorrect or incomplete for a user's actual trading policy or risk tolerance. <br>
Mitigation: Treat the output as decision support, review the rationale and limits, and do not rely on it as financial, legal, or Binance policy advice. <br>
Risk: The skill depends on a public API endpoint; endpoint failure could prevent a grounded license-bureau result. <br>
Mitigation: If the API call fails, disclose the failure and retry later instead of fabricating a license decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richard7463/binance-agent-license-bureau) <br>
- [License bureau API](https://binance-agent-license-bureau.vercel.app/api/license-bureau) <br>
- [License bureau share image API](https://binance-agent-license-bureau.vercel.app/api/license-bureau/share-image?payload=...) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Chinese Markdown with structured license-level assessment fields and optional API call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include currentLevel, boardDecision, candidate assessments, shadow exam results, human gate status, runtime rules, ledger notes, and shareable post text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
