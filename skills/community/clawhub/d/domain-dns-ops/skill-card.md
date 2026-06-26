## Description: <br>
Routes agents through Peter's manager repo workflows for Cloudflare, DNSimple, and Namecheap domain onboarding, nameserver changes, redirects, redirect-worker mappings, and DNS/HTTP verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to perform Peter's domain and DNS operations, including Cloudflare onboarding, registrar nameserver updates, redirect configuration, and DNS/HTTP verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Nameserver flips, redirects, Cloudflare zone changes, and bot-protection changes can affect live production domains. <br>
Mitigation: Confirm the exact domain, registrar, Cloudflare zone, redirect target, token permissions, approval, and rollback plan before executing changes. <br>
Risk: The skill depends on Peter's local ~/Projects/manager workflow and may not fit other environments. <br>
Mitigation: Install and use it only when intentionally operating that same manager repository workflow. <br>


## Reference(s): <br>
- [Manager repo pointers](references/manager-repo.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
