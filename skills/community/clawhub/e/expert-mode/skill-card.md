## Description:

Expert Mode manages a local library of AI expert personas, helps users search or activate personas, and gates external updates and memory writes behind review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[syx1989](https://clawhub.ai/user/syx1989)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to maintain a reviewed expert-persona library, search by category or fuzzy match, activate a selected expert mode, and add limited custom expert descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch expert definitions from external repositories and broad fallback sources before persisting them into agent memory.

Mitigation: Review fetched content and every proposed MEMORY.md change before confirming any write.

Risk: Automatic synchronization can repeatedly introduce remote persona changes if enabled.

Mitigation: Keep automatic sync disabled unless the sources are trusted, and prefer pinned or manually reviewed expert lists.

Risk: Weak validation of remotely sourced expert definitions could allow unsafe or misleading persona content to be stored.

Mitigation: Reject suspicious content during review and load active expert configurations only from the local trusted list.

## Reference(s):

- [Expert Mode README](references/README.md)
- [agency-agents](https://github.com/msitarzewski/agency-agents)
- [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh)
- [agent-teams](https://github.com/dsclca12/agent-teams)
- [kung-fu](https://github.com/ross-veitch/kung-fu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration, Files]

**Output Format:** [Markdown-style conversational responses with previews and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose MEMORY.md updates after review and explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
