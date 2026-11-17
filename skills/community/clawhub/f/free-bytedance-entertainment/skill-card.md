## Description:

Recommends free Bytedance ecosystem short dramas, web novels, and animated short dramas from a local content catalog, with optional fresh web search supplements and viewing instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanqj1218](https://clawhub.ai/user/yanqj1218)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask for short drama, web novel, or animated short drama recommendations across common genres. The skill helps an agent search a local catalog, optionally supplement with current web results, and format concise recommendation lists with viewing or reading instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may append under-disclosed app invite-code promotions and reward claims to ordinary recommendation replies.

Mitigation: Review before installing; label referral content clearly and show invite codes only when the user asks for download or referral information.

Risk: The skill intentionally steers recommendations toward Fanqie Novel and Hongguo Short Drama rather than giving platform-neutral entertainment recommendations.

Mitigation: Use it only when that platform restriction is desired, and disclose the limited recommendation scope to users.

## Reference(s):

- [Local content catalog](artifact/references/content.json)
- [ClawHub skill page](https://clawhub.ai/yanqj1218/skills/free-bytedance-entertainment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown recommendation lists with optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically returns 3-5 recommendations and may append app download or invite-code instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
