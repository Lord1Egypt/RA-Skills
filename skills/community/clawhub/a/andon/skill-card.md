## Description: <br>
Andon is a local alert and production status-board tracker for adding, listing, searching, removing, exporting, and summarizing status entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations teams and agents use Andon to maintain a simple local status board for production alerts, task records, and operational notes. It supports command-line workflows for checking current status, managing entries, exporting records, and viewing basic statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local status records may contain operational or sensitive notes and are written to a user-controlled data directory. <br>
Mitigation: Keep ANDON_DIR pointed at a dedicated private folder and limit access to directories that are appropriate for operational records. <br>
Risk: The remove command deletes a selected entry from the local JSONL data file. <br>
Mitigation: Confirm the entry number before using remove and keep backups when records must be retained. <br>
Risk: Exports can create JSON or CSV files in the current working directory. <br>
Mitigation: Export only to directories where operational records can safely be stored and shared. <br>


## Reference(s): <br>
- [ClawHub Andon skill page](https://clawhub.ai/xueyetianya/andon) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes JSONL status records under ANDON_DIR or ~/.andon by default and can export JSON or CSV files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
