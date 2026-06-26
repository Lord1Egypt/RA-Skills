## Description: <br>
Gate spot trading and account operations skill for buy/sell actions, balance checks, order management, fill verification, and conditional or trigger orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate Gate spot accounts through configured MCP tools, including account queries, trade drafting, order placement after confirmation, amendments, cancellations, and post-trade verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real Gate spot account changes through order placement, amendment, and cancellation tools. <br>
Mitigation: Use a Gate API key with the smallest practical permissions, keep ambiguous trading language in draft or read-only mode, and require explicit per-action confirmation before any write operation. <br>
Risk: Security evidence flags inconsistent TP/SL and confirmation behavior that needs review before installation. <br>
Mitigation: Review TP/SL and trigger-order paths before deployment, echo trigger conditions and prices in the draft, and require fresh confirmation for each trigger or multi-leg order. <br>


## Reference(s): <br>
- [Gate Skills Homepage](https://github.com/gate/gate-skills) <br>
- [Gate Spot MCP Specification](references/mcp.md) <br>
- [Gate Spot Runtime Rules](references/gate-runtime-rules.md) <br>
- [Gate Spot Scenarios](references/scenarios.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/gaixianggeng/gate-exchange-spot-v2-staging) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown responses with order drafts, execution reports, account summaries, and setup or recovery guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Gate MCP credentials and per-action confirmation before write operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
