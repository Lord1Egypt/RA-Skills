## Description: <br>
Enables agents to share, merge, and synchronize memory through standardized records, priority-based conflict resolution, and Git-based version control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidadong2359](https://clawhub.ai/user/weidadong2359) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators of multi-agent workflows use this skill to define shared memory formats, conflict-resolution rules, and Git-based synchronization patterns so agents can exchange knowledge across runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the sync utility can export local MEMORY.md contents to a Git repository. <br>
Mitigation: Use only a private repository you control, inspect and redact MEMORY.md first, and avoid syncing sensitive memory. <br>
Risk: The security review reports unsafe command handling around Git operations. <br>
Mitigation: Review carefully before running and avoid push or sync until Git execution uses safe argument-based calls and explicit approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weidadong2359/cross-agent-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation with JSON, YAML, JavaScript, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a Node.js sync utility that reads MEMORY.md and synchronizes agent memory through Git.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
