## Description: <br>
Sets up and operates a Feishu Bitable personal bookkeeping workflow with local Markdown bill files, Feishu synchronization, record querying, deletion, and an optional Android dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naeemtc](https://clawhub.ai/user/naeemtc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure a Feishu-based personal accounting system, record income and expenses, query summaries, and optionally view records in an Android dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles long-lived Feishu app credentials and tenant tokens. <br>
Mitigation: Use a dedicated low-privilege Feishu app, avoid exposing secrets in chat or logs, store credentials only where needed, and rotate any secret that may have been disclosed. <br>
Risk: The skill can create, update, and delete remote financial records and local bill files. <br>
Mitigation: Start with a test Base, keep backups of important records, and manually confirm record indexes and targets before running delete or cleanup actions. <br>
Risk: Image-based bill parsing can misread amounts, dates, or categories. <br>
Mitigation: Confirm parsed image entries with the user before writing them to local files or Feishu records. <br>
Risk: The optional Android APK is a separate application that stores Feishu access details for dashboard use. <br>
Mitigation: Verify the APK source and release before installation, prefer building from trusted source when possible, and use scoped credentials for the dashboard. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/naeemtc/feishu-accounting) <br>
- [Publisher profile](https://clawhub.ai/user/naeemtc) <br>
- [Project homepage from ClawHub metadata](https://github.com/NaeemTC/feishu-accounting-skill) <br>
- [Categories reference](references/categories.md) <br>
- [Feishu permissions API reference](references/feishu-permissions-api.md) <br>
- [Feishu Base API pitfalls](references/feishu-base-api-pitfalls.md) <br>
- [APK architecture](references/apk-architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, local Markdown bill files, Python script outputs, and Feishu Bitable records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create and delete local bill records, synchronize remote Feishu records, and provide Android dashboard installation guidance.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
