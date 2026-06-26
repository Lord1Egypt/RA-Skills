## Description: <br>
Monitors OpenClaw JSON logs for ERROR-level entries, records recent issues, and provides system-level remediation suggestions for gateway, port, and session problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amd5](https://clawhub.ai/user/amd5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor local OpenClaw runtime logs, deduplicate recent error reports, and receive suggested checks for gateway connectivity, port usage, and session cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scheduled install behavior is unclear, including a declared postinstall script that is not present in the artifact. <br>
Mitigation: Review install behavior before use, ask the publisher to include or remove the installer, and document how any cron job is created and disabled. <br>
Risk: The skill runs local commands and writes persisted log excerpts, while some documentation describes behavior as manual or read-only. <br>
Mitigation: Run without elevated privileges, review command execution before enabling automation, and treat saved log excerpts as potentially sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amd5/error-monitor-fix) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/amd5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports and console text, with optional JSON output from scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes deduplicated error summaries and fix history under the local OpenClaw workspace when run.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
