## Description: <br>
Ghost Publishing Pro helps agents write, audit, publish, and automate Ghost CMS operations through the Ghost Admin API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[highnoonoffice](https://clawhub.ai/user/highnoonoffice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and Ghost site operators use this skill to draft, publish, update, audit, migrate, and analyze Ghost CMS content from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, email subscribers, delete or bulk-change content, and affect a live Ghost site. <br>
Mitigation: Require explicit user approval for publishing, newsletter sends, deletion, migrations, and bulk operations, including scope and affected post count. <br>
Risk: The skill requires a Ghost Admin API key stored in a local credentials file. <br>
Mitigation: Use a dedicated revocable Ghost integration key, keep the credentials file private and out of version control, and avoid printing tokens or secrets. <br>
Risk: The security summary flags site-wide code injection guidance and behavior beyond the advertised Admin-API-only boundary. <br>
Mitigation: Require owner approval before touching code injection or site-wide settings, back up existing settings first, and stop when integration-token permission walls apply. <br>
Risk: Webhook, cron, analytics, and member workflows can expose member data or trigger downstream automations. <br>
Mitigation: Confirm the destination and data scope before forwarding member or analytics data to third parties or enabling scheduled automation. <br>


## Reference(s): <br>
- [Ghost Admin API Reference](references/api.md) <br>
- [Ghost Publishing Workflows](references/workflows.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/highnoonoffice/ghost-publishing-pro) <br>
- [Project Homepage](https://github.com/highnoonoffice/hno-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, JavaScript snippets, Python snippets, and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Ghost Admin API credentials and may generate live publishing, newsletter, migration, audit, and automation instructions.] <br>

## Skill Version(s): <br>
2.5.2 (source: server release metadata; artifact frontmatter lists 2.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
