## Description: <br>
ClawCV is a WonderCV career assistant skill that helps agents analyze resumes, rewrite resume sections, match resumes to jobs and campus roles, export one-page PDFs, and provide job-search coaching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[000wonderclaw](https://clawhub.ai/user/000wonderclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and job seekers use ClawCV inside MCP-capable AI tools to review resumes, improve resume content, compare resumes with job descriptions, find campus recruiting roles, create PDF resumes, and get interview or career-planning guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume and career data may be sent to WonderCV's backend for processing. <br>
Mitigation: Use the skill only when the user explicitly wants ClawCV processing, and avoid sending unnecessary sensitive personal details. <br>
Risk: The skill requires an API key and installs the `clawcv` npm package. <br>
Mitigation: Install only if you trust WonderCV and the `clawcv` package, keep `SKILL_BACKEND_API_KEY` secret, and use HTTPS for account and API-key setup. <br>
Risk: Career, resume, and job-matching guidance can be incomplete or unsuitable for a user's specific goals. <br>
Mitigation: Review outputs before acting on them, especially before submitting resumes, applying to roles, or using generated PDFs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/000wonderclaw/clawcv) <br>
- [WonderCV ClawCV](https://www.wondercv.com/clawcv) <br>
- [WonderCV Website](https://wondercv.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, lists, inline shell commands, configuration snippets, and links where applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include resume analysis, rewrite suggestions, job-match findings, campus role listings, generated PDF links, account guidance, and feedback links.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
