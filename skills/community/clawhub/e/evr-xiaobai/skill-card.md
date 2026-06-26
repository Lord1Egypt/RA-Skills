## Description: <br>
EVR Framework helps an AI agent execute actions, verify results, and report evidence so task completion is grounded in observable checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aptratcn](https://clawhub.ai/user/aptratcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to make AI work follow an Execute, Verify, Report loop. It is intended to reduce fake completions, missing validation, repeated failed retries, and silent failures in agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages agents to run and verify shell commands, including examples that modify files or permissions. <br>
Mitigation: Review proposed commands, target paths, and verification checks before execution, especially for destructive file operations or permission changes. <br>
Risk: The security evidence is clean but notes that users seeking maximum assurance should re-check final scan status. <br>
Mitigation: Confirm the installed skill name, publisher handle, displayed files, and final scan status before using the release in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aptratcn/evr-xiaobai) <br>
- [Publisher profile](https://clawhub.ai/user/aptratcn) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [English README](artifact/README_EN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts agents to include executed command output, verification method, verification result, concrete data, and next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
