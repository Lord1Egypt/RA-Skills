## Description:

Automatically adds unfamiliar technical jargon from coding sessions to the user's tech glossary with analogy-based explanations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emanxchan](https://clawhub.ai/user/emanxchan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding assistants use this skill to recognize technical terms that may be unfamiliar and add clear glossary entries for later learning. It is tailored to a personal GitHub-hosted tech glossary workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project code or sensitive examples may be copied into the glossary.

Mitigation: Require the agent to show proposed entries first, sanitize examples, and avoid real project code by default.

Risk: Glossary changes may be committed and pushed to GitHub without explicit approval.

Mitigation: Require the agent to show the Git diff and remote, then ask for explicit approval before any commit or push.

## Reference(s):

- [Glossary Format Reference](artifact/references/glossary-format.md)
- [ClawHub Skill Page](https://clawhub.ai/emanxchan/skills/auto-glossary)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown glossary entries with optional code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform glossary file edits and Git commit/push steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
