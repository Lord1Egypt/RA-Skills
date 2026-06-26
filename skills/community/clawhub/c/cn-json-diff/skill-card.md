## Description: <br>
Compare two JSON files and show differences across nested structures, arrays, and changed values using Python standard library tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare two local JSON files and identify added, removed, type-changed, or value-changed paths during debugging, review, or configuration checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compared JSON values may be printed in terminal output, which can expose sensitive file contents in logs or shared sessions. <br>
Mitigation: Run the skill only on JSON files whose values may be displayed, or redact sensitive fields before comparison. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/freedompixels/cn-json-diff) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON-formatted terminal output with difference paths and counts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads two user-provided local JSON files and reports differences without network access or external dependencies.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
