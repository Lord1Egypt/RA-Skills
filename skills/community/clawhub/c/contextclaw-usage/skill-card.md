## Description: <br>
Manage and analyze OpenClaw sessions by checking usage, pruning old sessions, cleaning orphaned files, and viewing stats via CLI or dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rmruss2022](https://clawhub.ai/user/rmruss2022) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect session storage, identify large or old sessions, preview cleanup actions, and run ContextClaw commands for pruning or orphan cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live prune or orphan cleanup commands can delete OpenClaw session files. <br>
Mitigation: Run analyze and dry-run cleanup first, review the deletion preview, back up important sessions, and only approve live cleanup when the proposed deletion set is acceptable. <br>
Risk: The ContextClaw package reads OpenClaw session history to provide analysis and cleanup. <br>
Mitigation: Install and use the package only if the publisher and package are trusted and session-history access is acceptable. <br>


## Reference(s): <br>
- [ContextClaw Plugin Usage on ClawHub](https://clawhub.ai/rmruss2022/contextclaw-usage) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend dry-run cleanup commands, dashboard checks, status checks, and live cleanup commands after review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
