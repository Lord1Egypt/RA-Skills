## Description:

Reads A-share intraday and after-close market tape, including theme strength, sector money-flow rankings, limit-up pools, verified intraday board-flow charts, and institutional survey heat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsetsugekka](https://clawhub.ai/user/tsetsugekka)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-analysis agents use this skill to assemble concise Chinese A-share market tape reports from requested modules such as theme strength, sector flow, limit-up activity, intraday board-flow charts, and institutional survey heat. It helps compare current or after-close signals while keeping source, timestamp, and fallback status visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data may be delayed, incomplete, stale, or mixed across sources and time windows, which can make rankings or tape reads misleading.

Mitigation: Report source, data time, snapshot status, and fallback changes; avoid combining incompatible sources or windows into precise conclusions.

Risk: Outputs could be mistaken for investment advice.

Mitigation: Treat results as market research only and keep user-facing conclusions neutral, source-labeled, and timestamped.

Risk: Mutable third-party theme data or shared temporary caches could affect rankings on compromised or multi-user systems.

Mitigation: Validate refreshed JSON before use, preserve cache freshness checks, and use isolated cache directories with appropriate local permissions.

Risk: Public market-data endpoints can rate-limit, fail, or return non-JSON responses.

Mitigation: Use aggregate requests, throttle repeated calls, stop increasing request volume after endpoint failures, and clearly state when a module is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tsetsugekka/skills/cn-market-tape)
- [Server-resolved GitHub provenance](https://github.com/tsetsugekka/codex-market-skills/tree/main/skills/cn-market-tape)
- [Market tape source routing](references/market-tape-source-routing.md)
- [Intraday flow chart SOP](references/intraday-flow-chart-sop.md)
- [Theme mainline lifecycle lens](references/theme-mainline-lifecycle.md)
- [Theme methodology source](https://finance.sina.com.cn/wm/2026-06-03/doc-iniaecsk0758056.shtml)
- [Public theme data source](https://daytrading.monster/themes)
- [Eastmoney institutional survey API](https://datacenter-web.eastmoney.com/api/data/v1/get)
- [Eastmoney delayed quote API](https://push2delay.eastmoney.com/api/qt/ulist.np/get)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese Markdown reports with tables, status lines, optional chart instructions, optional JSON, and optional CSV files from bundled scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include data timestamps, source labels, fallback status, and research-only caveats where relevant.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
