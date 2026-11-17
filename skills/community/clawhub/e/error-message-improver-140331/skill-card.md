## Description:

Helps developers, support teams, SaaS operators, and users turn vague errors into clearer messages that explain what failed, why it failed, and what action to take next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Application developers, support teams, SaaS operators, and affected users use this skill to rewrite unclear troubleshooting failures into actionable messages, workflows, templates, checklists, analyses, code changes, or decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording and implicit invocation may cause the skill to be applied to general debugging or support prompts where it was not deliberately requested.

Mitigation: Use it intentionally for rewriting or designing clearer error messages, and confirm that the requested task is actually about troubleshooting communication before applying its workflow.

Risk: Generated error-message guidance can be inaccurate or incomplete when the original failure context is missing or ambiguous.

Mitigation: Review the proposed wording, assumptions, and next steps against the real system behavior, then test any generated code or configuration before release.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/error-message-improver-140331)
- [OpenShift Impersonation for Multi-Cluster Auth](https://github.com/kiali/kiali/issues/10038)
- [error[vg call] No reference paths found](https://github.com/vgteam/vg/issues/4974)
- [SegmentFault error-messages](https://segmentfault.com/t/error-messages)
- [Hyprland 0.55 announced the switch to Lua for its config files](https://news.ycombinator.com/item?id=49002105)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with optional code blocks, checklists, templates, or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream guidance; no external tools, credentials, persistence, or installation actions are required by the skill itself.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
