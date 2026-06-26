## Description: <br>
Designs agent-evaluated flow tests for browser tasks, LLM outputs, and tool workflows. Invoke when exact asserts are brittle and semantic success matters more than literal equality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qipengguo](https://clawhub.ai/user/qipengguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to design flow tests for browser tasks, LLM outputs, and multi-tool workflows where exact assertions are brittle. It helps separate deterministic checks from semantic evaluation and define evidence, rubrics, and bounded verdicts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flow-test evidence may capture credentials, secrets, or unnecessary private page contents if the test scope is too broad. <br>
Mitigation: Collect only the evidence needed for the rubric and exclude credentials, secrets, and unrelated private content from test logs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Structured Markdown test specification with deterministic checks, evidence schema, semantic rubric, execution notes, and final verdict format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a bounded verdict format of pass, fail, or needs_review.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
