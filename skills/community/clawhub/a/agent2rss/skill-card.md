## Description: <br>
Agent2RSS helps agents manage RSS channels and publish content to RSS feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaotutu](https://clawhub.ai/user/yaotutu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to initialize Agent2RSS configuration, create and manage RSS channels, and publish markdown or JSON content to an RSS feed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Channel tokens may be exposed through examples, configuration, logs, or dry-run output. <br>
Mitigation: Review output before sharing it, keep the local config file private, and rotate any token copied from examples or exposed in logs. <br>
Risk: Publishing actions send content to the configured Agent2RSS server. <br>
Mitigation: Verify the serverUrl before upload or publish actions and avoid sending sensitive drafts to untrusted services. <br>


## Reference(s): <br>
- [Agent2RSS API examples](references/api-examples.md) <br>
- [ClawHub listing](https://clawhub.ai/yaotutu/agent2rss) <br>
- [Agent2RSS project](https://github.com/yaotutu/agent2rss) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown guidance with bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a configured Agent2RSS server and may print dry-run request details.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
