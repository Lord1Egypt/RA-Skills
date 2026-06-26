## Description: <br>
FuncPulse helps QA, product, and engineering teams map financial AI requirements, PRDs, test cases, and multi-repo code changes into traceability matrices that expose coverage gaps, missing compliance evidence, defect priorities, and acceptance risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[start-fish](https://clawhub.ai/user/start-fish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, developers, and product teams use this skill to validate whether PRDs and test cases are covered by implementation changes, especially for financial AI, agent, model, and RAG workflows. It produces acceptance evidence such as coverage summaries, traceability matrices, defect lists, reproduction steps, and prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Validation reports and repository metadata may contain proprietary, regulated, internal, or financial AI information and may be uploaded over plain HTTP without a clear consent gate. <br>
Mitigation: Review generated reports before upload, use only data permitted to be sent to ai-testcase.jd.com, and prefer a local-only or HTTPS and consent-gated version for sensitive materials. <br>


## Reference(s): <br>
- [Financial AI Validation Playbook](references/financial-ai-validation-playbook.md) <br>
- [QA Analysis Methods](references/qa-analysis-methods.md) <br>
- [Test Validation Report Template](references/test-validation-report.md) <br>
- [Multi-Repo Analysis Guide](references/multi-repo-analysis.md) <br>
- [Test Case Traceability Guide](references/test-case-traceability.md) <br>
- [Code Change Test Coverage Guide](references/code-change-test-coverage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown business validation report with traceability matrices, coverage summaries, defect lists, reproduction steps, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create report files under a reports directory and may upload generated validation reports to the configured report API.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and package.json; artifact/_meta.json lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
