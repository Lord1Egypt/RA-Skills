## Description: <br>
Create, verify, and document DoDAF 2.0/2.1 architecture models with guided interviews, generated view products, completeness checks, consistency checks, and consolidated reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hsuhsuehi](https://clawhub.ai/user/hsuhsuehi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Defense architects, systems engineers, and analysts use this skill to structure DoDAF 2.0/2.1 architecture work, gather stakeholder and mission context, generate required view products, verify traceability, and assemble review-ready reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive defense-planning details could be shared externally during research steps. <br>
Mitigation: Disable web search or sanitize query context before use, and do not provide classified, export-controlled, sensitive mission, stakeholder, system, or capability details. <br>
Risk: Generated verification results may overstate the strength of completeness and consistency checks. <br>
Mitigation: Treat verification findings as heuristic checks and require review by a qualified architecture or domain expert before relying on them. <br>
Risk: The skill generates many project artifacts that can be difficult to audit if mixed with unrelated files. <br>
Mitigation: Run the skill in a dedicated project directory so generated documents, diagrams, matrices, and reports are easy to inspect and manage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hsuhsuehi/dodaf) <br>
- [DoDAF 2.0/2.1 Viewpoints Reference](references/dodaf-views.md) <br>
- [draw.io Desktop](https://github.com/jgraph/drawio-desktop) <br>
- [Pandoc installation documentation](https://pandoc.org/installing.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documents, draw.io diagrams, CSV matrices, optional PDF/DOCX/HTML reports, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use optional local tools such as Pandoc, XeLaTeX, or draw.io Desktop for document conversion and diagram export.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
