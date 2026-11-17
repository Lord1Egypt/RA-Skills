## Description:

Installs a stack of five agent tools for reflection, proactivity, learning, memory, and skill extraction so an agent can improve over repeated interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[certainlogicai](https://clawhub.ai/user/certainlogicai)

### License/Terms of Use:

Business Source License 1.1

## Use Case:

Developers and agent operators use this skill to install a bundled self-improvement stack that helps an agent retain local knowledge, learn from corrections, act proactively, and extract reusable skills from successful work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The stack references behavior-changing external component skills through ambiguous, unpinned package names.

Mitigation: Verify each referenced skill's publisher, exact version, and license before installation, and prefer pinned versions where the installer supports them.

Risk: The memory component stores local data under ~/self-improving/.

Mitigation: Inspect the stored data before using the skill with private or business information, and apply local data retention controls appropriate to the environment.

Risk: Package metadata is inconsistent across evidence sources.

Mitigation: Confirm the release slug, version, and license against the server-resolved release page and bundled license file before enterprise deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/certainlogicai/skills/ai-agent-self-improving-stack)
- [Publisher Profile](https://clawhub.ai/user/certainlogicai)
- [CertainLogic Self-Improving Stack Documentation](https://certainlogic.ai/docs/self-improving-stack)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation and usage guidance for a locally stored, externally resolved skill stack.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
