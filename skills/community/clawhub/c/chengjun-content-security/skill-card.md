## Description:

Checks text for sensitive terms, official-title wording, forbidden words, grammar issues, and punctuation problems by calling Chengjun's external content-security API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengjunai](https://clawhub.ai/user/chengjunai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to review submitted text for sensitive wording, restricted terms, grammar problems, and punctuation issues before publication or workflow handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted text is sent to Chengjun's external API and may be exposed through service or intermediary URL logs.

Mitigation: Do not submit secrets, regulated data, confidential drafts, or private personal data unless approved; prefer a fixed version that sends text in the POST body with clear privacy and retention terms.

Risk: The skill depends on an external API token and network service.

Mitigation: Store CHENGJUN_API_KEY in an approved secret manager or environment variable, rotate it as needed, and handle API failures before using results in automated publication workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengjunai/skills/chengjun-content-security)
- [Chengjun platform](https://platform.vsbclub.com/)
- [Chengjun API endpoint](https://api.vsbclub.com/pre-sys/precheck/text)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON result with status code, message, and categorized precheck findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CHENGJUN_API_KEY and limits each text submission to 5000 characters.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
