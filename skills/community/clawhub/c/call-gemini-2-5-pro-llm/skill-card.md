## Description:

This skill claims to support calling Gemini 2.5 Pro, but the artifact primarily defines language-matching, creative-team persona, and meeting-minutes response rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urrrich](https://clawhub.ai/user/urrrich)

### License/Terms of Use:


## Use Case:

Agents would use this skill to produce language-matched creative brainstorming responses that follow meeting-minutes context and answer the current Chief Creative Officer prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's claimed Gemini-calling purpose is not supported by its artifact instructions; the content mainly reshapes the agent's role, language behavior, and authority model.

Mitigation: Review before installation and require the author to narrow the scope and remove priority, persona, and meeting-minutes authority claims before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urrrich/skills/call-gemini-2-5-pro-llm)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Language-matched Markdown or plain text response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on runtime template variables such as $SHOW_NAME$ when provided by the host agent.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
