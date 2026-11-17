## Description: <br>
域名DNS管理免费版 helps individual developers and small teams manage single-domain DNS workflows for Cloudflare, DNSimple, and Namecheap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and small operations teams use this skill to plan and execute basic DNS record management, domain onboarding, nameserver changes, and verification workflows across supported providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live DNS, nameserver, and redirect changes that may disrupt production domains if applied incorrectly. <br>
Mitigation: Use least-privilege provider tokens, show the current DNS state and proposed diff before changes, verify each change with DNS lookups, and keep rollback records. <br>
Risk: Server security evidence notes unrelated project-management trigger language that could activate the skill in the wrong context. <br>
Mitigation: Review invocation context before using the skill and ignore unrelated trigger language that is not part of the DNS management task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/domain-dns-manager-free) <br>
- [Skill Source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-style result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference provider credentials through environment variables and requires human review before executing DNS changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
