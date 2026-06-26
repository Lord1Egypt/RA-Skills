## Description: <br>
Formats DOCX, Markdown, and plain-text documents against user-provided layout standards while aiming to preserve the original wording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and document-processing agents use this skill to normalize document layout, typography, spacing, indentation, margins, and heading styles against a supplied standard or preset. It is suited for format correction, not content editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Whitespace and blank-line normalization can change meaning in contracts, evidence, compliance files, code-like Markdown, templates, or other spacing-sensitive documents. <br>
Mitigation: Run the skill on copies, review a diff before relying on the result, and avoid treating it as strictly text-preserving when spacing matters. <br>
Risk: DOCX preset and heuristic title detection can apply broad formatting changes that may not match a user's intended style. <br>
Mitigation: Require an explicit format standard or preset, review the adjustment list, and manually inspect important outputs before use. <br>


## Reference(s): <br>
- [Format Rules Reference](references/format-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/smallkeyboy/doc-format-fixer) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/smallkeyboy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated or modified document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a corrected document plus a concise list of formatting adjustments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
