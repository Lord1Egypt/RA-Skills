## Description:

Ensures AI output contains only the result, not the prompt. Use when writing code, documentation, or content where prompt instructions, rationale, or meta-commentary must not leak into the output. Applies to all file types to prevent phrases like "as requested", "per the prompt", or change announcements from appearing in generated content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation authors, and agents use this skill to keep generated code, documentation, and content free of prompt instructions, rationale, and meta-commentary. It is useful when output should be production-ready and self-contained.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to rewrite prompt-derived wording into cleaner standalone content, which can remove text that was intended to be preserved verbatim.

Mitigation: Review generated diffs and preserve prompt text only when the user explicitly requests verbatim transcription or when editing prompt and instruction artifacts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jhauga/skills/exclude-prompt-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance applied to generated files and agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable behavior; applies prompt-leakage checks across file types.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
