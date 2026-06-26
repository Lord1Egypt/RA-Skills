## Description: <br>
Monitors a curated list of AI and technology Twitter/X accounts, summarizes the day's key posts with an available LLM, and delivers a formatted digest to a configured chat channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FredHJC](https://clawhub.ai/user/FredHJC) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure, run, or schedule an automated AI news briefing from selected Twitter/X accounts. It is intended for daily digest generation, one-shot monitoring runs, and maintenance of the monitored account list, summary language, and delivery target. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires AISA and LLM API keys and can store them in a local scripts/.env file. <br>
Mitigation: Keep scripts/.env out of source control and backups, restrict file permissions where possible, and provide only the keys needed for the chosen run mode. <br>
Risk: The setup wizard can auto-detect and reuse OpenClaw credentials. <br>
Mitigation: Create scripts/.env manually instead of running setup.py when OpenClaw credential auto-detection is not desired. <br>
Risk: Scheduled execution can post unattended digests to the configured chat target. <br>
Mitigation: Test with a low-risk channel first and add an OpenClaw cron job only when unattended posting is intended. <br>


## Reference(s): <br>
- [Default Monitored Accounts](references/accounts.md) <br>
- [AISA API](https://aisa.one) <br>
- [ClawHub Skill Release](https://clawhub.ai/FredHJC/ai-twitter-digest) <br>
- [FredHJC Publisher Profile](https://clawhub.ai/user/FredHJC) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest text with source links, optional chat card preview links, and setup or scheduling commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a local .env configuration file and a deduplication state file during setup or execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
