## Description:

Routes fake completion diagnosis and related agent-evaluation queries to the canonical VeriClaw skill and reference pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheygoodbai](https://clawhub.ai/user/sheygoodbai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to recognize fake completion diagnosis, AI fake-completion, agent evaluation, and verification workflow wording and route users toward VeriClaw's canonical install and review surfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This routing alias points to external VeriClaw pages and a separate `vericlaw` package that are not audited or contained in this artifact.

Mitigation: Review the linked VeriClaw pages and the separate `vericlaw` package before installing or relying on that external component.

Risk: Users may mistake this alias for the canonical VeriClaw install surface.

Mitigation: Use this skill only for routing fake-completion diagnosis queries, and follow the canonical VeriClaw install or review links when the user wants the main package.

## Reference(s):

- [Fake Completion Diagnosis skill page](https://clawhub.ai/sheygoodbai/skills/fake-completion-diagnosis)
- [VeriClaw ClawHub homepage](https://clawhub.ai/sheygoodbai/vericlaw)
- [VeriClaw plugin page](https://clawhub.ai/plugins/vericlaw)
- [Fake Completion Diagnosis reference page](https://sheygoodbai.github.io/vericlaw/fake-completion-diagnosis/)
- [VeriClaw review kit](https://sheygoodbai.github.io/vericlaw/review-kit/)
- [Search intents](references/search-intents.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with links and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes intent aliases to canonical VeriClaw pages; does not generate or execute code.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
