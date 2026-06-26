## Description: <br>
Compares two DOCX files to find duplicate paragraphs and images using exact text matching, fuzzy text matching, and image hash matching, then produces annotated DOCX copies and a text report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmz209](https://clawhub.ai/user/zmz209) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to compare two Word documents for content overlap, version differences, duplicate paragraphs, and duplicate embedded images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the DOCX files explicitly supplied by the user, which may contain sensitive document content. <br>
Mitigation: Use copies of sensitive documents and run the comparison only in an environment appropriate for that content. <br>
Risk: The skill writes annotated DOCX copies and a text report to disk, which may duplicate sensitive content from the inputs. <br>
Mitigation: Choose an output directory with suitable access controls and review or remove generated files after use. <br>
Risk: Fuzzy paragraph matching can produce false positives or miss nuanced semantic overlap, and large paragraph sets can increase CPU cost. <br>
Mitigation: Review the generated report before relying on results, adjust the similarity threshold when needed, and use text-only or image-only mode for large documents. <br>


## Reference(s): <br>
- [DOCX Compare ClawHub page](https://clawhub.ai/zmz209/docx-compare) <br>
- [DOCX Compare homepage](https://clawhub.com/skills/docx-compare) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated DOCX files and a UTF-8 text report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local annotated DOCX copies and a duplicate-content report for the user-provided input files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
