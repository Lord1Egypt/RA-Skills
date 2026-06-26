## Description: <br>
A Bilibili CLI skill for publishing, deleting, and reposting dynamic posts; querying videos, users, and live rooms; searching content; and using related MCP tooling for danmaku retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OSSKn4w7](https://clawhub.ai/user/OSSKn4w7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to let an agent automate Bilibili account workflows such as content posting, deletion, search, user and video lookup, and live room queries. It is best suited to accounts where the operator can review actions before public or account-changing operations run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authenticated control over a user's Bilibili account and public content. <br>
Mitigation: Require manual approval before post, delete, repost, like, or batch operations, and use a low-risk account where possible. <br>
Risk: Bilibili cookies or session credentials may be exposed if stored in plaintext configuration files or environment logs. <br>
Mitigation: Protect or avoid plaintext cookie files, limit credential access, and rotate cookies if exposure is suspected. <br>
Risk: External CLI or MCP code used by the skill may change behavior or introduce additional risk. <br>
Mitigation: Review, pin, and scan external CLI and MCP dependencies before enabling the skill. <br>
Risk: Frequent authenticated API use may trigger platform risk controls or account restrictions. <br>
Mitigation: Throttle automation, avoid high-volume batch actions, and keep a human approval step for account-changing operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/OSSKn4w7/bilibili-skill) <br>
- [bilibili-api](https://github.com/Nemo2011/bilibili-api) <br>
- [bilibili-mcp-server](https://github.com/huccihuang/bilibili-mcp-server) <br>
- [CLI-Anything](https://github.com/HKUDS/CLI-Anything) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, bilibili-cli, and Bilibili session credentials supplied through environment variables or a local cookie file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
