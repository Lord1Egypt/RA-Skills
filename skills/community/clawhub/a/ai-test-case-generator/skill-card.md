## Description: <br>
Generates structured Chinese Markdown test cases from requirements using common test design methods, with optional conversion to Excel through an external service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LianWilliam](https://clawhub.ai/user/LianWilliam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA teams, developers, and quality assurance departments use this skill to turn requirements into prioritized test cases with steps, assertions, tags, boundary coverage, and negative-path coverage. It is suited for feature test design and supplemental coverage analysis before manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Excel export workflow can send generated content to an external HTTP service without a clear consent step or secure transport. <br>
Mitigation: Review generated Markdown locally and avoid automatic Excel conversion for confidential requirements; use a local converter or a trusted HTTPS service for sensitive product, customer, financial, or unreleased feature details. <br>
Risk: Generated test cases may appear complete while still missing domain-specific risks or acceptance criteria. <br>
Mitigation: Have a qualified tester review coverage, priorities, expected results, and negative paths against the source requirements before using the cases for release decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LianWilliam/ai-test-case-generator) <br>
- [Markdown-to-Excel conversion endpoint](http://office-tools.wh.ctrm.5636cloud.com/api/v1/office/md-to-excel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown test cases plus an optional Markdown Excel download link] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language output with P0-P3 priorities, test-type tags, step-by-step assertions, and optional external Excel conversion.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
