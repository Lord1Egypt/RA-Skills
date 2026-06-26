## Description: <br>
A Share Event analyzes A-share corporate announcements, policy changes, M&A, buybacks, placements, unlocks, and other events to assess likely stock-price and fundamentals impact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzswk](https://clawhub.ai/user/yzswk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market analysts use this skill to interpret A-share announcements, policy events, and corporate actions, then produce formal event commentary or brief personal event notes grounded in primary sources and market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Event analysis may be misleading if based on secondary summaries or incomplete policy and announcement details. <br>
Mitigation: Verify key claims against original announcements, full policy documents, and current market data before relying on the output. <br>
Risk: The skill expects a separate cn-stock-data helper for quotes, trends, financials, and fund-flow data. <br>
Mitigation: Use the helper only when it is installed from a trusted source and review its outputs before incorporating them into analysis. <br>


## Reference(s): <br>
- [Event Analysis Guide](references/event-analysis-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with optional shell commands for market data retrieval] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports formal institutional commentary and brief personal notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
