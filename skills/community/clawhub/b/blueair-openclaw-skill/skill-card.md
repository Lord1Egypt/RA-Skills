## Description: <br>
Use when managing Blueair air purifiers, checking indoor air quality, or responding to respiratory discomfort complaints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[you96](https://clawhub.ai/user/you96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with Blueair purifiers use this skill to have an agent check household air quality, interpret sensor readings, and propose or perform supported purifier controls. <br>

### Deployment Geography for Use: <br>
US, EU, AU, CN, and RU Blueair regions <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Blueair account credentials and purifier controls. <br>
Mitigation: Use a dedicated low-privilege Blueair account if available and restrict permissions on ~/.blueair/config.json. <br>
Risk: Purifier state changes could affect multiple devices or be inferred from broad user requests. <br>
Mitigation: Require agent confirmation before changing purifier state, especially for bulk or inferred actions. <br>
Risk: The test-login helper may print device data. <br>
Mitigation: Run test-login only when needed for setup or troubleshooting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/you96/blueair-openclaw-skill) <br>
- [README](README.md) <br>
- [Basic usage examples](examples/basic-usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and summarized device status data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Blueair credentials and Node.js dependencies before status or control commands can run.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
