## Description: <br>
Blind Review Sanitizer helps prepare manuscripts for double-blind peer review by removing or highlighting likely author-identifying content within supported local file formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Academic authors, editors, and research support teams use this skill to prepare .docx, .md, and .txt manuscripts for double-blind review by removing or highlighting names, affiliations, acknowledgments, contact details, and self-citation cues. It also supports bounded fallback guidance when automated processing is not possible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated anonymization may miss document metadata, images, headers, footers, supplementary files, or indirect identity clues. <br>
Mitigation: Manually review the generated manuscript and perform separate metadata and supplementary-file checks before submission. <br>
Risk: The DOCX dependency may be missing, ambiguous, or unpinned for .docx processing. <br>
Mitigation: Verify and pin the intended DOCX package before installation, or limit automated processing to .md and .txt files and report the dependency gap. <br>
Risk: The tool reads manuscript files and writes a blinded output file, so unintended paths could expose or overwrite local work. <br>
Mitigation: Run it only on approved local manuscript copies and review input and output paths before execution. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub Release Page](https://clawhub.ai/aipoch-ai/blind-review-sanitizer-1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Sanitized manuscript files, command-line summaries, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a blinded output file for supported inputs and reports processed identifiers; final anonymity still requires manual review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
