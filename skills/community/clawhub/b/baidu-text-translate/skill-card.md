## Description: <br>
Translate text through trans-cli with the Baidu Translation AI API, including JSON output, Baidu language codes, API key setup, diagnostics, and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-translate](https://clawhub.ai/user/baidu-translate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to translate text, diagnose trans-cli setup, choose Baidu-specific language codes, and recover from common Baidu Translation API errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Translated text is sent to Baidu through the external trans-cli package and Baidu Translation API. <br>
Mitigation: Install only if the external package and Baidu text processing are acceptable for the intended data, and avoid sending sensitive text unless approved. <br>
Risk: The skill requires a Baidu API key through TRANS_API_KEY or trans-cli configuration. <br>
Mitigation: Prefer a secure environment variable or secret manager; keep ~/.trans-cli/config.json permissions restrictive and rotate exposed keys. <br>
Risk: Baidu language codes differ from common ISO codes and can cause invalid-language failures. <br>
Mitigation: Use trans languages or the documented Baidu code table before issuing translation commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/baidu-translate/baidu-text-translate) <br>
- [Baidu Translate](https://fanyi.baidu.com) <br>
- [Baidu Translation Open Platform](https://fanyi-api.baidu.com/) <br>
- [Baidu Translation Developer Center](https://fanyi-api.baidu.com/manage/developer) <br>
- [Baidu Translation API Key Management](https://fanyi-api.baidu.com/manage/apiKey) <br>
- [Baidu Translation Account Recharge](https://fanyi-api.baidu.com/manage/account) <br>
- [Baidu Translation Usage Details](https://fanyi-api.baidu.com/api/trans/user/usage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide use of trans text --json, trans doctor --json, trans languages, and TRANS_API_KEY configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
