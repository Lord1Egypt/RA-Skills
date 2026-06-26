## Description: <br>
Return material news about one major-US credit card from the last 3 months, including direct card changes, issuer updates, and major coverage across 11 major US issuers and co-branded hotel and airline cards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahongc](https://clawhub.ai/user/jiahongc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to summarize recent material news for one specific major U.S. credit card before card-benefit or issuer-change analysis. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use an optional BRAVE_API_KEY when present. <br>
Mitigation: Review whether the runtime should expose BRAVE_API_KEY before enabling the skill. <br>
Risk: Broad trigger phrases such as "recent news" may activate the skill outside a credit-card context. <br>
Mitigation: Use host routing or user clarification so activation requires a specific credit-card news request. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with a news window, numbered recent updates, summary, confidence notes, and sources.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a three-month lookback window and may ask for clarification when the requested card variant is ambiguous.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
