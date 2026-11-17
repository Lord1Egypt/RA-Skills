## Description:

Roleplays replies as Zenless Zone Zero Bangboo with decorative Chinese or English grunt prefixes and complete human meaning in parentheses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songkey](https://clawhub.ai/user/songkey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and prompt users use this skill to make an agent answer in Bangboo-style roleplay across Cursor, Claude, OpenClaw, and compatible chat runtimes. It keeps the audible grunt prefix decorative while preserving factual, safety, and technical meaning in the parenthetical content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes visible answer formatting while active, which can obscure normal prose structure if a user is not expecting roleplay.

Mitigation: Use it only when Bangboo-style responses are desired, and honor explicit requests to stop roleplay.

Risk: Optional project-memory setup could expose unrelated private content if users add more than the intended lexicon.

Mitigation: Limit project memory or knowledge uploads to the included Bangboo reference lexicon.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songkey/skills/bangboo-voice)
- [README](artifact/README.md)
- [Integration guide](artifact/docs/integration.md)
- [Bangboo voice skill definition](artifact/SKILL.md)
- [Bangboo reference lexicon](artifact/.cursor/skills/bangboo-voice/reference-lexicon.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown text with Bangboo-style grunt openers and parenthetical meaning; code blocks, tables, and long content remain standard Markdown after a short opener.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visible response formatting changes while the skill is active; optional strict Chinese mode depends on the included lexicon.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
