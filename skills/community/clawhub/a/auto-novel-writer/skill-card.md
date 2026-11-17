## Description:

Auto Novel Writer helps writers plan, draft, review, and revise long-form Chinese male-oriented web novels with project structure, chapter memory, outline tracking, style cleanup, and consistency checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[captaindaveluo](https://clawhub.ai/user/captaindaveluo)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and developers use this skill to organize Chinese web-novel projects, generate chapter drafts, maintain recent-chapter memory, and check style or continuity before continuing a serial novel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file scripts can read or write outside the intended novels folder through unsanitized path inputs.

Mitigation: Install and run the skill only in a dedicated workspace, avoid absolute paths or names containing ../, and back up existing writing projects before running create or chapter commands.

Risk: Generated chapter, style, and consistency guidance may miss story conflicts or introduce unsuitable revisions.

Mitigation: Review generated drafts and repair suggestions before treating them as final novel content.

## Reference(s):

- [Writing Guide](artifact/references/writing_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/captaindaveluo/skills/auto-novel-writer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose, local project files, review reports, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language novel drafting and review output; helper scripts read and write local files in the writing workspace.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
