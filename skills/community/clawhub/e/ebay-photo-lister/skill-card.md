## Description:

Turn a photo and one-line caption into a complete, eBay-validated draft listing with AI title and description, category selection, item specifics, photo upload, and price extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scotty-1987](https://clawhub.ai/user/scotty-1987)

### License/Terms of Use:

MIT-0

## Use Case:

External resellers and commerce agents use this skill to turn item photos and captions into eBay draft listings for review, validation, and optional publication after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unbundled paid external ListBlitz pipeline with eBay and Anthropic credentials.

Mitigation: Review the exact ListBlitz package before use, verify what code will run, and use least-privilege revocable credentials.

Risk: Live eBay listings could be published through the external pipeline.

Mitigation: Do not allow live publication unless the exact draft has been inspected and explicitly approved by the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scotty-1987/skills/ebay-photo-lister)
- [ListBlitz full kit](https://jenkinsscotty.gumroad.com/l/zmtxiu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and listing draft details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create job JSON inputs and relay eBay validation results and listing URLs through the agent workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
