## Description: <br>
Anti-detection browser automation MCP skill for OpenClaw agents with tools for navigation, interaction, extraction, downloads, profiles, sessions, and stealth web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redf0x1](https://clawhub.ai/user/redf0x1) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw agents to a local CamoFox MCP server for authorized browser automation, content extraction, session/profile handling, downloads, and stealth search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stealth browser automation can be misused or applied to systems without authorization. <br>
Mitigation: Install and use only for systems the operator is authorized to automate. <br>
Risk: The packaged setup pins camofox-mcp 1.10.0 while security evidence recommends a newer runtime. <br>
Mitigation: Prefer upgrading the runtime to camofox-mcp 1.13.2 or newer before deployment. <br>
Risk: The MCP endpoint can expose sensitive browser, session, file, and download actions. <br>
Mitigation: Keep the endpoint bound to localhost or otherwise authenticated, use disposable profiles, avoid personal or production cookies, and require explicit confirmation before submissions, bulk actions, downloads, or deletions. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/redf0x1/camofox-mcp) <br>
- [CamoFox MCP homepage](https://github.com/redf0x1/camofox-mcp#readme) <br>
- [SKILL.md](SKILL.md) <br>
- [manifest.yaml](manifest.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke an HTTP MCP server that returns browser snapshots, screenshots, file metadata/content, and browser action results.] <br>

## Skill Version(s): <br>
1.10.0 (source: frontmatter, manifest.yaml, changelog released 2026-02-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
