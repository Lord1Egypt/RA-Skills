## Description:

大女主小说创作主编，负责在明确创作意图下协调大纲、写作、润色、审稿和排版流程，生成女性向大女主小说成品。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongzichixiangjiao](https://clawhub.ai/user/kongzichixiangjiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent to plan, write, revise, review, and package Chinese-language female-led web fiction. It is designed for end-to-end novel drafting workflows that produce an outline, chapter drafts, final Markdown, and TXT output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read prior outline or chapter files while resuming a draft.

Mitigation: Use a fresh, dedicated output directory that does not contain private or unrelated documents.

Risk: The skill can create or overwrite matching chapter, final Markdown, or TXT files in its output directory.

Mitigation: Back up existing drafts before running the skill and review the selected output path before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kongzichixiangjiao/skills/danuzhu-novel-master)
- [Logic checker sub-skill](artifact/references/06a-逻辑检查/SKILL.md)
- [Text checker sub-skill](artifact/references/06b-文字检查/SKILL.md)
- [Narrative reviewer sub-skill](artifact/references/06c-叙事审稿/SKILL.md)
- [Typesetter sub-skill](artifact/references/07-排版/SKILL.md)
- [AI-style revision sub-skill](artifact/references/08-去AI味/SKILL.md)
- [First-person narrator and writer sub-skill](artifact/references/09-八卦女生叙事人格/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Chinese-language outline, chapter Markdown, final Markdown, and TXT manuscript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read existing outline or chapter files to resume work and may overwrite matching draft or final-output files in the selected output directory.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
