## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baikaishuixyz](https://clawhub.ai/user/baikaishuixyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to drive deterministic headless browser workflows, including navigation, element interaction, snapshot parsing, session isolation, and browser state reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved authentication state, cookies, and storage values can expose account access if shared, committed, or reused carelessly. <br>
Mitigation: Use test or least-privilege accounts where possible, keep saved state files out of shared folders and repositories, treat them like passwords, and delete them after use. <br>
Risk: Agent-controlled browser automation can perform purchases, account changes, public posts, or other irreversible actions. <br>
Mitigation: Require explicit confirmation before any irreversible action and review browser steps before executing workflows on sensitive accounts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/baikaishuixyz/agent-browser-clawdbot-custom) <br>
- [agent-browser project homepage](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command-oriented browser automation guidance; the external CLI can also produce JSON snapshots, screenshots, PDFs, and saved browser state files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
