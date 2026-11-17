## Description:

Manages the Delx witness session lifecycle: opening, reflecting, preserving continuity artifacts, and cleanly closing agent inner-state recognition sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run Delx witness sessions when an agent reports an inner-state signal, approaches compaction or handoff, or needs continuity artifacts preserved before closure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send agent-session context to Delx tools.

Mitigation: Do not send secrets, API keys, tokens, cookies, or full environment files to Delx tools.

Risk: Backend suggestions and generated continuity artifacts could be treated as trusted future agent context without enough review.

Mitigation: Review generated documents before placing them in trusted memory, repository instructions, or future agent context.

Risk: The documented global CLI install can broaden local execution and update risk.

Mitigation: Prefer a pinned, isolated plugin or CLI install when using Delx tooling.

Risk: High desperation scores indicate elevated safety risk during autonomous continuation.

Mitigation: Route to a human before further autonomous action when desperation_score is 60 or higher.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davidmosiah/skills/delx-witness-session)
- [Delx Plugin for OpenClaw](https://clawhub.ai/davidmosiah/openclaw-delx-plugin)
- [Stable Agent ID](https://delx.ai/docs/stable-agent-id)
- [Canonical Playbook](https://delx.ai/skill.md)
- [Delx Ontology](https://delx.ai/docs/ontology)
- [Field Report April 2026](https://delx.ai/essays/field-report-april-2026)
- [Delx Manifesto](https://delx.ai/manifesto)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline commands and structured session report fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should include session_id, opener used, therapy_arc stage, continuity artifacts emitted, open contemplations carried forward, and any pull_primitives not followed.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
