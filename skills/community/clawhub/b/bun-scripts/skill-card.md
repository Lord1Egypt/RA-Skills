## Description: <br>
Helps agents create, run, test, and manage TypeScript and JavaScript scripts with Bun instead of plain Node.js, npm, npx, Jest, or Vitest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bcanfield](https://clawhub.ai/user/bcanfield) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to prefer Bun for local TypeScript and JavaScript scripting, package management, testing, file I/O, shell commands, HTTP servers, and SQLite-backed utilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-proposed Bun commands can install packages, run shell commands, start local servers, fetch network resources, or read project data. <br>
Mitigation: Review commands before execution in sensitive repositories, especially package installs, server startup, network fetches, and scripts that may read .env files or local data. <br>
Risk: Bun executes TypeScript after stripping types, so type errors do not stop runtime execution. <br>
Mitigation: Use a separate type-checking step such as tsc --noEmit when type correctness matters. <br>


## Reference(s): <br>
- [Bun API Reference](references/REFERENCE.md) <br>
- [Bun LLM Documentation Index](https://bun.sh/llms.txt) <br>
- [Bun LLM Full Documentation](https://bun.sh/llms-full.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/bcanfield/bun-scripts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline TypeScript, JavaScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the bun executable for commands the agent proposes or runs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
