## Description:

Translate text using Baidu AI Translation API via trans-cli with Baidu-specific language codes, API key management, error handling, and environment diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-translate](https://clawhub.ai/user/baidu-translate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to translate text with Baidu's trans-cli, diagnose API key and account readiness, choose Baidu-specific language codes, and respond to translation errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Translated text is sent to Baidu's external translation service.

Mitigation: Avoid translating secrets, credentials, private documents, or regulated data unless that data sharing has been approved.

Risk: The skill depends on installing and running the external @bdtrans/trans-cli npm package.

Mitigation: Review the npm package and version before installation, especially in sensitive environments.

Risk: The Baidu API key may be exposed through unsafe shell history, config files, or prompts.

Mitigation: Prefer TRANS_API_KEY or carefully managed config storage and do not paste credentials into translated text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baidu-translate/skills/baidu-text-translate)
- [Baidu Translate](https://fanyi.baidu.com)
- [Baidu Translation Open Platform](https://fanyi-api.baidu.com/)
- [Baidu Developer Center](https://fanyi-api.baidu.com/manage/developer)
- [Baidu API Key Management](https://fanyi-api.baidu.com/manage/apiKey)
- [Baidu Account Recharge](https://fanyi-api.baidu.com/manage/account)
- [Baidu Translation Usage Details](https://fanyi-api.baidu.com/api/trans/user/usage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on trans-cli JSON output, exit codes, language codes, API key setup, and environment diagnostics.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
