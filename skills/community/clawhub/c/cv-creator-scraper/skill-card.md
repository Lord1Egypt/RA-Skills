## Description: <br>
Creativault Creator Scraper helps agents search, collect, export, and contact creators across TikTok, YouTube, Instagram, and Twitter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[creativault](https://clawhub.ai/user/creativault) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, creator partnership teams, and agents use this skill to discover creator prospects, collect creator data, export campaign files, and manage outreach workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect creator contact data and export creator/contact files. <br>
Mitigation: Use it only with a lawful, policy-compliant basis and handle exported files as sensitive data. <br>
Risk: The skill can send real outreach emails, including batch sends. <br>
Mitigation: Verify recipient lists, message content, and user authorization before sending any outreach. <br>
Risk: The scanner summary flags an overbroad self-update mechanism that can rewrite or delete skill files. <br>
Mitigation: Keep CV_SKILL_AUTO_UPDATE disabled unless remote updates are intentional, and review update manifests before running confirmed updates. <br>
Risk: The skill requires sensitive credentials for API access and operator identity. <br>
Mitigation: Store CV_API_KEY and CV_USER_IDENTITY securely and limit access to trusted operators. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/creativault/cv-creator-scraper) <br>
- [API Reference](references/api-reference.md) <br>
- [Platform Parameters](references/platform-params.md) <br>
- [Industry Categories](references/industry-categories.md) <br>
- [Country Codes](references/country-codes.md) <br>
- [Language Codes](references/language-codes.md) <br>
- [Error Codes](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON API inputs, and exported xlsx/csv/html files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce creator/contact datasets and signed download links through the Creativault API.] <br>

## Skill Version(s): <br>
1.8.0 (source: release evidence, target metadata, artifact frontmatter, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
