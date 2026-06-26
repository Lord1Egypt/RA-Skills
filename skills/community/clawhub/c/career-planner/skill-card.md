## Description: <br>
A career planning advisor that conducts a structured intake interview, validates options with market research when needed, and produces a personalized career plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzw6](https://clawhub.ai/user/jzw6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals use this skill when they need career direction, are considering a job or career change, or want role recommendations based on their background, skills, interests, constraints, and goals. The agent guides the conversation, synthesizes the user's profile, researches relevant job-market signals when needed, and prepares an actionable career plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for sensitive career context such as salary goals, constraints, employers, and work history. <br>
Mitigation: Users should avoid sharing names, employers, or details they do not want saved, and can ask the agent to anonymize the plan or keep advice in chat. <br>
Risk: The skill creates a downloadable Markdown report that may contain personal career information. <br>
Mitigation: Review the report before sharing it, remove private details, and store it only in locations appropriate for personal career records. <br>
Risk: Salary benchmarks and job-demand signals can become outdated or vary by location. <br>
Mitigation: When web research is used, cite sources in the report and verify current local salary and hiring data before making decisions. <br>


## Reference(s): <br>
- [Report Template](references/report-template.md) <br>
- [Role Database](references/role-database.md) <br>
- [Skill-to-Role Mapping Reference](references/skill-to-role-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Conversational guidance and a downloadable Markdown career plan report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to Chinese unless the user prefers English; report content is personalized from user-provided career information and may cite web research sources when market data is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
