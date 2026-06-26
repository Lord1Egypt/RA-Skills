## Description: <br>
Generate production-ready App Store and Play Store screenshots from a codebase by reading app colors, screens, and copy, then creating a finished screenshot set in exact store dimensions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twworks-org](https://clawhub.ai/user/twworks-org) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and app teams use this skill to gather app context, confirm screenshot direction, and generate App Store or Play Store screenshot sets through AppScreenshotStudio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Codebase summaries, app metadata, unreleased strategy, or proprietary details may be sent to AppScreenshotStudio as a third-party service. <br>
Mitigation: Review the gathered app summary, colors, screen names, metadata, and copy before API calls, and remove secrets or proprietary details that should not be shared externally. <br>
Risk: Screenshot generation chat calls can spend AppScreenshotStudio credits. <br>
Mitigation: Confirm the user-approved screenshot direction before running credit-spending chat calls and check the returned credit status. <br>
Risk: The skill requires an AppScreenshotStudio API key in the environment. <br>
Mitigation: Keep APPSCREENSHOTSTUDIO_API_KEY out of shared logs, files, and generated app context. <br>


## Reference(s): <br>
- [ClawHub AppScreenshotStudio release page](https://clawhub.ai/twworks-org/appscreenshotstudio) <br>
- [AppScreenshotStudio OpenClaw homepage](https://appscreenshotstudio.com/openclaw) <br>
- [AppScreenshotStudio account settings](https://appscreenshotstudio.com/settings) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce AppScreenshotStudio project IDs, generated layout summaries, credit status, and exported image URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
