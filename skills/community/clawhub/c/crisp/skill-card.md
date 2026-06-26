## Description: <br>
Customer support via Crisp API. Use when the user asks to check, read, search, or respond to Crisp inbox messages. Requires Crisp website ID and plugin token (authenticated via environment variables CRISP_WEBSITE_ID, CRISP_TOKEN_ID, and CRISP_TOKEN_KEY). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-phan](https://clawhub.ai/user/paul-phan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Support teams and operators use this skill to let an agent inspect Crisp inbox state, read and search customer conversations, draft or send replies, mark messages read, and resolve conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent real read/write access to live Crisp customer conversations. <br>
Mitigation: Install only for workflows that require Crisp inbox access, use the narrowest viable token scopes, and keep credentials in a trusted environment. <br>
Risk: Agent replies or conversation-state changes could affect customer communications. <br>
Mitigation: Require explicit human approval before sending customer replies, marking conversations read, or resolving conversations. <br>


## Reference(s): <br>
- [Crisp REST API Reference](references/api.md) <br>
- [Crisp API](https://api.crisp.chat) <br>
- [Crisp Marketplace](https://marketplace.crisp.chat/) <br>
- [ClawHub Skill Page](https://clawhub.ai/paul-phan/crisp) <br>
- [Publisher Profile](https://clawhub.ai/user/paul-phan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can perform authenticated Crisp API read/write actions when the required environment variables are set.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
