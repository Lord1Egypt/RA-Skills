## Description:

Publish Art Tutor helps learners choose art-study resources from a configured local knowledge base, plan staged learning paths, and get technique guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingxiahotmail](https://clawhub.ai/user/qingxiahotmail)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and art coaches use this skill to match goals, skill level, and available study time to local art books, exercises, and staged learning plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the agent to scan files under a configurable local knowledge_base_path, and broad or untrusted paths can expose unrelated local file names or metadata.

Mitigation: Configure knowledge_base_path to a narrow, trusted art-resource folder and review PowerShell scan commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qingxiahotmail/skills/art-tutor)
- [Art knowledge-base catalog](artifact/references/corpus.md)
- [Art learning paths guide](artifact/references/learning_paths.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with resource paths, study plans, practice recommendations, and optional PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on the configured local knowledge_base_path and the available files in that folder.]

## Skill Version(s):

1.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
