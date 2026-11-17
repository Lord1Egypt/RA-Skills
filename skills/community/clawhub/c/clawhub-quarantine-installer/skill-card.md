## Description:

Installs ClawHub skills into a dedicated quarantine directory and produces basic audit reports so developers can review flagged third-party skills before promoting them to production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alessandropcostabr](https://clawhub.ai/user/alessandropcostabr)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to install suspicious or third-party ClawHub skills into an isolated review directory, run pattern-based checks, and inspect the generated text report before any manual promotion to production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs suspicious or flagged skills with a high-impact forced installation flow.

Mitigation: Run it only in a disposable VM or container with no sensitive credentials, and manually inspect the installed skill before any production promotion.

Risk: The quarantine path organizes files but does not enforce a real security sandbox.

Mitigation: Treat the generated report as a review aid, not a containment boundary, and rely on external isolation for execution safety.

Risk: The install command uses the ClawHub CLI through an unpinned npx invocation.

Mitigation: Pin and verify the ClawHub CLI version where possible before running the installer.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/alessandropcostabr/skills/clawhub-quarantine-installer)
- [Project homepage](https://github.com/alessandropcostabr/clawhub-quarantine-installer)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command output, and timestamped plain-text audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates quarantine and report directories under the user's OpenClaw home path when the scripts are run.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
