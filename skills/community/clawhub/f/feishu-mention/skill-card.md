## Description: <br>
Converts Feishu/Lark @mentions in message text into Feishu-compatible <at> XML tags using OpenClaw account configuration, bot discovery, aliases, and group-member lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helong0911-alt](https://clawhub.ai/user/helong0911-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill before sending Feishu/Lark messages that contain @mentions, so raw mention text is converted into notification-capable Feishu <at> tags. It supports configured bot mentions, optional user aliases, and group-member resolution through Feishu APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Feishu credentials and cached identity mappings can expose sensitive workspace data if shared. <br>
Mitigation: Keep openclaw.json, appSecret values, cache files, and debug logs private; redact them before sharing support material or logs. <br>
Risk: @all or sensitive mentions may notify more recipients than intended. <br>
Mitigation: Review resolved messages containing @all or sensitive names before sending them to Feishu/Lark. <br>
Risk: Mention resolution depends on Feishu bot permissions, group membership, and cache freshness. <br>
Mitigation: Confirm the configured bot has the required Feishu permissions and clear the local mention cache when account or group membership changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/helong0911-alt/feishu-mention) <br>
- [README.md](README.md) <br>
- [QUICKSTART.md](QUICKSTART.md) <br>
- [FEISHU_MESSAGE_FORMAT.md](FEISHU_MESSAGE_FORMAT.md) <br>
- [integration.md](integration.md) <br>
- [Feishu bot info OpenAPI endpoint](https://open.feishu.cn/open-apis/bot/v3/info) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration guidance] <br>
**Output Format:** [String containing Feishu/Lark message text with <at user_id="...">name</at> XML tags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires text, accountId, and chatId inputs; unresolved mentions are preserved as original text.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
