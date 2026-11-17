## Description:

Connects OpenClaw or ClawHub agents to a hosted Chinese trademark SaaS platform API for trademark search, detail lookup, export jobs, point and module checks, and binding guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willeleven](https://clawhub.ai/user/willeleven)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and developers use this skill to search Chinese trademark records, inspect details, export selected results, and check account capabilities through a platform account. Agents should present point costs before billable actions and treat returned trademark data as informational rather than legal advice.

### Deployment Geography for Use:

China Mainland single-region deployment; all users are currently served through tm.zhengquai.com, and overseas regions are not yet available.

## Known Risks and Mitigations:

Risk: A platform token can be sent to an arbitrary configured host, and plaintext HTTP is possible when ALLOW_HTTP is enabled.

Mitigation: Set CHINA_TM_PLATFORM_BASE_URL to https://tm.zhengquai.com, keep ALLOW_HTTP disabled outside isolated local testing, and use only a token intended for this platform.

Risk: Search, detail, and export commands can perform billable account actions.

Mitigation: Confirm estimated point costs before each cost-bearing action, avoid repeated retries on insufficient balance, and rely on platform responses for final charges and refunds.

Risk: Trial-points documentation may be inconsistent according to the security guidance.

Mitigation: Treat the live capabilities response as authoritative for point balance and trial entitlement until the publisher clarifies the documentation.

Risk: Trademark results may be delayed, incomplete, or unsuitable as legal advice.

Mitigation: Use results for informational research only and consult official CNIPA records or a qualified trademark professional before legal, filing, or business decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/willeleven/skills/chinese-trademark-search-skill)
- [Platform Homepage](https://tm.zhengquai.com)
- [README](README.md)
- [API Contract](API_CONTRACT_EN.md)
- [Data Residency](DATA_RESIDENCY.md)
- [Security Notice](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured JSON from the CLI, with agent-facing summaries and guidance rendered as text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a platform account, CHINA_TM_USER_TOKEN, and CHINA_TM_PLATFORM_BASE_URL; cost-bearing actions consume platform points.]

## Skill Version(s):

1.2.0 (source: package.json, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
