## Description: <br>
龙虾MBTI性格诊断。基于用户与龙虾的互动模式，分析并生成龙虾的MBTI人格报告。当用户说"测测我的MBTI"、"你是什么龙虾"、"龙虾诊断"时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyang0807](https://clawhub.ai/user/xiaoyang0807) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users invoke the skill to generate a playful MBTI-style personality report from their recent natural-language interactions with the agent. The skill also provides fallback guidance when there is no interaction history or too little data for a confident report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill profiles recent chat history and memory to infer personality traits without a clear opt-in. <br>
Mitigation: Install only when comfortable with that review, and treat generated reports as private until the user has reviewed them. <br>
Risk: Generated reports are designed to be shareable and may expose personal interaction patterns. <br>
Mitigation: Review the report before sharing or posting screenshots. <br>
Risk: The artifact includes a raw GitHub clone/pull install path. <br>
Mitigation: Prefer the ClawHub install path unless the repository has been independently verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoyang0807/claw-self-mbti) <br>
- [Project homepage](https://github.com/xiaoyang0807/claw-mbti) <br>
- [README](artifact/README.md) <br>
- [Diagnosis reference manual](artifact/reference.md) <br>
- [16-type reference](artifact/types.md) <br>
- [Usage examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown personality diagnosis report with tables, short fallback guidance, or installation/update commands when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are based on recent chat and memory signals and may be formatted for screenshot sharing.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata; artifact frontmatter says 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
