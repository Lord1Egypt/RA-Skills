## Description: <br>
Search, install, and export agentars from the CatchClaw marketplace. Use when the user wants to find, install, or package agent templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aLIEzu](https://clawhub.ai/user/aLIEzu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search the CatchClaw marketplace, install selected agentars, export local agents as ZIP packages, and roll back overwritten workspaces when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing untrusted agentars can introduce unsafe workspace content. <br>
Mitigation: Install only agentars you trust and review installed files before relying on them. <br>
Risk: Overwrite installs can replace the main OpenClaw workspace. <br>
Mitigation: Prefer installing as a new agent, require explicit user selection before overwrite, and use rollback backups when needed. <br>
Risk: Using --api-key creates a local plaintext credential file. <br>
Mitigation: Use --api-key only when required, protect the generated credentials file, and remove it when it is no longer needed. <br>
Risk: Exported ZIPs may contain sensitive local content, especially when memory is included. <br>
Mitigation: Keep MEMORY.md excluded unless explicitly requested and review exported ZIPs before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aLIEzu/catchclaw-bak) <br>
- [CatchClaw homepage](https://github.com/OpenAgentar/catchclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline CLI commands and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled CLI may create local workspace files, credential files, backups, and export ZIPs after the user confirms the relevant action.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
