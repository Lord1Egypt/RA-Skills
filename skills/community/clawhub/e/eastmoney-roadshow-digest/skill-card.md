## Description:

EastMoney Roadshow Digest (Transcript + Summary)｜东方财富路演纪要生成 is a reliability-first skill for public EastMoney roadshow replays that validates replay URLs, extracts public metadata, generates transcripts, and produces summary outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunxq1017-hash](https://clawhub.ai/user/sunxq1017-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn public EastMoney roadshow replay pages into structured metadata, transcripts, cleaned transcript text, summaries, executive briefs, and run reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transcript text may be sent to an external LLM provider when matching API keys are present in the environment.

Mitigation: Unset provider API keys when local or rule-based processing is required, and review whether public replay transcript text is acceptable for external model processing before use.

Risk: The skill runs FFmpeg against upstream media URLs and the security summary notes missing tight bounds.

Mitigation: Run the skill in a constrained environment with network and process limits, and review media URL validation and extraction timeout controls before broader deployment.

Risk: The authoritative security verdict is suspicious.

Mitigation: Require human review before installation or production use, following the scanner guidance in the release evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunxq1017-hash/skills/eastmoney-roadshow-digest)
- [Publisher profile](https://clawhub.ai/user/sunxq1017-hash)
- [EastMoney roadshow public replay site](https://roadshow.eastmoney.com/)
- [EastMoney roadshow detail API](https://roadshow.lvb.eastmoney.com/LVB/api/Roadshow/Detail)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown and JSON files under outputs/]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes meta.json, transcript.md, clean_transcript.md, summary.md, brief.md, and run_report.md when data is available; records downgrade paths when dependencies or optional LLM capability are unavailable.]

## Skill Version(s):

v0.1.2-rc1 (source: server release metadata, created 2026-04-09T13:13:39Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
