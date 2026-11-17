## Description:

Converts selected local videos or supported public video links into cleaned transcripts, summaries, rewrites, quote extractions, shot breakdowns, and translations using a Qwen-backed video text service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content creators, operators, and developers use this command skill to turn selected video files or public video URLs into transcripts and prompt-directed copy such as summaries, meeting notes, scripts, quote lists, and translations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, video URLs, and prompts are sent to the Guaikei service, and the artifact's privacy and retention claims are not independently verifiable.

Mitigation: Avoid confidential meetings, sensitive media, and private prompts unless the service's retention and privacy terms have been reviewed and approved.

Risk: Untrusted, internal, private-network, or very large URLs may create avoidable data exposure or availability risk because explicit URL allowlisting, private-address blocking, and size or time limits are not evidenced.

Mitigation: Use trusted public URLs or local files only, avoid internal services and cloud metadata URLs, and add allowlists plus size and time limits before broader deployment.

## Reference(s):

- [Server-resolved source repository](https://github.com/why20261/douyinvideo2text-ai)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyinvideo2text-ai)
- [Guaikei video text service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown content on stdout, with progress and diagnostics on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; accepts one video file, public video URL, or previous task ID plus an optional prompt.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
