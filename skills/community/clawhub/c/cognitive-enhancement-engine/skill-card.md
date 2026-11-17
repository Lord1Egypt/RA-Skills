## Description:

Cognitive Enhancement Engine provides AI agents with working memory, TF-IDF vector memory, planning, reasoning, reflection, and metacognitive monitoring using Python standard library components.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen-feng123](https://clawhub.ai/user/chen-feng123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent builders use this skill to add local memory, retrieval, planning, reasoning, reflection, and task execution helpers to Python-based agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script silently makes a persistent shell-profile alias change with unsafe quoting.

Mitigation: Review setup.sh before running it; prefer copying or importing engine.py directly, or manually add any launcher command until the profile modification is explicit, opt-in, and safely escaped.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chen-feng123/skills/cognitive-enhancement-engine)
- [API Specification](references/API_SPEC.md)
- [Use Guide](references/USE_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, Python code examples, JSON-like dictionaries, Markdown documentation, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Python engine returns in-memory strings, lists, and dictionaries; setup guidance may modify a shell profile if the setup script is run.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
