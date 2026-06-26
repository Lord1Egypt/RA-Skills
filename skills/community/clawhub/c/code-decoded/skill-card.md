## Description: <br>
Turn a codebase into a self-contained interactive HTML course for onboarding, walkthroughs, or stakeholder explanation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leostehlik](https://clawhub.ai/user/leostehlik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, onboarding teams, and stakeholders use this skill to turn a repository into a self-contained HTML walkthrough that explains architecture, key code paths, and user-facing flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML may expose private code snippets, internal file paths, and implementation details. <br>
Mitigation: Review the generated HTML before sharing it outside the project. <br>
Risk: The skill reads repository files while building the walkthrough. <br>
Mitigation: Install and run it only in repositories where code review and architectural summarization by an agent are acceptable. <br>
Risk: Generating output at an existing path could overwrite prior work. <br>
Mitigation: Confirm the output path before writing and require approval before overwriting an existing file. <br>


## Reference(s): <br>
- [HTML Output Structure](references/html-structure.md) <br>
- [Design Principles](references/design-principles.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/leostehlik/code-decoded) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Single self-contained HTML file with inline CSS and JavaScript] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Works offline and may include repository code snippets, internal file paths, architecture details, quizzes, glossary terms, and navigation.] <br>

## Skill Version(s): <br>
0.2.1 (source: server-resolved release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
