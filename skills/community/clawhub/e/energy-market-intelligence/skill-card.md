## Description: <br>
Build sourced, decision-ready Alberta energy market briefings covering AESO pool prices, supply/demand balance, outage events, regulatory changes, and commercial implications for traders, facility managers, data center developers, and sustainability teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitcanadabrett](https://clawhub.ai/user/gitcanadabrett) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as energy traders, facility managers, data center developers, sustainability teams, and PPA evaluators use this skill to turn public Alberta electricity market data and regulatory sources into sourced commercial briefings. It supports market snapshots, supply and demand analysis, source-tiered developments, commercial implications, justified market stance, and practical next actions without giving trading, procurement, legal, compliance, or PPA signing advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake informational market analysis or recommended next actions for trading, hedging, procurement, legal, compliance, or PPA signing advice. <br>
Mitigation: Frame outputs as analysis and monitoring prompts, preserve the skill's advice boundaries, verify current AESO data, and consult qualified professionals before financial or operational commitments. <br>
Risk: Alberta market conditions can shift quickly, so missing or stale data may make a briefing unsuitable for current decisions. <br>
Mitigation: Apply the no-source and stale-data gates, label data vintage and confidence, and verify live AESO and regulatory sources before acting. <br>
Risk: Low-confidence market commentary or speculation could be blended with confirmed AESO or AUC facts. <br>
Mitigation: Use the skill's source-tier rubric, separate confirmed data from projections and speculation, and avoid treating tier-3 material as confirmed fact. <br>


## Reference(s): <br>
- [Alberta Market Structure](references/alberta-market-structure.md) <br>
- [Commercial Translation - Energy Market Intelligence](references/commercial-translation-energy.md) <br>
- [Price Context Frames - Alberta Pool Price](references/price-context-frames.md) <br>
- [Source Quality Rubric - Alberta Energy Market](references/source-quality-rubric.md) <br>
- [ClawHub skill release page](https://clawhub.ai/gitcanadabrett/energy-market-intelligence) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/gitcanadabrett) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown briefing with source tiers, confidence labels, commercial implications, and next actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves source traceability and labels stale, sparse, projected, or unverified data.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
