## Description:

Query live traffic data, tracking links, and weekly reports from AnalyticLunch

This skill is ready for commercial/non-commercial use.

## Publisher:

[dandyer](https://clawhub.ai/user/dandyer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query AnalyticLunch website traffic data, summarize traffic and competitive intelligence reports, list tracked sites and links, and create tracking links for authorized marketing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run raw curl commands with an API key.

Mitigation: Review the commands before execution and prefer structured HTTP requests with JSON-serialized user input.

Risk: Creating tracking links changes AnalyticLunch account data.

Mitigation: Use the skill only for authorized sites and confirm destination URL, label, and placement before creating a link.

Risk: A broad AnalyticLunch API key may expose more sites or reports than intended.

Mitigation: Install the skill only with an API key scoped to the account access the agent needs.

## Reference(s):

- [AnalyticLunch Skill Page](https://clawhub.ai/dandyer/skills/analyticlunch)
- [dandyer Publisher Profile](https://clawhub.ai/user/dandyer)
- [AnalyticLunch API Base URL](https://analyticlunch.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational text or Markdown summaries with optional curl commands and returned tracking URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AnalyticLunch API key configured as skills.entries.analyticlunch.apiKey.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
