## Description:

AutoMD-Viz generates publication-quality molecular dynamics visualizations, including molecular structure figures, data plots, trajectory projections, and summary reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billwanttobetop](https://clawhub.ai/user/billwanttobetop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and computational researchers use this skill to generate journal-ready figures and reports from molecular dynamics structures, trajectories, and analysis outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted filenames or option values may be converted into executable PyMOL or Python code by the shell workflow.

Mitigation: Use only trusted input files, trusted filenames, and trusted option values, preferably inside an isolated environment.

Risk: Running the skill on untrusted projects can expose the user to command or script execution through generated visualization scripts.

Mitigation: Review generated PyMOL and Python snippets before execution, and avoid untrusted projects until the workflow validates options and passes values as data.

Risk: Unpinned scientific Python and visualization dependencies can reduce reproducibility and supply-chain control.

Mitigation: Pin dependencies for release, production, or regulated workflows.

## Reference(s):

- [Artifact README](artifact/README.md)
- [Artifact skill guide](artifact/SKILL.md)
- [Publication visualization troubleshooting](artifact/publication-viz-errors.md)
- [PyMOL Wiki](https://pymolwiki.org/)
- [VMD User Guide](https://www.ks.uiuc.edu/Research/vmd/current/ug/)
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)
- [Nature final submission guidelines](https://www.nature.com/nature/for-authors/final-submission)
- [Science manuscript preparation instructions](https://www.science.org/content/page/instructions-preparing-initial-manuscript)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and generated visualization files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce PNG, SVG, PDF, EPS, PyMOL session files, and visualization reports depending on the selected mode.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
