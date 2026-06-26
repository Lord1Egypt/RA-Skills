## Description: <br>
Generates ranked improvement candidates for a target skill from feedback signals, failure traces, and evaluator baseline failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this tool to generate structured improvement candidates for a target skill, incorporate prior failure traces, and prioritize changes from feedback or evaluator failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send target SKILL.md excerpts and evaluator failure details through a local Claude CLI path. <br>
Mitigation: Use sanitized inputs, avoid secrets and private benchmark data in sources or traces, and require review before applying generated changes. <br>
Risk: Generated improvement proposals may be incorrect or misleading if applied directly. <br>
Mitigation: Review candidate JSON, scan the target skill, and run relevant tests or evaluation gates before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanyasheng/auto-improvement-generator) <br>
- [Publisher profile](https://clawhub.ai/user/lanyasheng) <br>


## Skill Output: <br>
**Output Type(s):** [json, text, shell commands, guidance] <br>
**Output Format:** [JSON candidate artifact with a stdout path to the written file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ranked candidate objects with IDs, categories, risk levels, execution plans, failure trace status, and a truth anchor; human review is needed before applying prompt, workflow, test, or code changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
