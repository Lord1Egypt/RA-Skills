## Description:

Publish OpenClaw skills to ClawHub using the web dashboard only (no CLI login). Use when an agent must reliably upload a local skill folder, avoid auth-loop failures, and enforce privacy-safe publishing with verification evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dalomeve](https://clawhub.ai/user/dalomeve)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to publish local OpenClaw skill folders through the ClawHub web dashboard while checking required metadata, avoiding CLI authentication flows, and collecting verification evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow publishes a selected local skill folder through the ClawHub dashboard, so choosing the wrong account or folder could publish unintended content.

Mitigation: Confirm the browser is signed into the intended ClawHub account and verify the selected skill folder before submitting the publish flow.

Risk: Skill files may contain secrets, private identifiers, or machine-specific paths if they are not reviewed before upload.

Mitigation: Run the preflight privacy checks and use the included privacy checklist to search for credential-like strings and private information before publishing.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dalomeve/skills/clawhub-web-publisher)
- [ClawHub dashboard](https://clawhub.ai/dashboard)
- [Privacy Checklist](references/privacy-checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown instructions with a structured text completion report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes publish result fields for skill name, version, URL, skill ID, verification status, privacy scan, and notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
