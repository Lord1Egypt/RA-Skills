## Description: <br>
Helps agents plan or review a frontend testing strategy by mapping project risks to appropriate test layers, coverage priorities, commands, and file scopes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bovinphang](https://clawhub.ai/user/bovinphang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill when deciding how to distribute frontend quality coverage across static checks, unit tests, component tests, integration tests, E2E tests, visual regression, accessibility, security, performance, and CI gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recommend test commands, CI gates, or file changes that are too broad for a repository's actual risk profile. <br>
Mitigation: Review proposed coverage against existing project conventions, business-critical paths, and maintenance capacity before adding tools or gates. <br>
Risk: A testing plan may overemphasize one layer, such as E2E or component tests, and miss cheaper or more reliable coverage. <br>
Mitigation: Check that each recommendation is tied to a concrete risk and that faster layers are preferred for pure logic and stable component behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bovinphang/fec-testing-strategy) <br>
- [Publisher profile](https://clawhub.ai/user/bovinphang) <br>
- [Package homepage](https://github.com/bovinphang/frontend-craft) <br>
- [Package repository](https://github.com/bovinphang/frontend-craft) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with prioritized testing plans, risk-to-layer mappings, suggested commands, and file-scope recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May identify follow-on specialty review areas such as accessibility, security, performance, E2E, or component testing.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release evidence, artifact metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
