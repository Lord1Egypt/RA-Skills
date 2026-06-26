## Description: <br>
Coordinates consulting and research agents through a file-system workflow for research, framing, execution, audit, iteration, and delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lorwaleroy](https://clawhub.ai/user/lorwaleroy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, consultants, and project leads use this skill to coordinate multi-agent consulting deliverables with shared project state, handoff documents, review gates, forbidden-term scans, and version snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow writes and coordinates shared local project files, which can expose or overwrite project information if used in an unsuitable directory. <br>
Mitigation: Install it only for projects where shared local files are appropriate, and set project-specific output paths before use. <br>
Risk: Optional notes or retrospective paths outside the project folder can leak confidential project context if synchronized or shared. <br>
Mitigation: Remove or disable backup paths that sync to shared vaults, and keep client secrets or confidential retrospectives out of personal memory folders. <br>
Risk: Automatic handoff routing can send work to the wrong receiver path if the agent registry is stale or misconfigured. <br>
Mitigation: Review receiver paths in AGENT_REGISTRY.yaml before enabling automatic handoff routing. <br>


## Reference(s): <br>
- [Agent Card Specification](references/agent-card-spec.md) <br>
- [Forbidden Terms Specification](references/forbidden-terms-spec.md) <br>
- [Handoff Specification](references/handoff-spec.md) <br>
- [State Lifecycle](references/state-lifecycle.md) <br>
- [Version Control Specification](references/version-control-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown templates, YAML configuration, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces file-based project protocols and validation workflows for agent handoffs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
