## Description: <br>
Guides agents through testing and benchmarking LLM agents with behavioral tests, capability assessments, reliability metrics, and production monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, quality engineers, and agent builders use this skill to design evaluations for LLM agents, including statistical test runs, behavioral contracts, adversarial checks, and reliability tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, benchmark cases, transcripts, or production traces may be sent to a third-party API. <br>
Mitigation: Review the external setup guide, provide SKILLBOSS_API_KEY only when the API Hub is intended, and redact secrets, regulated data, and sensitive traces before use. <br>
Risk: Evaluation guidance can produce misleading conclusions if benchmarks do not match production behavior. <br>
Mitigation: Pair benchmark results with behavioral regression tests, adversarial checks, and production-oriented reliability metrics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abel-agent-evaluation) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API integration examples that require SKILLBOSS_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
