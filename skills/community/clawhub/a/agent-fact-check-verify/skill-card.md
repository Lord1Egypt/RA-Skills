## Description:

Guides agents through multi-source fact checking of user claims using official, media, fact-checking, and social sources, then returns a concise verdict with supporting links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nhzallen](https://clawhub.ai/user/nhzallen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill when they need an agent to verify public claims, summarize the true state of affairs, and provide a small set of supporting links. It is especially suited to Traditional Chinese fact-checking workflows that require neutral conclusions and explicit uncertainty handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may perform multiple web and social-source searches, which can depend on current public availability and account-specific access.

Mitigation: Install only where that search posture is acceptable, review unavailable helper-file requirements for the environment, and avoid authenticated social CLIs unless the account context is understood.

Risk: Fact-checking results may miss unpublished, unavailable, or paywalled evidence.

Mitigation: Retain the required limitation notice and have users treat conclusions as based on publicly available information.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/NHZallen/agent-fact-check-verify)
- [ClawHub skill page](https://clawhub.ai/nhzallen/skills/agent-fact-check-verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with four fixed sections and up to five reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public-source evidence, with a required limitation notice for unavailable or paywalled information.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
