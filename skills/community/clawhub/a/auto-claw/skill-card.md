## Description: <br>
Auto-Claw autonomously monitors and optimizes WordPress sites with SEO fixes, performance audits, A/B testing, security checks, and competitor tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiongmao11132](https://clawhub.ai/user/xiongmao11132) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
D2C brands, WordPress agencies, and site operators use this agent to audit and automate WordPress SEO, performance, conversion experiments, content workflows, competitor monitoring, and selected site operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad live-site WordPress control may affect content, plugins, files, SEO behavior, or persistent site code. <br>
Mitigation: Install first in a staging or isolated WordPress environment, and do not grant production SSH, WP-CLI, web-root, webhook, or vault access until controls are reviewed. <br>
Risk: Approval and safety controls may be weaker than the release description implies. <br>
Mitigation: Require explicit human confirmation for publishing, persistent mu-plugin installation, destructive actions, and any operation that writes to a live site. <br>
Risk: Shell command construction and live-site defaults can increase execution risk. <br>
Mitigation: Replace shell string construction with safe argument lists and remove live-site defaults before production use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiongmao11132/auto-claw) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [CLI quick reference](artifact/QUICKREF.md) <br>
- [SEO deployment notes](artifact/docs/seo-deployment-20260324.md) <br>
- [Performance deployment notes](artifact/docs/performance-deployment-20260324.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON reports, generated HTML snippets, and CLI or shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may propose or perform WordPress changes; review in staging before granting live-site access.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
