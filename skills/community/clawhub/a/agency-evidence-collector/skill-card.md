## Description: <br>
Expert AI agent specializing in evidence collector. From The Agency (github.com/msitarzewski/agency-agents). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouqkt](https://clawhub.ai/user/zhouqkt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA reviewers use this agent to collect visual evidence, compare implementations against specifications, and produce evidence-backed quality reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to run a local QA script before review. <br>
Mitigation: Use it only in intended project directories and review qa-playwright-capture.sh before any execution. <br>
Risk: Screenshot-based QA can expose sensitive repository or application data. <br>
Mitigation: Avoid sensitive repos unless screenshots and local file inspection are acceptable for the review. <br>
Risk: The skill encourages a strongly skeptical, failure-oriented review posture. <br>
Mitigation: Treat each reported issue as a claim that must be supported by referenced evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouqkt/agency-evidence-collector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and evidence references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference screenshots and local test-result files generated during QA review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
