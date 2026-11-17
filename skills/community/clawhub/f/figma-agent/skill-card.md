## Description:

Figma MCP integration for OpenClaw that helps agents read Figma designs, inspect variables and Code Connect context, and create or edit Figma designs through structured workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rasimme](https://clawhub.ai/user/rasimme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agent operators use this skill to inspect Figma files, discover design-system variables, review screens, and perform controlled create or edit workflows with validation after writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow reads tokens from other local MCP clients and stores a bearer token in OpenClaw configuration with limited scoping and disclosure.

Mitigation: Run the bootstrap script with --dry-run first, verify the selected credential file, review ~/.openclaw/openclaw.json permissions, and remove or rotate the copied token when it is no longer needed.

Risk: Write workflows can modify Figma files and require access to an account with a Figma Full Seat.

Mitigation: Prefer a duplicate or branch for write workflows and validate every write with Figma metadata or screenshots before reporting completion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rasimme/skills/figma-agent)
- [Publisher Profile](https://clawhub.ai/user/rasimme)
- [Project Homepage](https://github.com/rasimme/figma-agent)
- [Figma Remote MCP Server](https://help.figma.com/hc/en-us/articles/32132100833559)
- [Figma MCP Endpoint](https://mcp.figma.com/mcp)
- [Workflow Selection](references/workflow-selection.md)
- [Core Rules](references/core-rules.md)
- [Prompting Patterns](references/prompting-patterns.md)
- [Figma API Reference](references/figma-api.md)
- [Plugin API Gotchas](references/plugin-api-gotchas.md)
- [Variable Discovery Playbook](references/playbooks/variable-discovery.md)
- [Design Audit Review Playbook](references/playbooks/design-audit-review.md)
- [Design System Cleanup Playbook](references/playbooks/design-system-cleanup.md)
- [Native Screen Generation Playbook](references/playbooks/native-screen-generation.md)
- [Screen Review Loop Playbook](references/playbooks/screen-review-loop.md)
- [Color Tokenization Playbook](references/playbooks/color-tokenization.md)
- [HTML-to-Figma Prototyping Playbook](references/playbooks/html-to-figma-prototyping.md)
- [Stitch Import Cleanup Playbook](references/playbooks/stitch-import-cleanup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, code snippets, file paths, and optional screenshot attachment references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write workflows require validation with Figma metadata or screenshots before reporting success.]

## Skill Version(s):

0.3.0 (source: server release evidence, package.json, CHANGELOG released 2026-04-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
