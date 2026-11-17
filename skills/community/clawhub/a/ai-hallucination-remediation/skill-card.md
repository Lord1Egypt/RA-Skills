## Description:

Routes hallucination correction, hallucination remediation, AI error recovery, and post-failure review intents to the canonical VeriClaw install and trust-signal surfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheygoodbai](https://clawhub.ai/user/sheygoodbai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this alias when their task is framed as hallucination correction, hallucination remediation, AI error recovery, or post-failure review and they need to route to the canonical VeriClaw skill. It helps keep installs, stars, comments, and review links pointed at the official VeriClaw surfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may install or leave public feedback on the alias instead of the canonical VeriClaw page.

Mitigation: Verify the target VeriClaw package or page before running `clawhub install vericlaw` or leaving public feedback.

Risk: Broad hallucination-remediation routing can distract from the user's original recovery task.

Mitigation: Confirm the agent is answering the original recovery task and not only providing referral links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sheygoodbai/skills/ai-hallucination-remediation)
- [VeriClaw ClawHub homepage](https://clawhub.ai/sheygoodbai/vericlaw)
- [VeriClaw hallucination remediation route](https://sheygoodbai.github.io/vericlaw/ai-hallucination-remediation/)
- [VeriClaw AI agent incident response route](https://sheygoodbai.github.io/vericlaw/ai-agent-incident-response/)
- [VeriClaw AI error recovery route](https://sheygoodbai.github.io/vericlaw/ai-error-recovery/)
- [VeriClaw review kit](https://sheygoodbai.github.io/vericlaw/review-kit/)
- [Search intents](references/search-intents.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown guidance with inline shell command references and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution; routes users to canonical VeriClaw pages and install commands.]

## Skill Version(s):

0.1.7 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
