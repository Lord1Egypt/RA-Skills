## Description: <br>
Agentspace helps developers share and observe an AI dev agent's selected workspace from a browser using the ascli CLI and agentspace.so dev API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to sync, inspect, and share a named development folder during AI agent runs, build debugging, output review, and dev-to-dev handoff. It is intended for live workspace observability and share-link workflows around files the user explicitly selects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected development folder is uploaded to a third-party service and may contain sensitive, proprietary, or unnecessary files. <br>
Mitigation: Confirm the exact path before syncing or sharing, choose the narrowest folder possible, and avoid sharing secrets or proprietary files. <br>
Risk: Generated share links can expose workspace contents or permit edits when edit access is selected. <br>
Mitigation: Prefer view-only links unless edit access is needed, review recipients before sharing, and avoid inventing URLs; return only URLs printed by ascli. <br>
Risk: The .ascli.json binding contains a workspace id and anonymous claim token that should be treated like an access token. <br>
Mitigation: Avoid exposing .ascli.json in broad shares and rotate or refresh the workspace if the token may have been disclosed. <br>
Risk: Using an @latest npm invocation can execute a newer package version than the one previously reviewed. <br>
Mitigation: Consider pinning or reviewing the @agentspace-so/ascli package version before running npm or npx commands. <br>


## Reference(s): <br>
- [Agentspace homepage](https://agentspace.so) <br>
- [ClawHub release page](https://clawhub.ai/kalvinrv/agentspace-dev) <br>
- [Agent Space Commands](references/commands.md) <br>
- [Developer reference for agentspace dev sessions](references/developer.md) <br>
- [npm @agentspace-so/ascli](https://www.npmjs.com/package/@agentspace-so/ascli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and URL guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ascli commands, workspace/share URLs returned by the CLI, and path-confirmation guidance.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
