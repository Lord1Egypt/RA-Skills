## Description:

Audit personal or brand sites for AI agent discoverability and fix structured data, trust anchor pages, llms.txt, crawlability checks, and Ghost-specific deployment patterns where the evidence supports action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[highnoonoffice](https://clawhub.ai/user/highnoonoffice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and agent operators use this skill to assess and improve how AI agents understand personal, brand, or Ghost Pro sites. It guides audits, CMS-level fixes, structured handoffs for repository changes, and post-change verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may use Ghost Admin credentials or a dedicated Ghost staff browser session to publish pages, append JSON-LD, or configure redirects.

Mitigation: Use a dedicated staff account, approve public copy before publication, and confirm changes are limited to the intended site.

Risk: Generated public pages or structured data could be inaccurate if the site owner does not review the proposed content.

Mitigation: Review exact copy and schema values before publishing, then verify each live change with the skill's documented checks.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/highnoonoffice/skills/agent-ready)
- [Project homepage](https://github.com/highnoonoffice/hno-skills)
- [Ora scoring guide](references/ora-scoring-guide.md)
- [Ghost deployment reference](references/ghost-deployment.md)
- [JSON-LD templates](references/json-ld-templates.md)
- [llms.txt templates](references/llms-txt-templates.md)
- [Coding agent handoffs](references/codex-handoffs.md)
- [Verification commands](references/verification-commands.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON-LD examples, llms.txt templates, and structured agent handoff blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for review before execution and include verification steps for live site changes.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
