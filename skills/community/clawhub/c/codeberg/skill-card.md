## Description: <br>
Interact with Codeberg using the `tea` CLI. Use `tea issue`, `tea pr`, `tea actions`, and `tea api` for issues, PRs, Actions, and advanced queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[razzeee](https://clawhub.ai/user/razzeee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and maintainers use this skill to manage Codeberg repositories through the `tea` CLI, including issues, pull requests, Actions variables and secrets, API queries, and login setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through access-token setup and repository administration. <br>
Mitigation: Use a least-privilege Codeberg token, prefer secure credential storage or environment-based authentication, and install the skill only when repository administration is intended. <br>
Risk: Repository secret and variable commands can expose sensitive operational metadata in transcripts or logs. <br>
Mitigation: Avoid displaying secret names unless necessary and redact token, secret, and variable output before sharing logs or transcripts. <br>
Risk: Generated `tea api` and Actions commands can change or reveal repository state if run without review. <br>
Mitigation: Review commands before execution and scope repository access to the target owner and repository. <br>


## Reference(s): <br>
- [Codeberg](https://codeberg.org) <br>
- [Tea CLI Go module](https://code.gitea.io/tea) <br>
- [ClawHub Codeberg Skill](https://clawhub.ai/razzeee/codeberg) <br>
- [razzeee ClawHub Profile](https://clawhub.ai/user/razzeee) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the `tea` CLI and may require `jq` for examples that filter API responses.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
