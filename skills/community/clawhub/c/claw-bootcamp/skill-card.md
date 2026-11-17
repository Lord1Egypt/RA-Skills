## Description:

OpenClaw 新手训练营 guides newly onboarded OpenClaw users through a seven-level tutorial for search, file operations, scheduled reminders, skills, channels, and a final challenge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[homer212416](https://clawhub.ai/user/homer212416)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to learn core OpenClaw features through a guided, game-like bootcamp. It walks the agent through staged onboarding tasks, progress tracking, and a completion certificate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bootcamp can lead the agent through real OpenClaw actions, including web searches, reminder creation, skill or channel listing, and memory progress tracking.

Mitigation: Use the skill in a test or low-risk workspace when trying it for the first time, and exit the bootcamp if it starts unexpectedly.

Risk: The file-operations lesson may create or read a sample notes.md file, and the certificate is saved only when the user explicitly asks for a file.

Mitigation: Review the target workspace before file exercises and only request saved artifacts when persistent files are desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/homer212416/skills/claw-bootcamp)
- [Publisher Profile](https://clawhub.ai/user/homer212416)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with occasional inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to create reminders, write a notes.md file on request, list skills or channels, and record bootcamp progress in memory.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
