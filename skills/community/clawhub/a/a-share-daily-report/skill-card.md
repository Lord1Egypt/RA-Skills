## Description: <br>
Generates A-share morning and evening market reports from multiple market data sources, with optional Feishu document publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shoukuan](https://clawhub.ai/user/shoukuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate daily A-share pre-market and post-market market commentary, watchlist analysis, and optional Feishu notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated report contents or portfolio details may be sent externally through Feishu publishing. <br>
Mitigation: Clear or replace the Feishu target_chat_id, avoid sensitive watchlist content unless external sharing is acceptable, and use --publish only when publishing is intended. <br>
Risk: Credential fragments may appear in logs. <br>
Mitigation: Remove or patch API-key prefix logging before using real credentials. <br>
Risk: Generated trading guidance may be incomplete or not personalized. <br>
Mitigation: Treat reports as non-personalized market commentary and review them before making decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shoukuan/a-share-daily-report) <br>
- [README](artifact/README.md) <br>
- [Data sources](artifact/DATA_SOURCES.md) <br>
- [Interface design](artifact/INTERFACE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with optional PNG charts, PDF files, and Feishu document links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports morning or evening report modes, optional report date, configurable output directory, and optional Feishu publishing.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
