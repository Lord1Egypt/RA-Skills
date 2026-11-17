## Description:

Daily Bazi Analysis helps OpenClaw answer Chinese BaZi daily fortune and suitability questions by combining the user's Four Pillars with the current date's annual, monthly, and daily flow pillars.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilir-is-here](https://clawhub.ai/user/lilir-is-here)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill when asking for Chinese BaZi daily fortune, daily suitability, or actionable auspicious and inauspicious guidance. The skill is intended to guide an agent through date lookup, Four Pillars profile handling, source-tagged BaZi interpretation, and concise daily recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores or logs user-linked Four Pillars birth-chart data, which can create privacy and retention concerns.

Mitigation: Require explicit user consent before saving profile data, provide review and deletion controls, and minimize retained logs.

Risk: Broad activation on generic daily scheduling questions may route users into BaZi guidance when they did not intend that use case.

Mitigation: Narrow activation to explicit BaZi or daily-fortune intent and keep advice framed as non-deterministic guidance.

Risk: Calendar data imports can affect shared data if run with excessive database privileges or an unexpected table target.

Mitigation: Run imports with a fixed table name, low database privileges, and validation of expected date and flow-pillar fields.

Risk: Bundled classic source texts have documented coverage gaps, which can make some structure or climate-adjustment conclusions incomplete.

Mitigation: Disclose incomplete source coverage in affected answers and avoid substituting unsourced model knowledge for missing classic text.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lilir-is-here/skills/bazi-daily)
- [Classic Sources Routing](references/classic-sources-routing.md)
- [Classics Text Cache](references/classics/README.md)
- [Bazi Calendar Schema](references/bazi-calendar-schema.md)
- [Heartbeat Contract For Bazi Profile](references/heartbeat-contract.md)
- [Import Command Template](references/import-command-template.md)
- [A. Di Tian Sui Source Text](references/classics/A_滴天髓.txt)
- [B. Yuan Hai Zi Ping Source Text](references/classics/B_渊海子平.txt)
- [C. Qiong Tong Bao Jian Source Text](references/classics/C_穷通宝鉴.txt)
- [Wannianrili Four Pillars Lookup](https://wannianrili.bmcx.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with source-tagged analysis, recommendations, and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a complete Four Pillars profile and date-indexed BaZi calendar data; outputs interpretive guidance rather than deterministic professional advice.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
