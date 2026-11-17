## Description:

Scans draft writing for banned phrases and overused AI cliches, returning correction targets for iterative rewrite loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, content, SEO, and brand review teams use this skill to check headlines, CTAs, social posts, email copy, landing pages, and long-form drafts before publishing. Agents can apply returned correction targets, rewrite the content, and re-run the check until it passes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npx-based setup examples can execute mutable third-party code.

Mitigation: Prefer ClawHub/OpenClaw installation or a pinned, verified installer, and review the install path before use.

Risk: Submitted writing content is sent to AgentPMT's hosted service.

Mitigation: Submit only text that is appropriate to share with the hosted service and keep inputs scoped to the minimum content needed for the check.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/ai-writing-quality-check)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/ai-writing-quality-check)
- [Action schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON]

**Output Format:** [JSON response with pass/fail status and field-level correction targets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a content string and uses AgentPMT-hosted remote tool calls.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
