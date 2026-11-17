## Description:

Guides extraction and unpacking of Chrome extension CRX3 packages from Chrome Web Store URLs into readable source files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikopako](https://clawhub.ai/user/nikopako)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to obtain and inspect Chrome extension packages for auditing, learning, and interoperability analysis, subject to applicable rights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded extension packages or extracted files may be untrusted.

Mitigation: Use an isolated working directory, verify the CRX file before unpacking, and treat extracted files as untrusted.

Risk: Mirror downloads and proxy use can expose downloads or local network settings to third parties.

Mitigation: Prefer the official Google endpoint, avoid mirrors unless necessary, and do not share local proxy settings.

Risk: Redistributing extracted proprietary source may exceed the user's authorization.

Mitigation: Check applicable permissions and do not share downloaded proprietary code without authorization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nikopako/skills/chrome-extension-source)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes download validation, unpacking steps, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
