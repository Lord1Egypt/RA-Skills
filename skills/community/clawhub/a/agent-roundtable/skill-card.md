## Description: <br>
Multi-agent roundtable discussion for topic-driven, multi-round debate with convergence detection and conclusion generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parsifalc](https://clawhub.ai/user/parsifalc) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate structured discussions among multiple agent roles for technical reviews, product decisions, root-cause analysis, requirements clarification, and architecture tradeoffs. It helps capture sequential viewpoints, consensus, disagreements, and conclusion material for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discussion text can be persisted locally and shared through the web viewer or external chat notifications. <br>
Mitigation: Avoid using the skill for confidential discussions unless storage and recipients are approved; keep the web viewer disabled or bound to localhost unless remote access is intentional. <br>
Risk: The skill can use external chat notifications and may require OAuth tokens or other sensitive credentials. <br>
Mitigation: Use only approved notification channels, protect tokens, and confirm recipients before enabling notifications for sensitive discussions. <br>
Risk: The bundle includes subprocess, browser, network sharing, and release or operations scripts that may be inappropriate in sensitive environments. <br>
Mitigation: Review or remove operational scripts before deployment, constrain output paths, and run the skill in an environment with appropriate process and network controls. <br>


## Reference(s): <br>
- [Roundtable homepage](https://roundtable.izmw.me) <br>
- [README](README.md) <br>
- [API Reference](docs/API.md) <br>
- [Integration Guide](docs/INTEGRATION.md) <br>
- [Adapter Guide](docs/ADAPTER.md) <br>
- [Architecture](docs/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline tool calls, shell commands, YAML snippets, and JSON-serializable discussion summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Discussion content may be persisted locally and may be shared through the optional web viewer or configured chat notifications.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release evidence, SKILL.md frontmatter, pyproject.toml, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
