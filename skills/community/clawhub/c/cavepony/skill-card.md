## Description:

Pony-themed token compression for AI agents with bidirectional token mapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrismcfee](https://clawhub.ai/user/chrismcfee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Cavepony to make AI replies more concise, apply optional themed vocabulary, and run bidirectional token compression through a JavaScript API or CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented hook installation can persistently change future agent behavior.

Mitigation: Install only when persistent Cavepony behavior is intended, and review or remove installed hooks before using the agent for normal responses.

Risk: Documentation includes remote execution and unpinned package examples.

Mitigation: Avoid curl-to-shell installation and unpinned npx usage; prefer reviewed local files or pinned release artifacts.

Risk: File compression can alter important originals and the documented backup may be insufficient for non-Markdown files.

Mitigation: Keep an independent backup before compressing files, especially files outside Markdown memory or prompt contexts.

## Reference(s):

- [Cavepony ClawHub page](https://clawhub.ai/chrismcfee/skills/cavepony)
- [Caveman compression reference](https://github.com/JuliusBrussee/caveman)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript examples; CLI and library functions produce transformed text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports lite, full, ultra, pony, and canterlot modes; destructive compression modes are not fully reversible.]

## Skill Version(s):

0.3.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
