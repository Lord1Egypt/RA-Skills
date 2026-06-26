## Description: <br>
Capture and prepare App Store / Google Play screenshots for any React Native / Expo app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenshowinnovation](https://clawhub.ai/user/tenshowinnovation) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to generate, resize, summarize, and optionally upload localized iOS App Store and Google Play screenshots for React Native or Expo apps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional upload helpers can replace existing App Store or Google Play screenshot slots. <br>
Mitigation: Verify the app or package ID, locale, device slot, and screenshot directory before upload; pass --keep-existing unless replacement is intended. <br>
Risk: Store upload commands require sensitive App Store Connect or Google Play credentials. <br>
Mitigation: Use least-privilege store credentials and review commands before execution. <br>
Risk: Screenshots may contain secrets, private test data, or unreleased product content. <br>
Mitigation: Review generated images before upload or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenshowinnovation/expo-app-store-screenshots) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown guidance with shell and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces screenshot workflow instructions, local file paths, per-device summaries, and optional store upload commands.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
