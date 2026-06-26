## Description: <br>
提供高考志愿填报工具，用于查询学校和专业历年录取分数线、招生计划、院校和专业信息，并基于分数和位次生成志愿推荐。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and education advisors use this skill to query Chinese gaokao admissions data, convert scores to ranks, compare schools and majors, and prepare college application recommendations. The skill requires a XiaoBenYang API key and its source notes that 2026 data is temporarily virtualized from 2025 data until updated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required XiaoBenYang API key is stored locally in a plaintext .env file. <br>
Mitigation: Keep the .env file out of shared folders and version control, restrict local file access, and rotate the key if it may have been exposed. <br>
Risk: Gaokao query details are sent to the XiaoBenYang API. <br>
Mitigation: Install and use the skill only when sharing those query details with the external API provider is acceptable. <br>
Risk: The source states that 2026 data is temporarily virtualized from 2025 data. <br>
Mitigation: Treat 2026 recommendations as provisional and verify final admissions data before making application decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/gaokao-expert-v) <br>
- [Publisher profile](https://clawhub.ai/user/cainingnk) <br>
- [XiaoBenYang API key site](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries of JSON API results and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include school lists, score and rank lookups, admissions probability labels, and raw API-derived values summarized for the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
