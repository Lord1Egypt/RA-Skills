## Description:

Discover who you're becoming through your own experience. Automated soul synthesis that reads your memory, finds the patterns you keep returning to, and builds an identity document grounded in evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:


## Use Case:

External ClawHub users and agents use this skill to synthesize a local SOUL.md identity document from memory files and related OpenClaw context, then inspect status, provenance, backups, and traces for generated identity claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads personal memory files, USER.md, interviews, and OpenClaw session logs, then stores derived identity data under .neon-soul.

Mitigation: Review and remove sensitive content before synthesis, use --dry-run to preview processing, and install only when this local data processing is acceptable.

Risk: Derived identity content can be sent to the configured Ollama endpoint if OLLAMA_BASE_URL points to a remote service.

Mitigation: Keep Ollama configured to a trusted local endpoint unless remote processing is intentional and approved.

Risk: SOUL.md may be committed to git automatically in a repository.

Mitigation: Review repository status and ignore rules before running synthesis when SOUL.md or .neon-soul data should remain private.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leegitw/skills/consciousness-soul-identity)
- [Publisher profile](https://clawhub.ai/user/leegitw)
- [NEON homepage](https://liveneon.ai)
- [Ollama local service endpoint](http://localhost:11434)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries, shell command guidance, SOUL.md, and .neon-soul JSON state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Incremental synthesis can cache prior analysis and can write SOUL.md plus backups under .neon-soul.]

## Skill Version(s):

0.4.9 (source: server release metadata; artifact frontmatter is 0.4.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
