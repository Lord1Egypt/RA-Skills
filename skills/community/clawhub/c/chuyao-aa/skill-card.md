## Description: <br>
Helps developers wrap MTL open platform APIs as Spring Boot HTTP endpoints by adding the MTL SDK dependency, configuring an ApiClient bean, creating a REST controller, and generating GET or POST handler code from native API definitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when integrating with MTL open platform APIs in Spring Boot projects and need consistent generated wrapper endpoints, dependency setup, client configuration, and optional logging hooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated code can place client identifiers, tokens, or other credentials into project files. <br>
Mitigation: Keep clientIdentifier and token values out of committed source code and review generated diffs before use. <br>
Risk: Optional request and response logging may capture business data, identifiers, or secrets. <br>
Mitigation: Enable logging only when needed and treat captured request and response payloads as sensitive data. <br>
Risk: Generated API wrappers may not match the intended native MTL API behavior if the supplied interface definition is incomplete or wrong. <br>
Mitigation: Confirm the native path, method, query parameters, request body, and description with the user before generating handlers. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/chuyao-aa) <br>
- [MTL Open API Endpoint](https://open.mtl4.alibaba-inc.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Java, XML, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-specific implementation guidance and generated Spring Boot wrapper code for user-provided MTL API definitions.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
