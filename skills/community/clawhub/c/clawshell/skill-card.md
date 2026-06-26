## Description: <br>
Human-in-the-loop security layer. Intercepts high-risk commands and requires push notification approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polucas](https://clawhub.ai/user/polucas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Clawshell to route agent shell commands through a human approval wrapper for high-risk operations and to inspect recent command decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact describes a shell-command approval wrapper, but the implementation and dependencies are not included in the artifact. <br>
Mitigation: Verify the actual ClawShell tool implementation and dependencies before relying on it as a security control. <br>
Risk: Command text may appear in approval notifications or logs and can contain sensitive information. <br>
Mitigation: Use dedicated notification credentials and review log retention before deployment. <br>
Risk: Pattern-based command analysis can miss encoded, split, or obfuscated commands. <br>
Mitigation: Use Clawshell as defense in depth alongside sandboxing and human review, not as a standalone security guarantee. <br>


## Reference(s): <br>
- [Clawshell on ClawHub](https://clawhub.ai/polucas/clawshell) <br>
- [Pushover application setup](https://pushover.net/apps/build) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [JSON-like tool responses and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and Pushover or Telegram credentials; command decisions are logged to JSONL.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
