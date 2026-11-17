## Description:

自动搜索携程酒店，支持实时比价和详情获取。使用浏览器自动化技术，实现携程账号登录、酒店搜索、详情获取和对比分析功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexfeng75](https://clawhub.ai/user/alexfeng75)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers, travel planners, and agents can use this skill to search Ctrip hotels by city, date, price range, and lodging type, then compare hotel options and recommendations. Developers can also use the included Node.js and Playwright code as an automation workflow for Ctrip hotel search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a browser session that may be logged into a Ctrip account.

Mitigation: Review the automation before use, avoid unattended account actions, and verify hotel results directly on Ctrip before relying on them.

Risk: The artifact includes credential and API-key handling paths that could expose Ctrip credentials or MATON_API_KEY if real secrets are stored in project files.

Mitigation: Use environment variables or a secret manager, keep local configuration files out of version control, and do not commit or share real account passwords or API keys.

Risk: The MATON/Brave search scripts are separate from the Ctrip browser automation path and are under-disclosed in the skill documentation.

Mitigation: Treat those scripts as optional third-party search integrations, review their endpoints and data handling, and only provide API credentials if the publisher documents and justifies their use.

Risk: The release evidence says the skill overstates some live-search capability.

Mitigation: Treat generated recommendations and demo hotel data as advisory, and confirm current price, availability, and policies on Ctrip before booking or making travel decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexfeng75/skills/ctrip-hotel-search)
- [README](artifact/README.md)
- [Usage guide](artifact/USAGE.md)
- [Project summary](artifact/PROJECT_SUMMARY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-like search reports with inline JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hotel lists, prices, ratings, comparison summaries, and recommended top picks; live results should be verified directly on Ctrip.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
