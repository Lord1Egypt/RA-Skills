## Description: <br>
Drive a GitHub pull request through an iterative review-and-fix loop until review feedback and CI are clear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevetdp](https://clawhub.ai/user/stevetdp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill when they want an agent to manage a GitHub PR after it is opened: collect review feedback, implement fixes, preserve the requested commit history, push updates, resolve threads, and monitor CI until the requested stop condition is met. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may push commits, resolve review threads, and update PR history on the target repository. <br>
Mitigation: Use it only with a clearly scoped repository, PR, branch, and history strategy; limit force-with-lease to the active PR head branch. <br>
Risk: GitHub credentials can grant repository write access. <br>
Mitigation: Prefer existing GitHub MCP or CLI authentication, scope GITHUB_TOKEN to the intended repository and branch, and do not paste tokens into chat. <br>
Risk: The review loop can keep polling for reviews and CI until a completion signal is met. <br>
Mitigation: Define the expected stop condition and treat missing permissions, ambiguous targets, or unavailable reviewer systems as blockers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevetdp/gh-pr-review-loop) <br>
- [Publisher profile](https://clawhub.ai/user/stevetdp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, code-change summaries, and PR or CI status updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include code changes, commits, PR updates, review-thread resolutions, and CI monitoring when the host has scoped GitHub access.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
