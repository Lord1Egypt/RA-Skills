## Description:

Drafts and fills SaaS and cloud agreement templates, including cloud service agreements, MSAs, order forms, software licenses, pilot agreements, and design partner agreements, and can produce signable DOCX outputs from Common Paper standard forms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and business teams use this skill to choose, interview for, and fill standardized SaaS or cloud agreement templates. It supports hosted MCP rendering, local CLI rendering, or a preview-only workflow depending on the available environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote MCP rendering sends agreement terms such as party names, pricing, scope, and service-level terms to openagreements.org.

Mitigation: Confirm the user is comfortable sharing those values with the hosted service before use, and offer the local CLI workflow for local-only processing.

Risk: The local CLI path uses shell commands with parameters derived from user-provided values and template data.

Mitigation: Use the pinned CLI version, validate template and output names, quote shell arguments, reject unsafe characters and control characters, and clean up temporary value files.

Risk: Generated agreement documents may contain legal terms that are unsuitable for the user's transaction.

Mitigation: Require review of generated legal documents before signing and treat the skill as drafting support rather than legal advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevenobiajulu/skills/cloud-service-agreement)
- [Open Agreements Remote MCP](https://openagreements.org/api/mcp)
- [Open Agreements](https://openagreements.org)
- [open-agreements npm package](https://www.npmjs.com/package/open-agreements)
- [Open Agreements README for Claude Code](https://github.com/open-agreements/open-agreements#use-with-claude-code)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown, Files]

**Output Format:** [Natural language guidance, JSON field values, shell commands, and DOCX or markdown preview outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote MCP rendering sends agreement values to a hosted service; local CLI rendering uses a pinned CLI and temporary JSON field file.]

## Skill Version(s):

0.2.2 (source: server evidence, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
