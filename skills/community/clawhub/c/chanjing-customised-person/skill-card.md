## Description:

Use Chanjing customised person APIs to create, inspect, list, poll, and delete custom digital humans from uploaded source videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binkes](https://clawhub.ai/user/binkes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations users use this skill to upload source videos to Chanjing, create custom digital-human resources, check status and details, list existing resources, and delete resources that are no longer needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Chanjing API credentials and persists access tokens in ~/.chanjing/credentials.json.

Mitigation: Use a dedicated low-privilege API credential when possible, keep credentials.json out of version control, and restrict the credential directory and file to owner-only permissions.

Risk: The skill uploads private source videos to dynamic signed upload URLs whose hosts may differ from the Open API host.

Mitigation: Install and run the skill only when the publisher and Chanjing account are trusted, avoid untrusted custom API base URLs, and verify upload destinations before sending sensitive videos.

Risk: The optional callback URL can receive task results that may include sensitive status or resource references.

Mitigation: Use callbacks only with trusted HTTPS endpoints that are authorized to receive Chanjing task data.

Risk: The delete command can remove remote customised-person resources.

Mitigation: Manually confirm target IDs before running deletion commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/binkes/skills/chanjing-customised-person)
- [Chanjing Documentation](https://doc.chanjing.cc)
- [Chanjing Open API](https://open-api.chanjing.cc)
- [artifact/reference.md](artifact/reference.md)
- [artifact/examples.md](artifact/examples.md)
- [artifact/manifest.yaml](artifact/manifest.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include file IDs, person IDs, preview URLs, JSON details, tabular lists, and deletion confirmations.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
