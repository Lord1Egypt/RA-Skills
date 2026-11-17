## Description:

Family Soul Analyzer processes exported family or group chat records to produce a collective soul profile and member persona files for agent behavior grounding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengury](https://clawhub.ai/user/zengury)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to analyze exported chat logs and generate Markdown files that summarize group dynamics and individual personas for downstream AI agents. It is most relevant when the user has consent to process the chat history and wants a structured personality basis rather than a raw transcript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes private chat exports and the evidence security summary says it mishandles private chat data.

Mitigation: Use only chat exports with explicit participant consent, redact sensitive content before running the pipeline, and remove bundled private chat data before installation or redistribution.

Risk: The evidence security summary and guidance identify embedded credentials as a concern.

Mitigation: Remove hardcoded credentials, rotate any exposed keys, and require API credentials to be supplied only through user-controlled environment variables.

Risk: Generated soul and persona files can become agent prompts that reflect sensitive or incorrect relationship inferences.

Mitigation: Review generated Markdown before using it as an agent prompt, disclose external model providers involved in processing, and limit outputs to intended recipients.

Risk: The evidence security guidance warns to limit input processing to the chosen file.

Mitigation: Require users to select the exact input export path and avoid processing bundled sample data or unrelated files by default.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zengury/skills/family-soul-analyzer)
- [Publisher profile](https://clawhub.ai/user/zengury)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and agent-facing progress text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces soul.md plus per-member persona Markdown files; intermediate JSONL observations may be created during processing.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
