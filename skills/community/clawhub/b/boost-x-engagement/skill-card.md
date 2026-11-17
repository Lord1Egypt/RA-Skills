## Description:

Runs an X engagement workflow that drafts or posts originals, replies, and reposts using account, topic, voice, allowlist, and cap settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rabgpt](https://clawhub.ai/user/rabgpt)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, growth operators, and developers use this skill to run a configurable X engagement loop with manual approval in interactive mode and stricter automated posting limits in scheduled mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish originals and reposts automatically from the user's X account in scheduled mode.

Mitigation: Use a dedicated logged-in X profile, verify the active account before posting, keep conservative daily caps, and require manual approval for replies.

Risk: The artifact includes a remote curl-to-bash installer command for Implexa.

Mitigation: Do not run the installer unless it has been independently reviewed and trusted.

Risk: Automated reposts may amplify content as an endorsement.

Mitigation: Use a narrow repost allowlist and skip candidates involving politics, culture-war topics, personal drama, layoffs, or unverifiable claims.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rabgpt/skills/boost-x-engagement)
- [Publisher Profile](https://clawhub.ai/user/rabgpt)
- [Implexa](https://implexa.ai)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration, Guidance]

**Output Format:** [Structured JSON run summary with generated post text, skipped-action reasons, queued drafts, and cap status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include posted originals, reposts, replies, skipped items, drafts for approval, and daily caps remaining.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
