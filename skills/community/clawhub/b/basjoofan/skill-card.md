## Description: <br>
Easy Run Test helps agents run basjoofan API, performance, load, stress, and HTTP tests from .fan test scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lamb](https://clawhub.ai/user/lamb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to generate and run basjoofan commands for API checks and controlled performance, load, stress, and HTTP testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API, load, stress, or performance tests can disrupt systems when run against unauthorized targets or with excessive load settings. <br>
Mitigation: Use the skill only against systems you own or have explicit permission to test, and keep concurrency, duration, and run counts within approved limits. <br>
Risk: Request bodies, tokens, customer data, or multipart upload examples can expose sensitive information during test execution. <br>
Mitigation: Use non-sensitive test data and do not include secrets, tokens, private customer data, or sensitive local files in generated requests. <br>
Risk: The skill installs and runs a basjoofan binary from a GitHub release source. <br>
Mitigation: Install only when you trust the basjoofan GitHub release source and review the release source before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lamb/basjoofan) <br>
- [Publisher profile](https://clawhub.ai/user/lamb) <br>
- [Basjoofan GitHub releases API](https://api.github.com/repos/basjoofan/core/releases/latest) <br>
- [Basjoofan binary release download pattern](https://github.com/basjoofan/core/releases/download/v${VERSION}/basjoofan-${VERSION}-${ARCH}-${OS}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash and basjoofan script examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include basjoofan CLI options for concurrency, duration, run count, script path, result recording, and statistics output.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
