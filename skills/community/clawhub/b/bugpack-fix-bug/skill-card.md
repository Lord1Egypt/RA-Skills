## Description: <br>
Fix a bug from BugPack by reading its context, locating code, applying fixes, and updating status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duhuazhu](https://clawhub.ai/user/duhuazhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill when asked to fix a BugPack issue: it fetches bug context, analyzes screenshots and related files, edits the relevant code, and updates the bug status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may apply an incorrect code change or update the wrong BugPack issue status. <br>
Mitigation: Review the diff, run relevant tests, and confirm the correct bug ID before relying on the fixed status. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON and shell-style API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source edits and BugPack status updates performed by the agent.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
