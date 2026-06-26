## Description: <br>
Cleans and structures raw drawing text from Markdown files by filtering noise such as axis labels, drawing-frame fields, dimension-only lines, and encoding artifacts, then grouping retained content into drawing information, design notes, material strength, component IDs, reinforcement information, elevations and dimensions, node practices, and other review items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lialia691691-alt](https://clawhub.ai/user/lialia691691-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and construction-document reviewers use this skill to clean OCR or extractor output from structural drawing Markdown files before downstream quantity takeoff or manual review. It produces categorized, deduplicated text with cleanup statistics so users can inspect retained design and reinforcement information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool reads and writes local Markdown files, and automatic input selection can choose an unintended Markdown file when no input path is supplied. <br>
Mitigation: Specify explicit input and output files, and run the tool in a directory without unrelated Markdown files. <br>
Risk: Cleaning rules can remove useful drawing text or leave excessive noise when the source extraction quality differs from expected drawing patterns. <br>
Mitigation: Review the reported denoising rate and inspect retained categories, especially the other and component-ID sections, before using the output downstream. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lialia691691-alt/drawing-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown file with categorized sections and cleanup statistics, plus CLI status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a cleaned Markdown file from a local Markdown input; default output naming is derived from the input filename.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
