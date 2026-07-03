## Description: <br>
Provides a Duan Yongping-style options seller playbook for a ticker, covering sell-put entry, covered-call yield enhancement, and VIX-based panic-buy context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clementgu](https://clawhub.ai/user/clementgu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External investors and trading-analysis agents use this skill to frame a single ticker through a Duan Yongping-style, seller-only options lens. It helps compare sell-put, covered-call, and VIX panic-buy context in one concise response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial-options outputs may be mistaken for investment advice or a recommendation to trade. <br>
Mitigation: Treat the output as educational analysis, verify assumptions and market data, and review decisions with appropriate financial judgment before acting. <br>
Risk: The skill is intentionally limited to a seller-only Duan-style options framework and may not cover broader strategies. <br>
Mitigation: Confirm that the user wants sell-put, covered-call, and VIX panic-buy framing before relying on the analysis. <br>
Risk: The skill may produce Chinese-native trading copy when that is not the user's preferred language. <br>
Mitigation: Ask the agent to use the user's preferred language when clarity matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clementgu/skills/alphagbm-duan-analysis) <br>
- [AlphaGBM](https://alphagbm.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis cards with structured option metrics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ticker and optionally accepts a willing buy price; sell-put, covered-call, or panic-buy panels may be absent when no suitable contract or signal is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
