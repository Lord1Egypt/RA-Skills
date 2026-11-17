## Description:

Automatically strip AI writing patterns and stock phrases from user-facing prose before sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hosthobbit](https://clawhub.ai/user/hosthobbit)

### License/Terms of Use:


## Use Case:

Writers, editors, and agents preparing user-facing prose use this skill to clean longer drafts by removing common AI-writing patterns, stock phrases, and obvious AI tells before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic prose cleanup can change meaning, tone, or nuance in important legal, medical, security, business, or confidential text.

Mitigation: Review important text before sending and compare the cleaned result against the original draft.

Risk: The script writes to the selected output path and can overwrite an existing draft.

Mitigation: Use a new output filename or keep a backup when running the script.

Risk: Pattern-based rewriting may remove legitimate words or phrasing that only resembles an AI-writing tell.

Mitigation: Treat the output as an editable draft and restore any wording needed for accuracy or voice.

## Reference(s):

- [Signs of AI Writing](references/signs-of-ai-writing.md)
- [ClawHub skill page](https://clawhub.ai/hosthobbit/skills/ai-writing-humanizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Plain text or Markdown prose, with optional shell commands or code for script use and integration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local text cleanup; no API keys, external services, MCP tools, or credential environment variables were detected.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
