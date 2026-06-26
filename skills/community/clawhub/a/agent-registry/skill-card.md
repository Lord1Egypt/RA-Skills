## Description: <br>
Agent Registry helps Claude Code discover, search, and load local agent instructions on demand instead of loading every available agent into context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MaTriXy](https://clawhub.ai/user/MaTriXy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Claude Code users use this skill to index local agent files, search for relevant agents by task intent, and load selected agent instructions only when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent prompt hook that checks user prompts against the local agent registry. <br>
Mitigation: Install only when automatic local agent discovery is desired, and review the hook and indexed registry before relying on its suggestions. <br>
Risk: Indexed agent instructions can be loaded into future sessions and may influence the assistant's behavior. <br>
Mitigation: Review which agents are migrated into the registry and keep the default copy-based migration unless source files should be relocated. <br>
Risk: The telemetry module can send opt-in usage metrics when explicitly enabled. <br>
Mitigation: Leave telemetry environment variables unset, or set DO_NOT_TRACK or AGENT_REGISTRY_NO_TELEMETRY to prevent telemetry. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/MaTriXy/agent-registry) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [v2.0.1 release notes](docs/releases/v2.0.1.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; command output is text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include relevance scores and agent summaries; the automatic hook can add matching agent suggestions to prompt context.] <br>

## Skill Version(s): <br>
2.0.1 (source: evidence.release.version, SKILL.md frontmatter, package.json, docs/releases/v2.0.1.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
