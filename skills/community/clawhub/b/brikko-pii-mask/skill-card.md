## Description: <br>
Masks Russian personal data in prompts before an agent sends them to an LLM, then restores placeholders in the model response through Brikko's API or a self-hosted endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bbchort](https://clawhub.ai/user/bbchort) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to mask personal data in customer or business text before sending it to an LLM, especially for Russian PII and 152-FZ compliance workflows. The skill then restores the original values in the final response when a valid mapping is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw PII may be sent to Brikko's hosted API during masking and restoration. <br>
Mitigation: Install only when the organization approves Brikko as a processor, or configure BRIKKO_API_URL for a self-hosted endpoint before processing sensitive data. <br>
Risk: Placeholder mappings are stored remotely for up to one hour when the hosted API is used. <br>
Mitigation: Avoid sending data that requires stricter residency or retention controls unless self-hosted mode is configured. <br>
Risk: A leaked or misconfigured BRIKKO_API_KEY could expose the integration to unauthorized use. <br>
Mitigation: Store BRIKKO_API_KEY as a secret, rotate it if exposed, and verify the configured endpoint before piping customer data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bbchort/brikko-pii-mask) <br>
- [Brikko Homepage](https://brikko.ru) <br>
- [Brikko PII Mask Documentation](https://brikko.ru/docs/skills/pii-mask) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON for masking results and plain text for restored responses, with shell command examples in documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRIKKO_API_KEY. Raw PII is sent to Brikko unless BRIKKO_API_URL points to a self-hosted endpoint; remote mappings are retained for one hour; mask input is limited to 1 MB.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
