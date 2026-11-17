## Description:

Check brand name safety across domains, social handles, trademarks, app stores, and SaaS channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brndmk](https://clawhub.ai/user/brndmk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check proposed brand names before launch across domains, social handles, trademarks, app stores, search presence, package registries, and SaaS channels. It helps compare candidates, assess safety risk, and produce JSON evidence reports for brand-review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned npm MCP server, so reviewed behavior may change when the package changes.

Mitigation: Pin `brandomica-mcp-server` to a reviewed version and use package integrity or provenance checks before installation.

Risk: The MCP server may run with the user agent's local permissions during brand checks.

Mitigation: Run it with only the workspace, network access, and credentials required for the specific brand-checking task.

Risk: Trademark, filing readiness, and conflict results can affect launch or legal decisions.

Mitigation: Treat outputs as decision-support evidence and have qualified reviewers confirm high-impact trademark or filing actions.

## Reference(s):

- [Brandomica homepage](https://www.brandomica.com)
- [Brandomica MCP server page](https://www.brandomica.com/mcp-server)
- [ClawHub skill page](https://clawhub.ai/brndmk/skills/brandomica)
- [Publisher profile](https://clawhub.ai/user/brndmk)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown or JSON summaries from MCP tool calls, including scores, verdicts, comparisons, availability data, and evidence reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Brand names must be lowercase alphanumeric with optional hyphens. Batch checks support 2-50 names according to the artifact documentation.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter, clawhub.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
