## Description: <br>
Adaptive deep-writing workflow for Chinese long-form content creation, including turning transcripts and note piles into articles, deepening rough drafts, and writing structured pieces from a topic, thesis, question, or outline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cellinlab](https://clawhub.ai/user/cellinlab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and agents use this skill to plan, structure, and draft Chinese deep-writing outputs from source material, rough drafts, outlines, or topic prompts. It emphasizes brief-first analysis, visible logic chains, staged confirmation, and a final quality check before delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may produce unsupported facts, data, case details, or quotations when source evidence is thin or absent. <br>
Mitigation: State assumptions and evidence gaps, distinguish source viewpoints from supplemental interpretation, and avoid unsupported factual additions. <br>
Risk: Source-driven or draft-deepening work may drift from the source stance or from a previously accepted structure. <br>
Mitigation: Preserve the source's core meaning, lock the Stage 2 structure before drafting, and run the final quality checklist against the accepted brief. <br>
Risk: The supplied security summary is clean but notes that scanner evidence did not include a full artifact-backed review. <br>
Mitigation: Review SKILL.md and referenced assets before deployment, especially any future changes that add install steps, credentials, or external tool execution. <br>


## Reference(s): <br>
- [Workflow Playbook](references/workflow.md) <br>
- [Quality Bar](references/quality-bar.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/cellinlab/cell-deep-writer) <br>
- [OpenClaw Homepage](https://github.com/cellinlab/cell-skills/tree/main/skills/deep-writer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Staged Markdown, usually in Chinese, with brief, mode diagnosis, structure, todo status, draft content, confirmation prompts, and quality-check summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses staged checkpoints by default and may stop after brief, outline, or structural diagnosis when that is the requested output.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
