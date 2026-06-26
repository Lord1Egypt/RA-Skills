## Description: <br>
Find traditional inns inside ancient towns and water villages, including courtyard houses, wooden architecture, lantern-lit alleys, and old-world stays, with additional Fliggy-powered travel booking support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel agents use this skill to search for traditional inns in ancient towns or water villages and return real-time booking-oriented results. The skill is intended for travel planning workflows that rely on flyai CLI output rather than model memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install a global third-party npm CLI before running travel searches. <br>
Mitigation: Review and approve the flyai CLI source and installation path before deployment; use a controlled environment when possible. <br>
Risk: The skill may keep local logs of travel queries when the runbook behavior is followed. <br>
Mitigation: Confirm whether local logging is enabled, avoid recording sensitive travel details, and rotate or disable logs according to deployment policy. <br>
Risk: The skill returns booking links and may support purchase-oriented travel workflows. <br>
Mitigation: Require user confirmation before any purchase or booking action and keep booking decisions outside unattended automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/ancient-inn) <br>
- [Publisher profile](https://clawhub.ai/user/xiejinsong) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands when setup or retry steps are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should be derived from live flyai CLI output and include booking links when travel results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
