## Description: <br>
Generates academic survey drafts from user topics or recent arXiv papers, with topic selection, LaTeX/PDF generation, quality checks, and iterative improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vixuowis](https://clawhub.ai/user/vixuowis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to draft structured literature surveys, gather recent arXiv metadata, create LaTeX/PDF outputs, and run basic quality-improvement loops before human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts arXiv and can generate ongoing network traffic and files when scheduled for unattended hourly runs. <br>
Mitigation: Run it with intentional scheduling only, monitor network and storage use, and use a constrained output directory. <br>
Risk: The skill compiles generated or supplied LaTeX locally with pdflatex. <br>
Mitigation: Review generated TeX before compilation and execute in a constrained environment. <br>
Risk: Improvement commands can overwrite local TeX documents. <br>
Mitigation: Keep backups and work on copies before running improvement or optimization commands. <br>
Risk: Generated surveys may include incorrect citations, weak novelty claims, or misleading academic analysis. <br>
Mitigation: Manually verify citations, claims, novelty scores, and survey conclusions before relying on the output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vixuowis/academic-survey-self-improve) <br>
- [Publisher profile](https://clawhub.ai/user/vixuowis) <br>
- [arXiv API endpoint used by the artifact](http://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown instructions with Python command examples; generated artifacts may include LaTeX source, PDF files, JSON topic history, and console summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, arXiv network access for paper search modes, and a local LaTeX/pdflatex installation for PDF compilation. Academic claims and citations should be manually verified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
