## Description: <br>
Audit and harden an OpenClaw workspace setup with concise, enforceable rules, safety boundaries, and low-bloat instruction design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cwheeler67](https://clawhub.ai/user/cwheeler67) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit and tighten OpenClaw workspace bootstrap and memory files while preserving user preferences and safety boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changes to bootstrap or memory files can alter how future agents follow instructions. <br>
Mitigation: Require a visible diff and rationale before edits are applied. <br>
Risk: Overbroad hardening edits can accidentally weaken privacy or approval boundaries. <br>
Mitigation: Keep edits targeted, preserve explicit user preferences, and ask before applying broad policy changes. <br>


## Reference(s): <br>
- [Workspace Hardening Rubric](references/rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown summary with optional file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a hardening summary, files changed, and one highest-leverage next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
