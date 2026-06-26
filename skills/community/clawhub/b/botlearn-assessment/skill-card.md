## Description: <br>
botlearn-assessment runs a five-dimension BotLearn capability self-assessment covering reasoning, retrieval, creation, execution, and orchestration, then scores the run and generates reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvinxhk](https://clawhub.ai/user/calvinxhk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to benchmark an agent's reasoning, retrieval, content creation, execution, and tool orchestration capabilities and to track results over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Assessment prompts, answers, and generated history files may contain sensitive or proprietary information. <br>
Mitigation: Avoid using sensitive prompts or proprietary data in assessments, and review generated reports before sharing them. <br>
Risk: Generated HTML or SVG reports may be unsafe if the underlying JSON was manually edited or came from an untrusted source. <br>
Mitigation: Open generated reports only when the report data was produced locally or otherwise trusted. <br>
Risk: Questions that require unavailable tools are skipped and receive a score of 0, which can affect benchmark interpretation. <br>
Mitigation: Review skipped-question status and tool availability before comparing results across runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/calvinxhk/botlearn-assessment) <br>
- [README](README.md) <br>
- [Full exam flow](flows/full-exam.md) <br>
- [Exam execution flow](flows/exam-execution.md) <br>
- [Report generation flow](flows/generate-report.md) <br>
- [Scoring strategy](strategies/scoring.md) <br>
- [Exam report schema](assets/exam-report-schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses plus generated Markdown, HTML, JSON, and SVG report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Node.js report renderers when available and writes assessment history under results/.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
