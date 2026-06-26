## Description: <br>
Manage iOS apps, TestFlight builds, submissions, and analytics via App Store Connect API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill to manage iOS and macOS apps through App Store Connect, including API authentication, TestFlight distribution, App Review submissions, app metadata updates, and analytics retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform powerful Apple developer-account actions when used with real App Store Connect credentials. <br>
Mitigation: Use the least-privilege App Manager or app-scoped API key and manually approve actions that submit builds, change metadata, invite testers, create apps or bundle IDs, or alter release settings. <br>
Risk: App Store Connect API credentials and .p8 private keys could grant broad account access if mishandled. <br>
Mitigation: Keep the .p8 file secure, store credential paths in environment variables, rotate keys periodically, and avoid committing credentials to version control. <br>


## Reference(s): <br>
- [App Store Connect skill page](https://clawhub.ai/ivangdavila/app-store-connect) <br>
- [App Store Connect](https://appstoreconnect.apple.com) <br>
- [App Store Connect API endpoint](https://api.appstoreconnect.apple.com/v1/apps) <br>
- [Skill homepage](https://clawic.com/skills/app-store-connect) <br>
- [API Authentication](artifact/api-auth.md) <br>
- [Common Workflows](artifact/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON, Ruby, Python, JavaScript, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ASC_ISSUER_ID, ASC_KEY_ID, and ASC_PRIVATE_KEY_PATH environment variables for authenticated App Store Connect workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
