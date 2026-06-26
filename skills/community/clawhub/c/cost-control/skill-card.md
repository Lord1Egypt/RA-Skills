## Description: <br>
Prevent runaway API costs with 3-tier protection: caution, emergency, and hard cap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to add configurable spend controls around expensive APIs, including AI model APIs, cloud compute, and paid third-party services. It helps agents propose integration code, shell commands, and configuration steps for tiered budget thresholds, emergency blocking, and an optional external watchdog. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external watchdog can terminate the process identified by state/app.pid when configured thresholds are exceeded. <br>
Mitigation: Verify state/app.pid is created by the intended application, test the watchdog in staging, and document the rollback process before enabling the cron job. <br>
Risk: Incorrect thresholds or pricing settings can either block valid API usage too early or fail to stop overspending quickly enough. <br>
Mitigation: Set thresholds against the actual budget and provider pricing, then run a staged test with conservative limits before production use. <br>
Risk: Emergency and kill-switch flags require manual cleanup, so a false alarm can keep API calls paused. <br>
Mitigation: Define an operator runbook for investigating the cause, removing the cron entry if needed, and clearing emergency flags only after the issue is fixed. <br>


## Reference(s): <br>
- [Cost Control ClawHub Release](https://clawhub.ai/TheShadowRose/cost-control) <br>
- [Publisher Profile](https://clawhub.ai/user/TheShadowRose) <br>
- [README](artifact/README.md) <br>
- [Known Limitations](artifact/LIMITATIONS.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces integration guidance for local file-based cost tracking, emergency flags, manual kill-switch use, and cron-based watchdog setup.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
