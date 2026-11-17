## Description:

DeepSop TK工作台 helps an agent turn natural-language TikTok video requests into DeepSOP Toby tasks that generate AI videos, schedule TikTok publishing, and return playback, like, comment, share, and video-link results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuoai](https://clawhub.ai/user/kukuoai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operators use this skill to generate AI video content, configure TikTok account publishing parameters, submit DeepSOP Toby tasks, and retrieve publishing analytics. The skill is intended for workflows where the user has authority to use the configured DeepSOP API key and TikTok accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a DeepSOP API key to submit TikTok publishing tasks and query video analytics.

Mitigation: Use it only with approved DeepSOP and TikTok accounts, keep DEEPSOP_API_KEY controlled, and confirm the selected account, prompt, privacy level, schedule, and publishing counts before submission.

Risk: Security evidence identifies weak controls around scheduled callbacks and payload validation.

Mitigation: Review callback provenance handling before deployment and enforce strict validation of account IDs, publish counts, intervals, times, and unknown fields.

Risk: The skill can participate in DeepSOP package purchase flow steps.

Mitigation: Require explicit user confirmation and a fresh balance check before any package purchase action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kukuoai/skills/deepsop-tiktokflow)
- [Artifact README](artifact/README.md)
- [Artifact Skill Instructions](artifact/SKILL.md)
- [DeepSOP login](https://ai.deepsop.com/login?source=5)
- [DeepSOP registration](https://ai.deepsop.com/register?source=5)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON request bodies and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit DeepSOP API requests using DEEPSOP_API_KEY and may schedule a one-time result query callback.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
