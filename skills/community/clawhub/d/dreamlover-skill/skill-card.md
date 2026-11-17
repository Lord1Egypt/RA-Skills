## Description:

Always run intake first before creating or updating distilled agent skills for anime and game virtual characters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobemorelucky](https://clawhub.ai/user/tobemorelucky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create or update text-first anime and game character skills that separate factual canon, behavioral persona, and wording examples before installing a Codex wrapper and optionally exporting an OpenClaw wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated child skills may persist conversation-derived memory on disk.

Mitigation: Review memory behavior before installation, keep runtime memory outside exported skill packages, and use the documented read/write gates so only stable, relevant user-provided information is stored.

Risk: Generated commands or paths may become unsafe if user text is used without validation.

Mitigation: Validate slugs and file paths before writing generated packages, and avoid shell-style command templates that interpolate untrusted user text.

Risk: Character generation may mix unsupported canon, persona inference, or copied source text into generated skills.

Mitigation: Keep canon, persona, and style examples in separate layers, require intake confirmation before writes, and apply the artifact safety rules for copyright and character integrity.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tobemorelucky/skills/dreamlover-skill)
- [Product Requirements](docs/PRD.md)
- [Input Contract](docs/input-contract.md)
- [Output Contract](docs/output-contract.md)
- [Safety Rules](docs/safety.md)
- [Memory Policy](references/memory_policy.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance plus generated skill files and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated child skills use a canonical character source, platform wrapper files, and conditional local memory behavior when enabled.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
