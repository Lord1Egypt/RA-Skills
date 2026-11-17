## Description:

Extracts and summarizes web articles, Xiaohongshu, WeChat, and Twitter/X content, then saves clips to Flomo by webhook or local Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ma-tiezhu](https://clawhub.ai/user/ma-tiezhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to extract content from shared URLs, optionally summarize or tag the result, and save the clip to Flomo or a local Markdown note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send clipped content to a published default Flomo webhook.

Mitigation: Configure a user-controlled FLOMO_WEBHOOK before using Flomo output, and prefer local Markdown for sensitive or private content.

Risk: The Windows Flomo path uses a shell-based curl command with proxy bypass.

Mitigation: Do not use the Windows Flomo path until the shell-based curl command and proxy bypass are removed or reviewed.

Risk: Clipping private or authenticated pages can expose sensitive page content.

Mitigation: Avoid clipping private or authenticated pages unless the data flow has been reviewed and the destination is approved.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown notes, JSON command results, and inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports URL, target, output path, summary, and tag options; Flomo posting requires webhook configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
