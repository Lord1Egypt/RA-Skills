## Description:

字幕鲸 turns local MP4 files or directly downloadable MP4 links into cleaned transcripts and prompt-guided summaries, rewrites, quote lists, scene scripts, or translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, editors, and teams use the command to transcribe completed MP4 videos, then turn the speech into summaries, meeting notes, rewritten copy, quotes, scene scripts, or translations with a prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary is suspicious and cites a token requirement, promotional messaging, a reported download-handling weakness, and incomplete analysis of 11 components; safety is not confirmed.

Mitigation: Review the release security findings before installation, inspect download behavior, and run it with access limited to the intended video and a dedicated temporary location.

Risk: Processing uploads video to a remote service, and the documented service terms state that files are deleted after processing within 24 hours.

Mitigation: Obtain permission before submitting recordings and avoid sending sensitive video unless the service's handling terms meet the user's requirements.

Risk: A GUAIKEI_API_TOKEN is required, and use may incur per-video charges or consume a plan's daily allowance.

Mitigation: Use an authorized token, check the applicable billing plan before processing, and keep the token out of shared commands and logs.

## Reference(s):

- [字幕鲸 release on ClawHub](https://clawhub.ai/engheng-art/skills/captionwhale)
- [字幕鲸 service website](https://www.guaikei.com)
- [Project repository (package metadata)](https://github.com/um-why/video2text-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or Markdown, depending on the requested prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one MP4 per invocation; output is a transcript or prompt-directed text such as a summary, rewrite, quotes, scene script, or translation.]

## Skill Version(s):

1.0.1 (source: release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
