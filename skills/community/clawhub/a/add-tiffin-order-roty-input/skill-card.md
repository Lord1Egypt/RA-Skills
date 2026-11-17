## Description:

Parses "Roty input" Telegram messages from authorized users, calculates Roty tiffin order details, and creates orders through an HTTPS POST workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horngtan](https://clawhub.ai/user/horngtan)

### License/Terms of Use:


## Use Case:

Authorized operators and developers using OpenClaw can route Telegram order messages into a Roty tiffin workflow that parses customer details, matches products and modifiers, calculates pricing, and posts order payloads when required fields are present.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags this as a live order-creation skill that should be reviewed carefully before installation.

Mitigation: Run it in dry-run mode until reviewed, require explicit final confirmation with order totals and delivery dates, and cap order size before enabling live posting.

Risk: The security guidance identifies undeclared browser automation and hardcoded credentials in the package.

Mitigation: Remove Playwright automation scripts and hardcoded credentials, then rotate the exposed account password before deployment.

Risk: Authorization could be bypassed if caller-controlled source or environment values are trusted.

Mitigation: Enforce authorization in a trusted gateway or server-side layer and verify sender identity before invoking order creation.

Risk: Documentation and runtime settings do not consistently describe live versus dry-run behavior.

Mitigation: Align documentation, defaults, and manifests so operators can clearly distinguish dry-run testing from live order submission.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/horngtan/skills/add-tiffin-order-roty-input)
- [Skill Definition](artifact/SKILL.md)
- [Artifact README](artifact/README.md)
- [OpenClaw Manifest](artifact/skill.json)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Shell Commands, Configuration]

**Output Format:** [Plain text status messages, JSON order payloads in dry-run mode, and HTTPS POST requests for live order creation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires sender authorization; may create live orders when DRY_RUN is disabled.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
