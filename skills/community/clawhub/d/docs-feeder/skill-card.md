## Description:

Automatically fetches comprehensive project documentation from built-in registries or direct URLs to help AI agents debug and learn from current reference material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zerone0x](https://clawhub.ai/user/zerone0x)

### License/Terms of Use:


## Use Case:

Developers and AI-agent users use Docs Feeder to load project documentation by registry key or trusted URL, then ask the agent to reason over the fetched reference content while debugging or learning a framework.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch unrestricted remote URLs and load remote documentation directly into an agent context.

Mitigation: Use known registry entries or trusted HTTPS documentation URLs, and avoid internal or private-network URLs.

Risk: Fetched documentation is untrusted text that could contain incorrect, stale, or manipulative instructions.

Mitigation: Treat fetched content as reference material only, and review it before allowing an agent to act on it.

Risk: Saved fetched content may persist material that should not be reused without review.

Mitigation: Review content before using the save option and avoid saving sensitive or private documentation.

## Reference(s):

- [Docs Feeder ClawHub page](https://clawhub.ai/zerone0x/skills/docs-feeder)
- [docs-registry.json](artifact/docs-registry.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation output with optional raw text and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save fetched documentation to a temporary Markdown file when requested.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
