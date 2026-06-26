## Description: <br>
Write H2 chapter lead blocks (`sections/S<sec_id>_lead.md`) that preview the chapter's comparison lens and connect its H3 subsections, without adding new facts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WILLOSCAR](https://clawhub.ai/user/WILLOSCAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate body-only lead blocks for H2 chapters that have multiple H3 subsections. It is intended for research-writing workspaces where chapter briefs, outlines, and citation files already define the facts and citation scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes broader research-pipeline files and workspace-writing behavior beyond the narrow chapter-lead description. <br>
Mitigation: Inspect the bundled `pipelines/` and `tooling/` files before installing and run the skill only in a backed-up workspace. <br>
Risk: The skill writes generated chapter lead files and a report into the target workspace. <br>
Mitigation: Review changes to `sections/S<sec_id>_lead.md` and `output/CHAPTER_LEADS_REPORT.md` before merging them into a draft. <br>
Risk: Generated leads could overstate unsupported facts or use citations outside the intended chapter scope if inputs are incomplete. <br>
Mitigation: Provide complete chapter briefs and citation files, then verify that each lead uses only citation keys present in `citations/ref.bib` and facts supported later in the chapter. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/WILLOSCAR/chapter-lead-writer) <br>
- [Overview](artifact/references/overview.md) <br>
- [Lead Block Archetypes](artifact/references/lead_block_archetypes.md) <br>
- [Throughline Patterns](artifact/references/throughline_patterns.md) <br>
- [Bridge Examples](artifact/references/bridge_examples.md) <br>
- [Bad Narration Examples](artifact/references/bad_narration_examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown files and a Markdown report generated from local outline, brief, and citation inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes one body-only lead file per eligible H2 section and `output/CHAPTER_LEADS_REPORT.md`; intended outputs contain no headings and add no new facts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
