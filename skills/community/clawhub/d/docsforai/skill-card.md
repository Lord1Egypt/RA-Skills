## Description: <br>
Crawl and read documentation websites using DocsForAI for library, framework, SDK, API, and tool documentation lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dx2331lxz](https://clawhub.ai/user/dx2331lxz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to crawl requested documentation sites into local Markdown and read only the relevant sections before writing, debugging, configuring, or upgrading code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches documentation websites requested by the user and stores downloaded content locally. <br>
Mitigation: Use it only for documentation sites you intend the agent to access, and review the persistent docs directory when local retention matters. <br>
Risk: The fallback pip install command can modify the system Python environment. <br>
Mitigation: Prefer the uv install path and use the pip fallback only when system Python impact is understood. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dx2331lxz/docsforai) <br>
- [DocsForAI PyPI Package](https://pypi.org/project/docsforai/) <br>
- [DocsForAI GitHub Project](https://github.com/dx2331lxz/DocsForAI) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent local Markdown documentation folders and MEMORY.md entries for crawled sites.] <br>

## Skill Version(s): <br>
0.7.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
