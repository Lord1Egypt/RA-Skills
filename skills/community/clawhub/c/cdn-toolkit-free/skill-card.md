## Description: <br>
Guides personal developers through CDN deployment and tuning, including cache policy setup, basic security hardening, performance diagnostics, and domain configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft and review CDN cache, HTTPS, security header, DNS, and performance diagnostic configurations for personal websites or small projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live CDN account changes can alter production CDN behavior. <br>
Mitigation: Review every command, use least-privilege CDN tokens, test in staging or a maintenance window, and keep backups plus a rollback plan. <br>
Risk: Host firewall rules can block origin access or disrupt traffic. <br>
Mitigation: Validate rules before applying them, preserve the current firewall configuration, and confirm a rollback path before production execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cdn-toolkit-free) <br>
- [Cloudflare IP ranges](https://www.cloudflare.com/ips-v4) <br>
- [Cloudflare zone settings API endpoint](https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/settings/always_use_https) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell, nginx, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that call CDN APIs or modify host firewall rules; review before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
