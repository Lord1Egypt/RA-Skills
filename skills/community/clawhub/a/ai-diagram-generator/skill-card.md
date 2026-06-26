## Description: <br>
AI-powered diagram creation, editing, and format conversion. Generate flowcharts, sequence diagrams, ER diagrams, architecture diagrams and more in Mermaid, draw.io, PlantUML, and Graphviz formats. Powered by evolink.ai <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and technical teams use this skill to create, edit, convert, explain, and preview software, architecture, data, and workflow diagrams from terminal-driven agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI commands send selected diagram prompts or files to EvoLink for processing. <br>
Mitigation: Avoid confidential architecture, network, database, or business diagrams unless EvoLink's data handling is acceptable for the use case. <br>
Risk: The edit command overwrites the selected diagram file in place. <br>
Mitigation: Keep backups or version control before using edit commands, and review generated changes before relying on them. <br>
Risk: Previewing PlantUML diagrams sends diagram code to plantuml.com for rendering. <br>
Mitigation: Use local rendering options for sensitive diagrams or avoid PlantUML preview for confidential content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/evolinkai/ai-diagram-generator) <br>
- [Project Homepage](https://github.com/EvoLinkAI/diagram-skill-for-openclaw) <br>
- [EvoLink API Documentation](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=diagram) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, plain-text explanations, and generated diagram source files in Mermaid, draw.io, PlantUML, or Graphviz formats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AI commands require EVOLINK_API_KEY and send selected prompts or diagram files to EvoLink for processing; local template and preview commands can run without the API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
