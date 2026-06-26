## Description: <br>
Feishu/Lark bot operations guidance for the Hermes Agent lifecycle, covering deployment, debugging, @mention behavior, bot-to-bot messaging, dropped messages, session mix-ups, WebSocket stability, authentication issues, and interactive card callbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[femi-ronvue](https://clawhub.ai/user/femi-ronvue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who administer Hermes Feishu/Lark bots use this skill to diagnose outages, tune gateway configuration, verify Feishu API behavior, repair @mention handling, and recover bot connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recovery commands can disrupt a live Hermes Feishu bot by killing gateway processes, clearing locks, or changing runtime configuration. <br>
Mitigation: Review the recovery script before execution, back up .env and config.yaml, prefer targeted allowlist or configuration fixes, and use a maintenance window for disruptive restarts. <br>
Risk: Broad access-control settings such as GATEWAY_ALLOW_ALL_USERS=true or permissive bot-to-bot options can weaken who may interact with the bot. <br>
Mitigation: Use the broad settings only for diagnosis when necessary, return to targeted allowlists or mention-only behavior, and confirm effective access after restart. <br>
Risk: Feishu app secrets and tenant tokens used during API diagnostics can be exposed through shell history, logs, or copied command output. <br>
Mitigation: Protect .env files, redact tokens before sharing logs, avoid persisting secrets in command history, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/femi-ronvue/feishu-bot-ops) <br>
- [AT_MAP code patch reference](references/at-mention-code-fix.md) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Lark tenant access token endpoint](https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu message API endpoint](https://open.feishu.cn/open-apis/im/v1/messages/<message_id>) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash, YAML, Python, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes diagnostic sequences, recovery commands, configuration values, and verification checklists.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
