## Description: <br>
Polishes Markdown blog drafts by fixing spelling and grammar, improving clarity when needed, preserving the original language, and asking before major paragraph changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3ffyang](https://clawhub.ai/user/j3ffyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and developers use this skill to lightly polish Markdown blog drafts while keeping the original tone and language. It is useful for typo fixes, grammar cleanup, simple clarity edits, and producing a polished Markdown copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to read and display the raw draft, which can expose private notes, credentials, unpublished material, or other sensitive content. <br>
Mitigation: Use it only on drafts that are acceptable to share with the agent, and remove secrets or sensitive unpublished material before polishing. <br>
Risk: The polished output is written to a file path chosen by the user or a default derived from the draft path, which can accidentally replace an existing file if paths are reused carelessly. <br>
Mitigation: Review or choose the output path before writing, and keep a backup of the original draft. <br>
Risk: Light clarity edits may alter meaning if the draft is ambiguous or factually uncertain. <br>
Mitigation: Review the change summary and the polished Markdown before publishing, especially where the skill added explanatory sentences. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/j3ffyang/blog-polisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown file plus a Markdown summary of changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a polished Markdown copy at the requested output path or a default polished filename.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter and _meta.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
