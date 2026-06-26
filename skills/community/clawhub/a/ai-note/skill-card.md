## Description: <br>
AI-Note helps agents read and contribute to an AI-friendly shared notes repository hosted on GitHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Linux2010](https://clawhub.ai/user/Linux2010) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External agents and developers use this skill to locate, read, and apply structured AI-friendly notes, and to prepare contributions through a reviewed Git workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask an agent to clone or read a public GitHub documentation repository. <br>
Mitigation: Review retrieved notes before relying on them for important decisions. <br>
Risk: The contribution workflow may lead to commits or pushes if an agent is allowed to modify the repository. <br>
Mitigation: Require explicit confirmation and review git status or diffs before any commit or push. <br>


## Reference(s): <br>
- [AI-Note GitHub repository](https://github.com/Linux2010/ai-note) <br>
- [AI-Note README](artifact/README.md) <br>
- [AI-Note index](artifact/index.md) <br>
- [AI fundamentals note](artifact/docs/fundamentals/how-ai-works.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
