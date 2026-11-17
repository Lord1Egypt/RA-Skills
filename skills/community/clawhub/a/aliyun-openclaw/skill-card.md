## Description:

Guides developers through deploying and operating an OpenClaw gateway on Alibaba Cloud, including SSH tunneling, device pairing, Browser Relay, and Feishu integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoyoalphax](https://clawhub.ai/user/yoyoalphax)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up and manage a remote OpenClaw deployment on Alibaba Cloud. It provides operational guidance for tunneling, gateway access, device approval, Browser Relay setup, model configuration, and Feishu integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence identifies live-looking root credentials and service secrets in the artifact.

Mitigation: Rotate the exposed SSH password, gateway token, model API key, Tavily key, and Feishu secret before installation or publication, then replace them with placeholders in the skill package.

Risk: The security summary flags broad remote-control configuration.

Mitigation: Disable root password login, restrict gateway binding and allowed origins, and require explicit operator review before running remote administration commands.

Risk: The security guidance notes unpinned packages and container images.

Mitigation: Pin package versions and container image digests or reviewed tags before using the deployment workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yoyoalphax/skills/aliyun-openclaw)
- [Browser Relay guide](artifact/browser_relay_guide.md)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw device pairing documentation](https://docs.openclaw.ai/web/control-ui#device-pairing-first-connection)
- [Alibaba Cloud Model Studio documentation](https://help.aliyun.com/zh/model-studio/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command blocks and JSON configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes remote administration and configuration guidance that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
