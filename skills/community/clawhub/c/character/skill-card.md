## Description:

MBTI 完整版或简版逐题作答，提交后获取性格类型结果。当用户说：我想测个 MBTI、给我性格测试题，或类似 MBTI 测评时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run a full or simplified MBTI questionnaire one question at a time, submit the collected answer codes, and return an MBTI personality result. Developers can also use its command-line modes to fetch questions, submit answers, or run a local interactive quiz.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quiz answers and answer codes are sent to JisuAPI to produce the MBTI result.

Mitigation: Use the skill only when users accept third-party processing, and avoid highly sensitive personal assessments unless that handling is acceptable.

Risk: The skill reads the JisuAPI credential from JISU_API_KEY and makes network requests to JisuAPI.

Mitigation: Store the API key in the environment and avoid exposing it in prompts, logs, or shared command output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/character)
- [JisuAPI](https://www.jisuapi.com/)
- [JisuAPI MBTI Personality Test API](https://www.jisuapi.com/api/character/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; quiz answers or answer codes are sent to JisuAPI for scoring.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
