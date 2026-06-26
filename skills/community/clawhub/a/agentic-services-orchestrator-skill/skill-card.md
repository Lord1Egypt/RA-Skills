## Description: <br>
Coordinate schema-driven workflows across configurable domains using workflow definitions, adapters, active tracks, artifact versions, approval/risk triage, event logs, validation, and recovery actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[completetech](https://clawhub.ai/user/completetech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and service teams use this skill to coordinate multi-stage workflow state, routing, approvals, handoffs, blockers, event logs, and recovery paths across configurable workflow domains. It is most useful when work spans multiple specialists, artifacts, owners, or approval gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate commercial, legal, billing, external-send, public-proof, production-launch, or credential-sensitive workflow decisions. <br>
Mitigation: Review and record the relevant approval gate before allowing those actions to move beyond draft or planning status. <br>
Risk: Generated workflow or document artifacts can become misleading if required facts, approvers, owners, or artifact versions are missing or stale. <br>
Mitigation: Use the bundled state validation, event logging, blocker tracking, and recovery guidance before treating an artifact as current or approved. <br>
Risk: The optional renderer writes PDF, PNG, or Markdown files to user-selected paths. <br>
Mitigation: Run the renderer only when explicitly requested and confirm output paths before generation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/completetech/agentic-services-orchestrator-skill) <br>
- [Project Homepage](https://github.com/CompleteTech-LLC/agentic-services-orchestrator-skill) <br>
- [Workflow Definition Schema](references/workflow-definition-schema.yaml) <br>
- [CompleteTech Services Workflow](references/completetech-services-workflow.yaml) <br>
- [Hiring Pipeline Workflow](references/hiring-pipeline-workflow.yaml) <br>
- [Orchestration Architecture](references/orchestration-architecture.md) <br>
- [Full Workflow Variables](references/full-workflow-variables.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, shell commands] <br>
**Output Format:** [Markdown guidance, YAML workflow state, and optional local PDF/PNG/Markdown artifacts when the bundled renderer is explicitly run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-only workflow routing; writes only user-selected artifact paths when the document renderer is explicitly invoked.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
