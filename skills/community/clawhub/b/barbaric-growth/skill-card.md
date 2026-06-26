## Description: <br>
Automates GitHub trend research, ByteRover knowledge capture, OpenMOSS task logging, and StarOffice status updates for autonomous knowledge creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jokerli530](https://clawhub.ai/user/jokerli530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run an autonomous research loop that finds GitHub projects, analyzes them, records knowledge, creates local tasks, and updates status dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence identifies autonomous research behavior with local task creation, dashboard updates, and persistent memory writes. <br>
Mitigation: Install only when autonomous local workflow changes are intended, and review generated tasks, status updates, and memory writes before relying on them. <br>
Risk: The release evidence reports under-scoped background monitoring and a hardcoded external service credential. <br>
Mitigation: Remove and rotate the embedded EvoMap secret, require user-provided scoped credentials, and start monitoring only after explicit opt-in with a clear uninstall path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jokerli530/barbaric-growth) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and local status files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write persistent local task, token, monitor, and memory state under the user's OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
