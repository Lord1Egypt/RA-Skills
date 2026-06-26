## Description: <br>
Use the Mingdata DMP CLI to manage audiences, insight tasks, media sync tasks, RTQ deals, and reference data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingri26](https://clawhub.ai/user/mingri26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and run the Mingdata DMP CLI for audience management, insight tasks, media sync workflows, RTQ deals, and DMP reference data lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports operations that can upload, transform, sync, create, or modify sensitive audience and deal data. <br>
Mitigation: Confirm authorization, data scope, and destination before running DMP data commands. <br>
Risk: The skill references plaintext credentials and local DMP configuration. <br>
Mitigation: Use a secret manager or CI secret store, avoid logging environment variables or audience file paths, and restrict permissions on local DMP config. <br>
Risk: The skill directs installation of a release binary from a third-party repository. <br>
Mitigation: Install only from a trusted source and independently verify the release binary before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mingri26/dmp-cli) <br>
- [Repository](https://github.com/a652/dmp-cli) <br>
- [Releases](https://github.com/a652/dmp-cli/releases) <br>
- [DMP CLI Command Reference](references/commands.md) <br>
- [DMP CLI Workflows](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of json, plain, and table CLI output modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
