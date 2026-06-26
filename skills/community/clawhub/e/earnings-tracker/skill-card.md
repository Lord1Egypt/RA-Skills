## Description: <br>
Tracks earnings calendars and company financial-report signals for configured stock watchlists, with an emphasis on A-share data via AKShare. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market analysts can use this skill to scan configured earnings watchlists and produce a concise earnings-calendar report. The shipped code focuses on China A-share earnings data and writes a local JSON report for downstream agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner verdict is suspicious because the documentation does not match the shipped code. <br>
Mitigation: Use the Python command from package.json and review expected behavior before installing or running the skill. <br>
Risk: The script writes results to a hard-coded local OpenClaw memory path. <br>
Mitigation: Change or remove the hard-coded output path before running it in a different environment. <br>
Risk: Documented US-market tracking and Discord or Telegram alert behavior may not be implemented by the shipped code. <br>
Mitigation: Treat the current release as an A-share scanner unless the artifact is updated and retested. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunnyhot/earnings-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands] <br>
**Output Format:** [Console text and JSON file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configured stock watchlist and writes earnings-calendar results to a local JSON file.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
