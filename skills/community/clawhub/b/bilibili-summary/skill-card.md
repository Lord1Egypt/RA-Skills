## Description:

Helps agents fetch Bilibili video subtitles, generate concise summaries, and locate keyword timestamps from subtitle files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baikemark](https://clawhub.ai/user/baikemark)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help an agent analyze Bilibili videos by retrieving subtitles, summarizing video content, and answering timestamp lookup questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may create and reuse a local Bilibili session cookie.

Mitigation: Review before installing; keep cookie.txt out of shared folders and repositories, restrict file permissions, and consider using a separate low-risk Bilibili account.

Risk: The skill can be triggered by incidental Bilibili links.

Mitigation: Confirm the user wants subtitle retrieval or video analysis before running login or fetch commands.

Risk: Unpinned or floating installs can make later behavior harder to review.

Mitigation: Prefer a fixed reviewed version with pinned dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baikemark/skills/bilibili-summary)
- [skills.sh installer](https://skills.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown responses with shell commands and generated TXT, SRT, and VTT subtitle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cache subtitles under subtitles_output/<BVID>/ and may use a local cookie.txt file for authenticated Bilibili subtitle access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
