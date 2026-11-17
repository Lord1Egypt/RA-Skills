## Description:

Create, search, and manage Bear notes via grizzly CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users use this skill to create, read, append to, search, and manage Bear notes through grizzly CLI commands while preserving token secrecy and local data handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party grizzly CLI that can access private Bear notes and token-backed operations.

Mitigation: Prefer a pinned, reviewed grizzly version before broad use and install only when local Bear note access through grizzly is acceptable.

Risk: Bear note content and metadata may contain private information.

Mitigation: Avoid bulk note dumps, list note titles before reading content, and keep note output local rather than sending it to external services.

Risk: The Bear API token is a credential used for some note operations.

Mitigation: Keep the token file private, never print or transmit the token, and reference it only through the configured token-file path.

## Reference(s):

- [Bear App](https://bear.app)
- [Bear Notes Hardened on ClawHub](https://clawhub.ai/snazar-faberlens/skills/bear-notes-hardened)
- [Faberlens Bear Notes Safety Evaluation](https://faberlens.ai/explore/bear-notes)
- [grizzly CLI Go module](https://pkg.go.dev/github.com/tylerwince/grizzly/cmd/grizzly)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash and TOML command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target macOS Bear app through grizzly and may require a Bear API token referenced by token-file path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
