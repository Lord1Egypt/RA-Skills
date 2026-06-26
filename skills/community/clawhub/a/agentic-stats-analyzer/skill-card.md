## Description: <br>
对候选队列执行描述性统计与组间比较，生成感染率对比、描述统计表、结果摘要与论文框架草案。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emergenceronearth](https://clawhub.ai/user/emergenceronearth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and analysis-focused agents use this skill to summarize candidate cohort data, compare infection rates between groups, and draft a paper structure from the available analysis dataset. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on /home/ubuntu/workspace/demo/mock_data/analysis.json, so stale or untrusted data can lead to misleading statistical summaries. <br>
Mitigation: Verify that analysis.json is the intended dataset and that its provenance is trusted before relying on generated findings. <br>
Risk: The skill reports status to localhost:5001/api/report, which may expose workflow status to an unexpected local service if the environment is misconfigured. <br>
Mitigation: Install only where that localhost reporting service is expected, or review the command before execution in other environments. <br>
Risk: The output includes research and paper-framework guidance that may be over-relied on for research or medical decisions. <br>
Mitigation: Treat the generated analysis as a draft and have a qualified reviewer validate the data, methods, and conclusions before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emergenceronearth/agentic-stats-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with tables, findings, cautions, paper outline, and inline bash status-report commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a fixed local analysis.json dataset and reports progress to an expected localhost service.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
