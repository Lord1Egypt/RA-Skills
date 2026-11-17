## Description:

Humanizes AI-generated text by detecting common LLM writing patterns, scoring text with statistical indicators, and producing natural rewrite suggestions or safe auto-fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wings229](https://clawhub.ai/user/wings229)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agents use this skill to review drafts for AI-writing signals, generate concise issue reports, and rewrite text so it sounds more natural while preserving the core meaning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Developer installation can trust third-party dependencies and parent-directory lint configuration.

Mitigation: Review before installing as a standalone project; regenerate dependencies from a trusted registry and remove or audit the parent-directory ESLint import before running npm install, lint, or check.

Risk: Always-on guidance can persistently change agent writing behavior.

Mitigation: Apply always-on prompt changes only where the desired writing style is approved, and review outputs for tone, accuracy, and preservation of the user's intended meaning.

Risk: Humanization guidance could be misused to hide required AI disclosure or invent personal experience.

Mitigation: Use the skill for style editing only; preserve required AI-use disclosures and do not add fabricated first-person claims, facts, or experiences.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wings229/skills/ai-humanizer-local)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Copyleaks stylistic fingerprint research](https://arxiv.org/abs/2503.01659)
- [blader/humanizer](https://github.com/blader/humanizer)
- [OpenClaw](https://github.com/nichochar/openclaw)
- [Pattern documentation](docs/PATTERNS.md)
- [Real-world before/after examples](docs/EXAMPLES.md)
- [AI vocabulary reference](references/ai-vocabulary.md)
- [Human writing style guide](references/style-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Plain text, Markdown reports, JSON analysis, and CLI-oriented shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores text from 0-100, groups findings by priority, and may include auto-fixed text for safe mechanical edits.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
