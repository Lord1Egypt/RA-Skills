## Description:

Humanize AI-generated text by detecting common LLM writing patterns, analyzing statistical style signals, and suggesting rewrites that sound natural, specific, and human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sp012lk](https://clawhub.ai/user/sp012lk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and writing editors use this skill to detect AI-sounding patterns in drafts, receive analysis reports or suggestions, and rewrite text while preserving the core meaning and intended tone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be used to misrepresent who wrote a piece of text or to hide AI assistance where disclosure is required.

Mitigation: Use the skill for editing clarity and removing boilerplate, and follow academic integrity, employment, platform, legal, or disclosure rules that apply to the writing.

Risk: Always-on rewriting guidance can change shared agents' writing behavior without users realizing style rewriting is active.

Mitigation: Enable always-on use only in contexts where users are told that writing may be rewritten for human-like style.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sp012lk/skills/ai-humanizer-bak)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Copyleaks stylometric fingerprint research](https://arxiv.org/abs/2503.01659)
- [blader/humanizer reference project](https://github.com/blader/humanizer)
- [OpenClaw](https://github.com/nichochar/openclaw)
- [Pattern documentation](references/patterns.md)
- [AI vocabulary reference](references/ai-vocabulary.md)
- [Style guide reference](references/style-guide.md)
- [Examples](docs/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Plain text rewrites, markdown reports, and optional JSON analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline text analysis; may provide auto-fix suggestions when requested.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
