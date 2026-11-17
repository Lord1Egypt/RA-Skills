## Description:

Rewrites Chinese, English, and Japanese text to reduce AI-like style by improving information density, evidence discipline, scenario fit, and template/fingerprint cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yamasite](https://clawhub.ai/user/yamasite)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, marketers, product teams, researchers, and support teams use this skill to diagnose and rewrite drafts for clearer information transfer, fewer template-style cues, and stricter citation discipline across Chinese, English, and Japanese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional scanner may be mistaken for an AI detector.

Mitigation: Treat scanner output only as style-lint hints and do not use it as proof of authorship.

Risk: The optional scanner reads local text and can print matched context snippets or write a local summary log.

Mitigation: Run it only on intended files, avoid sensitive text unless appropriate, and use --logfile only when a local log is desired.

Risk: Rewriting can accidentally preserve or introduce unsupported claims, vague evidence, or fabricated citations.

Mitigation: Apply the skill's hallucination and citation-verification gates; ask for sources or downgrade/remove unverifiable claims.

## Reference(s):

- [AI Flavor Principles](references/principles.md)
- [Citation Verification](references/citation-verification.md)
- [Chinese Rewrite Moves](references/zh.md)
- [English Rewrite Moves](references/en.md)
- [Japanese Rewrite Moves](references/ja.md)
- [Signs of AI Writing Mapping](references/signs-of-ai-writing.md)
- [Model and Platform Tells](references/model-tells.md)
- [Wikipedia: Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Fake Citation Checker](https://www.aidetectors.io/blog/fake-citation-checker)
- [Hallucinator Citation Verification Tool](https://github.com/gianlucasb/hallucinator)
- [Claude System Prompt Release Notes](https://docs.claude.com/en/release-notes/system-prompts)
- [Claude Prompt Engineering Best Practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- [GLM Model Documentation](https://docs.bigmodel.cn/cn/guide/models/text/glm-4.7)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with rewritten draft, change notes, follow-up questions, and optional local style-lint report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional scanner is a heuristic linter for style fingerprints, not proof of AI authorship.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
