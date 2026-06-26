## Description: <br>
Find Everything helps an agent search across skills, MCP servers, prompt templates, and open-source projects from multiple registries and discovery sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZadAnthony](https://clawhub.ai/user/ZadAnthony) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to locate relevant skills, MCP servers, prompt templates, or repositories, compare results, and decide what to inspect or install next. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shell-based searches can be affected by untrusted or shell-special search text. <br>
Mitigation: Use explicit invocation, keep search terms plain, and review any generated command before execution. <br>
Risk: The skill can guide installation of discovered resources. <br>
Mitigation: Manually confirm each install and review source, metadata, and security scan results before approving. <br>
Risk: The skill can propose persistent additions to its source registry. <br>
Mitigation: Approve registry changes only for sources you trust and can review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ZadAnthony/find-everything) <br>
- [Publisher Profile](https://clawhub.ai/user/ZadAnthony) <br>
- [Source Registry](references/registry.json) <br>
- [Security Checklist](references/security-checklist.md) <br>
- [Known Skills List](references/known_skills.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown recommendations with source, relevance, safety, and next-action notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include skipped source notes, install hints, and risk labels for search results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
