## Description: <br>
Scan and analyze installed skills. Use when user wants to (1) scan a specific skill directory to view its name, description, and details, or (2) scan all installed skills to list all available skills with their names and descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect a specific skill directory or all installed skills under a chosen directory and view metadata from SKILL.md files, including names, paths, and descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill setup installs the external skill-361 Python CLI package. <br>
Mitigation: Install only when the package source is trusted and review the package before use in sensitive environments. <br>
Risk: The scan-all workflow recursively reads skill metadata files under the user-provided directory. <br>
Mitigation: Run scans against a specific skill folder or the OpenClaw skills directory instead of broad private directories. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/goog/361) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and text scan summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports metadata for user-selected skill paths and recursively discovered SKILL.md files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
