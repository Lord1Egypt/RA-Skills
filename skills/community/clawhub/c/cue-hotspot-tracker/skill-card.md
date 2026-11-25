## Description:

用 Cue 通常 5-10 分钟（最长约 15 分钟）实时扫描今日 A 股热点板块与近 24h 催化资讯，拆解盘中催化逻辑与受益方向；跑完自动生成「看板图」与「报告长图」，报告全文以 Cue 链接交付。

This skill is ready for commercial/non-commercial use.

## Publisher:

[panting09266-ai](https://clawhub.ai/user/panting09266-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users following the Chinese A-share market can use the skill to review intraday sector activity and recent catalysts, then receive a summarized dashboard image, a full report image, and a Cue report link.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: ClawScan reports a mismatch between the market-research description and the inspected document-conversion code, so the advertised research behavior may not match the reviewed code.

Mitigation: Review the skill and its referenced files before use, and verify market claims against current sources.

Risk: The security scan was partial because a referenced local path was missing; the scanner also reports remote fetching and scheduled-run instructions.

Mitigation: Treat the scan as incomplete, inspect the missing path, keep the Cue API key in local configuration or an environment variable, and enable recurring runs only by explicit choice.

Risk: The guidance includes purchase, reward, and referral prompts.

Mitigation: Review those prompts independently and follow them only when you choose to.

## Reference(s):

- [SOP dashboard schema](references/sop-schema.md)
- [ClawHub skill release page](https://clawhub.ai/panting09266-ai/skills/cue-hotspot-tracker)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Guidance]

**Output Format:** [Intraday research report, dashboard and long-form PNG images, and a Cue share link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is delivered through a Cue link; the skill documentation says not to paste the full report into chat by default.]

## Skill Version(s):

1.0.15 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
