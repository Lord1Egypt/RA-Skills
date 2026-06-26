## Description: <br>
Use this when a user wants to search Daiso/다이소, convenience stores/편의점, marts, Olive Young/올리브영, Megabox/메가박스, Lotte Cinema/롯데시네마, or CGV data through the Daiso project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hmmhmmhm](https://clawhub.ai/user/hmmhmmhm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to choose and run Daiso CLI or MCP workflows for Korean retail, convenience store, mart, Olive Young, and cinema search tasks, including products, stores, inventory, movies, showtimes, seats, health checks, and JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide workflows that access live external retail and cinema services, so results such as stock, prices, showtimes, and seat counts may change. <br>
Mitigation: Tell users when data comes from live services, preserve the command used, and rerun or narrow queries when freshness matters. <br>
Risk: The CLI requires an environment that can run npx and may access networked services. <br>
Mitigation: Run health checks before use, review commands before execution, and provide the MCP URL or equivalent API path when the local CLI cannot run. <br>
Risk: Administrative or credentialed environments may expose repository, GitHub CLI, Convex, or moderator/admin access to workflows. <br>
Mitigation: Use least-privilege credentials, review commands before write actions, and install only when comfortable granting the workflow that level of access. <br>


## Reference(s): <br>
- [Daiso CLI Command Map](references/cli-command-map.md) <br>
- [Daiso MCP Homepage](https://github.com/hmmhmmhm/daiso-mcp) <br>
- [Daiso MCP Endpoint](https://mcp.aka.page) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves product IDs, store codes, theater codes, movie codes, and notes that live external data may change.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
