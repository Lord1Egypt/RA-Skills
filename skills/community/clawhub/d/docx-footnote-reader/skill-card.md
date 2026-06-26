## Description: <br>
Extract footnotes, endnotes, and body text from .docx files using Node.js. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[landylai0604](https://clawhub.ai/user/landylai0604) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document reviewers use this skill to extract body text, footnotes, and endnotes from Word documents such as technical specifications, legal documents, and academic papers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can see the contents of DOCX files selected for extraction. <br>
Mitigation: Use only documents the agent is allowed to read, and avoid sensitive files unless that exposure is acceptable. <br>
Risk: The skill depends on the npm package word-extractor to parse documents. <br>
Mitigation: Review the dependency before using this skill in a sensitive environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Plain text extraction output, JavaScript API return objects, and markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns document body text plus arrays of trimmed footnotes and endnotes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
