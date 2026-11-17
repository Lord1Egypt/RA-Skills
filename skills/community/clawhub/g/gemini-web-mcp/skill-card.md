## Description:

Extends an agent with Gemini Web for second opinions, current web search, multimodal understanding, Deep Research, media generation, and explicit Gemini account workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckycat133](https://clawhub.ai/user/luckycat133)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route Gemini Web-assisted work into one focused lane: assistance or research, artifact creation, or explicit account management. It helps agents incorporate Gemini results, source evidence, operation handles, or generated files into the user's requested workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gemini Web calls may send selected prompts, files, URLs, or media-generation requests outside the local agent workflow.

Mitigation: Choose the narrowest capability lane and tool profile for the task, share only necessary context, and require observed source evidence before presenting current-web answers as grounded.

Risk: Cookie-based authentication can expose sensitive Gemini account access if cached, logged, backed up, or shared.

Mitigation: Use browser cookie export only with explicit approval, avoid logging or sharing cookie values, restrict local file access, and remove cached authentication material when it is no longer needed.

Risk: Account, history, scheduled-action, and cleanup workflows can read private Gemini data or mutate and delete account resources.

Mitigation: Use account operations only on explicit user request, start with read-only identification, and require read-back verification before claiming a mutation or deletion succeeded.

Risk: Deep Research and media generation can return queued, timed-out, partial, or remote-only results that are not complete deliverables.

Mitigation: Preserve operation and artifact identifiers, resume the same operation instead of duplicating it, and verify local files before treating generated artifacts as complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luckycat133/skills/gemini-web-mcp)
- [Project homepage](https://github.com/Luckycat133/gemini-web-mcp)
- [Task workflows](references/workflows.md)
- [Artifact acceptance and handoff](references/artifacts.md)
- [Long operations](references/operations.md)
- [Tool surface reference](references/tool_surface.md)
- [Recovery playbook](references/recovery.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with structured tool results and artifact references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source URLs, local or remote artifact identifiers, verification status, and resumable operation handles when the selected workflow produces them.]

## Skill Version(s):

0.2.1 (source: SKILL.md metadata and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
