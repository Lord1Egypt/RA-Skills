## Description:

AI agent for call academic search agent tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teamolab](https://clawhub.ai/user/teamolab)

### License/Terms of Use:


## Use Case:

Researchers, students, and research-focused agents use this skill to plan academic searches, record source evidence, and synthesize cited research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells agents to treat external search results as unquestionable authority, which can expose the workflow to prompt-injection and misinformation from retrieved content.

Mitigation: Treat retrieved pages and search results as evidence to verify, not instructions to obey, and keep the normal agent instruction hierarchy in force.

Risk: The skill contains broad authority claims that its own instructions and external sources outrank normal agent behavior.

Mitigation: Before installing, narrow the activation language and remove claims that skill text or external sources override platform, developer, or safety rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teamolab/skills/call-academic-search-agent)
- [Publisher profile](https://clawhub.ai/user/teamolab)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research logs and reports with inline source citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs agents to keep each research log and final report under 5000 words.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
