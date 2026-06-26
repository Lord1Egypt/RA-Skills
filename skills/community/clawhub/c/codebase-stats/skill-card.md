## Description: <br>
Codebase Stats analyzes local projects for lines of code, language distribution, simplified function complexity, comment ratio, dependency counts, largest files, and tech debt indicators across 40+ languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect a codebase's size, language mix, complexity hotspots, dependency footprint, and maintenance signals before planning or reviewing engineering work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads local project files and reports metrics for the selected directory. <br>
Mitigation: Run it only against specific code folders intended for analysis and avoid broad home or secrets-containing directories. <br>
Risk: Using --output can overwrite an existing file at the chosen path. <br>
Mitigation: Choose an explicit report filename and confirm it is safe to replace before running with --output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/codebase-stats) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Terminal text, Markdown, or JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can optionally write a report file with --output; scans local files in the selected project directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
