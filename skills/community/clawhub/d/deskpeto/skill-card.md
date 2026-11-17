## Description:

DeskPeto helps an agent guide users through creating, previewing, installing, and troubleshooting AI desktop pet packages from DeskPeto, including in-chat animated pet cards, one-command desktop installation, MCP connection setup, and free shared-gallery pet installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juntook](https://clawhub.ai/user/juntook)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create or install DeskPeto desktop pets, connect DeskPeto MCP, summon animated pet cards in supported hosts, and troubleshoot pet package installation. The skill also helps users understand when remote installer commands, tokens, and host configuration changes need review before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installer commands can change host configuration and start an invisible background process.

Mitigation: Install only after user consent, prefer manual zip installation for static pet assets when practical, and review or back up host configuration before allowing hook changes.

Risk: Reusable tokens or signed URLs may be exposed if pasted into chat, logs, or URLs.

Mitigation: Avoid sharing reusable tokens in chat or URLs where possible, use device-code authorization when supported, and refresh expired one-hour links from DeskPeto instead of reusing old links.

## Reference(s):

- [DeskPeto website](https://deskpeto.com)
- [DeskPeto installation guide](https://deskpeto.com/guide)
- [DeskPeto shared gallery](https://deskpeto.com/shared)
- [DeskPeto MCP connection page](https://mcp.deskpeto.com/mcp/connect)
- [Pet page HTML template](references/pet-page.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and an HTML template adaptation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include time-limited installer or sprite URLs supplied by the user or DeskPeto tools.]

## Skill Version(s):

0.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
