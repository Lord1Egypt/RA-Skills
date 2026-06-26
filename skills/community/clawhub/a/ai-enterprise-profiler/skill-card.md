## Description: <br>
面向 AI 从业者的企业研究技能，适用于企业画像、竞品扫描、融资与团队分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiqizhixin](https://clawhub.ai/user/jiqizhixin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI industry practitioners, investment researchers, business development teams, marketers, and strategy teams use this skill to build structured company profiles, compare competitors, summarize financing and team signals, and form company or sector-level conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enterprise research queries are sent to the Jiqizhixin API with the user's JQZX_API_TOKEN. <br>
Mitigation: Treat the token as secret and avoid submitting confidential acquisition, investment, or competitive targets unless disclosure to that API is acceptable. <br>
Risk: The skill's broad trigger language may cause it to be used for general AI questions beyond enterprise research. <br>
Mitigation: Narrow local trigger or routing language so the skill is used for AI-company research, competitor scans, financing analysis, and related enterprise profiling tasks. <br>
Risk: Company, financing, team, and competitive information may be incomplete or time-sensitive. <br>
Mitigation: State coverage boundaries when samples are sparse and supplement with appropriate recent-news or public-source checks for current events. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiqizhixin/ai-enterprise-profiler) <br>
- [Jiqizhixin Data Service](https://www.jiqizhixin.com/data-service) <br>
- [api-v1-enterprises.md](references/api-v1-enterprises.md) <br>
- [keyword_reference.md](references/keyword_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, structured tables, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JQZX_API_TOKEN for authenticated enterprise search through the disclosed Jiqizhixin API.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
