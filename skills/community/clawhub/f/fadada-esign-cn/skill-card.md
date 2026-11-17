## Description:

Automates FaDaDa FASC API 5.0 electronic contract workflows, including sending contracts for signature, checking signing status, and downloading signed documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fadada-esign](https://clawhub.ai/user/fadada-esign)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operations teams use this skill to configure FaDaDa credentials and automate HR contracts, sales contracts, and other agreement signing workflows through Python or the fadada CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send sensitive contracts, signer data, and credentials to configurable network destinations.

Mitigation: Install only when the publisher is trusted, keep credentials in environment variables or a secret manager, and verify server_url before use.

Risk: Send and batch operations may route contracts or notifications to unintended recipients.

Mitigation: Confirm the exact contract file, recipient details, and destination before every send or batch operation.

Risk: Signing links, download links, generated reports, and signed documents may expose sensitive agreement data.

Mitigation: Treat links, reports, and downloaded files as sensitive and restrict access and retention.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fadada-esign/skills/fadada-esign-cn)
- [FaDaDa Open Platform](https://www.fadada.com/)
- [FASC API 5.0 Documentation](https://docs.fadada.com/)
- [FaDaDa FASC API 5.0 Interface Reference](references/api_reference.md)
- [FaDaDa Data Model Reference](references/data_models.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide execution that sends contracts, returns signing or download links, and writes JSON reports or downloaded signed documents.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and target metadata; artifact setup.py and _skillhub_meta.json list 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
