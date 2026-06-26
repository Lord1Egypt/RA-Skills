## Description: <br>
为求职者基于本地求职档案和岗位 JD 生成个性化 BOSS 直聘打招呼话术，并支持多岗位匹配排序和截图 JD 识别确认。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KaguraNanaga](https://clawhub.ai/user/KaguraNanaga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and career-assistance agents use this skill to draft tailored BOSS Zhipin greeting messages from a saved job-search profile and one or more job descriptions. It can compare multiple JDs, rank fit, and ask for confirmation after screenshot-based JD extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves detailed resume, salary, preference, and job-search profile information locally. <br>
Mitigation: Use it only when local retention is acceptable, avoid pasting sensitive details that should not be retained, and confirm how to view, update, or delete the saved profile. <br>
Risk: The artifact requests Bash permission even though the documented workflow does not need shell execution. <br>
Mitigation: Remove or disable Bash permission before deployment unless a reviewed operational need is added. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/KaguraNanaga/boss-greeting) <br>
- [Greeting examples](references/examples.md) <br>
- [Profile template](references/profile-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Plain text greeting messages, Markdown ranking tables, and Markdown profile updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated greetings are constrained to 200-250 Chinese characters and include a word count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
