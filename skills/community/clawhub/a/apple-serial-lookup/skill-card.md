## Description:

Look up Apple device information from a serial number by combining local decoding for older serials with guided web lookup steps for fuller model, specification, and coverage details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siatrial](https://clawhub.ai/user/siatrial)

### License/Terms of Use:


## Use Case:

External users, developers, and support workflows can use this skill when an Apple serial number needs to be identified, decoded, or checked against Apple and device-specification lookup sources. It is most useful for finding device family, model details, manufacturing data for older serials, warranty direction, and next-step lookup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web lookup steps may disclose a full Apple serial number to search engines or third-party lookup sites.

Mitigation: Prefer the bundled local decoder first, and obtain explicit user approval before submitting the full serial number to external services.

Risk: Older serial decoding and model-code mappings are incomplete and may not identify every device or configuration.

Mitigation: Treat local decode results as preliminary and verify unknown, randomized, or high-impact results with Apple Check Coverage or a trusted specification source.

## Reference(s):

- [Serial format and encoding](references/serial-format.md)
- [Model code database](references/model-codes.md)
- [EveryMac Ultimate Mac Lookup](https://everymac.com/ultimate-mac-lookup/?search_keywords=SERIAL)
- [Apple Check Coverage](https://checkcoverage.apple.com/)
- [Beetstech Apple Device Lookup](https://beetstech.com/apple-device-lookup)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with optional JSON decoder output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include locally decoded manufacturing data, model-code matches, web lookup findings, and guidance for randomized or unknown serials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
