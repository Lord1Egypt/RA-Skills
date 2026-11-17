## Description:

Send and automate emails using ConvertKit or Mailchimp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing operators use this skill to create draft marketing email sequences, manage ConvertKit subscribers, and generate local JSON performance reports. It is aimed at product launch, welcome, and nurture campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell scripts use a ConvertKit API secret and can change live marketing account data.

Mitigation: Review scripts before use, start with a test account or test sequence, and protect or rotate API credentials if exposed in logs.

Risk: Subscriber operations and generated reports can involve subscriber-related data.

Mitigation: Control access to local report directories and verify list, recipient, and sequence targets before live runs.

Risk: The documentation advertises Mailchimp and one-off-send workflows that are not fully represented by the bundled implementation.

Mitigation: Treat those workflows as unverified until the missing implementation is reviewed or added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clawdiri-ai/skills/email-automation-dv)
- [Artifact README](artifact/README.md)
- [Artifact Deployment Summary](artifact/DEPLOYMENT.md)
- [ConvertKit API Endpoint](https://api.convertkit.com/v3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON files, Guidance]

**Output Format:** [Markdown guidance with bash commands and generated JSON sequence or report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ConvertKit API credentials for live API calls; local reports may contain subscriber-related metrics.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
