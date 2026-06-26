## Description: <br>
Work with Immich photo library via MCP (claw2immich) - search photos by people, dates, locations, albums, download assets via shared links, and handle multi-person search, CLIP smart search, and metadata queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoeRu](https://clawhub.ai/user/JoeRu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to let an agent search, browse, and retrieve photos from a self-hosted Immich library through the claw2immich MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Immich MCP access can expose private photo library content, people, locations, albums, and metadata. <br>
Mitigation: Install only when the claw2immich MCP server is trusted, prefer a read-only Immich profile or tool allowlist, and use a trusted local or TLS-protected MCP endpoint. <br>
Risk: Unauthenticated shared links can expose private photos outside the Immich account boundary. <br>
Mitigation: Require explicit user approval before creating or sending shared links, and prefer short-lived links or authenticated Immich links when possible. <br>


## Reference(s): <br>
- [claw2immich](https://github.com/JoeRu/claw2immich) <br>
- [Immich](https://immich.app) <br>
- [Immich API docs](https://immich.app/docs/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Immich asset links, thumbnail handling guidance, and MCP tool call patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
