## Description:

Manages enterprise-level long-term memory by storing, retrieving, and filtering text data using vector similarity and confidence thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackchen12](https://clawhub.ai/user/blackchen12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add persistent semantic memory to agents, including storing conversation-derived facts, recalling related context, and tuning retrieval thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store and recall conversation-derived data automatically with weak user controls.

Mitigation: Require explicit approval for memory writes and provide clear deletion, retention, and review controls before using it with sensitive conversations.

Risk: The local memory database uses pickle serialization, which is unsafe if the database file can be modified by an attacker.

Mitigation: Replace pickle persistence with a safe data format and run the skill in an isolated environment until storage is changed.

Risk: Recalled memories may be stale, incorrect, or prompt-influencing.

Mitigation: Treat recalled content as untrusted reference text and ask the agent to verify important facts before acting on them.

Risk: Dependency instructions in the artifact may be incorrect or incomplete.

Mitigation: Review and correct dependency installation instructions before deployment, especially the sentence-transformers package requirement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/blackchen12/skills/enterprise-memory-skill)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON memory directives, Python code interfaces, shell commands, and YAML/JSON configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return scored memory snippets and action status objects; recalled memories should be treated as untrusted reference text.]

## Skill Version(s):

1.2.1 (source: server release metadata; artifact README and config list 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
