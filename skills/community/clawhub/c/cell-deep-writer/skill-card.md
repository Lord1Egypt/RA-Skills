## Description:

Adaptive deep-writing workflow for all forms of deep content creation in Chinese, including turning transcripts and note piles into articles, deepening rough drafts, or writing structured long-form content from a topic, thesis, question, or outline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cellinlab](https://clawhub.ai/user/cellinlab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create or refine Chinese long-form content from transcripts, notes, drafts, outlines, topics, theses, or questions. It supports staged work from brief and logic analysis through structure design to a final Markdown draft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce unsupported facts, data, examples, or quotations during long-form drafting.

Mitigation: Require the agent to distinguish source material from supplemental interpretation, state assumptions, and avoid claims that are not grounded in user-provided evidence or available context.

Risk: A polished draft may drift from the source material, accepted outline, or intended thesis.

Mitigation: Keep the brief and Stage 2 structure as checkpoints, preserve the accepted section order, and run the final draft against the quality checklist before delivery.

Risk: Default Chinese output may not match every user's language expectation.

Mitigation: Ask for or honor the requested language when needed; otherwise make the Chinese default clear in the staged output.

## Reference(s):

- [Workflow Playbook](references/workflow.md)
- [Quality Bar](references/quality-bar.md)
- [OpenClaw Homepage](https://github.com/cellinlab/cell-skills/tree/main/skills/deep-writer)
- [ClawHub Skill Page](https://clawhub.ai/cellinlab/skills/cell-deep-writer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with staged Chinese writing outputs, brief sections, outline sections, todo status, and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese and staged confirmation before full drafting unless one-pass output is requested.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
