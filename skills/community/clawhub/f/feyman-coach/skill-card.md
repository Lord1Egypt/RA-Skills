## Description: <br>
A personal knowledge coach based on the Feynman learning technique that helps users review concepts, diagnose weak points, and generate personalized study suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LewisBase](https://clawhub.ai/user/LewisBase) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external learners, and developers use this skill to apply the Feynman technique to personal notes, run guided concept reviews, identify weak areas, and create follow-up study material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The daily review script scans Markdown files in the configured vault and can surface note metadata in generated review tasks. <br>
Mitigation: Set vault_path narrowly, review the selected notes with --list, and run --dry-run before writing review files. <br>
Risk: Generated review files are written under Z_Utils/feynman-coach and may contain titles, paths, or study prompts derived from private notes. <br>
Mitigation: Review generated files before sharing or committing them, and avoid broad or public repositories for sensitive note vaults. <br>
Risk: The documented GitHub Actions workflow can commit and push generated review files if users enable it. <br>
Mitigation: Enable automated push only when repository visibility and generated note metadata are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LewisBase/feyman-coach) <br>
- [Feynman Technique reference](https://fs.blog/feyman-technique/) <br>
- [Obsidian Spaced Repetition plugin](https://github.com/st3v3nmw/obsidian-spaced-repetition) <br>
- [Anki flashcard software](https://apps.ankiweb.net/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands, configuration snippets, diagnostic reports, review tasks, and flashcard-style study material.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Markdown review files under Z_Utils/feynman-coach when the daily review script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
