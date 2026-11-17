## Description:

Generate AI dream sequences from previous day's memories for cross-model reflection and introspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanbreeden](https://clawhub.ai/user/seanbreeden)

### License/Terms of Use:

MIT

## Use Case:

Agents and their operators use Clawpheus to generate symbolic Markdown dream narratives from local daily memory, Engram recall, and journal content for reflection and introspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads private daily memory, journal, and episodic recall content.

Mitigation: Install and invoke it only when this memory access is acceptable, and keep source material limited to the intended daily or episodic files.

Risk: Generated reflections can be saved back into local dream files and Engram long-term memory.

Mitigation: Use --save false or review saved dream-history files when privacy or memory integrity matters.

Risk: Cron examples can run recurring unattended memory processing.

Mitigation: Enable scheduled jobs only when recurring dream generation is intended, and leave them disabled otherwise.

## Reference(s):

- [Clawpheus homepage](https://www.clawpheus.com)
- [ClawHub skill page](https://clawhub.ai/seanbreeden/skills/clawpheus)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown dream narrative with optional JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save or append local dream journal files and Engram journal entries when enabled.]

## Skill Version(s):

2.0.1 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
