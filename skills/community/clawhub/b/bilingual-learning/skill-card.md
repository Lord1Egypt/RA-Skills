## Description: <br>
双语学习 Skill - CN → EN。当用户使用此 skill 时，agent 会在最终输出前强制进行双语学习处理，包括难度调整、考试检测和双语输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haodong-lei-ray](https://clawhub.ai/user/haodong-lei-ray) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to add passive CN-to-EN bilingual learning, vocabulary checks, and spelling quizzes into normal coding or conversational responses. It also provides local CLI utilities for managing new-word and known-word lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save vocabulary history in local data files. <br>
Mitigation: Use it only when local vocabulary persistence is acceptable, and review stored word lists as part of normal workspace hygiene. <br>
Risk: Delete and clear commands can remove saved word lists. <br>
Mitigation: Review command targets before running delete or clear operations, especially when managing shared or long-lived vocabulary data. <br>
Risk: The skill changes response style by adding bilingual learning checks and quizzes. <br>
Mitigation: Enable it only in conversations where bilingual learning content is desired. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/haodong-lei-ray/bilingual-learning) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal text with optional JSON-backed local vocabulary records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local vocabulary data files for new and known words.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
