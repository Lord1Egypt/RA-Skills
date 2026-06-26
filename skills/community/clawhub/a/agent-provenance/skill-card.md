## Description: <br>
File provenance tracking, authority levels, commit conventions, and governance policies for accountable agent-maintained instruction, topic, contact, and memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richgoodson](https://clawhub.ai/user/richgoodson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep agent-authored workspace memory and instruction changes reviewable through provenance headers, authority levels, review cadences, and git commit conventions. It is suited to OpenClaw workspaces where agents maintain files such as AGENTS.md, MEMORY.md, topic files, and contact notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to maintain provenance headers, schedule OpenClaw cron checks, and commit changes to instruction and memory files. <br>
Mitigation: Install only in workspaces where that behavior is acceptable, review git history and diff reports, and keep human review dates current. <br>
Risk: Provenance headers, contact notes, and commit messages could accidentally include sensitive values if users or agents record too much detail. <br>
Mitigation: Record the existence and storage location of credentials, not secret values, and keep secrets out of headers, notes, and commit messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richgoodson/agent-provenance) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/richgoodson) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with provenance header templates, review prompts, commit-message conventions, and OpenClaw cron/check instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw and git in the workspace; no API keys or external channel credentials are required by default.] <br>

## Skill Version(s): <br>
2.1.4 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
