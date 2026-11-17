## Description:

Doubao Seed Skill lets an agent analyze image content with ByteDance Doubao vision models and write results to a file for reliable retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maoyutofu](https://clawhub.ai/user/maoyutofu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users can use this skill to call a Doubao/Volcengine vision model for image analysis, including local images or image URLs. Agent integrations should direct the CLI to write results to a unique temporary output file before reading them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and trust an unverified precompiled binary that handles API keys and local images.

Mitigation: Prefer a pinned release with published SHA-256 checksums or signatures, and install the binary in a user-owned directory instead of /usr/local/bin.

Risk: API keys and local images may be processed by the external CLI and Doubao/Volcengine service.

Mitigation: Use a narrowly scoped ARK_API_KEY and review data handling expectations before passing local images or prompts to the tool.

## Reference(s):

- [Doubao Seed Skill release page](https://github.com/maoyutofu/doubao-seed-skill/releases/latest)
- [Doubao Seed skill configuration](artifact/doubao-seed.yaml)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Text file output from a CLI command, with Markdown usage guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact recommends unique temporary output paths, synchronous execution, file polling, and a 90 second timeout.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
