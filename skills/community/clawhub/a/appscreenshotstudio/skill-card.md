## Description:

Generate production-ready App Store and Play Store screenshots from your codebase. Reads your app's colors, screens, and copy - then creates a finished screenshot set in exact store dimensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twworks-org](https://clawhub.ai/user/twworks-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and app teams use this skill to inspect an app codebase, confirm store screenshot priorities, and generate App Store or Play Store screenshot sets through AppScreenshotStudio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends selected app metadata, screen names, colors, features, and marketing copy to appscreenshotstudio.com.

Mitigation: Review the project summary before generation and remove secrets, private roadmap details, or sensitive customer information.

Risk: The skill requires an AppScreenshotStudio API key for authenticated API calls.

Mitigation: Store APPSCREENSHOTSTUDIO_API_KEY in an environment variable or secret manager and do not paste it into prompts, files, or generated copy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twworks-org/skills/appscreenshotstudio)
- [AppScreenshotStudio OpenClaw Page](https://appscreenshotstudio.com/openclaw)
- [AppScreenshotStudio Account Settings](https://appscreenshotstudio.com/settings)
- [TW Works Publisher Profile](https://clawhub.ai/user/twworks-org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and API response references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce AppScreenshotStudio project IDs and CDN image URLs after authenticated API calls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
