## Description:

Generates Agent Skill packages from position-agent prompts by extracting job capabilities, internalizing supporting knowledge, creating compliant skill directories, and syncing the prompt's skill mapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charleschor](https://clawhub.ai/user/charleschor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to convert position-agent prompt capabilities into installable Agent Skill directories with internalized knowledge, source maps, and updated prompt mappings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-provided position-agent prompts and knowledge directories or IMA sources during generation.

Mitigation: Confirm the supplied sources are appropriate for agent processing before use, and limit inputs to the materials needed for the target position skills.

Risk: Confidential business material may be summarized and internalized into generated skill files.

Mitigation: Review generated knowledge documents and source maps for sensitive content before distributing or mounting the resulting skill packages.

Risk: Generated prompt updates or skill packages may contain incomplete or misleading guidance if source evidence is missing.

Mitigation: Use the generated knowledge-gap markers and quality checklist to identify missing evidence, then review and scan the skill packages before deployment.

## Reference(s):

- [Skill Extraction Framework](references/skill-extraction-framework.md)
- [Skill Package Checklist](references/skill-package-checklist.md)
- [Position Skill Template](assets/templates/position-skill-template.md)
- [Agent Skills Specification](assets/specs/agents-skills-specification.md)
- [Agent Skills Documentation Index](https://agentskills.io/llms.txt)
- [ClawHub Skill Page](https://clawhub.ai/charleschor/skills/chudaxia-ai-coach-position-skills-generator)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown instructions, generated Agent Skill directories, knowledge documents, source maps, and prompt mapping tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated skills are expected to include SKILL.md files, assets/knowledge/knowledge.md, references/source-map.md, and knowledge-gap documentation when evidence is insufficient.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
