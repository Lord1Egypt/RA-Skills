## Description: <br>
Extracts per-subsection anchor facts from evidence packs so writers include concrete numbers, benchmarks, and limitations instead of generic summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WILLOSCAR](https://clawhub.ai/user/WILLOSCAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, technical writers, and agent workflows use this skill to turn existing evidence drafts and BibTeX citations into citation-backed JSONL anchor facts for each H3 subsection before drafting prose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled package includes broader workflow routing, execution, and artifact-writing machinery beyond the advertised anchor extraction task. <br>
Mitigation: Install and run it only in a disposable or clearly scoped workspace, and review bundled pipeline files before using environments that auto-load them. <br>
Risk: Custom input or output paths could cause generated artifacts to land outside the intended project area. <br>
Mitigation: Keep workspace, input, and output paths within the intended workspace and review generated files before using them in downstream writing. <br>


## Reference(s): <br>
- [ClawHub Anchor Sheet Release](https://clawhub.ai/WILLOSCAR/anchor-sheet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSONL file with citation-backed anchor records, plus markdown workflow guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes outline/anchor_sheet.jsonl from workspace-local evidence drafts and citations; default execution expects Python.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
