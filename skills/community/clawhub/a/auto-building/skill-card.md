## Description: <br>
Auto Building helps agents guide users through configuring and running an AUTO-BUILDING content aggregation system that collects, reviews, classifies, and publishes content from user-selected sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to set up customized news, product monitoring, industry intelligence, resource directory, or information aggregation systems. The skill provides configuration guidance, setup commands, and examples for data sources, categories, collection rules, review, and publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs users to run an external npm project. <br>
Mitigation: Review the repository and npm dependencies before installation, and prefer a pinned commit or release. <br>
Risk: The configured system can collect content from arbitrary web sources. <br>
Mitigation: Configure only authorized sources and add rate limits, robots.txt or terms-of-service checks, and privacy and copyright controls for recurring collection jobs. <br>
Risk: Collected content may be incorrect, inappropriate, or unsuitable for publication. <br>
Mitigation: Keep the human review workflow enabled before publishing collected content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/addogiavara-tech/auto-building) <br>
- [Publisher profile](https://clawhub.ai/user/addogiavara-tech) <br>
- [Project homepage](https://sora.wboke.com/) <br>
- [OpenClaw install repository](https://github.com/hasd52636-a11y/Auto_Building_new) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON or TypeScript configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include local Node.js setup steps, source configuration examples, and review workflow instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, CHANGELOG.md, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
