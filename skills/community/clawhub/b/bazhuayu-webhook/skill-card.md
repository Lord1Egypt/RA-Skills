## Description: <br>
Triggers Bazhuayu/Octoparse RPA tasks through a configured webhook and passes custom parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blogwebsem](https://clawhub.ai/user/blogwebsem) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation operators use this skill to configure and trigger Bazhuayu/Octoparse RPA workflows from an agent or shell, pass task parameters, and verify webhook credential setup before live execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook URL and signing key exposure could let an unauthorized party trigger configured RPA tasks. <br>
Mitigation: Store real values in a secrets manager or tightly permissioned private environment file, and do not commit config files, env files, logs, screenshots, or shell profiles containing credentials. <br>
Risk: Live runs can trigger real RPA automation against the configured account or workflow. <br>
Mitigation: Use the documented test or dry-run mode before live execution, and enable unattended cron execution only when repeated task triggering is intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/blogwebsem/bazhuayu-webhook) <br>
- [README](README.md) <br>
- [Quickstart](QUICKSTART.md) <br>
- [Webhook Setup Guide](WEBHOOK_SETUP.md) <br>
- [Security Guide](SECURITY.md) <br>
- [Bazhuayu RPA Help Center](https://rpa.bazhuayu.com/helpcenter) <br>
- [Webhook Trigger Documentation](https://rpa.bazhuayu.com/helpcenter/docs/skmvua) <br>
- [RPA API Documentation](https://rpa.bazhuayu.com/helpcenter/docs/rpaapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and text command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus BAZHUAYU_WEBHOOK_URL and BAZHUAYU_WEBHOOK_KEY environment variables for live webhook execution.] <br>

## Skill Version(s): <br>
2.0.4 (source: package.json, release evidence, RELEASE-2.0.4.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
