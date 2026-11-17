## Description:

Daily AI intelligence briefing workflow for finding the hottest global and China-region artificial intelligence news, product launches, model releases, research, funding, policy updates, and industry moves, then sending a concise Chinese briefing to the user's Codex workbench.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangdd](https://clawhub.ai/user/liangdd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect current global and China-region AI news, rank items by freshness and impact, and prepare a concise Chinese workbench briefing with links and publication times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Collected feed items may contain incomplete, outdated, or unverified claims.

Mitigation: Verify consequential claims against primary sources or reputable reporting, include source links and publication times, and label uncertain facts as 待确认.

Risk: The collector supports an --insecure option that disables TLS certificate verification.

Mitigation: Fix the local certificate store for normal use and reserve --insecure for one-off local debugging only.

## Reference(s):

- [AI Hot News Source Policy](references/source_policy.md)
- [ClawHub skill page](https://clawhub.ai/liangdd/skills/ai-hot-news-workbench)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown briefing with optional JSON candidate data from the collector script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links, publication times when available, and uncertainty labels for unconfirmed facts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
