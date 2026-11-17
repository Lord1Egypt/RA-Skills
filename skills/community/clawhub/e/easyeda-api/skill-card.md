## Description:

EasyEDA Pro API skill for AI agents working with PCB design, schematic editing, footprint and symbol management, project operations, live EasyEDA debugging, and EasyEDA extension development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanranxiaoxi](https://clawhub.ai/user/yanranxiaoxi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and electronics engineers use this skill to look up EasyEDA APIs, generate or debug EasyEDA extension code, and optionally operate a running EasyEDA Pro session through a local bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local EasyEDA bridge can execute arbitrary EasyEDA code against connected projects without authentication or origin restrictions.

Mitigation: Start the bridge only when live EasyEDA control is intended, stop it after use, avoid untrusted browsing while it runs, and review generated code before execution.

Risk: Generated API calls can modify PCB, schematic, library, or project data in the active EasyEDA session.

Mitigation: Confirm the active EasyEDA window and project before execution, keep backups or versioned copies of important designs, and test destructive changes on non-production files first.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yanranxiaoxi/skills/easyeda-api)
- [Run API Gateway Extension](https://jlc-ext.com/item/oshwhub/run-api-gateway)
- [EasyEDA API Reference Index](references/_index.md)
- [EasyEDA API Quick Reference](references/_quick-reference.md)
- [EasyEDA Document Source Format](format/index.md)
- [AI Extension Development Guide](guide/how-to-start-for-ai.md)
- [Bridge Usage Guide](guide/invoke-apis.md)
- [Error Handling Guide](guide/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate EasyEDA JavaScript intended for execution in a connected EasyEDA Pro browser runtime.]

## Skill Version(s):

1.1.24 (source: server release metadata; artifact metadata reports 1.1.29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
