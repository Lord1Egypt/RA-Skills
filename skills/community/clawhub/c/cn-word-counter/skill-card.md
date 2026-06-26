## Description: <br>
Counts words, characters, and lines for supplied text using a local Python standard-library script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and agent workflows use this skill to measure text length locally and return word, character, and line counts as structured output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Word counts are based on whitespace splitting, so Chinese text without spaces may not reflect linguistic word segmentation. <br>
Mitigation: Treat word count as approximate for unsegmented Chinese text; use the character and line counts when exact segmentation is not required. <br>
Risk: The release metadata includes a sensitive-credential capability tag that conflicts with the security evidence. <br>
Mitigation: Do not provision credentials for this skill unless a future release adds documented credential handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-word-counter) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands] <br>
**Output Format:** [JSON object with words, chars, and lines fields; agent-facing instructions may be Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No network access or credentials are needed according to the security evidence.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
