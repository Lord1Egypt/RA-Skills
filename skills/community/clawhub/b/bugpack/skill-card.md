## Description: <br>
BugPack - AI-powered bug tracking and fixing toolkit. List bugs, view bug details with screenshots, and fix bugs automatically. Includes three workflows: list-bugs, view-bug, fix-bug. Requires BugPack server running locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duhuazhu](https://clawhub.ai/user/duhuazhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use BugPack to inspect locally tracked bugs, review screenshots and related files, apply fixes, and update bug status through a local BugPack server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can edit source code and update local bug status. <br>
Mitigation: Review source-code diffs and BugPack status updates before relying on a bug as fixed. <br>
Risk: The workflow starts a local helper through npx bugpack-mcp. <br>
Mitigation: Verify the npm package and consider pinning a trusted version before running it. <br>


## Reference(s): <br>
- [BugPack on ClawHub](https://clawhub.ai/duhuazhu/bugpack) <br>
- [duhuazhu publisher profile](https://clawhub.ai/user/duhuazhu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with API examples, shell commands, and code-change guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source-code edits and local BugPack status updates after user review.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
