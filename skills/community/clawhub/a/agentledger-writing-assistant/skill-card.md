## Description:

AI writing partner for solopreneurs and content creators that drafts, edits, and improves emails, blog posts, newsletters, social captions, and reports while maintaining the user's voice, adapting to format and audience, and integrating with content-calendar, inbox-triage, and solopreneur-assistant skills.

This skill is for research and development only.

## Publisher:

[clawdssen](https://clawhub.ai/user/clawdssen)

### License/Terms of Use:

CC-BY-NC-4.0

## Use Case:

Solopreneurs, content creators, and developers use this skill to have an agent draft, edit, repurpose, and improve written content while matching a local voice profile and target audience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent AGENTS.md and HEARTBEAT.md snippets can change future agent writing behavior.

Mitigation: Review those snippets before installation and keep only the standing behavior the user explicitly wants.

Risk: writing-state.md and generated drafts may contain client names, business details, proprietary style preferences, or other sensitive information.

Mitigation: Store writing-state.md and drafts locally and keep them out of public repositories.

Risk: Generated emails, posts, newsletters, and reports may contain inaccurate, unsuitable, or unapproved content.

Mitigation: Require human review before any draft is sent or published.

## Reference(s):

- [Writing Assistant Advanced Patterns](artifact/references/advanced-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/clawdssen/skills/agentledger-writing-assistant)
- [The Agent Ledger](https://theagentledger.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown, prose drafts, editing notes, and setup snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on local writing-state.md preferences and user-supplied draft content.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
