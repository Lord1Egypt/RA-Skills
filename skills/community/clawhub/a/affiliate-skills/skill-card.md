## Description: <br>
Affiliate Skills helps agents research affiliate programs, compare commission details, plan affiliate funnels, create marketing content, build landing assets, distribute campaigns, and review performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonpiaz](https://clawhub.ai/user/sonpiaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External affiliate marketers, creators, and developers use this skill suite to select affiliate programs, generate compliant promotional content, create landing pages, schedule distribution, and analyze optimization opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installed package includes a full affiliate-marketing suite, which is broader than a simple affiliate-program lookup helper. <br>
Mitigation: Install only when the full suite is intended, and review which bundled skills and scripts are relevant before enabling them in an agent workflow. <br>
Risk: Generated blog posts, social posts, landing pages, and Reddit guidance may create public-facing content with inaccurate claims, inadequate disclosure, or platform-policy concerns. <br>
Mitigation: Review all generated content before publication, keep affiliate disclosures visible, and avoid using guidance for stealth promotion or ban evasion. <br>
Risk: The affiliate-check helper can run a persistent local daemon and use an optional AFFITOR_API_KEY. <br>
Mitigation: Set AFFITOR_API_KEY only when needed, avoid exposing it in prompts or logs, and stop the daemon when finished. <br>
Risk: Distribution and publishing scripts may deploy or publish assets beyond local drafting. <br>
Mitigation: Run deployment or publishing scripts only when intentionally maintaining or publishing the package. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sonpiaz/affiliate-skills) <br>
- [list.affitor.com API Reference](API.md) <br>
- [Quick Start Guide](QUICKSTART.md) <br>
- [Skill Registry](registry.json) <br>
- [Affiliate Funnel Overview](docs/affiliate-funnel-overview.md) <br>
- [FTC Compliance Reference](shared/references/ftc-compliance.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, shell commands, and generated HTML or configuration files depending on the selected skill] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use AFFITOR_API_KEY for expanded affiliate-program search results and may generate public-facing marketing assets that require human review before publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, and root SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
