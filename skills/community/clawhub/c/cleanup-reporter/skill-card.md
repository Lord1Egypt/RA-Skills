## Description: <br>
Scan your machine for large directories, duplicate files, and stale resume files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MalavyaRaval](https://clawhub.ai/user/MalavyaRaval) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local machine users use this skill to scan disk usage, identify duplicate files, find stale resume files, and generate a local cleanup report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated reports and duplicate-file listing may expose private local file paths. <br>
Mitigation: Review report contents before sharing them, and delete ~/reports/cleanup_report_*.md and /tmp/duplicates.txt when they are no longer needed. <br>
Risk: The scanner targets /mnt/c/Users/malav, which may not match the installing user's machine. <br>
Mitigation: Confirm or adjust the scan path before running the script. <br>
Risk: The skill depends on local shell tools for disk analysis and duplicate detection. <br>
Mitigation: Install ncdu and rdfind from trusted package sources before use. <br>


## Reference(s): <br>
- [Cleanup Reporter on ClawHub](https://clawhub.ai/MalavyaRaval/cleanup-reporter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown report with shell command status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a dated cleanup report under ~/reports and a temporary duplicate-file listing under /tmp.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
