## Description: <br>
Install and connect cogmem as a durable memory backend for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuqin164](https://clawhub.ai/user/liuqin164) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, configure, migrate, and wire cogmem as durable memory for OpenClaw workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make cogmem a durable memory layer that captures and reuses sensitive conversation and workspace memory. <br>
Mitigation: Enable it only when durable memory is intended, review imported profile and session files first, and avoid the automatic wrapper until future turn capture is acceptable. <br>
Risk: Memory import or recall may include more historical context than a user expects. <br>
Mitigation: Run the dry-run import before migration and inspect source-level import scope before writing records. <br>
Risk: Installing from an unpinned source can change behavior as the upstream package changes. <br>
Mitigation: Pin a specific commit for installation when stability or reviewability matters. <br>


## Reference(s): <br>
- [Cogmem Memory on ClawHub](https://clawhub.ai/liuqin164/cogmem) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell, TOML, TypeScript, and text code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, migration, runtime wiring, debug, service, and MCP bridge guidance.] <br>

## Skill Version(s): <br>
2.5.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
