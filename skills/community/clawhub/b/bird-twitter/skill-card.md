## Description: <br>
Twitter/X CLI wrapper using bird for posting tweets, replying, reading, searching, and managing timelines through a GraphQL-based X CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chuhuilove](https://clawhub.ai/user/chuhuilove) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to run bird CLI workflows for Twitter/X account actions such as tweeting, replying, reading timelines, searching posts, and checking credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses live Twitter/X session cookies and can perform real account actions. <br>
Mitigation: Provide AUTH_TOKEN and CT0 only in a trusted environment, treat them like passwords, and explicitly review prompts before tweet, reply, follow, or unfollow actions. <br>
Risk: Session cookies may be exposed through logs, shell history, or untrusted command contexts. <br>
Mitigation: Do not commit, log, share, or paste AUTH_TOKEN or CT0 into untrusted shells; revoke or refresh the Twitter/X session if exposure is suspected. <br>


## Reference(s): <br>
- [Bird Twitter ClawHub release](https://clawhub.ai/chuhuilove/bird-twitter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON or plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request execution of bird CLI commands that use AUTH_TOKEN and CT0 session cookies.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
