## Description: <br>
This skill evaluates arithmetic expressions using the Unix `bc` calculator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danstaal](https://clawhub.ai/user/danstaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to evaluate basic or advanced arithmetic expressions with Unix bc syntax and arbitrary precision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes local node and bc binaries to evaluate supplied expressions. <br>
Mitigation: Install only where local command execution for calculator requests is acceptable. <br>
Risk: Untrusted, huge, or intentionally non-terminating bc programs may consume local resources because the wrapper does not show a timeout or input validator. <br>
Mitigation: Avoid feeding untrusted or unbounded bc programs, and run the skill in an environment with appropriate execution controls for shared or automated use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danstaal/bc-calc) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text calculator results or bc error messages, with Markdown usage examples in documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local node and bc binaries; the bc math library is enabled by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
