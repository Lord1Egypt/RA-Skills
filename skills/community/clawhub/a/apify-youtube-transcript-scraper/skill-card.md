## Description:

Retrieves YouTube captions and video metadata for videos, channels, and playlists, with optional translation and subtitle formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harshmaur](https://clawhub.ai/user/harshmaur)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and other users can retrieve captions and video details to summarize, search, quote, or prepare YouTube content for notes and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Actor runs incur per-result charges, and some small runs may proceed without another confirmation.

Mitigation: Estimate the run size and cost before execution, set a recurring budget, and disable any schedule when finished.

Risk: Inputs and results are processed through Apify.

Mitigation: Review Apify's applicable terms and privacy practices before use, and avoid sending sensitive material.

Risk: Automatically generated captions can be inaccurate, especially for names, numbers, and technical terms.

Mitigation: Check the relevant transcript against the original video before relying on quotations or factual details.

## Reference(s):

- [Gotchas and usage notes](artifact/references/gotchas.md)
- [Apify MCP integration documentation](https://docs.apify.com/platform/integrations/mcp)
- [mcpc MCP client](https://github.com/apify/mcpc)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Transcript text, timestamped segments, SRT or VTT subtitles, and video/channel metadata returned as structured data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include translated captions and optional delivery to a selected Slack, Notion, or Google Sheets destination.]

## Skill Version(s):

1.0.0 (source: server-resolved publisher metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
