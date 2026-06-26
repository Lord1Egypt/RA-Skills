## Description: <br>
Book Writer helps agents create AI-assisted book outlines and expanded chapter drafts from prompts, with optional formulas, charts, tables, code, and citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pyjhhh](https://clawhub.ai/user/pyjhhh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, writers, educators, and content teams use this skill to generate book outlines, expand chapters, and draft long-form content for academic, technical, fiction, and textbook projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some generated file writes are not safely confined when output paths are user-controlled. <br>
Mitigation: Treat output paths as trusted input and use normal filenames under generated_books until path normalization is added. <br>
Risk: The dependency installer upgrades unpinned packages. <br>
Mitigation: Install in a virtual environment and review or pin the dependency list before running the installer. <br>
Risk: Prompts, manuscripts, and search requests may be sent to OpenAI or Google services when API credentials are configured. <br>
Mitigation: Avoid sensitive prompts or manuscripts unless external API processing is acceptable for the use case. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown chapters, JSON outlines, generated book files, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use OpenAI and Google API credentials from the environment and writes generated content under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
