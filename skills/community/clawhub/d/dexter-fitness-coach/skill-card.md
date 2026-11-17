## Description:

Personalized fitness planning and workout accountability coach for beginners and intermediates. Use when users want a training plan, workout logging, progress check-ins, or practical fitness guidance with a supportive coaching style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexterqiu-collab](https://clawhub.ai/user/dexterqiu-collab)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request practical fitness plans, workout logging, progress check-ins, and basic recovery or nutrition guidance. It is best suited for beginner and intermediate fitness goals where the agent should keep advice realistic, conservative, and accountable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Python prototype can persist health, workout, body-metric, and conversation logs locally.

Mitigation: Treat stored fitness and conversation data as sensitive, keep storage access scoped, and review the data directory before enabling shared or hosted use.

Risk: Weakly scoped local-file behavior can become unsafe if untrusted user_id values are accepted by the prototype.

Mitigation: Use trusted, validated user identifiers and isolate per-user data paths before running the prototype with real users.

Risk: Configuration files include placeholders for API keys and Feishu application secrets.

Mitigation: Keep live secrets out of tracked config.yaml and provide credentials through a secret manager or deployment environment.

Risk: The included GitHub publishing script can push repository contents to a remote.

Mitigation: Do not run the publishing script from a repository that contains credentials, private data, or unreviewed local files.

Risk: Fitness and nutrition guidance can be misunderstood as medical advice.

Mitigation: Keep recommendations conservative, ask about injuries or medical limits when relevant, and direct users with pain, health conditions, or eating-disorder risk to qualified professionals.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dexterqiu-collab/skills/dexter-fitness-coach)
- [Feishu Open API](https://open.feishu.cn/open-apis)
- [BigModel API](https://open.bigmodel.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text coaching responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workout sets, reps, rest periods, progress summaries, workout log summaries, and conservative safety notes.]

## Skill Version(s):

1.1.0 (source: server release metadata and openclaw.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
