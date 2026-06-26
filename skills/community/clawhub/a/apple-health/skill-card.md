## Description: <br>
Connect agents to Apple Health exports with MCP setup, schema validation, and privacy-safe analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users configuring agent access to exported Apple Health CSV data use this skill to validate local exports, wire the Apple Health MCP server, discover schemas, and run bounded health queries without exposing raw health records by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Apple Health exports and query summaries may contain sensitive personal health information. <br>
Mitigation: Point HEALTH_DATA_DIR only at the intended local export folder, prefer bounded summary queries, avoid raw-row output unless explicitly needed, and review or delete ~/apple-health when no longer needed. <br>
Risk: The workflow relies on a third-party MCP package and whichever MCP client receives the query results. <br>
Mitigation: Install and run the MCP package only when the user trusts the package and client, and keep health CSV rows local unless the user explicitly asks to share them. <br>
Risk: Analysis can be misleading when the Apple Health export is stale. <br>
Mitigation: Track the last export timestamp and request a fresh iPhone export before presenting current-day or latest trend conclusions. <br>


## Reference(s): <br>
- [ClawHub Apple Health release](https://clawhub.ai/ivangdavila/apple-health) <br>
- [Skill homepage](https://clawic.com/skills/apple-health) <br>
- [npm package registry](https://registry.npmjs.org) <br>
- [Fallback healthkit-sync skill](https://raw.githubusercontent.com/openclaw/skills/main/skills/mneves75/healthkit-sync/SKILL.md) <br>
- [Fallback apple-watch skill](https://raw.githubusercontent.com/openclaw/skills/main/skills/lainnet-42/apple-watch/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with JSON configuration snippets, shell commands, and SQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should use local export paths, explicit date windows, visible units, and schema-confirmed table names.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
