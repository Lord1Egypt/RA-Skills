## Description: <br>
A multi-review academic manuscript refinement skill for moving papers from draft to final revision through repeated review, issue consolidation, structural optimization, language polishing, and PDF integrity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyaoshen](https://clawhub.ai/user/yuyaoshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and academic writing teams use this skill to coordinate multi-tool manuscript review, revise drafts, verify paper data and references, polish language, and prepare final LaTeX/PDF submission artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends academic manuscripts through broad external review and editing tools. <br>
Mitigation: Use the skill only on a copy of the manuscript in a dedicated folder and confirm what each external tool can read or store before execution. <br>
Risk: The workflow includes auto-approved tool execution and references an API key environment variable. <br>
Mitigation: Disable auto-approve where possible, review commands before running them, and handle API keys outside shell history. <br>
Risk: The Humanizer step is framed around reducing AI-detection signals in academic writing. <br>
Mitigation: Do not use the Humanizer step to bypass AI-use disclosure, authorship, or academic-integrity requirements. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yuyaoshen/academic-paper-refinement) <br>
- [CCF Academic Evaluation Reference](https://www.ccf.org.cn/Academic_Evaluation/By_category/) <br>
- [Neel Nanda: How to Write ML Papers](https://www.alignmentforum.org/posts/eJGptPbbFPZGLpjsp/) <br>
- [Sebastian Farquhar: 5-Sentence Abstract](https://sebastianfarquhar.com/on-research/) <br>
- [Gopen and Swan: The Science of Scientific Writing](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf) <br>
- [EvoScientist GitHub](https://github.com/EvoScientist/EvoScientist) <br>
- [AutoResearchClaw GitHub](https://github.com/aiming-lab/AutoResearchClaw) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands, LaTeX/PDF artifact expectations, review report templates, and a PDF integrity shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces staged manuscript folders, review reports, revision notes, final paper files, and PDF validation results when executed by an agent.] <br>

## Skill Version(s): <br>
7.5.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
