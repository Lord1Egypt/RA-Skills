## Description: <br>
学历教育与职业培训找资料工具。学历教育包括考研（公共课/专业课真题）、专升本、自考等；职业培训包括考公（行测/申论）、教师资格证、经济师、建造师、会计师、法律职业资格等。支持三种类型：找试题试卷、找教辅资料、找备考课程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kayy123](https://clawhub.ai/user/kayy123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners, exam candidates, and agents use this skill to search for education and vocational training materials such as exam papers, study aids, and preparation courses. It is intended for finding and presenting resource links for supported Chinese education and certification exam topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary says the skill performs daily update checks and may automatically replace the installed skill. <br>
Mitigation: Review release changes before installing updates and prefer an opt-in update flow for managed deployments. <br>
Risk: The server security guidance notes external Baidu requests over HTTP and transmission of device or network details. <br>
Mitigation: Use only with non-sensitive queries, review network behavior before deployment, and prefer a version that removes IP and hostname transmission and uses protected transport. <br>
Risk: The server security summary says the skill asks users to paste an API key into chat. <br>
Mitigation: Do not paste API keys into chat; configure credentials through a secure secret store or environment variable. <br>
Risk: Fallback search behavior can return external resources that may not fully match the user's requested conditions. <br>
Mitigation: Review returned links and resource metadata before opening, downloading, or sharing them with end users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kayy123/education-search) <br>
- [API documentation](references/api.md) <br>
- [Auto-update documentation](references/auto-update.md) <br>
- [Baidu search configuration](references/baidu-search-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance, API calls] <br>
**Output Format:** [Markdown tables and concise Chinese-language guidance, with shell commands or configuration steps when setup or update actions are needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Resource results are presented as source, year, category, subject, title, and link fields; counts should match displayed table rows.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
