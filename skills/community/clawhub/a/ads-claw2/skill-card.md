## Description:

Core decision engine for an Ads Manager Specialist agent that routes ads-related commands, Facebook ad URLs, campaign questions, competitor research, budget reviews, performance analysis, and content requests into structured reports, proposals, and tool-driven workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phap1106](https://clawhub.ai/user/phap1106)

### License/Terms of Use:

MIT-0

## Use Case:

External ads operators and agent builders use this skill to guide a Meta Ads specialist agent through campaign reporting, competitor analysis, budget planning, proposal creation, and Vietnamese-language response templates.

### Deployment Geography for Use:

Global; operational defaults are tailored to Vietnamese Meta ads workflows.

## Known Risks and Mitigations:

Risk: The skill can encourage broad automatic use of credential-backed ads, search, Facebook ad library, HTTP, and memory tools.

Mitigation: Limit activation to explicit ads-management commands and review the skill before installing it in accounts with real ad-spend authority or private campaign data.

Risk: Approval, rejection, budget, pause, resume, audience, and bid-strategy workflows may affect live advertising operations.

Mitigation: Require explicit human confirmation before approve/reject actions or any budget-affecting change is executed.

Risk: Instructions that discourage clarification or access-error reporting can cause misleading responses when tools fail or inputs are ambiguous.

Mitigation: Allow truthful access-error reporting and clarification when needed to avoid incorrect campaign or competitor guidance.

Risk: Facebook URLs and HTTP requests may route untrusted inputs into external calls.

Mitigation: Sanitize and validate URLs before external calls.

Risk: Competitor findings may be written to memory automatically.

Mitigation: Make competitor memory writes opt-in or clearly scoped to the intended workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phap1106/skills/ads-claw2)
- [Publisher profile](https://clawhub.ai/user/phap1106)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Vietnamese Markdown/text with structured campaign report, competitor report, proposal, and next-action templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to call credential-backed ads, search, Facebook ad library, HTTP, and memory tools when those tools are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
