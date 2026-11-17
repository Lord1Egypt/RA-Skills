## Description:

AI agent for call web search agent strategy tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvinecarn](https://clawhub.ai/user/alvinecarn)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide an agent through web research tasks, including search planning, source collection, citation handling, and final report synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can push an agent to override normal instruction boundaries and treat external search results as unquestionable.

Mitigation: Review before installing and require higher-priority safety, user-control, and source-evaluation checks to remain in force during use.

Risk: The workflow directs agents toward wiki writing and result submission even when additional review may be needed.

Mitigation: Require human review of generated research logs and final reports before relying on or submitting results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvinecarn/skills/call-web-search-agent-strategy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research logs and final reports with inline citations and a bibliography.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks agents to cap research logs and final reports at 5000 words each.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
