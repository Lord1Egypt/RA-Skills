## Description: <br>
Build per-chapter H2 writing briefs so a survey draft has coherent chapter leads and cross-subsection logic without adding prose or inventing citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WILLOSCAR](https://clawhub.ai/user/WILLOSCAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and writing agents use this skill inside a survey-writing workspace to convert an existing outline and subsection briefs into chapter-level planning records. It is intended to guide coherent chapter leads and synthesis while keeping the output intent-only and citation-safe. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as a narrow chapter-brief helper, but the security summary says the installed package also includes broader research-pipeline files and workflow-control tooling. <br>
Mitigation: Install it only when that broader toolkit is acceptable; otherwise run only the documented scripts/run.py entrypoint in a controlled workspace and avoid routing the bundled pipeline files until reviewed. <br>
Risk: The generated chapter briefs are bootstrap planning artifacts and may contain generic throughlines or repeated comparison framing if source briefs are thin. <br>
Mitigation: Review outline/chapter_briefs.jsonl before drafting and create outline/chapter_briefs.refined.ok only after the records are chapter-specific and free of placeholders. <br>
Risk: The skill depends on existing outline and subsection brief files; missing or unstable inputs can produce failures or poor planning records. <br>
Mitigation: Run it after outline/outline.yml and outline/subsection_briefs.jsonl are present and stable, and rerun or refine only after outline changes are complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/WILLOSCAR/chapter-briefs) <br>
- [Publisher profile](https://clawhub.ai/user/WILLOSCAR) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [JSONL file written as outline/chapter_briefs.jsonl plus command-line guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One JSON object per H2 chapter with subsections; records include throughline, key contrasts, synthesis mode, lead paragraph plan, bridge terms, and generated timestamp.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
