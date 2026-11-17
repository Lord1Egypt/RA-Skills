## Description:

Generates concise daily deal reports from Chinese ecommerce deal sources and can push the results to configured messaging channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gf1023456](https://clawhub.ai/user/gf1023456)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers who track ecommerce discounts use this skill to collect deal snapshots, rank notable offers, generate a daily markdown or text report, and optionally schedule or push that report to messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded Feishu credentials and a fixed recipient can expose secrets or send deal reports to an unintended account.

Mitigation: Remove the embedded credentials, rotate the exposed secret, and require all Feishu destinations to come from user-controlled configuration or environment variables before running or scheduling the skill.

Risk: Installing dependencies without a reviewed lockfile or pinned versions can pull unreviewed package changes.

Mitigation: Use a reviewed lockfile or pinned dependency set before running npm install.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gf1023456/skills/daily-deals-1-0-0)
- [SMZDM deal source](https://faxian.smzdm.com/h3s183t0f0c0p1/)
- [Shihuo deal source](https://www.shihuo.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain-text deal reports with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be printed locally, written to files, or pushed to configured messaging channels.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
