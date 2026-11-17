## Description:

Guides creator research by evaluating benchmark accounts and organizing their earliest, highest-engagement, and latest posts into a practical learning roadmap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzifei](https://clawhub.ai/user/iamzifei)

### License/Terms of Use:

MIT-0

## Use Case:

Independent knowledge creators use this skill to choose a relevant creator to study and structure an analysis of that creator’s content and monetization path. It helps turn observed patterns into an original learning roadmap while discouraging reuse of names, wording, or cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid collection can create unexpected API charges.

Mitigation: Estimate the request count and cost, then get approval before collecting data.

Risk: An exposed API key or third-party login can put credentials or accounts at risk.

Mitigation: Use a dedicated, narrowly permissioned TikHub key, keep it out of logs, and explain credential handling before using login-dependent paths.

Risk: Saved preferences and rejection reasons may contain sensitive information.

Mitigation: Keep the configured memory folder private and decide explicitly whether those details should be retained.

Risk: Missing fetch support files or shared dependencies may prevent automated collection from working as expected.

Mitigation: Review the missing fetch script and shared dependencies before enabling automation.

## Reference(s):

- [Three-filter criteria](artifact/references/三筛判据.md)
- [Collection guide](artifact/references/抓取手册.md)
- [Benchmarking rules](artifact/references/规则卡.md)
- [ClawHub skill page](https://clawhub.ai/iamzifei/skills/aikey-benchmark)
- [Project upgrade guide](https://github.com/iamzifei/aikey#老用户升级zmm-已改名为-ai-key)
- [TikHub](https://tikhub.io)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, CSV, Shell commands]

**Output Format:** [Markdown reports and structured CSV data, with shell commands for supported collection workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account comparisons, post metrics, three post batches, and a learning roadmap; available data depends on the platform and collection path.]

## Skill Version(s):

0.2.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
