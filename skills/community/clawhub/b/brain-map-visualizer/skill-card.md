## Description: <br>
Brain Map Visualizer helps OpenClaw users turn local markdown vault and session journal history into an interactive D3 and React attention graph showing project clusters, co-access relationships, and emerging projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[highnoonoffice](https://clawhub.ai/user/highnoonoffice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add a local dashboard view that visualizes how markdown files and session journals cluster by project attention, co-access frequency, and recent momentum. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated graph can expose sensitive work history, private session details, or file relationships from local journals. <br>
Mitigation: Redact secrets and private chat or session details before bootstrapping journals, and keep the generated graph JSON private. <br>
Risk: Dashboard and rebuild endpoints can reveal or refresh local attention data if exposed without access control. <br>
Mitigation: Configure real access control before exposing the dashboard or rebuild API beyond localhost. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/highnoonoffice/brain-map-visualizer) <br>
- [Project homepage](https://github.com/highnoonoffice/hno-skills) <br>
- [BrainMapProjects component](references/component.md) <br>
- [Graph schema and API routes](references/graph-schema.md) <br>
- [Journal parser script](references/journal-parser.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and JavaScript code, JSON schema examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation instructions and local configuration for a React component, Next.js API routes, a journal parser, and the generated graph JSON schema.] <br>

## Skill Version(s): <br>
3.3.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
