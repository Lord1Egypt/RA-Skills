## Description: <br>
Use when configuring Maven plugins, setting up common plugins like compiler, surefire, jar, or creating custom plugin executions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and build engineers use this skill to configure Maven build, testing, packaging, release, quality, and code-generation plugins. It provides reusable Maven XML examples, command examples, and best-practice guidance for POM plugin configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copyable Maven command examples can rewrite project version files or alter dependency and plugin versions. <br>
Mitigation: Apply suggestions on a clean branch and review generated POM and version-control diffs before committing or running in CI. <br>
Risk: The exec-maven-plugin example can make future builds run a shell script. <br>
Mitigation: Use the bash execution example only when the referenced script is trusted and intentionally allowed in local and CI builds. <br>


## Reference(s): <br>
- [Oracle Java SE 17 API documentation](https://docs.oracle.com/en/java/javase/17/docs/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Maven XML and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
