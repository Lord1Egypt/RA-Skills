## Description:

Analyzes TikTok videos by collecting transcript, metadata, visual scene notes, and CreatOK suggestions so an agent can explain the script, storyboard, hook, metrics, and conversion structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newt0n](https://clawhub.ai/user/newt0n)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, sellers, and developer-assisted content teams use this skill to analyze a TikTok URL, recover the original script and storyboard, and understand the video's hook, pacing, metrics, and conversion structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The run ID may allow artifacts to be written outside the intended folder.

Mitigation: Validate or constrain run_id values before running the skill, and review generated artifact paths before trusting outputs.

Risk: TikTok URLs and extracted content are sent to CreatOK for analysis.

Mitigation: Use only trusted, non-sensitive videos when sharing content with the external analysis service is acceptable.

Risk: Untrusted video or API text may influence the agent's final analysis.

Mitigation: Keep clear prompt-injection boundaries around transcript, visual, and remote response text, and review final guidance before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/newt0n/skills/creatok-analyze-video)
- [CreatOK service](https://www.creatok.ai)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown analysis supported by JSON artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes per-run artifacts including video details, transcript JSON and text, vision JSON, and outputs/result.json.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
