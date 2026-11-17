## Description:

中国机动车车牌号码解析与识别。Use when the user provides a Chinese license plate number and wants to identify the province, city, plate type, or validate its format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to parse Chinese vehicle license plate numbers, validate their format, and identify registration province, city code, and plate type. It is useful for offline plate lookup, user support, and data normalization workflows where no API access is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on static offline plate and city-code reference data, so newly introduced or changed local code assignments may be missing.

Mitigation: For current or operational decisions, compare results with authoritative public traffic-management notices or updated local plate-code references.

Risk: Users may treat registration-region output as the vehicle or owner current location.

Mitigation: State that results describe registration attribution only and do not identify current vehicle location or owner information.

Risk: Unexpected requests for credentials, network calls, or hidden actions would conflict with the release security evidence.

Mitigation: Deploy as an offline reference skill and deny requests to use secrets, external services, or non-reference side effects.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/china-plate)
- [Nationwide city code reference](references/city-codes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text plate parsing result with validation status and registration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline output; no credentials, network access, API calls, code, shell commands, or configuration output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
