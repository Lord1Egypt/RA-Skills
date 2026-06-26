## Description: <br>
EVE manages the research lifecycle with Auto, Semi-Manual, and Manual modes for literature search, gap analysis, idea generation, experiment planning, and publication-ready LaTeX drafting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amzayn](https://clawhub.ai/user/amzayn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, students, and developers use this skill to coordinate literature discovery, citation analysis, research-gap review, idea generation, experiment planning, paper drafting, and project memory workflows through an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install-time code can modify the local environment. <br>
Mitigation: Review install.sh and the Python scripts before installation, and run the skill in a constrained workspace where possible. <br>
Risk: Research notes and prompts may be sent to external LLM endpoints using local AI credentials. <br>
Mitigation: Verify OPENAI_BASE_URL and OPENAI_API_KEY before use, and avoid processing sensitive or confidential research material unless the endpoint is approved. <br>
Risk: Server-monitoring features can operate over SSH with weak controls. <br>
Mitigation: Use scoped credentials, avoid broad production SSH keys, and re-enable host-key verification where supported. <br>
Risk: Persistent project memory can retain research context across sessions. <br>
Mitigation: Periodically inspect or delete the skill memory directory, especially after working with sensitive projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amzayn/eve-research-supervisor-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON templates, LaTeX/code snippets, and generated research files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local project memory, downloaded papers, BibTeX, figures, tables, and LaTeX paper drafts.] <br>

## Skill Version(s): <br>
5.1.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
