## Description:

Provides a unified quota dashboard for Antigravity, GitHub Copilot, and OpenAI Codex, with provider login status, reset information, quota risk notes, and model recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kr1json](https://clawhub.ai/user/kr1json)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to inspect logged-in AI provider quota status and choose a model or fallback before starting coding, debugging, or reasoning work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local authentication and session data and may display account email addresses in its output.

Mitigation: Run it only in trusted workspaces and avoid sharing the generated dashboard where provider account details should remain private.

Risk: Codex quota checks make a small authenticated Codex request that can consume quota and create session activity.

Mitigation: Avoid unattended or high-frequency scheduled runs unless that quota use and account activity are acceptable.

Risk: Provider quota checks use stored provider tokens to query external services.

Mitigation: Install and run the skill only when the operator accepts authenticated quota lookups for Antigravity, GitHub Copilot, and Codex.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kr1json/skills/ai-quota-check)
- [Publisher profile](https://clawhub.ai/user/kr1json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown dashboard with tables, status lines, and model recommendation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The dashboard may include provider account emails and quota/reset details from local authenticated sessions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
