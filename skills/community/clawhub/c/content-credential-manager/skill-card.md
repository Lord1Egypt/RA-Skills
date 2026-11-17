## Description:

Tracks API credential configuration status for a content-creation skill matrix and guides users through configuring credentials for platforms such as WeChat, Xiaohongshu, Meitu, StepFun, and Tavily.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amazinglittlefish](https://clawhub.ai/user/amazinglittlefish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to check which content-creation skills have usable credentials, identify missing API keys or cookies, and record credential values in a local OpenClaw credentials file before running publishing or media-generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles high-value API keys and browser session cookies, and release security evidence classifies the package as suspicious because credential sharing and storage are exposed.

Mitigation: Enter secrets through a local secure prompt or OS keychain when possible, avoid passing secrets through chat or command-line arguments, and rotate any credential that may have been exposed.

Risk: Credentials are stored in ~/.openclaw/credentials.json, so weak file permissions or shared machines could expose connected accounts.

Mitigation: Verify the credentials file and containing directory are private, keep file permissions restricted to the local user, and avoid storing browser session cookies unless necessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amazinglittlefish/skills/content-credential-manager)
- [Tavily API key portal](https://app.tavily.com)
- [StepFun API platform](https://platform.stepfun.com)
- [Meitu open platform](https://www.miraclevision.com/open-claw)
- [WeChat public platform](https://mp.weixin.qq.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and local JSON credential configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update ~/.openclaw/credentials.json and mask credential values in script output.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
