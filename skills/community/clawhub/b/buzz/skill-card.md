## Description: <br>
Real-time news aggregator with Discord & Telegram push. Manage Jin10, BlockBeats, RSS, X KOLs, Polymarket, OpenNews via REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxcnny930](https://clawhub.ai/user/zxcnny930) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use Buzz to install and manage a local news-alert service that aggregates market, crypto, RSS, X KOL, and Polymarket updates and pushes notifications to Discord or Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The REST API may be unauthenticated if dashboard.password is empty. <br>
Mitigation: Set dashboard.password before exposing the service beyond localhost and include the password parameter on API calls. <br>
Risk: The server can bind to all network interfaces and expose configuration-changing endpoints. <br>
Mitigation: Restrict port 3848 to localhost or a trusted network with firewall rules or a reverse proxy. <br>
Risk: config.json may contain bot tokens, webhook URLs, and API keys. <br>
Mitigation: Keep config.json out of version control and protect access to the host and working directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zxcnny930/buzz) <br>
- [Publisher profile](https://clawhub.ai/user/zxcnny930) <br>
- [Buzz source repository referenced by artifact](https://github.com/zxcnny930/buzz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, curl examples, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include REST API examples for local configuration and operational checks.] <br>

## Skill Version(s): <br>
1.1.1 (source: SKILL.md frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
