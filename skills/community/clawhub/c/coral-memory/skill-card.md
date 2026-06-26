## Description: <br>
DEPRECATED - Use persistent-agent-memory instead. This skill has been replaced by persistent-agent-memory (clawhub install persistent-agent-memory). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[divyvasal](https://clawhub.ai/user/divyvasal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users encounter this deprecated skill as a migration pointer from Coral Memory to persistent-agent-memory. It tells users which replacement skill to install for memory storage, retrieval, and deletion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deprecated skill redirects users to persistent-agent-memory, which may have separate API key, storage, retrieval, deletion, network, or persistence behavior. <br>
Mitigation: Review the replacement skill's security card and permissions before installing or deploying it. <br>
Risk: The artifact declares CORAL_API_KEY as an environment requirement even though this deprecated version contains only a migration notice. <br>
Mitigation: Do not provide credentials to this deprecated skill unless a reviewed replacement workflow requires them. <br>


## Reference(s): <br>
- [Coral Bricks](https://coralbricks.ai) <br>
- [Persistent Agent Memory for AI Agents](https://www.coralbricks.ai/blog/persistent-memory-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with an inline shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deprecated notice; no executable code is included in this version.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
