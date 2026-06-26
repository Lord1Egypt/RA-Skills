## Description: <br>
Analyzes Java microservice Controller call chains, traces calls through Service, Mapper, and Repository layers, extracts SQL, and writes a structured JSON report for documentation, audit, and architecture review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[14686039](https://clawhub.ai/user/14686039) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, API documentation maintainers, code auditors, and architecture reviewers use this skill to inspect how a Java Spring Controller reaches business logic and database access. It is useful for generating call-chain reports, reviewing SQL usage, and understanding module implementation details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may contain internal API paths, business logic, database access patterns, and SQL statements. <br>
Mitigation: Write reports only to trusted project locations and apply normal repository or document access controls before sharing them. <br>
Risk: Analysis depends on common Spring Boot, MyBatis, and Spring Data JPA conventions, so unusual project structure or dynamic wiring may produce incomplete call chains. <br>
Mitigation: Review the generated JSON against the source code before using it for audits, API documentation, or architecture decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/14686039/controller-call-chain-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Files, JSON] <br>
**Output Format:** [Structured JSON report written to a local file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The output file is named after the analyzed Controller class and is written to the configured output directory, defaulting to docs/api_analysis/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
