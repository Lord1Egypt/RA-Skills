## Description: <br>
This skill extracts and analyzes PDF, EPUB, TXT, and Markdown books to generate WorkBuddy knowledge-base, action-guide, or hybrid skill packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guipi888](https://clawhub.ai/user/guipi888) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, knowledge workers, and learners use this skill to turn electronic books into structured analysis reports and locally installable WorkBuddy skills for reference or practical action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install generated WorkBuddy skills persistently, which may leave broad or unwanted triggers active. <br>
Mitigation: Review generated SKILL.md files and trigger phrases before installation, and remove generated skills that are too broad or no longer needed. <br>
Risk: The skill can install Python packages while extracting PDF or EPUB files. <br>
Mitigation: Use a sandbox or disposable environment for untrusted books and review dependency installation before running extraction scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guipi888/book-to-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and generated WorkBuddy skill files, with shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create persistent local WorkBuddy skills and install Python package dependencies while extracting PDF or EPUB files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
