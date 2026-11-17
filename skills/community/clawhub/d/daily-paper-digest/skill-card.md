## Description:

Daily Paper Digest aggregates recent AI papers from arXiv and Hugging Face and formats them for delivery to chat applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qjymary](https://clawhub.ai/user/qjymary)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and OpenClaw users use this skill to collect daily AI paper updates, filter them by configurable topics, and produce a formatted digest for chat delivery or scheduled review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes scheduled outbound requests to arXiv and Hugging Face paper sources.

Mitigation: Prefer explicit slash-command or scheduled activation and restrict network egress to the documented paper sources.

Risk: Pinned dependencies may need maintenance before production deployment.

Mitigation: Review and update pinned Python dependencies before production use.

Risk: The Hugging Face detail helper can fetch a caller-provided paper URL if exposed as a callable tool.

Mitigation: Remove that helper from exposed tool surfaces or validate allowed URLs before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qjymary/skills/daily-paper-digest)
- [Hugging Face Papers](https://huggingface.co/papers)
- [arXiv Category Taxonomy](https://arxiv.org/category_taxonomy)
- [OpenClaw metadata homepage](https://github.com/your-username/daily-paper-digest)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Formatted text digest with paper titles, authors, abstracts, source links, and source counts; documentation includes Markdown and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are configurable through JSON source and filter settings and are intended for Chinese-language chat delivery.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
