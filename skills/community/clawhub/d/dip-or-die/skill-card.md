## Description: <br>
Helps users decide whether and how to buy market dips, with emphasis on target selection, options posture, position sizing, and risk discipline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skb2026](https://clawhub.ai/user/skb2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill as trading-guidance context for evaluating whether a market dip is suitable for cautious entry, especially when considering long-dated lightly in-the-money call options. It should support human review and planning, not autonomous trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading and options guidance may be unsuitable for a user's financial situation or may be wrong under current market conditions. <br>
Mitigation: Require independent human review of assumptions, position sizing, and market data before acting on any output. <br>
Risk: The skill discusses aggressive dip-buying and options strategies that can lead to total loss of the committed capital. <br>
Mitigation: Use the guidance only for planning and education; keep strict loss limits and avoid treating the skill as financial advice. <br>
Risk: An agent could overstep by converting guidance into account actions. <br>
Mitigation: Do not grant brokerage credentials, trading permissions, or autonomous order-placement authority based on this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skb2026/dip-or-die) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance and decision checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution, tool calls, credentials, or brokerage access are produced by the skill.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
