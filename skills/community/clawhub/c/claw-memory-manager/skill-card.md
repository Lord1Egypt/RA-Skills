## Description: <br>
Manage OpenClaw Agent memory features by enabling, disabling, checking, and tuning Dreaming memory consolidation and Active Memory injection with dry-run previews, backups, and optional gateway restarts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who run OpenClaw use this skill to configure built-in memory behavior without manually editing nested JSON. It helps preview, apply, verify, and roll out Dreaming or Active Memory settings across local and managed deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent OpenClaw memory configuration changes and restart the gateway. <br>
Mitigation: Use --dry-run first, review the planned JSON changes, and pass --no-restart when restart timing must be controlled. <br>
Risk: Active Memory can surface prior stored memories in future direct chats. <br>
Mitigation: Review memory contents before enabling Active Memory and use the conservative preset for sensitive work. <br>
Risk: Managed deployments may require synchronized config mirrors to survive restarts. <br>
Mitigation: Let the skill auto-detect mirror paths and verify the resulting runtime config after changes. <br>


## Reference(s): <br>
- [Feature Catalog - OpenClaw Agent Memory Features](references/features.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/songhonglei/claw-memory-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May apply persistent OpenClaw configuration changes and restart the gateway unless dry-run or no-restart flags are used.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
