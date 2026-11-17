## Description:

AIDSO虾搜 GEO 一体化 Skill，支持统一 API Key 绑定、检查、品牌诊断报告、品牌知识库、GEO 内容生产、GEO 问题挖掘。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangyuanmile-coder](https://clawhub.ai/user/tangyuanmile-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketers use this skill to work with the AIDSO GEO service for brand diagnosis reports, brand knowledge additions, GEO content generation, and AI search question mining. Developers or agents running it need Python 3 and an AIDSO_GEO_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan says the API-key binding flow sends the secret as ordinary content to a remote knowledge endpoint and stores keys locally in plaintext.

Mitigation: Use a low-privilege AIDSO key where possible, avoid entering secrets in normal chat or shell history, rotate any key previously bound with this version, and remove artifact/.env when no longer needed.

Risk: The security guidance notes that GEO_API_BASE_URL or wrapper environment changes can redirect authenticated question-mining requests.

Mitigation: Keep the default API base URL unless a trusted operator intentionally changes it, and review wrapper environment variables before running authenticated commands.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tangyuanmile-coder/skills/aidso-xiasou-geo)
- [AIDSO GEO service](https://geo.aidso.com)
- [AIDSO GEO API key settings](https://geo.aidso.com/setting?type=apiKey)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or JSON/text returned from AIDSO service, with shell commands for local helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and AIDSO_GEO_API_KEY; outputs can include report URLs, generated GEO content, brand knowledge add status, and question lists.]

## Skill Version(s):

2.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
