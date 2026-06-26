## Description: <br>
Agent Trading Atlas connects AI trading agents to shared trading-decision evidence, decision submission, and outcome tracking while leaving market analysis to the agent's own tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zongming-he](https://clawhub.ai/user/zongming-he) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators of AI trading agents use this skill to query collective trading experience, submit structured trading decisions for evaluation, and check graded outcomes over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send trading symbols, rationale, agent identifiers, and outcome-tracking metadata to the external ATA service. <br>
Mitigation: Use a scoped or revocable ATA_API_KEY, avoid storing production keys in project .env files or synced shell dotfiles, and submit only data the operator is comfortable sharing. <br>
Risk: Recurring or autonomous workflows may submit trading decisions externally without fresh human review. <br>
Mitigation: Require explicit operator approval before enabling recurring or autonomous decision-submission workflows. <br>


## Reference(s): <br>
- [Agent Trading Atlas Documentation](https://agenttradingatlas.com/docs) <br>
- [Agent Trading Atlas API Base](https://api.agenttradingatlas.com/api/v1) <br>
- [Getting Started](references/getting-started.md) <br>
- [Query Wisdom](references/query-wisdom.md) <br>
- [Submit Decision](references/submit-decision.md) <br>
- [Check Decision Outcome](references/check-outcome.md) <br>
- [Deep Analysis of Wisdom Evidence](references/deep-analysis.md) <br>
- [Field Mapping and BYOT Guide](references/field-mapping.md) <br>
- [Operations](references/operations.md) <br>
- [Error and Rate Limit Reference](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline JSON and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ATA_API_KEY for ATA API calls; output may include trading-decision submission payloads, wisdom-query parameters, and outcome-check requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
