## Description: <br>
Provides OpenClaw agents with permission checks, audit logging, memory management, versioning, auto-organization, suggestions, and knowledge graph tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abcd784253626](https://clawhub.ai/user/abcd784253626) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to add permission-gated tool execution and managed memory workflows to agents, including storage, recall, updates, version history, automatic organization, and permission checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports auto-loaded memory tools, under-scoped subprocess behavior, remote embedding, and permissive approval behavior. <br>
Mitigation: Review auto-loaded tools and defaults before installation, disable trusted-session auto-approval for write actions, and keep auto-organization in dry-run mode until reviewed. <br>
Risk: Remote embedding can transfer memory or other sensitive content to a third-party service when configured. <br>
Mitigation: Avoid setting the OpenViking API key or embedding sensitive content unless third-party transfer is acceptable. <br>
Risk: Audit history may depend on working-directory memory/audit-log.md behavior. <br>
Mitigation: Check the audit-log path and retention behavior before relying on audit history. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abcd784253626/enhanced-permissions) <br>
- [README](artifact/README.md) <br>
- [Installation Guide](artifact/INSTALL-GUIDE.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and JavaScript examples, JSON configuration, and command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command-style tool responses and memory, versioning, organization, and permission-check results.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata, package.json, SKILL.md, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
