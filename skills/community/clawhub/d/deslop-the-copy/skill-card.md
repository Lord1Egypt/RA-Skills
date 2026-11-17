## Description:

Deslop, humanize, edit, or audit AI-sounding, robotic, generic, corporate, or ChatGPT-like copy while preserving the writer's voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyzer](https://clawhub.ai/user/skyzer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to edit or audit AI-sounding prose while preserving the writer's meaning, factual claims, formality, and voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Aggressive style rules may over-edit intentional voice, formatting, or punctuation.

Mitigation: Review rewritten text against the source for preserved meaning, factual claims, formality, and voice; use detection mode when findings are needed without rewriting.

Risk: The zero-em-dash rule can alter quoted evidence in detection reports.

Mitigation: Render any source em dash as [em dash] in quotations and verify the finding still reflects the original text.

## Reference(s):

- [Deslop evaluation](references/eval.md)
- [ClawHub skill page](https://clawhub.ai/skyzer/skills/deslop-the-copy)
- [Wikipedia WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup)
- [Wikipedia Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown, depending on whether the user requests an edit or a detection report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Edit mode returns only cleaned text unless commentary is requested; detection mode names patterns, quotes evidence, and gives concise fixes.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
