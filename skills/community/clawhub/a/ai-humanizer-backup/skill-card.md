## Description:

Humanize AI-generated text by detecting common LLM writing patterns, statistical style signals, and suspicious vocabulary, then rewrite or report on the text in a more natural voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wings229](https://clawhub.ai/user/wings229)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agents use this skill to score drafts for AI-writing patterns, get specific improvement guidance, and produce humanized rewrites while preserving the original meaning and intended tone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be used to misrepresent authorship or bypass school, workplace, publishing, or compliance rules.

Mitigation: Use it as editing support and disclose AI assistance where policy or context requires it.

Risk: AI-writing scores are heuristic style feedback and may produce false positives or false negatives.

Mitigation: Treat scores as review signals, not as proof of authorship, and have a human reviewer make final decisions.

Risk: Interactive terminal output from untrusted text could be confusing or unsafe to consume directly.

Mitigation: Prefer JSON or otherwise sanitized output handling when processing untrusted input through the CLI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wings229/skills/ai-humanizer-backup)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Copyleaks stylometric research](https://arxiv.org/abs/2503.01659)
- [AI vocabulary reference](references/ai-vocabulary.md)
- [Pattern reference](references/patterns.md)
- [Style guide](references/style-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance, shell commands]

**Output Format:** [Human-facing text or Markdown, with optional JSON analysis and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-likeness scores, pattern findings, statistics, suggestions, and auto-fix rewrites.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
