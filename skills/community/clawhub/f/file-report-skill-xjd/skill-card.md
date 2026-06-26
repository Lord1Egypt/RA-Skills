## Description: <br>
Counts file types in a specified directory and returns a Markdown report with the path, timestamp, file-type table, and total count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xujiangdong](https://clawhub.ai/user/xujiangdong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other ClawHub users use this skill when they want an agent to inspect a chosen directory, count files by extension without recursing into subdirectories, and return a concise Markdown summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to inspect local directory contents, which can expose file names and file types from directories the user selects. <br>
Mitigation: Install only when this directory inspection is desired, and grant read-only filesystem access when the host environment supports it. <br>
Risk: The artifact declares filesystem.write even though the stated behavior returns the Markdown report in chat. <br>
Mitigation: Prefer read-only access for normal use and avoid granting write access unless a deployment adds a separate file-writing workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xujiangdong/file-report-skill-xjd) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report includes the inspected directory path, timestamp, file-type counts, files without extensions, and total file count.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
