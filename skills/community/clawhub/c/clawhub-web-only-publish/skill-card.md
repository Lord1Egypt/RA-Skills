## Description:

Publish skills to ClawHub via web dashboard only. No CLI login, no device flow. Reuse existing browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers and skill maintainers use this skill to publish ClawHub skills through an already authenticated browser session when CLI login is unavailable or unreliable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing from the wrong authenticated ClawHub account can release the skill under the wrong publisher.

Mitigation: Confirm the visible ClawHub username before upload.

Risk: Uploading a skill folder can expose secrets or private files if the folder is not inspected first.

Mitigation: Scan the skill folder for credentials, tokens, secrets, and unintended private files before publishing.

Risk: The fallback CLI publish command can publish an unintended path if reused without checking the target.

Mitigation: Use the CLI fallback only when already authenticated and after confirming the exact path and version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dalomeve/skills/clawhub-web-only-publish)
- [ClawHub upload dashboard](https://clawhub.ai/upload)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with ordered workflow steps and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces publishing instructions and verification criteria; it does not execute publishing itself.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
