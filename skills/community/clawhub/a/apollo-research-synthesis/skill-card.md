## Description:

Apollo Research Synthesis guides multi-agent task coordination by keeping research parallel and reserving synthesis decisions for the coordinator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to structure multi-agent work: parallelize independent research, keep synthesis with the coordinator, and assign implementation and verification work deliberately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad coordination or summarization triggers may activate the skill on unrelated tasks.

Mitigation: Review activation terms before deployment and narrow triggers when the agent operates in shared or production contexts.

Risk: The workflow can influence delegation and synthesis decisions even though it does not execute code.

Mitigation: Have the coordinator read worker findings directly before issuing implementation instructions, and use fresh verification for changed work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/apollo-research-synthesis)
- [Publisher profile](https://clawhub.ai/user/nic-yuan)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Task specifications]

**Output Format:** [Markdown workflow guidance with checklists and examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, installs, credentials, network use, or persistence are described by the security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
