## Description: <br>
Sync your AI coding stats to Code Card - beautiful, shareable developer profiles <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eibrahim](https://clawhub.ai/user/eibrahim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure and run Code Card CLI commands that sync Claude Code, Codex, and OpenClaw coding-session statistics into a shareable Code Card profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync commands can send AI coding-session statistics to Code Card. <br>
Mitigation: Review Code Card's CLI behavior and privacy terms before syncing, and run the skill only when sharing those statistics is acceptable. <br>
Risk: The setup stores a local Code Card API key that could be exposed through logs or shell output. <br>
Mitigation: Do not paste or log the API key, and treat the local configuration file as sensitive. <br>
Risk: Using `npx code-card@latest` can execute a newly published package version without prior review. <br>
Mitigation: Pin a reviewed package version when operating in controlled or production-like environments. <br>
Risk: Recommended cron jobs can create recurring background uploads of coding-session data. <br>
Mitigation: Add cron jobs only after confirming ongoing automatic syncs are desired and approved. <br>


## Reference(s): <br>
- [Code Card website](https://www.codecard.dev) <br>
- [Code Card npm package](https://www.npmjs.com/package/code-card) <br>
- [ClawHub skill page](https://clawhub.ai/eibrahim/code-card-sync) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, sync, status, profile, and optional cron command guidance; requires Node.js 18+ with node and npx available.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
