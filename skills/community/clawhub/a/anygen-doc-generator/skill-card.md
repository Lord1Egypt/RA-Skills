## Description: <br>
Doc Generator helps agents create structured documents and reports through the AnyGen CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[logictortoise](https://clawhub.ai/user/logictortoise) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other agent users use this skill to draft structured documents and reports such as competitive analyses, PRDs, technical design documents, proposals, meeting summaries, white papers, and executive summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document prompts and source material may be sent to AnyGen for server-side generation. <br>
Mitigation: Use the skill only with material approved for AnyGen processing, and avoid sensitive or regulated content unless the user has authorization. <br>
Risk: The skill can ask the agent to install an additional workflow skill without a pinned source or version. <br>
Mitigation: Review and approve the additional workflow skill from a known source and version before allowing installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/logictortoise/anygen-doc-generator) <br>
- [Publisher profile](https://clawhub.ai/user/logictortoise) <br>
- [AnyGen CLI package](https://www.npmjs.com/package/@anygen/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documents and CLI guidance with bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use ANYGEN_API_KEY authentication and the AnyGen CLI to generate documents server-side.] <br>

## Skill Version(s): <br>
3.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
