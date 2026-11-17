## Description:

Provides agent access to dLazy's hosted Claude Opus 4.7 CLI for long-context reasoning, code generation, complex tool orchestration, and multimodal inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to call Claude Opus 4.7 through the dLazy CLI with prompt, image, and video inputs. It is suited for hosted model inference workflows that can send prompts and selected media to dLazy services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on the external @dlazy/cli npm package.

Mitigation: Install only when the publisher is trusted, prefer npx or an isolated environment for temporary use, and verify the intended package version is 1.2.0.

Risk: Prompts and selected local image or video files are sent to dLazy services for inference.

Mitigation: Avoid sending sensitive data unless approved for the use case, and review dLazy service terms and organizational data-handling requirements before use.

Risk: Authentication may store a dLazy API key in the local CLI configuration.

Mitigation: Use a revocable API key, rotate or revoke it from the dLazy dashboard when needed, and prefer per-invocation environment variables or isolated configuration for shared systems.

Risk: The artifact documentation contains a package-version inconsistency between the install command and provenance text.

Mitigation: Follow the security guidance to verify that the intended @dlazy/cli package version is 1.2.0 before installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/dlazy-claude-opus-4-7)
- [dLazy CLI source](https://github.com/dlazyai/cli)
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON result envelope with generated output values or asynchronous task status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npm or npx, a dLazy API key, and network access to api.dlazy.com and files.dlazy.com.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
