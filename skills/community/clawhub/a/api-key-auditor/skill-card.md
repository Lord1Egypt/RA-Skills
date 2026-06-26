## Description: <br>
Scans files under ~/.openclaw/workspace/skills for hardcoded API keys, tokens, and secrets, checks whether they are registered in openclaw.json env.vars, and can migrate unregistered credentials into that config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lemonGGGit](https://clawhub.ai/user/lemonGGGit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw skill directories for hardcoded credentials and understand whether each finding is already integrated, mcporter-managed, or still needs migration. It can also propose and perform migration into openclaw.json when run with --fix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: --fix can broaden secret exposure by writing discovered credentials into openclaw.json. <br>
Mitigation: Run the read-only audit first, review every finding, and back up ~/.openclaw/openclaw.json before using --fix. <br>
Risk: mcporter-managed keys may be copied into OpenClaw config even though the documentation says they do not need migration. <br>
Mitigation: Treat mcporter-managed findings as review-required and avoid migrating them unless the operator intentionally wants those secrets centralized in OpenClaw config. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lemonGGGit/api-key-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/lemonGGGit) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console report with file locations, credential status labels, migration guidance, and optional openclaw.json updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only by default; --fix mode writes discovered unregistered credentials into openclaw.json env.vars.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
