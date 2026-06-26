## Description: <br>
Automated pre-publish scanner that detects and blocks sensitive data like credentials, tokens, emails, and personal paths in ClawHub skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vilda007](https://clawhub.ai/user/vilda007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill before ClawHub publication to scan skill directories for credentials, tokens, emails, personal paths, and other sensitive content that should not be released. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner is a security helper, but evidence notes one detection-quality weakness and says it is not a complete secret-scanning guarantee. <br>
Mitigation: Review or test the allowlist before relying on it to block publication of local paths, usernames, or other sensitive project content. <br>
Risk: The artifact scans local files and prints detected matches, which can expose sensitive strings in terminal output during review. <br>
Mitigation: Run it locally in a trusted environment and treat scan output as sensitive until findings are replaced with placeholders or environment-variable references. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vilda007/skills/clawhub-publish-security) <br>
- [Publisher profile](https://clawhub.ai/user/vilda007) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner exits nonzero when sensitive-content findings are detected.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
