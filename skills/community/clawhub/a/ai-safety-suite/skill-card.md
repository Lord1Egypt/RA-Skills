## Description:

Routes agent developers to nine independently published safety sub-skills for red-team testing, injection defense, leak checks, runtime guarding, and skill admission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers use this routing guide to select the appropriate independent sub-skill when testing agents for prompt injection, checking for leaks, guarding tool calls, or reviewing third-party skills. The router does not perform these checks itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mistaking the routing guide for a complete security check could leave an agent unprotected.

Mitigation: Review each referenced sub-skill separately before relying on it, particularly those handling prompts, tool calls, MCP configurations, or unpublished disclosures.

## Reference(s):

- [PromptShield ClawHub release](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-safety-suite)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text stage list or routing note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Names the relevant sub-skill and expected result without running its security checks.]

## Skill Version(s):

1.0.1 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
