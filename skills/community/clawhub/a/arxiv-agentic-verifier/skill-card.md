## Description: <br>
Actively verifies Python and JavaScript code correctness by generating targeted test cases that expose logic flaws based on problem constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to check candidate Python or JavaScript solutions by generating targeted edge-case tests and comparing actual output against expected output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes submitted code directly without enforcing a sandbox. <br>
Mitigation: Run it only in a disposable sandbox or container with limited filesystem access, no secrets, and restricted networking. <br>
Risk: Code and problem details may be sent to OpenAI when an API key is configured. <br>
Mitigation: Use it only with code that is acceptable to share under the organization's data handling policy. <br>


## Reference(s): <br>
- [Scaling Agentic Verifier for Competitive Coding](https://arxiv.org/abs/2602.09012) <br>
- [ClawHub skill page](https://clawhub.ai/wanng-ide/arxiv-agentic-verifier) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [JSON-like verification results with console text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated test input, expected output, pass/fail status, failure reason, and runtime details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
