## Description:

AI Skill for building EasyEDA Pro extension plugins, including plugin code generation, API querying, extension.json configuration, i18n localization, and optional debugging workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonyang170](https://clawhub.ai/user/jasonyang170)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, modify, build, and debug EasyEDA Pro extension plugins while checking EasyEDA API signatures and runtime constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional MCP debugging can preserve EasyEDA browser login state and cached console logs.

Mitigation: Use the debugging workflow only in an isolated development workspace, avoid shared machines, and clear MCP browser data and console logs after debugging.

Risk: Setup and build workflows may run npm commands and import generated plugins into a live EasyEDA browser session.

Mitigation: Review dependencies first and require explicit confirmation before importing plugins or using cached login state with a real EasyEDA account.

## Reference(s):

- [EasyEDA Pro API Complete Reference](artifact/resources/api-reference.md)
- [Common Pitfalls and Lessons Learned](artifact/resources/experience.md)
- [EasyEDA Pro API SDK](https://github.com/easyeda/pro-api-sdk.git)
- [extension-dev-mcp-tools](https://github.com/easyeda/extension-dev-mcp-tools)

## Skill Output:

**Output Type(s):** [Analysis, Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with TypeScript, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce EasyEDA Pro plugin project files, extension.json configuration, i18n files, build commands, and debugging guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter metadata version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
