## Description:

Discover which free or low-cost AI APIs are reachable from the current environment, verify them safely, and recommend a task-to-provider routing plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuxuclassmate](https://clawhub.ai/user/xuxuclassmate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check reachable AI API providers, safely verify credentials after approval, and choose a low-cost routing plan for chat, code, speech, or multimodal tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make outbound requests to AI provider domains while checking availability.

Mitigation: Use short, explicit reachability probes and tell the user which providers will be contacted before testing.

Risk: Credential verification may involve API keys if the user chooses to test authenticated endpoints.

Mitigation: Request only the minimum key needed, mask secrets in logs and notes, and do not store keys unless the user explicitly approves it.

Risk: Provider availability, quotas, and free-tier costs are time-sensitive.

Mitigation: Base routing recommendations on current verified results and re-check providers when conditions may have changed.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with provider status notes, routing recommendations, and inline code or shell commands when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reachable providers, credential requirements, task-to-provider routing, cost or quota notes, and missing coverage.]

## Skill Version(s):

1.0.1 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
