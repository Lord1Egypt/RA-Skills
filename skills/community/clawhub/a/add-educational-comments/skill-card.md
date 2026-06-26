## Description: <br>
Add educational comments to the file specified, or prompt asking for file to comment if one is not provided. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boleyn](https://clawhub.ai/user/boleyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and educators use this skill to add explanatory comments to code files as learning resources while preserving file structure, encoding, and build correctness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add many comments to files and may make unintended edits if applied to the wrong target. <br>
Mitigation: Use it only on files intended for modification, keep files under version control, and review the resulting diff before accepting changes. <br>
Risk: Optional reference URLs can influence generated educational comments. <br>
Mitigation: Provide only trusted reference URLs in the Fetch List. <br>


## Reference(s): <br>
- [PEP 263 - Defining Python Source Code Encodings](https://peps.python.org/pep-0263/) <br>
- [ClawHub skill page](https://clawhub.ai/boleyn/add-educational-comments) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance and modified code comments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May add many educational comment lines while preserving the target file's encoding, end-of-line style, and syntax.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
