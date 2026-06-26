## Description: <br>
Tasks and habits that live in a plain markdown file on your machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tallhamn](https://clawhub.ai/user/tallhamn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to let an agent manage local task and habit lists through the ClawKeeper CLI while storing the data in markdown files under CLAWKEEPER_DIR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and writes user-selected local task and habit data. <br>
Mitigation: Set CLAWKEEPER_DIR to a dedicated folder for non-sensitive task data. <br>
Risk: Fuzzy text matching can modify or delete the wrong task or habit. <br>
Mitigation: Prefer stable item IDs for edits, completions, and deletions. <br>
Risk: The skill depends on an external npm package named clawkeeper. <br>
Mitigation: Install only if you trust the npm package and its release source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tallhamn/clawkeeper) <br>
- [Publisher profile](https://clawhub.ai/user/tallhamn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CLAWKEEPER_DIR to select the local markdown storage directory; command responses report ok/data or ok/error.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
