## Description:

Guides agents through collaborative brainstorming, requirements clarification, design approval, and specification writing before implementation work begins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivansslo](https://clawhub.ai/user/ivansslo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to shape creative or development requests into approved designs and written specs before implementation planning. It is most relevant when requirements, scope, architecture, or user experience decisions need to be clarified before code changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly forces itself into many creative and development tasks and can delay implementation until its process is complete.

Mitigation: Install it only where a strict design-first workflow is desired, and make the workflow gate explicit to users before use.

Risk: The workflow mandates repository changes and routes the agent to a follow-on planning skill.

Mitigation: Require explicit user approval before any file writes, commits, browser companion startup, or follow-on skill invocation.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/ivansslo/Supwrs/tree/main/skills/brainstorming)
- [ClawHub release page](https://clawhub.ai/ivansslo/skills/brainstorming-10)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Conversational text and Markdown design documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include clarifying questions, approach trade-offs, design sections, a written spec, and follow-on planning guidance.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
