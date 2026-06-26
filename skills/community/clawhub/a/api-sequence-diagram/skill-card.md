## Description: <br>
Analyzes a specified Java API endpoint or service method, traces the call chain, and produces a Mermaid sequence diagram with key decisions, exception branches, and business-logic notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijie012](https://clawhub.ai/user/lijie012) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Java Controller, Service, Mapper, SQL, and integration paths for an API and turn that understanding into a reviewable sequence diagram and call-chain summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires the agent to read application source code, mapper XML, SQL, and related call-chain files, which may expose sensitive implementation details. <br>
Mitigation: Use it only in repositories where that source access is acceptable, and review generated diagrams and business-logic summaries before sharing or treating them as authoritative. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lijie012/api-sequence-diagram) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with Mermaid sequenceDiagram code blocks and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes endpoint overview, key decision table, layered call-chain details, and optional notes on transactions, exceptions, performance, and external dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
