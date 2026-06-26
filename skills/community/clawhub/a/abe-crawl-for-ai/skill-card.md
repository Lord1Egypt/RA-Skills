## Description: <br>
Web scraping via SkillBoss API Hub. Use for fetching full page content with JavaScript rendering. Handles complex pages with dynamic content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch rendered web page content and return clean markdown or JSON for pages that need JavaScript rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs and page-derived data are sent to SkillBoss/HeyBoss for scraping. <br>
Mitigation: Avoid private, signed, internal, or authenticated URLs unless approved for that data flow. <br>
Risk: The skill requires a sensitive SkillBoss API key. <br>
Mitigation: Use a dedicated key where possible and manage it through approved secret storage with rotation and revocation controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abe-crawl-for-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Markdown by default; pretty-printed JSON when the --json option is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and the SKILLBOSS_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
