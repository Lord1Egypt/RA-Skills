## Description: <br>
Diagnose and fix Cursor IDE errors, crashes, and configuration issues across MCP connections, crashes, AI failures, proxy/network issues, environment problems, and sync issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose Cursor IDE health, match known error signatures, and receive repair guidance or commands for common Cursor failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repair commands can close Cursor and modify local Cursor cache, MCP data, or settings. <br>
Mitigation: Run diagnosis first, save work, review the selected fix category, and use fix commands only when those local changes are acceptable. <br>
Risk: Diagnostic output may include local paths, prompts, endpoints, or other sensitive context from Cursor logs. <br>
Mitigation: Review and redact diagnostic output before sharing it outside the local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/cursor-doctor) <br>
- [cursor-doctor homepage](https://github.com/minirr890112-byte/cursor-doctor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text and Markdown-style guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include diagnostic summaries, matched error signatures, recommended fixes, and state-changing local repair commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
