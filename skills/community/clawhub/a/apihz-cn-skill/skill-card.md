## Description:

ApiHz API client skill for accessing 409+ service endpoints, including weather, earthquake data, IP geolocation, temporary email, translation, timestamp, ICP, ping, and exchange-rate APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lihuiyang-03](https://clawhub.ai/user/lihuiyang-03)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure ApiHz credentials, browse API categories, and call ApiHz services from scripts or generated code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ApiHz API keys may be exposed through HTTP fallback paths or unvalidated catalog URLs.

Mitigation: Use a low-privilege ApiHz account, rotate exposed or test keys, force HTTPS-only APIHZ_BASE_URL and APIHZ_LIST_URL, avoid HTTP fallback nodes, and validate destinations against trusted ApiHz hosts.

Risk: Local credential files may be committed, shared, or left readable by other users.

Mitigation: Verify that .credentials/apihz.txt is ignored by version control and owner-readable only before committing or sharing the workspace.

Risk: The security verdict is suspicious for this release.

Mitigation: Review the skill before installing it with real credentials and deploy only after the credential and network-routing risks are addressed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lihuiyang-03/skills/apihz-cn-skill)
- [ApiHz service site](https://www.apihz.cn/?shareid=10013679)
- [ApiHz GET/POST documentation](https://www.apihz.cn/template/miuu/getpost.php)
- [ApiHz optimal endpoint lookup](https://api.apihz.cn/getapi.php)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and API response descriptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to run Node.js scripts that use ApiHz credentials and produce local credential or cache files.]

## Skill Version(s):

1.0.4 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
