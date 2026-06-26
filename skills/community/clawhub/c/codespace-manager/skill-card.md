## Description: <br>
Creates, manages, and exposes isolated code-server development environments in Docker through Cloudflare Tunnel, with Bun, uv, and OpenCode pre-installed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lanbasara](https://clawhub.ai/user/Lanbasara) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create, start, stop, inspect, and remove isolated browser IDE environments backed by Docker containers. Review before installing because the security evidence notes public browser IDE exposure, password handling, and host filesystem path risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Lanbasara/codespace-manager) <br>
- [Docker installation documentation](https://docs.docker.com/get-docker/) <br>
- [Cloudflare Tunnel downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) <br>
- [Bun installer](https://bun.sh/install) <br>
- [uv installer](https://astral.sh/uv/install.sh) <br>
- [OpenCode configuration schema](https://opencode.ai/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Docker, cloudflared, jq, password, tunnel URL, and destructive lifecycle command guidance that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
