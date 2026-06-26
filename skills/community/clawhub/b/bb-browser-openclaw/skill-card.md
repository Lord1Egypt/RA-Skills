## Description: <br>
Turn any website into a CLI command across 36 platforms and 103 commands using OpenClaw's browser directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a1437707640-ui](https://clawhub.ai/user/a1437707640-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run bb-browser site adapters through OpenClaw for structured extraction from social, developer, news, finance, video, and knowledge sites, including logged-in pages when the user intentionally uses that browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate through a logged-in browser session against arbitrary sites and may read visible account data. <br>
Mitigation: Use it only on trusted sites, confirm the exact site and data before running adapter tests, and avoid sensitive accounts unless that access is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a1437707640-ui/bb-browser-openclaw) <br>
- [Publisher profile](https://clawhub.ai/user/a1437707640-ui) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional structured JSON from bb-browser commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the bb-browser binary. Site commands must include --openclaw; --json and --jq can be used for structured output and filtering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
