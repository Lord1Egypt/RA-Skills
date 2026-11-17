## Description:

Records, structures, interprets, and queries Chinese-language dream journal entries stored as local Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abycloudcn-jpg](https://clawhub.ai/user/abycloudcn-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to keep a private Chinese-language dream journal, generate structured summaries and tags, interpret dreams cautiously, and search recent or keyword-matched dream history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive dream entries are stored as plaintext Markdown files on local disk.

Mitigation: Use the skill only on trusted accounts and devices, and review or back up ~/.openclaw/memory/dreams/ according to the user's privacy needs.

Risk: The skill does not provide deletion or overwrite safeguards for saved entries.

Mitigation: Review saved files manually before relying on them, and manage deletion or correction directly in ~/.openclaw/memory/dreams/ until safer controls are added.

Risk: Dream interpretation can sound more certain than the evidence supports.

Mitigation: Keep interpretations gentle and tentative, and distinguish possible associations from definite conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abycloudcn-jpg/skills/dream-journal)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chinese prose, JSON script input/output, and Markdown dream journal files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dream entries are written as plaintext Markdown files under ~/.openclaw/memory/dreams/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
