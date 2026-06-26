## Description: <br>
Provides a tool-agnostic methodology for using AI coding assistants through tool selection, context engineering, prompt templates, workflow patterns, verification checklists, and team adoption guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to choose AI coding tools, structure prompts and project rules, verify AI-generated code, manage costs, and roll out AI-assisted development practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated project rule files or prompt-library files can shape future agent behavior in a repository. <br>
Mitigation: Review generated .cursorrules, CLAUDE.md, AGENTS.md, .windsurfrules, .aider.conf.yml, and prompt-library files before committing or deploying them. <br>
Risk: AI coding guidance can lead to incorrect code or weak verification if applied without human review. <br>
Mitigation: Use the skill's review, testing, and security checklists before accepting AI-generated changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1kalin/afrexai-ai-coding-toolkit) <br>
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with tables, checklists, templates, and inline code or shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate project rule files, prompt-library templates, review checklists, tool comparisons, rollout plans, or cost-optimization recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
