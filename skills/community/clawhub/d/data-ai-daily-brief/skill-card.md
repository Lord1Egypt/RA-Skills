## Description: <br>
Turns any industry into a daily intelligence briefing by searching, filtering, writing, and delivering structured briefs to configured channels with formatting checks and a business review gate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Practitioners, analysts, and teams use this skill to generate sourced daily industry intelligence briefs and distribute them through configured collaboration, email, or publishing channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send generated brief content outside the workspace through configured delivery channels. <br>
Mitigation: Enable only intended delivery targets and review the configured recipients or webhooks before use. <br>
Risk: GitHub Pages delivery can publish report output to the public internet. <br>
Mitigation: Use GitHub Pages only for content intended for public release and review the generated report before publishing. <br>
Risk: Channel credentials and tokens are needed for delivery integrations. <br>
Mitigation: Store credentials in environment variables or a secret store rather than committing them in configuration files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haiyangchenbj/skills/data-ai-daily-brief) <br>
- [README](README.md) <br>
- [Changelog](CHANGELOG.md) <br>
- [CodeBuddy](https://www.codebuddy.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown daily brief, HTML report, and channel-specific delivery content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write brief files and publish to configured external channels, including public GitHub Pages when enabled.] <br>

## Skill Version(s): <br>
5.0.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
