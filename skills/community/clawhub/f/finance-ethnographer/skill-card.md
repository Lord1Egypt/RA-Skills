## Description: <br>
Always-on finance UX research. Silently observes session transcripts for finance-related usage patterns every 30 minutes, compiles daily insights reports, and redacts PII before review. Nothing leaves the machine automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dflam1](https://clawhub.ai/user/dflam1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users and finance UX researchers use this skill to observe local OpenClaw session transcripts for finance-related topics, synthesize daily usage insights, and review redacted reports before sharing anything externally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently monitors broad local chat transcripts for finance-related usage patterns. <br>
Mitigation: Install only with explicit user intent, review the cron entries before enabling them, and use setup_cron.py --remove to stop monitoring. <br>
Risk: Raw local observations and unredacted reports may contain sensitive financial or personal text. <br>
Mitigation: Keep generated data local, share only REDACTED report files, and delete generated observations or reports when monitoring is no longer wanted. <br>
Risk: Automated redaction may miss sensitive details. <br>
Mitigation: Run redaction validation and manually review redacted reports before emailing, uploading, or otherwise sharing report data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dflam1/finance-ethnographer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local JSONL observation logs and Markdown reports, including REDACTED report variants for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
