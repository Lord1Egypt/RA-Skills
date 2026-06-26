## Description: <br>
Track and manage electrochemistry samples from synthesis to characterization with data linking, event logging, search, export, and dashboard visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xrayxiaoruiyang-pixel](https://clawhub.ai/user/xrayxiaoruiyang-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Electrochemistry lab researchers and engineers use this skill to track physical sample inventory, synthesis metadata, characterization file links, experimental events, exports, and dashboards in a local SQLite database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk CSV or JSON imports can overwrite sample records when imported rows reuse existing sample_id values. <br>
Mitigation: Back up samples.db before bulk imports and review incoming sample_id values for duplicates. <br>
Risk: Linked file paths and free-text notes are stored in the local database and may reference sensitive lab data. <br>
Mitigation: Link only relevant files and avoid storing unrelated sensitive details in sample notes or attachment descriptions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xrayxiaoruiyang-pixel/ec-sample-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/xrayxiaoruiyang-pixel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Command-line text output, CSV, JSON, Markdown reports, SQLite database records, and PNG dashboard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local samples.db records, config.yaml settings, exported sample files, linked file-path metadata, and dashboard images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
