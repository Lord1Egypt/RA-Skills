## Description: <br>
Analyzes a local code directory to identify its main functions, module structure, technology stack, and architecture, then generates a standardized project introduction document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ttjsndx](https://clawhub.ai/user/ttjsndx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect unfamiliar local codebases, summarize technology stack and directory responsibilities, and generate a Markdown project introduction for onboarding or architecture review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the selected local project folder, which may contain secrets or proprietary material. <br>
Mitigation: Run it only on explicit project paths and avoid repositories containing material you do not want inspected. <br>
Risk: The skill can write a Markdown output file and may overwrite an important path if one is supplied carelessly. <br>
Mitigation: Choose an output path deliberately and review it before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ttjsndx/code-project-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown project introduction document and console text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a Markdown file to the requested output path; command-line use defaults to a project introduction file inside the target directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
