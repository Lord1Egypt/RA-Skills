## Description: <br>
Keep context when work moves between agents or between a user and a human by using the Codifica protocol as shared, persistent task memory stored in Git-tracked plain text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidedicillo](https://clawhub.ai/user/davidedicillo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use Codifica to coordinate repository work through shared task state, handoffs, decisions, and completion notes. It is intended for repositories that opt into the Codifica protocol with codifica.json and Git-tracked state files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may coordinate through Git-tracked Codifica files in repositories where automatic commits or pushes should be controlled. <br>
Mitigation: Use the skill only in repositories that intentionally adopt Codifica, and rely on branches, protected remotes, or limited Git credentials where commits and pushes need review. <br>
Risk: Task notes and state files may expose secrets or private information if sensitive details are written into shared task memory. <br>
Mitigation: Review Codifica state before use and avoid storing secrets, credentials, or private information in task notes. <br>
Risk: Agents can act on stale, incorrect, or overly broad task state if they skip the repository configuration and protocol files. <br>
Mitigation: Review codifica.json, the referenced spec, file scope, and task state before claiming or completing work. <br>


## Reference(s): <br>
- [Codifica on ClawHub](https://clawhub.ai/davidedicillo/codifica) <br>
- [Codifica homepage](https://github.com/davidedicillo/codifica) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git and a repository-level Codifica configuration before protocol actions apply.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
