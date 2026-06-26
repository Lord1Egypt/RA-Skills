## Description: <br>
Automatically runs Python, C, and x86_64 assembly code, uses an LLM to repair failures, and returns the revised code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyk-404](https://clawhub.ai/user/zyk-404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to test Python, C, or x86_64 assembly snippets and receive a repaired version when execution, compilation, assembly, or linking fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs and may re-run submitted Python, C, or assembly code locally without an approval gate. <br>
Mitigation: Use it only in a disposable sandbox, virtual machine, or container intended for local code execution. <br>
Risk: Submitted code and error output may be sent to an LLM for repair. <br>
Mitigation: Do not submit secrets, private keys, proprietary code, or untrusted code unless local execution and LLM processing are acceptable. <br>
Risk: Automatically repaired code may still be incorrect or unsafe. <br>
Mitigation: Review the repaired code before relying on it or allowing it to run again. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zyk-404/code-run-auto-fix) <br>


## Skill Output: <br>
**Output Type(s):** [code, text] <br>
**Output Format:** [String containing the repaired source code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs submitted code locally and may make one LLM repair attempt before returning code.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
