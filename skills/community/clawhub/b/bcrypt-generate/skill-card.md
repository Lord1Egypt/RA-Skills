## Description: <br>
Hash passwords using bcrypt or verify a password against a bcrypt hash. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate bcrypt hashes for passwords or verify a password against an existing bcrypt hash using Python. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's one-line shell examples can expose real passwords in shell history or process listings. <br>
Mitigation: Review before use with real passwords; prefer reading secrets from stdin, an interactive prompt, or a temporary script that avoids command-line password literals. <br>
Risk: Invalid bcrypt rounds or malformed hashes can cause confusing failures or slow execution. <br>
Mitigation: Validate the rounds value and hash prefix before running commands, and warn users when high cost factors may be intentionally slow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ohernandez-dev-blossom/bcrypt-generate) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and plain-text hash or verification result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Hashing output is a bcrypt hash string; verification output is a match or non-match result.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
