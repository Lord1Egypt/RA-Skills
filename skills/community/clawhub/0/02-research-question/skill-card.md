## Description:

Use when the user knows the broad field and reads papers to find concrete, researchable, experimentally testable gaps or research questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snake-fan](https://clawhub.ai/user/snake-fan)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers use this skill to turn a completed paper-reading field map into concrete, evidence-backed research question cards aligned with writing intent and practical constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated research questions can overstate gaps if the source papers or evidence notes are incomplete or inaccurate.

Mitigation: Review Research Question Cards against the cited Field Map and Supporting Evidence records before treating recommendations as decision-ready.

Risk: The workflow creates or updates markdown artifacts under a research-question workspace.

Mitigation: Run it in the intended workspace and review file changes before relying on the generated artifacts.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/snake-fan/Paper-Reading-Skills/tree/main/skills/02-research-question)
- [ClawHub release page](https://clawhub.ai/snake-fan/skills/02-research-question)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown files and conversational guided choices]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a repo-local research-question workspace and preserves user edits when resuming existing work.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
