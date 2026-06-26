## Description: <br>
AI Labs Builder creates modern websites, AI applications, dashboards, and automated workflows with Next.js, TypeScript, Tailwind, shadcn/ui, and MCP integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slemo54](https://clawhub.ai/user/slemo54) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and builders use this skill to generate scaffolding, commands, and configuration for websites, AI apps, dashboards, and workflow automation projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator writes project files and runs npm/npx tooling. <br>
Mitigation: Use an explicit empty project directory and review generated code before deployment. <br>
Risk: Generated workflow projects can expose webhook handling without authentication or signature checks. <br>
Mitigation: Add authentication and signature verification before exposing any generated webhook server. <br>
Risk: Generated AI apps may process provider credentials, prompts, or user data. <br>
Mitigation: Keep API keys in environment variables and avoid entering sensitive data until privacy and provider handling are reviewed. <br>
Risk: Broad invocation triggers can match general project creation requests. <br>
Mitigation: Confirm the intended project type and destination before running project generation commands. <br>


## Reference(s): <br>
- [Next.js Documentation](https://nextjs.org/docs) <br>
- [Tailwind CSS Documentation](https://tailwindcss.com/docs) <br>
- [shadcn/ui](https://ui.shadcn.com) <br>
- [OpenAI API Documentation](https://platform.openai.com/docs) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, generated code snippets, and project scaffolding instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate project files and run npm/npx tooling through bundled shell scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
