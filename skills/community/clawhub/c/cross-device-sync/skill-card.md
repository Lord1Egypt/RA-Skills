## Description: <br>
Helps OpenClaw users synchronize memory files across devices through a private GitHub repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coreyleung-art](https://clawhub.ai/user/coreyleung-art) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to set up GitHub-backed synchronization of memory files across multiple devices. It generates setup guidance, sync scripts, and status-check commands for bidirectional backup and restore workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub personal access token exposure during repository access. <br>
Mitigation: Use a least-privilege, disposable token scoped only to the intended private repository, rotate it regularly, and review generated commands before running them. <br>
Risk: Broad workspace synchronization may copy sensitive files or delete unexpected backup content. <br>
Mitigation: Limit the sync directory to non-secret memory files, review exclude and delete behavior in the generated scripts, and test manually before enabling scheduled sync. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coreyleung-art/cross-device-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, generated Bash scripts, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts for a GitHub repository URL and personal access token; generated scripts use git and rsync.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
