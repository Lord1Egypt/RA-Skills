## Description: <br>
Advanced filesystem operations - listing, searching, batch processing, and directory analysis for Clawdbot <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq258067284](https://clawhub.ai/user/qq258067284) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to list, search, copy, visualize, and analyze local files and directories with filtering and safety-oriented defaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is incomplete, so the filesystem executable and its safety controls cannot be verified from the submitted artifact. <br>
Mitigation: Install only after inspecting the actual executable from a trusted source or receiving a complete package from the publisher. <br>
Risk: The skill requests broad local filesystem access and can perform copy or overwrite-oriented workflows. <br>
Mitigation: Limit use to specific project folders, require confirmation for copy or overwrite actions, and run dry-run previews before changes. <br>
Risk: Autonomous filesystem access could expose home directories, credentials, or system paths. <br>
Mitigation: Avoid granting access to sensitive directories and keep protected system paths outside the agent's working scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qq258067284/filesystem2) <br>
- [Publisher profile](https://clawhub.ai/user/qq258067284) <br>
- [Declared repository](https://github.com/gtrusler/clawdbot-filesystem) <br>
- [Declared issue tracker](https://github.com/gtrusler/clawdbot-filesystem/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce file listings, search results, tree views, copy previews, and directory statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
