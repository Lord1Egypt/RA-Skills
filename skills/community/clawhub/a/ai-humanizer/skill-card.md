## Description:

Humanizer detects common AI-writing patterns, scores text for AI-like signals, and suggests or applies edits that make drafts sound more natural and specific.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandonwise](https://clawhub.ai/user/brandonwise)

### License/Terms of Use:

MIT

## Use Case:

Writers, editors, and developers use this skill to review drafts for AI-like wording, statistical uniformity, chatbot artifacts, and filler patterns, then receive concrete suggestions or rewritten text. It can also provide CLI-based analysis reports and prompt-style guidance for agents that should avoid generic AI writing habits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be used to mask AI authorship signals in contexts where authorship transparency matters.

Mitigation: Use it only for appropriate editing and avoid using it to conceal AI involvement in schoolwork, hiring materials, compliance filings, legal documents, or similar high-stakes contexts.

Risk: Always-on prompt templates can create persistent style behavior in an agent.

Mitigation: Enable always-on guidance only when a persistent writing policy is intended and document how to remove or override it.

Risk: The security guidance reports a terminal-output safety issue for untrusted analyzed text.

Mitigation: Prefer JSON output or a cautious terminal environment when analyzing untrusted text until terminal-control escaping is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brandonwise/skills/ai-humanizer)
- [AI writing patterns reference](references/patterns.md)
- [AI vocabulary reference](references/ai-vocabulary.md)
- [Human writing style guide](references/style-guide.md)
- [Usage examples](docs/EXAMPLES.md)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Copyleaks stylometric research](https://arxiv.org/abs/2503.01659)
- [blader/humanizer](https://github.com/blader/humanizer)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text rewrites and suggestions, Markdown reports, JSON analysis, and CLI commands or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can score text from stdin or files, produce reports, group suggestions by priority, and apply limited automatic fixes.]

## Skill Version(s):

2.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
