## Description: <br>
Provides agent-facing setup, scripts, and JavaScript client examples for using ApiHz APIs for weather, earthquake data, IP lookup, temporary email, translation, and related services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lihuiyang-03](https://clawhub.ai/user/lihuiyang-03) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure ApiHz credentials, browse available API categories, call selected APIs interactively, and integrate ApiHz calls through a JavaScript client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API credentials can be exposed if users configure HTTP endpoints or send credentials in query strings. <br>
Mitigation: Use HTTPS-only APIHZ_BASE_URL and APIHZ_LIST_URL values, prefer POST requests, and review endpoint settings before running the scripts. <br>
Risk: The test report references a key value used with this version. <br>
Mitigation: Rotate any ApiHz key shown in the artifact or used during testing before production use. <br>
Risk: The automatic check-in script can make recurring credentialed account requests when scheduled. <br>
Mitigation: Enable cron scheduling only after approving that recurring account activity. <br>
Risk: Some provider APIs may process sensitive personal identifiers or network targets. <br>
Mitigation: Avoid sending sensitive personal data unless the data flow is approved, and use network testing features only on systems you are authorized to test. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lihuiyang-03/apihz-cn-skill) <br>
- [ApiHz registration and service site](https://www.apihz.cn/?shareid=10013679) <br>
- [ApiHz GET/POST usage documentation](https://www.apihz.cn/template/miuu/getpost.php) <br>
- [ApiHz preferred endpoint lookup](https://api.apihz.cn/getapi.php) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in local credential configuration, API cache files, and outbound ApiHz API requests when the documented scripts are run.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
