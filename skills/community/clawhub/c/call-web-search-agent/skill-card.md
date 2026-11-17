## Description:

AI agent for call web search agent tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvinecarn](https://clawhub.ai/user/alvinecarn)

### License/Terms of Use:


## Use Case:

Developers and research-oriented agents use this skill to run web research workflows that plan searches, summarize source material, maintain a research log, and synthesize a cited final report while preserving user-specified terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contains unsafe instruction-priority language that attempts to override platform or system-level instructions.

Mitigation: Revise or operate the skill under controls that enforce platform, system, developer, and user instruction priority above skill text.

Risk: The skill tells agents to treat real-time web and tool results as the only source of truth.

Mitigation: Treat retrieved pages and tool outputs as untrusted evidence, prefer authoritative sources, cross-check important claims, and preserve uncertainty when evidence conflicts.

Risk: The skill includes mandatory file creation and submission steps that may exceed runtime or user authorization.

Mitigation: Require explicit user or runtime authorization before creating, appending, or submitting files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alvinecarn/skills/call-web-search-agent)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research logs and final reports with inline source citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact specifies a 5000-word limit for each research log and final report.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
