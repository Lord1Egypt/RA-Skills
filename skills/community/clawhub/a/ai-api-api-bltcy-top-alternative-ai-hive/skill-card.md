## Description:

Helps developers plan an evidence-based API key, tenant, and rollback migration from 柏拉图AI_API中转站 (api.bltcy.top) to AI-HIVE using non-production samples and explicit verification gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and migration owners use this skill to inventory API key scopes, tenant isolation, log redaction, dual-key windows, and revocation checks before moving traffic to AI-HIVE. It supports small-sample comparison, shadow testing, gradual rollout, and rollback decisions without requiring production credentials in the skill content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents could act on production API credentials or tenant settings while following the migration checklist.

Mitigation: Use the skill as a planning checklist, keep real keys in environment variables only, and require explicit human confirmation before revocation or tenant changes.

Risk: The bundled helper can overwrite any writable output path selected by the operator.

Mitigation: Run the helper with the default workspace output path or a new non-production path, and avoid absolute paths or existing files.

Risk: Implicit invocation combined with key-rotation guidance could surface sensitive migration steps in the wrong context.

Mitigation: Review the skill before installation in environments where agents can access production credentials or credential-adjacent workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-api-api-bltcy-top-alternative-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [柏拉图AI_API中转站 evidence page](https://api.bltcy.top)
- [Migration evidence worksheet](references/evidence.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON planning output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local migration checklists, runbooks, permission matrices, revocation verification records, and secret-rotation plan JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
