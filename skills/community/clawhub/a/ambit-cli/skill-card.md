## Description: <br>
Helps agents use the ambit CLI to create and destroy private networks, deploy private Fly.io apps behind Tailscale, check router health, list routers, and diagnose connectivity problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToxicPine](https://clawhub.ai/user/ToxicPine) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to operate Ambit workflows for private, internet-invisible application deployment on Fly.io with Tailscale-based access. It helps plan and run network creation, app deployment, router status checks, troubleshooting, and teardown commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports high-privilege infrastructure actions that can create, deploy, modify, or destroy Fly.io and Tailscale resources. <br>
Mitigation: Require explicit user approval before running deploy, destroy, --yes, or --self-approve actions, and review planned changes before execution. <br>
Risk: Ambit workflows may use a Tailscale API token and external templates or npm packages. <br>
Mitigation: Protect and scope the Tailscale API token, avoid exposing secrets in logs or command history, review external packages, and prefer pinned template refs or commits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ToxicPine/ambit-cli) <br>
- [Tailscale API keys](https://login.tailscale.com/admin/settings/keys) <br>
- [Tailscale ACL tags](https://login.tailscale.com/admin/acls/visual/tags) <br>
- [Fly.io flyctl installation](https://fly.io/docs/flyctl/install/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON output guidance when the ambit --json flag is relevant.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
