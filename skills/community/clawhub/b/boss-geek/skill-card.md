## Description: <br>
BOSS直聘求职者工具 that uses OpenCLI with a logged-in Chrome session to search jobs, view details, greet HR contacts, inspect chat lists, and send messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spyqwer1](https://clawhub.ai/user/spyqwer1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job seekers and agents use this skill to operate BOSS直聘 through OpenCLI for job search, job-detail review, HR greetings, chat review, and message sending from the user's logged-in browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands such as greet and send can send real messages from the user's logged-in BOSS直聘 account. <br>
Mitigation: Manually verify the recipient, job, and exact message before running greet or send. <br>
Risk: The skill relies on a Chrome login session and the OpenCLI browser extension. <br>
Mitigation: Use a separate Chrome profile and install only after reviewing the referenced external OpenCLI plugin source. <br>
Risk: Recommended jobs may no longer be active. <br>
Mitigation: Run detail against the returned securityId before greeting HR or sending related messages. <br>


## Reference(s): <br>
- [OpenCLI](https://github.com/jackwener/opencli) <br>
- [City and Filter Codes](references/codes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/spyqwer1/boss-geek) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and tabular command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger real BOSS直聘 account actions through OpenCLI when the user runs greet or send commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
