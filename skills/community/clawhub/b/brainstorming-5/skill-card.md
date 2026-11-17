## Description:

You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovemymobilewebsite-dotcom](https://clawhub.ai/user/lovemymobilewebsite-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to turn creative or implementation requests into approved designs before writing code. It supports context review, clarifying questions, approach comparison, design documentation, spec review, and transition into implementation planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enforces a strict design-first workflow that can alter normal agent behavior and block implementation until approvals are complete.

Mitigation: Install it only when the workspace wants mandatory design approval before coding, and confirm the approval gates fit the team's workflow.

Risk: The optional browser companion runs a local web server with persistent session files and unauthenticated event handling.

Mitigation: Keep the companion bound to 127.0.0.1, avoid 0.0.0.0 unless network access is contained, add .superpowers/ to .gitignore, and clean up session files when finished.

Risk: The workflow can create design documents, start long-running local server processes, and request commits as part of the design process.

Mitigation: Require explicit user approval before commits or long-running server use, and review generated documents before moving to implementation planning.

## Reference(s):

- [ClawHub Brainstorming skill release](https://clawhub.ai/lovemymobilewebsite-dotcom/skills/brainstorming-5)
- [Visual Companion Guide](artifact/visual-companion.md)
- [Spec Document Reviewer Prompt Template](artifact/spec-document-reviewer-prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown conversation, design documents, review prompts, and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create project design documents and use a local browser companion when visual brainstorming is approved.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
