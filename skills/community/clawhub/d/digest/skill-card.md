## Description:

Curates news, feeds, and industry sources into personalized recurring digests with sourcing, filtering, ranking, delivery, preference learning, and verification guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to build personalized daily, weekly, or scheduled news digests for topics, competitors, people, industries, and markets. It is intended for recurring digest curation and tuning, not for summarizing user-provided documents or internal business reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain local personalization history, learned preferences, and sent-item logs.

Mitigation: Review or delete ~/Clawic/data/digest/ when long-term personalization history should not be retained.

Risk: Scheduled sends or external delivery channels can send digest content to the wrong place or at an unwanted time.

Mitigation: Confirm timezone, schedule, and selected channels such as email, Slack, or Telegram before enabling recurring or external delivery.

Risk: Single-source, stale, or weakly sourced news items can mislead readers if promoted as settled facts.

Mitigation: Require named sources, check original dates, deduplicate syndicated coverage, and hold or clearly hedge single-source surprising claims.

## Reference(s):

- [Digest ClawHub release](https://clawhub.ai/ivangdavila/skills/digest)
- [Digest Clawic skill page](https://clawic.com/skills/digest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown digest guidance with structured sections, source notes, preference updates, and channel-specific delivery guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local personalization state, preferences, and sent-item history under ~/Clawic/data/digest/.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
