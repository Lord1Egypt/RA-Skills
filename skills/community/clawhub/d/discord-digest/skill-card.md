## Description: <br>
Generate formatted digests from Discord servers using a user token by reading selected channels and threads and summarizing activity with links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NikolayBohdanov](https://clawhub.ai/user/NikolayBohdanov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to monitor configured Discord servers and produce concise activity reports from selected channels or threads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Discord user token can provide broad account access if exposed through shell history, logs, or the local config file. <br>
Mitigation: Prefer a bot or OAuth-based alternative, avoid passing tokens on the command line, keep the config file private, and rotate the token immediately if it is exposed. <br>
Risk: Automated digest forwarding can disclose Discord server content to unauthorized recipients. <br>
Mitigation: Enable scheduled forwarding only when channel owners and all recipients are authorized, and review configured servers and channels before running automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NikolayBohdanov/discord-digest) <br>
- [Discord API endpoint](https://discord.com/api/v10) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest text with direct links, plus command output and JSON configuration values.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Digest period, server selection, and channel selection are configurable.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
