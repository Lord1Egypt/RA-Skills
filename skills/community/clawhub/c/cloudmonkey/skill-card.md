## Description: <br>
Manage Apache CloudStack infrastructure using the cloudmonkey (cmk) CLI - list/start/stop/destroy VMs, manage networks, volumes, snapshots, and run any CloudStack API command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiranchavala](https://clawhub.ai/user/kiranchavala) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to manage Apache CloudStack resources through the local cloudmonkey CLI, including virtual machines, networks, volumes, snapshots, templates, public IP addresses, profiles, and output formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to local CloudStack profiles and infrastructure operations. <br>
Mitigation: Use a dedicated least-privilege cmk profile and avoid exposing production or administrator profiles. <br>
Risk: Mutating commands such as starting, stopping, destroying, expunging, or switching profiles can affect running infrastructure. <br>
Mitigation: Require explicit user approval for every mutating command and any profile switch. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local cmk executable and configured CloudStack profile.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
