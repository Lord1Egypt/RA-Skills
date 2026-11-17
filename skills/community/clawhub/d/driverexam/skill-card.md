## Description:

获取小车/客车/货车/摩托车科目一与科目四题库。当用户说：来几道驾考科目一题、摩托车科四模拟，或类似驾考刷题时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch Chinese driver's license exam practice questions for small cars, buses, trucks, and motorcycles across subject one and subject four. It supports guided practice sessions where the agent presents questions, checks answers, and explains the official answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exam query parameters and the JISU_API_KEY are sent to JisuAPI.

Mitigation: Set JISU_API_KEY only as an environment variable, avoid personal or sensitive information in request fields, and use the minimum parameters needed for the practice session.

Risk: The skill depends on JisuAPI authorization, quotas, and service availability.

Mitigation: Confirm the API key has access to the driver exam API and handle returned API errors or rate limits before relying on the results in a practice workflow.

## Reference(s):

- [JisuAPI Driver Exam API Documentation](https://www.jisuapi.com/api/driverexam/)
- [JisuAPI Website](https://www.jisuapi.com/)
- [ClawHub Driver Exam Skill Page](https://clawhub.ai/jisuapi/skills/driverexam)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON from the command-line helper, typically summarized by the agent as practice questions, answers, and explanations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the JISU_API_KEY environment variable.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
