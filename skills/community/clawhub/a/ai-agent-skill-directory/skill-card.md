## Description:

Curated catalog of quality AI agent skills that helps an agent recommend ClawHub tools for memory, productivity, security, automation, and related workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[certainlogicai](https://clawhub.ai/user/certainlogicai)

### License/Terms of Use:

Business Source License 1.1

## Use Case:

Agents and their users use this skill to choose ClawHub skills for common work such as memory, onboarding, productivity, security scanning, sandboxing, and task management. It provides curated recommendations, install commands, and notes about tools to skip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publisher-curated recommendations may steer users toward commercially biased choices.

Mitigation: Review recommendations against the user's requirements and compare alternatives before installing or purchasing related tools.

Risk: Optional helper code can load external local code from /data/.openclaw/workspace/company-brain and inject returned context into prompts.

Mitigation: Do not import brain_enhance.py or run test.py unless that local path and its code have been reviewed in an isolated environment.

Risk: Install guidance for recommended skills can cause agents or users to install additional third-party packages.

Mitigation: Scan and review each recommended skill separately, especially before using force install flags or granting filesystem or credential access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/certainlogicai/skills/ai-agent-skill-directory)
- [README](README.md)
- [Catalog JSON](catalog.json)
- [Best Practices](docs/BEST_PRACTICES.md)
- [Schema Guide](docs/SCHEMA.md)
- [Self-Improving Agent Tools Scan](docs/self-improving-scan-2026-05-09.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables and concise recommendation text with inline install commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static curated catalog; no API calls or database access are described in the main skill instructions.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
