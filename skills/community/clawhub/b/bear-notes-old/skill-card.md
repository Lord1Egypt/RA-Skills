## Description: <br>
Create, search, and manage Bear notes via grizzly CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangfeng1995](https://clawhub.ai/user/huangfeng1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers on macOS use this skill to create, read, search, append to, and organize Bear notes through the grizzly CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local Bear API token for some note operations. <br>
Mitigation: Store the token outside shell history, restrict permissions on ~/.config/grizzly and the token file, and rotate or revoke the token when no longer needed. <br>
Risk: The skill depends on the third-party grizzly CLI to access or modify local Bear notes. <br>
Mitigation: Install and use the skill only when the grizzly CLI is trusted for local Bear note operations. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/huangfeng1995/bear-notes-old) <br>
- [Bear app](https://bear.app) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and TOML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce JSON when grizzly callbacks are enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
