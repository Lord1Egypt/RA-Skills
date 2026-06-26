## Description: <br>
Generates API test design matrices from OpenAPI and Swagger specifications by combining scripted constraint extraction with AI review of natural-language descriptions for normal, error, boundary, relationship, authentication, pagination, CRUD, and response-assertion coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujianyeey-oss](https://clawhub.ai/user/liujianyeey-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to turn OpenAPI or Swagger API specifications into structured test case matrices, generated Markdown reports, optional YAML test configuration, and AI-reviewed coverage guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenAPI or Swagger files, which may contain sensitive API descriptions. <br>
Mitigation: Use it only on specifications that are acceptable in the agent workflow and direct generated files to a dedicated output directory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liujianyeey-oss/api-case-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, YAML configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, YAML test configuration, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenAPI or Swagger files and writes generated case files to a selected output directory.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
