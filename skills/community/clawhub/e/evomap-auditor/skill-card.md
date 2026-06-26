## Description: <br>
Performs security scans on third-party skills, validates asset hashes, and supports sandboxed zero-trust execution workflows within the EvoMap ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcusqin111-boop](https://clawhub.ai/user/marcusqin111-boop) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to inspect EvoMap or GEP-A2A skills before inheritance or execution, validate canonical asset hashes, and plan zero-trust controls for untrusted capsules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes sandbox execution patterns but does not itself provide an enforced sandbox. <br>
Mitigation: Use it only with an environment that already enforces filesystem controls, network allowlisting, and logging before executing untrusted skills. <br>


## Reference(s): <br>
- [GEP-A2A Protocol](https://evomap.ai/docs/gep) <br>
- [EvoMap Security Standards](https://evomap.ai/security) <br>
- [ClawHub Skill Page](https://clawhub.ai/marcusqin111-boop/evomap-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with optional command and JavaScript helper usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include audit findings, hash-validation steps, and sandbox-control recommendations.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
