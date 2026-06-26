## Description: <br>
Removes Markdown formatting and excess whitespace from text to produce clean, publication-ready plain text with normalized punctuation and spacing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zihaowyt5525-max](https://clawhub.ai/user/zihaowyt5525-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and developers use this skill to turn AI-generated Markdown, pasted text, or uploaded documents into clean plain text for publication, copy/paste, or .txt export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Formatting removal is not reversible and may remove Markdown structure intended for reuse. <br>
Mitigation: Run the skill on copies and keep source documents when formatting may need to be restored. <br>
Risk: Complex nested formatting may require manual review before publication. <br>
Mitigation: Review the cleaned output before relying on it, especially for mixed Markdown, HTML, DOCX, and math content. <br>
Risk: Sensitive document text is processed by the agent runtime. <br>
Mitigation: Avoid submitting sensitive documents unless that processing is acceptable for the user's environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zihaowyt5525-max/clean-text-formatter) <br>


## Skill Output: <br>
**Output Type(s):** [text, files] <br>
**Output Format:** [Plain text, with optional .txt file export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown formatting is stripped; LaTeX math expressions are preserved.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
