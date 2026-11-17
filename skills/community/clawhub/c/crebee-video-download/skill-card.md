## Description:

CreBee helps an agent download a user-provided video page link through the local CreBee desktop client and return the finished local file path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[n8spxd](https://clawhub.ai/user/n8spxd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content-operations agents use this skill to save videos from supported social and video platforms as local finished files for collection, comparison, or creator workflow handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads user-provided video links through the local CreBee client, may consume CreBee API quota, and saves completed files to the system Downloads folder.

Mitigation: Use it only after the user asks to download a specific link, report the resulting file path, and make quota or save-location effects clear when relevant.

Risk: The skill depends on a locally running, logged-in CreBee desktop client with available API quota.

Mitigation: Use the documented local client and troubleshooting flow; do not ask users to paste tokens or redirect calls away from the local CreBee service.

Risk: Timeouts or connection interruptions can leave the download result and quota consumption uncertain.

Mitigation: Do not automatically repeat the download; ask the user to check CreBee or the Downloads folder before deciding whether to run it again.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/n8spxd/skills/crebee-video-download)
- [CreBee website](https://www.crebee.cn)
- [CreBee download page](https://www.crebee.cn/#/download)
- [Video download reference](artifact/references/media-download.md)
- [Troubleshooting reference](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with command snippets and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CreBee CLI status interpretation, completed video file paths, and concise troubleshooting guidance.]

## Skill Version(s):

1.9.13 (source: server release evidence and skill metadata comment)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
