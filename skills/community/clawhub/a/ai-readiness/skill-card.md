## Description: <br>
Generates a complete set of AI readiness files for any website from a single command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[russwittmann](https://clawhub.ai/user/russwittmann) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and marketing teams use this skill to research a website and generate deployable AI-readiness files such as ai.txt, llms.txt, schema, RAG indexes, and deployment guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated website claims, URLs, crawler rules, policy text, schema, or AI-readiness files may be inaccurate if the research results are stale, incomplete, or misinterpreted. <br>
Mitigation: Review every generated file before publishing, with particular attention to robots.txt, policy text, schema, and claims derived from web research. <br>
Risk: The skill creates deployable files in the workspace that may affect how AI systems and crawlers interpret a website if published without review. <br>
Mitigation: Publish only after confirming the generated files match the site's intended crawler permissions, training-data policy, brand facts, and deployment location. <br>


## Reference(s): <br>
- [AI Readiness File Specifications](references/file-specs.md) <br>
- [AI Readiness documentation](https://ai.silverbackmarketing.com) <br>
- [@silverbackmarketing/ai-readiness npm package](https://www.npmjs.com/package/@silverbackmarketing/ai-readiness) <br>
- [llms.txt standard](https://llmstxt.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [A workspace folder containing text, Markdown, JSON, JSONL, XML, and configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an 18-file AI-readiness set for the target domain, including ai.txt, llms.txt, llms-full.txt, ai-sitemap.xml, schema files, RAG indexes, policy text, a deployment checklist, README, and robots.txt.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
