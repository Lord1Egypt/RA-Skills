## Description: <br>
Monitor Costco inventory by ZIP and run it safely with OpenClaw cron. Keep secrets outside the skill directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cweiping](https://clawhub.ai/user/cweiping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and run repeatable Costco product availability checks by ZIP code, write snapshot and report files, and schedule monitoring with OpenClaw cron. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-frequency Costco monitoring through residential proxies may cause blocks, terms-of-service issues, and proxy costs. <br>
Mitigation: Use the skill only with authorization, set a conservative polling interval, and review or remove residential proxy and block-recovery guidance before scheduling runs. <br>
Risk: Proxy credentials can be exposed in command-line arguments, generated output, logs, or snapshots. <br>
Mitigation: Keep real secrets outside the skill directory in a restricted environment file, avoid placing real proxy passwords on command lines, and restrict access to logs and snapshot files. <br>
Risk: Blocked, CAPTCHA, or ambiguous Costco responses can produce unknown or misleading availability results. <br>
Mitigation: Treat blocked or ambiguous responses as unknown, review reports before acting on them, and avoid alerting until repeated checks confirm the condition. <br>


## Reference(s): <br>
- [Costco Inventory Monitoring Standard](references/costco-inventory-standard.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cweiping/costco-inventory-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus JSON, JSONL, and plain-text report files when executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces monitoring plans, runnable check commands, structured snapshots, state files, logs, and a latest report file.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
