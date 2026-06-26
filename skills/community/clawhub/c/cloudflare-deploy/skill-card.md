## Description: <br>
Deploy applications and infrastructure to Cloudflare using Workers, Pages, and related platform services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tbeard602](https://clawhub.ai/user/tbeard602) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose Cloudflare platform services, prepare authentication, deploy Workers or Pages projects, and troubleshoot common Cloudflare deployment paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad Cloudflare infrastructure changes, including deployment, DNS, email, and production bindings. <br>
Mitigation: Use staging resources first and review every proposed Cloudflare change before execution, especially DNS, email, billing, and production-binding changes. <br>
Risk: The skill requires Cloudflare authentication and may rely on sensitive credentials. <br>
Mitigation: Use scoped Cloudflare API tokens with the minimum required permissions and avoid exposing tokens in prompts, logs, repositories, or generated files. <br>
Risk: Some deployment or networking examples can expose services or run code with insufficient access controls. <br>
Mitigation: Add authentication, allowlists, and rollback steps before publishing services or copying examples into production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tbeard602/cloudflare-deploy) <br>
- [Cloudflare Deploy skill instructions](artifact/SKILL.md) <br>
- [Wrangler authentication reference](artifact/references/wrangler/auth.md) <br>
- [Workers reference](artifact/references/workers/README.md) <br>
- [Pages reference](artifact/references/pages/README.md) <br>
- [Cloudflare API reference](artifact/references/api/README.md) <br>
- [Terraform reference](artifact/references/terraform/README.md) <br>
- [Pulumi reference](artifact/references/pulumi/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Cloudflare deployment commands, configuration changes, and troubleshooting steps that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
