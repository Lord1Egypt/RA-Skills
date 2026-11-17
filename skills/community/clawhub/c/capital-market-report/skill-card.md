## Description:

Generate high-signal, impact-driven capital market anomaly and delta reports covering both Chinese and global markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangzhe1991](https://clawhub.ai/user/yangzhe1991)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and market-focused agent users use this skill to gather recent Chinese and global market news, compare against prior 24-hour reports, and produce concise Markdown briefings focused on anomalies, deltas, and actionable market impact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and writes local OpenClaw memory/report files and caches fetched news.

Mitigation: Review the file paths and persistence behavior before installing, and run it only in a workspace where this local storage is acceptable.

Risk: The security guidance identifies an unsafe automatic report-deletion command that can remove more report history than intended.

Mitigation: Correct or remove the deletion instruction before routine use, and confirm cleanup commands target only reports older than the intended 24-hour window.

Risk: The skill invokes other local skill scripts for stock, crypto, hot-topic, and rumor data.

Mitigation: Install and review those dependent local skills before use, and verify market prices through the designated pricing tools rather than memory or web-search summaries.

## Reference(s):

- [Capital Market Report on ClawHub](https://clawhub.ai/yangzhe1991/skills/capital-market-report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration]

**Output Format:** [Markdown report with cited source URLs, inline command examples, and local report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are expected to include 24-hour delta comparisons, source diversity checks, market-isolation notes, leading-signal scanning, and anti-hallucination checks.]

## Skill Version(s):

6.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
