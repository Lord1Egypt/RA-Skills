## Description:

Generates weekly AI and computer-vision briefing reports by gathering source material, helping the host agent structure the brief, and rendering the result into report files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llx9826](https://clawhub.ai/user/llx9826)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and host-agent users use this skill to plan AI or computer-vision briefings, fetch and deduplicate relevant source material, and render completed briefs. It supports host AI mode without an extra LLM API key, while the standalone engine can run its own configured LLM pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound web requests to configured news, search, finance, RSS, GitHub, and research-paper sources.

Mitigation: Run it with restricted network egress and approve only the data sources needed for the briefing task.

Risk: The skill_proxy adapter can bridge to local third-party skill modules.

Mitigation: Keep skill_proxy disabled unless the target module is explicitly trusted and installed from a known source.

Risk: Untrusted RSS feed URLs or task_config values can influence what the tool fetches and renders.

Mitigation: Do not allow untrusted users to provide raw RSS URLs or task_config payloads without review.

Risk: Standalone mode can call a configured LLM provider and render reports through a browser.

Mitigation: Use pinned dependencies, isolate runtime credentials, and review rendered output before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/llx9826/skills/ai-cv-weekly)
- [Publisher profile](https://clawhub.ai/user/llx9826)
- [Host AI skill instructions](artifact/clawcat_skill/SKILL.md)
- [Project README](artifact/README.md)
- [Adapter registry](artifact/clawcat/adapters/registry.json)
- [Configuration example](artifact/config.yaml)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, JSON, Markdown, Files]

**Output Format:** [Structured dictionaries and rendered HTML, PDF, PNG, Markdown, and JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Host AI mode returns planning data, fetched items, and output file paths; standalone mode may call a configured LLM provider.]

## Skill Version(s):

7.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
