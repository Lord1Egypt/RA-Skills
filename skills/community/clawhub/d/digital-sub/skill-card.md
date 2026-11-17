## Description:

查询企业名称或纯数字股票代码对应的近24小时企业舆情日报，并在缺少 kr_skills_api_key 时完成 API Key 申请、微信扫码绑定和后续查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[36kr-com](https://clawhub.ai/user/36kr-com)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to query a company name or plain numeric stock code and receive a concise 24-hour company sentiment report. The workflow also supports API key acquisition and WeChat QR binding when the local kr_skills_api_key is missing or invalid.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company queries and API-key traffic are sent to 36Kr services.

Mitigation: Install and invoke the skill only when sharing those queries and credentials with 36Kr is acceptable.

Risk: The workflow can generate and persist an API key across sessions.

Mitigation: Require explicit user confirmation before key generation, shell profile edits, launchctl changes, or other persistent environment updates.

Risk: Evidence notes that credentialed traffic may use an insecure daily-report endpoint.

Mitigation: Prefer the documented HTTPS daily-report endpoint and avoid sending API keys over HTTP.

Risk: QR code handling can create temporary files or open local image viewers in CLI environments.

Mitigation: Use safe temporary locations, validate Base64 before writing files, and confirm before opening generated QR files.

## Reference(s):

- [API reference](references/api.md)
- [Base64 QR rendering reference](references/rendering.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown summary with API request guidance and QR image rendering guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include masked credential status, converted publish times, clickable report links, and rendered WeChat QR codes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
