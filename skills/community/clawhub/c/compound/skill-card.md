## Description: <br>
Calculate compound interest and investment growth using financial formulas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to run compound-interest calculations, compare investment rates, project savings growth, generate schedules and tables, and export calculation history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calculation inputs and results are saved locally in ~/.compound/data.jsonl. <br>
Mitigation: Use the skill only for data you are comfortable storing locally, keep the history file in a private location, and delete it when retention is not desired. <br>
Risk: Export can write to a user-provided OUTPUT path and may overwrite existing files. <br>
Mitigation: Choose export paths deliberately, avoid sensitive shared locations, and review the target file before running export. <br>
Risk: Financial projections can be mistaken for advice or guaranteed outcomes. <br>
Mitigation: Treat outputs as calculation aids and verify assumptions, rates, and time periods before using results for financial decisions. <br>


## Reference(s): <br>
- [Compound skill page](https://clawhub.ai/xueyetianya/compound) <br>
- [Publisher profile](https://clawhub.ai/user/xueyetianya) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text output with optional JSON, CSV, or JSONL export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local calculation history to ~/.compound/data.jsonl and configuration to ~/.compound/config.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
