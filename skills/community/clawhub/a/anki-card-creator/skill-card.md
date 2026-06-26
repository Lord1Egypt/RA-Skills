## Description: <br>
Creates simple local Anki-compatible TSV flashcards from Q&A text, drug facts, or anatomy details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, educators, and agent users can generate local Anki import files for medical study cards from structured Q&A input or a small set of drug and anatomy parameters. Generated cards should be reviewed for medical accuracy before import or study use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation advertises PDF, image occlusion, cloze, automated tagging, media, and .apkg features that are not supported by the reviewed implementation. <br>
Mitigation: Use this release as a basic local TSV generator only, and do not rely on the advertised advanced features unless a future reviewed version includes them. <br>
Risk: Generated medical study cards can contain incomplete or inaccurate information. <br>
Mitigation: Review generated cards against trusted source material before importing them into Anki or using them for study. <br>
Risk: The output path is written by the local script and may overwrite an existing file. <br>
Mitigation: Run the tool in a dedicated study folder and provide explicit input and output paths. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with example shell commands and local TSV output for Anki import] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The implementation uses local files only and has no external dependencies beyond the Python standard library.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
