## Description: <br>
Deploy and manage Fly.io apps via CLI - apps, machines, volumes, secrets, certificates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Melvynx](https://clawhub.ai/user/Melvynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, authenticate, deploy, inspect, and administer Fly.io applications and related resources through flyctl commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward Fly.io commands that deploy, scale, alter secrets, open SSH or proxy sessions, or destroy resources. <br>
Mitigation: Verify the active Fly.io account, app, region, machine, volume, and secret names, and require explicit confirmation before resource-changing commands. <br>


## Reference(s): <br>
- [Fly.io install script](https://fly.io/install.sh) <br>
- [ClawHub skill page](https://clawhub.ai/Melvynx/fly) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Use --json for programmatic flyctl command output where supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
