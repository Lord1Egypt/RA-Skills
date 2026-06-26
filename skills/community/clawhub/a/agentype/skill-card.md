## Description: <br>
Agentype runs a local AI-agent usage analysis workflow that collects deterministic JSON, infers a persona from aggregate usage signals, and renders a terminal summary or PNG poster. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyzlmh](https://clawhub.ai/user/cyzlmh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use Agentype to inspect local AI-agent usage metadata, understand token and workflow patterns, and produce a persona summary or poster. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local AI-agent usage metadata, including projects, agents, models, token counts, and usage rhythm. <br>
Mitigation: Run it only in trusted local environments and review generated summaries or files before sharing them. <br>
Risk: The workflow may use the agentype-cli package through a uvx fallback when the command is not already installed. <br>
Mitigation: Prefer a trusted local install or verify the agentype-cli package before using the fallback command. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Terminal text with local JSON cache updates and an optional PNG poster file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output/agentype.json and can write output/agentype.png; raw session files and private transcripts are not exposed unless the user explicitly asks for debugging data.] <br>

## Skill Version(s): <br>
0.1.8 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
