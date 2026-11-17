## Description:

Monitors comments across major Chinese social platforms, classifies sentiment, generates personalized replies, alerts operators to negative public-opinion signals, and stores credentials locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xikal](https://clawhub.ai/user/xikal)

### License/Terms of Use:

MIT-0

## Use Case:

External social-media operations teams use this skill to monitor brand-account comments, draft or send replies, detect negative sentiment, trigger alerts, and produce comment-analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to install mutable, unreviewed code from a referenced repository.

Mitigation: Use a pinned release or reviewed commit with a lockfile, and review the repository before installation.

Risk: The skill handles account cookies or API tokens for social platforms.

Mitigation: Use least-privileged platform tokens, avoid main-account cookies, store credentials securely, and rotate credentials regularly.

Risk: Automated replies can affect public accounts or publish unsuitable responses.

Mitigation: Enable human review before replies are posted, especially for complaints, negative sentiment, or other high-risk comments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xikal/skills/comments-monitor-reply)
- [Homepage](https://github.com/openclaw-skills/comments-monitor-reply#readme)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with slash-command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce reply templates, alert settings, monitoring commands, and periodic public-opinion reports.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
