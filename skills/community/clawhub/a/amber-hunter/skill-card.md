## Description:

Amber Hunter is a local AI memory engine that encrypts, stores, searches, and summarizes OpenClaw and Claude Code sessions and files for recall and optional cloud sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ankechenlab-node](https://clawhub.ai/user/ankechenlab-node)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Amber Hunter to capture long-running AI collaboration context as local memory capsules, retrieve relevant past decisions or preferences, and compile related memories into personal wiki-style concept pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service reads agent sessions and workspace metadata, which may include sensitive private context.

Mitigation: Install only after reviewing the capture behavior and run it in workspaces where local memory collection is acceptable.

Risk: Security evidence flags plaintext master password and DID key storage concerns.

Mitigation: Do not trust the skill with sensitive memories until secret storage is fixed and verified.

Risk: Security evidence flags unauthenticated local endpoints and local access to private session data.

Mitigation: Keep the service bound to trusted local environments and review localhost endpoint exposure before use.

Risk: The skill attempts background persistence and automatic capture.

Mitigation: Confirm any LaunchAgent, cron, systemd, or hook installation before enabling the skill and disable background tasks when not needed.

## Reference(s):

- [Amber Hunter ClawHub page](https://clawhub.ai/ankechenlab-node/skills/amber-hunter)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Huper](https://huper.org)
- [RAG upgrade protocol v1.2.41](docs/SPEC-RAG-v1.2.41.md)
- [Knowledge Compiler specification](docs/SPEC-knowledge-compiler-v1.0.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command snippets, JSON API responses, and wiki-style markdown concept pages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory capsules, recall results, injected prompt text, encrypted sync payloads, and concept-page markdown.]

## Skill Version(s):

1.2.41 (source: server release evidence, artifact SKILL.md, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
