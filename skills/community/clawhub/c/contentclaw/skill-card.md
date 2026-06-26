## Description: <br>
Automated content generation engine that transforms source material such as papers, podcasts, case studies, Reddit threads, and GitHub repositories into platform-ready posts, diagrams, infographics, posters, and breakdowns using recipes and brand graphs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thierrypdamiba](https://clawhub.ai/user/thierrypdamiba) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketing teams, and developer advocates use this skill to turn source URLs and research material into reviewed content specs, social posts, visual content, publishing drafts, and engagement follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Playwright scraping, including browser stealth behavior, which may create site terms-of-service or access-policy risk. <br>
Mitigation: Use the skill only where scraping is allowed, review target-site terms, and run it in a sandboxed environment. <br>
Risk: The skill can use stored Reddit/X cookies for scraping, publishing, and engagement tracking, which can act through the user's social accounts. <br>
Mitigation: Use separate social accounts where possible, restrict cookie scope, review publishing commands, and run dry-run previews before posting. <br>
Risk: The skill sends image prompts to fal.ai and topic discovery queries to Exa, and the security guidance warns against sensitive PDFs or internal URLs until cleanup and scoping issues are fixed. <br>
Mitigation: Use scoped API keys, avoid sensitive or internal source material, and review generated specs before external API-backed steps. <br>


## Reference(s): <br>
- [Content Claw ClawHub page](https://clawhub.ai/thierrypdamiba/contentclaw) <br>
- [Content Claw homepage](https://github.com/scaleintelligence/content-claw) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, image files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown content, JSON content specs, PNG image outputs, and command-oriented setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include platform-ready copy, image generation specifications, local content artifacts, publishing previews, and engagement summaries.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter, pyproject.toml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
