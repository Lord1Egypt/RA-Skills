## Description:

Browser Fingerprint Audit helps agents run the liarjs CLI to audit browser fingerprint consistency across JavaScript, rendering, WebRTC, timezone, TLS, HTTP, and ASN signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liarjsdev](https://clawhub.ai/user/liarjsdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and security testers use this skill to run and interpret browser fingerprint scans, compare spoofed or headless profiles against real browsers, and understand why a profile appears inconsistent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the scan through the default network path may send fingerprint and network details to liarjs.dev.

Mitigation: Use --offline when no outbound request should be made, or point --endpoint at a deployment the user controls.

Risk: The skill runs a third-party npm CLI.

Mitigation: Pin or preinstall a reviewed liarjs CLI version in sensitive environments before invoking the skill.

Risk: Attaching to an existing Chrome DevTools Protocol endpoint can interact with a browser session the user owns.

Mitigation: Use CDP attachment only when the user explicitly asks to scan that running browser, and identify the endpoint before attaching.

## Reference(s):

- [Browser fingerprint check reference](references/checks.md)
- [liarjs hosted scanner](https://liarjs.dev)
- [liarjs CLI field notes](https://liarjs.dev/cli/)

## Skill Output:

**Output Type(s):** [Shell commands, Analysis, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and scan-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe optional JSON scan output when the liarjs CLI is run with --json.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
