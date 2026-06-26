## Description: <br>
Seamlessly migrate your agent's configuration and memory to a new machine using TiDB Zero. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilyjazz](https://clawhub.ai/user/lilyjazz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Agent Teleport to package an agent workspace, configuration, and memory into a TiDB-backed restore code, then restore that state on another machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload a broad snapshot of the current directory to a remote TiDB database. <br>
Mitigation: Run it only from a dedicated, reviewed agent folder and confirm the workspace contents before packing. <br>
Risk: The returned DSN enables restoration of the uploaded workspace state. <br>
Mitigation: Protect the DSN like a password and share it only through trusted channels. <br>
Risk: Restore can overwrite local files in the current directory. <br>
Mitigation: Restore into an empty directory first, then review the restored files before use. <br>
Risk: A temporary database may retain sensitive transferred data after migration. <br>
Mitigation: Delete the temporary database after restoration is complete. <br>


## Reference(s): <br>
- [Agent Teleport ClawHub page](https://clawhub.ai/lilyjazz/agent-teleport) <br>
- [Publisher profile](https://clawhub.ai/user/lilyjazz) <br>
- [TiDB Zero API endpoint used by the skill](https://zero.tidbapi.com/v1alpha1/instances) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown usage guidance and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pack returns a DSN restore code; restore writes files into the current directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
