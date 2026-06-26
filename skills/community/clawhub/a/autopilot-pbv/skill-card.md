## Description: <br>
Autopilot coordinates complex coding work through a bounded Plan -> Build -> Verify loop that plans with Claude, builds with OMX, and verifies results before deciding whether to continue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuscut](https://clawhub.ai/user/qiuscut) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to drive multi-step refactors, automated repair loops, and changes that need repeated test or acceptance verification. It is intended for complex tasks where a single planning or coding pass is likely to miss issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run a multi-round coding agent that modifies repositories and executes commands with broad permissions. <br>
Mitigation: Use it on a clean branch or disposable checkout, review generated plans and diffs before relying on them, and remove sandbox or permission bypasses for routine use. <br>
Risk: Task context, logs, diffs, and artifacts may include private code or secrets and may be sent to external model providers. <br>
Mitigation: Protect the Anthropic API key, avoid running on sensitive repositories unless approved, and periodically delete task artifacts that contain private material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiuscut/autopilot-pbv) <br>
- [Plan format reference](artifact/references/plan-format.md) <br>
- [Verification guide](artifact/references/verify-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown plans and verification reports, task JSON, shell command snippets, and code changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires claude, omx, python3, and ANTHROPIC_API_KEY; execution is bounded to a maximum of five Plan -> Build -> Verify rounds.] <br>

## Skill Version(s): <br>
2.2.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
