## Description: <br>
Automatically discovers local CLAUDE.md guidance files from the current project and nearby parent directories for use by an agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaoxiang616](https://clawhub.ai/user/shaoxiang616) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to surface project-specific CLAUDE.md instructions from a workspace so the agent can follow local guidance while working in that project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically load local CLAUDE.md files into high-priority agent context without a clear confirmation step. <br>
Mitigation: Install only in trusted workspaces and inspect nearby CLAUDE.md files before allowing their contents to guide agent behavior. <br>
Risk: A leading-space file named ' CLAUDE.md' may be discovered alongside the standard CLAUDE.md name. <br>
Mitigation: Check for both CLAUDE.md and ' CLAUDE.md' in the current project and parent directories before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaoxiang616/claude-md-auto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown content assembled from discovered CLAUDE.md files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits combined output to 40,000 characters and searches the current directory plus parent directories up to four levels.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
