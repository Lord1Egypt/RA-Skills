## Description: <br>
C Language Support Library for OpenClaw skills. Provides AST parsing, CMake analysis, Unity test generation, and security rule checking for C projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as a shared C-language support library for parsing C source, analyzing CMake projects, generating Unity test scaffolding, and checking common C security rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michealxie001/c-support) <br>
- [Publisher profile](https://clawhub.ai/user/michealxie001) <br>
- [CWE-120: Buffer Copy without Checking Size of Input](https://cwe.mitre.org/data/definitions/120.html) <br>
- [CWE-134: Use of Externally-Controlled Format String](https://cwe.mitre.org/data/definitions/134.html) <br>
- [CWE-242: Use of Inherently Dangerous Function](https://cwe.mitre.org/data/definitions/242.html) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Python APIs that return structured analysis objects, findings, and generated C test code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python dependencies from requirements.txt; security evidence notes low dependency reproducibility risk and recommends sandboxing or pinned dependencies for stricter environments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
