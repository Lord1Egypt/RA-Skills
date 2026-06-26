## Description: <br>
Content Security Policy helps agents redact sensitive content, filter dangerous instructions, judge action permissions, and apply multi-level access controls when users request safety checks or sensitive operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foxyy1126](https://clawhub.ai/user/foxyy1126) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add agent-level safety checks for redacting secrets, screening dangerous commands, and deciding whether requested operations need confirmation or rejection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic redaction or instruction filtering may change user content or suppress a legitimate request. <br>
Mitigation: Review trigger conditions before use, keep an override path for workflows where rewriting is disruptive, and inspect outputs before relying on them. <br>
Risk: Permission decisions depend on accurate user role configuration. <br>
Mitigation: Configure the highest-privilege administrator and authorized users before enabling sensitive operations. <br>


## Reference(s): <br>
- [Instruction Filter Details](artifact/references/instruction-filter.md) <br>
- [Action Permission Judgment Details](artifact/references/action-judgment.md) <br>
- [Sanitizer Script](artifact/scripts/sanitizer.js) <br>
- [ClawHub Skill Page](https://clawhub.ai/foxyy1126/content-security-policy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript snippets and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return redacted content, command risk levels, permission decisions, and confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
