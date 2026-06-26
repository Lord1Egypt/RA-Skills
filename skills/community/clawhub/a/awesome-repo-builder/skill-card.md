## Description: <br>
Create a topic-specific GitHub awesome-list repository scaffold with a polished README, concise contribution rules, AI-agent instructions, URL verification, license, and reusable templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjsxply](https://clawhub.ai/user/zjsxply) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to create a focused awesome-list repository from a topic, optional taxonomy, inclusion criteria, and seed entries. It helps draft the repository structure, README, contribution guidance, agent instructions, URL verification script, and reusable templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local repository files and can overwrite generated files when --force is used. <br>
Mitigation: Use a dedicated empty output directory and use --force only when overwriting scaffold files is intentional. <br>
Risk: Generated README entries, AGENTS.md, templates, and verify_urls.py may need review before publication. <br>
Mitigation: Review generated content before publishing and run the URL verifier when the README includes external links. <br>
Risk: The workflow may research seed entries when the user does not provide them, which can introduce stale or unsuitable resources. <br>
Mitigation: Confirm the taxonomy, inclusion criteria, and seed resources before treating the generated repository as publication-ready. <br>


## Reference(s): <br>
- [Awesome Repository Structure](references/awesome-repo-structure.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Generated repository files plus concise Markdown status notes and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local scaffold files under a user-selected output directory; the generated URL verifier performs HTTP checks only when the user runs it.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
