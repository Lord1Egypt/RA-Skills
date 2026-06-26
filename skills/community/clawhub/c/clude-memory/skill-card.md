## Description: <br>
Persistent memory for AI agents with semantic search, association graphs, dream cycles, local-first offline operation, and MCP runtime support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebbsssss](https://clawhub.ai/user/sebbsssss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to add persistent memory through Clude MCP tools, recall long-term context by meaning, and manage memory locally or through optional cloud sync. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored memories may include sensitive personal, project, or preference data. <br>
Mitigation: Prefer local mode for private work, avoid storing secrets or sensitive personal details, and periodically review or delete memories. <br>
Risk: Cloud mode can sync memory data outside the local machine. <br>
Mitigation: Use cloud mode only when portability is needed and the data is appropriate for external syncing. <br>
Risk: The installer uses npm and npx commands that can install packages and modify MCP configuration. <br>
Mitigation: Review installation commands and MCP configuration before running them in environments where package installation is allowed. <br>


## Reference(s): <br>
- [Clude Memory on ClawHub](https://clawhub.ai/sebbsssss/clude-memory) <br>
- [Clude](https://clude.io) <br>
- [clude-bot npm package](https://www.npmjs.com/package/clude-bot) <br>
- [cludebot source repository](https://github.com/sebbsssss/cludebot) <br>
- [Clude benchmark](https://clude.io/benchmark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON MCP configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide use of MCP memory tools and installation commands after user review.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
