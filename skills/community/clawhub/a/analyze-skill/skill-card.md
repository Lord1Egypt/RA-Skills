## Description: <br>
Analyzes a provided skill package and produces a four-part Markdown report with a functional summary, scenario analysis, workflow diagrams, and a rating. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[opengjun](https://clawhub.ai/user/opengjun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill reviewers use this skill to inspect uploaded files, links, or local paths for skill packages and receive a compact design critique with ASCII or Mermaid diagrams and a star rating. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes user-provided packages, links, or paths, which may expose secrets or unrelated private files if broad archives or folders are supplied. <br>
Mitigation: Provide only the specific package, link, or path intended for inspection and avoid inputs containing secrets or unrelated private content. <br>
Risk: Generated summaries, critiques, diagrams, and ratings can be incomplete or misleading when the input package is missing documentation or uses an unfamiliar format. <br>
Mitigation: Review the generated report against the original package before using it for publication, installation, or operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/opengjun/analyze-skill) <br>
- [Mermaid Live](https://mermaid.live) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown report with ASCII diagrams and Mermaid code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional fifth example section when requested; concise sentence style.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
