## Description:

Generate, patch, read, and compress HTML pages for reports, dashboards, and docs with fast AI-agent speed and precise CSS selector updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xdnaimino](https://clawhub.ai/user/xdnaimino)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this MCP server to create, inspect, patch, and compress HTML reports, dashboards, docs, email-ready pages, and other structured pages instead of long markdown outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact tells users to run an unpinned external MCP package whose executable is not included in the reviewed artifact.

Mitigation: Prefer a reconciled, exact npm version with a known reviewed package, and avoid dynamic npx resolution in MCP client startup.

Risk: Generated HTML and email-ready output may be written or sent outside the expected location or workflow.

Mitigation: Run the server with limited filesystem, environment, and network access, and do not process secrets or regulated data unless output destinations are understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xdnaimino/skills/fast-html-mcp)
- [NPM package](https://www.npmjs.com/package/@aimino/opentalk2html-notmd)
- [Bundled README](references/README.md)
- [MCP server manifest](references/server.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell examples; generated agent artifacts are HTML pages or compressed HTML summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write, read, patch, format, preview, or compress HTML files through MCP tools.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
