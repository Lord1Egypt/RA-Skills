## Description:

EAI Awesome Work helps generate a weekly Chinese Markdown digest of embodied AI and robotics papers from arXiv cs.RO, with themed sections, translated abstracts, contribution summaries, trend insights, and optional industry news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessy-huang](https://clawhub.ai/user/jessy-huang)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and technical editors use this skill to produce a structured Chinese newsletter that summarizes recent embodied AI and robotics papers, organizes them by theme, and adds editorial trend commentary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may activate the skill when the user only mentions a related newsletter or paper roundup casually.

Mitigation: Invoke the skill with explicit requests for an EAI Awesome Work or embodied AI weekly roundup, and adjust triggers before deployment if accidental activation is a concern.

Risk: The fixed footer can list sources that were not actually used in a generated issue.

Mitigation: Review the footer before publishing and keep only the sources that were actually consulted for that issue.

## Reference(s):

- [EAI Awesome Work writing template](references/template.md)
- [arXiv cs.RO new submissions](https://arxiv.org/list/cs.RO/new)
- [arXiv cs.RO June 2026 archive](https://arxiv.org/list/cs.RO/2026-06)
- [ClawHub skill page](https://clawhub.ai/jessy-huang/skills/eai-awesome-work)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a dated newsletter file named Awesome_EmbodiedAI_工作速递_YYYYMMDD.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
