## Description: <br>
Manage AI agent skills using the @tiktok-fe/skills CLI (binary: ai-skills) for finding, installing, removing, updating, publishing, listing, and managing skills across coding agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nanki-nn](https://clawhub.ai/user/Nanki-nn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent operators use this skill to get concise, non-interactive command guidance for the ai-skills CLI when managing skills across tools such as Cursor, Claude Code, GitHub Copilot, Windsurf, Codex, and Gemini CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage automated installs, updates, removals, publishing, unpublishing, and cleanup actions that affect multiple AI agent tool directories. <br>
Mitigation: Review the exact target, scope, agent list, and command before allowing -y or --force, especially for remove, clean, update, publish, unpublish, or overwrite actions. <br>
Risk: The skill depends on guidance for the @tiktok-fe/skills npm package and the skill sources it installs from. <br>
Mitigation: Use the skill only when the package and requested source are trusted; prefer project scope, specify exact agents with --agents, and run list or --list checks before applying changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Nanki-nn/323) <br>
- [CLI Overview](artifact/llms/cli-overview.txt) <br>
- [AI Best Practices](artifact/llms/guides/ai-best-practices.txt) <br>
- [Skill Format Guide](artifact/llms/guides/skill-format.txt) <br>
- [Source Platforms Guide](artifact/llms/guides/source-platforms.txt) <br>
- [Supported Agents Guide](artifact/llms/guides/agents-list.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emphasizes pure-mode CLI usage, explicit scope flags, and confirmation flags for non-interactive agent workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
