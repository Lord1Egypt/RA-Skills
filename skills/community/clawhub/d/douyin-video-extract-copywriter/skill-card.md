## Description:

Transcribes local or public video sources into clean copy and can use a custom prompt to produce summaries, rewrites, quote extraction, shot breakdowns, translations, and other content transformations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, creators, operators, and developers use this skill to turn videos or previously created video-analysis tasks into reusable transcripts, summaries, marketing copy, meeting notes, course notes, translated text, or structured extraction outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos and URL contents may be sent to the Guaikei service and a storage provider.

Mitigation: Use the skill only with media that is approved for external processing, and avoid confidential local files.

Risk: URL inputs can cause the skill to download from sources broader than the documentation clearly bounds.

Mitigation: Do not run it against untrusted, internal, localhost, private-network, or metadata-service URLs.

Risk: Deletion and no-training statements are provider promises rather than behavior proven by the client code.

Mitigation: Confirm provider data-handling terms before using the skill for sensitive or regulated content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-video-extract-copywriter)
- [Server-resolved GitHub provenance](https://github.com/why20261/douyin-video-extract-copywriter)
- [Guaikei video copy service](https://www.guaikei.com)
- [node-downloader-helper reference](https://github.com/hgouveia/node-downloader-helper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown content emitted to stdout, with command-line examples for invocation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; progress and diagnostic messages may be emitted separately from the final content.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
