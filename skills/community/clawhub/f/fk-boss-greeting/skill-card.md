## Description: <br>
fk-boss-greeting helps an agent search Boss Zhipin for Java-oriented roles, filter excluded companies and job types, and send one-at-a-time recruiter greetings while tracking duplicates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huguiqi](https://clawhub.ai/user/huguiqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and their agents use this skill to find Java-related Boss Zhipin postings, apply blacklist and keyword filters, and send controlled recruiter greetings through the external boss CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Chrome Boss Zhipin login session to act as the user and send recruiter greetings. <br>
Mitigation: Review the external boss CLI source and package, confirm the active login and target recipient list, and run only when the user intends to send greetings. <br>
Risk: Scheduled or repeated runs can send many greetings without clear confirmation controls. <br>
Mitigation: Avoid scheduled runs unless they are monitored and can be disabled quickly; keep per-run limits and one-at-a-time sending enabled. <br>
Risk: Local logs may contain sensitive job-search history and recruiter interaction identifiers. <br>
Mitigation: Treat generated logs and tracking files as sensitive local data and remove or protect them according to the user's privacy needs. <br>


## Reference(s): <br>
- [filter-rules.json](references/filter-rules.json) <br>
- [kabi-boss-cli](https://github.com/jackwener/boss-cli) <br>
- [Boss Zhipin](https://www.zhipin.com) <br>
- [ClawHub release page](https://clawhub.ai/huguiqi/fk-boss-greeting) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke an external CLI that searches jobs, sends greetings, and writes local job-search logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
