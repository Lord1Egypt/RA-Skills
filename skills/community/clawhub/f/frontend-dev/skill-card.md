## Description: <br>
Generate production-ready Next.js projects with TypeScript, Tailwind CSS, shadcn/ui, and API integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wing8169](https://clawhub.ai/user/wing8169) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold and extend Next.js frontends, including project structure, UI components, API integration, local preview, and deployment guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage local development servers and may suggest broad PM2 commands. <br>
Mitigation: Review process-management commands before execution and avoid unscoped delete-all or kill commands. <br>
Risk: Optional live-preview setup may expose local work through Nginx or require sudo-level changes. <br>
Mitigation: Keep previews localhost-only by default and review any Nginx or sudo command before allowing it. <br>
Risk: Generated environment files or screenshots could include credentials or sensitive configuration. <br>
Mitigation: Use placeholder values for generated .env files and do not commit, zip, screenshot, or share real credentials. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local development server, PM2, Chromium screenshot, and Nginx preview commands for user review.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
