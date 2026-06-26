## Description: <br>
Deep Research Pro helps agents run multi-source web and news research through SkillBoss API Hub, synthesize findings, and deliver cited reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to plan research questions, search multiple web and news sources, fetch selected pages for deeper reading, and produce cited reports for decision support or writing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries, URLs, and selected page-fetch requests are sent to SkillBoss API Hub. <br>
Mitigation: Use the skill only when that third-party data flow is acceptable, and avoid confidential, regulated, secret, or internal-only topics unless approved. <br>
Risk: The skill requires a SkillBoss API key. <br>
Mitigation: Provide SKILLBOSS_API_KEY through a secure environment variable and avoid putting the key in prompts, reports, or checked-in files. <br>
Risk: Generated reports may be saved to local disk and can contain sensitive research topics or conclusions. <br>
Mitigation: Review saved files before sharing, choose an appropriate storage location, and remove reports that should not remain in the workspace. <br>
Risk: Web-derived research can be incomplete, stale, or misleading. <br>
Mitigation: Review cited sources, cross-check important claims, and treat unverified single-source findings as lower confidence. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/marjoriebroad/abe-deep-research-pro) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown reports with inline citations; optional JSON or saved Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may save full reports under ~/clawd/research/[slug]/report.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
