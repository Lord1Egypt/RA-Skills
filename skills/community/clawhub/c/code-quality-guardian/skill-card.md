## Description: <br>
Code Quality Guardian helps agents analyze code for style issues, code smells, complexity problems, and security findings across supported project types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run local quality checks over a selected code path, review findings, and generate reports for development or CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the project path selected by the user and invokes local analysis tools on that code. <br>
Mitigation: Run it in a project-scoped environment and only point it at repositories the user intends to analyze. <br>
Risk: Generated HTML reports may contain findings derived from untrusted repository content. <br>
Mitigation: Use care when opening generated HTML reports for untrusted repositories. <br>
Risk: CI results depend on locally installed analyzer tools and dependency versions. <br>
Mitigation: Pin dependencies before CI use and verify required tools are installed in the execution environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kaiyuelv/code-quality-guardian) <br>
- [Project homepage](https://github.com/kaiyuelv/code-quality-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, JSON reports, HTML reports, Markdown examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write optional report files to user-selected output paths and returns process exit codes for quality gates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
